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
| Risk management | AI risk tiering, AI risk register, risk-register reporting, control ownership, inherent/residual scoring, and decision tracking |
| Control catalog | Governance, identity, data, model, agent, vendor, monitoring, and continuity controls |
| Evidence management | Evidence register, test records, exception tracking, and audit-ready documentation |
| Evidence quality | Evidence freshness, ownership, source, cadence, status, and owner-review queues |
| Control testing | Evidence packs and examples for AI control design and operating-effectiveness review |
| Evaluation evidence | Release-readiness reporting for AI evaluation suites, dataset lineage, security cases, human review, pass rates, and stale evidence |
| Exception management | Aging report for expired, expiring, missing-expiration, and inconsistent AI governance exceptions |
| Data deletion evidence | Register and report for prompt, output, file, embedding, log, vector-store, and third-party deletion proof |
| Vendor due diligence | AI procurement scoring, vendor questionnaire, data handling, security, model controls, compliance, and continuity |
| Third-party dependency assurance | Provider/subprocessor register, assurance review, DPA status, subprocessor transparency, exit planning, and continuity evidence |
| Logging and retention | Checklist for prompt, output, embedding, tool-call, and operational log governance |
| Agentic safety | Tool-use review, privilege boundaries, human approval gates, and execution logging |
| Agentic risk mapping | Agentic failure modes mapped to controls, evidence, release gates, monitoring signals, and owner roles |
| OWASP LLM 2025 mapping | OWASP LLM application risks mapped to toolkit controls, evidence, release gates, monitoring signals, and owner queues |
| NIST AI RMF crosswalk | Govern, Map, Measure, and Manage functions mapped to controls, evidence, review cadence, and owner roles |
| Access recertification | User, administrator, service account, API key, break-glass, and agent tool permission review |
| Red-team readiness | Scenario-based AI red-team test planning, evidence capture, and release decisions |
| Red-team taxonomy | Finding classification by risk theme, severity floor, release decision, owner role, and control coverage |
| Incident response | AI-specific incident severity classification, escalation triggers, and evidence preservation |
| Incident evidence | Register and report for AI incident timelines, containment evidence, preserved logs, privacy review, communications, and remediation queues |
| Tabletop evidence | Exercise evidence register and reporting for decision logs, containment, communications, fallback, privacy review, and remediation |
| Decommissioning | Retirement checklist for model, provider, data, credential, log, vector-store, and integration shutdown |
| Model/provider changes | Approval workflow for model, provider, endpoint, embedding, safety-filter, region, and agent-runtime changes |
| Model monitoring | KPI register for quality, safety, retrieval integrity, drift, security, reliability, cost, privacy, and oversight |
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
2. Classify the use case with `templates/ai-risk-tiering-decision-record.md`.
3. Record risks in `templates/ai-risk-register.csv`.
4. Select controls from `controls/control-catalog.yaml`.
5. Track evidence in `templates/evidence-register.csv`.
6. Schedule operating-effectiveness tests in `templates/ai-control-test-schedule.csv`.
7. Use `templates/agentic-tool-review.md` before allowing AI agents to call tools or APIs.
8. Score external AI products with `templates/ai-procurement-scoring-worksheet.md`.
9. Complete `templates/vendor-ai-due-diligence.md` before approving external AI services.
10. Review logging decisions with `templates/ai-logging-retention-checklist.md`.
11. Run a tabletop exercise from `playbooks/` before production rollout.
12. Track tabletop exercise evidence with `templates/ai-tabletop-exercise-evidence-register.csv`.
13. Use `templates/ai-system-decommissioning-checklist.md` before retiring, replacing, or pausing an AI system.
14. Use `templates/model-provider-change-approval.md` before changing models, providers, endpoints, embeddings, regions, or safety filters.
15. Track production health with `templates/model-monitoring-kpi-register.md`.
16. Package control test evidence with `templates/ai-control-test-evidence-pack.md`.
17. Review active exceptions with `scripts/exception_aging_report.py`.
18. Summarize residual risk and owner review queues with `scripts/risk_register_report.py`.
19. Review deletion evidence gaps with `scripts/data_deletion_evidence_report.py`.
20. Review provider, subprocessor, and critical AI dependency gaps with `scripts/third_party_dependency_report.py`.
21. Review tabletop evidence gaps with `scripts/tabletop_evidence_report.py`.
22. Review AI evaluation evidence readiness with `scripts/evaluation_evidence_report.py`.
23. Map agentic failure modes to controls and release gates with `scripts/agentic_risk_control_report.py`.
24. Review AI access recertification gaps with `scripts/access_recertification_report.py`.
25. Review AI incident evidence gaps with `scripts/incident_evidence_report.py`.
26. Map OWASP LLM 2025 risks to governance controls with `scripts/owasp_llm_mapping_report.py`.
27. Map NIST AI RMF functions to toolkit evidence with `scripts/nist_ai_rmf_crosswalk_report.py`.
28. Summarize AI red-team finding taxonomy coverage with `scripts/red_team_taxonomy_report.py`.
29. Review evidence quality and freshness with `scripts/evidence_quality_report.py`.

