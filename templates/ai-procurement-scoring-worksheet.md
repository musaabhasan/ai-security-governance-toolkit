# AI Procurement Scoring Worksheet

Use this worksheet before approving an AI product, hosted model, embedded AI feature, agent platform, or AI-enabled learning tool. It converts procurement review into an evidence-based score that can be compared across vendors and repeated during renewal.

## 1. Procurement Context

| Field | Response |
| --- | --- |
| Product or service | |
| Vendor | |
| Business owner | |
| Security owner | |
| Data owner | |
| Intended users | |
| Primary use cases | |
| Deployment model | SaaS / private cloud / on-premises / embedded feature / API |
| Data classifications in scope | Public / internal / confidential / regulated / student / employee / customer |
| AI capabilities | Chat / RAG / summarization / classification / agentic actions / analytics / content generation |
| Contract stage | Exploration / proof of concept / procurement / renewal / expansion |

## 2. Scoring Method

Score each domain from 1 to 5.

| Score | Meaning |
| --- | --- |
| 1 | Unacceptable, missing, or unverified |
| 2 | Weak controls or incomplete evidence |
| 3 | Acceptable with manageable gaps |
| 4 | Strong controls with minor gaps |
| 5 | Strong controls, tested evidence, and clear accountability |

Weighted score = `weight x score`. Maximum score is 500. Convert to percentage by dividing the total weighted score by 5.

## 3. Mandatory Risk Gates

Do not approve procurement until these gates are resolved.

| Gate | Blocker Condition | Required Resolution |
| --- | --- | --- |
| Data protection | Vendor cannot explain training, retention, subprocessors, deletion, or data isolation | Obtain contractual controls and technical evidence |
| Identity and access | No SSO, MFA, role separation, or administrative audit trail for sensitive use cases | Require roadmap, compensating controls, or reject |
| Security assurance | No penetration-test summary, SOC 2/ISO evidence, vulnerability process, or incident notification terms | Obtain assurance evidence and contract language |
| Model behavior | No safety testing, content controls, bias evaluation, or harmful-output handling for high-impact use | Require test evidence and documented release criteria |
| Exit and portability | No practical data export, deletion certificate, model fallback, or migration plan | Complete exit plan before approval |

## 4. Weighted Review

| Domain | Weight | Score 1-5 | Weighted Score | Evidence Required | Risk Notes | Required Action |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Strategic fit and measurable value | 10 | | | Use-case owner, success metrics, adoption plan, measurable outcome | | |
| Data protection and privacy | 15 | | | Data flow, retention, deletion, training-use limits, subprocessors, privacy review | | |
| Security architecture and identity controls | 15 | | | SSO, MFA, RBAC, tenant isolation, encryption, key handling, admin audit logs | | |
| Model governance and transparency | 10 | | | Model/version disclosure, limitations, evaluation results, change notices, monitoring | | |
| Safety, bias, accessibility, and inclusion | 10 | | | Safety tests, bias checks, accessibility review, human escalation paths | | |
| Knowledge base and RAG governance | 8 | | | Source controls, freshness policy, citation behavior, ingestion approvals, deletion | | |
| Integration, API, and agentic tool risk | 8 | | | API permissions, tool approval gates, rate limits, sandboxing, abuse monitoring | | |
| Vendor assurance and contractual controls | 10 | | | SOC/ISO evidence, DPA, breach notification, right to audit, security roadmap | | |
| Continuity, portability, and exit readiness | 8 | | | SLA, fallback, export, deletion certificate, dependency map, renewal trigger | | |
| Cost, observability, and support | 6 | | | Token/cost controls, usage reports, latency metrics, support model, escalation path | | |

## 5. Decision Thresholds

| Result | Decision Guidance |
| --- | --- |
| 85-100% | Approve if mandatory gates are closed and owners accept residual risk |
| 70-84% | Conditional approval with remediation dates and compensating controls |
| 55-69% | Limited pilot only; production approval requires material improvement |
| Below 55% | Do not approve without a new risk decision and executive acceptance |

## 6. Procurement Decision Record

| Field | Response |
| --- | --- |
| Total weighted score | |
| Percentage score | |
| Mandatory gates closed | Yes / No |
| Residual risk rating | Low / Medium / High / Critical |
| Decision | Approve / conditionally approve / pilot only / reject |
| Required compensating controls | |
| Review date | |
| Renewal or revalidation trigger | |
| Business approver | |
| Security approver | |
| Data/privacy approver | |

## 7. Review Notes

Record dissenting opinions, unresolved evidence gaps, and any contractual assumptions that must be verified before signature.
