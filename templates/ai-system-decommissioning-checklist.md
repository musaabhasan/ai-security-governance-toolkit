# AI System Decommissioning Checklist

Use this checklist when retiring, replacing, pausing, or materially reducing an AI system, model, assistant, agent, or AI-enabled vendor service. Decommissioning should preserve required evidence while preventing abandoned models, credentials, logs, embeddings, datasets, integrations, and tool permissions from becoming unmanaged risk.

## 1. Decommissioning Scope

| Field | Response |
| --- | --- |
| System name | |
| Business owner | |
| Technical owner | |
| Security reviewer | |
| Privacy / data protection reviewer | |
| Decommissioning reason | End of pilot / vendor exit / replacement / risk decision / redundancy / incident response / other |
| Planned shutdown date | |
| Final decision owner | |

## 2. Dependency Inventory

| Dependency | Owner | Action Required | Evidence |
| --- | --- | --- | --- |
| Model or provider account | | Disable / retain / migrate / delete | |
| API keys or service credentials | | Revoke / rotate / transfer | |
| RAG corpus or vector store | | Archive / export / delete / re-index | |
| Prompt templates and system instructions | | Archive / migrate / delete | |
| Conversation logs and audit logs | | Retain / export / delete under policy | |
| Uploaded files or user content | | Return / archive / delete | |
| Fine-tuning or evaluation datasets | | Retain / delete / anonymize | |
| Agent tools, APIs, plugins, or workflows | | Disable / revoke / migrate | |
| Monitoring, alerting, and dashboards | | Disable / retain read-only | |
| Documentation and user-facing guidance | | Update / retire / redirect | |

## 3. Data and Evidence Handling

| Control Question | Response | Evidence |
| --- | --- | --- |
| Is there a legal, contractual, research, audit, or operational retention requirement? | | |
| Have prompts, outputs, embeddings, logs, and uploaded files been classified before deletion or retention? | | |
| Are retained records minimized to what is required? | | |
| Are retained records protected with access control and encryption? | | |
| Are deletion requests and certificates of deletion collected from vendors where applicable? | | |
| Are vector stores, caches, temporary files, and search indexes included in deletion scope? | | |
| Are model/provider telemetry exports retained where needed for audit or incident review? | | |
| Is user-facing data export or notification required? | | |

## 4. Access and Credential Revocation

| Access Type | Required Action | Completed | Evidence |
| --- | --- | --- | --- |
| Human user access | Disable roles and groups | Yes / No | |
| Administrator access | Remove admins and emergency accounts | Yes / No | |
| Service accounts | Disable or delete | Yes / No | |
| API keys and tokens | Revoke and rotate dependent credentials | Yes / No | |
| OAuth applications | Disable client or revoke scopes | Yes / No | |
| Agent tool permissions | Remove tool bindings and workflow permissions | Yes / No | |
| Vendor portals | Remove tenant, workspace, or integration access | Yes / No | |
| CI/CD secrets | Remove unused deployment secrets | Yes / No | |

## 5. Integration Shutdown

| Integration | Shutdown Check | Completed | Notes |
| --- | --- | --- | --- |
| Identity provider | Groups, SSO apps, and SCIM mappings removed | Yes / No | |
| LMS / student system / HR / CRM | Data connectors disabled and tested | Yes / No | |
| Email, ticketing, or workflow automation | Send/update actions disabled | Yes / No | |
| Webhooks and callback URLs | Endpoints removed or return safe status | Yes / No | |
| Scheduled jobs and queues | Jobs disabled and queues drained | Yes / No | |
| Knowledge-base ingestion | Crawlers and sync jobs stopped | Yes / No | |
| Analytics exports | Export jobs stopped or migrated | Yes / No | |

## 6. Risk and Continuity Review

| Question | Response |
| --- | --- |
| What business process replaces the AI system? | |
| Is there an approved manual fallback? | |
| Are users notified of the retirement date and replacement path? | |
| Are unresolved incidents, exceptions, or audit findings closed or transferred? | |
| Are regulatory, contractual, research, or accessibility obligations still covered? | |
| Are lessons learned captured for future AI approvals? | |

## 7. Final Verification

| Verification Step | Owner | Result | Evidence |
| --- | --- | --- | --- |
| System login disabled | | Pass / Fail | |
| API endpoint disabled or protected | | Pass / Fail | |
| Tool calls no longer execute | | Pass / Fail | |
| Vendor access revoked | | Pass / Fail | |
| Credentials revoked or rotated | | Pass / Fail | |
| Data deletion or retention evidence collected | | Pass / Fail | |
| Monitoring shows no unexpected traffic | | Pass / Fail | |
| Documentation updated | | Pass / Fail | |

## 8. Closure Decision

| Field | Response |
| --- | --- |
| Decommissioning status | Complete / Complete with exceptions / Deferred |
| Open exceptions | |
| Residual risk accepted by | |
| Closure date | |
| Next review date if retained evidence remains | |
