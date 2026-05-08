# AI Incident Evidence Report

Use this report before incident review meetings, AI governance forums, internal audit preparation, or post-incident closure. It converts the incident evidence register into a prioritized queue of missing evidence, overdue remediation, and escalation gaps.

The report is designed for AI-specific incidents where normal security incident processes need extra evidence around prompts, outputs, retrieval context, model/provider behavior, agent tool actions, downstream workflow effects, privacy review, and communications decisions.

## Register

Start from `templates/ai-incident-evidence-register.csv` and record one row per AI-related incident, near miss, or material control failure.

Required fields:

- `incident_id`: Unique incident or case identifier.
- `system`: AI system, assistant, model workflow, agent, or platform involved.
- `incident_type`: Short category such as `prompt_data_exposure`, `unauthorized_tool_action`, `incorrect_answer`, `bias_or_harmful_output`, `vendor_outage`, or `external_email_error`.
- `severity`: Operational incident severity such as `critical`, `high`, `medium`, or `low`.
- `detected_at`: Detection date in `YYYY-MM-DD` format.
- `reported_at`: Reporting or escalation date in `YYYY-MM-DD` format.
- `incident_owner`: Person accountable for the incident record and closure decision.
- `containment_owner`: Person accountable for technical containment.
- `data_exposure`: Whether the incident involved possible data exposure.
- `tool_misuse`: Whether the incident involved an agent tool call, API action, workflow action, or automated downstream change.
- `model_or_provider`: Model, provider, runtime, or service involved.
- `affected_users`: Estimated affected user, record, or workflow count.
- `evidence_reference`: Case, ticket, folder, SIEM query, review package, or evidence link.
- `timeline_complete`: Whether the timeline covers detection, triage, containment, escalation, recovery, and review.
- `containment_evidence`: Whether containment proof exists for high-impact systems or actions.
- `logs_preserved`: Whether prompt, output, identity, retrieval, tool-call, and downstream system logs are preserved.
- `privacy_reviewed`: Whether privacy, legal, or data protection review is complete when data exposure is possible.
- `communications_prepared`: Whether user, stakeholder, regulator, provider, or internal communications are prepared.
- `root_cause_status`: Root-cause state such as `in_progress`, `complete`, or `validated`.
- `remediation_due`: Remediation due date in `YYYY-MM-DD` format.
- `status`: Incident lifecycle status such as `open`, `investigating`, `contained`, `remediating`, `monitoring`, `resolved`, or `closed`.
- `notes`: Additional context, assumptions, and next actions.

## Report Script

Generate a Markdown report:

```bash
python scripts/incident_evidence_report.py examples/ai-incident-evidence-sample.csv --as-of 2026-05-09
```

Generate JSON for dashboards or CI:

```bash
python scripts/incident_evidence_report.py examples/ai-incident-evidence-sample.csv --as-of 2026-05-09 --format json
```

Fail a release, closure, or audit gate when high-severity evidence gaps remain:

```bash
python scripts/incident_evidence_report.py examples/ai-incident-evidence-sample.csv --as-of 2026-05-09 --fail-on-high
```

## Finding States

The script prioritizes the incident evidence queue with these states:

| State | Severity | Meaning | Expected Action |
| --- | --- | --- | --- |
| `incident_owner_missing` | High | No named incident owner is accountable for closure. | Assign an owner and record accountability. |
| `containment_owner_missing` | High | No named containment owner is accountable for technical response. | Assign containment ownership before governance review. |
| `data_exposure_privacy_review_missing` | High | Possible AI data exposure exists without privacy/legal review evidence. | Complete review and attach evidence before closure. |
| `tool_misuse_logs_missing` | High | Agent tool or workflow misuse occurred without preserved logs. | Preserve prompt, output, identity, tool-call, and downstream system logs. |
| `containment_evidence_missing` | High | A high-severity incident lacks containment proof. | Attach containment evidence and reviewer conclusion. |
| `evidence_reference_missing` | Medium | The incident has no case, ticket, or evidence package reference. | Add evidence reference before closure review. |
| `timeline_incomplete` | Medium | The timeline does not cover detection through recovery. | Complete timeline and decision log. |
| `communications_gap` | Medium | A high-severity incident lacks prepared communications. | Prepare stakeholder, user, regulator, or provider communications. |
| `root_cause_incomplete` | Medium | Root cause is not complete for an open incident. | Complete analysis and remediation plan. |
| `remediation_overdue` | Medium | Remediation due date has passed. | Escalate to governance or risk owner. |
| `remediation_due_soon` | Medium | Remediation is approaching its due date. | Confirm evidence will be ready on time. |
| `current` | Low | Evidence is complete enough for current lifecycle state. | Continue normal review cadence. |
| `closed` | Low | Incident is closed and evidence is retained. | Retain evidence according to policy. |

## Review Questions

- Does the evidence package preserve prompts, outputs, retrieval context, model/provider details, tool-call logs, identity context, and downstream system events?
- If data exposure is possible, has privacy/legal review been completed and documented?
- If an agent took an action, is there proof of the action, authorization path, policy decision, and containment or rollback result?
- Does the incident timeline show detection, escalation, containment, recovery, communications, and closure decisions?
- Are remediation due dates realistic, owned, and tracked through evidence rather than status text alone?
- Are lessons learned mapped back to controls, evaluation cases, monitoring thresholds, and approval gates?
