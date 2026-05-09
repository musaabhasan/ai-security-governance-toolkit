# AI Governance Escalation Decision Tree

Use this decision tree when an AI use case, incident, evaluation result, provider change, prompt release, RAG change, or agent tool request may exceed routine product-team approval. It helps teams route issues to the correct governance owners before risk acceptance becomes informal.

## Escalation Inputs

| Input | Record |
| --- | --- |
| System or use case |  |
| Request or event type | New use case / prompt release / model change / provider change / incident / exception / tool access / RAG change |
| Request owner |  |
| Risk owner |  |
| Date raised |  |
| Evidence reference |  |

## Decision Tree

### 1. Data Protection

Escalate to privacy or data protection review when any answer is `yes`:

- Does the system process personal, student, applicant, employee, patient, or sensitive operational data?
- Are prompt logs, transcripts, behavioral traces, or learning analytics reused for evaluation, research, or training?
- Is there automated decisioning, profiling, ranking, recommendation, monitoring, or early-alert logic?
- Is data transferred to a third-party provider, subprocessor, or cross-border service?
- Is the privacy notice, consent language, or retention rule incomplete?

Required evidence: DPIA triage, data lineage record, data-flow record, retention decision, provider/subprocessor review.

### 2. Security

Escalate to security review when any answer is `yes`:

- Does the AI system call tools, APIs, scripts, databases, browser sessions, cloud resources, package registries, or CI/CD systems?
- Are credentials, service accounts, OAuth scopes, SSH agents, browser profiles, Docker sockets, Kubernetes tokens, or cloud CLI profiles involved?
- Did a red-team test, MCP audit, prompt-injection test, or dependency audit create a high-risk finding?
- Could the system send, publish, deploy, merge, delete, grant access, or trigger an external action?
- Is logging insufficient to reconstruct prompts, tool calls, approvals, and downstream actions?

Required evidence: agentic tool review, MCP/security scan, red-team finding record, access recertification, incident evidence if applicable.

### 3. Academic Integrity And Research

Escalate to academic or research governance when any answer is `yes`:

- Does the system support assessment, feedback, grading, authorship, research analysis, or student-facing advice?
- Are AI-generated outputs used in scholarly work, classroom assessment, or learner evaluation?
- Does the study make causal, effectiveness, equity, or subgroup claims?
- Are multilingual instruments, consent materials, prompt logs, or learner traces used as research evidence?
- Are participant consent, de-identification, or ethics approval conditions unclear?

Required evidence: ethics checklist, consent/readability review, prompt-log privacy review, causal-claim readiness, translation equivalence, outcome equity review.

### 4. Legal, Procurement, And Third Party

Escalate to legal/procurement review when any answer is `yes`:

- Is a new provider, embedded AI feature, hosted model, or agent platform being purchased or expanded?
- Are contract, DPA, intellectual property, copyright, data-use, or indemnity terms unclear?
- Are subprocessors undisclosed or assurance documents stale?
- Is there no provider exit plan or fallback service for a critical workflow?
- Does the provider change region, model, endpoint, embedding, or safety-filter behavior?

Required evidence: procurement score, vendor due diligence, dependency register, provider change approval, exit plan.

### 5. Executive Or Risk Committee

Escalate to executive or risk committee review when any answer is `yes`:

- Is residual risk high after controls are applied?
- Is a policy exception required for release?
- Could failure materially affect learners, customers, staff, public trust, financial reporting, legal obligations, or continuity?
- Does the use case require a new risk appetite decision?
- Are control owners unable to close release-blocking evidence gaps before launch?

Required evidence: risk register, exception register, board assurance checklist, control evidence pack, residual risk decision.

## Escalation Outcome

| Decision | Owner | Evidence reference | Due date | Status |
| --- | --- | --- | --- | --- |
| Routine approval |  |  |  |  |
| Escalate to privacy/data protection |  |  |  |  |
| Escalate to security |  |  |  |  |
| Escalate to academic/research governance |  |  |  |  |
| Escalate to legal/procurement |  |  |  |  |
| Escalate to executive/risk committee |  |  |  |  |

## Review Cadence

Re-run this decision tree whenever the system changes model, provider, endpoint, prompt, RAG source, data source, user group, tool permission, region, safety filter, or release gate.
