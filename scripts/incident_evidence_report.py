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


REQUIRED_COLUMNS = [
    "incident_id",
    "system",
    "incident_type",
    "severity",
    "detected_at",
    "reported_at",
    "incident_owner",
    "containment_owner",
    "data_exposure",
    "tool_misuse",
    "model_or_provider",
    "affected_users",
    "evidence_reference",
    "timeline_complete",
    "containment_evidence",
    "logs_preserved",
    "privacy_reviewed",
    "communications_prepared",
    "root_cause_status",
    "remediation_due",
    "status",
    "notes",
]
YES_VALUES = {"yes", "true", "complete", "completed", "available", "preserved", "prepared"}
HIGH_INCIDENT_SEVERITIES = {"critical", "high", "severe", "sev1", "sev-1", "sev2", "sev-2"}
OPEN_STATUSES = {"open", "active", "investigating", "contained", "monitoring", "remediating", "pending_review"}
CLOSED_STATUSES = {"closed", "resolved", "retired", "cancelled", "canceled"}
ROOT_CAUSE_COMPLETE = {"complete", "completed", "approved", "validated", "accepted"}


@dataclass(frozen=True)
class IncidentEvidenceRecord:
    incident_id: str
    system: str
    incident_type: str
    incident_severity: str
    detected_at: str
    reported_at: str
    incident_owner: str
    containment_owner: str
    data_exposure: str
    tool_misuse: str
    model_or_provider: str
    affected_users: str
    evidence_reference: str
    timeline_complete: str
    containment_evidence: str
    logs_preserved: str
    privacy_reviewed: str
    communications_prepared: str
    root_cause_status: str
    remediation_due: str
    status: str
    age_days: int | None
    report_lag_days: int | None
    days_to_remediation: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI incident evidence readiness report.")
    parser.add_argument("input", type=Path, help="Path to an AI incident evidence CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument("--warning-days", type=int, default=14, help="Days before remediation due date to flag.")
    parser.add_argument("--fail-on-high", action="store_true", help="Exit with code 1 when high-severity gaps exist.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", type=Path, help="Optional output path. Defaults to stdout.")
    return parser.parse_args(argv)


def parse_iso_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD: {value}") from exc


def parse_optional_date(value: str, field_name: str) -> date | None:
    if not value:
        return None
    return parse_iso_date(value, field_name)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} is empty")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def build_report(rows: Iterable[dict[str, str]], as_of: date, warning_days: int) -> list[IncidentEvidenceRecord]:
    return [classify_incident(row, as_of, warning_days) for row in rows]


def classify_incident(row: dict[str, str], as_of: date, warning_days: int) -> IncidentEvidenceRecord:
    incident_id = row["incident_id"]
    detected = parse_optional_date(row["detected_at"], f"{incident_id} detected_at")
    reported = parse_optional_date(row["reported_at"], f"{incident_id} reported_at")
    remediation_due = parse_optional_date(row["remediation_due"], f"{incident_id} remediation_due")
    age_days = (as_of - detected).days if detected else None
    report_lag_days = (reported - detected).days if reported and detected else None
    days_to_remediation = (remediation_due - as_of).days if remediation_due else None

    status = normalize(row["status"])
    is_closed = status in CLOSED_STATUSES
    is_high_incident = normalize(row["severity"]) in HIGH_INCIDENT_SEVERITIES
    data_exposure = is_yes(row["data_exposure"])
    tool_misuse = is_yes(row["tool_misuse"])

    if not row["incident_owner"]:
        state = "incident_owner_missing"
        finding_severity = "high"
        action = "Assign an incident owner before the next governance review."
    elif not row["containment_owner"] and not is_closed:
        state = "containment_owner_missing"
        finding_severity = "high"
        action = "Assign a containment owner and record response accountability."
    elif data_exposure and not is_yes(row["privacy_reviewed"]):
        state = "data_exposure_privacy_review_missing"
        finding_severity = "high"
        action = "Complete privacy/legal review and attach evidence before closure."
    elif tool_misuse and not is_yes(row["logs_preserved"]):
        state = "tool_misuse_logs_missing"
        finding_severity = "high"
        action = "Preserve prompt, output, identity, tool-call, and downstream system logs."
    elif is_high_incident and not is_yes(row["containment_evidence"]):
        state = "containment_evidence_missing"
        finding_severity = "high"
        action = "Attach containment evidence for high-severity AI incident review."
    elif not row["evidence_reference"]:
        state = "evidence_reference_missing"
        finding_severity = "medium"
        action = "Add a link or case reference to the incident evidence package."
    elif not is_yes(row["timeline_complete"]):
        state = "timeline_incomplete"
        finding_severity = "medium"
        action = "Complete the incident timeline from detection through recovery."
    elif is_high_incident and not is_yes(row["communications_prepared"]):
        state = "communications_gap"
        finding_severity = "medium"
        action = "Prepare internal, stakeholder, regulator, or user communication artifacts."
    elif not is_closed and normalize(row["root_cause_status"]) not in ROOT_CAUSE_COMPLETE:
        state = "root_cause_incomplete"
        finding_severity = "medium"
        action = "Complete root-cause analysis and confirm remediation owner."
    elif not is_closed and days_to_remediation is not None and days_to_remediation < 0:
        state = "remediation_overdue"
        finding_severity = "medium"
        action = "Escalate overdue remediation to the incident owner and governance forum."
    elif not is_closed and days_to_remediation is not None and days_to_remediation <= warning_days:
        state = "remediation_due_soon"
        finding_severity = "medium"
        action = "Confirm remediation evidence will be ready before the due date."
    elif is_closed:
        state = "closed"
        finding_severity = "low"
        action = "Retain evidence according to the incident evidence retention schedule."
    else:
        state = "current"
        finding_severity = "low"
        action = "Continue normal incident review cadence."

    return IncidentEvidenceRecord(
        incident_id=incident_id,
        system=row["system"],
        incident_type=row["incident_type"],
        incident_severity=row["severity"],
        detected_at=row["detected_at"],
        reported_at=row["reported_at"],
        incident_owner=row["incident_owner"],
        containment_owner=row["containment_owner"],
        data_exposure=row["data_exposure"],
        tool_misuse=row["tool_misuse"],
        model_or_provider=row["model_or_provider"],
        affected_users=row["affected_users"],
        evidence_reference=row["evidence_reference"],
        timeline_complete=row["timeline_complete"],
        containment_evidence=row["containment_evidence"],
        logs_preserved=row["logs_preserved"],
        privacy_reviewed=row["privacy_reviewed"],
        communications_prepared=row["communications_prepared"],
        root_cause_status=row["root_cause_status"],
        remediation_due=row["remediation_due"],
        status=row["status"],
        age_days=age_days,
        report_lag_days=report_lag_days,
        days_to_remediation=days_to_remediation,
        state=state,
        severity=finding_severity,
        action=action,
    )


