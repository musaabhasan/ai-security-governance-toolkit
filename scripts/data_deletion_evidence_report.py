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
    "request_id",
    "system",
    "processor",
    "data_subject_or_dataset",
    "deletion_scope",
    "requested_at",
    "due_date",
    "completed_at",
    "evidence_reference",
    "verification_method",
    "verifier",
    "status",
    "retention_exception",
    "next_review_date",
    "notes",
]
COMPLETED_STATUSES = {"completed", "verified", "closed"}
OPEN_STATUSES = {"requested", "in_progress", "pending_vendor", "pending_verification"}
EXCEPTION_STATUSES = {"exception", "retained", "legal_hold", "blocked"}


@dataclass(frozen=True)
class DeletionEvidenceRecord:
    request_id: str
    system: str
    processor: str
    data_subject_or_dataset: str
    deletion_scope: str
    status: str
    due_date: str
    completed_at: str
    next_review_date: str
    days_to_due: int | None
    days_to_review: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI data deletion evidence report.")
    parser.add_argument("input", type=Path, help="Path to an AI data deletion evidence CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument(
        "--due-warning-days",
        type=int,
        default=14,
        help="Days before deletion due date to flag an open request as due soon.",
    )
    parser.add_argument(
        "--review-warning-days",
        type=int,
        default=30,
        help="Days before retention-exception review date to flag an exception as due soon.",
    )
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Exit with code 1 when high-severity deletion evidence gaps are present.",
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


def build_report(
    rows: Iterable[dict[str, str]],
    as_of: date,
    due_warning_days: int,
    review_warning_days: int,
) -> list[DeletionEvidenceRecord]:
    return [classify_record(row, as_of, due_warning_days, review_warning_days) for row in rows]


def classify_record(
    row: dict[str, str],
    as_of: date,
    due_warning_days: int,
    review_warning_days: int,
) -> DeletionEvidenceRecord:
    status = row["status"].strip().lower()
    due_date_text = row["due_date"].strip()
    completed_at_text = row["completed_at"].strip()
    next_review_text = row["next_review_date"].strip()
    evidence_reference = row["evidence_reference"].strip()
    verification_method = row["verification_method"].strip()
    verifier = row["verifier"].strip()
    retention_exception = row["retention_exception"].strip()

    due_date = parse_iso_date(due_date_text, f"{row['request_id']} due_date") if due_date_text else None
    completed_at = parse_iso_date(completed_at_text, f"{row['request_id']} completed_at") if completed_at_text else None
    next_review_date = (
        parse_iso_date(next_review_text, f"{row['request_id']} next_review_date") if next_review_text else None
    )

    days_to_due = (due_date - as_of).days if due_date is not None else None
    days_to_review = (next_review_date - as_of).days if next_review_date is not None else None

    if status in COMPLETED_STATUSES:
        if not evidence_reference:
            state = "missing_completion_evidence"
            severity = "high"
            action = "Attach deletion evidence from the processor or storage owner."
        elif not verification_method or not verifier:
            state = "unverified_completion"
            severity = "medium"
            action = "Record independent verification method and verifier."
        else:
            state = "verified"
            severity = "low"
            action = "Retain evidence through the approved retention period."
    elif status in EXCEPTION_STATUSES or retention_exception:
        if not retention_exception:
            state = "exception_without_reason"
            severity = "high"
            action = "Document the retention exception reason and approving owner."
        elif next_review_date is None:
            state = "exception_missing_review"
            severity = "high"
            action = "Add a review date for the retention exception."
        elif days_to_review is not None and days_to_review < 0:
            state = "exception_review_overdue"
            severity = "high"
            action = "Escalate overdue retention-exception review."
        elif days_to_review is not None and days_to_review <= review_warning_days:
            state = "exception_review_due_soon"
            severity = "medium"
            action = "Schedule retention-exception review before the due date."
        else:
            state = "retention_exception_active"
            severity = "medium"
            action = "Monitor retention exception until approved deletion or renewal."
    elif status in OPEN_STATUSES or not status:
        if due_date is None:
            state = "missing_due_date"
            severity = "high"
            action = "Add deletion due date and processor owner."
        elif days_to_due is not None and days_to_due < 0:
            state = "overdue_deletion"
            severity = "high"
            action = "Escalate overdue deletion to the system and processor owners."
        elif days_to_due is not None and days_to_due <= due_warning_days:
            state = "deletion_due_soon"
            severity = "medium"
            action = "Confirm processor execution path before due date."
        else:
            state = "open"
            severity = "low"
            action = "Track through the normal deletion workflow."
    else:
        state = "unknown_status"
        severity = "medium"
        action = "Normalize status and confirm deletion evidence requirements."

    return DeletionEvidenceRecord(
        request_id=row["request_id"],
        system=row["system"],
        processor=row["processor"],
        data_subject_or_dataset=row["data_subject_or_dataset"],
        deletion_scope=row["deletion_scope"],
        status=row["status"],
        due_date=due_date_text,
        completed_at=completed_at_text,
        next_review_date=next_review_text,
        days_to_due=days_to_due,
        days_to_review=days_to_review,
        state=state,
        severity=severity,
        action=action,
    )


