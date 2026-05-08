from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING = ROOT / "controls" / "owasp-llm-2025-control-mapping.csv"
CONTROL_ID_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z]+-[A-Z]+-\d{3})\s*$", re.MULTILINE)
REQUIRED_COLUMNS = [
    "owasp_id",
    "risk_name",
    "governance_intent",
    "control_ids",
    "required_evidence",
    "release_gate",
    "monitoring_signal",
    "owner_role",
]


def read_control_ids() -> set[str]:
    catalog = (ROOT / "controls" / "control-catalog.yaml").read_text(encoding="utf-8")
    return set(CONTROL_ID_PATTERN.findall(catalog))


def read_mapping(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(f"{path} has unexpected columns")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if len(rows) != 10:
        raise ValueError("OWASP LLM 2025 mapping must contain exactly 10 risks")
    return rows


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    catalog_ids = read_control_ids()
    seen = set()

    for row in rows:
        risk_id = row["owasp_id"]
        if not re.fullmatch(r"LLM(0[1-9]|10):2025", risk_id):
            errors.append(f"{risk_id or '<blank>'} is not a valid OWASP LLM 2025 risk ID")
        if risk_id in seen:
            errors.append(f"{risk_id} is duplicated")
        seen.add(risk_id)

        for column in REQUIRED_COLUMNS:
            if not row[column]:
                errors.append(f"{risk_id} is missing {column}")

        for control_id in split_semicolon(row["control_ids"]):
            if control_id not in catalog_ids:
                errors.append(f"{risk_id} maps to unknown control ID: {control_id}")

    expected = {f"LLM{index:02d}:2025" for index in range(1, 11)}
    missing = sorted(expected - {row["owasp_id"] for row in rows})
    if missing:
        errors.append("Missing OWASP risks: " + ", ".join(missing))

    return errors


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    control_counter: Counter[str] = Counter()
    owner_queues: dict[str, list[str]] = defaultdict(list)
    risks_with_missing_gates: list[str] = []
    risks_with_missing_monitoring: list[str] = []

    for row in rows:
        risk = f"{row['owasp_id']} {row['risk_name']}"
        for control_id in split_semicolon(row["control_ids"]):
            control_counter[control_id] += 1
        owner_queues[row["owner_role"]].append(risk)
        if not row["release_gate"]:
            risks_with_missing_gates.append(risk)
        if not row["monitoring_signal"]:
            risks_with_missing_monitoring.append(risk)

    return {
        "total_risks": len(rows),
        "unique_controls": len(control_counter),
        "control_coverage": dict(sorted(control_counter.items())),
        "owner_queues": {owner: risks for owner, risks in sorted(owner_queues.items())},
        "risks_with_missing_gates": risks_with_missing_gates,
        "risks_with_missing_monitoring": risks_with_missing_monitoring,
    }


def render_markdown(rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    lines = [
        "# OWASP LLM 2025 Control Mapping Report",
        "",
        f"- Mapped OWASP risks: `{summary['total_risks']}`",
        f"- Unique toolkit controls covered: `{summary['unique_controls']}`",
        f"- Risks missing release gates: `{len(summary['risks_with_missing_gates'])}`",
        f"- Risks missing monitoring signals: `{len(summary['risks_with_missing_monitoring'])}`",
        "",
        "## Owner Queue",
        "",
        "| Owner role | OWASP risks |",
        "| --- | --- |",
    ]

    owner_queues = summary["owner_queues"]
    assert isinstance(owner_queues, dict)
    for owner, risks in owner_queues.items():
        assert isinstance(risks, list)
        lines.append(f"| {owner} | {'; '.join(risks)} |")

    lines.extend([
        "",
        "## Control Coverage",
        "",
        "| Control ID | Mapped OWASP risks |",
        "| --- | ---: |",
    ])

    control_coverage = summary["control_coverage"]
    assert isinstance(control_coverage, dict)
    for control_id, count in control_coverage.items():
        lines.append(f"| {control_id} | {count} |")

    lines.extend([
        "",
        "## Risk Mapping",
        "",
        "| OWASP risk | Toolkit controls | Release gate | Monitoring signal |",
        "| --- | --- | --- | --- |",
    ])

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{row['owasp_id']} {row['risk_name']}",
                    row["control_ids"],
                    row["release_gate"],
                    row["monitoring_signal"],
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize OWASP LLM 2025 control mapping coverage.")
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-on-missing-gate", action="store_true")
    args = parser.parse_args()

    rows = read_mapping(args.mapping)
    errors = validate_rows(rows)
    summary = summarize(rows)

    if args.fail_on_missing_gate and summary["risks_with_missing_gates"]:
        errors.append("One or more OWASP LLM risks are missing release gates")

    if errors:
        for error in errors:
            print(f"OWASP LLM mapping validation failed: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"summary": summary, "risks": rows}, indent=2))
    else:
        print(render_markdown(rows, summary), end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
