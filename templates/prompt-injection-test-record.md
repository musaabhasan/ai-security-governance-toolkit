# Prompt Injection Test Record

Use this record to document prompt injection and indirect prompt injection tests before production release.

## Test Scope

- System:
- Model or provider:
- Test owner:
- Test date:
- Data sources:
- Tools enabled:

## Test Cases

| Test Case | Attack Path | Expected Control | Result | Evidence |
| --- | --- | --- | --- | --- |
| Direct instruction override | User prompt | System prompt and policy enforcement |  |  |
| Retrieved content injection | RAG source | Source isolation and output filtering |  |  |
| Tool misuse request | Agent tool call | Approval gate and tool permission boundary |  |  |
| Data exfiltration attempt | Prompt or retrieved content | Secret filtering and refusal behavior |  |  |
| Role confusion attempt | User prompt | Role hierarchy enforcement |  |  |

## Findings

- Passed controls:
- Failed controls:
- Required remediation:
- Retest date:
