# AI Evidence Quality Report

Use this report before release approval, internal audit preparation, governance forums, and control testing. It turns a flat evidence register into an owner queue for stale, missing, expired, unowned, or incomplete evidence.

## What The Report Reviews

| Review Area | Question |
| --- | --- |
| Ownership | Does every evidence item have a named owner? |
| Control mapping | Is each evidence item tied to a control ID? |
| Source quality | Does the record say where the evidence is stored or collected? |
| Freshness | Are `last_collected` and `next_due` populated? |
| Cadence | Does evidence age align with monthly, quarterly, semiannual, or annual review expectations? |
| Status | Is the evidence current, collected, approved, pending, required, or expired? |

## Run The Report

```bash
python scripts/evidence_quality_report.py --register examples/evidence-register-quality-sample.csv --as-of 2026-05-08
```

Generate JSON for dashboards or evidence repositories:

```bash
python scripts/evidence_quality_report.py --register evidence-register.csv --format json
```

Fail a release gate when high-risk evidence gaps exist:

```bash
python scripts/evidence_quality_report.py --register evidence-register.csv --fail-on-high
```

## Interpretation Guide

| Severity | Meaning |
| --- | --- |
| High | Evidence is overdue, expired, or missing an owner. |
| Medium | Evidence is incomplete, missing dates, not collected, or older than its stated cadence. |
| Low | Evidence is current enough for routine assurance review. |

## Recommended Workflow

1. Export the current evidence register before a governance review.
2. Run the report with the review date.
3. Route high and medium findings to evidence owners.
4. Refresh stale artifacts or link formal exceptions.
5. Store the report output with the approval package.
