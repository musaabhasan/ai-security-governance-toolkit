# AI DPIA Triage Report

Use this report before approving an AI system, assistant, agent, model change, analytics workflow, or education research tool that processes personal, student, staff, applicant, or sensitive operational data. It turns `templates/ai-dpia-triage-register.csv` into a queue for privacy owners and governance reviewers.

## When To Use

- Before a student-facing or employee-facing AI workflow launches.
- Before AI-assisted decisions, predictions, ranking, triage, or recommendations are used operationally.
- Before prompt logs, transcripts, learning analytics, or support tickets are reused for model evaluation or research.
- Before third-party providers process personal data or cross-border transfers are enabled.

## DPIA Triggers

Treat the following as formal review triggers:

- children, students, or vulnerable data subjects,
- special category, regulated, confidential, or highly sensitive data,
- automated decisioning without meaningful human review,
- large-scale monitoring or tracking,
- third-party cross-border processing,
- privacy notices not updated for the AI use case.

## Command Examples

Generate a Markdown report:

```bash
python scripts/dpia_triage_report.py examples/ai-dpia-triage-sample.csv --as-of 2026-05-09
```

Generate JSON for governance dashboards:

```bash
python scripts/dpia_triage_report.py examples/ai-dpia-triage-sample.csv --format json
```

Fail a release gate when high-risk triage gaps exist:

```bash
python scripts/dpia_triage_report.py examples/ai-dpia-triage-sample.csv --as-of 2026-05-09 --fail-on-high
```

## Owner Queue

The owner queue should be reviewed by the privacy owner, AI governance owner, system owner, and data owner. A `monitor` or `not_required` decision should be reconsidered when the trigger profile includes students, automated decisioning, large-scale monitoring, or cross-border processing.

## Evidence To Retain

- DPIA triage register.
- Privacy notice or participant notice reference.
- Human-review and appeal workflow evidence.
- Provider and transfer review evidence.
- Data minimization, retention, and deletion controls.
- Final privacy decision and launch approval.
