# AI Red-Team Finding Taxonomy

This taxonomy gives red-team findings a consistent language for governance review. It is designed to sit between test execution and release approval so findings can be grouped by risk theme, minimum severity, control coverage, required evidence, owner role, and release decision.

## Why This Matters

AI red-team work can lose value when findings are written as isolated narratives. A taxonomy helps teams compare findings across systems, identify repeated control failures, route issues to accountable owners, and defend release decisions with consistent evidence.

Use the taxonomy with:

- `templates/ai-red-team-test-plan.md`
- `templates/prompt-injection-test-record.md`
- `templates/ai-evaluation-evidence-register.csv`
- `templates/ai-control-test-evidence-pack.md`
- `templates/ai-incident-evidence-register.csv`

## Taxonomy Columns

| Column | Meaning |
| --- | --- |
| `finding_type` | Stable identifier for the red-team finding class. |
| `risk_theme` | Governance theme used for trend reporting and owner queues. |
| `severity_floor` | Minimum severity before compensating controls or context adjustments. |
| `example_signal` | Observable behavior that indicates this finding type. |
| `control_ids` | Toolkit controls expected to prevent, detect, or contain the issue. |
| `required_evidence` | Evidence needed before remediation can be accepted. |
| `release_decision` | Default release stance for unresolved findings. |
| `owner_role` | Primary role accountable for remediation or risk acceptance. |

## Operating Model

1. Classify each finding with one `finding_type`.
2. Record evidence listed in `required_evidence`.
3. Map remediation to the listed `control_ids`.
4. Route findings by `owner_role`.
5. Apply the default `release_decision` unless the risk owner documents a narrower decision.
6. Retest and attach evidence before closing high or critical findings.

## Report Command

```bash
python scripts/red_team_taxonomy_report.py
```

Generate JSON output for dashboards or evidence systems:

```bash
python scripts/red_team_taxonomy_report.py --format json
```

Block governance approval if any critical or high-severity taxonomy row lacks an owner:

```bash
python scripts/red_team_taxonomy_report.py --fail-on-unowned-high
```

## Review Cadence

Review the taxonomy after:

- a major model or provider change,
- a new agent tool integration,
- a significant prompt or retrieval redesign,
- a high-severity AI incident,
- repeated findings in the same risk theme,
- quarterly governance review.

The taxonomy should be versioned with the same care as prompts, model configurations, and control mappings because it affects release decisions and remediation accountability.
