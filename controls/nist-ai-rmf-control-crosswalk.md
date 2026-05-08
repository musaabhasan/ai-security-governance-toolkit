# NIST AI RMF Control Crosswalk

This crosswalk maps toolkit artifacts to the NIST AI Risk Management Framework 1.0 functions: Govern, Map, Measure, and Manage. It is a practical implementation aid for teams that need to convert a framework discussion into concrete evidence, owners, review cadence, and release governance.

Primary references:

- NIST AI Risk Management Framework: <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST AI RMF 1.0 publication: <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10>
- NIST AI RMF Playbook: <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>

## How To Use This Crosswalk

1. Start from the AI system intake and risk tiering record.
2. Select the NIST AI RMF function that best describes the review need.
3. Use `nist-ai-rmf-control-crosswalk.csv` to identify relevant toolkit controls, evidence, owner role, and cadence.
4. Attach evidence references before governance review or release approval.
5. Use the report script to identify whether a governance packet covers all four functions.

## Function Coverage

| NIST AI RMF function | Toolkit implementation focus |
| --- | --- |
| GOVERN | Ownership, policies, risk appetite, control accountability, senior assurance, and approval records |
| MAP | Use-case context, data flows, human impact, system boundaries, third-party dependencies, and deployment assumptions |
| MEASURE | Evaluation, red-team testing, access review, monitoring indicators, evidence quality, and operating-effectiveness tests |
| MANAGE | Risk treatment, exceptions, incident readiness, continuity, decommissioning, deletion, and provider exit |

## Reporting

Generate a crosswalk report:

```bash
python scripts/nist_ai_rmf_crosswalk_report.py --format markdown
python scripts/nist_ai_rmf_crosswalk_report.py --format json
```

Use `--fail-on-missing-function` when a governance packet is expected to cover all four NIST AI RMF functions.
