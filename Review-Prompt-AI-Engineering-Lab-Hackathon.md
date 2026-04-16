---
title: Deep Research Prompt - AI Engineering Lab Hackathon London 2026
tags: [ai, hackathon, deep-research, public-sector, obsidian, markdown]
aliases: [Hackathon Deep Research Prompt, Published Repo Research Prompt]
---

# Deep Research Prompt - AI Engineering Lab Hackathon London 2026

## Purpose

Use this prompt to produce a new, source-grounded research report for the published `ai-engineering-lab-hackathon-london-2026` repository.

This is an updated prompt for the published challenge pack. Do not rely on earlier assumptions that the repository only contained a README-level event brief. The repository now includes detailed challenge briefs, an open-brief guide, a setup guide, and starter data for several challenges. Your research should start from that published state, verify it, and then assess what it means for organisers, facilitators, judges, attendees and follow-on training.

## Role

You are conducting a **full, source-grounded deep research review** of the published AI Engineering Lab Hackathon London 2026 repository, its four challenge briefs, the open-brief option, the available starter data, the attendee landscape if supplied, and the wider public-sector AI engineering and digital delivery context.

Your job is to produce:

1. an **illustrated report** suitable for senior civil servants, organisers, facilitators, Forward Deployed Engineers, judges and technical leads
2. a **structured, extensively linked Markdown knowledge base** that works well in **Obsidian**, and still reads cleanly in **VS Code** and **GitHub**
3. a **verified set of Mermaid diagrams** that render correctly in those contexts, with static fallbacks where needed
4. a **practical view of how AI coding assistants can support attendees before, during and after the hackathon**, including how that support can become part of repeatable training
5. a **clear assessment of what the published repository now provides**, what gaps remain, and what should be added before or after the event

## Primary inputs

Use these as the starting corpus:

- the published `ai-engineering-lab-hackathon-london-2026` repository
- the repository's commit history and remotes, including the public upstream repository where available
- `README.md`, including event framing, day structure, judging model, AI-tool guidance and materials list
- `SETUP-GUIDE.md`, including pre-event setup, AI coding tool assumptions, device requirements and submission guidance
- `open-brief.md`, including open-brief scoping rules and prompts
- the four published challenge briefs:
  - `challenge-01-from-pdf-to-digital-service.md`
  - `challenge-02-unlocking-the-dark-data.md`
  - `challenge-03-supporting-casework-decisions.md`
  - `challenge-04-knowing-your-own-organisation.md`
- the starter data in:
  - `challenge-1/FORM-LIC-001-licence-application.pdf`
  - `challenge-2/structured_files/`
  - `challenge-2/unstructured_files/`
  - `challenge-3/cases.json`
  - `challenge-3/policy-extracts.json`
  - `challenge-3/workflow-states.json`
  - `challenge-4/workforce.json`
  - `challenge-4/tickets.json`
  - `challenge-4/org-chart.json`
  - `challenge-4/index.html`
- the AI Engineering Lab repository linked from the published README, and any directly relevant sibling repositories that materially illuminate intent, delivery approach, standards, training or repeatable use of AI coding assistants
- attendee-domain data, attendee organisation mappings, or participant lists if supplied alongside the research task
- current official UK Government guidance relevant to digital service delivery, accessibility, AI adoption, algorithmic transparency, security, privacy, procurement, open standards, service assurance and technology assurance
- publicly available evidence of AI, automation, algorithmic-tool or digital transformation activity in the participating public bodies, where such evidence exists

If an input is referenced but not available, state that clearly. Do not fabricate attendee bodies, internal organiser intent, unpublished repository contents or unverified deployments.

## Published repository baseline to verify

Treat the following as the updated starting baseline. Verify each item against the repository and commit history before relying on it:

