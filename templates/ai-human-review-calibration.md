# AI Human Review Calibration

Use this template to test whether human review for an AI-supported workflow is meaningful, consistent, independent, and auditable. It is designed for high-impact use cases such as education, employment, eligibility, finance, safety, security, discipline, case triage, admissions, and access decisions.

## 1. Review Context

| Field | Response |
| --- | --- |
| AI system or workflow |  |
| Decision or action being reviewed |  |
| Review owner |  |
| Business owner |  |
| Model, prompt, index, or ruleset version |  |
| Review population |  |
| Sample period |  |
| Sample size |  |
| Risk tier | Low / medium / high / prohibited |
| Review status | Planned / in progress / complete / blocked |

## 2. Human Review Purpose

| Question | Response | Evidence |
| --- | --- | --- |
| What can the reviewer approve, reject, change, or escalate? |  |  |
| Is the reviewer independent enough to challenge the AI output? | Yes / no / partial |  |
| Does the reviewer see the original evidence, not only the model answer? | Yes / no / partial |  |
| Can the reviewer request more information before deciding? | Yes / no / partial |  |
| Can the reviewer override the AI recommendation without penalty? | Yes / no / partial |  |
| Are reviewers trained on known model limitations and bias risks? | Yes / no / partial |  |

## 3. Calibration Sample

| Sample ID | AI Recommendation | Human Decision | Outcome Match | Override Reason | Evidence Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- |
|  | Approve / reject / escalate / classify / other |  | Match / partial / mismatch |  | Strong / adequate / weak / missing |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

Select samples across normal, borderline, high-risk, appealed, and previously misclassified cases. Do not rely only on successful or low-risk examples.

## 4. Consistency Checks

| Check | Expected Evidence | Status |
| --- | --- | --- |
| Two reviewers reach similar decisions on the same borderline case | Blind duplicate review sample | Pass / gap |
| Reviewers cite policy or source evidence, not only AI confidence | Decision rationale record | Pass / gap |
| Override decisions are explained | Override log with reason codes | Pass / gap |
| High-risk cases receive escalation or second review | Escalation queue record | Pass / gap |
| Reviewer decisions are sampled across departments or user groups | Sampling frame | Pass / gap |
| Reversal or appeal outcomes are fed back into reviewer guidance | Procedure update or learning log | Pass / gap |

## 5. Automation Bias Indicators

Escalate when any of the following are present:

- reviewers accept most AI recommendations without recorded rationale;
- reviewers rarely override high-confidence model outputs even when evidence conflicts;
- reviewer notes repeat model wording without independent analysis;
- review time is too short for the complexity of the decision;
- reviewers cannot see source evidence, policy criteria, or contradictory context;
- override rates differ materially by reviewer, department, or affected group;
- appeal reversals identify recurring reviewer blind spots.

## 6. Bias And Fairness Review

| Dimension | Review Question | Evidence |
| --- | --- | --- |
| Case mix | Does the sample include relevant groups, case types, and risk tiers? |  |
| Reviewer assignment | Are cases assigned without creating avoidable conflict or bias? |  |
| Outcome variance | Do approval, denial, escalation, or override rates differ unexpectedly? |  |
| Appeal signal | Do appealed or reversed cases reveal recurring decision patterns? |  |
| Accessibility | Can affected people submit context or corrections in accessible formats? |  |
| Language | Are notices, evidence summaries, and review communications understandable? |  |

Where lawful and appropriate, compare outcomes across relevant groups. If group-level analysis is not permitted, use proxy-safe qualitative review and monitor appeal themes.

## 7. Reviewer Workload And Capability

| Control | Minimum Expectation | Status |
| --- | --- | --- |
| Reviewer training | Role-specific training covers workflow, evidence, limitations, escalation, and documentation | Pass / gap |
| Time budget | Reviewer has enough time for meaningful assessment | Pass / gap |
| Evidence access | Reviewer can access source data, policy criteria, and model metadata needed for review | Pass / gap |
| Escalation support | Reviewer can consult privacy, security, legal, academic, HR, or operational experts | Pass / gap |
| Rotation or peer review | Critical cases receive second review or periodic peer calibration | Pass / gap |
| Conflict handling | Reviewers disclose conflicts or lack of independence | Pass / gap |

## 8. Metrics

| Metric | Purpose |
| --- | --- |
| AI-human agreement rate | Detects overreliance or unstable model behavior |
| Override rate by reviewer and decision type | Identifies reviewer drift or automation bias |
| Escalation rate | Shows whether difficult cases are routed appropriately |
| Average review time | Detects rubber-stamping or workload pressure |
| Appeal reversal rate | Reveals review quality and procedural fairness issues |
| Missing evidence rate | Measures whether reviewers can reconstruct decisions |
| Calibration disagreement rate | Measures consistency between reviewers |

## 9. Findings And Actions

| Finding | Severity | Required Action | Owner | Due Date |
| --- | --- | --- | --- | --- |
|  | Low / medium / high / critical |  |  |  |
|  |  |  |  |  |

## 10. Decision

| Decision Item | Response |
| --- | --- |
| Human review readiness | Ready / ready with conditions / hold |
| Required calibration frequency | Monthly / quarterly / after major change / other |
| Residual risk owner |  |
| Evidence package location |  |
| Approver |  |

## 11. Closure Notes

Document accepted limitations, sampling gaps, unresolved fairness questions, training updates, escalation changes, and any AI-supported decision types that must remain advisory until human review quality improves.
