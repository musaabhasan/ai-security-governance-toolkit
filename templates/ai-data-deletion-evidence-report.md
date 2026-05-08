# AI Data Deletion Evidence Report

Use this report before governance forums, privacy reviews, vendor assurance reviews, RAG platform audits, and AI system decommissioning to confirm that deletion requests have evidence across prompts, outputs, uploaded files, embeddings, logs, vector stores, and third-party processors.

## Operating Purpose

AI systems often copy the same data into several places: prompt logs, generated outputs, file stores, vector indexes, evaluation datasets, model-provider logs, analytics events, and support tickets. A deletion request is not complete until every in-scope location has either deletion evidence or an approved retention exception.

This report turns the deletion evidence register into an owner queue so governance teams can identify:

- overdue deletion requests,
- completed requests with no evidence attached,
- completed requests that have not been independently verified,
- retention exceptions with missing or overdue review dates,
- processors that repeatedly delay or under-document deletion evidence.

## Required Inputs

- Current deletion evidence register using `templates/ai-data-deletion-evidence-register.csv`
- Assessment date for the review
- Due-date warning window
- Retention-exception review warning window
- Processor, system owner, verifier, evidence reference, and status for each request

## Review States

| State | Meaning | Expected Action |
| --- | --- | --- |
| `overdue_deletion` | Open deletion request is past due | Escalate overdue deletion to the system and processor owners |
| `missing_due_date` | Open request has no due date | Add deletion due date and processor owner |
| `missing_completion_evidence` | Request is marked completed but no evidence reference exists | Attach deletion evidence from the processor or storage owner |
| `unverified_completion` | Completion evidence exists but verification is missing | Record independent verification method and verifier |
| `exception_without_reason` | Retention exception exists without a reason | Document the retention exception reason and approving owner |
| `exception_missing_review` | Retention exception has no next review date | Add a review date for the retention exception |
| `exception_review_overdue` | Retention exception review date has passed | Escalate overdue retention-exception review |
| `deletion_due_soon` | Open request is approaching its due date | Confirm processor execution path before due date |
| `exception_review_due_soon` | Retention exception review is approaching | Schedule review before the due date |
| `retention_exception_active` | Retention exception is active and within review window | Monitor until approved deletion or renewal |
| `open` | Request is open and not yet due | Track through the normal deletion workflow |
| `verified` | Request has completion evidence and verification | Retain evidence through the approved retention period |

## Command

```bash
python scripts/data_deletion_evidence_report.py examples/ai-data-deletion-evidence-sample.csv --as-of 2026-05-08
```

Write Markdown or JSON output:

```bash
python scripts/data_deletion_evidence_report.py examples/ai-data-deletion-evidence-sample.csv --as-of 2026-05-08 --format json --output reports/deletion-evidence.json
```

Use `--fail-on-high` in CI or release checks when overdue deletions, missing completion evidence, or unmanaged retention exceptions should block rollout.

## Governance Questions

- Which processors have overdue deletion requests?
- Which completed requests are missing evidence or independent verification?
- Which vector stores, uploaded files, logs, or provider-side records remain in scope?
- Which retention exceptions need review before the next governance forum?
- Which systems repeatedly create deletion evidence gaps?
- Which evidence records should be sampled by internal audit or privacy teams?
