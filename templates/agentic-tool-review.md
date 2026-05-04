# Agentic Tool Review

Use this template before allowing an AI agent or assistant to invoke tools, APIs, scripts, data stores, workflow actions, or external services.

## 1. Tool Summary

| Field | Response |
| --- | --- |
| Tool name | |
| Tool owner | |
| System or API | |
| Business purpose | |
| Environment | Development / Test / Production |

## 2. Capability

| Capability | Allowed? | Notes |
| --- | --- | --- |
| Read data | | |
| Write data | | |
| Delete data | | |
| Send messages | | |
| Trigger workflow | | |
| Change permissions | | |
| Execute code | | |
| Access external network | | |

## 3. Authority Boundary

- What exact actions can the agent perform?
- What actions are explicitly prohibited?
- What user, role, or service identity does the agent use?
- Can the agent escalate privileges directly or indirectly?
- Can the agent call another agent or workflow?

## 4. Approval Rules

| Action Type | Auto-Approve | Human Approval | Prohibited |
| --- | --- | --- | --- |
| Read public data | | | |
| Read internal data | | | |
| Read confidential data | | | |
| Update records | | | |
| Delete records | | | |
| Send external communication | | | |
| Change access rights | | | |

## 5. Logging and Evidence

- Are all tool calls logged?
- Are prompts and outputs logged safely?
- Are sensitive values redacted?
- Can logs support incident investigation?
- Are decisions linked to the exact payload and identity?

## 6. Decision

| Decision | Approved / Approved with Conditions / Rejected |
| --- | --- |
| Security owner | |
| Business owner | |
| Approval date | |
| Review date | |
| Conditions | |
