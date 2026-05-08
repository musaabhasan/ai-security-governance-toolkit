# AI Exception Aging Report

Use this report before governance forums, risk acceptance reviews, internal audit preparation, and control testing to identify AI governance exceptions that are expired, expiring soon, missing expiration dates, or using inconsistent status values.

## Operating Purpose

AI exceptions should be temporary, owned, compensated, and reviewed before they become unmanaged residual risk. This report turns the exception register into a review queue so governance teams can focus on decisions instead of manually scanning spreadsheets.

## Required Inputs

- Current AI exception register using `templates/ai-exception-register.csv`
- Assessment date used for the review
- Warning window for upcoming expirations
- Risk owner, approver, compensating control, and status for each exception

## Review States

| State | Meaning | Expected Action |
| --- | --- | --- |
| `expired` | Open exception has passed its expiration date | Escalate for closure, reapproval, or compensating-control review |
| `missing_expiration` | Open exception has no expiration date | Add expiration and reapprove before relying on the exception |
| `expiring_soon` | Open exception expires inside the warning window | Schedule risk-owner review before expiry |
| `unknown_status` | Status is not recognized as open or closed | Normalize the status and confirm whether the exception is active |
| `active` | Exception remains within the approved validity window | Track through normal review cadence |
| `closed` | Exception is no longer active | Confirm evidence retention and closure notes |

## Command

```bash
python scripts/exception_aging_report.py examples/ai-exception-register-sample.csv --as-of 2026-05-08 --warning-days 45
```

Write Markdown or JSON output for reporting and automation:

```bash
python scripts/exception_aging_report.py examples/ai-exception-register-sample.csv --as-of 2026-05-08 --format json --output reports/exception-aging.json
```

Use `--fail-on-expired` in CI when expired or missing-expiration exceptions should block release promotion.

## Governance Questions

- Which exceptions need immediate risk-owner action?
- Which compensating controls require evidence before the next approval meeting?
- Which systems repeatedly request exceptions against the same control?
- Which exceptions should be converted into remediation work instead of renewed?
- Which closed exceptions need evidence retained for audit sampling?
