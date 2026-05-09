# AI Evidence Retention Schedule

Use this schedule to define how long AI governance evidence should be retained, who owns it, where it is stored, and when it must be reviewed or deleted. It is designed for audit preparation, privacy review, incident response, model/provider change control, and regulated education or public-sector environments.

## Schedule Inputs

| Field | Value |
| --- | --- |
| AI system or portfolio |  |
| Business owner |  |
| Evidence owner |  |
| Risk tier | Low / Moderate / High / Critical |
| Data classification | Public / Internal / Confidential / Restricted / Sensitive |
| Retention policy reference |  |
| Legal hold active? | Yes / No |
| Last reviewed |  |
| Next review due |  |

## Retention Matrix

| Evidence category | Examples | Minimum retention | Owner | Storage expectation | Deletion trigger |
| --- | --- | --- | --- | --- | --- |
| Intake and approval records | AI system intake, risk tiering record, approval minutes, residual-risk decisions | Life of system plus 2 years | Governance owner | Approved governance repository or GRC platform | System retired and retention period complete |
| Data lineage and data-flow evidence | Source inventory, transformations, transfer records, data-flow diagrams, legal basis | Life of system plus 2 years | Data owner | Controlled document store with version history | Dataset retired and audit window closed |
| Evaluation evidence | Evaluation suite, test dataset lineage, pass/fail results, human review, failure analysis | 3 years after release or material change | Model owner | Immutable or versioned release evidence folder | Replaced by reviewed successor and retention met |
| Prompt and configuration evidence | System instructions, prompt versions, safety settings, retrieval configuration, tool permissions | Life of active version plus 2 years | Product owner | Version-controlled repository or approved configuration archive | Version superseded and retention met |
| Access and identity evidence | Access reviews, service account approvals, API key ownership, break-glass logs | 2 years after access removal | Identity owner | Access governance or ticketing system | Account or token removed and retention met |
| Operational logs | Prompt metadata, output metadata, tool-call logs, retrieval traces, administrative events | 90 days to 1 year based on risk and privacy approval | Operations owner | Central logging with access controls and masking | Log retention expires unless legal hold applies |
| Incident evidence | Timeline, preserved logs, containment proof, privacy review, communications, remediation records | 5 years after closure or per incident policy | Incident owner | Incident management system with evidence hashes where practical | Incident closed and retention period complete |
| Exception evidence | Exception request, compensating controls, risk owner approval, expiry review | 2 years after closure | Risk owner | Risk register or GRC platform | Exception closed and retention met |
| Vendor and provider evidence | Due diligence, DPA, assurance reports, subprocessor list, exit plan, change notices | Contract life plus 3 years | Procurement owner | Vendor risk system or controlled repository | Contract ended and retention period complete |
| Deletion and decommissioning evidence | Deletion requests, processor confirmations, vector-store deletion, credential revocation, shutdown checklist | 3 years after completion | System owner | Controlled repository with request/ticket references | Completion verified and retention met |
| Research and education ethics evidence | Consent records, ethics approval, de-identification record, instrument versions, participant notices | Per ethics approval, consent terms, and institutional policy | Research owner | Restricted research evidence store | Study closed and approved retention met |

## Risk-Based Adjustments

Increase the retention period or require stronger evidence controls when any condition applies:

- The system is classified as high or critical risk.
- The system processes sensitive, learner, employee, health, financial, or regulated data.
- The system supports decisions that affect access, assessment, eligibility, safety, employment, or public services.
- The system uses third-party providers that can change models, regions, safety filters, or subprocessors.
- There is an active incident, complaint, audit, investigation, litigation hold, or regulatory inquiry.
- Evaluation results show high-severity safety, privacy, bias, hallucination, or tool-misuse findings.

## Privacy And Minimization Controls

| Control | Required decision |
| --- | --- |
| Redaction | Decide which prompt, output, log, and transcript fields must be masked before retention. |
| Pseudonymization | Replace direct identifiers with controlled keys when raw identity is not required. |
| Access boundary | Restrict retained evidence to owners, auditors, incident responders, and approved reviewers. |
| Encryption | Store restricted evidence in encrypted repositories or platforms with managed keys. |
| Search exposure | Prevent retained evidence from being indexed into unrelated knowledge bases or analytics tools. |
| Retention override | Document the approving owner for any extension beyond the approved retention window. |

## Review Questions

- Are retained prompts, outputs, traces, and logs still necessary for the stated control objective?
- Is any retained evidence more sensitive than the system's approved storage boundary allows?
- Are retention periods aligned with privacy notices, consent language, contracts, and legal obligations?
- Is stale evidence being retained because deletion ownership is unclear?
- Can auditors reconstruct approval, evaluation, access, incident, and decommissioning decisions without accessing excessive personal data?
- Are legal holds, investigations, and open incidents clearly preventing normal deletion where needed?

## Closure Record

| Evidence category | Retention met? | Deletion or archive reference | Reviewer | Review date | Notes |
| --- | --- | --- | --- | --- | --- |
| Intake and approval records |  |  |  |  |  |
| Data lineage and data-flow evidence |  |  |  |  |  |
| Evaluation evidence |  |  |  |  |  |
| Prompt and configuration evidence |  |  |  |  |  |
| Access and identity evidence |  |  |  |  |  |
| Operational logs |  |  |  |  |  |
| Incident evidence |  |  |  |  |  |
| Vendor and provider evidence |  |  |  |  |  |

## Review Cadence

Review this schedule at least annually and whenever the AI system changes risk tier, data classification, provider, region, model family, logging configuration, research use, or incident status.
