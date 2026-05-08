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
    "access_id",
    "system",
    "identity",
    "identity_type",
    "role",
    "permission_level",
    "data_access",
    "tool_access",
    "owner",
    "business_justification",
    "last_login_date",
    "last_review_date",
    "mfa_enabled",
    "break_glass",
    "api_key_or_token",
    "status",
    "employment_status",
    "review_decision",
    "next_review_date",
    "notes",
]
YES_VALUES = {"yes", "true", "enabled", "complete", "completed", "approved"}
PRIVILEGED_MARKERS = ("admin", "owner", "privileged", "superuser", "write", "manage", "approve")
HIGH_IMPACT_TOOL_MARKERS = ("delete", "deploy", "execute", "write", "send", "approve", "grant", "payment", "merge")
INACTIVE_STATUSES = {"inactive", "disabled", "suspended", "revoked", "removed"}
SEPARATION_MARKERS = {"terminated", "departed", "offboarded", "transferred", "unknown"}


@dataclass(frozen=True)
class AccessRecord:
    access_id: str
    system: str
    identity: str
    identity_type: str
    role: str
    permission_level: str
    data_access: str
    tool_access: str
    owner: str
    business_justification: str
    last_login_date: str
    last_review_date: str
    mfa_enabled: str
    break_glass: str
    api_key_or_token: str
    status: str
    employment_status: str
    review_decision: str
    next_review_date: str
    days_since_login: int | None
    days_since_review: int | None
    days_to_next_review: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI access recertification report.")
    parser.add_argument("input", type=Path, help="Path to an AI access recertification CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument("--privileged-max-age-days", type=int, default=90, help="Maximum review age for privileged access.")
    parser.add_argument("--standard-max-age-days", type=int, default=180, help="Maximum review age for standard access.")
    parser.add_argument("--inactive-days", type=int, default=60, help="Days since login before active access is flagged as stale.")
    parser.add_argument("--review-warning-days", type=int, default=30, help="Days before next review to flag access due soon.")
    parser.add_argument("--fail-on-high", action="store_true", help="Exit with code 1 when high-severity access gaps exist.")
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
    privileged_max_age_days: int,
    standard_max_age_days: int,
    inactive_days: int,
    review_warning_days: int,
) -> list[AccessRecord]:
    return [
        classify_access(row, as_of, privileged_max_age_days, standard_max_age_days, inactive_days, review_warning_days)
        for row in rows
    ]


