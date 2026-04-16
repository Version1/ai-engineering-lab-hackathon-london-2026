---
title: "Challenge 2 Wiki Evaluation Benchmark"
note_type: "evaluation-benchmark"
tags:
  - "challenge-2"
  - "evaluation"
  - "llm-wiki"
  - "documentation"
updated: "2026-04-16"
---

# Challenge 2 Wiki Evaluation Benchmark

This benchmark is documentation only. It is designed to test how well an AI coding agent can use the Challenge 2 wiki as a source-backed knowledge base, not how much it already knows about government policy.

The benchmark assumes each agent is given access to the repository and asked to answer using only `challenge-2/wiki/`, `challenge-2/AGENTS.md`, and the machine-readable files under `challenge-2/wiki/data/`. The raw source files may be inspected only when the question explicitly asks about provenance back to the raw file path.

## Harness Prompt

Use this common instruction for every model run:

> You are answering a Challenge 2 wiki evaluation question. Use only the local repository content under `challenge-2/wiki/`, `challenge-2/wiki/data/`, and `challenge-2/AGENTS.md`. Cite the source IDs or wiki paths you used. If the wiki flags a source as draft, stale, superseded, synthetic, low quality, or past review, include that caveat. Do not use web search or outside knowledge.

Recommended captured fields for the harness:

- `model`: `gemini-cli`, `claude-code`, or `codex`
- `question_id`
- `question`
- `answer_text`
- `cited_sources`
- `elapsed_seconds`
- `tool_call_count`
- `score_0_to_5`
- `scorer_notes`

## Harness Implementation

The local harness lives in `challenge-2/tools/run_wiki_eval.py`. It parses this benchmark note, builds a wiki-only prompt for each selected question, invokes the selected CLI clients, and writes a DSAP-shaped audit pack under `challenge-2/evaluation/runs/<run-id>/`.

For fairness, generated prompts tell evaluated clients not to inspect this benchmark note or `challenge-2/evaluation/` while answering, because those paths contain gold answers and scoring material. The MCP read/search tools apply the same exclusion.

Typical dry-run smoke test:

```bash
python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --run-id smoke
```

