# AI Security Governance Toolkit

Practical governance artifacts for organizations adopting large language models, AI assistants, and agentic workflows in regulated, education, and public-sector environments.

This toolkit is built around a simple premise: AI security is not only a model problem. It is a governance, data, identity, continuity, vendor, assurance, and operating-model problem.

## Who This Is For

- Information security and risk leaders building AI governance programs
- IT and digital transformation teams introducing AI-assisted workflows
- Education technology teams evaluating AI tutors, assistants, and learning tools
- Internal audit, compliance, and assurance teams reviewing AI control evidence
- Researchers and practitioners translating AI security guidance into practical operations

## What Is Inside

| Area | Artifacts |
| --- | --- |
| AI system intake | Initial AI use-case review, data classification, deployment model, ownership, and approval path |
| Risk management | AI risk register, control ownership, inherent/residual scoring, and decision tracking |
| Control catalog | Governance, identity, data, model, agent, vendor, monitoring, and continuity controls |
| Evidence management | Evidence register, test records, exception tracking, and audit-ready documentation |
| Agentic safety | Tool-use review, privilege boundaries, human approval gates, and execution logging |
| EdTech example | AI assistant governance profile for learning platforms and student-facing workflows |
| Playbooks | Prompt injection incident response and AI service outage tabletop scenarios |
| Policy as code | Open Policy Agent examples for AI tool execution decisions |

## Reference Frameworks

The toolkit is designed to be framework-aware without pretending to replace formal assurance work.

- NIST AI Risk Management Framework: <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST Cybersecurity Framework: <https://www.nist.gov/cyberframework>
- OWASP Top 10 for Large Language Model Applications: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- OWASP GenAI Security Project: <https://genai.owasp.org/>

## Quick Start

1. Copy `templates/ai-system-intake.md` for each AI use case.
2. Record risks in `templates/ai-risk-register.csv`.
3. Select controls from `controls/control-catalog.yaml`.
4. Track evidence in `templates/evidence-register.csv`.
5. Use `templates/agentic-tool-review.md` before allowing AI agents to call tools or APIs.
6. Run a tabletop exercise from `playbooks/` before production rollout.

## Suggested Repository Use

This repo can support:

- internal AI governance workshops
- AI system approval reviews
- EdTech AI assistant assessments
- vendor due diligence
- policy and evidence design
- control mapping work
- research companion material
- public speaking or training demonstrations

## Project Principles

- Controls must have owners.
- AI tools must have bounded authority.
- Data classification must happen before model selection.
- Human approval must be explicit for high-impact actions.
- Evidence must be created during operations, not reconstructed after incidents.
- Continuity planning must include model, provider, integration, and data dependencies.
- Security reviews must cover prompts, context, tools, plugins, APIs, vendors, logs, and outputs.

## Status

This is an initial public toolkit. It is intended to grow through practical examples, mappings, and implementation notes.

## Disclaimer

This repository provides practical security governance material. It is not legal advice, regulatory advice, or a substitute for formal risk assessment, audit, or compliance review.
