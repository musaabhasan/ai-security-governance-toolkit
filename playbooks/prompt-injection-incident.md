# Prompt Injection Incident Playbook

## Purpose

Guide initial response when an AI system may have followed malicious instructions, revealed sensitive data, misused a tool, or produced unsafe output due to prompt injection or context manipulation.

## Severity Triggers

| Severity | Trigger |
| --- | --- |
| Critical | Sensitive data exposed, privileged action performed, external communication sent, records changed |
| High | Tool misuse attempted, unauthorized data requested, policy bypass successful in test or production |
| Medium | Malicious prompt detected and blocked, no data or action impact |
| Low | User reports suspicious behavior with no confirmed security impact |

## Immediate Actions

1. Preserve logs, prompts, context, tool-call records, output, user identity, and timestamps.
2. Disable or restrict affected tool access if action misuse is possible.
3. Move the system to safe mode if sensitive data exposure is suspected.
4. Notify the system owner, security owner, privacy owner, and operational support team.
5. Identify whether the incident affects students, employees, customers, public services, or regulated data.

## Investigation Questions

- What input triggered the behavior?
- Was external or retrieved context involved?
- Did the system call any tool, API, plugin, database, script, or workflow?
- Did it read, write, delete, send, or approve anything?
- Did logs contain sensitive data?
- Was the output shown to a user, stored, sent externally, or used in a decision?
- Was the same attack repeated across users or sessions?

## Containment Options

- Disable affected prompt path
- Disable tool or plugin
- Reduce agent permissions
- Require human approval for all actions
- Remove contaminated context or documents
- Rotate exposed credentials
- Block repeated attack pattern
- Update detection and monitoring rules

## Recovery

- Validate patched prompts, policies, and tool boundaries.
- Run adversarial tests before re-enabling production access.
- Confirm evidence capture is complete.
- Record business impact and corrective actions.
- Update risk register and control evidence.

## Post-Incident Review

| Topic | Notes |
| --- | --- |
| Root cause | |
| Control failure | |
| Data impact | |
| Operational impact | |
| User impact | |
| Corrective actions | |
| Owner | |
| Due date | |
