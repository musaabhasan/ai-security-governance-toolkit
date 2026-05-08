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
    "dependency_id",
    "system",
    "provider",
    "service_category",
    "dependency_type",
    "data_access",
    "criticality",
    "contract_owner",
    "approved_use",
    "region",
    "subprocessors_listed",
    "dpa_status",
    "security_assurance",
    "assurance_review_date",
    "exit_plan_status",
    "business_continuity_status",
    "status",
    "next_review_date",
    "notes",
]
SENSITIVE_DATA_MARKERS = ("student", "personal", "participant", "regulated", "confidential", "pii", "phi")
ACTIVE_STATUSES = {"active", "pilot", "approved", "production", "in_use"}


@dataclass(frozen=True)
class DependencyRecord:
    dependency_id: str
    system: str
    provider: str
    service_category: str
    dependency_type: str
    data_access: str
    criticality: str
    contract_owner: str
    dpa_status: str
    subprocessors_listed: str
    security_assurance: str
    assurance_review_date: str
    exit_plan_status: str
    business_continuity_status: str
    status: str
    next_review_date: str
    days_since_assurance: int | None
    days_to_review: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI third-party dependency report.")
    parser.add_argument("input", type=Path, help="Path to an AI third-party dependency CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument(
        "--assurance-max-age-days",
        type=int,
        default=365,
        help="Maximum age for third-party security assurance before it is flagged as stale.",
    )
    parser.add_argument(
        "--review-warning-days",
        type=int,
        default=30,
        help="Days before next review date to flag an active dependency as due soon.",
    )
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Exit with code 1 when high-severity dependency gaps are present.",
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
    assurance_max_age_days: int,
    review_warning_days: int,
) -> list[DependencyRecord]:
    return [classify_dependency(row, as_of, assurance_max_age_days, review_warning_days) for row in rows]


def classify_dependency(
    row: dict[str, str],
    as_of: date,
    assurance_max_age_days: int,
    review_warning_days: int,
) -> DependencyRecord:
    data_access = row["data_access"].strip()
    criticality = normalize(row["criticality"])
    dpa_status = normalize(row["dpa_status"])
    subprocessors = normalize(row["subprocessors_listed"])
    security_assurance = row["security_assurance"].strip()
    exit_plan = normalize(row["exit_plan_status"])
    continuity = normalize(row["business_continuity_status"])
    lifecycle_status = normalize(row["status"])
    assurance_date_text = row["assurance_review_date"].strip()
    next_review_text = row["next_review_date"].strip()

    assurance_date = parse_iso_date(assurance_date_text, f"{row['dependency_id']} assurance_review_date") if assurance_date_text else None
    next_review_date = parse_iso_date(next_review_text, f"{row['dependency_id']} next_review_date") if next_review_text else None
    days_since_assurance = (as_of - assurance_date).days if assurance_date is not None else None
    days_to_review = (next_review_date - as_of).days if next_review_date is not None else None

    sensitive = is_sensitive(data_access)
    high_or_critical = criticality in {"high", "critical"}
    is_critical = criticality == "critical" or "critical" in normalize(row["dependency_type"])
    is_active = lifecycle_status in ACTIVE_STATUSES or lifecycle_status == ""

    if dpa_status not in {"executed", "approved", "signed", "not required"}:
        state = "missing_dpa"
        severity = "high" if sensitive else "medium"
        action = "Complete or approve the data-processing agreement before continued use."
    elif subprocessors in {"no", "unknown", "missing", ""} and sensitive:
        state = "missing_subprocessor_transparency"
        severity = "high"
        action = "Obtain and review the provider subprocessor list for sensitive data processing."
    elif not security_assurance:
        state = "missing_security_assurance"
        severity = "high" if high_or_critical else "medium"
        action = "Collect current security assurance evidence from the provider."
    elif days_since_assurance is not None and days_since_assurance > assurance_max_age_days:
        state = "overdue_assurance_review"
        severity = "high" if high_or_critical else "medium"
        action = "Refresh provider assurance review and document accepted residual risk."
    elif days_since_assurance is None:
        state = "missing_assurance_review_date"
        severity = "medium"
        action = "Record the date of the last assurance review."
    elif is_critical and exit_plan not in {"approved", "tested"}:
        state = "critical_exit_plan_gap"
        severity = "high"
        action = "Approve an exit plan for the critical AI dependency."
    elif is_critical and continuity not in {"tested"}:
        state = "critical_continuity_gap"
        severity = "high"
        action = "Run and record a continuity test for the critical dependency."
    elif is_active and next_review_date is None:
        state = "missing_next_review"
        severity = "medium"
        action = "Set the next provider review date."
    elif is_active and days_to_review is not None and days_to_review < 0:
        state = "review_overdue"
        severity = "medium"
        action = "Escalate overdue provider review to the contract owner."
    elif is_active and days_to_review is not None and days_to_review <= review_warning_days:
        state = "review_due_soon"
        severity = "medium"
        action = "Schedule provider review before the due date."
    else:
        state = "current"
        severity = "low"
        action = "Track through the normal vendor-risk review cadence."

    return DependencyRecord(
        dependency_id=row["dependency_id"],
        system=row["system"],
        provider=row["provider"],
        service_category=row["service_category"],
        dependency_type=row["dependency_type"],
        data_access=data_access,
        criticality=row["criticality"],
        contract_owner=row["contract_owner"],
        dpa_status=row["dpa_status"],
        subprocessors_listed=row["subprocessors_listed"],
        security_assurance=security_assurance,
        assurance_review_date=assurance_date_text,
        exit_plan_status=row["exit_plan_status"],
        business_continuity_status=row["business_continuity_status"],
        status=row["status"],
        next_review_date=next_review_text,
        days_since_assurance=days_since_assurance,
        days_to_review=days_to_review,
        state=state,
        severity=severity,
        action=action,
    )


def summarize(records: list[DependencyRecord]) -> dict[str, object]:
    severity_counts = Counter(record.severity for record in records)
    state_counts = Counter(record.state for record in records)
    critical_dependencies = sum(1 for record in records if normalize(record.criticality) == "critical")
    sensitive_dependencies = sum(1 for record in records if is_sensitive(record.data_access))
    return {
        "total": len(records),
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
        "critical_dependencies": critical_dependencies,
        "sensitive_dependencies": sensitive_dependencies,
        "missing_dpa": state_counts["missing_dpa"],
        "missing_subprocessor_transparency": state_counts["missing_subprocessor_transparency"],
        "overdue_assurance_review": state_counts["overdue_assurance_review"],
        "critical_exit_or_continuity_gaps": state_counts["critical_exit_plan_gap"] + state_counts["critical_continuity_gap"],
    }


def render_markdown(
    records: list[DependencyRecord],
    as_of: date,
    assurance_max_age_days: int,
    review_warning_days: int,
) -> str:
    summary = summarize(records)
    lines = [
        "# AI Third-Party Dependency Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Assurance maximum age: `{assurance_max_age_days}` days",
        f"- Review warning window: `{review_warning_days}` days",
        f"- Total dependencies: `{summary['total']}`",
        f"- High-severity items: `{summary['high']}`",
        f"- Medium-severity items: `{summary['medium']}`",
        f"- Critical dependencies: `{summary['critical_dependencies']}`",
        f"- Sensitive-data dependencies: `{summary['sensitive_dependencies']}`",
        f"- Missing DPAs: `{summary['missing_dpa']}`",
        f"- Missing subprocessor transparency: `{summary['missing_subprocessor_transparency']}`",
        f"- Overdue assurance reviews: `{summary['overdue_assurance_review']}`",
        f"- Critical exit or continuity gaps: `{summary['critical_exit_or_continuity_gaps']}`",
        "",
        "## Provider Queue",
        "",
        "| Provider | Dependencies | High | Medium | Critical | Sensitive Data | Action |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for provider, provider_records in provider_summary(records):
        lines.append(
            "| {provider} | {dependencies} | {high} | {medium} | {critical} | {sensitive} | {action} |".format(
                provider=escape_pipe(provider),
                dependencies=len(provider_records),
                high=sum(1 for record in provider_records if record.severity == "high"),
                medium=sum(1 for record in provider_records if record.severity == "medium"),
                critical=sum(1 for record in provider_records if normalize(record.criticality) == "critical"),
                sensitive=sum(1 for record in provider_records if is_sensitive(record.data_access)),
                action=escape_pipe(provider_action(provider_records)),
            )
        )

    lines.extend(
        [
            "",
            "## Dependency Details",
            "",
            "| Dependency | System | Provider | Category | Type | Data Access | Criticality | Owner | State | Severity | Action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in sorted(records, key=sort_key):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.dependency_id),
                    escape_pipe(record.system),
                    escape_pipe(record.provider),
                    escape_pipe(record.service_category),
                    escape_pipe(record.dependency_type),
                    escape_pipe(record.data_access),
                    escape_pipe(record.criticality),
                    escape_pipe(record.contract_owner),
                    record.state,
                    record.severity,
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json(
    records: list[DependencyRecord],
    as_of: date,
    assurance_max_age_days: int,
    review_warning_days: int,
) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "assurance_max_age_days": assurance_max_age_days,
        "review_warning_days": review_warning_days,
        "summary": summarize(records),
        "dependencies": [asdict(record) for record in sorted(records, key=sort_key)],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def provider_summary(records: list[DependencyRecord]) -> list[tuple[str, list[DependencyRecord]]]:
    grouped: dict[str, list[DependencyRecord]] = defaultdict(list)
    for record in records:
        grouped[record.provider or "unassigned"].append(record)
    return sorted(
        grouped.items(),
        key=lambda item: (
            -max(severity_value(record.severity) for record in item[1]),
            -len(item[1]),
            item[0].lower(),
        ),
    )


def provider_action(records: list[DependencyRecord]) -> str:
    if any(record.state == "missing_dpa" for record in records):
        return "Resolve DPA status before expansion or renewal."
    if any(record.state == "missing_subprocessor_transparency" for record in records):
        return "Request subprocessor list and complete sensitive-data review."
    if any(record.state in {"critical_exit_plan_gap", "critical_continuity_gap"} for record in records):
        return "Close critical exit and continuity gaps."
    if any(record.state in {"overdue_assurance_review", "missing_security_assurance"} for record in records):
        return "Refresh provider assurance evidence."
    if any(record.state in {"review_overdue", "review_due_soon", "missing_next_review"} for record in records):
        return "Schedule governance review with the contract owner."
    return "Track through normal vendor-risk review cadence."


def sort_key(record: DependencyRecord) -> tuple[int, int, str, str]:
    state_order = {
        "missing_dpa": 0,
        "missing_subprocessor_transparency": 1,
        "missing_security_assurance": 2,
        "overdue_assurance_review": 3,
        "critical_exit_plan_gap": 4,
        "critical_continuity_gap": 5,
        "missing_assurance_review_date": 6,
        "review_overdue": 7,
        "review_due_soon": 8,
        "missing_next_review": 9,
        "current": 10,
    }
    return (
        -severity_value(record.severity),
        state_order.get(record.state, 99),
        record.provider.lower(),
        record.dependency_id,
    )


def severity_value(value: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(value, 0)


def is_sensitive(value: str) -> bool:
    lowered = normalize(value)
    return any(marker in lowered for marker in SENSITIVE_DATA_MARKERS)


def normalize(value: str) -> str:
    return value.strip().lower().replace("_", " ").replace("-", " ")


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
        if args.assurance_max_age_days < 0 or args.review_warning_days < 0:
            raise ValueError("warning windows must be zero or greater")
        records = build_report(load_rows(args.input), as_of, args.assurance_max_age_days, args.review_warning_days)
        content = (
            render_markdown(records, as_of, args.assurance_max_age_days, args.review_warning_days)
            if args.format == "markdown"
            else render_json(records, as_of, args.assurance_max_age_days, args.review_warning_days)
        )
        write_output(content, args.output)
        if args.fail_on_high and any(record.severity == "high" for record in records):
            return 1
        return 0
    except ValueError as exc:
        print(f"third-party dependency report failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
