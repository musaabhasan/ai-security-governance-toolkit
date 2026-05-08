from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z]+-[A-Z]+-\d{3})\s*$", re.MULTILINE)
HIGH_IMPACT_ACTIONS = {
    "delete_record",
    "send_external_email",
    "change_access",
    "approve_request",
    "execute_code",
}
REQUIRED_CSV_HEADERS = {
    "agentic-risk-control-mapping.csv": [
        "risk_id",
        "risk_theme",
        "agentic_failure_mode",
        "control_ids",
        "required_evidence",
        "minimum_test",
        "release_gate",
        "monitoring_signal",
        "owner_role",
    ],
    "ai-agent-tool-inventory.csv": [
        "agent_name",
        "tool_name",
        "tool_type",
        "environment",
        "permission_level",
        "data_access",
        "approval_required",
        "logging_location",
        "owner",
        "review_date",
        "status",
        "notes",
    ],
    "ai-access-recertification-register.csv": [
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
    ],
    "ai-control-test-schedule.csv": [
        "control_id",
        "control_name",
        "system",
        "control_owner",
        "test_owner",
        "test_method",
        "test_cadence",
        "evidence_source",
        "last_tested",
        "next_due",
        "result",
        "remediation_due",
        "notes",
    ],
    "ai-control-test-evidence-examples.csv": [
        "pack_id",
        "control_id",
        "control_name",
        "system",
        "test_objective",
        "population",
        "sample_size",
        "evidence_source",
        "evidence_quality",
        "result",
        "exception_summary",
        "remediation_owner",
        "remediation_due",
        "next_test_due",
        "reviewer_notes",
    ],
    "ai-exception-register.csv": [
        "exception_id",
        "system",
        "control_reference",
        "exception_description",
        "risk_owner",
        "approved_by",
        "approval_date",
        "expiration_date",
        "compensating_control",
        "status",
        "review_notes",
    ],
    "ai-procurement-scoring-worksheet.csv": [
        "domain",
        "weight",
        "score_1_to_5",
        "weighted_score",
        "evidence_reference",
        "risk_notes",
        "required_action",
        "owner",
        "due_date",
        "status",
    ],
    "model-monitoring-kpi-register.csv": [
        "kpi_id",
        "system",
        "model_or_provider",
        "metric_category",
        "metric_name",
        "definition",
        "data_source",
        "threshold",
        "review_cadence",
        "owner",
        "escalation_trigger",
        "last_result",
        "status",
        "notes",
    ],
    "ai-risk-register.csv": [
        "risk_id",
        "use_case",
        "risk_statement",
        "risk_theme",
        "owner",
        "inherent_likelihood",
        "inherent_impact",
        "inherent_rating",
        "controls",
        "residual_likelihood",
        "residual_impact",
        "residual_rating",
        "decision",
        "status",
        "review_date",
    ],
    "ai-data-deletion-evidence-register.csv": [
        "request_id",
        "system",
        "processor",
        "data_subject_or_dataset",
        "deletion_scope",
        "requested_at",
        "due_date",
        "completed_at",
        "evidence_reference",
        "verification_method",
        "verifier",
        "status",
        "retention_exception",
        "next_review_date",
        "notes",
    ],
    "ai-third-party-dependency-register.csv": [
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
    ],
    "ai-tabletop-exercise-evidence-register.csv": [
        "exercise_id",
        "scenario",
        "system",
        "exercise_date",
        "facilitator",
        "participants",
        "evidence_reference",
        "incident_domain",
        "severity_tested",
        "decision_log_complete",
        "communications_tested",
        "technical_containment_tested",
        "provider_fallback_tested",
        "legal_privacy_reviewed",
        "lessons_owner",
        "remediation_due",
        "status",
        "notes",
    ],
    "ai-evaluation-evidence-register.csv": [
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
    ],
    "evidence-register.csv": [
        "evidence_id",
        "control_id",
        "evidence_name",
        "system",
        "owner",
        "source",
        "frequency",
        "last_collected",
        "next_due",
        "status",
        "notes",
    ],
}


def fail(message: str) -> None:
    raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_markdown_headings() -> None:
    for directory in ("templates", "playbooks", "policies"):
        for path in sorted((ROOT / directory).rglob("*.md")):
            text = read_text(path).strip()
            if not text.startswith("# "):
                fail(f"{path.relative_to(ROOT)} must start with a level-one heading")


def validate_template_index() -> None:
    index_path = ROOT / "templates" / "README.md"
    index_text = read_text(index_path)
    template_paths = sorted(path for path in (ROOT / "templates").glob("*.md") if path.name != "README.md")
    missing = [path.name for path in template_paths if f"]({path.name})" not in index_text]
    if missing:
        fail(f"templates/README.md is missing templates: {', '.join(missing)}")


