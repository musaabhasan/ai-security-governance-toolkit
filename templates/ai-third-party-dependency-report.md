# AI Third-Party Dependency Report

Use this report before production rollout, renewal, major model/provider changes, audit preparation, or vendor-risk review. It turns the `ai-third-party-dependency-register.csv` into an actionable queue for AI providers, model APIs, vector stores, agent platforms, observability tools, email services, workflow tools, and other services that process or influence AI system behavior.

## Review Objectives

- Identify AI dependencies with missing or incomplete data-processing agreements.
- Confirm whether subprocessors are listed and reviewed for systems handling sensitive, student, regulated, or confidential data.
- Detect stale or missing security assurance evidence such as SOC 2, ISO 27001, penetration-test summaries, or equivalent control attestations.
- Surface critical dependencies without tested exit and continuity plans.
- Group issues by provider and contract owner so remediation can be assigned.

## Register Fields

| Field | Purpose |
| --- | --- |
| `dependency_id` | Stable identifier for the dependency record. |
| `system` | AI system, assistant, workflow, research tool, or platform using the dependency. |
| `provider` | Vendor, open-source service operator, hosted platform, or internal shared service. |
| `service_category` | Model inference, embedding, vector database, observability, email, storage, workflow, LMS integration, or similar category. |
| `dependency_type` | Primary processor, subprocessor, critical dependency, fallback provider, evaluation service, or support service. |
| `data_access` | Data class visible to the dependency. Examples: public, internal, student records, research participant data, confidential, regulated. |
| `criticality` | Low, medium, high, or critical. |
| `contract_owner` | Accountable owner for contract, assurance, and remediation. |
| `approved_use` | Approved purpose and boundaries for the dependency. |
| `region` | Processing or hosting region when known. |
| `subprocessors_listed` | `yes`, `no`, or `unknown`. |
| `dpa_status` | `executed`, `approved`, `pending`, `missing`, or `not_required`. |
| `security_assurance` | Current security assurance artifact or control evidence. |
| `assurance_review_date` | Last assurance review date in `YYYY-MM-DD` format. |
| `exit_plan_status` | `approved`, `draft`, `missing`, or equivalent status. |
| `business_continuity_status` | `tested`, `documented`, `untested`, `missing`, or equivalent status. |
| `status` | Active, pilot, proposed, retired, blocked, or equivalent lifecycle state. |
| `next_review_date` | Next governance/vendor review date in `YYYY-MM-DD` format. |
| `notes` | Constraints, conditions, or remediation context. |

## Report Command

```bash
python scripts/third_party_dependency_report.py examples/ai-third-party-dependency-sample.csv --as-of 2026-05-08
```

Generate JSON for dashboards or CI gates:

```bash
python scripts/third_party_dependency_report.py examples/ai-third-party-dependency-sample.csv --as-of 2026-05-08 --format json --output reports/third-party-dependencies.json
```

Block a release or renewal review when high-severity dependency gaps exist:

```bash
python scripts/third_party_dependency_report.py examples/ai-third-party-dependency-sample.csv --as-of 2026-05-08 --fail-on-high
```

## Severity Model

| State | Default Severity | Meaning |
| --- | --- | --- |
| `missing_dpa` | High for sensitive data, otherwise medium | Dependency lacks an executed or approved data-processing agreement when one is expected. |
| `missing_subprocessor_transparency` | High for sensitive data, otherwise medium | Subprocessor list is missing, marked no, or unknown. |
| `missing_security_assurance` | High for high/critical dependencies, otherwise medium | No current assurance artifact is recorded. |
| `overdue_assurance_review` | High for high/critical dependencies, otherwise medium | Assurance review date is older than the configured review interval. |
| `assurance_review_due_soon` | Medium | Review date is approaching within the warning window. |
| `critical_exit_plan_gap` | High | Critical dependency lacks an approved exit plan. |
| `critical_continuity_gap` | High | Critical dependency lacks tested continuity evidence. |
| `review_overdue` | Medium | Governance review date has passed. |
| `review_due_soon` | Medium | Governance review is approaching. |
| `current` | Low | No immediate reporting gap is detected. |

## Review Workflow

1. Export active AI providers, model APIs, vector stores, RAG platforms, tool gateways, observability systems, workflow systems, and notification services into the register.
2. Confirm data access and criticality with the system owner and data protection lead.
3. Run the report before release, renewal, material provider change, or internal audit.
4. Route high-severity items to the provider owner and system risk owner.
5. Record remediation evidence in the evidence register after contracts, assurance packages, subprocessor reviews, exit plans, or continuity tests are completed.

## Governance Notes

- A dependency can be operationally small but governance-critical if it receives prompts, outputs, embeddings, student data, research participant data, credentials, or agent tool traces.
- A fallback provider should be reviewed even when it is rarely used because failover often happens during incidents.
- For agentic systems, review tool gateways, memory stores, and orchestration services as AI dependencies, not only model providers.
