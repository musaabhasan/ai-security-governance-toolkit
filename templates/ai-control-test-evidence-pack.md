# AI Control Test Evidence Pack

Use this pack to turn a control test into an audit-ready evidence record. It is
designed for AI assistants, RAG systems, agentic workflows, embedded AI features,
and hosted model services where reviewers need to know not only whether a
control exists, but whether it operated effectively during the review period.

## 1. Test Identification

| Field | Entry |
| --- | --- |
| Evidence pack ID |  |
| AI system or service |  |
| Business owner |  |
| Technical owner |  |
| Control ID |  |
| Control name |  |
| Test owner |  |
| Review period |  |
| Test date |  |
| Result | Pass / Pass with observation / Needs remediation / Fail |

## 2. Control Objective

State the control objective in one or two sentences.

Example: "Only approved agent tools may be invoked in production, and high-impact
tool calls require a recorded human approval before execution."

## 3. Test Procedure

| Step | Procedure | Evidence expected |
| --- | --- | --- |
| 1 | Identify the approved control requirement and owner. | Control catalog reference or policy excerpt |
| 2 | Select the tested population and sample. | Population export, sample rationale, date range |
| 3 | Execute the test method. | Query output, screenshots, logs, config export, or ticket evidence |
| 4 | Compare observed behavior with the expected control state. | Pass/fail notes and exceptions |
| 5 | Record remediation or management response. | Issue link, owner, due date, compensating control |

## 4. Evidence Inventory

| Evidence item | Source | Hash or stable reference | Retention location | Reviewer note |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 5. Population And Sampling

| Field | Entry |
| --- | --- |
| Population definition |  |
| Population size |  |
| Sample size |  |
| Sampling method | Full population / risk-based / random / judgmental |
| Exclusions |  |
| Sampling rationale |  |

## 6. Result Assessment

| Finding type | Criteria |
| --- | --- |
| Pass | Evidence demonstrates the control operated as designed for the reviewed population. |
| Pass with observation | Control operated, but evidence quality, timeliness, or automation should improve. |
| Needs remediation | Control partially operated or had exceptions requiring tracked remediation. |
| Fail | Control did not operate, could not be evidenced, or exceptions exceeded tolerance. |

## 7. Exceptions And Remediation

| Exception | Impact | Owner | Due date | Remediation action | Status |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 8. Reviewer Conclusion

Summarize whether the control is designed effectively, operating effectively, and
supported by sufficient evidence. State any limitation on the conclusion, such
as incomplete logs, missing approval receipts, inconsistent timestamps, or a
sample that does not cover the full review period.

## 9. Minimum Evidence Quality Checks

- Evidence has an owner and collection timestamp.
- Evidence source is independent enough for the tested control.
- Screenshots are supported by system exports where possible.
- Log extracts include query conditions or report parameters.
- Sensitive prompts, outputs, personal data, and secrets are redacted.
- Hashes or stable references are recorded for exported files.
- Remediation items have owners and due dates.
- The result is reflected in the control test schedule.

