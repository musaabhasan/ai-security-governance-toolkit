# Agentic Risk Control Mapping Report

Mapped risk themes: `10`

## Owner Queue

| Owner Role | Risk Themes |
| --- | ---: |
| AI platform owner | 2 |
| Identity owner | 1 |
| Internal audit owner | 1 |
| Model risk owner | 1 |
| Operations owner | 1 |
| Privacy owner | 1 |
| Security owner | 2 |
| Third-party risk owner | 1 |

## Control Coverage

| Control ID | Mapped Risk Themes |
| --- | ---: |
| `AI-AGT-001` | 3 |
| `AI-AGT-002` | 3 |
| `AI-BCM-001` | 2 |
| `AI-DATA-001` | 1 |
| `AI-DATA-002` | 1 |
| `AI-GOV-001` | 3 |
| `AI-GOV-002` | 2 |
| `AI-ID-001` | 2 |
| `AI-OPS-001` | 4 |
| `AI-SEC-001` | 4 |
| `AI-VND-001` | 2 |

## Mapping Detail

| Risk ID | Theme | Failure Mode | Controls | Release Gate | Monitoring Signal | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| AR-001 | Instruction and goal manipulation | User or retrieved content changes the agent goal or overrides higher-priority instructions | `AI-SEC-001`, `AI-AGT-001` | Block release when high-severity instruction override succeeds | Repeated denied instruction-override attempts | Security owner |
| AR-002 | Tool misuse and unsafe action | Agent invokes an approved tool for an unapproved purpose or with unsafe parameters | `AI-AGT-001`, `AI-AGT-002`, `AI-OPS-001` | Block release when unsafe tool action executes without approval | High-risk tool call without matching approval ID | AI platform owner |
| AR-003 | Privilege and delegation abuse | Agent uses broad service credentials or acts beyond the user or task authority | `AI-ID-001`, `AI-AGT-002` | Block release when tool access is not bound to identity and task scope | Tool call using unexpected credential context | Identity owner |
| AR-004 | Sensitive data disclosure | Agent exposes regulated or confidential data through responses, tools, logs, memory, or provider calls | `AI-DATA-001`, `AI-DATA-002`, `AI-VND-001` | Block release when regulated data leaves an approved boundary | Unexpected sensitive-data pattern in output or logs | Privacy owner |
| AR-005 | Memory and state poisoning | Untrusted content is promoted into agent memory or long-term state and later influences decisions | `AI-SEC-001`, `AI-OPS-001`, `AI-GOV-001` | Block release when unreviewed memory changes can affect high-impact actions | Memory write from untrusted source or expired state | AI platform owner |
| AR-006 | Agent supply-chain exposure | Plugins, skills, tools, prompts, models, or dependencies change agent behavior without review | `AI-VND-001`, `AI-GOV-002`, `AI-SEC-001` | Block release when unreviewed external component can execute or influence tools | New tool or dependency with no approval record | Third-party risk owner |
| AR-007 | Inter-agent communication failure | One agent transfers authority, context, or instructions to another without preserving trust boundaries | `AI-GOV-001`, `AI-ID-001`, `AI-AGT-001` | Block release when receiving agent trusts unsigned or unscoped handoff context | Agent-to-agent handoff missing source identity | Security owner |
| AR-008 | Resource and cost exhaustion | Agent loops, retries, expands context, or consumes excessive API, compute, workflow, or storage resources | `AI-OPS-001`, `AI-BCM-001` | Block release when spend or concurrency limits are missing for agentic workflows | Token spend spike or repeated failed action chain | Operations owner |
| AR-009 | Audit and non-repudiation gap | Teams cannot reconstruct what the agent knew, decided, approved, and executed | `AI-GOV-001`, `AI-OPS-001`, `AI-AGT-002` | Block release when high-impact actions lack reconstructable evidence | Missing correlation ID across prompt, policy, and tool logs | Internal audit owner |
| AR-010 | Model or provider behavior drift | Model, safety filter, provider, prompt, retrieval index, or routing change alters risk posture | `AI-GOV-002`, `AI-BCM-001`, `AI-SEC-001` | Block release when evaluation evidence is stale or release-blocking failures remain | New model/provider version without matching approval | Model risk owner |