- The published repository is a complete hackathon starter pack, not just an initial README.
- It contains a top-level event README, setup guide, open-brief guide, four detailed challenge briefs and starter data.
- The README frames the event as a one-day hackathon for engineers in the AI Engineering Lab community, focused on building working prototypes while using AI coding tools throughout the software delivery workflow.
- The event is explicitly about **how AI coding tools change the way teams work**, not only about embedding AI into the prototype.
- The event does **not** provide central access to AI model APIs for prototypes. Teams may use their own departmental or personal access, local models, or mocked AI capabilities.
- The event is tool-agnostic across AI coding assistants, naming GitHub Copilot, Amazon Kiro, Gemini Code Assist and similar tools as examples.
- Four challenge briefs are published:
  - **Challenge 1: From PDF to digital service**
  - **Challenge 2: Unlocking the dark data**
  - **Challenge 3: Supporting casework decisions**
  - **Challenge 4: Knowing your own organisation**
- The repository also encourages teams to bring an **open brief**, provided it is achievable as a working one-day prototype and uses open or synthetic data.
- Judging combines milestone progress during the day with table-based judge review. There are no stage presentations for every team; the top finalists present near the end.
- Each team has support from a Version 1 Forward Deployed Engineer.
- Challenge 1 provides a sample licence-application PDF.
- Challenge 2 provides both structured text-based documents and unstructured binary-format documents.
- Challenge 3 provides synthetic case, policy and workflow JSON.
- Challenge 4 provides synthetic workforce, ticket and organisation data, plus a starter `index.html`.

Where the evidence is partial, stale or ambiguous, say so plainly. If repository versions or files have changed since this prompt was written, prefer the repository's current state and record the difference.

## Research objectives

### 1) Full published repository review

Conduct a complete review of the hackathon repository and directly relevant linked or sibling repositories.

Assess:

- what is present in the published pack
- what has changed since the initial repository state
- what is absent from the published pack
- what is implied but not yet supplied
- what is reusable as-is by attendees, facilitators and organisers
- what needs to be added before the event if organisers want a stronger participant experience
- what is especially useful for attendees who are newer to AI coding assistants
- what will support repeatable training after the event

Produce a maturity assessment covering:

- challenge design
- repo structure
- onboarding and setup
- starter data quality and coverage
- open-brief support
- standards and assurance coverage
- accessibility support
- privacy, security and data-handling guidance
- judging readiness
- milestone tracking readiness
- facilitator and FDE support
- team submission process
- training value
- post-event reusability

### 2) Deep review of the four published challenges

For each official challenge, produce a full review and a practical delivery frame.

The four published challenges are:

1. **From PDF to digital service**
2. **Unlocking the dark data**
3. **Supporting casework decisions**
4. **Knowing your own organisation**

For **each challenge**, answer at minimum:

- What precise public-sector problem is this challenge trying to solve?
- Which users matter most? Distinguish external users, frontline staff, operational managers, policy teams, technical teams and senior leaders where relevant.
- What public-sector bodies in the attendee group, if attendee data is available, are most likely to care about this challenge, and why?
- What analogous services, records, processes, forms, document sets or operational workflows already exist in the public domain?
- What starter data is supplied in the repository?
- What additional open or synthetic data could support a one-day prototype safely?
- What is the minimum viable prototype that could credibly be built in one day?
- What architectures are plausible for a demoable prototype?
- Which parts of the work are best accelerated by AI coding assistants?
- Which parts must stay strongly human-led?
- What are the main delivery risks: accessibility, privacy, bias, hallucination, security, procurement, governance, operational risk, misuse, unsupported automation, poor data quality or misleading analytics?
- Which official standards, policies and assurance artefacts are most relevant?
- How should success be measured during the event and after the event?
- What would a good judge expect to see in a demo?
- What should a good "next 30/90/180 day" follow-on roadmap look like?

For each challenge, produce:

- a concise strategic summary
- a detailed research note
- a prototype options paper with 2 to 4 credible implementation patterns
- a starter-data assessment
- a standards and assurance checklist
- a suggested one-day build plan
- a suggested evidence pack for judging
- a suggested facilitator/FDE intervention guide
- a suggested training note showing how AI coding assistants can help on that challenge specifically

### 3) Assess the open brief route

Review `open-brief.md` as its own pathway, not as an appendix.

Assess:

- whether the open-brief guidance is clear enough for teams to bring real problems safely
- how well it enforces user-centred problem framing
- whether the "before 10:00" facilitator check is operationally sufficient
- how open-brief teams should be judged consistently against teams using the four official challenges
- what additional templates, examples or guardrails would reduce risk
- what kinds of open-brief problems are likely to work well in one day
- what kinds of problems should be redirected, narrowed or rejected
- how open-brief teams should handle data protection, synthetic data, official-sensitive material and production system access

Produce an open-brief assessment note, a triage checklist for facilitators, and three to five safe example open-brief patterns.

### 4) Identify and assess additional future challenge briefs

From the wider repository ecosystem, AI Engineering Lab materials and public-sector digital delivery needs, identify **additional challenge themes** that would be valuable as optional future hackathon briefs, workshop modules or gameday exercises.

At minimum, assess whether the following should be carried forward as additional or future briefs:

- data processing and visualisation
- legacy modernisation
- security vulnerability assessment and remediation
- performance, resilience and operability
- adaptive testing and risk-based quality engineering
- multi-service architecture design
- production deployment and incident response
- standards/compliance copilot for UK government delivery
- AI landscape and horizon-scanning support for public-sector teams
- AI-assisted SDLC assurance and documentation pack generation

For each additional brief:

- define the problem clearly
- identify likely public-sector bodies or teams who would care
- explain whether it is suitable for a one-day prototype, a future gameday, a workshop module, or a follow-on training path
- explain how strongly it supports training in AI coding assistants
- note dependencies, assurance constraints, data barriers and facilitation needs

### 5) Build an attendee-centred public-sector AI application key

If attendee-domain data, attendee organisation mappings, or participant lists are supplied, use them to:

- identify participating public-sector bodies
- quantify attendee concentration by body and by sector
- group bodies into meaningful clusters
- map each body to its **likely priority AI application areas**
- distinguish between:
  - verified public evidence of existing AI or algorithmic-tool use
  - publicly stated AI priorities or strategies
  - reasoned opportunity areas based on remit and service model

Prioritise the bodies with the strongest attendee representation, but still include the full landscape.

Produce:

- a ranked body-by-body key
- a body-to-challenge fit matrix
- a sector heatmap
- a shortlist of "highest shared opportunity" themes across the attendee base
- a note on where common reusable prototype patterns could span multiple bodies

If attendee data is not available, produce a clearly marked placeholder method and explain what cannot be concluded without the data. Do not infer attendance from repository ownership alone.

### 6) Evaluate how AI coding assistants should be used in the hackathon and follow-on training

This is a central part of the work.

Analyse how AI coding assistants can support teams across the lifecycle:

- challenge understanding and scoping
- user-story generation
- repo setup
- architecture exploration
- code generation and refactoring
- data extraction and schema design
- test creation
- accessibility improvements
- documentation and README generation
- standards lookup and assurance prompts
- debugging
- demo preparation
- judging evidence capture
- reflective learning after the build

Compare the strengths, weaknesses and likely learning value of the tools named in the source material, plus any clearly relevant adjacent tools if justified by evidence.

The assessment must include:

- where assistants genuinely accelerate work
- where they create false confidence
- where novice users typically struggle
- how FDEs and facilitators can reduce wasted time
- how teams should capture evidence of tool use without making the event bureaucratic
- how organisers could turn hackathon activity into a repeatable training journey
- how to separate "AI used to build the prototype" from "AI embedded inside the prototype"
- how to handle mocked AI endpoints honestly in demos

Design a **training framework** that could be used:

- before the hackathon
- during the hackathon
- after the hackathon

Include practical assets such as:

- prompt patterns
- task decomposition patterns
- review checklists
- human-in-the-loop safeguards
- assistant anti-patterns and failure modes
- facilitation cues for FDEs and table judges
- evidence-capture templates
- suggested retrospective questions

## Standards, policy and assurance lens

Review all findings through the lens of current official guidance where relevant, including but not limited to:

- UK Government Service Standard
- GOV.UK Design System and GOV.UK Prototype Kit guidance
- accessibility requirements for public-sector websites and apps, including WCAG 2.2 expectations
- AI Playbook for the UK Government
- algorithmic transparency requirements and guidance
- data protection and privacy expectations
- cyber security and secure-by-design expectations
- government technology, open standards and technology code of practice guidance
- spend controls, commercial and procurement considerations where relevant
- AI life-cycle, governance and assurance expectations
- records management, information governance and knowledge-management expectations where relevant

