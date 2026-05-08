from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z]+-[A-Z]+-\d{3})\s*$", re.MULTILINE)


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


def main() -> int:
    checks = [
        validate_markdown_headings,
        validate_template_index,
        validate_control_catalog,
        validate_csv_templates,
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
