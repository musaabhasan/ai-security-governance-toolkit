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
        validate_csv_templates,
        validate_policy_as_code_examples,
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
