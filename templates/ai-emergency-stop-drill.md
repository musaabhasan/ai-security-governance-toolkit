# AI Emergency Stop Drill

Use this template to test whether an AI system, assistant, model gateway, RAG workflow, or agentic tool can be paused, contained, rolled back, and safely restarted when it creates unacceptable risk. It is intended for production and pre-production systems that can affect users, records, access, money, credentials, communications, learning outcomes, safety, compliance, or operational continuity.

## 1. Drill Context

| Field | Response |
| --- | --- |
| AI system or workflow |  |
| Business owner |  |
| Technical owner |  |
| Security or risk owner |  |
| Drill date |  |
| Environment | Development / test / staging / production |
| Scope | Model / prompt / RAG index / agent tool / provider / integration / workflow |
| Risk tier | Low / medium / high / prohibited |
| Drill type | Tabletop / technical simulation / live failover / production exercise |

## 2. Emergency Stop Triggers

| Trigger | Example Signal | Stop Authority |
| --- | --- | --- |
| Prompt injection or data exfiltration | System prompt extraction, tool abuse, sensitive data in output | Security owner |
| Unsafe automated action | Agent changes access, sends messages, deletes data, or approves requests incorrectly | Business owner |
| Provider degradation | Safety filter change, outage, latency spike, unexpected model behavior | Platform owner |
| RAG integrity failure | Stale, poisoned, unapproved, or mis-cited source drives answers | Knowledge owner |
| Privacy incident | Personal data, student data, credentials, or confidential records exposed | Privacy owner |
| Legal or policy hold | Regulator, audit, legal, HR, academic, or compliance request | Governance owner |
| Harmful output pattern | Repeated unsafe, biased, misleading, or unsupported outputs | Review lead |

## 3. Stop Controls Inventory

| Control | Location | Owner | Tested |
| --- | --- | --- | --- |
| Disable bot instance or workflow |  |  | Yes / no |
| Disable provider credential or route |  |  | Yes / no |
| Disable tool invocation |  |  | Yes / no |
| Disable prompt version |  |  | Yes / no |
| Freeze RAG index or source collection |  |  | Yes / no |
| Pause queue or scheduler |  |  | Yes / no |
| Revoke API key, token, or service account |  |  | Yes / no |
| Activate fallback model or static response |  |  | Yes / no |

## 4. Drill Scenario

| Scenario Item | Response |
| --- | --- |
| Initiating event |  |
| Affected users, records, systems, or workflows |  |
| Expected stop decision | Pause / disable / route around / revoke / rollback / escalate |
| Maximum acceptable stop time |  |
| Required evidence | Logs, traces, prompt versions, source IDs, tool calls, approvals, hashes |
| Communication channels |  |
| Restart decision owner |  |

## 5. Execution Steps

| Step | Expected Result | Evidence |
| --- | --- | --- |
| Detect trigger and open incident or drill record | Case ID exists |  |
| Confirm stop authority and decision owner | Owner accepts decision |  |
| Disable affected capability | System no longer performs risky action |  |
| Preserve logs, traces, prompts, outputs, and tool-call records | Evidence package created |  |
| Notify affected operational owners | Communications sent |  |
| Switch to fallback or manual process | Service remains controlled |  |
| Validate containment | No further risky output or action occurs |  |
| Decide rollback, remediation, or restart | Approval recorded |  |

## 6. Evidence Package

| Evidence Item | Required Detail |
| --- | --- |
| Stop decision | Who stopped the system, when, why, and under what authority |
| System state | Model, prompt, RAG index, provider, tool, and workflow versions |
| Trigger evidence | Logs, traces, screenshots, support cases, alerts, or evaluator results |
| Containment evidence | Disabled flags, revoked credentials, route changes, queue status |
| Impact assessment | Affected users, records, actions, decisions, or business process |
| Communications | Internal notification, user notice, regulator or customer contact if required |
| Restart approval | Owner, conditions, validation, monitoring window, and residual risk |

## 7. Restart Criteria

Do not restart until:

- the trigger condition is understood and remediated or explicitly risk-accepted;
- affected prompts, tools, RAG sources, credentials, routes, or workflows are corrected;
- logs and evidence are preserved under the retention schedule;
- regression tests or red-team checks pass for the relevant failure mode;
- fallback and manual processes are stable;
- communications and support guidance are ready;
- a named owner approves restart and monitoring criteria.

## 8. Metrics

| Metric | Purpose |
| --- | --- |
| Time to stop | Measures operational readiness |
| Time to confirm containment | Shows whether risky actions truly stopped |
| Evidence completeness | Measures audit readiness |
| Fallback activation time | Measures continuity planning |
| Restart defects | Detects premature restart |
| Repeat trigger count | Identifies unresolved root cause |
| Owner response time | Shows whether authority and escalation paths work |

## 9. Findings And Actions

| Finding | Severity | Required Action | Owner | Due Date |
| --- | --- | --- | --- | --- |
|  | Low / medium / high / critical |  |  |  |
|  |  |  |  |  |

## 10. Drill Decision

| Decision Item | Response |
| --- | --- |
| Emergency stop readiness | Ready / ready with conditions / hold |
| Required remediation |  |
| Next drill date |  |
| Residual risk owner |  |
| Evidence package location |  |
| Approver |  |

## 11. Closure Notes

Document assumptions, gaps, technical limits, authority gaps, communication delays, fallback issues, restart risks, and any AI capabilities that must remain disabled until remediation is complete.