Validate repository artifacts before opening a pull request:

```bash
python scripts/validate_repository.py
```

The validator checks Markdown templates, template index coverage, control catalog structure, CSV headers, and policy-as-code examples.

## Artifact Catalog

| Artifact | Purpose |
| --- | --- |
| `templates/ai-change-impact-assessment.md` | Review governance, data, model, tool, compliance, and continuity impact after AI system changes |
| `templates/ai-risk-tiering-decision-record.md` | Classify AI systems into risk tiers, set required control baselines, define approval routes, and record residual-risk decisions |
| `templates/ai-system-decommissioning-checklist.md` | Retire AI systems safely by handling data, credentials, vector stores, logs, vendor access, integrations, evidence, and residual risk |
| `templates/ai-data-flow-record.md` | Document AI data sources, processing steps, destinations, classifications, and controls |
| `templates/ai-data-deletion-evidence-register.csv` | Track AI deletion requests, processors, scopes, due dates, completion evidence, verification, and retention exceptions |
| `templates/ai-data-deletion-evidence-report.md` | Operating guide for reporting overdue deletions, missing evidence, unverified completions, and retention-exception review queues |
| `templates/ai-access-review.md` | Review user, administrator, service account, API key, and agent tool permissions |
| `templates/ai-access-recertification-register.csv` | Track AI access assignments, privileged roles, service accounts, tokens, tool permissions, MFA, review dates, and recertification decisions |
| `templates/ai-access-recertification-report.md` | Operating guide for reviewing stale access, unowned tokens, separated users, break-glass approval, and high-impact agent tool permissions |
| `templates/human-approval-matrix.md` | Define when AI-assisted actions require review, approval, or dual approval |
| `templates/board-ai-security-assurance-checklist.md` | Executive assurance checklist for approving high-impact AI systems |
| `templates/ai-control-evidence-raci.md` | Assign control ownership and evidence accountability across AI governance roles |
| `templates/ai-control-test-evidence-pack.md` | Package AI control test objectives, population, sample, evidence inventory, exceptions, remediation, and reviewer conclusions |
| `templates/ai-control-test-evidence-examples.csv` | Spreadsheet-friendly examples for operating-effectiveness evidence packs across agent tools, prompt injection, RAG boundaries, monitoring, and continuity |
| `templates/ai-evidence-quality-report.md` | Operating guide for reviewing stale, missing, expired, unowned, or incomplete AI governance evidence |
| `templates/ai-evaluation-evidence-register.csv` | Track AI evaluation suites, dataset lineage, model/prompt/index versions, pass rates, failures, security/bias/citation coverage, human review, and release decisions |
| `templates/ai-evaluation-evidence-report.md` | Operating guide for reviewing stale, incomplete, low-scoring, or release-blocking AI evaluation evidence |
| `templates/ai-red-team-test-plan.md` | Plan AI red-team scenarios, evidence capture, pass/fail criteria, and release decisions |
| `controls/ai-red-team-finding-taxonomy.md` | Classify AI red-team findings by risk theme, severity floor, evidence, release decision, owner role, and control mapping |
| `controls/ai-red-team-finding-taxonomy.csv` | Spreadsheet-friendly red-team finding taxonomy for dashboards, approval gates, and remediation queues |
| `templates/ai-risk-register-report.md` | Operating guide for summarizing residual AI risk by theme, owner, and review-date status |
| `templates/ai-incident-severity-matrix.md` | Classify AI incidents by data exposure, tool misuse, output harm, identity impact, continuity, and escalation triggers |
| `templates/ai-incident-evidence-register.csv` | Track AI incident timelines, evidence references, data exposure, tool misuse, containment evidence, preserved logs, privacy review, communications, root cause, remediation due dates, and closure status |
| `templates/ai-incident-evidence-report.md` | Operating guide for reviewing missing AI incident evidence, privacy review gaps, tool-misuse log preservation, containment proof, incomplete timelines, and overdue remediation |
| `templates/prompt-injection-test-record.md` | Record direct and indirect prompt injection test cases, outcomes, and remediation |
| `templates/ai-agent-tool-inventory.csv` | Track agent tools, environments, permissions, data access, owners, and review dates |
| `templates/ai-control-test-schedule.csv` | Schedule AI control testing, evidence sources, test owners, results, and remediation due dates |
| `templates/ai-exception-register.csv` | Track AI governance exceptions, expirations, risk owners, and compensating controls |
| `templates/ai-exception-aging-report.md` | Operational guide for aging AI exceptions and converting registers into risk-owner review queues |
| `templates/ai-model-card-lite.md` | Capture lightweight model use, limitations, oversight, and risk notes |
| `templates/ai-procurement-scoring-worksheet.md` | Score AI vendors, hosted models, embedded AI features, and agent platforms before purchase, renewal, or expansion |
| `templates/ai-procurement-scoring-worksheet.csv` | Spreadsheet-friendly companion for weighted procurement scoring, evidence gaps, and remediation ownership |
| `templates/ai-third-party-dependency-register.csv` | Track AI providers, subprocessors, critical services, data access, DPA status, assurance evidence, exit plans, and continuity posture |
| `templates/ai-third-party-dependency-report.md` | Operating guide for reviewing third-party AI dependency gaps before release, renewal, audit, or provider change |
| `templates/ai-tabletop-exercise-evidence-register.csv` | Track AI tabletop exercise evidence, decision logs, containment tests, communications, fallback, privacy review, and remediation |
| `templates/ai-tabletop-evidence-report.md` | Operating guide for reviewing tabletop exercise gaps before release, audit, or governance review |
| `templates/model-provider-exit-plan.md` | Plan provider exit triggers, fallback options, data export, and deletion evidence |
| `templates/model-provider-change-approval.md` | Review model/provider changes for data handling, quality, safety, RAG behavior, tool use, cost, continuity, and approval routing |
| `templates/model-monitoring-kpi-register.md` | Define post-approval AI monitoring KPIs, thresholds, evidence sources, owners, and escalation rules |
| `templates/model-monitoring-kpi-register.csv` | Spreadsheet-friendly companion for model monitoring KPI tracking and review records |
| `controls/agentic-risk-control-mapping.md` | Map agentic AI failure modes to practical controls, evidence, release gates, monitoring signals, and owner roles |
| `controls/agentic-risk-control-mapping.csv` | Spreadsheet-friendly companion for agentic risk-to-control mapping |
| `controls/owasp-llm-2025-control-mapping.md` | Map OWASP LLM 2025 risks to toolkit controls, evidence expectations, release gates, monitoring signals, and owner roles |
| `controls/owasp-llm-2025-control-mapping.csv` | Spreadsheet-friendly companion for OWASP LLM 2025 governance mapping |
| `controls/nist-ai-rmf-control-crosswalk.md` | Map NIST AI RMF Govern, Map, Measure, and Manage functions to toolkit controls, evidence, cadence, and owner roles |
| `controls/nist-ai-rmf-control-crosswalk.csv` | Spreadsheet-friendly companion for NIST AI RMF evidence crosswalks |
| `policies/ai-log-retention-policy.md` | Define retention expectations for prompts, outputs, embeddings, tool calls, and security events |
| `playbooks/ai-data-leak-triage.md` | Triage suspected AI data exposure through prompts, outputs, logs, embeddings, or providers |
| `playbooks/agentic-tool-misuse-response.md` | Contain and investigate incorrect or unauthorized agent tool actions |
| `scripts/exception_aging_report.py` | Generate Markdown or JSON reports for expired, expiring, missing-expiration, and inconsistent AI exceptions |
| `scripts/risk_register_report.py` | Generate Markdown or JSON summaries of residual AI risk, owner queues, review dates, and theme-level exposure |
| `scripts/data_deletion_evidence_report.py` | Generate Markdown or JSON reports for AI data deletion evidence gaps and processor review queues |
| `scripts/third_party_dependency_report.py` | Generate Markdown or JSON reports for provider, subprocessor, assurance, exit-plan, and continuity gaps |
| `scripts/tabletop_evidence_report.py` | Generate Markdown or JSON reports for tabletop exercise evidence gaps, owner queues, and release-blocking readiness issues |
| `scripts/evaluation_evidence_report.py` | Generate Markdown or JSON reports for AI evaluation evidence readiness, stale evidence, missing coverage, release-blocking failures, and owner queues |
| `scripts/agentic_risk_control_report.py` | Generate Markdown or JSON summaries of agentic risk mappings, owner queues, control coverage, release gates, and monitoring signals |
| `scripts/access_recertification_report.py` | Generate Markdown or JSON reports for AI access recertification gaps, privileged access, service accounts, API tokens, break-glass access, and high-impact agent tool permissions |
| `scripts/incident_evidence_report.py` | Generate Markdown or JSON reports for AI incident evidence gaps, privacy review, containment proof, log preservation, timelines, communications, root cause, and remediation queues |
| `scripts/owasp_llm_mapping_report.py` | Generate Markdown or JSON summaries of OWASP LLM 2025 risk-to-control coverage, release gates, monitoring signals, and owner queues |
| `scripts/nist_ai_rmf_crosswalk_report.py` | Generate Markdown or JSON summaries of NIST AI RMF function coverage, control coverage, evidence cadence, and owner queues |
| `scripts/red_team_taxonomy_report.py` | Generate Markdown or JSON summaries of red-team finding severity, release holds, owner queues, and control coverage |
| `scripts/evidence_quality_report.py` | Generate Markdown or JSON reports for evidence ownership, freshness, overdue items, cadence gaps, and owner queues |
| `examples/ai-data-deletion-evidence-sample.csv` | Sample deletion evidence register covering overdue, verified, missing-evidence, and retention-exception states |
| `examples/ai-access-recertification-sample.csv` | Sample AI access recertification register covering privileged access, unowned tokens, separated identities, break-glass access, and current audit roles |
| `examples/ai-access-recertification-report.json` | Example machine-readable output from the access recertification report |
| `examples/ai-incident-evidence-sample.csv` | Sample AI incident evidence register covering privacy review gaps, missing tool logs, incomplete timelines, containment evidence gaps, overdue remediation, and closed incidents |
| `examples/ai-incident-evidence-report.json` | Example machine-readable output from the incident evidence report |
| `examples/ai-third-party-dependency-sample.csv` | Sample third-party AI dependency register covering missing DPA, subprocessor transparency, stale assurance, and continuity gaps |
| `examples/ai-tabletop-exercise-evidence-sample.csv` | Sample tabletop evidence register covering provider fallback, prompt injection, data exposure, and agent tool misuse scenarios |
| `examples/ai-evaluation-evidence-sample.csv` | Sample evaluation evidence register covering RAG, security, citation, human review, low pass-rate, and stale evidence cases |
| `examples/ai-exception-register-sample.csv` | Sample exception register for report testing and governance workshop demonstrations |
| `examples/agentic-risk-control-report.md` | Example Markdown report summarizing agentic risk owner queues, control coverage, release gates, and monitoring signals |
| `examples/agentic-risk-control-report.json` | Example machine-readable output from the agentic risk control mapping report |
| `examples/ai-red-team-taxonomy-report.json` | Example machine-readable output from the red-team finding taxonomy report |
| `examples/evidence-register-quality-sample.csv` | Sample evidence register with current, stale, expired, required, and owner-missing evidence states |
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
