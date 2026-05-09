# AI Model Risk Acceptance Register

Use this register when an AI system, hosted model, embedded AI feature, RAG workflow, or agentic workflow has residual risk that the organization chooses to accept for a defined period. It should not replace remediation. It records why acceptance is justified, what compensating controls are operating, who is accountable, when the decision expires, and what conditions trigger rollback or renewed review.

## 1. Acceptance Summary

| Field | Detail |
| --- | --- |
| Acceptance ID |  |
| AI system or use case |  |
| Model, provider, or agent runtime |  |
| Business owner |  |
| Technical owner |  |
| Risk owner |  |
| Decision date |  |
| Expiration date |  |
| Review cadence | Monthly / Quarterly / Before each release / Other |
| Approval forum |  |
| Evidence reference |  |

## 2. Residual Risk Statement

| Field | Detail |
| --- | --- |
| Risk theme | Data exposure / unsafe output / bias / hallucination / tool misuse / availability / vendor dependency / academic integrity / other |
| Residual risk statement |  |
| Inherent likelihood | Low / Medium / High |
| Inherent impact | Low / Medium / High |
| Residual likelihood | Low / Medium / High |
| Residual impact | Low / Medium / High |
| Affected users or groups |  |
| Sensitive data involved | None / Personal / Student / Financial / Health / Confidential / Restricted |
| Regulatory, contractual, or policy impact |  |
| Known limitations |  |

## 3. Acceptance Rationale

Document why acceptance is being requested instead of immediate remediation.

| Question | Response |
| --- | --- |
| Why can the risk not be fully remediated before use? |  |
| What business, research, learning, or operational value depends on this use? |  |
| What alternatives were considered? |  |
| Why is the selected deployment boundary proportionate to the residual risk? |  |
| What evidence supports the current risk rating? |  |

## 4. Required Compensating Controls

| Control | Owner | Evidence | Frequency | Status |
| --- | --- | --- | --- | --- |
| Human review or approval gate |  |  |  |  |
| Data minimization or redaction |  |  |  |  |
| Prompt, RAG, or tool-use restriction |  |  |  |  |
| Monitoring, sampling, or quality review |  |  |  |  |
| Incident escalation path |  |  |  |  |
| User notice, transparency, or opt-out |  |  |  |  |
| Fallback, pause, or rollback control |  |  |  |  |

## 5. Boundaries And Exclusions

| Boundary | Approved Scope | Explicitly Excluded |
| --- | --- | --- |
| User groups |  |  |
| Data categories |  |  |
| Integrations and tools |  |  |
| Output use | Drafting / advisory / decision support / automated action / other |  |
| Geography or tenancy |  |  |
| Time period |  |  |

## 6. Review Triggers

Review or revoke this acceptance if any of the following occur:

- Model, provider, endpoint, region, embedding model, prompt, RAG source, or agent tool changes.
- Evaluation pass rate drops below the agreed threshold.
- Safety, citation, privacy, bias, or academic-integrity findings increase.
- Affected user group expands beyond the approved boundary.
- New sensitive data category is introduced.
- Incident, complaint, appeal, or near miss is linked to the accepted risk.
- Compensating controls fail, become stale, or cannot be evidenced.
- Expiration date is reached without renewal approval.

## 7. Monitoring Metrics

| Metric | Threshold | Owner | Evidence Source | Review Frequency |
| --- | --- | --- | --- | --- |
| Unsafe or policy-violating outputs |  |  |  |  |
| Unsupported or uncited claims |  |  |  |  |
| Human override rate |  |  |  |  |
| User complaint or appeal rate |  |  |  |  |
| Tool-use denial or escalation rate |  |  |  |  |
| Provider latency or outage impact |  |  |  |  |
| Cost or token-budget variance |  |  |  |  |

## 8. Approval Decision

| Role | Name | Decision | Date | Conditions |
| --- | --- | --- | --- | --- |
| Business owner |  | Approved / Rejected / Conditional |  |  |
| Risk owner |  | Approved / Rejected / Conditional |  |  |
| Information security |  | Approved / Rejected / Conditional |  |  |
| Privacy or legal |  | Approved / Rejected / Conditional / Not required |  |  |
| Academic or clinical reviewer |  | Approved / Rejected / Conditional / Not required |  |  |
| Executive sponsor |  | Approved / Rejected / Conditional / Not required |  |  |

## 9. Closure Or Renewal

| Field | Detail |
| --- | --- |
| Closure status | Closed / Renewed / Revoked / Superseded |
| Closure or renewal date |  |
| Closure evidence |  |
| Residual risk after remediation |  |
| Renewal decision and conditions |  |
| Next review date |  |