def summarize(records: list[IncidentEvidenceRecord]) -> dict[str, int]:
    states = Counter(record.state for record in records)
    severity = Counter(record.severity for record in records)
    closed = sum(1 for record in records if normalize(record.status) in CLOSED_STATUSES)
    return {
        "total": len(records),
        "high": severity["high"],
        "medium": severity["medium"],
        "low": severity["low"],
        "open": len(records) - closed,
        "closed": closed,
        "data_exposure_privacy_review_missing": states["data_exposure_privacy_review_missing"],
        "tool_misuse_logs_missing": states["tool_misuse_logs_missing"],
        "containment_evidence_missing": states["containment_evidence_missing"],
        "timeline_incomplete": states["timeline_incomplete"],
        "remediation_overdue": states["remediation_overdue"],
    }


def render_markdown(records: list[IncidentEvidenceRecord], as_of: date, warning_days: int) -> str:
    summary = summarize(records)
    lines = [
        "# AI Incident Evidence Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Remediation warning window: `{warning_days}` days",
        f"- Total incidents: `{summary['total']}`",
        f"- High-severity evidence gaps: `{summary['high']}`",
        f"- Medium-severity evidence gaps: `{summary['medium']}`",
        f"- Open incidents: `{summary['open']}`",
        f"- Closed incidents: `{summary['closed']}`",
        "",
        "## Incident Evidence Review Queue",
        "",
        "| Incident | System | Type | Incident Severity | Owner | Status | Age | Due In | State | Finding Severity | Action |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for record in sorted(records, key=sort_key):
        age = "" if record.age_days is None else str(record.age_days)
        due = "" if record.days_to_remediation is None else str(record.days_to_remediation)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.incident_id),
                    escape_pipe(record.system),
                    escape_pipe(record.incident_type),
                    escape_pipe(record.incident_severity),
                    escape_pipe(record.incident_owner),
                    escape_pipe(record.status),
                    age,
                    due,
                    record.state,
                    record.severity,
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json(records: list[IncidentEvidenceRecord], as_of: date, warning_days: int) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "warning_days": warning_days,
        "summary": summarize(records),
        "records": [asdict(record) for record in sorted(records, key=sort_key)],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def sort_key(record: IncidentEvidenceRecord) -> tuple[int, int, str]:
    severity_order = {"high": 0, "medium": 1, "low": 2}
    due = record.days_to_remediation if record.days_to_remediation is not None else 99999
    return (severity_order.get(record.severity, 9), due, record.incident_id)


def is_yes(value: str) -> bool:
    return normalize(value) in YES_VALUES


def normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|")


def write_output(content: str, output_path: Path | None) -> None:
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    else:
        print(content)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    as_of = parse_iso_date(args.as_of, "as_of")
    rows = load_rows(args.input)
    records = build_report(rows, as_of, args.warning_days)
    content = render_json(records, as_of, args.warning_days) if args.format == "json" else render_markdown(records, as_of, args.warning_days)
    write_output(content, args.output)
    if args.fail_on_high and any(record.severity == "high" for record in records):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except ValueError as exc:
        print(f"incident_evidence_report.py: {exc}", file=sys.stderr)
        raise SystemExit(2)