Do **not** merely list standards. Show **how each standard changes what a good hackathon prototype should look like**.

Examples:

- For Challenge 1, show how GOV.UK form patterns and accessibility requirements affect flow design, validation, error summaries and confirmation pages.
- For Challenge 2, show how provenance, versioning and metadata affect whether extracted content can safely support search or question answering.
- For Challenge 3, show how human decision accountability, explainability and workflow auditability affect caseworker-support designs.
- For Challenge 4, show how data quality, privacy, aggregation, role-based access and senior-leader decision support affect workforce or operations dashboards.

## Research method

Use a method that is explicit, reproducible and audit-friendly.

### Source hierarchy

Prioritise sources in this order unless there is a strong reason not to:

1. repository contents and commit history
2. official UK Government publications and service manuals
3. official publications from participating bodies
4. official algorithmic transparency records and comparable public records
5. National Audit Office and equivalent high-trust public-sector analysis
6. reputable technical documentation and recognised expert sources
7. reputable reporting or commentary, used only where primary sources are unavailable and clearly labelled as secondary

### Evidence rules

- Mark every substantive claim as one of: **Verified fact**, **Publicly stated position**, **Reasoned inference**, or **Recommendation**.
- Never present inferred use cases as if they are verified live deployments.
- State clearly where no public evidence was found.
- Where sources disagree, summarise the disagreement.
- Note publication or update dates where recency matters.
- Record access dates for web sources.
- Quote sparingly. Prefer concise paraphrase with precise links.
- Use repository file paths and commit hashes when citing repository evidence.

### Suggested workflow

1. Catalogue the repository contents and commit history.
2. Read the README, setup guide, open brief, four challenge briefs and all starter data.
3. Create a source register and evidence ledger before drafting conclusions.
4. Review official standards and policy sources relevant to each challenge.
5. Review any supplied attendee data and map organisations to sectors and likely challenge fit.
6. Research public evidence for participating bodies only after the attendee list is established.
7. Draft challenge notes, repository review, training framework and standards analysis.
8. Build diagrams and matrices.
9. Validate Markdown links and Mermaid rendering.
10. Produce the final illustrated report and knowledge base.

## Required outputs

Create all research outputs in a dedicated folder such as `research-report/` or another clearly named output directory. Do not overwrite the published hackathon challenge materials unless explicitly asked.

## A. Illustrated report

Produce a polished illustrated report with:

- executive summary
- key findings
- published repository review
- challenge-by-challenge analysis
- open-brief assessment
- attendee landscape analysis, if attendee data is supplied
- AI coding-assistant training analysis
- standards and assurance view
- recommendations for organisers
- recommendations for facilitators, FDEs and judges
- recommendations for participating teams
- appendix of evidence and methods

The report should include diagrams, tables, heatmaps, matrices and callouts where useful.

## B. Obsidian / VS Code / GitHub Markdown knowledge base

Create a linked Markdown pack with a structure like this:

- `README.md`
- `00-Start-Here/`
- `01-Executive-Summary/`
- `02-Published-Repo-Review/`
- `03-Challenges/`
  - `Challenge-01-From-PDF-to-Digital-Service.md`
  - `Challenge-02-Unlocking-the-Dark-Data.md`
  - `Challenge-03-Supporting-Casework-Decisions.md`
  - `Challenge-04-Knowing-Your-Own-Organisation.md`
  - `Open-Brief-Assessment.md`
- `04-Attendee-Landscape/`
- `05-AI-Coding-Assistants/`
- `06-Standards-and-Assurance/`
- `07-Additional-Briefs/`
- `08-Methods-and-Sources/`
- `assets/diagrams/`
- `assets/images/`
- `data/`

### Markdown design requirements

Optimise for all three environments:

- **GitHub**: use relative Markdown links, readable tables, normal image embeds and code fences
- **VS Code**: keep folder/file names human-readable and predictable
- **Obsidian**: use YAML frontmatter, aliases, tags, maps-of-content, and backlinks-friendly structure

Use these conventions:

