from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "templates" / "ai-rollback-readiness-register.csv"
REQUIRED_COLUMNS = [
    "rollback_id",
    "system",
    "change_type",
    "current_version",
    "fallback_version",
    "rollback_owner",
    "trigger_condition",
    "last_drill_date",
    "rollback_runbook",
    "evaluation_baseline",
    "traffic_shift_plan",
    "data_schema_compatible",
    "credential_rollback_ready",
    "communication_plan",
    "approval_status",
    "next_drill_due",
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
    reviewed = [review_item(row, as_of) for row in rows]
    severity_counts = Counter(item["severity"] for item in reviewed)
    owner_queues: dict[str, list[str]] = defaultdict(list)
    change_counts = Counter(item["change_type"] or "unspecified" for item in reviewed)

    for item in reviewed:
        if item["severity"] in {"high", "medium"}:
            owner_queues[item["rollback_owner"] or "unassigned"].append(str(item["rollback_id"]))

    return {
        "summary": {
            "rollback_items": len(reviewed),
            "high": severity_counts["high"],
            "medium": severity_counts["medium"],
            "low": severity_counts["low"],
            "change_type_counts": dict(sorted(change_counts.items())),
            "owner_queues": {owner: items for owner, items in sorted(owner_queues.items())},
        },
        "items": reviewed,
    }


def review_item(row: dict[str, str], as_of: date) -> dict[str, object]:
    flags: list[str] = []
    for column in ("rollback_id", "system", "change_type", "current_version", "fallback_version", "rollback_owner"):
        if not row[column]:
            flags.append(f"{column} missing")

    if not row["trigger_condition"]:
        flags.append("trigger condition missing")
    if not row["rollback_runbook"]:
        flags.append("rollback runbook missing")
    if not row["evaluation_baseline"]:
        flags.append("evaluation baseline missing")
    if not row["traffic_shift_plan"]:
        flags.append("traffic shift plan missing")
    if not truthy(row["data_schema_compatible"]):
        flags.append("data schema compatibility not confirmed")
    if not truthy(row["credential_rollback_ready"]):
        flags.append("credential rollback readiness not confirmed")
    if not row["communication_plan"]:
        flags.append("communication plan missing")

    approval = row["approval_status"].lower()
    if approval not in {"approved", "approved_with_controls"}:
        flags.append("rollback plan is not approved")

    last_drill = parse_date(row["last_drill_date"])
    next_drill = parse_date(row["next_drill_due"])
    if last_drill is None:
        flags.append("last drill date missing")
    if next_drill is None:
        flags.append("next drill due missing")
    elif next_drill < as_of:
        flags.append("rollback drill is overdue")

    return {
        "rollback_id": row["rollback_id"],
        "system": row["system"],
        "change_type": row["change_type"],
        "rollback_owner": row["rollback_owner"],
        "approval_status": row["approval_status"],
        "severity": severity_for(flags),
        "flags": flags,
        "recommended_action": recommended_action(flags),
    }


def severity_for(flags: list[str]) -> str:
    high_markers = (
        "runbook missing",
        "evaluation baseline missing",
        "data schema compatibility",
        "credential rollback",
        "not approved",
        "drill is overdue",
    )
    if any(any(marker in flag for marker in high_markers) for flag in flags):
        return "high"
    if flags:
        return "medium"
    return "low"


def recommended_action(flags: list[str]) -> str:
    if any("runbook" in flag for flag in flags):
        return "Create a tested rollback runbook before releasing the model, prompt, provider, or RAG change."
    if any("evaluation baseline" in flag for flag in flags):
        return "Record baseline evaluation results so rollback can be justified against quality, safety, or citation regression."
    if any("drill is overdue" in flag for flag in flags):
        return "Run a rollback drill and update evidence before the next release approval."
    if any("not approved" in flag for flag in flags):
        return "Route the rollback plan for owner and risk approval before launch."
    if flags:
        return "Resolve rollback readiness gaps before production release or provider change."
    return "Rollback plan is suitable for routine release review."


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


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
        "# AI Rollback Readiness Report",
        "",
        f"- Rollback items: `{summary['rollback_items']}`",
        f"- High-risk gaps: `{summary['high']}`",
        f"- Medium-risk gaps: `{summary['medium']}`",
        "",
        "## Owner Queue",
        "",
        "| Owner | Rollback items needing review |",
        "| --- | --- |",
    ]

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    if owner_queues:
        for owner, rollback_ids in owner_queues.items():
            assert isinstance(rollback_ids, list)
            lines.append(f"| {escape_cell(owner)} | {'; '.join(rollback_ids)} |")
    else:
        lines.append("| none | none |")

    lines.extend([
        "",
        "## Findings",
        "",
        "| Rollback | System | Change type | Owner | Severity | Flags | Recommended action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])

    for item in items:
        assert isinstance(item, dict)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(str(item["rollback_id"])),
                    escape_cell(str(item["system"])),
                    escape_cell(str(item["change_type"])),
                    escape_cell(str(item["rollback_owner"] or "unassigned")),
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
    parser = argparse.ArgumentParser(description="Review rollback readiness for AI model, prompt, provider, and RAG releases.")
    parser.add_argument("register", nargs="?", type=Path, default=DEFAULT_REGISTER)
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
