# AI Risk Tiering Decision Record

Use this record after AI system intake and before pilot or production approval. It turns a use case into a documented risk tier, required control baseline, approval route, and review cadence.

## 1. System Snapshot

| Field | Response |
| --- | --- |
| System name | |
| Use case owner | |
| Technical owner | |
| Security reviewer | |
| Privacy reviewer | |
| Model or provider | |
| Deployment model | SaaS / private cloud / on-prem / local / hybrid |
| Intended users | |
| Environment | Research / pilot / production |
| Decision date | |

## 2. Tiering Factors

Score each factor from 0 to 3.

| Factor | 0 - Minimal | 1 - Low | 2 - Moderate | 3 - High | Score |
| --- | --- | --- | --- | --- | --- |
| Data sensitivity | Public data only | Internal data | Confidential data | Regulated, personal, student, patient, financial, or credential data | |
| User impact | No individual impact | Advisory impact only | Could influence service quality, learning support, or operations | Could affect access, grading, employment, finance, safety, legal rights, or essential services | |
| Autonomy | Drafting or summarization only | Human-triggered retrieval or recommendations | AI recommends actions that humans normally accept | AI can initiate, approve, deny, modify, delete, transact, notify, or execute tools | |
| External exposure | Internal isolated use | Authenticated internal users | Partner, student, customer, or vendor-facing | Public, multi-tenant, internet-facing, or unknown users | |
| Model and supply-chain uncertainty | Fully controlled local model or reviewed provider | Reviewed provider with standard controls | New provider, new model family, or limited assurance | Unreviewed model/provider, plugins, agents, or third-party tool chain | |
| Explainability and contestability | Outputs are transparent and easy to verify | Outputs require light review | Outputs require specialist review | Affected users need formal challenge, appeal, or audit trail | |
| Continuity dependency | Non-critical convenience feature | Workaround available | Operational dependency with manual fallback | Business-critical, safety-critical, or time-sensitive dependency | |
| Abuse potential | Low misuse value | Limited misuse value | Useful for phishing, data inference, or operational manipulation | Enables credential exposure, tool misuse, fraud, malware assistance, or high-impact social engineering | |

## 3. Automatic Tier Escalation Triggers

Set the tier to Tier 3 or Tier 4 when any trigger applies, even if the numeric score appears lower.

| Trigger | Applies | Notes |
| --- | --- | --- |
| The system processes regulated, personal, student, patient, financial, authentication, or confidential business data | Yes / No | |
| The system can call tools, APIs, databases, scripts, workflow actions, email, identity systems, or external services | Yes / No | |
| Output can materially affect access, assessment, grading, employment, safety, finance, legal rights, or essential services | Yes / No | |
| The system is public-facing, student-facing, customer-facing, or multi-tenant | Yes / No | |
| The model, provider, plugin, or agent runtime has not completed vendor/security review | Yes / No | |
| The system has no tested fallback or rollback path | Yes / No | |

## 4. Risk Tier Decision

| Tier | Score Range | Typical Meaning | Minimum Approval Route |
| --- | --- | --- | --- |
| Tier 1 | 0-5 | Low-impact assistant or internal productivity use | Use case owner and technical owner |
| Tier 2 | 6-10 | Moderate business process support with limited sensitive data or limited external exposure | Use case owner, security reviewer, and data owner |
| Tier 3 | 11-16 | Sensitive data, user-facing workflow, material operational dependency, or tool-enabled assistant | Security, privacy, business owner, continuity owner, and senior technology approver |
| Tier 4 | 17+ or automatic escalation | High-impact, regulated, public-facing, agentic, or rights-affecting system | Executive risk owner, legal/privacy, security leadership, and formal release gate |

| Field | Response |
| --- | --- |
| Total score | |
| Automatic escalation trigger used? | Yes / No |
| Final tier | Tier 1 / Tier 2 / Tier 3 / Tier 4 |
| Rationale for final tier | |
| Accepted by risk owner | Yes / No |
| Conditions before launch | |

## 5. Required Control Baseline

| Control Area | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AI system intake | Required | Required | Required | Required | | |
| Data-flow record | Recommended | Required | Required | Required | | |
| Vendor due diligence | If external | Required if external | Required | Required | | |
| Model card or provider assurance record | Recommended | Required | Required | Required | | |
| Prompt, output, and tool logging decision | Recommended | Required | Required | Required | | |
| Access review | Recommended | Required | Required | Required before launch and recurring | | |
| Human approval matrix | If actions exist | Required for material actions | Required | Required with dual approval for high-impact actions | | |
| Red-team or adversarial test plan | Optional | Recommended | Required | Required with retest evidence | | |
| Incident severity mapping | Recommended | Required | Required | Required | | |
| Continuity and exit plan | Recommended | Recommended | Required | Required with tested fallback | | |
| Control test schedule | Optional | Required for key controls | Required | Required with executive reporting | | |

## 6. Residual Risk and Launch Decision

| Question | Response |
| --- | --- |
| Are all Tier-required controls implemented or formally excepted? | |
| Are known limitations documented for users and reviewers? | |
| Are monitoring, escalation, and evidence owners assigned? | |
| Are fallback and rollback procedures tested? | |
| Is residual risk accepted by the correct owner? | |
| Launch decision | Approve / Approve with conditions / Defer / Reject |

## 7. Review Cadence

| Tier | Minimum Review Cadence | Change Events That Require Re-Tiering |
| --- | --- | --- |
| Tier 1 | Annual | New sensitive data, new provider, new tool access, external exposure |
| Tier 2 | Every 6 months | New data category, new user population, new model/provider, expanded logging, material workflow change |
| Tier 3 | Quarterly | New tool/API access, public exposure, privacy-impact change, automation increase, incident, control failure |
| Tier 4 | Monthly or release-cycle based | Any model, provider, data, tool, approval, legal, continuity, or user-impact change |

## 8. Sign-Off

| Role | Name | Decision | Date | Notes |
| --- | --- | --- | --- | --- |
| Use case owner | | | | |
| Technical owner | | | | |
| Security reviewer | | | | |
| Privacy reviewer | | | | |
| Continuity owner | | | | |
| Executive risk owner | | | | |
