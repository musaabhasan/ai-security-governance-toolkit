# AI Data Leak Triage Playbook

Use this playbook when sensitive information may have been exposed through an AI prompt, output, log, embedding store, plugin, or provider workflow.

## First Hour

1. Record the reporter, system, time, and suspected data class.
2. Preserve relevant prompts, outputs, logs, tool calls, and provider events.
3. Disable affected integrations or logging paths if continued exposure is likely.
4. Identify whether data left organizational control.
5. Notify the incident lead, system owner, and privacy or compliance contact.

## Triage Questions

| Question | Answer | Evidence |
| --- | --- | --- |
| What data class was involved? |  |  |
| Was the data sent to an external provider? |  |  |
| Was the data stored in prompts, logs, embeddings, or tickets? |  |  |
| Was the data used for training or retained by a vendor? |  |  |
| Are deletion or containment actions available? |  |  |

## Closure

- Root cause:
- Controls changed:
- Notifications completed:
- Evidence location:
- Lessons learned owner:
