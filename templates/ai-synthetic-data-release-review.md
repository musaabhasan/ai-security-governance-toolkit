# AI Synthetic Data Release Review

Use this template before creating, sharing, publishing, or reusing synthetic data for AI development, model evaluation, analytics, education, research, vendor testing, or public demonstration. Synthetic data should be treated as a controlled derivative dataset until privacy, utility, lineage, and release controls are proven.

## 1. Release Context

| Field | Response |
| --- | --- |
| Release ID |  |
| Dataset name |  |
| Business or research owner |  |
| Technical owner |  |
| Data protection or privacy reviewer |  |
| Intended use | Training / evaluation / demo / research / vendor testing / education / analytics |
| Release audience | Internal / limited partner / vendor / public / open dataset |
| Source data classification | Public / internal / confidential / regulated / student / health / HR / financial |
| Synthetic generation method | Rules / statistical / simulation / generative model / hybrid |
| Release decision requested | Approve / approve with conditions / hold / reject |

## 2. Source Data Lineage

| Source Asset | Owner | Classification | Legal Basis or Consent | Retention Rule | Sensitive Attributes | Notes |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Lineage requirements:

- Document every source dataset used to generate or validate the synthetic output.
- Record whether any source includes minors, students, patients, employees, protected attributes, credentials, security events, or rare populations.
- Confirm whether the source data can legally support synthetic derivation for the intended audience.
- Link to deletion, retention, and consent constraints that must flow into the synthetic dataset.

## 3. Generation Controls

| Control Question | Evidence | Status |
| --- | --- | --- |
| Are direct identifiers removed before generation where possible? |  | Pass / gap |
| Are quasi-identifiers generalized, bucketed, suppressed, or controlled? |  | Pass / gap |
| Are rare records, outliers, and small groups protected from reproduction? |  | Pass / gap |
| Are training prompts, seeds, model versions, and generation scripts versioned? |  | Pass / gap |
| Are source records prevented from being copied verbatim into synthetic output? |  | Pass / gap |
| Are sensitive labels balanced without creating misleading distributions? |  | Pass / gap |
| Is generated data clearly marked as synthetic in metadata and documentation? |  | Pass / gap |

## 4. Privacy and Re-Identification Tests

| Test | Minimum Expectation | Evidence |
| --- | --- | --- |
| Exact match scan | No synthetic row or text block materially reproduces a source record |  |
| Near-neighbor review | Synthetic records are not unusually close to rare source records |  |
| Membership inference check | Release does not reveal whether a specific person or record was in the source data |  |
| Attribute inference review | Sensitive attributes cannot be inferred beyond approved risk tolerance |  |
| Small group protection | Rare groups, uncommon cases, and outliers are suppressed or generalized |  |
| Free-text leakage scan | Names, emails, IDs, phone numbers, locations, secrets, or case-specific facts are not reproduced |  |
| Linkage risk review | Public or partner datasets cannot reasonably relink synthetic rows to people or cases |  |

Escalate when:

- any direct identifier appears in synthetic output;
- a generated record closely matches a rare source record;
- security events, medical narratives, student records, or HR cases remain linkable;
- the release is public or vendor-facing and privacy tests are incomplete.

## 5. Utility and Representativeness

| Utility Check | Evidence | Decision Impact |
| --- | --- | --- |
| Target task performance is measured against a non-sensitive validation baseline |  |  |
| Key distributions are close enough for intended use but not copied record-by-record |  |  |
| Bias, fairness, or subgroup behavior is reviewed where relevant |  |  |
| Known limitations are documented for downstream users |  |  |
| Synthetic data is not used to justify decisions beyond its validated purpose |  |  |
| Evaluation labels remain meaningful after synthesis |  |  |

Synthetic data can be privacy-preserving and still unsuitable if it distorts the decision boundary, hides minority failure modes, or creates unrealistic security, education, or operational patterns.

## 6. Release Boundary

| Release Control | Required Decision |
| --- | --- |
| Allowed audience |  |
| Allowed use cases |  |
| Prohibited use cases |  |
| Redistribution allowed | Yes / no / with approval |
| External publication allowed | Yes / no |
| Vendor or partner access allowed | Yes / no / contract required |
| Retention period |  |
| Deletion or recall process |  |
| Required attribution or notice |  |
| Required license or data-use agreement |  |

## 7. Documentation Requirements

Release documentation should include:

- synthetic data purpose,
- generation method summary,
- source lineage summary,
- data dictionary,
- privacy tests performed,
- utility tests performed,
- limitations and prohibited use,
- known bias or coverage gaps,
- refresh cadence,
- contact owner,
- deletion and issue-reporting path.

Do not disclose sensitive source details that would make re-identification easier.

## 8. Release Decision

| Decision Item | Response |
| --- | --- |
| Privacy risk rating | Low / medium / high |
| Utility confidence | Low / medium / high |
| Residual risk owner |  |
| Required conditions |  |
| Approved audience |  |
| Review expiry date |  |
| Evidence package location |  |
| Final decision | Approve / approve with conditions / hold / reject |
| Approver |  |

## 9. Post-Release Monitoring

| Monitoring Signal | Owner | Trigger |
| --- | --- | --- |
| Re-identification concern or user report |  |  |
| Downstream misuse outside approved purpose |  |  |
| New source data deletion request affects synthetic derivative |  |  |
| Bias or utility issue discovered after release |  |  |
| Public linkage dataset becomes available |  |  |
| Vendor or partner access expands |  |  |

If a release is recalled, preserve the release package, issue notice, deletion evidence, downstream recipient list, and closure decision.