def classify_access(
    row: dict[str, str],
    as_of: date,
    privileged_max_age_days: int,
    standard_max_age_days: int,
    inactive_days: int,
    review_warning_days: int,
) -> AccessRecord:
    access_id = row["access_id"]
    last_login_text = row["last_login_date"].strip()
    last_review_text = row["last_review_date"].strip()
    next_review_text = row["next_review_date"].strip()
    last_login = parse_iso_date(last_login_text, f"{access_id} last_login_date") if last_login_text else None
    last_review = parse_iso_date(last_review_text, f"{access_id} last_review_date") if last_review_text else None
    next_review = parse_iso_date(next_review_text, f"{access_id} next_review_date") if next_review_text else None
    days_since_login = (as_of - last_login).days if last_login else None
    days_since_review = (as_of - last_review).days if last_review else None
    days_to_next_review = (next_review - as_of).days if next_review else None

    privileged = is_privileged(row["permission_level"], row["role"]) or is_break_glass(row["break_glass"])
    token_access = is_yes(row["api_key_or_token"]) or "token" in normalize(row["identity_type"]) or "api" in normalize(row["identity_type"])
    high_impact_tool = has_high_impact_tool(row["tool_access"])
    active = normalize(row["status"]) not in INACTIVE_STATUSES
    separated = normalize(row["employment_status"]) in SEPARATION_MARKERS
    review_max_age = privileged_max_age_days if privileged else standard_max_age_days

    if separated and active:
        state = "separated_identity_still_active"
        severity = "high"
        action = "Remove or suspend access immediately and attach offboarding evidence."
    elif privileged and not is_yes(row["mfa_enabled"]):
        state = "privileged_without_mfa"
        severity = "high"
        action = "Block privileged access until MFA is enabled and verified."
    elif token_access and not row["owner"]:
        state = "unowned_token_or_service_account"
        severity = "high"
        action = "Assign a named owner and rotate credentials if ownership cannot be proven."
    elif is_break_glass(row["break_glass"]) and normalize(row["review_decision"]) not in {"approved", "retain"}:
        state = "break_glass_not_approved"
        severity = "high"
        action = "Obtain explicit break-glass approval, scope, monitoring evidence, and expiry."
    elif high_impact_tool and normalize(row["review_decision"]) not in {"approved", "retain"}:
        state = "high_impact_tool_access_unapproved"
        severity = "high"
        action = "Disable high-impact tool access until a reviewer approves the role and evidence."
    elif privileged and days_since_review is None:
        state = "privileged_review_missing"
        severity = "high"
        action = "Complete privileged access recertification before continued use."
    elif privileged and days_since_review > privileged_max_age_days:
        state = "privileged_review_overdue"
        severity = "high"
        action = "Escalate overdue privileged recertification to the system owner."
    elif privileged and not row["business_justification"]:
        state = "privileged_justification_missing"
        severity = "high"
        action = "Document business justification or remove privileged access."
    elif active and days_since_login is not None and days_since_login > inactive_days:
        state = "stale_active_access"
        severity = "medium"
        action = "Confirm need or remove inactive access from the AI system."
    elif days_since_review is None:
        state = "review_missing"
        severity = "medium"
        action = "Complete access review and record reviewer decision."
    elif days_since_review > review_max_age:
        state = "review_overdue"
        severity = "medium"
        action = "Refresh access review and update the next review date."
    elif active and next_review is None:
        state = "next_review_missing"
        severity = "medium"
        action = "Set next review date for recurring recertification."
    elif active and days_to_next_review is not None and days_to_next_review < 0:
        state = "next_review_overdue"
        severity = "medium"
        action = "Escalate overdue next review to the owner."
    elif active and days_to_next_review is not None and days_to_next_review <= review_warning_days:
        state = "review_due_soon"
        severity = "medium"
        action = "Schedule recertification before the review date."
    else:
        state = "current"
        severity = "low"
        action = "Keep access in the normal recertification cadence."

    return AccessRecord(
        access_id=access_id,
        system=row["system"],
        identity=row["identity"],
        identity_type=row["identity_type"],
        role=row["role"],
        permission_level=row["permission_level"],
        data_access=row["data_access"],
        tool_access=row["tool_access"],
        owner=row["owner"],
        business_justification=row["business_justification"],
        last_login_date=last_login_text,
        last_review_date=last_review_text,
        mfa_enabled=row["mfa_enabled"],
        break_glass=row["break_glass"],
        api_key_or_token=row["api_key_or_token"],
        status=row["status"],
        employment_status=row["employment_status"],
        review_decision=row["review_decision"],
        next_review_date=next_review_text,
        days_since_login=days_since_login,
        days_since_review=days_since_review,
        days_to_next_review=days_to_next_review,
        state=state,
        severity=severity,
        action=action,
    )


def summarize(records: list[AccessRecord]) -> dict[str, int]:
    severity_counts = Counter(record.severity for record in records)
    state_counts = Counter(record.state for record in records)
    return {
        "total": len(records),
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
        "separated_identity_still_active": state_counts["separated_identity_still_active"],
        "privileged_without_mfa": state_counts["privileged_without_mfa"],
        "unowned_token_or_service_account": state_counts["unowned_token_or_service_account"],
        "privileged_review_overdue": state_counts["privileged_review_overdue"],
        "high_impact_tool_access_unapproved": state_counts["high_impact_tool_access_unapproved"],
    }