def validate_control_catalog() -> None:
    catalog_text = read_text(ROOT / "controls" / "control-catalog.yaml")
    control_ids = CONTROL_ID_PATTERN.findall(catalog_text)
    if len(control_ids) < 10:
        fail("controls/control-catalog.yaml should contain at least ten controls")
    duplicates = sorted({control_id for control_id in control_ids if control_ids.count(control_id) > 1})
    if duplicates:
        fail(f"Duplicate control IDs found: {', '.join(duplicates)}")

    required_sections = ("objective:", "risk_themes:", "evidence:", "test:")
    for control_id in control_ids:
        start = catalog_text.index(f"id: {control_id}")
        next_match = CONTROL_ID_PATTERN.search(catalog_text, start + len(control_id))
        block = catalog_text[start : next_match.start() if next_match else len(catalog_text)]
        for section in required_sections:
            if section not in block:
                fail(f"{control_id} is missing {section}")


def validate_agentic_risk_control_mapping_assets() -> None:
    script_path = ROOT / "scripts" / "agentic_risk_control_report.py"
    guide_path = ROOT / "controls" / "agentic-risk-control-mapping.md"
    mapping_path = ROOT / "controls" / "agentic-risk-control-mapping.csv"
    markdown_report_path = ROOT / "examples" / "agentic-risk-control-report.md"
    json_report_path = ROOT / "examples" / "agentic-risk-control-report.json"

    for path in (script_path, guide_path, mapping_path, markdown_report_path, json_report_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("AR-001", "release gate", "monitoring signals", "--fail-on-missing-gate"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing agentic mapping guidance: {required}")

    catalog_ids = set(CONTROL_ID_PATTERN.findall(read_text(ROOT / "controls" / "control-catalog.yaml")))
    with mapping_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    with mapping_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    if header != REQUIRED_CSV_HEADERS["agentic-risk-control-mapping.csv"]:
        fail(f"{mapping_path.relative_to(ROOT)} has unexpected headers")
    if not rows:
        fail(f"{mapping_path.relative_to(ROOT)} is empty")
    if len(rows) < 8:
        fail(f"{mapping_path.relative_to(ROOT)} should include multiple agentic risk themes")

    risk_ids = [row["risk_id"] for row in rows]
    duplicates = sorted({risk_id for risk_id in risk_ids if risk_ids.count(risk_id) > 1})
    if duplicates:
        fail(f"Duplicate agentic risk IDs found: {', '.join(duplicates)}")

    for row in rows:
        missing = [column for column in REQUIRED_CSV_HEADERS["agentic-risk-control-mapping.csv"] if not row[column].strip()]
        if missing:
            fail(f"{row['risk_id']} is missing required mapping fields: {', '.join(missing)}")
        for control_id in [item.strip() for item in row["control_ids"].split(";") if item.strip()]:
            if control_id not in catalog_ids:
                fail(f"{row['risk_id']} maps to unknown control ID: {control_id}")

    markdown_report_text = read_text(markdown_report_path)
    for required in ("Mapped risk themes: `10`", "Owner Queue", "Control Coverage"):
        if required not in markdown_report_text:
            fail(f"{markdown_report_path.relative_to(ROOT)} is missing report section: {required}")

    json_report = json.loads(read_text(json_report_path))
    if json_report.get("summary", {}).get("mapped_risk_themes") != len(rows):
        fail(f"{json_report_path.relative_to(ROOT)} has an unexpected mapped risk count")


def validate_csv_templates() -> None:
    for path in sorted((ROOT / "templates").glob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        header = rows[0]
        if any(not column.strip() for column in header):
            fail(f"{path.relative_to(ROOT)} has an empty header column")
        if len(set(header)) != len(header):
            fail(f"{path.relative_to(ROOT)} has duplicate header columns")
        for index, row in enumerate(rows[1:], start=2):
            if len(row) != len(header):
                fail(f"{path.relative_to(ROOT)} row {index} has {len(row)} columns; expected {len(header)}")
        expected = REQUIRED_CSV_HEADERS.get(path.name)
        if expected is not None and header != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")


def validate_policy_as_code_examples() -> None:
    policy_path = ROOT / "policies" / "opa" / "agent_tool_policy.rego"
    allowed_path = ROOT / "policies" / "opa" / "example-input-allowed.json"
    denied_path = ROOT / "policies" / "opa" / "example-input-denied.json"

    policy_text = read_text(policy_path)
    for required in ("default allow := false", "high_impact_actions", "deny_reason contains"):
        if required not in policy_text:
            fail(f"{policy_path.relative_to(ROOT)} is missing policy construct: {required}")

    allowed = json.loads(read_text(allowed_path))
    denied = json.loads(read_text(denied_path))

    for path, example in ((allowed_path, allowed), (denied_path, denied)):
        validate_policy_input_shape(path, example)

    if not policy_example_allows(allowed):
        fail(f"{allowed_path.relative_to(ROOT)} should represent an allowed policy decision")
    if policy_example_allows(denied):
        fail(f"{denied_path.relative_to(ROOT)} should represent a denied policy decision")


def validate_exception_aging_report_assets() -> None:
    script_path = ROOT / "scripts" / "exception_aging_report.py"
    guide_path = ROOT / "templates" / "ai-exception-aging-report.md"
    sample_path = ROOT / "examples" / "ai-exception-register-sample.csv"

    for path in (script_path, guide_path, sample_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("expired", "missing_expiration", "expiring_soon", "--fail-on-expired"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing exception-aging guidance: {required}")

    with sample_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        fail(f"{sample_path.relative_to(ROOT)} is empty")
    expected = REQUIRED_CSV_HEADERS["ai-exception-register.csv"]
    if rows[0] != expected:
        fail(f"{sample_path.relative_to(ROOT)} has unexpected headers")
    if len(rows) < 4:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple exception states")


def validate_risk_register_report_assets() -> None:
    script_path = ROOT / "scripts" / "risk_register_report.py"
    guide_path = ROOT / "templates" / "ai-risk-register-report.md"

    for path in (script_path, guide_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("--fail-on-residual", "Residual risk counts by theme", "Owner review queue"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing risk-register report guidance: {required}")


def validate_data_deletion_evidence_assets() -> None:
    script_path = ROOT / "scripts" / "data_deletion_evidence_report.py"
    guide_path = ROOT / "templates" / "ai-data-deletion-evidence-report.md"
    register_path = ROOT / "templates" / "ai-data-deletion-evidence-register.csv"
    sample_path = ROOT / "examples" / "ai-data-deletion-evidence-sample.csv"

    for path in (script_path, guide_path, register_path, sample_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("overdue_deletion", "missing_completion_evidence", "unverified_completion", "--fail-on-high"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing deletion evidence guidance: {required}")

    expected = REQUIRED_CSV_HEADERS["ai-data-deletion-evidence-register.csv"]
    for path in (register_path, sample_path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        if rows[0] != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")
    if len(list(csv.reader(sample_path.open("r", encoding="utf-8", newline="")))) < 4:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple deletion states")


def validate_third_party_dependency_assets() -> None:
    script_path = ROOT / "scripts" / "third_party_dependency_report.py"
    guide_path = ROOT / "templates" / "ai-third-party-dependency-report.md"
    register_path = ROOT / "templates" / "ai-third-party-dependency-register.csv"
    sample_path = ROOT / "examples" / "ai-third-party-dependency-sample.csv"

    for path in (script_path, guide_path, register_path, sample_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in (
        "missing_dpa",
        "missing_subprocessor_transparency",
        "overdue_assurance_review",
        "--fail-on-high",
    ):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing third-party dependency guidance: {required}")

    expected = REQUIRED_CSV_HEADERS["ai-third-party-dependency-register.csv"]
    for path in (register_path, sample_path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        if rows[0] != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")
    if len(list(csv.reader(sample_path.open("r", encoding="utf-8", newline="")))) < 4:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple third-party dependency states")


def validate_tabletop_evidence_assets() -> None:
    script_path = ROOT / "scripts" / "tabletop_evidence_report.py"
    guide_path = ROOT / "templates" / "ai-tabletop-evidence-report.md"
    register_path = ROOT / "templates" / "ai-tabletop-exercise-evidence-register.csv"
    sample_path = ROOT / "examples" / "ai-tabletop-exercise-evidence-sample.csv"

    for path in (script_path, guide_path, register_path, sample_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("missing_evidence", "decision_log_gap", "provider_fallback_gap", "--fail-on-high"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing tabletop evidence guidance: {required}")

    expected = REQUIRED_CSV_HEADERS["ai-tabletop-exercise-evidence-register.csv"]
    for path in (register_path, sample_path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        if rows[0] != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")
    if len(list(csv.reader(sample_path.open("r", encoding="utf-8", newline="")))) < 4:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple tabletop exercise states")


def validate_evaluation_evidence_assets() -> None:
    script_path = ROOT / "scripts" / "evaluation_evidence_report.py"
    guide_path = ROOT / "templates" / "ai-evaluation-evidence-report.md"
    register_path = ROOT / "templates" / "ai-evaluation-evidence-register.csv"
    sample_path = ROOT / "examples" / "ai-evaluation-evidence-sample.csv"

    for path in (script_path, guide_path, register_path, sample_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in ("missing_dataset_lineage", "missing_security_cases", "stale_evaluation", "--fail-on-high"):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing evaluation evidence guidance: {required}")

    expected = REQUIRED_CSV_HEADERS["ai-evaluation-evidence-register.csv"]
    for path in (register_path, sample_path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        if rows[0] != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")
    if len(list(csv.reader(sample_path.open("r", encoding="utf-8", newline="")))) < 4:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple evaluation evidence states")


def validate_access_recertification_assets() -> None:
    script_path = ROOT / "scripts" / "access_recertification_report.py"
    guide_path = ROOT / "templates" / "ai-access-recertification-report.md"
    register_path = ROOT / "templates" / "ai-access-recertification-register.csv"
    sample_path = ROOT / "examples" / "ai-access-recertification-sample.csv"
    json_report_path = ROOT / "examples" / "ai-access-recertification-report.json"

    for path in (script_path, guide_path, register_path, sample_path, json_report_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    guide_text = read_text(guide_path)
    for required in (
        "separated_identity_still_active",
        "privileged_without_mfa",
        "unowned_token_or_service_account",
        "--fail-on-high",
    ):
        if required not in guide_text:
            fail(f"{guide_path.relative_to(ROOT)} is missing access recertification guidance: {required}")

    expected = REQUIRED_CSV_HEADERS["ai-access-recertification-register.csv"]
    for path in (register_path, sample_path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f"{path.relative_to(ROOT)} is empty")
        if rows[0] != expected:
            fail(f"{path.relative_to(ROOT)} has unexpected headers")
    if len(list(csv.reader(sample_path.open("r", encoding="utf-8", newline="")))) < 5:
        fail(f"{sample_path.relative_to(ROOT)} should include multiple access recertification states")

    json_report = json.loads(read_text(json_report_path))
    summary = json_report.get("summary", {})
    if summary.get("total") != 6:
        fail(f"{json_report_path.relative_to(ROOT)} has an unexpected total access count")
    if summary.get("high", 0) < 4:
        fail(f"{json_report_path.relative_to(ROOT)} should include high-severity access gaps")


def validate_policy_input_shape(path: Path, example: dict[str, object]) -> None:
    required_top_level = ("agent", "tool", "action", "data_classification", "human_approval")
    for field in required_top_level:
        if field not in example:
            fail(f"{path.relative_to(ROOT)} missing required field: {field}")

    agent = example["agent"]
    tool = example["tool"]
    human_approval = example["human_approval"]
    if not isinstance(agent, dict) or not isinstance(tool, dict) or not isinstance(human_approval, dict):
        fail(f"{path.relative_to(ROOT)} must use objects for agent, tool, and human_approval")

    for field in ("id", "approved", "allowed_tools"):
        if field not in agent:
            fail(f"{path.relative_to(ROOT)} missing agent.{field}")
    if "name" not in tool:
        fail(f"{path.relative_to(ROOT)} missing tool.name")
    if "approved" not in human_approval or "approver" not in human_approval:
        fail(f"{path.relative_to(ROOT)} missing human_approval approval fields")


def policy_example_allows(example: dict[str, object]) -> bool:
    agent = example["agent"]
    tool = example["tool"]
    human_approval = example["human_approval"]
    assert isinstance(agent, dict)
    assert isinstance(tool, dict)
    assert isinstance(human_approval, dict)

    if agent.get("approved") is not True:
        return False
    if tool.get("name") not in agent.get("allowed_tools", []):
        return False

    action = str(example["action"])
    if action in HIGH_IMPACT_ACTIONS:
        return human_approval.get("approved") is True and human_approval.get("approver") != agent.get("id")

    return example.get("data_classification") != "regulated"


def main() -> int:
    checks = [
        validate_markdown_headings,
        validate_template_index,
        validate_control_catalog,
        validate_agentic_risk_control_mapping_assets,
        validate_csv_templates,
        validate_policy_as_code_examples,
        validate_exception_aging_report_assets,
        validate_risk_register_report_assets,
        validate_data_deletion_evidence_assets,
        validate_third_party_dependency_assets,
        validate_tabletop_evidence_assets,
        validate_evaluation_evidence_assets,
        validate_access_recertification_assets,
    ]
    for check in checks:
        check()
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Repository validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
