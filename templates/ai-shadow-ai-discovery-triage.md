# AI Shadow Use Discovery Triage

Use this template when an organization discovers unapproved, unmanaged, or unclear AI use through network logs, expense records, browser telemetry, procurement requests, support tickets, surveys, DLP alerts, endpoint detections, or staff disclosure. The goal is to convert shadow AI signals into accountable risk decisions without immediately treating every discovery as misconduct.

## 1. Discovery Context

| Field | Response |
| --- | --- |
| Discovery ID |  |
| Discovery date |  |
| Reporting source | Network / DLP / endpoint / expense / procurement / survey / support / audit / self-disclosure |
| Business unit or department |  |
| Suspected AI service or feature |  |
| Known users or roles |  |
| Initial reviewer |  |
| Related system or workflow |  |
| Current status | Intake / validating / contained / approved with conditions / retired / escalated |

## 2. Discovery Signal Evidence

| Signal | Evidence Reference | Confidence | Notes |
| --- | --- | --- | --- |
| Domain or API traffic |  | High / medium / low |  |
| Browser extension or desktop app |  | High / medium / low |  |
| Expense or invoice record |  | High / medium / low |  |
| Uploaded file or DLP event |  | High / medium / low |  |
| Staff disclosure or survey response |  | High / medium / low |  |
| Procurement or vendor inquiry |  | High / medium / low |  |
| Support ticket or helpdesk request |  | High / medium / low |  |

Discovery rules:

- Do not infer sensitive data exposure from domain access alone.
- Do not identify individual users in broadly shared reports unless needed for containment or investigation.
- Preserve raw telemetry in restricted evidence storage and share only scoped summaries.
- Prefer direct validation with the business owner before assuming the tool is unauthorized.

## 3. Use Case and Data Exposure Triage

| Question | Response | Evidence |
| --- | --- | --- |
| What business or academic task is the AI tool supporting? |  |  |
| Is the tool used for drafting, summarization, coding, research, advising, decision support, automation, or data analysis? |  |  |
| What data categories may have been entered or uploaded? | Public / internal / confidential / regulated / student / HR / financial / source code / credentials |  |
| Does the use involve personal data, students, employees, patients, minors, or regulated records? | Yes / no / unknown |  |
| Does the AI output influence decisions about access, grades, employment, eligibility, finance, security, or compliance? | Yes / no / unknown |  |
| Does the tool have connectors, browser access, plugins, file upload, memory, or workflow automation? | Yes / no / unknown |  |
| Is there a contract, DPA, retention statement, or approved security review? | Yes / no / partial |  |

## 4. Risk Classification

| Risk Area | Indicators | Initial Rating |
| --- | --- | --- |
| Data leakage | File upload, prompt entry, API integration, logs, model training reuse, weak deletion rights | Low / medium / high |
| Identity and access | Shared accounts, unmanaged OAuth consent, broad scopes, browser extension permissions | Low / medium / high |
| Output reliance | Decisions, advice, eligibility, safety, compliance, or academic outcomes depend on generated output | Low / medium / high |
| Vendor and legal | No contract, unclear retention, unclear region, subprocessors, no assurance evidence | Low / medium / high |
| Security operations | Unknown tool calls, code execution, external posting, credential handling, lack of audit logs | Low / medium / high |
| Business continuity | Critical workflow depends on unmanaged service or personal account | Low / medium / high |

Escalate immediately when:

- credentials, secrets, student records, protected personal data, or regulated records may have been uploaded;
- the AI tool can change records, send messages, trigger workflows, run code, or access internal systems;
- the output affects high-impact decisions without approved human review;
- the tool is paid by institutional funds but has no accountable owner or contract path.

## 5. Stakeholder Review

| Role | Required When | Assigned Reviewer | Decision |
| --- | --- | --- | --- |
| Business owner | Any recurring or workflow-relevant use |  |  |
| Information security | Sensitive data, connectors, plugins, workflow actions, or credentials |  |  |
| Privacy or data protection | Personal, student, employee, health, or regulated data |  |  |
| Legal or procurement | Paid service, vendor terms, DPA, contract, or region issue |  |  |
| Academic or professional governance | Student-facing, assessment, advising, or credentialing use |  |  |
| IT operations | Integration, network allow-list, SSO, support, or continuity impact |  |  |

## 6. Decision Options

| Decision | Use When | Required Conditions |
| --- | --- | --- |
| Approve with controls | Use case is valuable and risk can be managed | Owner, contract path, data rules, logging, review cadence, user guidance |
| Approve limited pilot | Value is plausible but evidence is incomplete | Defined pilot scope, no sensitive data, user group, evaluation plan, sunset date |
| Migrate to approved service | Users need the capability but the current tool is unsuitable | Approved alternative, migration plan, communication, deletion request |
| Contain and review | Sensitive exposure or high-risk capability is possible | Preserve evidence, suspend use, assess data, notify required owners |
| Retire or block | Tool is unnecessary, unsafe, duplicative, or unsupported | Communication, exception path, evidence retention, deletion proof where feasible |
| Accept documented exception | Business need remains and risk owner accepts residual risk | Expiry date, compensating controls, review cadence, executive approval if high risk |

## 7. Remediation Plan

| Action | Owner | Due Date | Evidence |
| --- | --- | --- | --- |
| Assign business and technical owner |  |  |  |
| Confirm data categories and uploaded files |  |  |  |
| Review terms, retention, training use, deletion, and subprocessors |  |  |  |
| Remove broad OAuth scopes or unmanaged extensions |  |  |  |
| Disable tool integrations or workflow actions until approved |  |  |  |
| Request deletion or export evidence where needed |  |  |  |
| Move users to approved service or approved configuration |  |  |  |
| Publish safe-use guidance for the affected team |  |  |  |
| Add tool to inventory, risk register, and review cadence |  |  |  |

## 8. Evidence Package

Retain:

- discovery summary and raw evidence location,
- tool or vendor identity,
- department and owner decision,
- data category analysis,
- stakeholder decisions,
- remediation actions,
- deletion or containment evidence,
- residual risk acceptance,
- communication record,
- next review date.

Do not include unnecessary raw prompts, full documents, personal messages, or complete browser histories in routine governance reports. Store sensitive discovery artifacts under restricted access and reference them by evidence ID.

## 9. Closure Record

| Field | Response |
| --- | --- |
| Final disposition | Approved / pilot / migrated / contained / retired / exception |
| Residual risk rating | Low / medium / high |
| Risk owner |  |
| Evidence package location |  |
| User communication completed | Yes / no |
| Inventory updated | Yes / no |
| Risk register updated | Yes / no |
| Review due date |  |
| Closure approver |  |
