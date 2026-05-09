# AI Agent Memory Governance Register

Use this register when an AI assistant, agent, tutor, workflow bot, or copilot stores memory across sessions. Persistent memory can improve continuity, but it also creates privacy, consent, deletion, provenance, stale-fact, and misuse risks that need explicit governance evidence.

## 1. Memory Asset Inventory

| Field | Response |
| --- | --- |
| Memory asset ID | |
| AI system or agent | |
| Business owner | |
| Technical owner | |
| Memory type | User profile / Preference / Task state / Knowledge summary / Tool outcome / Conversation summary / Other |
| Storage location | |
| Storage provider | |
| Data classification | Public / Internal / Confidential / Restricted / Regulated |
| Data subjects | Employees / Students / Customers / Patients / Public users / Other |
| Legal basis or consent model | |
| Review cadence | |
| Current status | Proposed / Approved / Restricted / Retired |

## 2. Collection And Write Rules

| Control Question | Evidence |
| --- | --- |
| What events are allowed to write memory? | |
| Is memory written only after user-visible notice or approved workflow action? | |
| Can the user review or correct stored memory? | |
| Are sensitive categories blocked or minimized before storage? | |
| Are tool outputs, retrieved documents, or model inferences separated from user-provided facts? | |
| Are confidence, source, and observation time stored with each memory record? | |

## 3. Retrieval And Use Boundaries

| Boundary | Decision |
| --- | --- |
| Which agents, tools, roles, or departments can retrieve this memory? | |
| Can memory be used for personalization, automation, analytics, evaluation, or training? | |
| Is memory filtered by task context, user identity, time, purpose, and data classification? | |
| Are stale or superseded facts excluded from current-state retrieval? | |
| Are historical facts retained for audit but blocked from current-answer generation? | |
| Can memory be exported or shared with a provider, vendor, or downstream system? | |

## 4. Lifecycle And Deletion Evidence

| Lifecycle Event | Evidence |
| --- | --- |
| Creation evidence | |
| User notice or consent evidence | |
| Review or correction evidence | |
| Supersession or stale-fact handling | |
| Retention period | |
| Deletion trigger | |
| Deletion verification method | |
| Deletion evidence owner | |
| Legal hold or retention exception | |

## 5. Risk And Control Mapping

| Risk Theme | Applicability | Control Evidence |
| --- | --- | --- |
| Unauthorized personalization | | |
| Memory poisoning | | |
| Stale or superseded facts | | |
| Sensitive data retention | | |
| Cross-user leakage | | |
| Provider or subprocessor transfer | | |
| Inaccurate inferred profile | | |
| Deletion failure | | |
| Audit reconstruction gap | | |

## 6. Approval Decision

| Decision Field | Response |
| --- | --- |
| Decision | Approved / Approved with Conditions / Rejected / Retired |
| Conditions | |
| Residual risk owner | |
| Privacy reviewer | |
| Security reviewer | |
| Business approver | |
| Decision date | |
| Next review date | |

## 7. Required Attachments

- Data flow record showing memory write, retrieval, use, and deletion paths.
- User notice, consent, or approved operational basis.
- Access-control evidence for memory stores and retrieval APIs.
- Redaction or minimization evidence for sensitive categories.
- Evaluation evidence for stale, poisoned, conflicting, and cross-user memory scenarios.
- Deletion test evidence and exception register references.
- Incident response path for memory leakage, poisoning, or incorrect personalization.
