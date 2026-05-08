# AI Access Recertification Report

Use this report to review access to AI systems, assistants, RAG platforms, model operations consoles, administrative portals, service accounts, API keys, and agent tool permissions.

## Purpose

AI access reviews need to cover more than human users. A complete recertification should include:

- privileged administrators,
- student or customer support roles,
- service accounts and API tokens,
- break-glass access,
- agent tool permissions,
- data access to prompts, outputs, embeddings, files, or learner records,
- high-impact actions such as delete, deploy, approve, send, grant, merge, or execute.

## Input Register

Use `templates/ai-access-recertification-register.csv` or `examples/ai-access-recertification-sample.csv`.

| Column | Purpose |
| --- | --- |
| `access_id` | Stable identifier for the access assignment. |
| `system` | AI system, assistant, portal, model operations tool, or agent runtime. |
| `identity` | User, group, service account, token, or API key name. |
| `identity_type` | `user`, `group`, `service_account`, `api_token`, or similar. |
| `role` | Business or technical role. |
| `permission_level` | Read, write, manage, admin, owner, privileged, or equivalent. |
| `data_access` | Data classes or datasets the identity can access. |
| `tool_access` | Agent tools, workflow actions, APIs, or model operations available to the identity. |
| `owner` | Named accountable owner for the access. |
| `business_justification` | Why the access is needed. |
| `last_login_date` | Last observed use in `YYYY-MM-DD` format. |
| `last_review_date` | Last recertification date in `YYYY-MM-DD` format. |
| `mfa_enabled` | Whether MFA or equivalent strong authentication is enabled. |
| `break_glass` | Whether the access is emergency or break-glass access. |
| `api_key_or_token` | Whether the identity uses a key, token, or non-human credential. |
| `status` | Active, disabled, suspended, revoked, removed, or similar. |
| `employment_status` | Active, transferred, terminated, departed, unknown, or equivalent. |
| `review_decision` | Approved, retain, remove, pending, or needs_review. |
| `next_review_date` | Next review date in `YYYY-MM-DD` format. |
| `notes` | Reviewer notes and evidence references. |

## Run The Report

```bash
python scripts/access_recertification_report.py examples/ai-access-recertification-sample.csv --as-of 2026-05-09
```

Use a release or audit gate:

```bash
python scripts/access_recertification_report.py examples/ai-access-recertification-sample.csv --fail-on-high
```

Export JSON for dashboards:

```bash
python scripts/access_recertification_report.py examples/ai-access-recertification-sample.csv --format json --output examples/ai-access-recertification-report.json
```

## Review States

| State | Meaning |
| --- | --- |
| `separated_identity_still_active` | A terminated, departed, transferred, or unknown identity still has active access. |
| `privileged_without_mfa` | Privileged or break-glass access lacks MFA evidence. |
| `unowned_token_or_service_account` | Non-human credential lacks a named owner. |
| `break_glass_not_approved` | Emergency access is not approved or retained by review. |
| `high_impact_tool_access_unapproved` | Tool access can change systems or send data but has not been approved. |
| `privileged_review_missing` | Privileged access lacks a review record. |
| `privileged_review_overdue` | Privileged access review is older than the allowed threshold. |
| `stale_active_access` | Active access has not been used within the inactivity threshold. |
| `review_overdue` | Standard access review is older than the allowed threshold. |
| `current` | Access is inside the review cadence. |

## Governance Use

- Run the report before launch, renewal, audit testing, and major model/provider changes.
- Treat high-severity items as release-blocking unless a documented compensating control exists.
- Rotate or revoke unowned keys and service accounts.
- Require explicit approval and evidence for break-glass access.
- Review high-impact tool access separately from ordinary read-only access.
