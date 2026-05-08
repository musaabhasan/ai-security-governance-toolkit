from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


OPEN_STATUSES = {"open", "approved", "active", "extended", "pending_review"}
CLOSED_STATUSES = {"closed", "resolved", "retired", "cancelled", "canceled", "rejected"}
REQUIRED_COLUMNS = [
    "exception_id",
    "system",
    "control_reference",
    "exception_description",
    "risk_owner",
    "approved_by",
    "approval_date",
    "expiration_date",
    "compensating_control",
    "status",
    "review_notes",
]


@dataclass(frozen=True)
class ExceptionRecord:
    exception_id: str
    system: str
    control_reference: str
    risk_owner: str
    status: str
    expiration_date: str
    days_to_expiration: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an aging report for AI governance exceptions.",
    )
    parser.add_argument("input", type=Path, help="Path to an AI exception register CSV file.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument("--warning-days", type=int, default=30, help="Days before expiration to flag as expiring soon.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", type=Path, help="Optional output path. Defaults to stdout.")
    parser.add_argument(
        "--fail-on-expired",
        action="store_true",
        help="Exit with code 1 when an open exception is expired or missing an expiration date.",
    )
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


def classify_record(row: dict[str, str], as_of: date, warning_days: int) -> ExceptionRecord:
    status = row["status"].strip().lower()
    expiration = row["expiration_date"].strip()
    is_closed = status in CLOSED_STATUSES

    if not expiration:
        return ExceptionRecord(
            exception_id=row["exception_id"],
            system=row["system"],
            control_reference=row["control_reference"],
            risk_owner=row["risk_owner"],
            status=row["status"],
            expiration_date="",
            days_to_expiration=None,
            state="closed_without_expiration" if is_closed else "missing_expiration",
            severity="info" if is_closed else "high",
            action="No action required for closed exception." if is_closed else "Add an expiration date and reapprove.",
        )

    expiration_date = parse_iso_date(expiration, f"{row['exception_id']} expiration_date")
    days_to_expiration = (expiration_date - as_of).days

    if is_closed:
        state = "closed"
        severity = "info"
        action = "No action required unless evidence retention is incomplete."
    elif days_to_expiration < 0:
        state = "expired"
        severity = "high"
        action = "Escalate for closure, reapproval, or compensating-control review."
    elif days_to_expiration <= warning_days:
        state = "expiring_soon"
        severity = "medium"
        action = "Schedule risk-owner review before the exception expires."
    elif status and status not in OPEN_STATUSES:
        state = "unknown_status"
        severity = "medium"
        action = "Normalize status and confirm whether the exception remains active."
    else:
        state = "active"
        severity = "low"
        action = "Track through the normal review cadence."

    return ExceptionRecord(
        exception_id=row["exception_id"],
        system=row["system"],
        control_reference=row["control_reference"],
        risk_owner=row["risk_owner"],
        status=row["status"],
        expiration_date=expiration,
        days_to_expiration=days_to_expiration,
        state=state,
        severity=severity,
        action=action,
    )


def build_report(rows: Iterable[dict[str, str]], as_of: date, warning_days: int) -> list[ExceptionRecord]:
    return [classify_record(row, as_of, warning_days) for row in rows]


def summarize(records: list[ExceptionRecord]) -> dict[str, int]:
    counts = Counter(record.state for record in records)
    return {
        "total": len(records),
        "expired": counts["expired"],
        "expiring_soon": counts["expiring_soon"],
        "missing_expiration": counts["missing_expiration"],
        "unknown_status": counts["unknown_status"],
        "active": counts["active"],
        "closed": counts["closed"] + counts["closed_without_expiration"],
    }


def render_markdown(records: list[ExceptionRecord], as_of: date, warning_days: int) -> str:
    summary = summarize(records)
    lines = [
        "# AI Exception Aging Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Warning window: `{warning_days}` days",
        f"- Total exceptions: `{summary['total']}`",
        f"- Expired: `{summary['expired']}`",
        f"- Expiring soon: `{summary['expiring_soon']}`",
        f"- Missing expiration: `{summary['missing_expiration']}`",
        f"- Unknown status: `{summary['unknown_status']}`",
        f"- Active: `{summary['active']}`",
        f"- Closed: `{summary['closed']}`",
        "",
        "## Exception Review Queue",
        "",
        "| Exception | System | Control | Owner | Status | Expiration | Days | State | Severity | Action |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for record in sorted(records, key=sort_key):
        days = "" if record.days_to_expiration is None else str(record.days_to_expiration)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.exception_id),
                    escape_pipe(record.system),
                    escape_pipe(record.control_reference),
                    escape_pipe(record.risk_owner),
                    escape_pipe(record.status),
                    escape_pipe(record.expiration_date),
                    days,
                    record.state,
                    record.severity,
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def sort_key(record: ExceptionRecord) -> tuple[int, int, str]:
    state_order = {
        "expired": 0,
        "missing_expiration": 1,
        "expiring_soon": 2,
        "unknown_status": 3,
        "active": 4,
        "closed_without_expiration": 5,
        "closed": 6,
    }
    days = record.days_to_expiration if record.days_to_expiration is not None else -9999
    return (state_order.get(record.state, 9), days, record.exception_id)


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|")


def render_json(records: list[ExceptionRecord], as_of: date, warning_days: int) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "warning_days": warning_days,
        "summary": summarize(records),
        "exceptions": [asdict(record) for record in sorted(records, key=sort_key)],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


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
        if args.warning_days < 0:
            raise ValueError("--warning-days must be zero or greater")
        records = build_report(load_rows(args.input), as_of, args.warning_days)
        content = (
            render_markdown(records, as_of, args.warning_days)
            if args.format == "markdown"
            else render_json(records, as_of, args.warning_days)
        )
        write_output(content, args.output)
        if args.fail_on_expired and any(record.state in {"expired", "missing_expiration"} for record in records):
            return 1
        return 0
    except ValueError as exc:
        print(f"exception aging report failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