Typical multi-client run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --clients codex,gemini,claude --questions Q001,Q002,Q003
```

The audited MCP layer lives in `challenge-2/tools/wiki_eval_mcp.py`. It exposes controlled wiki search/read tools, question listing, answer recording, and run finalisation without exposing gold answers to the evaluated client.

Run outputs include `answers.jsonl`, `event-ledger.jsonl`, `source-register.json`, `audit-card.json`, `integrity-manifest.json`, `generated/scoring-sheet.csv`, `generated/leaderboard.md`, and `bundle/DSAP-<run-id>.zip`.

For operational details see `challenge-2/evaluation/README.md`.

## Default Per-Question Rubric

Each question is worth 5 points.

- 5 points: complete, correct, source-backed answer; cites the relevant source ID or wiki path; includes any status, provenance, quality, or contradiction caveat required by the question.
- 4 points: materially correct and source-backed, but misses one minor required detail or caveat.
- 3 points: mostly correct factual answer, but incomplete, weakly sourced, or missing an important caveat.
- 2 points: partially correct but omits several required facts, confuses sources, or gives weak provenance.
- 1 point: minimal relevant content with major omissions.
- 0 points: incorrect, unsupported, uses outside knowledge as authority, fabricates values, or ignores the question.

Apply these global penalties unless a question-specific rubric says otherwise:

- Deduct 1 point if the answer does not cite at least one relevant source ID or wiki path.
- Deduct 1 point if the answer ignores an explicit source flag such as `draft`, `superseded`, `stale/conflicted`, `synthetic staff-directory fixture`, `past review`, or low OCR quality.
- Cap at 3 points if the answer uses a stale or superseded source as the current answer when the wiki identifies a newer source.
- Cap at 2 points if the answer invents facts not present in the wiki.

## Summative Scoring Regime

There are 100 questions, each worth 5 points, for a raw maximum of 500 points.

Final percentage score:

`final_score_percent = round((raw_points / 500) * 100, 1)`

Interpretation bands:

- 90.0 to 100.0: excellent wiki use; strong provenance, caveat handling, and exact table lookup.
- 75.0 to 89.9: good wiki use; mostly accurate with some missed edge cases or source-status caveats.
- 60.0 to 74.9: adequate wiki use; finds many facts but struggles with cross-source synthesis or risky sources.
- 40.0 to 59.9: weak wiki use; frequent omissions, poor citation, or unreliable synthesis.
- 0.0 to 39.9: not competitive; likely answering from guesses or outside priors.

Suggested category reporting:

- Wiki architecture and provenance: Q001-Q010, maximum 50 points.
- Housing, benefits, homelessness, and CTR: Q011-Q035, maximum 125 points.
- Business, employment, and workplace rights: Q036-Q055, maximum 100 points.
- Procurement and spending controls: Q056-Q062, maximum 35 points.
- Data protection, information security, FOI, social media, and whistleblowing: Q063-Q072, maximum 50 points.
- People policies and operational procedures: Q073-Q082, maximum 50 points.
- Overpayment, Social Fund, and staff-directory dark data: Q083-Q090, maximum 40 points.
- Welsh language, UC migration, OCR, statistics, and source-risk synthesis: Q091-Q100, maximum 50 points.

For a competitive leaderboard, rank by final percentage score. Use these tie-breakers in order:

1. Higher score on source-risk questions Q004, Q005, Q028, Q033, Q065, Q068, Q083, Q088, Q098, and Q100.
2. Higher average provenance score, measured by whether the cited source IDs match the gold sources.
3. Lower hallucination count.
4. Lower elapsed time, if the harness captures timing consistently.

## Question Set

### Q001

Category: Wiki architecture and provenance

Question: What is the source of truth for the Challenge 2 wiki, and what role does `wiki/` play?

Gold answer: The source of truth is the raw Challenge 2 corpus in `structured_files/` and `unstructured_files/`, which must be treated as read-only. The `wiki/` directory is the generated knowledge layer: source notes, topic pages, entity pages, maps, machine-readable data, architecture, lint report, and log. Every generated claim should remain traceable to a source note and raw source path. Sources: `challenge-2/AGENTS.md`, `challenge-2/wiki/architecture.md`.

Specific rubric: Full credit requires naming both raw source directories, saying they are immutable/read-only, and describing `wiki/` as generated/navigable rather than the original authority.

### Q002

Category: Wiki architecture and provenance

Question: According to the architecture page, what does the builder produce?

Gold answer: It produces 43 source notes, 14 topic pages, 14 entity pages, 5 maps of content, 3 workbook exports, and 5 flagged sources. Source: `challenge-2/wiki/architecture.md`.

Specific rubric: Full credit requires all six counts. Partial credit is proportional to correct counts.

### Q003

Category: Wiki architecture and provenance

Question: What source file formats and counts are listed for the Challenge 2 corpus?

Gold answer: `docx`: 11, `html`: 8, `md`: 7, `pdf`: 9, `txt`: 5, `xlsx`: 3. Sources: `challenge-2/wiki/index.md`, `challenge-2/wiki/architecture.md`.

Specific rubric: Full credit requires all six format counts. Deduct for missing or transposed counts.

### Q004

Category: Wiki architecture and provenance

Question: What does the lint report say about source count, note count, issue count, and generation time?

Gold answer: The lint report was generated at `2026-04-16T10:06:11+00:00`; it reports 43 sources, 81 notes, and 0 lint issues. Source: `challenge-2/wiki/lint-report.md`.

Specific rubric: Full credit requires all four values and cites the lint report.

### Q005

Category: Wiki architecture and provenance

Question: Which sources are listed as known challenge checks or review flags in the lint report?

Gold answer: `DOC-HB-003` is stale/conflicted because `DOC-HB-009` says it replaces the March 2024 version; `DOC-HB-006` is superseded and points readers to `DOC-HB-006a`; `UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8` is draft; `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023` is a synthetic staff-directory fixture; `UF-TRAVEL-AND-SUBSISTENCE-POLICY-V2-0` is past review because its next review was April 2022. Source: `challenge-2/wiki/lint-report.md`.

Specific rubric: Full credit requires all five source IDs and their flags. Cap at 3 if the answer lists flags without source IDs.

### Q006

Category: Wiki architecture and provenance

Question: What are the five maps of content, and how many sources does each map cover?

Gold answer: `Housing And Benefits Map`: 20 sources; `Small Business And Employment Map`: 12 sources; `Corporate Operations Map`: 13 sources; `People Policies Map`: 19 sources; `Risk Assurance And Compliance Map`: 20 sources. Sources: `challenge-2/wiki/index.md`, `challenge-2/wiki/maps/*.md`.

Specific rubric: Full credit requires all five map names and counts.

### Q007

Category: Wiki architecture and provenance

Question: Which topic has the most sources, and which topic has the fewest?

Gold answer: `Housing Benefit` has the most, with 15 sources. `Staff Directory` has the fewest, with 1 source. Source: `challenge-2/wiki/index.md`.

Specific rubric: Full credit requires both topic names and counts.

### Q008

Category: Wiki architecture and provenance

Question: Which entity page appears in the most source documents, and which entity page is second?

Gold answer: `Department For Work And Pensions` appears in 20 source documents. `Local Authorities` is second with 16 source documents. Source: `challenge-2/wiki/index.md` and `challenge-2/wiki/entities/dwp.md`.

Specific rubric: Full credit requires both entity names and counts.

### Q009

Category: Wiki architecture and provenance

Question: How should agents treat names, email-like values, phone-like values, and staff-directory entries in Challenge 2?

Gold answer: They should treat all Challenge 2 raw and generated data as synthetic hackathon fixture data and should not redact names, email-like values, phone-like values, roles, departments, or staff-directory entries solely because they resemble personal data. They should still flag real secrets, credentials, local filesystem paths, malformed links, bad provenance, and data copied from outside the Challenge 2 synthetic corpus. Source: `challenge-2/AGENTS.md`.

Specific rubric: Full credit requires both the non-redaction rule and the continuing duty to flag real issues.

### Q010

Category: Wiki architecture and provenance

Question: Summarise the ingest and validation flow shown in the architecture page.

Gold answer: The flow is: scan the corpus, fingerprint files with size and SHA-256, extract content using tools such as Pandoc, pdftotext, ExifTool, and openpyxl, normalise metadata, write source notes and export tables, cross-link source IDs/topics/entities/maps, lint for coverage, broken links, and risk signals, then produce a demo-ready vault. Source: `challenge-2/wiki/architecture.md`.

Specific rubric: Full credit requires the ordered flow and at least three named extraction/validation concepts.

### Q011

Category: Housing, benefits, homelessness, and CTR

Question: What are the main eligibility conditions for Housing Benefit in the current GOV.UK-style guidance?

Gold answer: A claimant may be eligible if they pay rent to a local authority, housing association, or private landlord; are on a low income or receive certain benefits such as Income Support, income-based JSA, or income-related ESA; have savings and capital below GBP 16,000, or below GBP 6,000 if in a care home; are not already receiving the housing costs element of Universal Credit; and are habitually resident in the UK, Channel Islands, Isle of Man, or Republic of Ireland. Source: `DOC-HB-001`.

Specific rubric: Full credit requires rent, low income/benefits, capital threshold, no UC housing costs element, and habitual residence.

### Q012

Category: Housing, benefits, homelessness, and CTR

Question: How does the current Housing Benefit guidance treat State Pension age claimants and most working-age new claims?

Gold answer: People who have reached State Pension age can still make a new Housing Benefit claim. Working-age new claims are generally directed to Universal Credit unless the claimant is in temporary or specified accommodation, or is already receiving the severe disability premium as part of an existing benefit. Source: `DOC-HB-001`.

Specific rubric: Full credit requires both the State Pension age rule and the working-age exceptions.

### Q013

Category: Housing, benefits, homelessness, and CTR

Question: What taper is used when Housing Benefit income exceeds the applicable amount?

Gold answer: If income exceeds the applicable amount, Housing Benefit is reduced by 65 pence for every pound of excess income. Sources: `DOC-HB-001`, `UF-ELIGIBILITY-CRITERIA-HOUSING-BENEFIT`.

Specific rubric: Full credit requires the 65 pence per GBP 1 excess-income taper and a Housing Benefit source.

### Q014

Category: Housing, benefits, homelessness, and CTR

Question: What does `DOC-HB-001` say about applying for Housing Benefit and backdating?

Gold answer: Housing Benefit is administered by the local council, and claims can usually be made online, by post, or by telephone. Claimants must provide evidence of identity, income, rent liability, and savings. Claims are normally backdated to the Monday after the council receives the claim, though backdating of up to one month, or three months for pension-age claimants, may be granted in some circumstances. Source: `DOC-HB-001`.

Specific rubric: Full credit requires the local council route, evidence types, normal Monday rule, and one-month/three-month backdating distinction.

### Q015

Category: Housing, benefits, homelessness, and CTR

Question: What is the gateway condition for a Discretionary Housing Payment?

Gold answer: The applicant must have entitlement to Housing Benefit or the housing costs element of Universal Credit. A DHP is not Housing Benefit itself, is not subject to the same statutory calculation rules, and there is no statutory right to a DHP. Local authorities have broad discretion and the claimant does not need to receive the maximum Housing Benefit to qualify. Source: `DOC-HB-002`.

Specific rubric: Full credit requires the gateway condition and at least two of the caveats about discretion, no statutory right, not HB itself, or no need for maximum HB.

### Q016

Category: Housing, benefits, homelessness, and CTR

Question: What mandatory evidence should DHP officers request?

Gold answer: Mandatory evidence includes proof of identity, a tenancy agreement, and a recent bank statement or income declaration. Additional evidence may be requested where necessary, but authorities must not impose excessive requirements that deter vulnerable applicants. Source: `DOC-HB-002`.

Specific rubric: Full credit requires all three mandatory evidence categories and the proportionality caveat.

### Q017

Category: Housing, benefits, homelessness, and CTR

Question: How should a DHP award amount and duration normally be set?

Gold answer: The award should generally bridge the gap between Housing Benefit entitlement and eligible rent, unless a partial award is more appropriate. It must not exceed the applicant's eligible rent liability. Short-term awards of 13 weeks are typical, with a review before any extension. Source: `DOC-HB-002`.

Specific rubric: Full credit requires bridge-the-gap, cannot exceed eligible rent liability, and 13-week typical duration.

### Q018

Category: Housing, benefits, homelessness, and CTR

Question: What are the DHP notification, review, and monitoring expectations?

Gold answer: The applicant must be notified in writing within 14 working days after the authority has all necessary information. Refusal notices must give reasons and explain the right to request an internal review. Reviews must be conducted by an officer not involved in the original decision. Authorities must record decisions with a clear audit trail and submit quarterly monitoring returns to DLUHC. Source: `DOC-HB-002`.

Specific rubric: Full credit requires the 14-working-day notice, internal review independence, audit trail, and quarterly DLUHC returns.

### Q019

Category: Housing, benefits, homelessness, and CTR

Question: What were the key dates, response count, and headline percentages from the DHP reform consultation summary?

Gold answer: The consultation ran from 1 June 2025 to 31 August 2025 and received 342 responses. Headline findings were: 73 percent agreed eligibility criteria should be broadened; 58 percent supported moving to a funding allocation model incorporating housing need indicators; 81 percent supported introducing a statutory right of appeal; and 67 percent supported standardised quarterly reporting of DHP expenditure and outcomes. Source: `DOC-HB-008`.

Specific rubric: Full credit requires the date range, 342 responses, and all four percentages with topics.

### Q020

Category: Housing, benefits, homelessness, and CTR

Question: What two-stage DHP appeals model did consultation respondents propose?

Gold answer: First, an internal reconsideration by a senior officer not involved in the original decision, completed within 14 days. Second, an independent review by a panel including at least one external member, completed within 28 days. Source: `DOC-HB-008`.

Specific rubric: Full credit requires both stages, the independence requirements, and both timescales.

### Q021

Category: Housing, benefits, homelessness, and CTR

Question: What did the Homelessness Reduction Act 2017 change about threatened homelessness and local authority duties?

Gold answer: It extended the period during which a person is treated as threatened with homelessness from 28 days to 56 days before likely loss of accommodation. The prevention duty under section 195 lasts for 56 days, and the relief duty under section 189B also lasts for 56 days. Source: `DOC-HB-005`.

Specific rubric: Full credit requires the 28-to-56-day change and both 56-day duty durations.

### Q022

Category: Housing, benefits, homelessness, and CTR

Question: When is the main housing duty owed, and what is the duty to refer?

Gold answer: The main housing duty under section 193 is owed when the applicant is homeless, eligible for assistance, in priority need, and not intentionally homeless. The duty to refer under section 213B requires specified public authorities, including hospitals, prisons, jobcentres, and social services departments, to refer service users who may be homeless or threatened with homelessness to the local housing authority with the individual's consent. Source: `DOC-HB-005`.

Specific rubric: Full credit requires all four main-duty tests and the consent-based referral rule with examples of public authorities.

### Q023

Category: Housing, benefits, homelessness, and CTR

Question: How does the social housing FAQ describe applying for social housing and reasonable preference?

Gold answer: Applicants join the local council's housing register, usually online, by telephone, or in person through the housing options team. Councils must give reasonable preference to people who are homeless or threatened with homelessness, people living in unsanitary, overcrowded, or otherwise unsatisfactory housing, people needing to move on medical or welfare grounds, and people needing to move to a particular area to avoid hardship. Source: `DOC-HB-004`.

Specific rubric: Full credit requires the housing register route and all four reasonable-preference groups.

### Q024

Category: Housing, benefits, homelessness, and CTR

Question: What bedroom standard rules does the social housing FAQ list?

Gold answer: The general rules are one bedroom for each adult couple; one for each other person aged 16 or over; one for two children of the same sex under 16; one for two children under 10 regardless of sex; and one for any remaining child. An extra bedroom may be allowed for an overnight carer or for a disabled person who cannot share a bedroom with their partner because of disability. Source: `DOC-HB-004`.

Specific rubric: Full credit requires all five base rules and the two extra-bedroom caveats.

### Q025

Category: Housing, benefits, homelessness, and CTR

Question: How should an answer handle the Right to Buy tenancy-period rule in `DOC-HB-010`?

Gold answer: The eligibility section says a tenant must have been a public sector tenant for at least 3 years, but the October 2025 update says the qualifying tenancy period was increased from 3 years to 5 years for all new applications received on or after 1 April 2025. Applications submitted before 1 April 2025 are assessed under the previous 3-year period. Source: `DOC-HB-010`.

Specific rubric: Full credit requires both the older 3-year statement and the later 5-year rule, with the application-date distinction.

### Q026

Category: Housing, benefits, homelessness, and CTR

Question: What Right to Buy discount caps and repayment scale are given?

Gold answer: The regional maximum discount is GBP 96,000 outside London and GBP 127,900 in London, frozen at 2024-25 levels for 2025-26. If the buyer sells within 5 years, discount repayment is 100 percent in year 1, 80 percent in year 2, 60 percent in year 3, 40 percent in year 4, and 20 percent in year 5. Source: `DOC-HB-010`.

Specific rubric: Full credit requires both caps, the freeze caveat, and all five repayment percentages.

### Q027

Category: Housing, benefits, homelessness, and CTR

Question: What are the key Right to Buy application-process deadlines?

Gold answer: The tenant submits RTB1 to the landlord. The landlord must acknowledge receipt within 4 weeks. The landlord must serve a Section 124 notice within 4 weeks if it admits the Right to Buy, or within 8 weeks if it denies it. A tenant who disagrees with valuation can request a District Valuer determination within 3 months of the Section 124 notice. The buyer has 12 months to complete once terms are agreed; after that the landlord may serve a notice requiring completion within 56 days. Source: `DOC-HB-010`.

Specific rubric: Full credit requires RTB1, 4-week acknowledgement, 4/8-week Section 124 rule, 3-month valuation challenge, 12-month completion, and 56-day notice.

### Q028

Category: Housing, benefits, homelessness, and CTR

Question: Which Council Tax Reduction guidance should be treated as current, and what warning applies to `DOC-HB-003`?

Gold answer: `DOC-HB-009` should be treated as the current CTR prescribed requirements guidance. It says it replaces the version published in March 2024. `DOC-HB-003` is flagged as stale/conflicted because `DOC-HB-009` replaces the March 2024 regulatory position. Sources: `DOC-HB-009`, `DOC-HB-003`, `challenge-2/wiki/lint-report.md`.

Specific rubric: Full credit requires identifying `DOC-HB-009` as current and explicitly warning against relying on `DOC-HB-003` as current.

### Q029

Category: Housing, benefits, homelessness, and CTR

Question: What commencement, scheme-revision, and reporting deadlines does the 2025 CTR guidance set?

Gold answer: The regulations apply in England only, come into force on 1 October 2025, and apply to 2025-26 and subsequent years. Local authorities must revise local schemes by 31 January 2026 or the default scheme will be imposed. Annual returns to the Department are due by 30 June after the end of each financial year. Source: `DOC-HB-009`.

Specific rubric: Full credit requires England-only scope, 1 October 2025, 31 January 2026, default-scheme consequence, and 30 June annual-return deadline.

### Q030

Category: Housing, benefits, homelessness, and CTR

Question: What income and capital threshold changes does the 2025 CTR guidance list?

Gold answer: Single claimant aged 18 to 24 increases from GBP 71.70 to GBP 77.25 per week; single claimant aged 25 or over increases from GBP 90.50 to GBP 97.60; couple where both are 18 or over increases from GBP 142.25 to GBP 153.30; lone parent increases from GBP 90.50 to GBP 97.60, with child additions in Schedule 2. The capital upper limit stays at GBP 16,000, and the lower capital limit increases from GBP 6,000 to GBP 6,500. Source: `DOC-HB-009`.

Specific rubric: Full credit requires all four income threshold changes and both capital limits.

### Q031

Category: Housing, benefits, homelessness, and CTR

Question: What new CTR provisions apply to carers, care leavers, and non-dependant deductions?

Gold answer: A claimant receiving Carer's Allowance, with income not exceeding 150 percent of the applicable amount, is entitled to a minimum CTR of 25 percent. Qualifying care leavers aged 18 to 25 must receive not less than 100 percent CTR, subject to a means test. Non-dependant deductions are GBP 15.80 per week for a non-dependant in remunerative work with gross weekly income of GBP 236 or more; GBP 5.25 where gross weekly income is below GBP 236; GBP 5.25 where not in remunerative work; and no deduction where the non-dependant receives Carer's Allowance. Source: `DOC-HB-009`.

Specific rubric: Full credit requires carers, care leavers, all deduction amounts, and the no-deduction Carer's Allowance caveat.

### Q032

Category: Housing, benefits, homelessness, and CTR

Question: What transitional protection must local authorities provide under the 2025 CTR guidance?

Gold answer: Where a revised scheme reduces an existing claimant's CTR, the local authority must provide transitional protection for at least 12 months from the revised scheme's effective date. During that period, the claimant's reduction must not fall below 75 percent of what would have been awarded under the previous scheme. Source: `DOC-HB-009`.

Specific rubric: Full credit requires the 12-month minimum and 75-percent floor.

### Q033

Category: Housing, benefits, homelessness, and CTR

Question: What inconsistency appears in the Housing Benefit Q3 2025-26 statistics note?

Gold answer: The summary states total Housing Benefit caseload in England at the end of December 2025 was 2,487,300, but the regional table's `England Total` row gives 2,387,300. A strong answer should report the inconsistency rather than silently choosing one. Source: `DOC-HB-007`.

Specific rubric: Full credit requires both conflicting figures and an explicit caveat about the inconsistency.

### Q034

Category: Housing, benefits, homelessness, and CTR

Question: What do the Q3 2025-26 Housing Benefit statistics say about London, total expenditure, and data quality?

Gold answer: London had 456,300 claimants and an average weekly award of GBP 162.40. Total Q3 2025-26 expenditure was GBP 3.64 billion, with GBP 2.41 billion in the social rented sector and GBP 1.23 billion in the private rented sector. Data from 4 local authorities, representing about 0.6 percent of the total caseload, were carried forward because returns were delayed or incomplete. Source: `DOC-HB-007`.

Specific rubric: Full credit requires the London count and award, the three expenditure figures, and the carried-forward data-quality caveat.

### Q035

Category: Housing, benefits, homelessness, and CTR

Question: How is self-employment income assessed for Housing Benefit, and when does the minimum income floor apply?

Gold answer: Local authorities assess self-employment income on net profit, deducting permitted business expenses from gross income over the relevant assessment period. The normal assessment period is the most recent full trading year; if trading for less than a year, the authority uses the period from start of trading to claim date and annualises it. The minimum income floor applies where the claimant has been self-employed for more than 12 months and is in gainful self-employment; it assumes earnings at least equivalent to the National Minimum Wage for expected hours, typically 35 hours per week for a single claimant without caring responsibilities. It does not apply during the first 12 months of a new business. Source: `DOC-SB-006`.

Specific rubric: Full credit requires net-profit basis, annualisation for new traders, MIF trigger, 35-hour typical assumption, and start-up-period exception.

### Q036

Category: Business, employment, and workplace rights

Question: What are the main steps and thresholds in the starting-a-business guidance?

Gold answer: The steps are choose a business structure, register the business, set up business tax, understand employer duties, and get required licences and insurance. All businesses must register with HMRC; sole traders register for Self Assessment, companies incorporate with Companies House, and partnerships register with HMRC and nominate a filing partner. Businesses must register within 3 months of starting to trade. VAT registration is required if taxable turnover exceeds GBP 90,000 per year. Employers must obtain Employers' Liability insurance with minimum cover of GBP 5 million. Food businesses must register with local environmental health at least 28 days before opening. Source: `DOC-SB-001`.

Specific rubric: Full credit requires the step list plus the 3-month, GBP 90,000, GBP 5 million, and 28-day thresholds.

### Q037

Category: Business, employment, and workplace rights

Question: How does the business-structures table compare sole traders, limited companies, and partnerships?

Gold answer: A sole trader has unlimited personal liability, pays Income Tax and Class 2/4 National Insurance via Self Assessment, and registers with HMRC. A limited company has liability limited to shares held, pays Corporation Tax on profits while directors pay Income Tax on salary and dividends, and must incorporate with Companies House and register for Corporation Tax. In a partnership, each partner has unlimited personal liability unless it is an LLP, each partner pays Income Tax on their share of profits via Self Assessment, and the partnership plus each partner must register with HMRC. Source: `DOC-SB-001`.

Specific rubric: Full credit requires liability, tax treatment, and registration for all three structures.

### Q038

Category: Business, employment, and workplace rights

Question: Who must register as self-employed with HMRC, what is the deadline, and what does HMRC send after registration?

Gold answer: A person must register if they earn more than GBP 1,000 in a tax year from self-employment or need to prove they are self-employed. They do not need to register below the GBP 1,000 trading allowance if they do not claim expenses. They must register by 5 October in the second tax year after starting the business, though HMRC recommends registering as soon as possible. HMRC sends a Unique Taxpayer Reference within 10 working days. Source: `DOC-SB-002`.

Specific rubric: Full credit requires the GBP 1,000 rule, deadline, recommendation, and 10-working-day UTR.

### Q039

Category: Business, employment, and workplace rights

Question: What National Insurance and record-keeping rules does the self-employment registration guidance give?

Gold answer: Self-employed people are liable for Class 2 National Insurance if profits exceed the Small Profits Threshold, currently GBP 6,725 per year. Class 4 National Insurance is calculated automatically on profits above GBP 12,570 when the return is filed. Self Assessment tax returns and payments are due by 31 January after the end of the tax year. Income and expense records must be kept for at least five years after the 31 January submission deadline. Source: `DOC-SB-002`.

Specific rubric: Full credit requires both NI thresholds, the 31 January filing/payment rule, and five-year record retention.

### Q040

Category: Business, employment, and workplace rights

Question: What late-registration penalties are listed for self-employed HMRC registration?

Gold answer: Up to 3 months late: initial penalty of GBP 100. 3 to 6 months: GBP 10 per day, up to GBP 900. 6 to 12 months: greater of 5 percent of tax due or GBP 300. More than 12 months: greater of 100 percent of tax due or GBP 300, depending on circumstances. Source: `DOC-SB-002`.

Specific rubric: Full credit requires all four bands and amounts.

### Q041

Category: Business, employment, and workplace rights

Question: What National Minimum Wage and National Living Wage rates apply from April 2025?

Gold answer: From 1 April 2025: age 21 and over National Living Wage is GBP 12.21 per hour; ages 18 to 20 is GBP 10.00; under 18 is GBP 7.55; apprentice rate is GBP 7.55. The apprentice rate applies to apprentices under 19 or aged 19 and over in the first year of apprenticeship; other apprentices get their age-band rate. Source: `DOC-SB-003`.

Specific rubric: Full credit requires all four rates and the apprentice caveat.

### Q042

Category: Business, employment, and workplace rights

Question: What common minimum-wage calculation errors and penalties are described?

Gold answer: Common errors include uniform or equipment deductions that reduce effective pay below the minimum wage, failing to pay for all working time, applying the wrong age band, averaging pay incorrectly over more than the pay reference period, and misclassifying salaried workers. Employers found to have underpaid must pay arrears and may face a penalty up to 200 percent of the total underpayment, capped at GBP 20,000 per worker. Repeated or deliberate failures may lead to public naming, prosecution, and director disqualification for up to 15 years. Source: `DOC-SB-003`.

Specific rubric: Full credit requires at least four errors plus arrears, 200-percent/GBP 20,000 penalty, and 15-year disqualification risk.

### Q043

Category: Business, employment, and workplace rights

Question: How does the auto-enrolment guidance classify workers?

Gold answer: Eligible jobholders are aged between 22 and State Pension age and earn more than GBP 10,000 per year, or pro-rated equivalent, and must be automatically enrolled. Non-eligible jobholders are aged 16 to 74 and earn more than GBP 6,240 but do not meet the full criteria, such as ages 16 to 21 or earnings between GBP 6,240 and GBP 10,000; they have the right to opt in. Entitled workers are aged 16 to 74 and earn below GBP 6,240; they can join a pension scheme but the employer need not contribute. Source: `DOC-SB-004`.

Specific rubric: Full credit requires all three categories, age ranges, earnings thresholds, and employer duties.

### Q044

Category: Business, employment, and workplace rights

Question: What contribution, opt-out, re-enrolment, and record-keeping rules does the auto-enrolment guidance give?

Gold answer: From April 2019 onwards, minimum defined-contribution rates are 3 percent employer, 5 percent employee, 8 percent total, based on qualifying earnings between GBP 6,240 and GBP 50,270. A worker can opt out within one calendar month of enrolment or receiving enrolment information, whichever is later, and contributions already deducted must be refunded. Employers must cyclically re-enrol eligible jobholders roughly every three years. Auto-enrolment records must be kept for six years. Source: `DOC-SB-004`.

Specific rubric: Full credit requires contribution rates, earnings band, opt-out/refund rule, three-year re-enrolment, and six-year records.

### Q045

Category: Business, employment, and workplace rights

Question: What escalating daily penalties can The Pensions Regulator impose for continued auto-enrolment non-compliance?

Gold answer: After a fixed penalty notice of GBP 400, escalating daily penalties are: 1 to 4 workers, GBP 50 per day; 5 to 49, GBP 500; 50 to 249, GBP 2,500; 250 to 499, GBP 5,000; 500 or more, GBP 10,000. Source: `DOC-SB-004`.

Specific rubric: Full credit requires all worker bands and daily rates, plus the GBP 400 fixed penalty context.

### Q046

Category: Business, employment, and workplace rights

Question: What unfair dismissal and redundancy rights are summarised in the Employment Rights Act note?

Gold answer: An employee with at least two years of continuous employment has the right not to be unfairly dismissed. Potentially fair reasons include capability or qualifications, conduct, redundancy, statutory-duty contravention, and some other substantial reason. Automatically unfair reasons apply regardless of service length and include asserting a statutory right, pregnancy or maternity, whistleblowing/protected disclosure, and trade union membership or activities. Employees with two years of continuous employment dismissed by reason of redundancy are entitled to a statutory redundancy payment, calculated by age, service up to 20 years, and capped weekly pay. Source: `DOC-SB-005`.

Specific rubric: Full credit requires the two-year rule, fair reasons, at least three automatic unfair reasons, and redundancy-payment basis.

### Q047

Category: Business, employment, and workplace rights

Question: What does the ERA summary say about flexible working requests and written employment particulars?

Gold answer: All employees have the right to request flexible working from day one. Employers must handle requests reasonably and notify the employee within two months unless an extension is agreed. Refusal must be on statutory business grounds. A tribunal can order reconsideration and award up to eight weeks' pay. Employers must provide every employee and worker with a written statement of employment particulars on or before the first day of employment; failure may lead to two or four weeks' pay in a later tribunal claim. Source: `DOC-SB-005`.

Specific rubric: Full credit requires day-one right, two-month decision, statutory grounds, eight-week compensation, first-day written statement, and two/four-week remedy.

### Q048

Category: Business, employment, and workplace rights

Question: What are the 2025-26 Statutory Sick Pay rates and duration rules?

Gold answer: For 2025-26, SSP is GBP 116.75 per week. The daily rate is GBP 23.35 for five qualifying days and GBP 19.46 for six qualifying days. SSP is payable for up to 28 weeks in a single period of incapacity, and the first three qualifying days are waiting days during which SSP is not payable. Source: `DOC-SB-007`.

Specific rubric: Full credit requires the weekly rate, both daily rates, 28-week duration, and three waiting days.

### Q049

Category: Business, employment, and workplace rights

Question: What qualifying and notification conditions apply to SSP?

Gold answer: The employee must be classed as an employee, have done some work for the employer, be off sick for four or more consecutive days including non-working days, earn an average of at least GBP 123 per week, and notify the employer by the required deadline. Employees are responsible for notifying within seven days of the first day of incapacity, but employers should note employees have up to 28 days to provide notification before SSP may be withheld, unless a contractual notification procedure was unreasonably not followed. For absences over seven days, a fit note is needed; seven days or fewer may be self-certified. Source: `DOC-SB-007`.

Specific rubric: Full credit requires eligibility tests, GBP 123 threshold, 7-day and 28-day notification distinction, and fit-note rule.

### Q050

Category: Business, employment, and workplace rights

Question: How does SSP interact with Housing Benefit and Council Tax Reduction?

Gold answer: Employees receiving SSP may also be entitled to means-tested benefits such as Housing Benefit or Council Tax Reduction. SSP counts as earned income for these benefit calculations. Employers are not required to notify the local authority that an employee is receiving SSP, but should be prepared to confirm SSP payments if requested by the employee or local authority. Source: `DOC-SB-007`.

Specific rubric: Full credit requires SSP counts as earned income and the employer notification/no-notification distinction.

### Q051

Category: Business, employment, and workplace rights

Question: Are private-sector employers legally subject to the homelessness duty to refer, and what should they do if an employee consents?

Gold answer: Private-sector employers are not subject to the statutory duty to refer, but the government strongly encourages employers to identify and support employees at risk of homelessness. If an employee consents, the employer should contact the housing options team at the local authority where the employee has a local connection, usually where they live or were last settled. The referral should include the employee's name, contact details, and a brief housing-circumstances description, but only information the employee has agreed to share. Source: `DOC-SB-008`.

Specific rubric: Full credit requires "not statutory", consent, local-connection authority, and agreed information only.

### Q052

Category: Business, employment, and workplace rights

Question: What are the statutory flexible-working request rules in `DOC-SB-009`?

Gold answer: All employees have the right to request flexible working from the first day of employment; the previous 26-week service requirement was removed on 6 April 2024. Employees may make up to two statutory requests in any 12-month period. Each request must be written, dated, and state it is a statutory request under section 80F of the Employment Rights Act 1996. Source: `DOC-SB-009`.

Specific rubric: Full credit requires day-one right, 26-week removal date, two requests per 12 months, and written/dedicated section 80F requirement.

### Q053

Category: Business, employment, and workplace rights

Question: What grounds can an employer use to refuse a statutory flexible-working request, and what remedy exists for process failures?

Gold answer: The eight refusal grounds are burden of additional costs, detrimental effect on ability to meet customer demand, inability to reorganise work among existing staff, inability to recruit additional staff, detrimental impact on quality, detrimental impact on performance, insufficiency of work during proposed working periods, and planned structural changes. The employer must consult before refusal. If the employer mishandles the request, misses the time limit, or uses other grounds, a tribunal may order reconsideration and award up to eight weeks' pay. Source: `DOC-SB-009`.

Specific rubric: Full credit requires all eight grounds, consultation, and tribunal remedy.

### Q054

Category: Business, employment, and workplace rights

Question: What was the methodology of the 2025 Small Business Survey?

Gold answer: The survey was conducted between September and November 2025, specifically 4 September to 28 November, online and by telephone. It covered registered SMEs in England with 0 to 249 employees, using a sample from the Inter-Departmental Business Register stratified by size band, sector, and region. It received 8,472 valid responses, a 28.3 percent response rate. Results were weighted to the SME population, and headline confidence intervals were within plus or minus 1.5 percentage points at the 95 percent confidence level. Source: `DOC-SB-010`.

Specific rubric: Full credit requires fieldwork dates, coverage, sample source/stratification, response count/rate, weighting, and confidence interval.

### Q055

Category: Business, employment, and workplace rights

Question: What were the main size, sector, and regional findings from the Small Business Survey?

Gold answer: Micro businesses had 5,284,000 businesses, 95.4 percent of all SMEs, and 8,912,000 employees. All SMEs totalled 5,537,000 businesses and 17,360,000 employees. Technology had the strongest net employment growth balance at plus 25 percent and estimated 62,000 net jobs created; professional services created the most net jobs, 89,000. Retail had minus 47,000 estimated net jobs. London had the highest confidence index at 112; the North East had the lowest at 88 and the largest year-on-year fall, minus 8. Source: `DOC-SB-010`.

Specific rubric: Full credit requires micro/all-SME values, technology/professional-services/retail employment findings, and London/North East confidence findings.

### Q056

Category: Procurement and spending controls

Question: What procurement thresholds apply to goods, services, works, and ICT in the 2024-25 spreadsheet?

Gold answer: Goods and services: under GBP 10,000 requires a single quote; GBP 10,000 to GBP 50,000 requires three written quotes. Works: under GBP 25,000 requires a single quote; GBP 25,000 to GBP 100,000 requires three written quotes, for capital works only. ICT: under GBP 10,000 requires a single quote; GBP 10,000 to GBP 50,000 requires a Technology Assessment and must involve CDDO for cloud. GBP 50,000 to the FTS threshold requires formal tender, and above the FTS threshold requires the full OJEU/FTS process. Source: `UF-PROCUREMENT-THRESHOLDS-2024-25`.

Specific rubric: Full credit requires all category thresholds and the cloud/CDDO and FTS escalation caveats.

### Q057

Category: Procurement and spending controls

Question: What approver and additional requirements apply at each procurement approval value band?

Gold answer: GBP 0 to GBP 10,000: Budget holder, no additional requirements. GBP 10,001 to GBP 50,000: Grade 6, business case required. GBP 50,001 to GBP 100,000: SCS1, business case plus Commercial review. GBP 100,001 to GBP 250,000: SCS2, full business case plus Commercial approval. GBP 250,001 to GBP 1,000,000: Finance Director, Investment Committee. Over GBP 1,000,000: Accounting Officer, HMT approval may be required. Source: `UF-PROCUREMENT-THRESHOLDS-2024-25`.

Specific rubric: Full credit requires all six value bands with approver and requirements.

### Q058

Category: Procurement and spending controls

Question: Which spending categories require Cabinet Office approval regardless of value?

Gold answer: Advertising, marketing, and communications; strategic supplier contracts above GBP 10 million total value; consultancy; redundancy and compensation above scheme terms; property, including new leases or lease extensions; digital and technology above GBP 1 million or using novel technology; commercial models such as PFI, concessions, and joint ventures; and grants to external bodies. Source: `UF-SPENDING-CONTROLS-GUIDANCE`.

Specific rubric: Full credit requires all eight categories and the thresholds/caveats for strategic suppliers and digital/technology.

### Q059

Category: Procurement and spending controls

Question: What approvals are needed for IT hardware over GBP 5,000, and what business-case thresholds may also matter?

Gold answer: Under DWP internal spending controls, IT hardware over GBP 5,000 requires IT Asset Board approval. Depending on total value, the procurement spreadsheet may also require procurement approvals and an ICT Technology Assessment, for example GBP 10,000 to GBP 50,000 requires Technology Assessment, and the approval matrix requires Grade 6 approval with a business case for GBP 10,001 to GBP 50,000. Separately, all expenditure over GBP 25,000 requires a business case: summary for GBP 25,000 to GBP 100,000, standard HMT Green Book five-case model for GBP 100,000 to GBP 1,000,000, and full business case with options analysis over GBP 1,000,000. Sources: `UF-SPENDING-CONTROLS-GUIDANCE`, `UF-PROCUREMENT-THRESHOLDS-2024-25`.

Specific rubric: Full credit requires IT Asset Board over GBP 5,000 plus the conditional procurement, technology assessment, and business-case caveats.

### Q060

Category: Procurement and spending controls

Question: How do urgent retrospective spending approvals work?

Gold answer: In genuinely urgent situations where obtaining approval would cause unacceptable delay, retrospective approval may be sought. It must be obtained within 5 working days, requires Director approval, and retrospective approvals are reported quarterly to the Audit and Risk Committee. Source: `UF-SPENDING-CONTROLS-GUIDANCE`.

Specific rubric: Full credit requires urgency, 5 working days, Director approval, and quarterly Audit and Risk Committee reporting.

### Q061

Category: Procurement and spending controls

Question: How does the recruitment policy say recruitment agency spend relates to procurement thresholds?

Gold answer: Use of recruitment agencies requires Commercial Directorate approval regardless of cost because recruitment agency spend falls under the consultancy spending control. The policy also states recruitment costs should be considered separately from procurement, and the Procurement Thresholds do not apply to salary commitments. Source: `UF-RECRUITMENT-AND-SELECTION-POLICY`.

Specific rubric: Full credit requires Commercial Directorate approval regardless of cost and the distinction between recruitment/salary commitments and procurement thresholds.

### Q062

Category: Procurement and spending controls

Question: What notes does the procurement thresholds workbook give about VAT, FTS thresholds, frameworks, emergency procurements, and review dates?

Gold answer: All values exclude VAT. FTS thresholds are updated every two years by the Cabinet Office. Framework call-offs should follow the framework's own competition rules. Emergency procurements require immediate contact with the Commercial Helpdesk. The thresholds replace the 2023-24 thresholds, where FTS was GBP 138,760. The workbook was last updated on 1 April 2024, next review is 1 April 2025, and the owner is Head of Commercial Policy. Source: `UF-PROCUREMENT-THRESHOLDS-2024-25`.

Specific rubric: Full credit requires all five notes plus last updated, next review, and owner.

### Q063

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What is the scope of the Acceptable Use Policy and what limited personal use does it allow?

Gold answer: The policy applies to all users of DWP IT, including employees, contractors, agency staff, and secondees. DWP IT is provided for business purposes. Limited personal use is permitted only if it does not interfere with work duties, incur cost to the department, bring the department into disrepute, or breach any other DWP policy. Source: `UF-ACCEPTABLE-USE-POLICY-IT-SYSTEMS`.

Specific rubric: Full credit requires user scope and all four conditions for limited personal use.

### Q064

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What email, classification, personal email, and web-filtering rules are in the Acceptable Use Policy?

Gold answer: Official correspondence must use the user's `@dwp.gov.uk` email address. OFFICIAL is the default and needs no marking; OFFICIAL-SENSITIVE must be marked in the subject line; SECRET and above must not be sent by email and must use the secure network. Personal webmail such as Gmail, Hotmail, and Yahoo must not be accessed on DWP devices, and DWP data must never be sent to personal email addresses. Blocked websites include adult content, gambling, social media, streaming except approved platforms, and file sharing/cloud storage except approved services. Attempts to bypass filtering with VPNs, proxies, Tor, and similar tools are serious breaches and security incidents. Source: `UF-ACCEPTABLE-USE-POLICY-IT-SYSTEMS`.

Specific rubric: Full credit requires email address rule, all three classification treatments, personal webmail/data rule, and web-filtering/bypass caveat.

### Q065

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: Which stale or update-needed notes appear inside the Acceptable Use Policy?

Gold answer: It contains a note to check whether DWP fully migrated to M365 because some teams were still on on-prem Exchange as of March 2022. It says the Software Catalogue reference is outdated because the catalogue was decommissioned in 2023 and replaced by the Digital Marketplace. It notes the VPN client is being replaced by Zscaler Internet Access, with rollout beginning Q1 2023 and dual running depending on device build. It also says the June 2024 review has not taken place and the policy is overdue for update. Source: `UF-ACCEPTABLE-USE-POLICY-IT-SYSTEMS`.

Specific rubric: Full credit requires all four internal staleness/update signals.

### Q066

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What data protection responsibilities and sharing checks does the staff guidance set out?

Gold answer: Staff must only access personal data needed for their work, not share it with anyone who does not need it, keep it secure through locked screens/encrypted devices/secure email, report suspected breaches immediately, and complete mandatory data protection training annually. Before sharing personal data outside the department, staff must confirm a lawful basis, check whether a data sharing agreement is in place, use secure transfer methods, and record what was shared and with whom. Source: `UF-DATA-PROTECTION-GUIDANCE-FOR-STAFF-MARCH-2024`.

Specific rubric: Full credit requires at least four responsibilities and all four sharing checks.

### Q067

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What are the data breach and Subject Access Request handling rules?

Gold answer: All personal data breaches must be reported to the Data Protection Officer within 24 hours using the intranet breach reporting form. Serious breaches must be reported to the Information Commissioner's Office within 72 hours, handled by the DPO. Subject Access Requests must be forwarded immediately to the SAR team at `sar@dwp.gov.uk`; staff should not respond directly. The department has 30 calendar days to respond to a SAR from receipt. Source: `UF-DATA-PROTECTION-GUIDANCE-FOR-STAFF-MARCH-2024`.

Specific rubric: Full credit requires 24-hour DPO breach reporting, 72-hour ICO serious-breach rule, SAR team forwarding, do-not-respond-directly, and 30-calendar-day SAR deadline.

### Q068

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: Why should the Information Security Policy not be treated as final approved guidance?

Gold answer: It is marked `DRAFT - NOT FOR DISTRIBUTION`, version 0.8 draft, February 2024, and says it has not been approved for publication and should not be distributed outside the Information Security team. It includes reviewer notes, a TODO to update forced 90-day password expiry because NCSC guidance recommends against forced expiry, a placeholder for Cloud Security to be drafted, and an end note saying sections 5, 8, 9, and 10 are still to be written. Source: `UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8`.

Specific rubric: Full credit requires the draft/not approved status and at least three incomplete/TODO examples.

### Q069

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What incident reporting, MFA, BYOD, and training rules are in the draft Information Security Policy?

Gold answer: MFA is required for all remote access and for systems handling OFFICIAL-SENSITIVE or above. Personal devices must not access departmental systems or data unless through an approved BYOD solution, and no BYOD solution is currently approved. All security incidents must be reported to the SOC immediately. Severity levels are P1 active compromise or data breach affecting live services, P2 suspected compromise or actively exploited vulnerability, P3 security policy violation or minor vulnerability, and P4 advisory or informational. All staff must complete Responsible for Information training annually; staff with elevated access need additional role-specific security training. Source: `UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8`.

Specific rubric: Full credit requires MFA, BYOD, SOC immediate reporting, P1-P4 definitions, and annual RfI training.

### Q070

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What FOI exemptions and escalation routes are built into the FOI response template?

Gold answer: The template includes full disclosure, Section 21 information accessible by other means, Section 40(2) personal data, Section 35(1)(a) formulation or development of government policy with a public-interest argument, and Section 43(2) commercial interests. If dissatisfied, the requester can seek an internal review by writing to the FOI Internal Review Team at DWP, Caxton House, Tothill Street, London SW1H 9NA, or emailing `foi.internalreview@dwp.gov.uk`. If still dissatisfied, they may complain to the Information Commissioner's Office at Wycliffe House, Water Lane, Wilmslow, Cheshire SK9 5AF, `www.ico.org.uk`. Source: `UF-FOI-RESPONSE-TEMPLATE`.

Specific rubric: Full credit requires all four exemption sections and both internal review and ICO routes.

### Q071

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What social media accounts, permissions, and political-activity categories are in the DWP social media guidance?

Gold answer: Official accounts listed are Twitter/X `@DWPgovuk`, LinkedIn `Department for Work and Pensions`, Facebook `DWP`, and YouTube `DWP Digital`. Only authorised Communications Directorate staff may post for DWP. New departmental social media accounts require Head of Digital Communications approval. Political categories are: AA/AO politically free, may engage in most political activities with permission; Grade 7 and above politically restricted, no national political activity and limited local activity with permission; EO/HEO/SEO intermediate, may engage in some political activities with permission. The note says Twitter was rebranded to X in October 2023 and the handle remains `@DWPgovuk`. Source: `UF-SOCIAL-MEDIA-GUIDANCE-FOR-STAFF`.

Specific rubric: Full credit requires accounts, authorisation/new-account approval, all three political categories, and the Twitter-to-X caveat.

### Q072

Category: Data protection, information security, FOI, social media, and whistleblowing

Question: What counts as a qualifying whistleblowing disclosure, and what are the main channels and timescales?

Gold answer: Qualifying disclosures under PIDA include reasonable-belief information showing a criminal offence, failure to comply with a legal obligation, miscarriage of justice, danger to health or safety, environmental damage, or deliberate concealment of any of those. Personal employment matters such as pay, grading, or workload should use the Grievance Policy. Preferred internal channels are line manager, Nominated Officer, HR Casework Team, Counter Fraud Team, and the confidential Raising Concerns helpline. External channels include the NAO, relevant regulator such as the ICO, or an MP. Concerns are acknowledged within 5 working days, investigations aim to complete within 60 working days, and records are retained for 7 years. Source: `UF-RAISING-CONCERNS-WHISTLEBLOWING-GUIDANCE`.

Specific rubric: Full credit requires all six disclosure categories, grievance distinction, internal/external channels, and 5-day/60-day/7-year timings.

### Q073

Category: People policies and operational procedures

Question: What annual leave entitlements and carry-over rules are in the DWP Annual Leave Policy?

Gold answer: AA/AO and EO staff get 23 days under 1 year and 1-2 years, 24 days for 2-5 years, 25 days for 5-10 years, and 30 days for 10+ years. HEO/SEO get 25, 25, 25, 27, and 30 days across those bands. Grade 7/6 get 25, 25, 27, 27, and 30. SCS get 30 days in all bands. All staff also get 8 public holidays and 1 privilege day for the King's Birthday. Up to 5 unused days may be carried over and must be used by 30 June; exceptional additional carry over may be approved by a Grade 6. Source: `UF-ANNUAL-LEAVE-POLICY`.

Specific rubric: Full credit requires grade/service entitlements, public holidays/privilege day, 5-day carry-over, 30 June deadline, and Grade 6 exception.

### Q074

Category: People policies and operational procedures

Question: What formal grievance process and timescales does the Grievance Policy set out?

Gold answer: Step 1 is written submission to the line manager, or manager's manager if the grievance is about the line manager. Step 2 is investigation and a grievance hearing within 15 working days, with the right to be accompanied by a trade union representative or colleague. Step 3 is a written decision within 10 working days of the hearing. Step 4 is appeal in writing within 10 working days; the appeal is heard by a manager at least one grade higher than the original decision maker. Appeal hearing is within 15 working days of appeal submission and appeal decision within 10 working days of the appeal hearing. Where a grievance overlaps with disciplinary process, the disciplinary process normally takes precedence and the grievance is paused. Source: `UF-GRIEVANCE-POLICY-2024`.

Specific rubric: Full credit requires all four steps, all timescales, accompaniment right, higher-grade appeal, and disciplinary-overlap rule.

### Q075

Category: People policies and operational procedures

Question: What does the Performance Management Framework require for objectives, conversations, ratings, and moderation?

Gold answer: It applies to AA to Grade 6, while SCS uses a separate Cabinet Office framework. The performance year is 1 April to 31 March, and agreements must be in place by 30 April. Each employee must have 3 to 5 SMART objectives, with at least one development objective and at least one aligned to the directorate business plan. There must be at least 4 formal conversations: objective setting in April, mid-year review in October, end-of-year review in March, and a development conversation at any time. Ratings are Exceeded, Met, and Not Met; `Must Improve` was removed in 2023-24. Ratings are moderated at directorate level by panels chaired by SCS1 or above, with expected distribution guidelines of about 25 percent Exceeded, 65-70 percent Met, and 5-10 percent Not Met, not quotas. Source: `UF-PERFORMANCE-MANAGEMENT-FRAMEWORK-2024-25`.

Specific rubric: Full credit requires scope, dates, objective rules, four conversations, three ratings plus removed rating, and moderation/distribution caveat.

### Q076

Category: People policies and operational procedures

Question: What Improving Performance, pay, and appeal rules does the Performance Management Framework describe?

Gold answer: Improving Performance has Stage 1 Support Plan for 8 weeks, Stage 2 Formal Review for 8 weeks, and Stage 3 Final Review for 4 weeks, after which dismissal or redeployment may be considered. Employees can be accompanied by a trade union representative or colleague, and records must be kept. Pay outcomes are: Exceeded can get a non-consolidated GBP 1,000 performance payment if applicable; Met gets standard pay progression if not at top of band; Not Met gets no pay progression and no performance payment. Appeals must be made within 10 working days and completed within 20 working days. Where performance appeal and grievance timelines conflict, the longer performance appeal timeline takes precedence. Source: `UF-PERFORMANCE-MANAGEMENT-FRAMEWORK-2024-25`.

Specific rubric: Full credit requires all three stages/durations, accompaniment and records, all three pay outcomes, and appeal timing/conflict rule.

### Q077

Category: People policies and operational procedures

Question: What does the DWP Flexible Working Policy say about hybrid attendance, request handling, core hours, and home equipment?

Gold answer: The standard expectation is at least 60 percent office attendance, so a full-time employee working 5 days spends at least 3 days in the office. Some roles require higher attendance; different local arrangements must be documented and approved by the relevant Grade 6. Requests are discussed informally, submitted through HR Online, answered within 28 days, confirmed in writing if approved, and subject to a 3-month trial for all new arrangements. Core hours are 10:00 to 12:00 and 14:00 to 16:00, Monday to Friday. Home workers are entitled to a department laptop, monitor on request, keyboard and mouse on request, and desk assessment, but office furniture is not provided except where occupational health recommends it. Source: `UF-FLEXIBLE-WORKING-POLICY`.

Specific rubric: Full credit requires 60 percent/3 days, Grade 6 caveat, 28 days, 3-month trial, core hours, and equipment/furniture rules.

### Q078

Category: People policies and operational procedures

Question: What approval is needed before advertising DWP vacancies by grade?

Gold answer: AA to EO vacancies require Grade 7 budget holder approval and confirmation of budget allocation. HEO to SEO require Grade 6 approval and a one-page business case. Grade 7 requires SCS1 Director approval with business case and Workforce Planning approval. Grade 6 requires SCS2 Director General approval with business case and ExCo notification. SCS requires Permanent Secretary approval with business case and Cabinet Office approval. Source: `UF-RECRUITMENT-AND-SELECTION-POLICY`.

Specific rubric: Full credit requires all five grade bands, approvers, and extra requirements.

### Q079

Category: People policies and operational procedures

Question: What recruitment panel, clearance, and record-retention requirements are stated?

Gold answer: Panels are: AA to EO, 2 members with at least one trained interviewer; HEO to SEO, 2 members with chair at least one grade above vacancy; Grade 7 to Grade 6, 3 members with SCS chair and at least one external panel member for Grade 6; SCS, 3-4 members with Civil Service Commissioner oversight and independent panel member. All panel members need unconscious bias training within the last 2 years. Clearances are BPSS for most DWP roles, 1-2 weeks; SC for sensitive systems, 6-8 weeks; DV for TOP SECRET material, 6-9 months. Records are kept 12 months after vacancy closes for unsuccessful candidates, duration of employment plus 6 years for successful candidates, and psychometric results for 2 years only. Source: `UF-RECRUITMENT-AND-SELECTION-POLICY`.

Specific rubric: Full credit requires panel rules, unconscious bias training, clearance timings, and retention periods.

### Q080

Category: People policies and operational procedures

Question: Why is the Travel and Subsistence Policy flagged, and what are its key rates?

Gold answer: It is version 2.0, dated April 2021, owned by People Services, with next review April 2022, so it is flagged as past review. Standard class rail is default; first class may be used where the journey is over 3 hours and the traveller needs to work. Car mileage is 45p per mile for the first 10,000 miles and 25p thereafter; motorcycle is 24p per mile. Subsistence rates are GBP 4.50 breakfast, GBP 4.50 lunch, GBP 12.50 evening meal, London overnight up to GBP 120, elsewhere up to GBP 75. Claims must be submitted within 2 months, and receipts are required for items over GBP 10. Source: `UF-TRAVEL-AND-SUBSISTENCE-POLICY-V2-0`.

Specific rubric: Full credit requires the past-review caveat and all travel, subsistence, claim, and receipt values.

### Q081

Category: People policies and operational procedures

Question: What incident reporting timeframes and retention rules are in the Incident Reporting Procedure?

Gold answer: Minor first-aid-only incidents require the online form the same day. Moderate medical-treatment incidents require the online form plus line manager notification within 2 hours. Major hospital-admission incidents require the online form plus phone notification to the H&S team immediately. Fatal or specified injuries require those steps plus a RIDDOR report immediately. Investigations are due in 5 working days for minor, 10 working days for moderate, and 15 working days for major/RIDDOR. Incident records must be kept at least 3 years; RIDDOR records at least 3 years from the incident, though some legal advisers recommend 6 years. Source: `UF-INCIDENT-REPORTING-V1`.

Specific rubric: Full credit requires all four severity actions/timeframes, investigation durations, and retention caveat.

### Q082

Category: People policies and operational procedures

Question: What are the key Budgeting Loan eligibility, amount, repayment, and review rules?

Gold answer: Budgeting Loans are interest-free loans for people who have received a qualifying benefit for at least 26 weeks. Qualifying benefits are Income Support, income-based JSA, income-related ESA, and Pension Credit. Minimum loan is GBP 100. Maximum is GBP 348 for a single claimant, GBP 464 for a couple without children, and GBP 812 for a claimant or couple with children. Outstanding Social Fund debt is deducted from the maximum. Repayment is by deduction from the qualifying benefit, normally 12 percent of applicable amount, or 5 percent where hardship would result, over up to 104 weeks. Decisions can be reviewed by a Social Fund Inspector if requested within 28 days. The source warns these are 2018 rates that have not been uprated, but the latest rates circular should still be checked. It also warns Budgeting Loans are being replaced by Budgeting Advances under Universal Credit and should not be used for UC Budgeting Advance decisions. Source: `UF-SOCIAL-FUND-BUDGETING-LOANS-GUIDANCE-CHAPTER12`.

Specific rubric: Full credit requires eligibility, benefits list, min/max amounts, debt deduction, repayment rates/period, 28-day review, 2018-rates caveat, and UC caveat.

### Q083

Category: Overpayment, Social Fund, and staff-directory dark data

Question: What overpayment recovery rates are listed for Universal Credit, JSA/ESA/Pension Credit, Housing Benefit, PIP/DLA, Child Benefit, and Tax Credits?

Gold answer: Universal Credit standard recovery is 15 percent of standard allowance, maximum 25 percent, hardship 5 percent. JSA, ESA, and Pension Credit use GBP 11.10 per week standard, GBP 22.20 maximum, GBP 3.70 hardship. Housing Benefit recovery varies by local authority and is recovered by the local authority, not DWP. PIP/DLA cannot be recovered from directly and must use another benefit or direct recovery. Child Benefit cannot be recovered from directly; recovery is via HMRC. Tax Credits are HMRC responsibility, not DWP. Source: `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`.

Specific rubric: Full credit requires the UC percentages, fixed JSA/ESA/PC amounts, and correct responsibility/cannot-recover caveats.

### Q084

Category: Overpayment, Social Fund, and staff-directory dark data

Question: What are the overpayment escalation thresholds, and what known error is flagged?

Gold answer: GBP 0-65: write off below cost of recovery, Team Leader, immediate. GBP 65.01-500: standard recovery from benefits, Decision Maker, within 28 days of overpayment decision. GBP 501-5,000: standard recovery plus direct earnings attachment if no benefit in payment, HEO, within 28 days. GBP 5,001-10,000: above plus consider civil court action, SEO, review at 90 days. GBP 10,001-50,000: above plus mandatory referral to Debt Enforcement, Grade 7, review at 60 days. GBP 50,001-100,000: senior management review plus potential fraud referral, G6, immediate review. Over GBP 100,000: Director approval required for recovery strategy, SCS1, immediate. Over GBP 1 million: Director General plus HMT referral, immediate; the action column is missing and should read `Full recovery strategy and ministerial briefing`. Source: `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`.

Specific rubric: Full credit requires all thresholds/authority levels and the missing-action known error.

### Q085

Category: Overpayment, Social Fund, and staff-directory dark data

Question: How does the overpayment workbook distinguish fraud, claimant error, official error, and technical overpayments?

Gold answer: Civil fraud means the claimant knowingly provided false information and uses maximum recovery rate plus a civil penalty of 50 percent of the overpayment, minimum GBP 350 and maximum GBP 5,000, with 6 years from overpayment decision. Criminal fraud is as above but referred for prosecution, using a court compensation order plus ongoing recovery, with 6 years from conviction. Claimant error means failure to report a change without fraudulent intent, standard recovery rate, 6 years from overpayment decision. Official error means DWP made a mistake, and recovery is only where the claimant could reasonably have been expected to know they were overpaid; DWP's position is 6 years, but Upper Tribunal decisions in 2022 and 2023 cast doubt, so the Court of Appeal case expected Q2 2024 should be awaited before relying on the table. Technical overpayment means system error, case-by-case assessment, no fixed policy, legal advice required. Source: `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`.

Specific rubric: Full credit requires definitions, recovery approach, limitation periods, and the official-error legal uncertainty caveat.

### Q086

Category: Overpayment, Social Fund, and staff-directory dark data

Question: What overpayment payment methods, minimum amounts, and contact details are listed?

Gold answer: Deduction from ongoing benefit has no minimum and is the preferred automatic method. Direct Debit minimum is GBP 1 per month via Debt Management helpline. Standing Order minimum is GBP 1 per month. Online payment by GOV.UK Pay minimum is GBP 5 at `go.to/repay-benefit-overpayment`. Telephone card payment minimum is GBP 5 via the Debt Management helpline. Cheque minimum is GBP 5, payable to DWP Debt Management, but cheques are being phased out with target removal December 2024. Direct Earnings Attachment has no minimum and needs no court order for benefit debts. Court order/County Court Judgment has no minimum, is a last resort, and requires legal authorisation. Contact details are Debt Management Helpline `0800 XXX XXXX`, Monday to Friday 08:00-18:00, and `debt.management@dwp.gov.uk`. Source: `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`.

Specific rubric: Full credit requires method minimums, cheque phase-out, DEA/CCJ caveats, and helpline/email/hours.

### Q087

Category: Overpayment, Social Fund, and staff-directory dark data

Question: What quality and update caveats does the overpayment workbook include?

Gold answer: It says the GBP 65 threshold was set in 2009, has never been uprated, is approximately GBP 45 in 2009 prices, and an NAO-recommended review from 2019 has not been actioned. The GBP 1 million threshold row is missing action text, which should be `Full recovery strategy and ministerial briefing`. The contact sheet says the document was last updated in November 2023; UC recovery rates are updated each April in line with the standard allowance; JSA/ESA/Pension Credit fixed rates are updated annually; and the shown rates are 2023-24 rates. Source: `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`.

Specific rubric: Full credit requires all three caveat clusters: GBP 65 stale threshold, GBP 1 million missing action, and 2023-24 rate/update warning.

### Q088

Category: Overpayment, Social Fund, and staff-directory dark data

Question: What does the staff-directory source say about synthetic status, missing data, grade formats, and refresh date?

Gold answer: The wiki flags `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023` as a synthetic staff-directory fixture, so entries should not be treated as real personal data. The notes say the extract is from the HR system as at 31 December 2023 and may not reflect recent moves or new starters. Some entries have missing data because the HR system allows blank fields. Grade formats are inconsistent due to a 2022 system migration. Names are in `Surname, Initial` format except where the source used full names. It was last refreshed on 5 January 2024. Sources: `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023`, `challenge-2/wiki/lint-report.md`, `challenge-2/AGENTS.md`.

Specific rubric: Full credit requires synthetic fixture caveat, HR extract date, missing-data note, grade-format reason, name-format note, and refresh date.

### Q089

Category: Overpayment, Social Fund, and staff-directory dark data

Question: In the staff directory, who holds the Director Digital Services, Deputy Director Financial Control, and Head of Disability Policy roles?

Gold answer: `Khan, F` is SCS1 in Digital, London, with role `Director, Digital Services`. `Chen, L` is G6 in Finance, Leeds, with role `Deputy Director, Financial Control`. `Singh, P` is Grade 7 in Policy, London, with role `Head of Disability Policy`. Source: `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023`.

Specific rubric: Full credit requires all three names, grades/directorates or locations, and roles, plus the staff-directory source citation.

### Q090

Category: Overpayment, Social Fund, and staff-directory dark data

Question: Which staff-directory entries contain missing name, grade, email, or phone fields?

Gold answer: `Patel, A` has no phone number. `Williams, S` has no email address. The Policy Adviser row has no name but has email `m.johnson@dwp.gov.uk`. `Brown, D` has no grade. Source: `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023`.

Specific rubric: Full credit requires all four missing-field cases and identifies which field is missing.

### Q091

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What is the Welsh Language Standards compliance summary for 2022-23?

Gold answer: Total standards: 148. Fully compliant: 129, or 87 percent. Partially compliant: 14, or 9 percent. Non-compliant: 5, or 3 percent. By category: service delivery 84 standards with 71 fully compliant, 9 partially compliant, 4 non-compliant; policy making 18 with 16 fully compliant, 2 partially compliant, 0 non-compliant; operational 34 with 30 fully compliant, 3 partially compliant, 1 non-compliant; record keeping 12 with 12 fully compliant, 0 partially compliant, 0 non-compliant. Source: `UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023`.

Specific rubric: Full credit requires total compliance figures and category breakdown.

### Q092

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What Welsh Language Standards non-compliance, complaints, and Welsh-speaking staff figures are reported?

Gold answer: Telephone services: 4 helplines lacked Welsh language option: Universal Credit, Disability benefits, Carer's Allowance, and Debt Management. A note says UC and Debt Management remained non-compliant as of March 2024 and missed the September 2023 target. Digital services launched without Welsh versions were UC journal messaging and PIP online claim tracking, both later delivered in January and March 2023. Three Jobcentres had English-only signage: Rhyl, Bangor, and Aberystwyth, rectified by April 2023. DWP received 23 complaints: 14 telephone, 5 correspondence in English only, 3 digital services, and 1 Jobcentre Plus site; all were resolved within 20 working days and 2 were notified to the Welsh Language Commissioner for formal investigation. As at 31 March 2023, DWP employed 3,247 staff in Wales, 412 or 12.7 percent self-reported Welsh speakers, 186 or 5.7 percent in Welsh-essential posts, and 89 or 2.7 percent in Welsh-desirable posts. Source: `UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023`.

Specific rubric: Full credit requires telephone, digital, signage, complaint, and staff-language figures, including missed-target caveat.

### Q093

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What costs and forward-plan caveats are in the Welsh Language Standards report?

Gold answer: Total Welsh language compliance expenditure for 2022-23 was GBP 1,247,000: translation services GBP 489,000; bilingual signage and print GBP 67,000; Welsh language training GBP 31,000; Welsh language adviser salaries GBP 412,000; digital service localisation GBP 198,000; other GBP 50,000. Plans for 2023-24 included full telephone-service compliance by December 2023, Welsh chatbot pilot subject to GOV.UK App development, 15 percent more Welsh-essential posts, and simultaneous publication of new policy documents in Welsh and English. The report notes several 2023-24 targets have passed their deadlines and that the 2023-24 compliance report was expected by March 2025 but had not yet been published. Source: `UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023`.

Specific rubric: Full credit requires total and category costs, plan items, and the missed-deadline/unpublished-report caveat.

### Q094

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What groups does the UC Migration Equality Impact Assessment identify as differentially affected, and what source-status caveats apply?

Gold answer: The assessment says managed migration differentially affects disabled claimants, claimants over State Pension age, women, and ethnic minority claimants. It covers migration from Income Support, income-based JSA, income-related ESA, Housing Benefit, Child Tax Credit, and Working Tax Credit to UC. It says the programme, known as Move to UC, was expected to complete by March 2025, but includes a note that this was the target at the time of writing and the programme has since been extended, so the latest timeline should be checked. Source: `UF-EQUALITY-IMPACT-ASSESSMENT-UC-MIGRATION`.

Specific rubric: Full credit requires all four affected groups, legacy benefits list, Move to UC, March 2025 target, and extension caveat.

### Q095

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What disability, sex, race, and mitigation details are in the UC Migration Equality Impact Assessment?

Gold answer: Disabled claimants on ESA Support Group transition to LCWRA with transitional protection so they do not receive less in cash terms at migration, but the LCWRA element, GBP 390.06 per month, is lower than ESA Support Group plus disability premium, transitional protection erodes as UC rates uprate, and UC work capability assessment differences may cause anxiety. Women are disproportionately affected by childcare-support calculation changes, the two-child limit for UC but not legacy Child Tax Credit claims before April 2017, and monthly assessment periods. Some ethnic minority claimants may face digital literacy/access, language, and cultural barriers to work-coach engagement; translation and face-to-face support exist but take-up is uneven. The mitigations section is incomplete and references an Annex C that was not included. Source: `UF-EQUALITY-IMPACT-ASSESSMENT-UC-MIGRATION`.

Specific rubric: Full credit requires disability, sex, race/ethnicity details and the incomplete Annex C caveat.

### Q096

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What programme status metrics and actions are in the UC Managed Migration Programme Board minutes?

Gold answer: Overall RAG status was AMBER, unchanged from January. January migration notices were 12,400 against a 15,000 target; cumulative total since programme start was 247,000. Completion rate was 78 percent within 3 months against an 85 percent target. Migration Helpline call volumes were up 34 percent from December, with average wait time 22 minutes against a 10-minute target. The programme was 4 months behind the published March 2025 completion date. Key actions included `23/47` data quality audit for cohort 3 still open and due end February, `24/03` SRO to present a rebaselined plan at the March board, `24/04` Finance BP to confirm whether helpline pressure is one-off or recurring, `24/05` Legal to assess judicial review risk by 28 February 2024, and `24/06` SRO to scope an independent assurance review. Source: `UF-PROGRAMME-BOARD-MINUTES-14-FEB-2024`.

Specific rubric: Full credit requires RAG, notice/completion/call metrics, 4-month delay, and at least four action references with owners or due points.

### Q097

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What finance, risk, and AOB points are recorded in the UC Managed Migration Programme Board minutes?

Gold answer: Q3 spend was GBP 47.2 million against GBP 52.1 million budget, a GBP 4.9 million underspend mainly due to delayed IT releases. Q4 forecast was GBP 58.3 million against GBP 54.0 million, a GBP 4.3 million pressure driven by helpline demand. Full-year forecast was GBP 193.5 million against GBP 198.0 million, a GBP 4.5 million underspend. Risk R-0023 on IT system capacity during peak migration had been on the register for 18 months without mitigation progressing because a planned infrastructure upgrade was descoped from the Q3 release due to Fraud Detection project priorities. A new potential judicial review risk from a disability rights organisation was raised. AOB recorded the March meeting moved to 13 March to avoid the PAC hearing, a BBC Panorama programme scheduled for March, and no objection to commissioning an independent assurance review. Source: `UF-PROGRAMME-BOARD-MINUTES-14-FEB-2024`.

Specific rubric: Full credit requires Q3/Q4/full-year finance figures, IT capacity risk, judicial review risk, and the three AOB points.

### Q098

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: What should an answer say about the Ministerial Questions briefing's OCR quality and Universal Credit processing-time data?

Gold answer: The source is marked OFFICIAL-SENSITIVE and low OCR quality; it warns the scanned text may be incorrectly recognised. The date appears as `12 March 2O24` with letter O in the OCR text, and some months also show `2O23` or `2O24`. Question 1 asks about average processing time for new UC claims over the last 12 months. The listed average days to first payment are: Mar 2023 31, Apr 2023 29, May 2023 28, Jun 2023 30, Jul 2023 32, Aug 2023 33, Sep 2023 30, Oct 2023 28, Nov 2023 27, Dec 2023 35, Jan 2024 31, Feb 2024 29. The target is 95 percent of new claims paid within 5 weeks, or 35 calendar days. The December figure reflects seasonal staffing pressures. The remainder of the document, 14 further questions, was not extracted due to OCR quality, and manual review is recommended. Source: `UF-MINISTERS-QUESTIONS-BRIEFING-PACK-12MARCH`.

Specific rubric: Full credit requires the low-OCR caveat, all 12 monthly values, the 95 percent/35-day target, December caveat, and manual-review warning.

### Q099

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: Which sources mention Discretionary Housing Payments according to the topic page?

Gold answer: The Discretionary Housing Payments topic page lists five sources: `DOC-HB-001`, `DOC-HB-002`, `DOC-HB-005`, `DOC-HB-008`, and `UF-PROGRAMME-BOARD-MINUTES-14-FEB-2024`. Source: `challenge-2/wiki/topics/discretionary-housing-payments.md`.

Specific rubric: Full credit requires all five source IDs and the topic-page citation.

### Q100

Category: Welsh language, UC migration, OCR, statistics, and source-risk synthesis

Question: If an agent is asked to answer from the wiki, which source-risk caveats should it actively preserve rather than smooth over?

Gold answer: It should preserve the wiki's explicit risk caveats: `DOC-HB-003` is stale/conflicted because `DOC-HB-009` replaces the March 2024 CTR guidance; `DOC-HB-006` is superseded and points to `DOC-HB-006a`; `UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8` is draft and not approved; `UF-STAFF-DIRECTORY-EXTRACT-Q4-2023` is a synthetic staff-directory fixture; `UF-TRAVEL-AND-SUBSISTENCE-POLICY-V2-0` is past review with next review April 2022; `UF-MINISTERS-QUESTIONS-BRIEFING-PACK-12MARCH` has low OCR quality and incomplete extraction; `UF-EQUALITY-IMPACT-ASSESSMENT-UC-MIGRATION` has incomplete mitigations and a missing Annex C; `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3` contains known errors and out-of-date rates caveats; and the Welsh Language Standards report contains missed-target/unpublished-follow-up caveats. Sources: `challenge-2/wiki/lint-report.md`, `DOC-HB-009`, `UF-MINISTERS-QUESTIONS-BRIEFING-PACK-12MARCH`, `UF-EQUALITY-IMPACT-ASSESSMENT-UC-MIGRATION`, `UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3`, `UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023`.

Specific rubric: Full credit requires at least the five lint-report flags plus OCR, missing-annex, overpayment known-error/update, and Welsh missed-target caveats. Cap at 3 if the answer only says "some sources are stale" without source IDs.
