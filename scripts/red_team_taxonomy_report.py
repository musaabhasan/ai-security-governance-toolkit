from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY = ROOT / "controls" / "ai-red-team-finding-taxonomy.csv"
CONTROL_ID_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z]+-[A-Z]+-\d{3})\s*$", re.MULTILINE)
REQUIRED_COLUMNS = [
    "finding_type",
    "risk_theme",
    "severity_floor",
    "example_signal",
    "control_ids",
    "required_evidence",
    "release_decision",
    "owner_role",
]
SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def read_control_ids() -> set[str]:
    catalog = (ROOT / "controls" / "control-catalog.yaml").read_text(encoding="utf-8")
    return set(CONTROL_ID_PATTERN.findall(catalog))


def read_taxonomy(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(f"{path} has unexpected columns")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    catalog_ids = read_control_ids()
    finding_types = [row["finding_type"] for row in rows]
    duplicates = sorted({item for item in finding_types if finding_types.count(item) > 1})

    if len(rows) < 8:
        errors.append("red-team taxonomy should include at least eight finding types")
    if duplicates:
        errors.append("duplicate finding types: " + ", ".join(duplicates))

    for index, row in enumerate(rows, start=2):
        label = row["finding_type"] or f"row {index}"
        for column in REQUIRED_COLUMNS:
            if not row[column]:
                errors.append(f"{label} is missing {column}")

        severity = row["severity_floor"].lower()
        if severity not in SEVERITY_ORDER:
            errors.append(f"{label} has unknown severity_floor: {row['severity_floor']}")

        for control_id in split_semicolon(row["control_ids"]):
            if control_id not in catalog_ids:
                errors.append(f"{label} maps to unknown control ID: {control_id}")

    return errors


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    severity_counts: Counter[str] = Counter()
    theme_counts: Counter[str] = Counter()
    control_counter: Counter[str] = Counter()
    owner_queues: dict[str, list[str]] = defaultdict(list)
    release_holds: list[str] = []

    for row in rows:
        severity = row["severity_floor"].lower()
        severity_counts[severity] += 1
        theme_counts[row["risk_theme"]] += 1
        owner_queues[row["owner_role"]].append(row["finding_type"])
        for control_id in split_semicolon(row["control_ids"]):
            control_counter[control_id] += 1
        if row["release_decision"].lower().startswith("hold release"):
            release_holds.append(row["finding_type"])

    return {
        "finding_types": len(rows),
        "severity_counts": dict(sorted(severity_counts.items())),
        "risk_theme_counts": dict(sorted(theme_counts.items())),
        "control_coverage": dict(sorted(control_counter.items())),
        "owner_queues": {owner: findings for owner, findings in sorted(owner_queues.items())},
        "release_holds": release_holds,
    }


def render_markdown(rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    lines = [
        "# AI Red-Team Finding Taxonomy Report",
        "",
        f"- Finding types: `{summary['finding_types']}`",
        f"- Release-hold finding types: `{len(summary['release_holds'])}`",
        f"- Owner queues: `{len(summary['owner_queues'])}`",
        "",
        "## Severity Mix",
        "",
        "| Severity floor | Finding types |",
        "| --- | ---: |",
    ]

    severity_counts = summary["severity_counts"]
    assert isinstance(severity_counts, dict)
    for severity, count in severity_counts.items():
        lines.append(f"| {severity} | {count} |")

    lines.extend([
        "",
        "## Owner Queue",
        "",
        "| Owner role | Finding types |",
        "| --- | --- |",
    ])

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    for owner, findings in owner_queues.items():
        assert isinstance(findings, list)
        lines.append(f"| {owner} | {'; '.join(findings)} |")

    lines.extend([
        "",
        "## Control Coverage",
        "",
        "| Control ID | Finding types mapped |",
        "| --- | ---: |",
    ])

    control_coverage = summary["control_coverage"]
    assert isinstance(control_coverage, dict)
    for control_id, count in control_coverage.items():
        lines.append(f"| {control_id} | {count} |")

    lines.extend([
        "",
        "## Taxonomy Detail",
        "",
        "| Finding type | Severity floor | Controls | Release decision |",
        "| --- | --- | --- | --- |",
    ])

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["finding_type"],
                    row["severity_floor"],
                    row["control_ids"],
                    row["release_decision"],
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def has_unowned_high(rows: list[dict[str, str]]) -> bool:
    for row in rows:
        severity = row["severity_floor"].lower()
        if SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER["high"] and not row["owner_role"]:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize AI red-team finding taxonomy coverage.")
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-on-unowned-high", action="store_true")
    args = parser.parse_args()

    rows = read_taxonomy(args.taxonomy)
    errors = validate_rows(rows)
    if args.fail_on_unowned_high and has_unowned_high(rows):
        errors.append("one or more critical or high-severity finding types lack owner_role")

    if errors:
        for error in errors:
            print(f"Red-team taxonomy validation failed: {error}", file=sys.stderr)
        return 1

    summary = summarize(rows)
    if args.format == "json":
        print(json.dumps({"summary": summary, "taxonomy": rows}, indent=2))
    else:
        print(render_markdown(rows, summary), end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