- every note has YAML frontmatter
- every major folder has an index/MOC note
- use relative Markdown links throughout
- where Obsidian-only features are used, provide a GitHub-safe fallback
- use callouts sparingly and only where they still read acceptably in GitHub
- include a glossary and acronym index
- include a source register and evidence ledger
- include "related notes" sections on long notes
- keep note titles stable and descriptive

## C. Mermaid diagrams

Create Mermaid diagrams that are **verified to render correctly** in GitHub, VS Code preview and Obsidian, or state clearly where a rendering environment could not be tested.

Use only Mermaid features that have been checked for compatibility.

At minimum include diagrams for:

- the overall research architecture
- the published repository structure
- the four challenge areas and their overlaps
- open-brief triage
- attendee clusters and body-to-challenge fit, if attendee data is supplied
- the AI-assisted hackathon workflow
- standards and assurance checkpoints through a one-day prototype lifecycle
- the post-hackathon training journey

Where a diagram is important, also provide a static SVG or PNG fallback in `assets/diagrams/`.

## D. Cross-linking and knowledge-management quality

The Markdown pack should feel like it was hand-crafted by a strong departmental knowledge-management team.

That means:

- clear navigation
- strong cross-linking
- no dead ends
- sensible naming
- consistent metadata
- concise summaries at the top of long notes
- reusable tables and comparison matrices
- notes that are readable on their own but stronger when traversed as a network
- explicit source links close to the claims they support

## Specific analyses to include

### Challenge comparison matrix

Create a matrix comparing all four official challenges, the open-brief route and any strong additional future briefs across:

- user value
- public-sector breadth
- attendee relevance, if attendee data is supplied
- one-day feasibility
- repository starter-data availability
- standards burden
- technical complexity
- risk level
- suitability for novice vs advanced teams
- suitability for demonstrating AI coding assistants well
- likely value for follow-on training

### Repository gap analysis

Create a gap analysis covering the published repository, including whether it should add:

- challenge-specific starter app templates
- per-challenge build checklists
- milestone definitions and dashboard schema
- judging rubrics
- judge question scripts
- evidence-capture templates
- prompt packs
- accessibility checklists
- data-protection and safe-data-use quick reference
- mocked AI endpoint examples
- team submission template
- facilitator runbooks
- post-event retrospective template
- reusable training modules

For every recommendation, distinguish between:

- must-have before the event
- useful before the event
- useful after the event
- future training asset

### Facilitation recommendations

Provide specific guidance for FDEs, facilitators and judges on:

- when to steer teams towards simpler prototypes
- when to push for stronger evidence of user need
- when to redirect teams away from unsafe data or production-system dependencies
- how to assess responsible use of AI coding assistants
- how to distinguish shallow demos from meaningful prototypes
- how to support teams using different assistant tools
- how to handle teams that want to embed live AI capabilities despite the event not providing model access
- how to score mocked AI capabilities fairly

### Training recommendations

Produce a repeatable training journey that uses the hackathon as evidence and practice, not just as a one-day event.

Include:

- pre-event preparation modules
- live event coaching patterns
- post-event review and consolidation
- advanced follow-on modules
- reusable prompt examples
- practical exercises mapped to each challenge
- suggested assessment criteria for AI-assisted software delivery skills

## Output quality bar

Your final output should be robust enough that organisers could:

- publish parts of it as event guidance
- use it to brief facilitators, FDEs and judges
- give it to teams as a pre-read
- use it to improve the published repository
- turn it into a reusable training pack for future cohorts

Do not optimise for superficial completeness. Optimise for:

- accuracy
- usefulness
- explicit evidence
- practical actionability
- clarity about uncertainty
- strong information architecture

## Final delivery checklist

Before finishing, confirm that the output includes:

- full published repository review
- commit-history and file-structure summary
- deep review of each of the four published challenges
- starter-data assessment for each relevant challenge
- open-brief assessment
- additional future brief recommendations
- attendee-centred public-sector AI application key, if attendee data is supplied
- clear placeholder and limitations note if attendee data is not supplied
- AI coding-assistant training and facilitation framework
- illustrated report
- linked Markdown knowledge base
- verified Mermaid diagrams with fallbacks where needed
- explicit distinction between fact, public statement, inference and recommendation
- source register and evidence ledger
- repository improvement recommendations grouped by timing and priority
