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
    "evaluation_id",
    "system",
    "evaluation_suite",
    "evaluation_type",
    "model_or_provider",
    "dataset_reference",
    "dataset_version",
    "prompt_version",
    "index_version",
    "cases_total",
    "pass_rate",
    "critical_failures",
    "high_failures",
    "human_review_completed",
    "security_cases_included",
    "bias_cases_included",
    "citation_cases_included",
    "last_run_date",
    "owner",
    "release_decision",
    "status",
    "notes",
]
YES_VALUES = {"yes", "true", "complete", "completed", "reviewed"}
OPEN_STATUSES = {"active", "open", "pilot", "production", "release_candidate", "pending"}
RELEASE_BLOCKING_DECISIONS = {"approve", "approved", "release", "released", "go", "go_live"}


@dataclass(frozen=True)
class EvaluationRecord:
    evaluation_id: str
    system: str
    evaluation_suite: str
    evaluation_type: str
    model_or_provider: str
    dataset_reference: str
    dataset_version: str
    prompt_version: str
    index_version: str
    cases_total: int
    pass_rate: float | None
    critical_failures: int
    high_failures: int
    human_review_completed: str
    security_cases_included: str
    bias_cases_included: str
    citation_cases_included: str
    last_run_date: str
    owner: str
    release_decision: str
    status: str
    days_since_run: int | None
    state: str
    severity: str
    action: str


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI evaluation evidence readiness report.")
    parser.add_argument("input", type=Path, help="Path to an AI evaluation evidence CSV register.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date in YYYY-MM-DD format.")
    parser.add_argument("--max-age-days", type=int, default=45, help="Maximum age for evaluation evidence.")
    parser.add_argument("--min-pass-rate", type=float, default=0.90, help="Minimum acceptable pass rate.")
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
    min_pass_rate: float,
) -> list[EvaluationRecord]:
    return [classify_evaluation(row, as_of, max_age_days, min_pass_rate) for row in rows]


def classify_evaluation(
    row: dict[str, str],
    as_of: date,
    max_age_days: int,
    min_pass_rate: float,
) -> EvaluationRecord:
    evaluation_id = row["evaluation_id"]
    cases_total = parse_int(row["cases_total"], f"{evaluation_id} cases_total")
    pass_rate = parse_optional_float(row["pass_rate"], f"{evaluation_id} pass_rate")
    critical_failures = parse_int(row["critical_failures"], f"{evaluation_id} critical_failures")
    high_failures = parse_int(row["high_failures"], f"{evaluation_id} high_failures")
    last_run_text = row["last_run_date"].strip()
    last_run_date = parse_iso_date(last_run_text, f"{evaluation_id} last_run_date") if last_run_text else None
    days_since_run = (as_of - last_run_date).days if last_run_date is not None else None
    release_decision = normalize(row["release_decision"])
    status = normalize(row["status"])
    active_or_release = status in OPEN_STATUSES or release_decision in RELEASE_BLOCKING_DECISIONS

    if not row["dataset_reference"] or not row["dataset_version"]:
        state = "missing_dataset_lineage"
        severity = "high"
        action = "Record dataset reference and version before relying on the evaluation."
    elif cases_total <= 0:
        state = "empty_evaluation_suite"
        severity = "high"
        action = "Add evaluation cases before using the suite for release evidence."
    elif critical_failures > 0:
        state = "critical_eval_failures"
        severity = "high"
        action = "Block release and remediate critical failures before approval."
    elif high_failures > 0:
        state = "high_eval_failures"
        severity = "high"
        action = "Review high-severity failures and document risk acceptance or remediation."
    elif pass_rate is None:
        state = "missing_pass_rate"
        severity = "medium"
        action = "Record pass rate or objective scoring result for the suite."
    elif pass_rate < min_pass_rate:
        state = "pass_rate_below_threshold"
        severity = "high" if active_or_release else "medium"
        action = "Tune, remediate, or downgrade release decision until the pass-rate threshold is met."
    elif active_or_release and not is_yes(row["human_review_completed"]):
        state = "missing_human_review"
        severity = "high"
        action = "Complete human review for representative failures, edge cases, and release-significant samples."
    elif active_or_release and not is_yes(row["security_cases_included"]):
        state = "missing_security_cases"
        severity = "high"
        action = "Add prompt-injection, data-exfiltration, tool-misuse, or abuse-case tests."
    elif "rag" in normalize(row["evaluation_type"]) and not is_yes(row["citation_cases_included"]):
        state = "missing_citation_cases"
        severity = "medium"
        action = "Add citation, source-support, and abstention cases for RAG evaluation."
    elif "education" in normalize(row["system"]) and not is_yes(row["bias_cases_included"]):
        state = "missing_bias_cases"
        severity = "medium"
        action = "Add bias, accessibility, and learner-impact cases for education-facing evaluation."
    elif not row["prompt_version"] or not row["model_or_provider"]:
        state = "missing_run_metadata"
        severity = "medium"
        action = "Record model/provider and prompt version so the evaluation can be reproduced."
    elif days_since_run is None:
        state = "missing_run_date"
        severity = "medium"
        action = "Record the last run date so evidence freshness can be assessed."
    elif days_since_run > max_age_days:
        state = "stale_evaluation"
        severity = "medium"
        action = "Refresh evaluation against the current model, prompt, index, and data sources."
    else:
        state = "current"
        severity = "low"
        action = "Keep evaluation in the normal release and monitoring cadence."

    return EvaluationRecord(
        evaluation_id=evaluation_id,
        system=row["system"],
        evaluation_suite=row["evaluation_suite"],
        evaluation_type=row["evaluation_type"],
        model_or_provider=row["model_or_provider"],
        dataset_reference=row["dataset_reference"],
        dataset_version=row["dataset_version"],
        prompt_version=row["prompt_version"],
        index_version=row["index_version"],
        cases_total=cases_total,
        pass_rate=pass_rate,
        critical_failures=critical_failures,
        high_failures=high_failures,
        human_review_completed=row["human_review_completed"],
        security_cases_included=row["security_cases_included"],
        bias_cases_included=row["bias_cases_included"],
        citation_cases_included=row["citation_cases_included"],
        last_run_date=last_run_text,
        owner=row["owner"],
        release_decision=row["release_decision"],
        status=row["status"],
        days_since_run=days_since_run,
        state=state,
        severity=severity,
        action=action,
    )


