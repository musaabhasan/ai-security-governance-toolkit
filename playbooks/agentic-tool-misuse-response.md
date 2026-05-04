# Agentic Tool Misuse Response Playbook

Use this playbook when an AI agent calls a tool incorrectly, exceeds approved authority, or takes an unexpected action.

## Containment

1. Pause or disable the affected agent workflow.
2. Revoke or rotate exposed tokens if tool credentials may be affected.
3. Preserve tool-call logs, prompts, outputs, approvals, and user session context.
4. Identify downstream systems changed by the tool call.
5. Restore affected records from trusted sources where needed.

## Investigation

| Area | Question | Notes |
| --- | --- | --- |
| Authorization | Did the tool permission match the approved use case? |  |
| Approval | Was a human approval required and recorded? |  |
| Prompt path | Did user input, retrieved content, or system context drive the action? |  |
| Guardrails | Did policy enforcement fail or operate as designed? |  |
| Impact | Were data, access, records, or external communications affected? |  |

## Recovery

- Corrective controls:
- Retest owner:
- Monitoring changes:
- Approval matrix update:
- Closure date:
