# AI Data Lineage Report

Use this report before approving a new AI system, RAG index, fine-tuning dataset, feature pipeline, model/provider change, or research dataset reuse. It turns `templates/ai-data-lineage-register.csv` into a governance review queue for data provenance, source ownership, transformation evidence, legal basis, retention, cross-border transfer, and review freshness.

## When To Use

- Before moving a prototype assistant, agent, RAG workflow, or analytics model into production.
- Before refreshing a vector index, fine-tuning dataset, evaluation dataset, or prompt-log analysis corpus.
- Before sharing research data, prompt traces, transcripts, or learning analytics with a third party.
- Before internal audit, privacy review, or model-risk review asks how a data asset entered an AI system.

## Required Evidence

- Source system and source owner for every data asset.
- Data classification and downstream use statement.
- Legal basis, consent scope, or approved data-use decision for sensitive or regulated records.
- Transformation evidence showing how raw data became prompts, embeddings, labels, features, fine-tuning data, or outputs.
- Quality check result, retention rule, transfer/subprocessor record, and review owner.
- Last reviewed and next review dates.

## Command Examples

Generate the Markdown report:

```bash
python scripts/data_lineage_report.py examples/ai-data-lineage-sample.csv --as-of 2026-05-09
```

Generate machine-readable output for dashboards or evidence repositories:

```bash
python scripts/data_lineage_report.py examples/ai-data-lineage-sample.csv --format json
```

Fail a release or governance gate when high-risk lineage gaps exist:

```bash
python scripts/data_lineage_report.py examples/ai-data-lineage-sample.csv --as-of 2026-05-09 --fail-on-high
```

## Owner Review Queue

Treat high-risk items as release blockers when they involve sensitive data, missing owners, overdue lineage review, missing legal basis, or cross-border transfers without a subprocessor record. Medium-risk items should be resolved before the next governance forum, evaluation refresh, or data-source update.

## Review Questions

- Can the team explain where each prompt, embedding, evaluation case, label, feature, or model-training record originated?
- Are owners accountable for source data, transformation logic, quality checks, retention, and downstream use?
- Are regulated, student, personal, confidential, or restricted records tied to a documented legal basis or consent scope?
- Is there evidence that redaction, minimization, transformation, and quality checks happened before the data reached the AI system?
- Are cross-border transfers and subprocessors explicitly reviewed rather than inferred from provider settings?
- Are lineage records refreshed when models, providers, indexes, prompts, or data pipelines change?
