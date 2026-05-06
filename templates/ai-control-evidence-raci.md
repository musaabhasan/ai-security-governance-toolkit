# AI Control Evidence RACI

Use this template to assign accountability for AI security controls and the evidence needed to prove that those controls are operating. It is intended for governance reviews, internal audit preparation, and operating-model design.

## Role Definitions

| Role | Responsibility |
| --- | --- |
| Business owner | Confirms purpose, impact, acceptable use, and user-facing obligations |
| System owner | Owns platform operation, integration, availability, and change control |
| Security owner | Defines control expectations, reviews risk, and validates remediation |
| Data owner | Approves data use, classification, retention, and transfer decisions |
| Privacy owner | Reviews personal-data handling, notices, consent, and data-subject obligations |
| Model owner | Tracks model selection, evaluation, limitations, and monitoring signals |
| Vendor owner | Manages third-party assurance, contracts, service levels, and exit planning |
| Internal audit | Reviews evidence quality and control operating effectiveness |

## Control Evidence Matrix

| Control area | Responsible | Accountable | Consulted | Informed | Evidence | Frequency |
| --- | --- | --- | --- | --- | --- | --- |
| AI system intake |  |  |  |  | Approved intake record | Per use case |
| Data classification |  |  |  |  | Data flow record and classification note | Per use case |
| Vendor due diligence |  |  |  |  | Completed vendor questionnaire and approval | Before onboarding |
| Access review |  |  |  |  | User, administrator, API key, and tool-access review | Quarterly |
| Prompt injection testing |  |  |  |  | Test record with cases, outcomes, and remediation | Before production and major change |
| Tool-use approval |  |  |  |  | Agentic tool review and approval decision | Before enabling tool access |
| Logging and retention |  |  |  |  | Retention decision and logging configuration | Per release |
| Output monitoring |  |  |  |  | Quality, safety, and exception review notes | Monthly |
| Incident response |  |  |  |  | Exercise notes and updated playbook | Quarterly |
| Provider exit planning |  |  |  |  | Exit plan and fallback validation | Annually |

## Evidence Quality Checks

- Evidence is linked to a named control.
- Evidence has a clear owner.
- Evidence includes a date or review period.
- Evidence can be independently inspected.
- Evidence shows the result of the control, not only the existence of a policy.
- Exceptions have expiry dates and compensating controls.
- Remediation actions have owners and target dates.

## Review Notes

| Date | Reviewer | Area reviewed | Findings | Action owner | Due date |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
