from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = [
    "risk_id",
    "use_case",
    "risk_statement",
    "risk_theme",
    "owner",
    "inherent_likelihood",
    "inherent_impact",
    "inherent_rating",
    "controls",
    "residual_likelihood",
    "residual_impact",
    "residual_rating",
    "decision",
    "status",
    "review_date",
]
RATING_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}
CLOSED_STATUSES = {"closed", "retired", "resolved", "accepted-closed", "cancelled", "canceled"}


@dataclass(frozen=True)
class RiskRecord:
    risk_id: str
    use_case: str
    risk_theme: str
    owner: str
    inherent_rating: str
    residual_rating: str
    decision: str
    status: str
    review_date: str
    days_to_review: int | None
    review_state: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI risk-register summary report.")
    parser.add_argument("input", type=Path, help="Path to an AI risk register CSV file.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument(
        "--review-warning-days",
        type=int,
        default=30,
        help="Days before review date to flag an open risk as due soon.",
    )
    parser.add_argument(
        "--fail-on-residual",
        choices=("none", "low", "medium", "high", "critical"),
        default="none",
        help="Exit with code 1 when an open risk has residual rating at or above this threshold.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", type=Path, help="Optional output path. Defaults to stdout.")
    return parser.parse_args(argv)


def parse_iso_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD: {value}") from exc


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} is empty")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def build_report(rows: Iterable[dict[str, str]], as_of: date, warning_days: int) -> list[RiskRecord]:
    return [classify_risk(row, as_of, warning_days) for row in rows]


def classify_risk(row: dict[str, str], as_of: date, warning_days: int) -> RiskRecord:
    status = row["status"].strip().lower()
    review_date_text = row["review_date"].strip()
    is_closed = status in CLOSED_STATUSES

    if not review_date_text:
        days_to_review = None
        review_state = "closed_without_review_date" if is_closed else "missing_review_date"
        action = "Confirm closure evidence retention." if is_closed else "Add review date and assign an owner review."
    else:
        review_date = parse_iso_date(review_date_text, f"{row['risk_id']} review_date")
        days_to_review = (review_date - as_of).days
        if is_closed:
            review_state = "closed"
            action = "Confirm closure evidence retention."
        elif days_to_review < 0:
            review_state = "overdue_review"
            action = "Escalate overdue risk review to the owner."
        elif days_to_review <= warning_days:
            review_state = "due_soon"
            action = "Schedule review before the due date."
        else:
            review_state = "current"
            action = "Track through the normal review cadence."

    return RiskRecord(
        risk_id=row["risk_id"],
        use_case=row["use_case"],
        risk_theme=row["risk_theme"],
        owner=row["owner"],
        inherent_rating=row["inherent_rating"],
        residual_rating=row["residual_rating"],
        decision=row["decision"],
        status=row["status"],
        review_date=review_date_text,
        days_to_review=days_to_review,
        review_state=review_state,
        action=action,
    )


def summarize(records: list[RiskRecord]) -> dict[str, object]:
    residual_counts = Counter(normalize_rating(record.residual_rating) for record in records)
    review_counts = Counter(record.review_state for record in records)
    return {
        "total": len(records),
        "residual": {rating: residual_counts[rating] for rating in ("critical", "high", "medium", "low", "unknown")},
        "review": dict(sorted(review_counts.items())),
        "open_high_or_above": sum(
            1 for record in records if is_open(record) and rating_value(record.residual_rating) >= RATING_ORDER["high"]
        ),
        "overdue_reviews": review_counts["overdue_review"],
        "due_soon": review_counts["due_soon"],
    }


