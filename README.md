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
| Vendor due diligence | AI vendor questionnaire for data handling, security, model controls, compliance, and continuity |
| Logging and retention | Checklist for prompt, output, embedding, tool-call, and operational log governance |
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
6. Complete `templates/vendor-ai-due-diligence.md` before approving external AI services.
7. Review logging decisions with `templates/ai-logging-retention-checklist.md`.
8. Run a tabletop exercise from `playbooks/` before production rollout.

## Artifact Catalog

| Artifact | Purpose |
| --- | --- |
| `templates/ai-change-impact-assessment.md` | Review governance, data, model, tool, compliance, and continuity impact after AI system changes |
| `templates/ai-data-flow-record.md` | Document AI data sources, processing steps, destinations, classifications, and controls |
| `templates/ai-access-review.md` | Review user, administrator, service account, API key, and agent tool permissions |
| `templates/human-approval-matrix.md` | Define when AI-assisted actions require review, approval, or dual approval |
| `templates/board-ai-security-assurance-checklist.md` | Executive assurance checklist for approving high-impact AI systems |
| `templates/ai-control-evidence-raci.md` | Assign control ownership and evidence accountability across AI governance roles |
| `templates/prompt-injection-test-record.md` | Record direct and indirect prompt injection test cases, outcomes, and remediation |
| `templates/ai-agent-tool-inventory.csv` | Track agent tools, environments, permissions, data access, owners, and review dates |
| `templates/ai-exception-register.csv` | Track AI governance exceptions, expirations, risk owners, and compensating controls |
| `templates/ai-model-card-lite.md` | Capture lightweight model use, limitations, oversight, and risk notes |
| `templates/model-provider-exit-plan.md` | Plan provider exit triggers, fallback options, data export, and deletion evidence |
| `policies/ai-log-retention-policy.md` | Define retention expectations for prompts, outputs, embeddings, tool calls, and security events |
| `playbooks/ai-data-leak-triage.md` | Triage suspected AI data exposure through prompts, outputs, logs, embeddings, or providers |
| `playbooks/agentic-tool-misuse-response.md` | Contain and investigate incorrect or unauthorized agent tool actions |
| `examples/edtech-ai-assistant-privacy-review.md` | Example privacy review for a student-facing AI assistant pilot |

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

<!-- portfolio:start -->
## Portfolio and Professional Profile

This repository is part of the professional portfolio of [Musaab Hasan](https://musaab.info), focused on cybersecurity, digital forensics, AI governance, EdTech, secure platforms, and research-driven digital transformation.

### Digital Forensics and Security Research Labs

- [Android Digital Forensics Lab](https://github.com/musaabhasan/android-forensics-lab) - Advanced Android forensics workbench for acquisition planning, anti-forensics evaluation, memory triage, evidence integrity, and case reconstruction.
- [Humanoid Robot Forensics Lab](https://github.com/musaabhasan/humanoid-robot-forensics-lab) - PHP/MySQL forensic casework platform for humanoid robot, companion app, and IoT evidence triage.
- [Smart Metering Security Lab](https://github.com/musaabhasan/smart-metering-security-lab) - Research portal based on smart metering security analysis for cyber-physical and smart-grid environments.
- [Drive-by Download ML Lab](https://github.com/musaabhasan/driveby-download-ml-lab) - Machine learning research portal for detecting drive-by download attacks and web-based malware delivery.
- [SQL Injection ML Detection Lab](https://github.com/musaabhasan/sqli-ml-detection-lab) - Research portal for SQL injection detection using machine learning and security telemetry.
- [IoT Board SSH Hardening Lab](https://github.com/musaabhasan/iot-board-ssh-hardening-lab) - SSH exposure assessment and hardening portal for IoT development boards and embedded Linux systems.
- [ZigBee WHAS Design Lab](https://github.com/musaabhasan/zigbee-whas-design-lab) - Research portal for designing and evaluating ZigBee wireless home automation systems.
- [Mammogram Fourier Analysis Lab](https://github.com/musaabhasan/mammogram-fourier-analysis-lab) - Medical image-processing research portal based on Fourier transform analysis for mammography.

### Security Culture and Transformation Platforms

- [Human Factors Risk Profiler](https://github.com/musaabhasan/human-factors-risk-profiler) - Human-centered security risk profiling portal for targeted interventions and behavior-aware controls.
- [Security Champion Network Portal](https://github.com/musaabhasan/security-champion-network-portal) - Platform for managing security champion networks, missions, recognition, and measurable impact.
- [Crisis Simulation Command Portal](https://github.com/musaabhasan/crisis-simulation-command-portal) - Cyber crisis simulation planning, scoring, and improvement platform for resilience exercises.
- [Behavioral Security Metrics Portal](https://github.com/musaabhasan/behavioral-security-metrics-portal) - Evidence-based security awareness metrics portal focused on behavior, culture, and intervention outcomes.
- [Security Culture Heatmap Portal](https://github.com/musaabhasan/security-culture-heatmap-portal) - Security culture maturity heatmap for norms, leadership signals, and organizational readiness.
- [Emerging Technology Security Culture Portal](https://github.com/musaabhasan/emerging-technology-security-culture-portal) - Adoption-readiness portal for emerging technology, governance, and security culture alignment.
- [AI Use Case Evaluation Portal](https://github.com/musaabhasan/ai-use-case-evaluation-portal) - Evaluation platform for AI use cases across value, feasibility, data readiness, privacy, ethics, and governance.
- [Transformation Roadmap Portal](https://github.com/musaabhasan/transformation-roadmap-portal) - Roadmap platform for moving security culture programs from compliance orientation to resilience and measurable change.

### Governance, Education, and Secure Enablement

- [Professional Development Registration System Framework](https://github.com/musaabhasan/pdrs-framework) - Secure registration and Moodle enrollment automation framework for professional development programs.
- [Multilingual Certificate Issuer](https://github.com/musaabhasan/multilingual-certificate-issuer) - Arabic/English certificate design, PDF generation, and throttled SMTP distribution platform.
- [AI Security Governance Toolkit](https://github.com/musaabhasan/ai-security-governance-toolkit) - Practical AI security governance controls, templates, evidence registers, playbooks, and policy-as-code examples.

Professional profile and research portfolio: [https://musaab.info](https://musaab.info)
<!-- portfolio:end -->
