from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "templates" / "evidence-register.csv"
REQUIRED_COLUMNS = [
    "evidence_id",
    "control_id",
    "evidence_name",
    "system",
    "owner",
    "source",
    "frequency",
    "last_collected",
    "next_due",
    "status",
    "notes",
]


def read_register(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(f"{path} has unexpected columns")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def review(rows: list[dict[str, str]], as_of: date) -> dict[str, object]:
    reviewed = [review_evidence(row, as_of) for row in rows]
    severity_counts = Counter(item["severity"] for item in reviewed)
    owner_queues: dict[str, list[str]] = defaultdict(list)
    control_coverage: Counter[str] = Counter()

    for item in reviewed:
        owner = item["owner"] or "unassigned"
        if item["severity"] in {"high", "medium"}:
            owner_queues[owner].append(item["evidence_id"])
        control_coverage[item["control_id"]] += 1

    return {
        "summary": {
            "evidence_items": len(reviewed),
            "high": severity_counts["high"],
            "medium": severity_counts["medium"],
            "low": severity_counts["low"],
            "control_coverage": dict(sorted(control_coverage.items())),
            "owner_queues": {owner: items for owner, items in sorted(owner_queues.items())},
        },
        "items": reviewed,
    }


def review_evidence(row: dict[str, str], as_of: date) -> dict[str, object]:
    flags: list[str] = []

    for column in ("evidence_id", "control_id", "evidence_name", "system", "owner", "source", "frequency"):
        if not row[column]:
            flags.append(f"{column} missing")

    status = row["status"].lower()
    if status not in {"current", "approved", "collected", "required", "pending", "expired"}:
        flags.append("status is not recognized")
    if status in {"required", "pending"}:
        flags.append("evidence is not yet collected")
    if status == "expired":
        flags.append("evidence is marked expired")

    last_collected = parse_date(row["last_collected"])
    next_due = parse_date(row["next_due"])
    if last_collected is None:
        flags.append("last_collected missing")
    if next_due is None:
        flags.append("next_due missing")
    elif next_due < as_of:
        flags.append("next_due is overdue")

    cadence_days = cadence_to_days(row["frequency"])
    if cadence_days is not None and last_collected is not None:
        age_days = (as_of - last_collected).days
        if age_days > cadence_days:
            flags.append(f"evidence age exceeds {row['frequency']} cadence")

    severity = severity_for(flags)
    return {
        "evidence_id": row["evidence_id"],
        "control_id": row["control_id"],
        "system": row["system"],
        "owner": row["owner"],
        "source": row["source"],
        "frequency": row["frequency"],
        "status": row["status"],
        "severity": severity,
        "flags": flags,
        "recommended_action": recommended_action(flags),
    }


def cadence_to_days(value: str) -> int | None:
    normalized = value.strip().lower()
    if normalized in {"per release", "per use case", "per major release"}:
        return None
    if normalized in {"monthly", "month"}:
        return 31
    if normalized in {"quarterly", "quarter"}:
        return 95
    if normalized in {"semiannual", "semi-annually", "semi-annually"}:
        return 190
    if normalized in {"annual", "annually", "yearly"}:
        return 370
    return None


def severity_for(flags: list[str]) -> str:
    if any("owner missing" in flag or "overdue" in flag or "expired" in flag for flag in flags):
        return "high"
    if any("missing" in flag or "not yet collected" in flag or "exceeds" in flag for flag in flags):
        return "medium"
    return "low"


def recommended_action(flags: list[str]) -> str:
    if any("owner missing" in flag for flag in flags):
        return "Assign evidence ownership before the control is presented for assurance review."
    if any("overdue" in flag or "expired" in flag for flag in flags):
        return "Collect or refresh evidence and record the next due date before release or audit submission."
    if any("last_collected missing" in flag or "next_due missing" in flag for flag in flags):
        return "Add collection and review dates so evidence freshness can be tested."
    if any("not yet collected" in flag for flag in flags):
        return "Collect the required artifact or link a formal exception before approval."
    if flags:
        return "Review the evidence record and resolve quality flags before relying on it."
    return "Evidence record is suitable for routine assurance review."


def parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def render_markdown(result: dict[str, object]) -> str:
    summary = result["summary"]
    assert isinstance(summary, dict)
    items = result["items"]
    assert isinstance(items, list)

    lines = [
        "# AI Evidence Quality Report",
        "",
        f"- Evidence items: `{summary['evidence_items']}`",
        f"- High-risk evidence gaps: `{summary['high']}`",
        f"- Medium-risk evidence gaps: `{summary['medium']}`",
        "",
        "## Owner Queue",
        "",
        "| Owner | Evidence items needing review |",
        "| --- | --- |",
    ]

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    if owner_queues:
        for owner, evidence_ids in owner_queues.items():
            assert isinstance(evidence_ids, list)
            lines.append(f"| {owner} | {'; '.join(evidence_ids)} |")
    else:
        lines.append("| none | none |")

    lines.extend([
        "",
        "## Evidence Findings",
        "",
        "| Evidence | Control | Owner | Severity | Flags | Recommended action |",
        "| --- | --- | --- | --- | --- | --- |",
    ])

    for item in items:
        assert isinstance(item, dict)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(str(item["evidence_id"])),
                    escape_cell(str(item["control_id"])),
                    escape_cell(str(item["owner"] or "unassigned")),
                    str(item["severity"]),
                    escape_cell("; ".join(item["flags"]) if item["flags"] else "none"),
                    escape_cell(str(item["recommended_action"])),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Review AI governance evidence quality and freshness.")
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-on-high", action="store_true")
    args = parser.parse_args()

    as_of = parse_date(args.as_of)
    if as_of is None:
        print("--as-of must use YYYY-MM-DD format", file=sys.stderr)
        return 2

    result = review(read_register(args.register), as_of)
    summary = result["summary"]
    assert isinstance(summary, dict)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render_markdown(result), end="")

    return 1 if args.fail_on_high and int(summary["high"]) > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
