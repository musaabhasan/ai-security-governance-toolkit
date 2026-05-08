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
    "exercise_id",
    "scenario",
    "system",
    "exercise_date",
    "facilitator",
    "participants",
    "evidence_reference",
    "incident_domain",
    "severity_tested",
    "decision_log_complete",
    "communications_tested",
    "technical_containment_tested",
    "provider_fallback_tested",
    "legal_privacy_reviewed",
    "lessons_owner",
    "remediation_due",
    "status",
    "notes",
]
HIGH_SEVERITIES = {"high", "critical"}
YES_VALUES = {"yes", "true", "tested", "complete", "completed"}
CLOSED_STATUSES = {"closed", "complete", "completed", "done", "retired", "accepted"}


@dataclass(frozen=True)
class TabletopRecord:
    exercise_id: str
    scenario: str
    system: str
    exercise_date: str
    facilitator: str
    participants: str
    evidence_reference: str
    incident_domain: str
    severity_tested: str
    lessons_owner: str
    remediation_due: str
    status: str
    days_since_exercise: int | None
    days_to_remediation: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI tabletop exercise evidence report.")
    parser.add_argument("input", type=Path, help="Path to an AI tabletop exercise evidence CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=180,
        help="Maximum age for a tabletop exercise before it is flagged for refresh.",
    )
    parser.add_argument(
        "--remediation-warning-days",
        type=int,
        default=14,
        help="Days before remediation due date to flag an open item as due soon.",
    )
    parser.add_argument("--fail-on-high", action="store_true", help="Exit with code 1 when high-severity gaps exist.")
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
    max_age_days: int,
    remediation_warning_days: int,
) -> list[TabletopRecord]:
    return [classify_exercise(row, as_of, max_age_days, remediation_warning_days) for row in rows]


def classify_exercise(
    row: dict[str, str],
    as_of: date,
    max_age_days: int,
    remediation_warning_days: int,
) -> TabletopRecord:
    exercise_date_text = row["exercise_date"].strip()
    remediation_due_text = row["remediation_due"].strip()
    exercise_date = parse_iso_date(exercise_date_text, f"{row['exercise_id']} exercise_date") if exercise_date_text else None
    remediation_due = parse_iso_date(remediation_due_text, f"{row['exercise_id']} remediation_due") if remediation_due_text else None
    days_since_exercise = (as_of - exercise_date).days if exercise_date is not None else None
    days_to_remediation = (remediation_due - as_of).days if remediation_due is not None else None

    incident_domain = normalize(row["incident_domain"])
    severity_tested = normalize(row["severity_tested"])
    status = normalize(row["status"])
    high_scope = severity_tested in HIGH_SEVERITIES
    is_closed = status in CLOSED_STATUSES

    if not row["evidence_reference"].strip():
        state = "missing_evidence"
        severity = "high" if high_scope else "medium"
        action = "Attach the exercise pack, decision log, screenshots, and after-action notes."
    elif not row["facilitator"].strip() or not row["participants"].strip() or not row["lessons_owner"].strip():
        state = "missing_accountability"
        severity = "medium"
        action = "Record facilitator, participant roles, and lesson/remediation owner."
    elif not is_yes(row["decision_log_complete"]):
        state = "decision_log_gap"
        severity = "high" if high_scope else "medium"
        action = "Complete the decision log so escalation and approval timing can be reviewed."
    elif not is_yes(row["technical_containment_tested"]):
        state = "technical_containment_gap"
        severity = "high" if high_scope else "medium"
        action = "Test containment steps for tool access, provider keys, RAG sources, or integration routes."
    elif incident_domain in {"provider_outage", "provider_change", "continuity", "fallback"} and not is_yes(row["provider_fallback_tested"]):
        state = "provider_fallback_gap"
        severity = "high" if high_scope else "medium"
        action = "Exercise fallback routing, provider recovery, cost controls, and communications during failover."
    elif incident_domain in {"data_exposure", "privacy", "regulated_data"} and not is_yes(row["legal_privacy_reviewed"]):
        state = "legal_privacy_review_gap"
        severity = "high"
        action = "Add privacy/legal review for notification, retention, evidence handling, and affected data classes."
    elif high_scope and not is_yes(row["communications_tested"]):
        state = "communications_gap"
        severity = "medium"
        action = "Run internal, user-facing, vendor, and executive communications paths."
    elif not is_closed and days_to_remediation is not None and days_to_remediation < 0:
        state = "overdue_remediation"
        severity = "high"
        action = "Escalate overdue lessons learned to the risk owner."
    elif not is_closed and days_to_remediation is not None and days_to_remediation <= remediation_warning_days:
        state = "remediation_due_soon"
        severity = "medium"
        action = "Confirm remediation owner progress before the due date."
    elif days_since_exercise is None:
        state = "missing_exercise_date"
        severity = "medium"
        action = "Record the exercise date so evidence freshness can be assessed."
    elif days_since_exercise > max_age_days:
        state = "stale_tabletop"
        severity = "medium"
        action = "Refresh the tabletop exercise against the current model, provider, data, and tool landscape."
    else:
        state = "current"
        severity = "low"
        action = "Track through the normal governance exercise cadence."

    return TabletopRecord(
        exercise_id=row["exercise_id"],
        scenario=row["scenario"],
        system=row["system"],
        exercise_date=exercise_date_text,
        facilitator=row["facilitator"],
        participants=row["participants"],
        evidence_reference=row["evidence_reference"],
        incident_domain=row["incident_domain"],
        severity_tested=row["severity_tested"],
        lessons_owner=row["lessons_owner"],
        remediation_due=remediation_due_text,
        status=row["status"],
        days_since_exercise=days_since_exercise,
        days_to_remediation=days_to_remediation,
        state=state,
        severity=severity,
        action=action,
    )


