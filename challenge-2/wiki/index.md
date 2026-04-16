---
title: "Challenge 2 Knowledge Base Index"
aliases:
  - "Challenge 2 Wiki"
  - "Dark Data Wiki"
note_type: "index"
tags:
  - "index"
  - "challenge-2"
  - "llm-wiki"
source_count: 43
updated: "2026-04-16"
---

# Challenge 2 Knowledge Base Index

This is the navigation entrypoint for the Challenge 2 Obsidian knowledge base. Raw documents remain in `structured_files/` and `unstructured_files/`; generated knowledge lives under `wiki/`.

## Start Here

- [Architecture overview](architecture.md)
- [Evaluation benchmark](evaluation-benchmark.md)
- [Lint report](lint-report.md)
- [Ingest log](log.md)
- [Machine-readable source register](data/source-register.json)

## Maps Of Content

- [Housing And Benefits Map](maps/housing-and-benefits.md)
- [Small Business And Employment Map](maps/small-business-and-employment.md)
- [Corporate Operations Map](maps/corporate-operations.md)
- [People Policies Map](maps/people-policies.md)
- [Risk Assurance And Compliance Map](maps/risk-assurance-and-compliance.md)

## Topic Pages

- [Housing Benefit](topics/housing-benefit.md) (15 sources)
- [Discretionary Housing Payments](topics/discretionary-housing-payments.md) (5 sources)
- [Council Tax Reduction](topics/council-tax-reduction.md) (8 sources)
- [Homelessness And Social Housing](topics/homelessness-and-social-housing.md) (8 sources)
- [Small Business And Self-employment](topics/small-business-and-self-employment.md) (8 sources)
- [Employment Rights And Flexible Working](topics/employment-rights-and-flexible-working.md) (10 sources)
- [Procurement And Spending Controls](topics/procurement-and-spending-controls.md) (3 sources)
- [Data Protection And Information Security](topics/data-protection-and-information-security.md) (6 sources)
- [FOI And Transparency](topics/foi-and-transparency.md) (6 sources)
- [People Policies](topics/people-policies.md) (12 sources)
- [Incident Risk And Assurance](topics/incident-risk-and-assurance.md) (13 sources)
- [Overpayment Recovery](topics/overpayment-recovery.md) (5 sources)
- [Welsh Language Standards](topics/welsh-language-standards.md) (4 sources)
- [Staff Directory](topics/staff-directory.md) (1 sources)

## Entity Pages

- [Department For Levelling Up Housing And Communities](entities/dluhc.md) (9 sources)
- [Department For Work And Pensions](entities/dwp.md) (20 sources)
- [Department For Business And Trade](entities/dbt.md) (2 sources)
- [HM Revenue And Customs](entities/hmrc.md) (6 sources)
- [Local Authorities](entities/local-authorities.md) (16 sources)
- [Housing Act 1996](entities/housing-act-1996.md) (1 sources)
- [Homelessness Reduction Act 2017](entities/homelessness-reduction-act-2017.md) (2 sources)
- [Employment Rights Act 1996](entities/employment-rights-act-1996.md) (4 sources)
- [HB1 Form](entities/hb1-form.md) (1 sources)
- [RTB1 Form](entities/rtb1-form.md) (1 sources)
- [Universal Credit Migration](entities/universal-credit-migration.md) (1 sources)
- [Cabinet Office](entities/cabinet-office.md) (4 sources)
- [Finance Directorate](entities/finance-directorate.md) (1 sources)
- [People Services](entities/people-services.md) (1 sources)

## Source Corpus

- Total sources: 43
- `docx`: 11
- `html`: 8
- `md`: 7
- `pdf`: 9
- `txt`: 5
- `xlsx`: 3

