# OWASP LLM 2025 Control Mapping

This mapping translates the OWASP Top 10 for Large Language Model Applications 2025 into practical governance controls, release gates, monitoring signals, and evidence expectations.

Primary references:

- OWASP GenAI Security Project: <https://genai.owasp.org/>
- OWASP Top 10 for LLM Applications 2025: <https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/>
- Official release repository: <https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/releases>

## How To Use This Mapping

1. Identify which OWASP LLM risks apply to the AI system, assistant, RAG workflow, or agent.
2. Map each applicable risk to the toolkit control IDs listed in `owasp-llm-2025-control-mapping.csv`.
3. Attach required evidence to the AI system approval packet.
4. Treat the release gate as a go/no-go condition before production rollout or major change approval.
5. Convert the monitoring signal into dashboards, alerts, review queues, or control-test samples.

## Risk-To-Control Summary

| OWASP risk | Governance focus | Toolkit controls |
| --- | --- | --- |
| LLM01:2025 Prompt Injection | Direct and indirect instruction attacks against model behavior, tools, and retrieval context | `AI-SEC-001`, `AI-AGT-001`, `AI-OPS-001` |
| LLM02:2025 Sensitive Information Disclosure | Leakage of personal, confidential, credential, or proprietary data through prompts, outputs, logs, or context | `AI-DATA-001`, `AI-DATA-002`, `AI-OPS-001` |
| LLM03:2025 Supply Chain | Provider, model, dataset, plugin, tool, and deployment dependency assurance | `AI-VND-001`, `AI-GOV-002`, `AI-BCM-001` |
| LLM04:2025 Data and Model Poisoning | Data lineage, source approval, poisoning tests, and monitoring for training, fine-tuning, RAG, and evaluation data | `AI-DATA-001`, `AI-SEC-001`, `AI-OPS-001` |
| LLM05:2025 Improper Output Handling | Validation before model output is used as code, commands, records, content, or operational decisions | `AI-SEC-001`, `AI-AGT-001`, `AI-AGT-002` |
| LLM06:2025 Excessive Agency | Scoped service identities, explicit tool allowlists, and human approval for high-impact actions | `AI-ID-001`, `AI-AGT-001`, `AI-AGT-002` |
| LLM07:2025 System Prompt Leakage | Protection of hidden prompts, policies, tool descriptions, and implementation details | `AI-DATA-001`, `AI-DATA-002`, `AI-SEC-001` |
| LLM08:2025 Vector and Embedding Weaknesses | Retrieval authorization, chunk integrity, embedding-store access, and stale source review | `AI-DATA-001`, `AI-SEC-001`, `AI-OPS-001` |
| LLM09:2025 Misinformation | Grounding, evaluation, user-impact review, human oversight, and post-release dispute monitoring | `AI-GOV-001`, `AI-GOV-002`, `AI-SEC-001`, `AI-OPS-001` |
| LLM10:2025 Unbounded Consumption | Rate limits, cost thresholds, throttling, continuity planning, and model-extraction monitoring | `AI-OPS-001`, `AI-BCM-001`, `AI-ID-001` |

## Evidence Expectations

The mapping is intentionally evidence-first. For each applicable risk, governance reviewers should be able to inspect:

- the assigned control owner,
- the control evidence reference,
- the latest test or review result,
- the release decision,
- residual risk acceptance if the release gate is not fully satisfied,
- monitoring evidence after production release.

## Release Gate Guidance

Use the release gate column in the CSV as the minimum approval rule. A project can strengthen it with stricter thresholds, but it should not release a production AI system when a listed gate is unresolved and no explicit risk acceptance exists.

Examples:

- LLM01: block release when high-severity prompt injection findings remain open.
- LLM06: block release when an agent has broad credentials, unreviewed tools, or missing approval gates.
- LLM10: block release when usage limits, cost alerts, and fallback procedures are not tested.

## Reporting

Generate a mapping report:

```bash
python scripts/owasp_llm_mapping_report.py --format markdown
python scripts/owasp_llm_mapping_report.py --format json
```

Use `--fail-on-missing-gate` in CI when the CSV is maintained by multiple contributors.
