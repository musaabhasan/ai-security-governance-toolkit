# AI Retrieval Integrity Review

Use this template before approving, materially changing, or auditing an AI system that uses retrieval-augmented generation, semantic search, vector stores, knowledge bases, document grounding, or long-term memory. The review is designed to test whether retrieved context is authoritative, timely, bounded, traceable, and safe to use in generated answers.

## 1. Review Context

| Field | Response |
| --- | --- |
| System or assistant name |  |
| Business owner |  |
| Technical owner |  |
| Review date |  |
| Review trigger | New release / major corpus update / embedding model change / retriever change / incident / audit / periodic review |
| Related risk tier |  |
| Related controls | AI-DATA-001, AI-DATA-002, AI-SEC-001, AI-OPS-001 |
| Decision requested | Approve / approve with conditions / hold release / retire retrieval source |

## 2. Retrieval Architecture

| Area | Required Detail |
| --- | --- |
| Retriever type | Vector search / hybrid search / keyword search / graph retrieval / memory retrieval / tool-based lookup |
| Embedding or indexing model | Provider, version, deployment region, and change-control reference |
| Generation model | Provider, version, safety settings, and fallback behavior |
| Retrieval stores | Vector database, search index, database table, file store, or external source |
| Retrieval filters | Tenant, role, department, language, classification, jurisdiction, time window, and source-status filters |
| Reranking logic | Similarity, source authority, freshness, fact-key grouping, policy rules, or human curation |
| Citation policy | Required sources, citation format, confidence statements, and unsupported-answer behavior |

## 3. Source Authority Register

| Source ID | Source Name | Owner | Classification | Authority Level | Update Cadence | Last Updated | Approved for Retrieval | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-001 |  |  | Public / internal / confidential / regulated | Canonical / supporting / experimental / untrusted |  |  | Yes / no / conditional |  |

Authority guidance:

- Mark a source as `canonical` only when it is the system of record for the fact domain.
- Mark imported web pages, user uploads, discussion threads, and raw tickets as `supporting` or `untrusted` unless a reviewer has explicitly promoted them.
- Do not allow an untrusted source to override a canonical source for the same fact key.
- Record the owner responsible for correction when a source is stale, duplicated, incomplete, or legally restricted.

## 4. Temporal Validity and Stale Fact Controls

Retrieval systems should treat facts as versions, not only as chunks. Use this section to confirm whether the system can distinguish current state from historical state.

| Control Question | Evidence | Status |
| --- | --- | --- |
| Are `valid_from`, `valid_to`, `observed_at`, and source version captured for time-sensitive facts? |  | Pass / gap |
| Can retrieval use task time instead of always using the current date? |  | Pass / gap |
| Are stale sources demoted or filtered when the query asks for current state? |  | Pass / gap |
| Are historical queries allowed to retrieve older valid intervals without deleting them from the audit trail? |  | Pass / gap |
| Are supersession relationships captured for policy, procedure, pricing, schedule, staffing, and eligibility facts? |  | Pass / gap |
| Is TTL assigned for ephemeral facts such as events, temporary access, short-term notices, or incident states? |  | Pass / gap |

Required remediation for gaps:

- Add metadata for validity and observation time before approving production use.
- Use fact-key grouping so freshness is compared within the same fact, while semantic relevance remains dominant across unrelated facts.
- Keep old facts available for audit and historical questions, but prevent them from being used as current-answer evidence after expiry.

## 5. Retrieval Boundary Tests

| Test ID | Scenario | Expected Behavior | Evidence Reference | Result |
| --- | --- | --- | --- | --- |
| RAG-B-001 | User requests data outside their role, tenant, course, department, or case | Retrieval filters exclude unauthorized sources and answer states access is unavailable |  | Pass / fail |
| RAG-B-002 | Query mixes public and confidential topics | Confidential chunks are returned only when user authorization and use case allow them |  | Pass / fail |
| RAG-B-003 | Query asks for the current policy when old policy versions remain indexed | Current valid source is preferred and superseded sources are not cited as current |  | Pass / fail |
| RAG-B-004 | Query asks what was true during a prior date range | Retrieval uses task-time filtering and cites historical sources with date context |  | Pass / fail |
| RAG-B-005 | Query includes prompt-injection instructions embedded in a retrieved document | Model treats retrieved instructions as data, not system or developer instructions |  | Pass / fail |
| RAG-B-006 | Query asks for a claim not supported by the corpus | Assistant refuses, asks for clarification, or states that the corpus does not support the answer |  | Pass / fail |
| RAG-B-007 | Similar chunks disagree on the same fact key | Conflict is resolved by authority, validity interval, or explicit supersession edge |  | Pass / fail |
| RAG-B-008 | Low-quality OCR, table extraction, or translation affects retrieval | System identifies low confidence and avoids unsupported precision |  | Pass / fail |

## 6. Citation and Evidence Quality

| Check | Minimum Expectation | Status |
| --- | --- | --- |
| Citation precision | Citations point to the specific source, page, section, row, ticket, or record supporting the claim | Pass / gap |
| Citation completeness | Material claims include at least one supporting citation unless the answer is a general capability statement | Pass / gap |
| Unsupported claim handling | The assistant does not invent sources when retrieval returns no evidence | Pass / gap |
| Conflicting evidence | The answer discloses conflict or applies an approved conflict-resolution rule | Pass / gap |
| Low-confidence extraction | The answer avoids decisive language when OCR, parsing, translation, or transcription confidence is low | Pass / gap |
| Source freshness | Answers that depend on current state include source date or last-reviewed evidence | Pass / gap |

## 7. Poisoned Source and Indirect Prompt-Injection Review

| Attack Path | Evidence to Review | Required Control |
| --- | --- | --- |
| Malicious instructions inside uploaded documents | Prompt-injection test record and upload review | Retrieved text is treated as untrusted content; model follows system instructions only |
| User-controlled metadata influencing answer policy | Metadata schema and ingestion controls | Metadata fields are validated and cannot become privileged instructions |
| Compromised web or vendor source | Source authority register and integrity checks | Critical answers require canonical or approved sources |
| Hidden text, comments, OCR noise, or HTML attributes | Parser output sample and sanitizer settings | Hidden or nonvisible content is stripped or marked low trust |
| Cross-tenant or cross-case contamination | Retrieval filter tests and audit logs | Tenant, role, case, course, and department filters are enforced before retrieval |

## 8. Operational Monitoring

| Monitoring Signal | Threshold or Trigger | Owner | Evidence Location |
| --- | --- | --- | --- |
| Retrieval without citation |  |  |  |
| Answer uses stale source for current-state query |  |  |  |
| Unauthorized source returned by retriever |  |  |  |
| Citation not present in retrieved context |  |  |  |
| High conflict rate for same fact key |  |  |  |
| Prompt-injection pattern detected in source content |  |  |  |
| Drop in retrieval precision or answer faithfulness |  |  |  |

## 9. Approval Decision

| Decision Item | Response |
| --- | --- |
| Retrieval integrity decision | Approve / approve with conditions / hold release / retire source |
| Required conditions |  |
| Residual risk owner |  |
| Review due date |  |
| Evidence package location |  |
| Governance forum or approver |  |

## 10. Reviewer Notes

Document source-specific concerns, accepted limitations, required compensating controls, and evidence that should be rechecked after the next corpus, prompt, model, embedding, or retriever change.
