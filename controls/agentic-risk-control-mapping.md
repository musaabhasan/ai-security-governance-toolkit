# Agentic Risk Control Mapping

This mapping translates common agentic AI failure modes into practical governance controls, evidence expectations, release gates, and monitoring signals. It is designed for systems where an AI assistant or agent can call tools, read documents, write records, trigger workflows, communicate with other agents, or act with delegated authority.

The companion CSV is `controls/agentic-risk-control-mapping.csv`. It can be reviewed directly in a spreadsheet or converted into Markdown or JSON with `scripts/agentic_risk_control_report.py`.

## Why This Mapping Exists

Agentic systems create risk through a chain of decisions and actions, not only through a single model response. A useful control mapping therefore needs to connect:

- the failure mode,
- the controls that should prevent or detect it,
- the evidence needed for review,
- the test that proves the control works,
- the release gate that blocks unsafe rollout,
- the runtime signal that should be monitored after launch.

This structure helps security, audit, privacy, platform, and risk owners discuss the same agentic workflow without relying on vague terms such as "guardrails" or "safe mode".

## Mapped Risk Themes

| Risk ID | Risk Theme | Primary Control Focus |
| --- | --- | --- |
| AR-001 | Instruction and goal manipulation | Prompt-injection testing and tool-boundary controls |
| AR-002 | Tool misuse and unsafe action | Tool allowlists, approval workflow, and action logs |
| AR-003 | Privilege and delegation abuse | Scoped identity and delegated authority evidence |
| AR-004 | Sensitive data disclosure | Data classification, logging decisions, and vendor data-use review |
| AR-005 | Memory and state poisoning | Memory promotion policy and state-change evidence |
| AR-006 | Agent supply-chain exposure | Vendor, dependency, prompt, model, and tool review |
| AR-007 | Inter-agent communication failure | Agent responsibility boundaries and message provenance |
| AR-008 | Resource and cost exhaustion | Usage thresholds, rate limits, and continuity planning |
| AR-009 | Audit and non-repudiation gap | Execution receipts, approval records, and evidence registers |
| AR-010 | Model or provider behavior drift | Change approval, regression evidence, and fallback tests |

## Operating Workflow

1. Start with the AI system intake and risk tiering record.
2. Identify which agentic risk themes apply to the workflow.
3. Review the mapped control IDs against `controls/control-catalog.yaml`.
4. Confirm the required evidence exists before pilot or production release.
5. Run the minimum test for every applicable risk theme.
6. Apply the release gate when evidence is missing or a high-impact test fails.
7. Add runtime monitoring signals to the model monitoring KPI register or security alert backlog.

## Report Generator

Render the mapping as Markdown:

```bash
python scripts/agentic_risk_control_report.py controls/agentic-risk-control-mapping.csv
```

Render JSON for evidence repositories or dashboards:

```bash
python scripts/agentic_risk_control_report.py controls/agentic-risk-control-mapping.csv --format json
```

Fail a pipeline when a mapping row has no release gate:

```bash
python scripts/agentic_risk_control_report.py controls/agentic-risk-control-mapping.csv --fail-on-missing-gate
```

## Review Questions

- Are all tool-enabled AI systems mapped to at least one agentic risk theme?
- Does every high-impact action have a human approval or compensating control?
- Can the team reconstruct which prompt, retrieved context, policy decision, approval, and tool call produced an outcome?
- Are memory writes, agent-to-agent handoffs, and provider changes treated as risk-relevant changes?
- Are monitoring signals routed to an accountable owner with an escalation path?
