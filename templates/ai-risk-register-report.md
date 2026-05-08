# AI Risk Register Report

Use this report before AI governance forums, control reviews, internal audit planning, and quarterly risk committee updates. It turns `templates/ai-risk-register.csv` into owner, theme, residual-rating, and review-date summaries.

## Operating Purpose

AI risk registers can become static inventories unless they are converted into recurring review queues. This report helps teams identify high residual risks, overdue reviews, upcoming owner actions, and themes where controls may need stronger evidence or redesign.

## Command

```bash
python scripts/risk_register_report.py templates/ai-risk-register.csv --as-of 2026-05-08 --review-warning-days 45
```

Write JSON for dashboards or evidence repositories:

```bash
python scripts/risk_register_report.py templates/ai-risk-register.csv --as-of 2026-05-08 --format json --output reports/ai-risk-register-report.json
```

Fail a pipeline or governance gate when open residual risks exceed a threshold:

```bash
python scripts/risk_register_report.py templates/ai-risk-register.csv --fail-on-residual high
```

## Review Outputs

- Residual risk counts by theme
- Owner review queue with maximum residual rating
- Overdue and upcoming review dates
- Risk-level action guidance
- JSON output for dashboards, evidence packs, or audit workpapers

## Governance Questions

- Which open risks still have high or critical residual exposure?
- Which risk owners have overdue or upcoming reviews?
- Which risk themes are accumulating medium or high residual exposure?
- Which mitigation decisions need evidence from the control test schedule?
- Which accepted risks need formal expiration, exception, or executive approval records?
