# AI Tabletop Evidence Report

Use this report before production launch, major model/provider changes, internal audit, board assurance reviews, and incident-response maturity assessments. It converts the `ai-tabletop-exercise-evidence-register.csv` into an actionable queue for tabletop exercise evidence, decision logs, communications testing, technical containment, provider fallback, privacy/legal review, and remediation ownership.

## Review Objectives

- Confirm that high-impact AI incident scenarios have recent tabletop evidence.
- Verify that each exercise has a facilitator, participants, lesson owner, evidence reference, and remediation due date.
- Detect missing evidence packs, incomplete decision logs, untested containment, provider fallback gaps, legal/privacy review gaps, stale exercises, and overdue remediation.
- Group findings by lesson owner so governance, security, privacy, platform, and service teams can close gaps before release or audit.

## Register Fields

| Field | Purpose |
| --- | --- |
| `exercise_id` | Stable identifier for the tabletop exercise. |
| `scenario` | Scenario name, such as provider outage, prompt injection, data exposure, or agent tool misuse. |
| `system` | AI system, assistant, agent, workflow, or platform exercised. |
| `exercise_date` | Date of the tabletop exercise in `YYYY-MM-DD` format. |
| `facilitator` | Person or team that ran the exercise. |
| `participants` | Role-based participant list. |
| `evidence_reference` | Link or path to the evidence pack, after-action notes, decision log, or screenshots. |
| `incident_domain` | Provider outage, prompt injection, data exposure, agent tool misuse, continuity, privacy, or equivalent domain. |
| `severity_tested` | Low, medium, high, or critical scenario severity. |
| `decision_log_complete` | Whether decision and escalation timestamps were captured. |
| `communications_tested` | Whether internal, executive, vendor, and user-facing communications were exercised. |
| `technical_containment_tested` | Whether containment actions were exercised for tools, providers, credentials, RAG sources, or integrations. |
| `provider_fallback_tested` | Whether fallback routing, recovery, cost control, and provider status handling were exercised. |
| `legal_privacy_reviewed` | Whether privacy/legal review was included for data exposure or regulated-data scenarios. |
| `lessons_owner` | Accountable owner for lessons learned and remediation. |
| `remediation_due` | Due date for open remediation in `YYYY-MM-DD` format. |
| `status` | Open, in progress, completed, accepted, retired, or equivalent state. |
| `notes` | Additional context, evidence gaps, or remediation notes. |

## Report Command

```bash
python scripts/tabletop_evidence_report.py examples/ai-tabletop-exercise-evidence-sample.csv --as-of 2026-05-09
```

Generate JSON for dashboards or CI gates:

```bash
python scripts/tabletop_evidence_report.py examples/ai-tabletop-exercise-evidence-sample.csv --as-of 2026-05-09 --format json
```

Block a release review when high-severity tabletop gaps remain:

```bash
python scripts/tabletop_evidence_report.py examples/ai-tabletop-exercise-evidence-sample.csv --as-of 2026-05-09 --fail-on-high
```

## Severity Model

| State | Default Severity | Meaning |
| --- | --- | --- |
| `missing_evidence` | High for high/critical scenarios, otherwise medium | No evidence pack or after-action record is attached. |
| `missing_accountability` | Medium | Facilitator, participants, or lesson owner is missing. |
| `decision_log_gap` | High for high/critical scenarios, otherwise medium | Escalation decisions and timing cannot be reconstructed. |
| `technical_containment_gap` | High for high/critical scenarios, otherwise medium | Containment was not exercised for tools, providers, credentials, RAG sources, or integrations. |
| `provider_fallback_gap` | High for high/critical provider scenarios, otherwise medium | Fallback routing, recovery, cost control, or provider communications were not tested. |
| `legal_privacy_review_gap` | High | Privacy/legal review is missing for data exposure, privacy, or regulated-data scenarios. |
| `communications_gap` | Medium | Communications path was not exercised for a high-impact scenario. |
| `overdue_remediation` | High | Lessons learned remain open after the remediation due date. |
| `remediation_due_soon` | Medium | Remediation is approaching its due date. |
| `stale_tabletop` | Medium | Exercise evidence is older than the configured maximum age. |
| `current` | Low | Evidence is current and no immediate reporting gap is detected. |

## Review Workflow

1. Record exercises for provider outages, prompt injection, RAG data exposure, agent tool misuse, model/provider changes, and privacy scenarios.
2. Attach the exercise evidence pack, decision log, communications artifacts, containment notes, and after-action record.
3. Run the report before release, audit, governance committee, or board assurance review.
4. Route high-severity gaps to the lesson owner and system risk owner.
5. Re-run after remediation to confirm the exercise record is complete and current.

## Governance Notes

- Tabletop exercises should prove response readiness, not only meeting attendance.
- High-impact AI systems need evidence that technical containment, communications, fallback routing, privacy/legal triage, and decision logs can work under pressure.
- Evidence should be stored with restricted access when it includes sensitive system names, incident hypotheses, vulnerability details, or regulated data.
