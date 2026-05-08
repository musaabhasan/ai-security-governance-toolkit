# Model Monitoring KPI Register

Use this register after an AI system is approved for pilot, production, or material expansion. It translates model monitoring into measurable indicators with owners, thresholds, review cadence, escalation triggers, and evidence sources.

## 1. Monitoring Context

| Field | Response |
| --- | --- |
| AI system | |
| Business owner | |
| Technical owner | |
| Risk owner | |
| Model or provider | |
| Deployment environment | Pilot / production / restricted production / internal lab |
| Use case risk tier | Low / moderate / high / prohibited until remediated |
| Data classifications | Public / internal / confidential / regulated / student / employee / customer |
| Monitoring period | |
| Review forum | AI governance board / security review / product review / audit committee |

## 2. KPI Categories

| Category | Purpose | Example Evidence |
| --- | --- | --- |
| Quality and task performance | Confirms the system remains useful for approved use cases. | Evaluation results, sampled reviews, benchmark results, user feedback. |
| Safety and policy behavior | Detects harmful outputs, policy violations, and unsafe tool use. | Safety classifier logs, human review, blocked actions, red-team regression results. |
| Data and retrieval integrity | Checks source quality, stale context, leakage risk, and RAG citation behavior. | Retrieval logs, source freshness reports, citation audits, ingestion records. |
| Drift and change detection | Identifies model, prompt, data, user, or provider changes that affect risk. | Version history, traffic patterns, embedding distribution reports, provider notices. |
| Security and abuse resistance | Measures prompt injection, credential exposure, excessive permission, and misuse signals. | Security events, tool-call logs, attack simulation results, incident tickets. |
| Reliability and continuity | Tracks latency, availability, fallback performance, and incident recovery. | Uptime reports, latency percentiles, fallback counts, outage records. |
| Cost and usage governance | Prevents uncontrolled consumption and unsupported expansion. | Token spend, user/group usage, budget alerts, exception approvals. |
| Human oversight | Verifies that human review, approvals, appeals, and escalation paths remain active. | Approval logs, sampled overrides, appeal records, supervisor review notes. |

## 3. KPI Register

| KPI ID | Metric Category | Metric Name | Definition | Data Source | Threshold | Review Cadence | Owner | Escalation Trigger | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KPI-001 | Quality | Task success rate | Percentage of sampled outputs meeting task rubric criteria. | Human review sample | Below 85% | Monthly | Product owner | Two consecutive misses | |
| KPI-002 | Safety | Policy violation rate | Share of outputs or actions violating content, privacy, or tool-use policy. | Safety logs and sampled review | Above 1% or any critical event | Weekly | Risk owner | Critical violation | |
| KPI-003 | Retrieval | Unsupported citation rate | Percentage of cited claims not supported by retrieved source text. | Citation audit | Above 5% | Monthly | Knowledge owner | High-impact unsupported claim | |
| KPI-004 | Drift | Prompt or model change without approval | Count of production changes missing approval record. | Change log | Any occurrence | Weekly | Technical owner | Unapproved change | |
| KPI-005 | Security | Prompt injection success rate | Percentage of test cases where injected content influenced instructions, secrets, or tools. | Red-team regression tests | Above 0% for high-impact tools | Release and quarterly | Security owner | Successful tool or data misuse | |
| KPI-006 | Reliability | P95 response latency | 95th percentile user-facing response latency. | Observability metrics | Above agreed SLA | Weekly | Platform owner | SLA breach | |
| KPI-007 | Continuity | Fallback success rate | Percentage of provider/model fallback attempts that complete safely. | Failover logs | Below 95% | Monthly | Platform owner | Failed fallback during incident | |
| KPI-008 | Cost | Monthly spend against budget | Actual spend divided by approved monthly budget. | Provider billing and internal chargeback | Above 90% warning, above 100% breach | Weekly | Finance or product owner | Budget breach | |
| KPI-009 | Oversight | Human approval bypass count | Number of high-impact actions completed without required approval. | Tool-call and approval logs | Any occurrence | Weekly | Governance owner | Bypass detected | |
| KPI-010 | Privacy | Sensitive data exposure count | Number of prompts, outputs, logs, or retrieved snippets containing prohibited data. | DLP or manual review | Any confirmed exposure | Weekly | Privacy owner | Confirmed exposure | |

## 4. Escalation Rules

| Condition | Action |
| --- | --- |
| Critical safety, privacy, or unauthorized tool-use event | Pause affected workflow, preserve evidence, notify incident owner, and start triage. |
| Two consecutive threshold breaches | Open remediation ticket with owner, due date, and compensating control. |
| Unapproved model, provider, prompt, tool, or retrieval change | Route through `model-provider-change-approval.md` before further expansion. |
| KPI evidence missing for one review period | Mark monitoring control as ineffective until evidence is restored. |
| KPI no longer matches current system behavior | Update the KPI and record the change rationale in the governance decision log. |

## 5. Review Record

| Field | Response |
| --- | --- |
| Review date | |
| Reviewer | |
| KPIs reviewed | |
| Threshold breaches | |
| Incidents linked | |
| Approved exceptions | |
| Required remediation | |
| Residual risk decision | Accept / conditionally accept / pause / retire |
| Next review date | |

## 6. Operating Notes

- Link every KPI to a concrete evidence source.
- Keep thresholds stricter for high-impact systems, agentic tools, regulated data, and student-facing or customer-facing workflows.
- Do not rely only on aggregate metrics. Include sampled human review for harms, unsupported claims, and contextual failures.
- Revisit KPIs after model changes, provider changes, prompt changes, retrieval corpus changes, integration changes, major incidents, or user-group expansion.
