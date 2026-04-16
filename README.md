# AI Engineering Lab Hackathon

A one-day event where you work in a small team to build a working prototype that addresses a real cross-government challenge. You will use your AI coding tools throughout the day to plan, write, test, and present your solution.

This event is open to all engineers in the AI Engineering Lab community, whether your department is currently on the programme or not.

## What this is

This is not a competition to write the most code. It is about showing how AI tools change the way you work, and building something that could make a real difference to how government operates.

### AI coding tools and your application

You will use AI coding tools (GitHub Copilot, Amazon Kiro, Gemini Code Assist, or similar) to help you plan, write, and test your prototype. These tools assist your development process. The [AI Engineering Lab repository](https://github.com/govuk-digital-backbone/aiengineeringlab) has resources and guidance on getting the most from AI coding tools.

> The event does not provide access to AI models (such as large language model APIs) for use within your application.

If your team has access to models through your own department or personal accounts, or if you want to use locally hosted models, that is fine. You can also mock AI capabilities in your prototype. The focus is on what you build and how you use your coding tools to build it, not on embedding AI into the solution itself.

By the end of the day, your team will have:

- chosen a challenge and scoped a realistic solution
- built a working prototype using AI-assisted development
- reflected on how AI tools shaped your approach
- explained your work to a judging panel at your table

## The challenges

The four challenges below are examples drawn from real cross-government needs. They are provided to give your team a well-defined problem with starter data and hints. You are not required to use them. If your team has a problem from your own work that you would rather tackle, bring it.

Your solution should be demoable by the end of the day.

### Open brief

Teams are actively encouraged to bring their own problems. If you work with a process, a dataset, or a user experience that frustrates you or the people around you, this is a good opportunity to do something about it. The four challenges above are examples — you are not required to use them.

To propose an open brief, speak to a facilitator during the morning session before 10:00. Your problem must be achievable as a working prototype in one day and use open or synthetic data.

[Read the full open brief guidance — including prompts to help you frame your problem](open-brief.md)

### Challenge 1: From PDF to digital service

In many parts of government, official processes still rely on PDF forms: download, print, fill in by hand, scan, and post or email back. Citizens receive no confirmation, have no way to check status, and may find out weeks later that something was missing. The teams receiving those submissions handle them manually at every step.

This challenge is about the citizen and the caseworker on either side of that process — and what a genuinely better experience looks like for both. A good starting point if your team is newer to AI coding tools.

Use `challenge-1/FORM-LIC-001-licence-application.pdf` as the default sample form for this challenge.

[Read the full challenge brief](challenge-01-from-pdf-to-digital-service.md)

### Challenge 2: Unlocking the dark data

Government produces an enormous amount of guidance, policy, and procedural documentation. Most of it is published. Very little of it is genuinely findable. Citizens cannot get a direct answer to a specific question. Officials spend significant time locating guidance that exists somewhere but is not easily accessible. The GOV.UK App is building chat capabilities that depend on this content being structured — and right now, most of it is not.

This challenge is about the citizen who wants an answer, the official who needs the right policy at the right moment, and the infrastructure that makes both possible.

Starter data is provided in `challenge-2/` — choose between structured files (20 text-based documents in HTML, Markdown, and plain text) and/or unstructured files (23 binary-format documents including Word, PDF, and spreadsheets).

[Read the full challenge brief](challenge-02-unlocking-the-dark-data.md)

### Challenge 3: Supporting casework decisions

Caseworkers across government spend a significant part of their day on information-gathering tasks — reading through notes to understand a case, looking up which policy applies, checking whether evidence has arrived, identifying what action is needed next. These are tasks that follow predictable patterns. The judgement and decision-making that genuinely requires a person gets less time as a result.

This challenge is about the caseworker who needs the right information quickly, the team leader who needs visibility of risk across their caseload, and the applicant who is waiting for a decision and does not know where their case stands.

[Read the full challenge brief](challenge-03-supporting-casework-decisions.md)

### Challenge 4: Knowing your own organisation

Departments hold significant information about their people, projects, and operational workload — but it is distributed across systems that were not designed to work together. When a minister asks a director how many people are working on a priority programme, the answer takes days to piece together. When a head of operations wants to know which teams are under pressure, they have to ask around rather than look it up.

This challenge is about the leader who needs a clear picture to make a decision, the operations manager who can see the pressure but cannot surface it in a form anyone can act on, and the team whose workload is invisible to the rest of the organisation.

[Read the full challenge brief](challenge-04-knowing-your-own-organisation.md)

## Judging

Scoring runs throughout the day, not just at the end. Your team earns points for reaching milestones during the build phase, tracked on a live dashboard visible to the room. Milestones include things like setting up your repository, producing a first working prototype, and demonstrating a complete user journey.

At the end of the build phase, judge pairs visit every team at their tables. Each pair asks a consistent set of questions about what you built, how you used AI tools, and what you would do next. They score against a simple rubric.

Your final score combines your milestone points with the judge review. There are no stage presentations.

## Day structure

| Time | Activity |
|------|----------|
| 08:30 | Arrival, registration and breakfast |
| 09:00 | Welcome and kick-off |
| 09:15 | Problem selection and team planning |
| 09:45 | Lightning talk: Version 1: From Requirements to Release - AI's Role Across the SDLC|
| 09:55 | Build phase |
| 11:00 | Morning break |
| 11:30 | Lightning talk: Microsoft: Lightning Talk: One Platform, Many Models — Choice at the Core|
| 11:45 | Build phase (continued) |
| 12:30 | Lunch break (optional working break) |
| 13:45 | Lightning talk: Anthropic: Let Claude Cook |
| 13:55 | Build phase (resumed) |
| 14:30 | Afternoon break |
| 14:45 | Build phase (final stretch) |
| 15:15 | Final review — judges return to teams for rubric scoring |
| 16:00 | Lightning talk: AWS: Pushing Security to the Left with Agentic AI|
| 16:15 | Top 3 Finalist Presentations|
| 16:30 | Winners announced and wrap-up |
| 16:45 | Post-Event Networking |

## Team formation

Teams are three to five people, pre-assigned before arrival. When you walk in, you already have a group to sit with. Each team is supported by a Forward Deployed Engineer (FDE) from Version 1, who acts as your technical anchor throughout the day. FDEs are experienced engineers who can help you scope your approach, unblock technical problems, and point you to the right resources. They will not write your code for you, but they know the challenges well and can help your team make decisions when you are stuck. If you registered without a team, you will be placed into one on the day.

## Materials included

This workshop includes:

- `README.md` (this file) — overview and day structure
- `Changelog.md` — dated change history for repository additions, changes, fixes and documentation updates
- `Context.md` — project context, architecture assumptions, data policy and operating constraints
- `Progress.md` — current implementation status, validation, blockers and next steps
- `AGENTS.md` — repo-wide operating rules, including the documentation lockstep policy
- `SETUP-GUIDE.md` — what to do before the event
- `open-brief.md` — guidance for teams bringing their own problem, including prompts to frame and scope it
- `challenge-01-from-pdf-to-digital-service.md` — detailed brief, data, and prompts for challenge 1
- `challenge-1/FORM-LIC-001-licence-application.pdf` — sample licence application PDF for challenge 1
- `challenge-02-unlocking-the-dark-data.md` — detailed brief, data, and prompts for challenge 2
- `challenge-2/` — starter data for challenge 2: `structured_files/` (text-based documents) and `unstructured_files/` (binary-format documents)
- `challenge-2/wiki/evaluation-benchmark.md` — 100-question source-backed benchmark for evaluating how AI coding agents use the Challenge 2 wiki
- `challenge-2/tools/run_wiki_eval.py` and `challenge-2/tools/wiki_eval_mcp.py` — Challenge 2 evaluation harness and auditable MCP layer
- `challenge-03-supporting-casework-decisions.md` — detailed brief, data, and prompts for challenge 3
- `challenge-04-knowing-your-own-organisation.md` — detailed brief, data, and prompts for challenge 4

---
Version: 1.0
Last updated: April 2026
