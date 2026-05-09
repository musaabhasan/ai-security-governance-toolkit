from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "templates" / "ai-dpia-triage-register.csv"
REQUIRED_COLUMNS = [
    "triage_id",
    "system",
    "use_case",
    "data_subjects",
    "data_classification",
    "special_category_data",
    "children_or_students",
    "automated_decisioning",
    "large_scale_processing",
    "monitoring_or_tracking",
    "third_party_provider",
    "cross_border_transfer",
    "human_review",
    "privacy_notice_updated",
    "dpia_owner",
    "planned_launch_date",
    "triage_decision",
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
    decision_counts = Counter(item["triage_decision"] or "unspecified" for item in reviewed)

    for item in reviewed:
        if item["severity"] in {"high", "medium"}:
            owner_queues[item["dpia_owner"] or "unassigned"].append(str(item["triage_id"]))

    return {
        "summary": {
            "triage_items": len(reviewed),
            "high": severity_counts["high"],
            "medium": severity_counts["medium"],
            "low": severity_counts["low"],
            "decision_counts": dict(sorted(decision_counts.items())),
            "owner_queues": {owner: items for owner, items in sorted(owner_queues.items())},
        },
        "items": reviewed,
    }


def review_item(row: dict[str, str], as_of: date) -> dict[str, object]:
    flags: list[str] = []

    for column in ("triage_id", "system", "use_case", "data_subjects", "data_classification", "dpia_owner"):
        if not row[column]:
            flags.append(f"{column} missing")

    if truthy(row["special_category_data"]):
        flags.append("special category data involved")
    if truthy(row["children_or_students"]):
        flags.append("children or students involved")
    if truthy(row["automated_decisioning"]) and not truthy(row["human_review"]):
        flags.append("automated decisioning lacks human review")
    if truthy(row["large_scale_processing"]) and truthy(row["monitoring_or_tracking"]):
        flags.append("large-scale monitoring or tracking")
    if truthy(row["third_party_provider"]) and truthy(row["cross_border_transfer"]):
        flags.append("third-party cross-border processing")
    if not truthy(row["privacy_notice_updated"]):
        flags.append("privacy notice not updated")

    launch_date = parse_date(row["planned_launch_date"])
    if launch_date is None:
        flags.append("planned_launch_date missing")
    elif launch_date < as_of and row["status"].lower() not in {"launched", "closed", "retired"}:
        flags.append("planned launch date has passed")

    decision = row["triage_decision"].lower()
    if decision not in {"dpia_required", "formal_review", "monitor", "not_required", "review_complete"}:
        flags.append("triage decision is not recognized")
    if decision in {"not_required", "monitor"} and requires_formal_dpia(flags):
        flags.append("decision appears too low for DPIA triggers")

    return {
        "triage_id": row["triage_id"],
        "system": row["system"],
        "use_case": row["use_case"],
        "data_classification": row["data_classification"],
        "dpia_owner": row["dpia_owner"],
        "triage_decision": row["triage_decision"],
        "severity": severity_for(flags),
        "flags": flags,
        "recommended_action": recommended_action(flags),
    }


def requires_formal_dpia(flags: list[str]) -> bool:
    return any(
        marker in flag
        for marker in (
            "special category data",
            "children or students",
            "automated decisioning lacks",
            "large-scale monitoring",
            "third-party cross-border",
        )
        for flag in flags
    )


def severity_for(flags: list[str]) -> str:
    high_markers = (
        "special category data",
        "children or students",
        "automated decisioning lacks",
        "large-scale monitoring",
        "third-party cross-border",
        "decision appears too low",
    )
    if any(any(marker in flag for marker in high_markers) for flag in flags):
        return "high"
    if flags:
        return "medium"
    return "low"


def recommended_action(flags: list[str]) -> str:
    if any("decision appears too low" in flag for flag in flags):
        return "Escalate to a formal DPIA or privacy review before launch because triage triggers exceed the recorded decision."
    if any("automated decisioning" in flag for flag in flags):
        return "Define human review, appeal, and override controls before using AI-supported decisions."
    if any("children or students" in flag for flag in flags):
        return "Complete child/student data protection review and document safeguards before recruitment or deployment."
    if any("third-party cross-border" in flag for flag in flags):
        return "Confirm transfer mechanism, subprocessor terms, and regional controls before production use."
    if flags:
        return "Resolve DPIA triage gaps and update evidence before launch approval."
    return "DPIA triage item is suitable for routine governance review."


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
        "# AI DPIA Triage Report",
        "",
        f"- Triage items: `{summary['triage_items']}`",
        f"- High-risk triage gaps: `{summary['high']}`",
        f"- Medium-risk triage gaps: `{summary['medium']}`",
        "",
        "## Owner Queue",
        "",
        "| Owner | Triage items needing review |",
        "| --- | --- |",
    ]

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    if owner_queues:
        for owner, triage_ids in owner_queues.items():
            assert isinstance(triage_ids, list)
            lines.append(f"| {escape_cell(owner)} | {'; '.join(triage_ids)} |")
    else:
        lines.append("| none | none |")

    lines.extend([
        "",
        "## Findings",
        "",
        "| Triage | System | Decision | Owner | Severity | Flags | Recommended action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])

    for item in items:
        assert isinstance(item, dict)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(str(item["triage_id"])),
                    escape_cell(str(item["system"])),
                    escape_cell(str(item["triage_decision"])),
                    escape_cell(str(item["dpia_owner"] or "unassigned")),
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
    parser = argparse.ArgumentParser(description="Review AI DPIA triage triggers and owner queues.")
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