def summarize(records: list[TabletopRecord]) -> dict[str, object]:
    severity_counts = Counter(record.severity for record in records)
    state_counts = Counter(record.state for record in records)
    domain_counts = Counter(record.incident_domain for record in records)
    return {
        "total": len(records),
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
        "missing_evidence": state_counts["missing_evidence"],
        "decision_log_gap": state_counts["decision_log_gap"],
        "provider_fallback_gap": state_counts["provider_fallback_gap"],
        "overdue_remediation": state_counts["overdue_remediation"],
        "domains": dict(sorted(domain_counts.items())),
    }


def render_markdown(
    records: list[TabletopRecord],
    as_of: date,
    max_age_days: int,
    remediation_warning_days: int,
) -> str:
    summary = summarize(records)
    lines = [
        "# AI Tabletop Exercise Evidence Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Exercise maximum age: `{max_age_days}` days",
        f"- Remediation warning window: `{remediation_warning_days}` days",
        f"- Total exercises: `{summary['total']}`",
        f"- High-severity gaps: `{summary['high']}`",
        f"- Medium-severity gaps: `{summary['medium']}`",
        f"- Missing evidence packs: `{summary['missing_evidence']}`",
        f"- Decision log gaps: `{summary['decision_log_gap']}`",
        f"- Provider fallback gaps: `{summary['provider_fallback_gap']}`",
        f"- Overdue remediation items: `{summary['overdue_remediation']}`",
        "",
        "## Exercise Queue",
        "",
        "| Exercise | System | Domain | State | Severity | Owner | Action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for record in sorted(records, key=record_sort_key):
        lines.append(
            "| "
            f"{record.exercise_id} - {record.scenario} | "
            f"{record.system} | "
            f"{record.incident_domain} | "
            f"{record.state} | "
            f"{record.severity} | "
            f"{record.lessons_owner or 'unassigned'} | "
            f"{record.action} |"
        )

    lines.extend(
        [
            "",
            "## Owner Queue",
            "",
            "| Owner | Exercises | High | Medium | Actions |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )

    for owner, owner_records in sorted(group_by_owner(records).items()):
        action_states = ", ".join(sorted({record.state for record in owner_records if record.state != "current"})) or "current"
        lines.append(
            "| "
            f"{owner or 'unassigned'} | "
            f"{len(owner_records)} | "
            f"{sum(1 for record in owner_records if record.severity == 'high')} | "
            f"{sum(1 for record in owner_records if record.severity == 'medium')} | "
            f"{action_states} |"
        )

    lines.extend(
        [
            "",
            "## Domain Coverage",
            "",
            "| Domain | Exercises |",
            "| --- | ---: |",
        ]
    )

    for domain, count in sorted(Counter(record.incident_domain for record in records).items()):
        lines.append(f"| {domain or 'unspecified'} | {count} |")

    return "\n".join(lines) + "\n"


def render_json(
    records: list[TabletopRecord],
    as_of: date,
    max_age_days: int,
    remediation_warning_days: int,
) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "max_age_days": max_age_days,
        "remediation_warning_days": remediation_warning_days,
        "summary": summarize(records),
        "records": [asdict(record) for record in sorted(records, key=record_sort_key)],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def group_by_owner(records: list[TabletopRecord]) -> dict[str, list[TabletopRecord]]:
    grouped: dict[str, list[TabletopRecord]] = defaultdict(list)
    for record in records:
        grouped[record.lessons_owner].append(record)
    return grouped


def record_sort_key(record: TabletopRecord) -> tuple[int, str, str]:
    severity_order = {"high": 0, "medium": 1, "low": 2}
    return (severity_order.get(record.severity, 3), record.state, record.exercise_id)


def normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def is_yes(value: str) -> bool:
    return normalize(value) in YES_VALUES


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    as_of = parse_iso_date(args.as_of, "as_of")
    records = build_report(load_rows(args.input), as_of, args.max_age_days, args.remediation_warning_days)
    output = (
        render_markdown(records, as_of, args.max_age_days, args.remediation_warning_days)
        if args.format == "markdown"
        else render_json(records, as_of, args.max_age_days, args.remediation_warning_days)
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if args.fail_on_high and any(record.severity == "high" for record in records):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError) as exc:
        print(f"Tabletop evidence report failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
