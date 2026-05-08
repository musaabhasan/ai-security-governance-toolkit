# AI Evaluation Evidence Report

Use this report before release approvals, model/provider changes, RAG index refreshes, high-impact workflow launches, and internal audit reviews. It checks whether AI evaluation evidence is current, reproducible, security-aware, and strong enough to support a release decision.

## Purpose

AI teams often run evaluations without preserving the evidence needed for governance. A pass rate is not enough. Reviewers need to know which dataset was used, which model and prompt were tested, whether security and bias cases were included, whether human review occurred, and whether failures should block release.

The companion register is `ai-evaluation-evidence-register.csv`.

## Required Evidence Fields

| Field | Why It Matters |
| --- | --- |
| `evaluation_id` | Stable identifier for audit and release references |
| `system` | AI system or workflow being evaluated |
| `evaluation_suite` | Name of the test suite or benchmark |
| `evaluation_type` | RAG, safety, bias, tool-use, citation, robustness, or answer-quality scope |
| `model_or_provider` | Model, provider, gateway, or runtime under test |
| `dataset_reference` and `dataset_version` | Evaluation dataset lineage |
| `prompt_version` | Prompt or system-instruction version under test |
| `index_version` | RAG index, knowledge base, corpus, or tool-surface version |
| `cases_total` | Number of cases in the suite |
| `pass_rate` | Objective outcome or normalized score |
| `critical_failures` and `high_failures` | Release-blocking findings |
| `human_review_completed` | Human review of failures, edge cases, and representative samples |
| `security_cases_included` | Prompt injection, data exfiltration, abuse, or tool-misuse coverage |
| `bias_cases_included` | Fairness, accessibility, learner impact, or protected-class coverage |
| `citation_cases_included` | Source-support, abstention, citation, or evidence-linkage coverage |
| `last_run_date` | Evidence freshness |
| `owner` | Accountable owner for remediation |
| `release_decision` | Draft, hold, approved, rejected, or accepted risk decision |
| `status` | Active, pilot, release candidate, production, retired, or closed |

## Report Command

```bash
python scripts/evaluation_evidence_report.py examples/ai-evaluation-evidence-sample.csv --as-of 2026-05-09
```

Write Markdown:

```bash
python scripts/evaluation_evidence_report.py examples/ai-evaluation-evidence-sample.csv --output reports/ai-evaluation-evidence.md
```

Write JSON for dashboards:

```bash
python scripts/evaluation_evidence_report.py examples/ai-evaluation-evidence-sample.csv --format json --output reports/ai-evaluation-evidence.json
```

Fail a release gate when high-severity gaps are present:

```bash
python scripts/evaluation_evidence_report.py examples/ai-evaluation-evidence-sample.csv --fail-on-high
```

Tune thresholds:

```bash
python scripts/evaluation_evidence_report.py examples/ai-evaluation-evidence-sample.csv --max-age-days 30 --min-pass-rate 0.92
```

## Finding States

| State | Meaning | Typical Action |
| --- | --- | --- |
| `missing_dataset_lineage` | Dataset reference or version is missing | Record dataset source, version, and hash before relying on results |
| `empty_evaluation_suite` | The suite has no cases | Add representative cases before release review |
| `critical_eval_failures` | Critical failures exist | Block release until remediated |
| `high_eval_failures` | High failures exist | Remediate or document formal risk acceptance |
| `missing_pass_rate` | No score is recorded | Add objective scoring or pass/fail result |
| `pass_rate_below_threshold` | Score is below the configured threshold | Tune, remediate, or hold release |
| `missing_human_review` | Production or release evidence lacks human review | Review edge cases, representative failures, and release-significant samples |
| `missing_security_cases` | Security coverage is absent for active or release-bound systems | Add prompt-injection, exfiltration, abuse, or tool-misuse cases |
| `missing_citation_cases` | RAG evaluation lacks citation/source-support coverage | Add citation, abstention, and unsupported-claim cases |
| `missing_bias_cases` | Education-facing evaluation lacks bias or learner-impact coverage | Add fairness, accessibility, and learner-impact cases |
| `missing_run_metadata` | Model/provider or prompt version is missing | Record reproducibility metadata |
| `missing_run_date` | Last run date is missing | Record evidence freshness |
| `stale_evaluation` | Evidence is older than the configured threshold | Re-run against the current model, prompt, index, and tool surface |
| `current` | Evidence is acceptable for routine cadence | Keep under normal monitoring |

## Review Guidance

Evaluation evidence should be tied to the exact system version being approved. A strong record includes model/provider version, prompt version, dataset version, index version, threshold policy, reviewer notes, failure analysis, and the release decision.

For RAG systems, keep retrieval quality separate from answer quality. For agentic systems, evaluate tool-use decisions and approval boundaries separately from final-answer quality. For education-facing systems, include learner-impact, accessibility, fairness, and citation/abstention cases.

