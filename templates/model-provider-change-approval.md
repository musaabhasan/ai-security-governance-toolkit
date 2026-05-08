# Model And Provider Change Approval

Use this workflow before changing an AI model, model version, provider, deployment region, inference endpoint, embedding model, safety filter, RAG retrieval model, or agent runtime. Model and provider changes can alter accuracy, privacy, cost, latency, explainability, safety behavior, data residency, and contractual obligations even when application code stays the same.

## 1. Change Summary

| Field | Response |
| --- | --- |
| AI system name | |
| Change owner | |
| Current model/provider | |
| Proposed model/provider | |
| Change type | Model version / provider / endpoint / embedding model / safety filter / agent runtime / region / other |
| Target environment | Research / pilot / production |
| Planned change window | |
| Rollback owner | |

## 2. Change Driver

| Driver | Applies | Notes |
| --- | --- | --- |
| Required provider deprecation | Yes / No | |
| Cost optimization | Yes / No | |
| Accuracy or quality improvement | Yes / No | |
| Latency or availability improvement | Yes / No | |
| New capability requirement | Yes / No | |
| Security or privacy concern | Yes / No | |
| Contract, compliance, or data residency change | Yes / No | |
| Incident response or emergency mitigation | Yes / No | |

## 3. Impact Assessment

| Impact Area | Review Question | Result | Evidence |
| --- | --- | --- | --- |
| Data handling | Will prompts, outputs, logs, embeddings, or files be processed differently? | | |
| Vendor training | Do provider terms change model-training or retention behavior? | | |
| Data residency | Does processing, storage, or support access move region? | | |
| Security controls | Are authentication, encryption, network, or tenant-isolation controls changing? | | |
| Output quality | Do evaluation results meet or exceed the current model baseline? | | |
| Bias and fairness | Do subgroup or protected-context results change materially? | | |
| Prompt behavior | Do system prompts, refusal rules, or guardrails behave differently? | | |
| RAG behavior | Do retrieval, citation, chunk ranking, or embedding results change? | | |
| Agentic tools | Does the model change tool-use frequency, parameters, or approval behavior? | | |
| Cost and quotas | Does token usage, pricing, rate limit, or budget exposure change? | | |
| Continuity | Is fallback, rollback, or provider exit still viable? | | |
| Contracting | Are DPA, procurement, support, SLA, or audit terms still valid? | | |

## 4. Required Tests

| Test | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Smoke test with standard prompts | Required | Required | Required | Required | | |
| Regression evaluation pack | Recommended | Required | Required | Required | | |
| Prompt injection and jailbreak checks | Recommended | Required | Required | Required | | |
| Citation and source-grounding checks | If RAG | If RAG | Required if RAG | Required if RAG | | |
| Sensitive-data handling checks | If applicable | Required | Required | Required | | |
| Bias/fairness review | Recommended | Recommended | Required | Required | | |
| Tool-call approval checks | If agentic | If agentic | Required | Required | | |
| Cost and latency comparison | Recommended | Required | Required | Required | | |
| Rollback test | Optional | Recommended | Required | Required | | |

## 5. Approval Route

| Condition | Minimum Approval |
| --- | --- |
| No sensitive data, no external users, no tool access, low-impact use | Product/use-case owner and technical owner |
| Sensitive data, user-facing workflow, or material quality change | Security reviewer, data owner, and business owner |
| Provider, region, retention, or training-term change | Privacy/data protection, procurement/legal, and security reviewer |
| Agentic tool access or high-impact decision support | Security leadership, business risk owner, and human-approval owner |
| Emergency change | Incident commander plus retrospective approval within defined review window |

## 6. Deployment Controls

| Control | Response |
| --- | --- |
| Rollout strategy | Canary / phased / all-at-once / emergency |
| Initial traffic percentage | |
| Monitoring window | |
| Success metrics | |
| Automatic rollback triggers | |
| Manual rollback steps | |
| User communication needed? | Yes / No |
| Documentation updated? | Yes / No |

## 7. Post-Change Review

| Review Item | Result | Evidence |
| --- | --- | --- |
| Evaluation results match approval evidence | | |
| Production monitoring shows expected latency, cost, and quality | | |
| Safety, refusal, and sensitive-data controls remain effective | | |
| User/support feedback reviewed | | |
| Incidents or exceptions opened after rollout | | |
| Old provider/model credentials retired if no longer needed | | |
| Risk register, model card, data-flow record, and vendor record updated | | |

## 8. Decision Record

| Field | Response |
| --- | --- |
| Decision | Approve / Approve with conditions / Defer / Reject / Emergency approve |
| Conditions | |
| Decision owner | |
| Decision date | |
| Next review date | |