def render_markdown(
    records: list[AccessRecord],
    as_of: date,
    privileged_max_age_days: int,
    standard_max_age_days: int,
    inactive_days: int,
) -> str:
    summary = summarize(records)
    lines = [
        "# AI Access Recertification Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Privileged review maximum age: `{privileged_max_age_days}` days",
        f"- Standard review maximum age: `{standard_max_age_days}` days",
        f"- Inactive access threshold: `{inactive_days}` days",
        f"- Total access records: `{summary['total']}`",
        f"- High-severity gaps: `{summary['high']}`",
        f"- Medium-severity gaps: `{summary['medium']}`",
        f"- Active separated identities: `{summary['separated_identity_still_active']}`",
        f"- Privileged access without MFA: `{summary['privileged_without_mfa']}`",
        f"- Unowned tokens or service accounts: `{summary['unowned_token_or_service_account']}`",
        "",
        "## Access Review Queue",
        "",
        "| Access | System | Identity | Type | Permission | Tools | State | Severity | Owner | Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for record in sorted(records, key=record_sort_key):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.access_id),
                    escape_pipe(record.system),
                    escape_pipe(record.identity),
                    escape_pipe(record.identity_type),
                    escape_pipe(record.permission_level),
                    escape_pipe(record.tool_access),
                    record.state,
                    record.severity,
                    escape_pipe(record.owner or "unassigned"),
                    escape_pipe(record.action),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Owner Queue",
            "",
            "| Owner | Records | High | Medium | Action States |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for owner, owner_records in sorted(group_by_owner(records).items()):
        states = ", ".join(sorted({record.state for record in owner_records if record.state != "current"})) or "current"
        lines.append(
            "| {owner} | {count} | {high} | {medium} | {states} |".format(
                owner=escape_pipe(owner or "unassigned"),
                count=len(owner_records),
                high=sum(1 for record in owner_records if record.severity == "high"),
                medium=sum(1 for record in owner_records if record.severity == "medium"),
                states=escape_pipe(states),
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_json(
    records: list[AccessRecord],
    as_of: date,
    privileged_max_age_days: int,
    standard_max_age_days: int,
    inactive_days: int,
) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "privileged_max_age_days": privileged_max_age_days,
        "standard_max_age_days": standard_max_age_days,
        "inactive_days": inactive_days,
        "summary": summarize(records),
        "access_records": [asdict(record) for record in sorted(records, key=record_sort_key)],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def group_by_owner(records: list[AccessRecord]) -> dict[str, list[AccessRecord]]:
    grouped: dict[str, list[AccessRecord]] = defaultdict(list)
    for record in records:
        grouped[record.owner].append(record)
    return grouped


def record_sort_key(record: AccessRecord) -> tuple[int, str, str]:
    severity_order = {"high": 0, "medium": 1, "low": 2}
    return (severity_order.get(record.severity, 3), record.state, record.access_id)


def is_privileged(permission_level: str, role: str) -> bool:
    text = f"{permission_level} {role}".lower()
    return any(marker in text for marker in PRIVILEGED_MARKERS)


def has_high_impact_tool(tool_access: str) -> bool:
    text = tool_access.lower()
    return any(marker in text for marker in HIGH_IMPACT_TOOL_MARKERS)


def is_break_glass(value: str) -> bool:
    return is_yes(value)


def is_yes(value: str) -> bool:
    return normalize(value) in YES_VALUES


def normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    as_of = parse_iso_date(args.as_of, "as_of")
    for name, value in (
        ("--privileged-max-age-days", args.privileged_max_age_days),
        ("--standard-max-age-days", args.standard_max_age_days),
        ("--inactive-days", args.inactive_days),
        ("--review-warning-days", args.review_warning_days),
    ):
        if value < 0:
            raise ValueError(f"{name} must be zero or greater")

    records = build_report(
        load_rows(args.input),
        as_of,
        args.privileged_max_age_days,
        args.standard_max_age_days,
        args.inactive_days,
        args.review_warning_days,
    )
    output = (
        render_markdown(records, as_of, args.privileged_max_age_days, args.standard_max_age_days, args.inactive_days)
        if args.format == "markdown"
        else render_json(records, as_of, args.privileged_max_age_days, args.standard_max_age_days, args.inactive_days)
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    if args.fail_on_high and any(record.severity == "high" for record in records):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError) as exc:
        print(f"access recertification report failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
