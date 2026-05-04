# Example: EdTech AI Assistant Governance Profile

## Use Case

An AI assistant helps staff and learners find approved learning resources, answer common LMS questions, and summarize public course guidance.

## Approved Scope

- Search public and internal course catalog content.
- Answer frequently asked LMS support questions.
- Summarize approved policy pages.
- Suggest where to find official support.

## Prohibited Scope

- Make grading decisions.
- Change student records.
- Reveal personal student data.
- Send messages on behalf of staff.
- Provide disciplinary, legal, medical, or immigration advice.
- Override academic policy.

## Data Rules

| Data Type | Use |
| --- | --- |
| Public course descriptions | Allowed |
| Internal LMS help articles | Allowed with access control |
| Student submissions | Not allowed |
| Grades and assessment records | Not allowed |
| Personal student data | Not allowed unless formally approved |
| Support tickets | Restricted, case-by-case review |

## Control Selection

| Control | Why It Applies |
| --- | --- |
| `AI-GOV-001` | The assistant needs named ownership and service accountability |
| `AI-GOV-002` | The use case needs approval before release |
| `AI-DATA-001` | Prompts and retrieval context must be classified |
| `AI-DATA-002` | Logs may capture student questions or staff prompts |
| `AI-AGT-001` | The assistant must only use approved lookup tools |
| `AI-SEC-001` | Prompt injection testing is required before rollout |
| `AI-BCM-001` | Learner support needs fallback during service outage |

## Evidence Pack

- Approved intake form
- Data classification worksheet
- Tool allowlist
- Prompt injection test results
- Logging and retention review
- User-facing limitation notice
- Service fallback procedure