| Source | Status | Format | Department | Flags |
| --- | --- | --- | --- | --- |
| [DOC-HB-001](sources/doc-hb-001-housing-benefit-check-if-you-re-eligible-gov-uk.md) | current | html | DLUHC |  |
| [DOC-HB-002](sources/doc-hb-002-discretionary-housing-payments-guidance-for-local-autho.md) | current | md | DLUHC |  |
| [DOC-HB-003](sources/doc-hb-003-council-tax-reduction-schemes-regulatory-framework-and.md) | current | txt | Department for Levelling Up, Housing and Communities | stale/conflicted: DOC-HB-009 says it replaces the March 2024 version |
| [DOC-HB-004](sources/doc-hb-004-social-housing-frequently-asked-questions-gov-uk.md) | current | html | DLUHC |  |
| [DOC-HB-005](sources/doc-hb-005-homelessness-prevention-and-relief-local-authority-duti.md) | unknown | txt | DLUHC |  |
| [DOC-HB-006](sources/doc-hb-006-housing-benefit-claim-form-hb1-completion-instructions.md) | superseded | md | DLUHC | superseded, points readers to DOC-HB-006a |
| [DOC-HB-007](sources/doc-hb-007-housing-benefit-caseload-statistics-quarter-3-2025-26.md) | current | html | DLUHC |  |
| [DOC-HB-008](sources/doc-hb-008-summary-of-responses-to-the-consultation-on-discretiona.md) | unknown | txt | DLUHC |  |
| [DOC-HB-009](sources/doc-hb-009-council-tax-reduction-schemes-prescribed-requirements-e.md) | current | txt | DLUHC |  |
| [DOC-HB-010](sources/doc-hb-010-right-to-buy-guidance-for-tenants-and-social-landlords.md) | current | md | DLUHC |  |
| [DOC-SB-001](sources/doc-sb-001-starting-a-business-in-the-uk-step-by-step.md) | current | html | Department for Business and Trade |  |
| [DOC-SB-002](sources/doc-sb-002-registering-as-self-employed-with-hmrc.md) | current | md | HM Revenue and Customs |  |
| [DOC-SB-003](sources/doc-sb-003-national-minimum-wage-and-national-living-wage-employer.md) | current | html | Department for Business and Trade |  |
| [DOC-SB-004](sources/doc-sb-004-workplace-pensions-auto-enrolment-duties-for-employers.md) | current | txt |  |  |
| [DOC-SB-005](sources/doc-sb-005-employment-rights-act-1996-plain-english-summary.md) | current | md | Department for Business and Trade |  |
| [DOC-SB-006](sources/doc-sb-006-self-employment-and-housing-benefit-how-income-is-asses.md) | current | md | Department for Levelling Up, Housing and Communities |  |
| [DOC-SB-007](sources/doc-sb-007-statutory-sick-pay-ssp-employer-guide.md) | current | html | HM Revenue and Customs |  |
| [DOC-SB-008](sources/doc-sb-008-employer-duties-under-the-homelessness-reduction-act-20.md) | current | html | DLUHC / DBT |  |
| [DOC-SB-009](sources/doc-sb-009-right-to-request-flexible-working-frequently-asked-ques.md) | current | md | Department for Business and Trade |  |
| [DOC-SB-010](sources/doc-sb-010-small-business-survey-2025-annual-findings.md) | current | html | Department for Business and Trade |  |
| [UF-ACCEPTABLE-USE-POLICY-IT-SYSTEMS](sources/uf-acceptable-use-policy-it-systems-acceptable-use-policy-it-systems-and.md) | unknown | pdf | DWP |  |
| [UF-ANNUAL-LEAVE-POLICY](sources/uf-annual-leave-policy-annual-leave-policy.md) | unknown | docx | DWP |  |
| [UF-DATA-PROTECTION-GUIDANCE-FOR-STAFF-MARCH-2024](sources/uf-data-protection-guidance-for-sta-data-protection-guidance-for-staff.md) | unknown | pdf | DWP |  |
| [UF-ELIGIBILITY-CRITERIA-HOUSING-BENEFIT](sources/uf-eligibility-criteria-housing-ben-housing-benefit-eligibility-criteria.md) | unknown | docx |  |  |
| [UF-EQUALITY-IMPACT-ASSESSMENT-UC-MIGRATION](sources/uf-equality-impact-assessment-uc-mi-equality-impact-assessment-universal-credit.md) | unknown | pdf |  |  |
| [UF-FLEXIBLE-WORKING-POLICY](sources/uf-flexible-working-policy-flexible-working-policy.md) | unknown | pdf | DWP |  |
| [UF-FOI-RESPONSE-TEMPLATE](sources/uf-foi-response-template-template-freedom-of-information-act-2000-response.md) | unknown | docx | DWP |  |
| [UF-GRIEVANCE-POLICY-2024](sources/uf-grievance-policy-2024-grievance-policy.md) | unknown | docx | DWP |  |
| [UF-INCIDENT-REPORTING-V1](sources/uf-incident-reporting-v1-incident-reporting-procedure.md) | unknown | docx | DWP |  |
| [UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8](sources/uf-information-security-policy-draf-draft-not-for-distribution.md) | draft | docx | DWP | draft |
| [UF-MINISTERS-QUESTIONS-BRIEFING-PACK-12MARCH](sources/uf-ministers-questions-briefing-pac-ministerial-questions-briefing.md) | unknown | pdf |  |  |
| [UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3](sources/uf-overpayment-recovery-procedures-overpayment-recovery-procedures-v2-3.md) | unknown | xlsx | DWP |  |
| [UF-PERFORMANCE-MANAGEMENT-FRAMEWORK-2024-25](sources/uf-performance-management-framework-performance-management-framework-2024-25.md) | unknown | docx | DWP |  |
| [UF-PROCUREMENT-THRESHOLDS-2024-25](sources/uf-procurement-thresholds-2024-25-procurement-thresholds-2024-25.md) | unknown | xlsx | Cabinet Office |  |
| [UF-PROGRAMME-BOARD-MINUTES-14-FEB-2024](sources/uf-programme-board-minutes-14-feb-2-uc-managed-migration-programme-board.md) | unknown | docx | DWP |  |
| [UF-RAISING-CONCERNS-WHISTLEBLOWING-GUIDANCE](sources/uf-raising-concerns-whistleblowing-raising-concerns-at-work.md) | unknown | docx | DWP |  |
| [UF-RECRUITMENT-AND-SELECTION-POLICY](sources/uf-recruitment-and-selection-policy-recruitment-and-selection-policy.md) | unknown | pdf | DWP |  |
| [UF-SOCIAL-FUND-BUDGETING-LOANS-GUIDANCE-CHAPTER12](sources/uf-social-fund-budgeting-loans-guid-social-fund-guide-chapter-12-budgeting-loans.md) | unknown | pdf |  |  |
| [UF-SOCIAL-MEDIA-GUIDANCE-FOR-STAFF](sources/uf-social-media-guidance-for-staff-social-media-guidance-for-staff.md) | unknown | docx | DWP |  |
| [UF-SPENDING-CONTROLS-GUIDANCE](sources/uf-spending-controls-guidance-dwp-spending-controls-guidance.md) | unknown | pdf | DWP |  |
| [UF-STAFF-DIRECTORY-EXTRACT-Q4-2023](sources/uf-staff-directory-extract-q4-2023-staff-directory-extract-q4-2023.md) | unknown | xlsx | DWP | synthetic staff-directory fixture |
| [UF-TRAVEL-AND-SUBSISTENCE-POLICY-V2-0](sources/uf-travel-and-subsistence-policy-v2-travel-and-subsistence-policy.md) | unknown | docx | DWP | past review: next review was April 2022 |
| [UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023](sources/uf-welsh-language-standards-complia-adroddiad-cydymffurfiaeth-safonau-r-gymraeg.md) | unknown | pdf | DWP |  |

## Demo Questions

- Which Council Tax Reduction guidance is current? Start with [Council Tax Reduction](topics/council-tax-reduction.md).
- Can a self-employed person claim Housing Benefit? Start with [Small Business And Self-employment](topics/small-business-and-self-employment.md) and [Housing Benefit](topics/housing-benefit.md).
- Which staff policies are draft, stale, or past review? Start with [People Policies Map](maps/people-policies.md).
- What approvals are needed for IT hardware over GBP 5,000? Start with [Procurement And Spending Controls](topics/procurement-and-spending-controls.md).
- Which documents mention Discretionary Housing Payments? Start with [Discretionary Housing Payments](topics/discretionary-housing-payments.md).
