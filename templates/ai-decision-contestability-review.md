# AI Decision Contestability Review

Use this template before approving or auditing an AI system that influences decisions about students, employees, applicants, customers, benefits, access, discipline, safety, finance, compliance, or other high-impact outcomes. The review checks whether affected people can understand, question, appeal, and correct AI-supported decisions through an accountable human process.

## 1. Decision Context

| Field | Response |
| --- | --- |
| AI system or workflow |  |
| Decision domain | Education / employment / finance / access / discipline / health / safety / compliance / other |
| Affected population |  |
| Business owner |  |
| Human decision owner |  |
| AI system owner |  |
| Review date |  |
| Risk tier | Low / medium / high / prohibited |
| Decision status | Advisory / triage / recommendation / automated decision / human-approved decision |

## 2. Decision Role of AI

| Question | Response | Evidence |
| --- | --- | --- |
| What input data does the AI system use? |  |  |
| What output does the AI system produce? |  |  |
| Does the output directly determine the outcome? | Yes / no / partial |  |
| Can a human override the output? | Yes / no / conditional |  |
| Is the human reviewer trained and accountable? | Yes / no / partial |  |
| Are affected people told that AI is involved? | Yes / no / partial |  |
| Does the system preserve evidence needed to reconstruct the decision? | Yes / no / partial |  |

## 3. Contestability Requirements

| Requirement | Minimum Expectation | Status |
| --- | --- | --- |
| Notice | Affected person receives understandable notice of the decision and how AI was used | Pass / gap |
| Reason | Decision reason is stated without exposing protected system details or third-party data | Pass / gap |
| Evidence access | Person can request relevant evidence, data, or policy basis used in the decision | Pass / gap |
| Correction path | Person can correct inaccurate input data or missing context | Pass / gap |
| Human review | A qualified human can review the decision independently of the original model output | Pass / gap |
| Appeal route | Appeal channel, deadline, owner, and expected response time are clear | Pass / gap |
| Non-retaliation | Appeal or correction request does not create adverse treatment | Pass / gap |
| Remediation | Incorrect decisions can be reversed, corrected, compensated, or recorded as error | Pass / gap |

## 4. Evidence Package

| Evidence Item | Required Detail | Location |
| --- | --- | --- |
| Decision record | Decision ID, date, owner, outcome, affected person reference |  |
| Model or prompt version | Model, provider, prompt, RAG index, tool version, or ruleset |  |
| Input data summary | Data categories, source systems, freshness, known limitations |  |
| Output summary | Score, recommendation, classification, cited context, confidence, or rationale |  |
| Human review record | Reviewer, date, decision, override, justification |  |
| Notice text | Message shown to affected person |  |
| Appeal record | Request, reviewer, outcome, timing, remediation |  |
| Audit trail | Logs, evidence hashes, access records, deletion or retention policy |  |

Do not expose raw prompts, protected system instructions, unrelated third-party data, or confidential security controls in appeal communications. Provide enough information for meaningful challenge without creating new privacy or security risks.

## 5. High-Risk Decision Checks

Escalate to legal, privacy, academic, HR, compliance, or executive governance when:

- the AI output materially affects admission, grades, scholarships, employment, discipline, access, finance, benefits, health, safety, or legal rights;
- the affected person cannot identify how to appeal or correct data;
- the system uses sensitive attributes or proxies;
- the human reviewer only rubber-stamps AI output;
- the model cannot provide evidence that can be reviewed by a human;
- appeal outcomes cannot be traced back to the source decision record;
- the system cannot suspend or reverse incorrect decisions.

## 6. Human Review Quality

| Review Quality Check | Evidence | Status |
| --- | --- | --- |
| Reviewer is independent enough to challenge the AI output |  | Pass / gap |
| Reviewer receives policy, evidence, and context beyond the model answer |  | Pass / gap |
| Reviewer can request additional information from the affected person |  | Pass / gap |
| Reviewer records rationale when upholding, changing, or reversing the decision |  | Pass / gap |
| Reviewer decisions are sampled for consistency and bias |  | Pass / gap |
| Reviewer workload allows meaningful assessment |  | Pass / gap |

## 7. Notice and Appeal Design

| Notice Element | Required Content |
| --- | --- |
| Decision outcome | Clear statement of what happened |
| AI involvement | Plain-language description of the AI role |
| Evidence basis | Data categories or policy sources used |
| Human contact | Responsible office or reviewer channel |
| Correction route | How to correct inaccurate data |
| Appeal route | Deadline, submission method, expected timeline |
| Support needs | Accessibility, language, and accommodation options |

## 8. Metrics and Monitoring

| Metric | Purpose |
| --- | --- |
| Appeal volume by decision type | Detects friction or unclear notice |
| Appeal success or reversal rate | Identifies model, data, or process quality issues |
| Average appeal response time | Measures procedural fairness |
| Data correction frequency | Reveals source data quality problems |
| Human override rate | Detects automation bias or model drift |
| Appeal outcomes by subgroup where lawful and appropriate | Detects potential disparate impact |
| Missing evidence rate | Measures audit readiness |

## 9. Decision

| Decision Item | Response |
| --- | --- |
| Contestability readiness | Ready / ready with conditions / hold |
| Required remediation |  |
| Residual risk owner |  |
| Review cadence |  |
| Evidence package location |  |
| Approver |  |

## 10. Closure Notes

Document limitations, accepted risks, unresolved legal or policy questions, communication constraints, and any decision types that must remain advisory until contestability controls mature.
