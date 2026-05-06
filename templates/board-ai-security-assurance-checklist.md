# Board AI Security Assurance Checklist

This checklist helps executives, audit committees, and senior technology leaders ask practical assurance questions before approving high-impact AI systems. It focuses on governance evidence, operational accountability, and security controls that can be reviewed without requiring the board to inspect source code or model internals.

## 1. Business Ownership

- Has an accountable business owner been assigned?
- Has an accountable technology owner been assigned?
- Has an accountable risk or security owner been assigned?
- Is the intended business outcome documented?
- Are the groups impacted by the AI system clearly identified?
- Is the system classified as low, moderate, or high impact?
- Are unacceptable uses explicitly documented?

## 2. Data Governance

- Are all input data sources documented?
- Are sensitive, regulated, personal, or student-related data elements identified?
- Is there a documented lawful or approved basis for processing?
- Are data minimization decisions recorded?
- Are retention periods defined for prompts, outputs, logs, embeddings, and derived records?
- Are third-party data transfers documented?
- Is there a deletion or exit plan for external providers?

## 3. Access And Identity Controls

- Are administrative roles separated from normal user roles?
- Is MFA required for privileged access?
- Are service accounts, API keys, and integration credentials inventoried?
- Are agent tools restricted to the minimum required permissions?
- Are high-impact actions gated by human approval?
- Are access reviews scheduled and evidenced?

## 4. Security Testing

- Has prompt injection testing been performed?
- Has indirect prompt injection testing been performed against files, emails, URLs, or retrieved content?
- Has sensitive-data leakage testing been performed?
- Has tool misuse testing been performed for agentic workflows?
- Has output integrity testing been performed for high-impact decisions?
- Are failed tests recorded with remediation owners and due dates?

## 5. Operational Monitoring

- Are prompts, outputs, tool calls, administrative actions, and exceptions logged where appropriate?
- Are logs protected from unauthorized access and tampering?
- Are alerts configured for abnormal tool use, high-risk prompts, policy denials, and unusual data volume?
- Can the organization reconstruct a material AI-assisted action after an incident?
- Are monitoring responsibilities assigned to a named team?

## 6. Vendor And Provider Assurance

- Has the provider completed a security and privacy review?
- Are model training, retention, and data-use commitments documented?
- Are geographic hosting and subprocessors reviewed where required?
- Are uptime, support, and incident notification commitments documented?
- Is there a tested fallback or manual process if the provider becomes unavailable?
- Is provider lock-in risk documented?

## 7. Human Oversight

- Are human approval thresholds documented?
- Are users told when AI materially influences a workflow?
- Are operators trained to challenge AI outputs rather than accept them by default?
- Are escalation paths available when outputs are unsafe, inaccurate, biased, or incomplete?
- Are exceptions and overrides recorded?

## 8. Incident Readiness

- Is there an AI-specific incident triage playbook?
- Are data leakage, prompt injection, model misuse, and agent tool misuse covered?
- Can the system be disabled or placed in read-only mode quickly?
- Are affected credentials and provider tokens rotatable?
- Are notification responsibilities defined?
- Are lessons learned translated into updated controls?

## 9. Approval Decision

| Decision area | Status | Evidence reference | Owner | Due date |
| --- | --- | --- | --- | --- |
| Business ownership | Not started / In progress / Complete |  |  |  |
| Data governance | Not started / In progress / Complete |  |  |  |
| Access control | Not started / In progress / Complete |  |  |  |
| Security testing | Not started / In progress / Complete |  |  |  |
| Monitoring | Not started / In progress / Complete |  |  |  |
| Vendor assurance | Not started / In progress / Complete |  |  |  |
| Human oversight | Not started / In progress / Complete |  |  |  |
| Incident readiness | Not started / In progress / Complete |  |  |  |

## Decision Notes

- Approved for production:
- Approved with conditions:
- Deferred pending remediation:
- Rejected:

## Minimum Evidence Pack

- AI system intake record
- Data flow record
- Risk register entries
- Access review
- Prompt injection test record
- Agent tool review, if agentic capabilities are enabled
- Vendor due diligence record, if an external provider is used
- Logging and retention decision
- Incident response owner and escalation path
