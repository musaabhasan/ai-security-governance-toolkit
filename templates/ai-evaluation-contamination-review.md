# AI Evaluation Dataset Contamination Review

Use this template before relying on evaluation scores for model, prompt, RAG, agent, classifier, or vendor release decisions. The review checks whether evaluation items, expected answers, labels, rubrics, or gold sources may have leaked into training data, prompt examples, synthetic data, demos, documentation, vendor test packs, or previous release artifacts.

## 1. Review Context

| Field | Response |
| --- | --- |
| AI system or evaluation pack |  |
| Evaluation purpose | Release gate / regression / safety / red-team / benchmark / vendor comparison / research |
| Evaluation owner |  |
| Dataset owner |  |
| Model, prompt, RAG index, or agent version |  |
| Evaluation period |  |
| Sample size |  |
| Risk tier | Low / medium / high / prohibited |
| Review status | Planned / in progress / complete / blocked |

## 2. Dataset Inventory

| Dataset Component | Description | Source | Owner | Sensitivity |
| --- | --- | --- | --- | --- |
| Prompts or questions |  |  |  | Public / internal / confidential / regulated |
| Expected answers |  |  |  |  |
| Rubrics or scoring rules |  |  |  |  |
| Gold documents or citations |  |  |  |  |
| Negative or abstention cases |  |  |  |  |
| Adversarial or red-team cases |  |  |  |  |
| Synthetic examples |  |  |  |  |

## 3. Contamination Paths

| Path | Review Question | Status |
| --- | --- | --- |
| Prompt examples | Were evaluation items used as few-shot examples, system instructions, or demos? | Pass / gap |
| Training or tuning data | Were questions, answers, labels, or rubrics included in fine-tuning, preference, or feedback data? | Pass / gap |
| RAG index | Are expected answers or evaluation rubrics indexed as retrievable knowledge? | Pass / gap |
| Synthetic data | Were evaluation items reused to generate synthetic training or test examples? | Pass / gap |
| Documentation or screenshots | Were answers or rubrics published in docs, support articles, notebooks, or demos? | Pass / gap |
| Vendor access | Did a provider or vendor receive the evaluation pack before running the test? | Pass / gap |
| Human reviewer memory | Are reviewers scoring cases they authored, trained on, or previously adjudicated? | Pass / gap |
| Public benchmark overlap | Do cases substantially match public benchmark, homework, certification, or exam items? | Pass / gap |

## 4. Leakage Signal Checks

Escalate when:

- model output matches expected answers with unusual phrasing or order;
- explanations mention hidden rubric language;
- wrong options are repeated exactly from the evaluation key;
- answer quality is high on known evaluation items but weak on paraphrases;
- retrieved context includes answer keys, rubrics, or evaluator notes;
- vendor or model logs show access to evaluation examples before release testing;
- synthetic examples are near-duplicates of holdout items;
- public search finds evaluation cases or expected answers.

## 5. Holdout And Split Controls

| Control | Minimum Expectation | Evidence |
| --- | --- | --- |
| Protected holdout set | Release-critical items are separated from training, prompt examples, and demos |  |
| Versioned dataset | Dataset version, item IDs, source hashes, and change log are retained |  |
| Access restriction | Only authorized evaluators can view answer keys and rubrics |  |
| Paraphrase probe | At least some cases test concept transfer without exact wording |  |
| Near-duplicate scan | Similarity review checks training, RAG, synthetic, and test sets |  |
| Vendor boundary | Vendor receives only what is required for evaluation execution |  |
| Reviewer independence | Reviewers are not scoring cases where they have conflict or prior exposure |  |

## 6. Evidence Package

| Evidence Item | Required Detail |
| --- | --- |
| Dataset manifest | Item IDs, source, owner, sensitivity, version, hash |
| Access log | Who accessed prompts, answers, labels, rubrics, and gold sources |
| Training data exclusion | Evidence that evaluation items were excluded from tuning and feedback sets |
| RAG exclusion | Evidence that answer keys and rubrics are not indexed for retrieval |
| Similarity scan | Near-duplicate results across training, synthetic, prompt, and evaluation data |
| Vendor statement | What was shared with the provider or vendor and when |
| Evaluation run record | Model, prompt, index, tool versions, timestamps, and outputs |
| Contamination findings | Open issues, severity, owner, and remediation |

## 7. Decision Rules

| Finding | Required Action |
| --- | --- |
| Exact holdout leakage into prompts, training, or RAG | Block release and replace affected items |
| Rubric or answer key retrieved by the system | Block release and remove source from retrieval |
| Near-duplicate overlap with training or synthetic data | Remove or quarantine affected items and rerun evaluation |
| Reviewer conflict | Reassign scoring and document independence |
| Public benchmark overlap without disclosure | Label results as benchmark-like, not independent validation |
| Vendor saw evaluation pack before test | Treat score as assisted evaluation unless controls prove isolation |

## 8. Metrics

| Metric | Purpose |
| --- | --- |
| Exact duplicate rate | Detects direct leakage |
| Near-duplicate rate | Detects paraphrase or synthetic reuse |
| Holdout access count | Measures exposure risk |
| RAG answer-key retrieval count | Detects index contamination |
| Paraphrase performance gap | Shows memorization risk |
| Reviewer conflict count | Measures scoring independence |
| Replaced item count | Tracks remediation burden |

## 9. Findings And Actions

| Finding | Severity | Required Action | Owner | Due Date |
| --- | --- | --- | --- | --- |
|  | Low / medium / high / critical |  |  |  |
|  |  |  |  |  |

## 10. Evaluation Decision

| Decision Item | Response |
| --- | --- |
| Dataset integrity | Ready / ready with conditions / hold |
| Evaluation score usable for release | Yes / no / limited |
| Required remediation |  |
| Retest required | Yes / no |
| Evidence package location |  |
| Approver |  |

## 11. Closure Notes

Document known limitations, accepted overlap, public benchmark dependencies, excluded items, retest scope, and any results that must be described as assisted, benchmark-like, or exploratory rather than independent release evidence.
