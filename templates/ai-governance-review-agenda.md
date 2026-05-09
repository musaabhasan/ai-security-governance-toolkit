# AI Governance Review Agenda

Use this agenda to run a structured AI governance forum for new use cases, release approvals, provider changes, material prompt or RAG changes, incidents, exceptions, and high-risk research or education deployments. The purpose is to convert evidence into clear decisions, accountable actions, and auditable records.

## Meeting Header

| Field | Value |
| --- | --- |
| Meeting date |  |
| Chair |  |
| Secretary or evidence owner |  |
| Portfolio or system scope |  |
| Review type | New approval / release gate / model change / provider change / incident review / exception review / periodic assurance |
| Risk tier | Low / Moderate / High / Critical |
| Decision deadline |  |

## Required Participants

| Role | Required when | Name |
| --- | --- | --- |
| Business owner | Every review |  |
| Product or system owner | Every review |  |
| Security owner | Agent tools, integrations, high-risk data, incidents, or elevated findings |  |
| Privacy or data protection owner | Personal, student, employee, sensitive, or third-party data is involved |  |
| Data owner | New data sources, RAG indexes, analytics, lineage changes, or retention questions |  |
| Model or evaluation owner | Model, prompt, retrieval, safety-filter, or evaluation evidence is being reviewed |  |
| Legal or procurement owner | Vendor, contract, DPA, IP, copyright, or subprocessor questions exist |  |
| Academic or research owner | Learner assessment, classroom study, consent, ethics, or scholarly evidence is involved |  |
| Operations owner | Continuity, monitoring, logging, rollback, outage, or runbook decisions are required |  |
| Executive risk owner | High residual risk, exceptions, material public trust impact, or appetite decision is required |  |

## Pre-Read Checklist

| Artifact | Required? | Link or evidence reference | Owner | Ready? |
| --- | --- | --- | --- | --- |
| AI system intake | Yes |  |  |  |
| Risk tiering decision record | Yes |  |  |  |
| Data-flow record | If data is processed |  |  |  |
| Data lineage report | If RAG, analytics, training, research, or evaluation data is used |  |  |  |
| DPIA triage report | If personal, student, employee, sensitive, or monitored data is used |  |  |  |
| Vendor due diligence or dependency report | If third-party AI services are used |  |  |  |
| Evaluation evidence report | If release, model, prompt, or retrieval changes are reviewed |  |  |  |
| Red-team or prompt-injection evidence | If externally exposed, agentic, or high-impact |  |  |  |
| Access recertification evidence | If privileged access, service accounts, or tool permissions changed |  |  |  |
| Rollback readiness report | If production release or material change is proposed |  |  |  |
| Evidence retention schedule | If logs, traces, research evidence, or incident evidence are retained |  |  |  |

## Standard Agenda

| Time | Topic | Lead | Expected output |
| --- | --- | --- | --- |
| 5 min | Decision objective and scope | Chair | Confirm what decision is being made today |
| 10 min | Use-case and user-impact summary | Business owner | Confirm value, affected users, and decision urgency |
| 10 min | Risk tier and escalation triggers | Risk owner | Confirm tier, review path, and required approvals |
| 15 min | Data, privacy, and retention evidence | Data/privacy owner | Confirm lawful basis, minimization, retention, and transfer controls |
| 15 min | Security, identity, and agent tool review | Security owner | Confirm tool permissions, credential boundaries, logging, and findings |
| 15 min | Evaluation, quality, and safety evidence | Evaluation owner | Confirm test coverage, pass rates, failures, limitations, and release gates |
| 10 min | Vendor, continuity, and rollback readiness | Operations/procurement owner | Confirm dependency, exit, fallback, and rollback controls |
| 10 min | Open exceptions and residual risk | Risk owner | Decide whether any risk requires acceptance, remediation, or escalation |
| 10 min | Decision and action log | Chair | Record approval, conditional approval, hold, rejection, or escalation |

## Decision Options

| Decision | Use when | Required record |
| --- | --- | --- |
| Approve | Required evidence is complete and residual risk is within appetite | Approval summary and evidence references |
| Conditionally approve | Evidence gaps are limited, owned, and do not block safe release | Conditions, due dates, and release restrictions |
| Hold | Required evidence is incomplete or release risk is not yet understood | Hold reason and owner remediation plan |
| Reject | Risk is outside appetite or controls are not feasible | Rejection rationale and reconsideration conditions |
| Escalate | Decision requires executive, legal, privacy, ethics, or external review | Escalation route and decision deadline |

## Decision Log

| Item | Decision | Owner | Due date | Evidence reference | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Risk Acceptance Record

Complete this section only when the forum accepts residual risk or approves a temporary exception.

| Field | Value |
| --- | --- |
| Accepted risk |  |
| Reason acceptance is justified |  |
| Compensating controls |  |
| Expiry date |  |
| Risk owner |  |
| Required monitoring |  |
| Re-review trigger |  |

## Follow-Up Tracker

| Action | Owner | Evidence expected | Due date | Status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Closure Criteria

A review is closed only when:

- The decision log is complete and linked to evidence.
- Conditional approvals have explicit owners, restrictions, and due dates.
- Release holds have a named remediation path.
- Exceptions have expiry dates and compensating controls.
- Escalations have a destination owner and decision deadline.
- The evidence owner stores the agenda, notes, and attachments in the approved retention location.
