from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CROSSWALK = ROOT / "controls" / "nist-ai-rmf-control-crosswalk.csv"
CONTROL_ID_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z]+-[A-Z]+-\d{3})\s*$", re.MULTILINE)
REQUIRED_COLUMNS = [
    "rmf_function",
    "rmf_theme",
    "governance_objective",
    "control_ids",
    "required_evidence",
    "review_cadence",
    "owner_role",
]
REQUIRED_FUNCTIONS = {"GOVERN", "MAP", "MEASURE", "MANAGE"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(f"{path} has unexpected columns")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if len(rows) < 8:
        raise ValueError("NIST AI RMF crosswalk should include multiple governance themes")
    return rows


def catalog_ids() -> set[str]:
    text = (ROOT / "controls" / "control-catalog.yaml").read_text(encoding="utf-8")
    return set(CONTROL_ID_PATTERN.findall(text))


def validate(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    known_controls = catalog_ids()
    functions = {row["rmf_function"] for row in rows}
    missing_functions = sorted(REQUIRED_FUNCTIONS - functions)
    if missing_functions:
        errors.append("Missing NIST AI RMF functions: " + ", ".join(missing_functions))

    for index, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            if not row[column]:
                errors.append(f"row {index} is missing {column}")
        if row["rmf_function"] not in REQUIRED_FUNCTIONS:
            errors.append(f"row {index} uses unknown RMF function: {row['rmf_function']}")
        for control_id in split_semicolon(row["control_ids"]):
            if control_id not in known_controls:
                errors.append(f"row {index} maps to unknown control ID: {control_id}")
    return errors


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    by_function: Counter[str] = Counter(row["rmf_function"] for row in rows)
    by_control: Counter[str] = Counter()
    owner_queues: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        for control_id in split_semicolon(row["control_ids"]):
            by_control[control_id] += 1
        owner_queues[row["owner_role"]].append(f"{row['rmf_function']} - {row['rmf_theme']}")

    return {
        "total_rows": len(rows),
        "functions_covered": sorted(by_function),
        "function_coverage": dict(sorted(by_function.items())),
        "control_coverage": dict(sorted(by_control.items())),
        "owner_queues": {owner: queue for owner, queue in sorted(owner_queues.items())},
    }


def render_markdown(rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    lines = [
        "# NIST AI RMF Crosswalk Report",
        "",
        f"- Crosswalk rows: `{summary['total_rows']}`",
        f"- Functions covered: `{', '.join(summary['functions_covered'])}`",
        "",
        "## Function Coverage",
        "",
        "| Function | Rows |",
        "| --- | ---: |",
    ]
    for function, count in summary["function_coverage"].items():
        lines.append(f"| {function} | {count} |")

    lines.extend(["", "## Owner Queue", "", "| Owner role | Themes |", "| --- | --- |"])
    for owner, themes in summary["owner_queues"].items():
        lines.append(f"| {owner} | {'; '.join(themes)} |")

    lines.extend(["", "## Crosswalk", "", "| Function | Theme | Controls | Evidence | Cadence |", "| --- | --- | --- | --- | --- |"])
    for row in rows:
        lines.append(
            f"| {row['rmf_function']} | {row['rmf_theme']} | {row['control_ids']} | "
            f"{row['required_evidence']} | {row['review_cadence']} |"
        )
    return "\n".join(lines) + "\n"


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize NIST AI RMF control crosswalk coverage.")
    parser.add_argument("--crosswalk", type=Path, default=DEFAULT_CROSSWALK)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-on-missing-function", action="store_true")
    args = parser.parse_args()

    rows = read_rows(args.crosswalk)
    errors = validate(rows)
    summary = summarize(rows)
    if args.fail_on_missing_function and set(summary["functions_covered"]) != REQUIRED_FUNCTIONS:
        errors.append("Crosswalk does not cover every NIST AI RMF function")

    if errors:
        for error in errors:
            print(f"NIST AI RMF crosswalk validation failed: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"summary": summary, "rows": rows}, indent=2))
    else:
        print(render_markdown(rows, summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