def parse_int(value: str, field_name: str) -> int:
    try:
        return int(value or "0")
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer: {value}") from exc


def parse_optional_float(value: str, field_name: str) -> float | None:
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a number: {value}") from exc
    if parsed > 1:
        parsed = parsed / 100
    if not 0 <= parsed <= 1:
        raise ValueError(f"{field_name} must be between 0 and 1 or 0 and 100: {value}")
    return parsed


def summarize(records: list[EvaluationRecord]) -> dict[str, object]:
    severity_counts = Counter(record.severity for record in records)
    state_counts = Counter(record.state for record in records)
    return {
        "total": len(records),
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
        "critical_eval_failures": state_counts["critical_eval_failures"],
        "high_eval_failures": state_counts["high_eval_failures"],
        "missing_human_review": state_counts["missing_human_review"],
        "missing_security_cases": state_counts["missing_security_cases"],
        "stale_evaluation": state_counts["stale_evaluation"],
    }


def render_markdown(records: list[EvaluationRecord], as_of: date, max_age_days: int, min_pass_rate: float) -> str:
    summary = summarize(records)
    lines = [
        "# AI Evaluation Evidence Report",
        "",
        f"- As of: `{as_of.isoformat()}`",
        f"- Evaluation maximum age: `{max_age_days}` days",
        f"- Minimum pass rate: `{min_pass_rate:.2f}`",
        f"- Total evaluations: `{summary['total']}`",
        f"- High-severity gaps: `{summary['high']}`",
        f"- Medium-severity gaps: `{summary['medium']}`",
        f"- Critical evaluation failures: `{summary['critical_eval_failures']}`",
        f"- High evaluation failures: `{summary['high_eval_failures']}`",
        f"- Missing human review: `{summary['missing_human_review']}`",
        f"- Missing security cases: `{summary['missing_security_cases']}`",
        f"- Stale evaluations: `{summary['stale_evaluation']}`",
        "",
        "## Evaluation Queue",
        "",
        "| Evaluation | System | Suite | Type | Pass Rate | Cases | State | Severity | Owner | Action |",
        "| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ]

    for record in sorted(records, key=record_sort_key):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_pipe(record.evaluation_id),
                    escape_pipe(record.system),
                    escape_pipe(record.evaluation_suite),
                    escape_pipe(record.evaluation_type),
                    "" if record.pass_rate is None else f"{record.pass_rate:.2f}",
                    str(record.cases_total),
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
            "| Owner | Evaluations | High | Medium | Action States |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for owner, owner_records in sorted(group_by_owner(records).items()):
        action_states = ", ".join(sorted({record.state for record in owner_records if record.state != "current"})) or "current"
        lines.append(
            "| {owner} | {count} | {high} | {medium} | {states} |".format(
                owner=escape_pipe(owner or "unassigned"),
                count=len(owner_records),
                high=sum(1 for record in owner_records if record.severity == "high"),
                medium=sum(1 for record in owner_records if record.severity == "medium"),
                states=escape_pipe(action_states),
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_json(records: list[EvaluationRecord], as_of: date, max_age_days: int, min_pass_rate: float) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "max_age_days": max_age_days,
        "min_pass_rate": min_pass_rate,
        "summary": summarize(records),
        "evaluations": [asdict(record) for record in sorted(records, key=record_sort_key)],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def group_by_owner(records: list[EvaluationRecord]) -> dict[str, list[EvaluationRecord]]:
    grouped: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for record in records:
        grouped[record.owner].append(record)
    return grouped


def record_sort_key(record: EvaluationRecord) -> tuple[int, str, str]:
    severity_order = {"high": 0, "medium": 1, "low": 2}
    return (severity_order.get(record.severity, 3), record.state, record.evaluation_id)


def normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def is_yes(value: str) -> bool:
    return normalize(value) in YES_VALUES


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    as_of = parse_iso_date(args.as_of, "as_of")
    if args.max_age_days < 0:
        raise ValueError("--max-age-days must be zero or greater")
    if not 0 <= args.min_pass_rate <= 1:
        raise ValueError("--min-pass-rate must be between 0 and 1")
    records = build_report(load_rows(args.input), as_of, args.max_age_days, args.min_pass_rate)
    output = (
        render_markdown(records, as_of, args.max_age_days, args.min_pass_rate)
        if args.format == "markdown"
        else render_json(records, as_of, args.max_age_days, args.min_pass_rate)
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
        print(f"evaluation evidence report failed: {exc}", file=sys.stderr)
        raise SystemExit(2)

