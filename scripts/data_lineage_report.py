from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "templates" / "ai-data-lineage-register.csv"
REQUIRED_COLUMNS = [
    "lineage_id",
    "system",
    "data_asset",
    "source_system",
    "source_owner",
    "data_classification",
    "processing_stage",
    "model_or_index_version",
    "downstream_use",
    "legal_basis_or_consent",
    "transformation_evidence",
    "quality_check",
    "retention_rule",
    "cross_border_transfer",
    "subprocessor",
    "review_owner",
    "last_reviewed",
    "next_review",
    "status",
    "notes",
]
SENSITIVE_CLASSIFICATIONS = {"confidential", "regulated", "restricted", "sensitive", "student", "personal"}


def read_register(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(f"{path} has unexpected columns")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def review(rows: list[dict[str, str]], as_of: date) -> dict[str, object]:
    reviewed = [review_lineage(row, as_of) for row in rows]
    severity_counts = Counter(item["severity"] for item in reviewed)
    classification_counts = Counter(item["data_classification"] or "unspecified" for item in reviewed)
    stage_counts = Counter(item["processing_stage"] or "unspecified" for item in reviewed)
    owner_queues: dict[str, list[str]] = defaultdict(list)

    for item in reviewed:
        owner = item["review_owner"] or item["source_owner"] or "unassigned"
        if item["severity"] in {"high", "medium"}:
            owner_queues[owner].append(str(item["lineage_id"]))

    return {
        "summary": {
            "lineage_items": len(reviewed),
            "high": severity_counts["high"],
            "medium": severity_counts["medium"],
            "low": severity_counts["low"],
            "classification_counts": dict(sorted(classification_counts.items())),
            "processing_stage_counts": dict(sorted(stage_counts.items())),
            "owner_queues": {owner: items for owner, items in sorted(owner_queues.items())},
        },
        "items": reviewed,
    }


def review_lineage(row: dict[str, str], as_of: date) -> dict[str, object]:
    flags: list[str] = []

    for column in (
        "lineage_id",
        "system",
        "data_asset",
        "source_system",
        "source_owner",
        "data_classification",
        "processing_stage",
        "downstream_use",
        "review_owner",
    ):
        if not row[column]:
            flags.append(f"{column} missing")

    classification = row["data_classification"].lower()
    if classification in SENSITIVE_CLASSIFICATIONS and not row["legal_basis_or_consent"]:
        flags.append("sensitive data missing legal basis or consent evidence")
    if classification in SENSITIVE_CLASSIFICATIONS and not row["retention_rule"]:
        flags.append("sensitive data missing retention rule")

    if not row["transformation_evidence"]:
        flags.append("transformation evidence missing")
    if row["quality_check"].lower() not in {"passed", "complete", "current", "reviewed"}:
        flags.append("quality check is not current")

    cross_border = row["cross_border_transfer"].lower()
    if cross_border in {"yes", "true", "y"} and not row["subprocessor"]:
        flags.append("cross-border transfer missing subprocessor record")

    last_reviewed = parse_date(row["last_reviewed"])
    next_review = parse_date(row["next_review"])
    if last_reviewed is None:
        flags.append("last_reviewed missing")
    if next_review is None:
        flags.append("next_review missing")
    elif next_review < as_of:
        flags.append("next_review is overdue")

    status = row["status"].lower()
    if status not in {"approved", "current", "draft", "retired", "blocked"}:
        flags.append("status is not recognized")
    if status in {"draft", "blocked"}:
        flags.append(f"lineage status is {status}")

    return {
        "lineage_id": row["lineage_id"],
        "system": row["system"],
        "data_asset": row["data_asset"],
        "source_system": row["source_system"],
        "data_classification": row["data_classification"],
        "processing_stage": row["processing_stage"],
        "review_owner": row["review_owner"],
        "severity": severity_for(flags),
        "flags": flags,
        "recommended_action": recommended_action(flags),
    }


def severity_for(flags: list[str]) -> str:
    high_markers = (
        "sensitive data missing legal basis",
        "cross-border transfer missing",
        "next_review is overdue",
        "source_owner missing",
        "review_owner missing",
        "lineage status is blocked",
    )
    if any(any(marker in flag for marker in high_markers) for flag in flags):
        return "high"
    if flags:
        return "medium"
    return "low"


def recommended_action(flags: list[str]) -> str:
    if any("legal basis" in flag for flag in flags):
        return "Record the lawful basis, consent scope, or approved data-use decision before relying on this data asset."
    if any("cross-border transfer" in flag for flag in flags):
        return "Link the approved subprocessor, transfer mechanism, and owner review before production use."
    if any("next_review is overdue" in flag for flag in flags):
        return "Refresh the lineage review and update downstream-use, retention, and quality evidence."
    if any("owner missing" in flag for flag in flags):
        return "Assign source and review owners so lineage issues can be remediated before governance review."
    if any("transformation evidence" in flag for flag in flags):
        return "Attach evidence that explains how the source data becomes prompts, embeddings, labels, features, or outputs."
    if flags:
        return "Resolve lineage metadata gaps before release, audit submission, or model/provider change approval."
    return "Lineage item is suitable for routine governance review."


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
        "# AI Data Lineage Report",
        "",
        f"- Lineage items: `{summary['lineage_items']}`",
        f"- High-risk lineage gaps: `{summary['high']}`",
        f"- Medium-risk lineage gaps: `{summary['medium']}`",
        "",
        "## Owner Review Queue",
        "",
        "| Owner | Lineage items needing review |",
        "| --- | --- |",
    ]

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    if owner_queues:
        for owner, lineage_ids in owner_queues.items():
            assert isinstance(lineage_ids, list)
            lines.append(f"| {escape_cell(owner)} | {'; '.join(lineage_ids)} |")
    else:
        lines.append("| none | none |")

    lines.extend([
        "",
        "## Findings",
        "",
        "| Lineage ID | System | Data asset | Classification | Stage | Owner | Severity | Flags | Recommended action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])

    for item in items:
        assert isinstance(item, dict)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(str(item["lineage_id"])),
                    escape_cell(str(item["system"])),
                    escape_cell(str(item["data_asset"])),
                    escape_cell(str(item["data_classification"])),
                    escape_cell(str(item["processing_stage"])),
                    escape_cell(str(item["review_owner"] or "unassigned")),
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
    parser = argparse.ArgumentParser(description="Review AI data lineage completeness, ownership, and governance readiness.")
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
