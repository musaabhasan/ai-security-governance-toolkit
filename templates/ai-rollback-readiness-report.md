# AI Rollback Readiness Report

Use this report before releasing model, prompt, provider, safety-filter, embedding, or RAG index changes. It turns `templates/ai-rollback-readiness-register.csv` into an owner queue for rollback runbooks, drill evidence, evaluation baselines, traffic-shift plans, schema compatibility, credential rollback, communications, and approval state.

## When To Use

- Before approving a high-impact model or provider change.
- Before publishing a prompt/persona release that changes safety, citation, or tool behavior.
- Before rebuilding a RAG index or replacing embedding models.
- Before production launches where rollback must happen quickly during an incident.

## Command Examples

Generate the Markdown report:

```bash
python scripts/rollback_readiness_report.py examples/ai-rollback-readiness-sample.csv --as-of 2026-05-09
```

Generate JSON:

```bash
python scripts/rollback_readiness_report.py examples/ai-rollback-readiness-sample.csv --format json
```

Fail a release gate when high-risk rollback gaps exist:

```bash
python scripts/rollback_readiness_report.py examples/ai-rollback-readiness-sample.csv --as-of 2026-05-09 --fail-on-high
```

## Required Evidence

- Trigger condition for rollback.
- Tested rollback runbook.
- Baseline evaluation or monitoring evidence.
- Traffic shift, feature flag, router, or alias rollback plan.
- Data schema compatibility confirmation.
- Credential rollback readiness.
- Communication plan and approval status.
- Recent rollback drill date and next drill due date.

## Owner Queue

High-risk gaps should block release when a runbook, baseline evaluation, schema compatibility, credential rollback, approval, or drill freshness is missing. Medium-risk gaps should be resolved before the next change advisory, model-risk review, or operational readiness meeting.
