# AI Service Outage Tabletop Exercise

## Scenario

An AI service used by an education or business process becomes unavailable during a peak operational period. The issue affects staff productivity, student support, assessment preparation, or internal decision support.

## Objectives

- Validate dependency awareness.
- Confirm fallback procedures.
- Test communication paths.
- Identify manual workarounds.
- Confirm recovery and backlog handling.

## Participants

- Business owner
- IT operations lead
- Information security lead
- Business continuity lead
- EdTech or platform owner
- Communications representative
- Vendor manager if applicable

## Injects

| Time | Inject | Expected Discussion |
| --- | --- | --- |
| T+0 | AI API returns intermittent errors | Detection, escalation, user messaging |
| T+30 | Vendor status page confirms regional issue | Dependency tracking, SLA, workaround |
| T+60 | Staff begin using unapproved public AI tools | Shadow AI control and communications |
| T+90 | Critical deadline approaches | Manual process, prioritization, risk acceptance |
| T+120 | Service restored with delayed responses | Recovery, backlog, monitoring |

## Key Questions

- What services depend on the AI provider?
- Which workflows can continue manually?
- Who approves temporary workarounds?
- How are users told what not to do?
- What data must not be pasted into public alternatives?
- What evidence is needed after the exercise?

## Outputs

- Action list
- Updated business impact analysis
- Updated dependency register
- Updated user communication template
- Updated risk register
- Control evidence for `AI-BCM-001`
