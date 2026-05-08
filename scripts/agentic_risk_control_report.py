from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_COLUMNS = [
    "risk_id",
    "risk_theme",
    "agentic_failure_mode",
    "control_ids",
    "required_evidence",
    "minimum_test",
    "release_gate",
    "monitoring_signal",
    "owner_role",
]


@dataclass(frozen=True)
class AgenticRiskMapping:
    risk_id: str
    risk_theme: str
    agentic_failure_mode: str
    control_ids: list[str]
    required_evidence: list[str]
    minimum_test: str
    release_gate: str
    monitoring_signal: str
    owner_role: str


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError("CSV header does not match the expected agentic risk mapping schema.")
        return list(reader)


def build_mappings(rows: list[dict[str, str]]) -> list[AgenticRiskMapping]:
    mappings: list[AgenticRiskMapping] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        risk_id = row["risk_id"].strip()
        if not risk_id:
            raise ValueError(f"row {index} is missing risk_id")
        if risk_id in seen_ids:
            raise ValueError(f"duplicate risk_id: {risk_id}")
        seen_ids.add(risk_id)

        missing = [column for column in REQUIRED_COLUMNS if not row[column].strip()]
        if missing:
            raise ValueError(f"{risk_id} is missing required fields: {', '.join(missing)}")

        mappings.append(
            AgenticRiskMapping(
                risk_id=risk_id,
                risk_theme=row["risk_theme"].strip(),
                agentic_failure_mode=row["agentic_failure_mode"].strip(),
                control_ids=split_semicolon(row["control_ids"]),
                required_evidence=split_semicolon(row["required_evidence"]),
                minimum_test=row["minimum_test"].strip(),
                release_gate=row["release_gate"].strip(),
                monitoring_signal=row["monitoring_signal"].strip(),
                owner_role=row["owner_role"].strip(),
            )
        )
    return mappings


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def render_markdown(mappings: list[AgenticRiskMapping]) -> str:
    owner_counts = Counter(mapping.owner_role for mapping in mappings)
    control_counts = Counter(control_id for mapping in mappings for control_id in mapping.control_ids)

    lines = [
        "# Agentic Risk Control Mapping Report",
        "",
        f"Mapped risk themes: `{len(mappings)}`",
        "",
        "## Owner Queue",
        "",
        "| Owner Role | Risk Themes |",
        "| --- | ---: |",
    ]
    for owner, count in sorted(owner_counts.items()):
        lines.append(f"| {escape_cell(owner)} | {count} |")

    lines.extend(
        [
            "",
            "## Control Coverage",
            "",
            "| Control ID | Mapped Risk Themes |",
            "| --- | ---: |",
        ]
    )
    for control_id, count in sorted(control_counts.items()):
        lines.append(f"| `{escape_cell(control_id)}` | {count} |")

    lines.extend(
        [
            "",
            "## Mapping Detail",
            "",
            "| Risk ID | Theme | Failure Mode | Controls | Release Gate | Monitoring Signal | Owner |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for mapping in mappings:
        lines.append(
            "| {risk_id} | {theme} | {failure} | {controls} | {gate} | {signal} | {owner} |".format(
                risk_id=escape_cell(mapping.risk_id),
                theme=escape_cell(mapping.risk_theme),
                failure=escape_cell(mapping.agentic_failure_mode),
                controls=", ".join(f"`{escape_cell(control_id)}`" for control_id in mapping.control_ids),
                gate=escape_cell(mapping.release_gate),
                signal=escape_cell(mapping.monitoring_signal),
                owner=escape_cell(mapping.owner_role),
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_json(mappings: list[AgenticRiskMapping]) -> str:
    owner_counts = Counter(mapping.owner_role for mapping in mappings)
    control_counts = Counter(control_id for mapping in mappings for control_id in mapping.control_ids)
    payload = {
        "summary": {
            "mapped_risk_themes": len(mappings),
            "owner_queue": dict(sorted(owner_counts.items())),
            "control_coverage": dict(sorted(control_counts.items())),
        },
        "mappings": [asdict(mapping) for mapping in mappings],
    }
    return json.dumps(payload, indent=2)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_output(text: str, output: Path | None) -> None:
    if output is None:
        print(text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an agentic risk control mapping report.")
    parser.add_argument("input", type=Path, help="Path to controls/agentic-risk-control-mapping.csv.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", type=Path, help="Optional output path.")
    parser.add_argument(
        "--fail-on-missing-gate",
        action="store_true",
        help="Exit with code 1 when any mapped risk has no release gate.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    mappings = build_mappings(load_rows(args.input))
    report = render_json(mappings) if args.format == "json" else render_markdown(mappings)
    write_output(report, args.output)
    missing_gate = any(not mapping.release_gate.strip() for mapping in mappings)
    return 1 if args.fail_on_missing_gate and missing_gate else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"agentic risk control report failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
