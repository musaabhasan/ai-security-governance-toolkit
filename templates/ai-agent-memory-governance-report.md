# AI Agent Memory Governance Report

Use this report before approving persistent memory for an AI assistant or agent, before expanding memory to new users or departments, and before audit review. The report turns memory records into owner queues for consent, deletion, stale-fact handling, access boundaries, and evidence quality.

## When To Use

- Before enabling cross-session memory for a chatbot, tutor, copilot, or agent.
- Before connecting memory to tools, workflow actions, RAG retrieval, or automation.
- Before using memory for personalization, analytics, evaluation, or training.
- Before retaining memory for students, employees, customers, patients, or other identifiable users.
- After an incident involving incorrect personalization, memory leakage, or memory poisoning.

## Required Evidence

- Memory asset owner and system owner.
- Approved purpose and allowed use cases.
- Legal basis, consent, notice, or approved operational basis.
- Data classification and data-subject category.
- Write rules, retrieval rules, and role boundaries.
- Source metadata, confidence, observation time, and supersession handling for stored facts.
- Retention, deletion trigger, deletion evidence, and exception handling.
- Security review for access controls, provider transfer, and cross-user leakage.
- Evaluation cases for stale, poisoned, sensitive, and conflicting memory.

## Memory Risk Review

| Risk Signal | Severity | Owner Queue |
| --- | --- | --- |
| Memory has no named business or technical owner | High | Assign owner or block release |
| Sensitive memory lacks consent, notice, or approved basis | High | Privacy review |
| Memory can be retrieved across users, roles, departments, or tenants without explicit filtering | High | Security architecture review |
| Memory stores inferred facts without confidence, source, or observation time | Medium | Product and governance review |
| Memory has no stale-fact or supersession handling | Medium | Engineering and model-risk review |
| Memory deletion cannot be verified | High | Data protection and platform review |
| Memory is transferred to a provider or subprocessor without approved dependency evidence | High | Vendor and privacy review |
| Memory can trigger tools or workflow actions without human approval boundaries | High | Agentic safety review |
| Memory is retained after system decommissioning or user withdrawal | High | Decommissioning and deletion review |

## Owner Review Queue

| Memory Asset | Finding | Severity | Owner | Due Date | Decision |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |

## Review Questions

- Can users understand, inspect, correct, or opt out of memory where required?
- Are user-provided facts, system observations, tool outputs, retrieved context, and model inferences stored as separate categories?
- Does every current-state answer use task-time filtering instead of blindly retrieving old facts?
- Are historical facts retained only when there is an approved audit or safety need?
- Can the team prove that deleted memory was removed from stores, indexes, caches, exports, and provider-side records?
- Are prompt-injection, memory-poisoning, and cross-user leakage scenarios included in evaluation evidence?
- Do agent tools treat memory as context, not as authority to take high-impact action?

## Release Decision

| Decision Field | Response |
| --- | --- |
| Release decision | Approved / Approved with Conditions / Rejected |
| Required conditions | |
| Blockers | |
| Evidence package | |
| Residual risk owner | |
| Review date | |
| Next review date | |

## Audit Notes

Preserve this report with the memory register, data flow record, deletion evidence, access review, evaluation evidence, privacy decision, and any risk acceptance record. For student-facing, employee-facing, healthcare, or regulated workflows, treat unresolved high-severity memory findings as release blockers.