def render_markdown(records: list[RiskRecord], as_of: date, warning_days: int) -> str:
    summary = summarize(records)
    lines = [
        "# AI Risk Register Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Review warning window: `{warning_days}` days",
        f"- Total risks: `{summary['total']}`",
        f"- Open high-or-above residual risks: `{summary['open_high_or_above']}`",
        f"- Overdue reviews: `{summary['overdue_reviews']}`",
        f"- Reviews due soon: `{summary['due_soon']}`",
        "",
        "## Residual Risk by Theme",
        "",
        "| Theme | Critical | High | Medium | Low | Unknown |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for theme, counts in theme_summary(records).items():
        lines.append(
            "| {theme} | {critical} | {high} | {medium} | {low} | {unknown} |".format(
                theme=escape_pipe(theme),
                critical=counts["critical"],
                high=counts["high"],
                medium=counts["medium"],
                low=counts["low"],
                unknown=counts["unknown"],
            )
        )

    lines.extend(
        [
            "",
            "## Owner Review Queue",
            "",
            "| Owner | Risks | Max Residual | Overdue | Due Soon | Action |",
            "| --- | ---: | --- | ---: | ---: | --- |",
        ]
    )
    for owner, owner_records in owner_summary(records):
        max_residual = max_rating(record.residual_rating for record in owner_records)
        overdue = sum(1 for record in owner_records if record.review_state == "overdue_review")
        due_soon = sum(1 for record in owner_records if record.review_state == "due_soon")
        lines.append(
            "| {owner} | {risks} | {max_residual} | {overdue} | {due_soon} | {action} |".format(
                owner=escape_pipe(owner),
                risks=len(owner_records),
                max_residual=max_residual,
                overdue=overdue,
                due_soon=due_soon,
                action=escape_pipe(owner_action(owner_records)),
            )
        )

    lines.extend(
        [
            "",
            "## Risk Review Details",
            "",
            "| Risk | Use Case | Theme | Owner | Inherent | Residual | Decision | Status | Review Date | Days | Review State | Action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for record in sorted(records, key=sort_key):
        days = "" if record.days_to_review is None else str(record.days_to_review)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.risk_id),
                    escape_pipe(record.use_case),
                    escape_pipe(record.risk_theme),
                    escape_pipe(record.owner),
                    escape_pipe(record.inherent_rating),
                    escape_pipe(record.residual_rating),
                    escape_pipe(record.decision),
                    escape_pipe(record.status),
                    escape_pipe(record.review_date),
                    days,
                    record.review_state,
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def theme_summary(records: list[RiskRecord]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = defaultdict(lambda: {rating: 0 for rating in ("critical", "high", "medium", "low", "unknown")})
    for record in records:
        summary[record.risk_theme or "unassigned"][normalize_rating(record.residual_rating)] += 1
    return dict(sorted(summary.items(), key=lambda item: (-max(item[1].values()), item[0].lower())))


def owner_summary(records: list[RiskRecord]) -> list[tuple[str, list[RiskRecord]]]:
    grouped: dict[str, list[RiskRecord]] = defaultdict(list)
    for record in records:
        grouped[record.owner or "unassigned"].append(record)
    return sorted(grouped.items(), key=lambda item: (-max(rating_value(record.residual_rating) for record in item[1]), item[0].lower()))


def owner_action(records: list[RiskRecord]) -> str:
    if any(record.review_state == "overdue_review" for record in records):
        return "Escalate overdue review before the next governance forum."
    if any(rating_value(record.residual_rating) >= RATING_ORDER["high"] and is_open(record) for record in records):
        return "Review residual risk acceptance and control evidence."
    if any(record.review_state == "due_soon" for record in records):
        return "Prepare owner update for the upcoming review date."
    return "Track through the normal review cadence."


def render_json(records: list[RiskRecord], as_of: date, warning_days: int) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "review_warning_days": warning_days,
        "summary": summarize(records),
        "theme_summary": theme_summary(records),
        "risks": [asdict(record) for record in sorted(records, key=sort_key)],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def should_fail(records: list[RiskRecord], threshold: str) -> bool:
    if threshold == "none":
        return False
    required = RATING_ORDER[threshold]
    return any(is_open(record) and rating_value(record.residual_rating) >= required for record in records)


def is_open(record: RiskRecord) -> bool:
    return record.status.strip().lower() not in CLOSED_STATUSES


def sort_key(record: RiskRecord) -> tuple[int, int, str]:
    review_order = {
        "overdue_review": 0,
        "missing_review_date": 1,
        "due_soon": 2,
        "current": 3,
        "closed_without_review_date": 4,
        "closed": 5,
    }
    days = record.days_to_review if record.days_to_review is not None else -9999
    return (-rating_value(record.residual_rating), review_order.get(record.review_state, 9), days, record.risk_id)


def max_rating(values: Iterable[str]) -> str:
    normalized = [normalize_rating(value) for value in values]
    return max(normalized, key=lambda rating: RATING_ORDER.get(rating, 0), default="unknown")


def normalize_rating(value: str) -> str:
    rating = value.strip().lower()
    return rating if rating in RATING_ORDER else "unknown"


def rating_value(value: str) -> int:
    return RATING_ORDER.get(normalize_rating(value), 0)


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_output(content: str, output: Path | None) -> None:
    if output is None:
        print(content)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        as_of = parse_iso_date(args.as_of, "--as-of")
        if args.review_warning_days < 0:
            raise ValueError("--review-warning-days must be zero or greater")
        records = build_report(load_rows(args.input), as_of, args.review_warning_days)
        content = (
            render_markdown(records, as_of, args.review_warning_days)
            if args.format == "markdown"
            else render_json(records, as_of, args.review_warning_days)
        )
        write_output(content, args.output)
        return 1 if should_fail(records, args.fail_on_residual) else 0
    except ValueError as exc:
        print(f"risk register report failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
