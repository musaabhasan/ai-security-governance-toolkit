# AI Risk to Control Mapping

This mapping translates common AI and LLM risk themes into practical governance controls. It is not a formal certification mapping.

| Risk Theme | Practical Control Response | Example Control IDs |
| --- | --- | --- |
| Prompt injection | Adversarial prompt testing, output validation, tool-use boundaries, incident playbooks | `AI-SEC-001`, `AI-AGT-001` |
| Sensitive information disclosure | Data classification, redaction, logging review, vendor data-use review | `AI-DATA-001`, `AI-DATA-002`, `AI-VND-001` |
| Excessive agency | Tool allowlists, scoped identities, human approval gates, action logging | `AI-ID-001`, `AI-AGT-001`, `AI-AGT-002` |
| Supply chain exposure | Vendor due diligence, model provenance checks, dependency review, contractual controls | `AI-VND-001` |
| Unbounded consumption | Usage thresholds, cost monitoring, rate limiting, abnormal behavior alerts | `AI-OPS-001` |
| Inaccurate or unsupported output | Human review, source attribution, confidence thresholds, output disclaimers | `AI-GOV-002`, `AI-SEC-001` |
| Model or provider outage | Business impact analysis, fallback process, manual service mode, recovery exercise | `AI-BCM-001` |
| Shadow AI adoption | Intake process, approval path, asset inventory, awareness and exception handling | `AI-GOV-001`, `AI-GOV-002` |
| Tool misuse | Mandatory mediation, scoped service accounts, deny-by-default policies, execution logs | `AI-ID-001`, `AI-AGT-001` |
| Audit failure | Evidence register, decision records, risk acceptance, periodic control testing | `AI-GOV-001`, `AI-OPS-001` |

## How To Use This Mapping

1. Select the AI use case.
2. Identify relevant risk themes.
3. Select controls from `control-catalog.yaml`.
4. Assign owners and evidence expectations.
5. Test the controls before production release.
6. Reassess after major model, vendor, prompt, tool, or data-flow changes.