def summarize(records: list[DeletionEvidenceRecord]) -> dict[str, object]:
    state_counts = Counter(record.state for record in records)
    severity_counts = Counter(record.severity for record in records)
    return {
        "total": len(records),
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
        "overdue_deletion": state_counts["overdue_deletion"],
        "missing_completion_evidence": state_counts["missing_completion_evidence"],
        "unverified_completion": state_counts["unverified_completion"],
        "retention_exceptions": sum(
            state_counts[state]
            for state in (
                "exception_without_reason",
                "exception_missing_review",
                "exception_review_overdue",
                "exception_review_due_soon",
                "retention_exception_active",
            )
        ),
        "verified": state_counts["verified"],
    }


def render_markdown(
    records: list[DeletionEvidenceRecord],
    as_of: date,
    due_warning_days: int,
    review_warning_days: int,
) -> str:
    summary = summarize(records)
    lines = [
        "# AI Data Deletion Evidence Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Deletion due warning window: `{due_warning_days}` days",
        f"- Retention-exception review warning window: `{review_warning_days}` days",
        f"- Total requests: `{summary['total']}`",
        f"- High-severity items: `{summary['high']}`",
        f"- Overdue deletions: `{summary['overdue_deletion']}`",
        f"- Missing completion evidence: `{summary['missing_completion_evidence']}`",
        f"- Unverified completions: `{summary['unverified_completion']}`",
        f"- Retention exceptions: `{summary['retention_exceptions']}`",
        f"- Verified completions: `{summary['verified']}`",
        "",
        "## Processor Queue",
        "",
        "| Processor | Requests | High | Medium | Overdue | Missing Evidence | Action |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for processor, processor_records in processor_summary(records):
        lines.append(
            "| {processor} | {requests} | {high} | {medium} | {overdue} | {missing} | {action} |".format(
                processor=escape_pipe(processor),
                requests=len(processor_records),
                high=sum(1 for record in processor_records if record.severity == "high"),
                medium=sum(1 for record in processor_records if record.severity == "medium"),
                overdue=sum(1 for record in processor_records if record.state == "overdue_deletion"),
                missing=sum(1 for record in processor_records if record.state == "missing_completion_evidence"),
                action=escape_pipe(processor_action(processor_records)),
            )
        )

    lines.extend(
        [
            "",
            "## Deletion Evidence Details",
            "",
            "| Request | System | Processor | Subject or Dataset | Scope | Status | Due | Completed | Review | State | Severity | Action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for record in sorted(records, key=sort_key):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.request_id),
                    escape_pipe(record.system),
                    escape_pipe(record.processor),
                    escape_pipe(record.data_subject_or_dataset),
                    escape_pipe(record.deletion_scope),
                    escape_pipe(record.status),
                    escape_pipe(record.due_date),
                    escape_pipe(record.completed_at),
                    escape_pipe(record.next_review_date),
                    record.state,
                    record.severity,
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def processor_summary(records: list[DeletionEvidenceRecord]) -> list[tuple[str, list[DeletionEvidenceRecord]]]:
    grouped: dict[str, list[DeletionEvidenceRecord]] = defaultdict(list)
    for record in records:
        grouped[record.processor or "unassigned"].append(record)
    return sorted(grouped.items(), key=lambda item: (-max(severity_value(record.severity) for record in item[1]), item[0].lower()))


def processor_action(records: list[DeletionEvidenceRecord]) -> str:
    if any(record.state == "overdue_deletion" for record in records):
        return "Escalate overdue deletion and request processor completion evidence."
    if any(record.state == "missing_completion_evidence" for record in records):
        return "Collect completion evidence before closing the request."
    if any(record.state.startswith("exception_") for record in records):
        return "Review retention exceptions with the data owner."
    if any(record.state == "unverified_completion" for record in records):
        return "Assign verifier and record verification method."
    return "Track through the normal evidence-retention cadence."


def render_json(
    records: list[DeletionEvidenceRecord],
    as_of: date,
    due_warning_days: int,
    review_warning_days: int,
) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "due_warning_days": due_warning_days,
        "review_warning_days": review_warning_days,
        "summary": summarize(records),
        "requests": [asdict(record) for record in sorted(records, key=sort_key)],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def sort_key(record: DeletionEvidenceRecord) -> tuple[int, int, str]:
    state_order = {
        "overdue_deletion": 0,
        "missing_due_date": 1,
        "missing_completion_evidence": 2,
        "exception_without_reason": 3,
        "exception_missing_review": 4,
        "exception_review_overdue": 5,
        "deletion_due_soon": 6,
        "exception_review_due_soon": 7,
        "unverified_completion": 8,
        "unknown_status": 9,
        "retention_exception_active": 10,
        "open": 11,
        "verified": 12,
    }
    days = record.days_to_due if record.days_to_due is not None else 9999
    return (-severity_value(record.severity), state_order.get(record.state, 99), days, record.request_id)


def severity_value(value: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(value, 0)


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
        if args.due_warning_days < 0 or args.review_warning_days < 0:
            raise ValueError("warning windows must be zero or greater")
        records = build_report(load_rows(args.input), as_of, args.due_warning_days, args.review_warning_days)
        content = (
            render_markdown(records, as_of, args.due_warning_days, args.review_warning_days)
            if args.format == "markdown"
            else render_json(records, as_of, args.due_warning_days, args.review_warning_days)
        )
        write_output(content, args.output)
        if args.fail_on_high and any(record.severity == "high" for record in records):
            return 1
        return 0
    except ValueError as exc:
        print(f"data deletion evidence report failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
