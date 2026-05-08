# AI Incident Severity Matrix

Use this matrix to classify AI-related incidents consistently before escalation,
communications, containment, and post-incident review. It is intended to extend
an existing security incident process with AI-specific impact dimensions.

## 1. Incident Snapshot

| Field | Entry |
| --- | --- |
| Incident ID |  |
| Date and time detected |  |
| Reporter |  |
| Affected AI system |  |
| Business owner |  |
| Technical owner |  |
| Security lead |  |
| Current severity |  |
| Current status | New / Triage / Containment / Recovery / Review |

## 2. AI-Specific Impact Dimensions

Score each dimension from 0 to 3.

| Dimension | 0 | 1 | 2 | 3 | Score |
| --- | --- | --- | --- | --- | --- |
| Data exposure | No sensitive data involved | Internal data only | Personal, student, customer, or regulated data suspected | Confirmed sensitive data exposure or exfiltration |  |
| Tool or action misuse | No tool action | Low-impact action attempted | Unauthorized action completed but reversible | High-impact action affecting records, access, finance, safety, or availability |  |
| Output harm | No harmful output | Minor inaccurate or low-risk output | Material misinformation, bias, or unsafe guidance in limited context | High-impact decision support, public harm, or repeated unsafe output |  |
| Prompt or context compromise | No prompt/context compromise | Attempted prompt injection blocked | Prompt injection changed behavior in limited scope | System instructions, retrieved context, or hidden data exposed |  |
| Identity and access impact | No identity impact | Single low-privilege account affected | Privileged or service identity affected | Shared credential, admin identity, or cross-system access affected |  |
| Business continuity | No disruption | Manual workaround available | Service degraded or workflow delayed | Critical process unavailable or fallback failed |  |
| Legal, regulatory, or contractual exposure | None expected | Internal policy issue | Reportable or contract-relevant concern possible | Reportable event, contractual breach, or regulator/customer notification likely |  |
| Public trust and reputational impact | Not externally visible | Limited user concern | Visible to a defined stakeholder group | Public, media, partner, or executive-level impact |  |

## 3. Severity Decision

| Severity | Typical score range | Required response |
| --- | --- | --- |
| SEV-4 Low | 1-4 | Track, correct, and review during normal operations. |
| SEV-3 Moderate | 5-8 | Assign incident owner, preserve evidence, and complete containment plan. |
| SEV-2 High | 9-14 | Activate security incident response, executive notification, and legal/privacy review. |
| SEV-1 Critical | 15+ or any automatic escalation trigger | Activate crisis response, suspend affected AI capability where needed, and begin formal communications process. |

## 4. Automatic Escalation Triggers

Escalate directly to SEV-1 or SEV-2 when any of the following are true:

- confirmed exposure of regulated, personal, student, patient, financial, or credential data,
- AI agent completed an unauthorized high-impact action,
- model or tool output created plausible safety, legal, or financial harm,
- hidden prompts, retrieved documents, or protected system context were disclosed,
- privileged service identity or shared credential was exposed,
- incident affects a public-facing or executive-critical service,
- the same failure repeats after containment,
- contractual, regulatory, or customer notification may be required.

## 5. Evidence to Preserve

| Evidence | Location or owner | Preserved |
| --- | --- | --- |
| Prompt, input, or task request |  |  |
| Model output or generated artifact |  |  |
| Retrieved context, document IDs, or embeddings reference |  |  |
| Tool call log and parameters |  |  |
| Approval workflow record |  |  |
| Identity and access logs |  |  |
| Network or provider logs |  |  |
| Data classification record |  |  |
| Screenshot, ticket, or user report |  |  |
| Containment action log |  |  |

## 6. Initial Response Actions

- Assign an incident owner and decision authority.
- Preserve evidence before modifying prompts, policies, tools, or logs.
- Identify affected users, data classes, tools, vendors, and downstream systems.
- Disable or restrict the affected AI capability when continued operation may expand harm.
- Review whether a human approval gate failed or was bypassed.
- Check for related incidents across similar prompts, tools, data sources, or agent workflows.
- Record the severity rationale and update it as facts change.

## 7. Post-Incident Review Questions

- Which AI control failed: governance, data, identity, tool policy, model behavior, monitoring, vendor control, or human approval?
- Was the incident caused by model output, retrieved context, tool execution, user instruction, vendor behavior, or system integration?
- Did monitoring detect the issue quickly enough?
- Were logs sufficient without exposing unnecessary sensitive data?
- Did the incident reveal missing policy-as-code, testing, red-team, or tabletop coverage?
- Which control owner must provide remediation evidence?
- Should the AI system intake, risk register, model card, or approval matrix be updated?
