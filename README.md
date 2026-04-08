# AI Engineering Lab Hackathon

A one-day event where you work in a small team to build a working prototype that addresses a real cross-government challenge. You will use your AI coding tools throughout the day to plan, write, test, and present your solution.

This event is open to all engineers in the AI Engineering Lab community, whether your department is currently on the programme or not.

## What this is

This is not a competition to write the most code. It is about showing how AI tools change the way you work, and building something that could make a real difference to how government operates.

### AI coding tools and your application

You will use AI coding tools (GitHub Copilot, Amazon Q Developer, Gemini Code Assist, or similar) to help you plan, write, and test your prototype. These tools assist your development process.

> The event does not provide access to AI models (such as large language model APIs) for use within your application.

If your team has access to models through your own department or personal accounts, or if you want to use locally hosted models, that is fine. You can also mock AI capabilities in your prototype. The focus is on what you build and how you use your coding tools to build it, not on embedding AI into the solution itself.

By the end of the day, your team will have:

- chosen a challenge and scoped a realistic solution
- built a working prototype using AI-assisted development
- reflected on how AI tools shaped your approach
- explained your work to a judging panel at your table

## The challenges

Your team picks one of the four challenges below, or proposes an open brief. All challenges are drawn from real cross-government needs. Your solution should be demoable by the end of the day.

### Open brief

If your team has a relevant problem you care about, pitch it to a facilitator during the morning session. It must be achievable in one day and use open or synthetic data.

### Challenge 1: From PDF to digital service

Government teams still rely on PDF forms and paper-based processes for tasks that should be simple digital services. Pick a real or realistic government form — a licence application, a reporting template, an internal request process — and turn it into a working digital service that a member of the public or a civil servant could actually use.

Your service should follow GOV.UK design patterns and meet WCAG 2.2 accessibility standards. Focus on building something that works end to end for a single user journey rather than covering every edge case.

This is a good starting point if your team is newer to AI coding tools. You can one-shot a working form in minutes and spend the rest of the day iterating.

Starting points: any publicly available government PDF form (search GOV.UK for forms in your policy area), the GOV.UK Design System at https://design-system.service.gov.uk, the GOV.UK Prototype Kit.

### Challenge 2: Unlocking the dark data

Vast amounts of government knowledge is trapped in unstructured documents — Word files, PDFs, and spreadsheets — scattered across departmental drives and websites. Build a solution that makes this content searchable, extractable, and usable by citizens and officials alike, without requiring manual migration or transformation.

Bonus: define a standard format for a GOV.UK app or chat interface to consume the extracted information.

Starting points: publicly available government documents from data.gov.uk, GOV.UK Content API (for comparison with structured content), Office for National Statistics publication archives, synthetic Word and PDF files.

### Challenge 3: The intelligent case worker

Thousands of caseworking systems exist across government, each siloed and manually intensive. Build reusable capabilities that work across these systems to summarise cases, automate routine workflows, and surface relevant policy in real time to support human decision-making.

If your team has access to AI models (through your department, personal accounts, or locally hosted models), you can integrate them into your solution. If not, you can mock AI endpoints to demonstrate how the system would work with model access. The judging focuses on the quality of the prototype and the approach, not on whether you have a live model behind it.

Starting points: synthetic case data and policy extracts will be provided on the day. GOV.UK Content API for policy pages, published process documentation from DWP, HMRC, or similar departments, and open source casework frameworks are also available.

### Challenge 4: Knowing your own organisation

Departments have surprisingly little visibility of how their people and resources are allocated. Managers struggle to answer basic questions: which teams are working on which projects, where the bottlenecks are, who is over-allocated, and what capacity exists. This information is scattered across HR systems, project trackers, and spreadsheets that do not talk to each other.

Build a tool that takes workforce and allocation data and gives a department a clear, usable picture of how its resources are deployed. Focus on answering one or two questions that a department head would actually ask, such as "Where are my bottlenecks?" or "Which teams are understaffed for the work they have been assigned?"

Starting points: synthetic HR and resource allocation data will be provided on the day. You can also generate your own mock data as a warm-up exercise. Civil Service statistics published by the Cabinet Office and ONS public sector employment data are available for additional context.

## Judging

Scoring runs throughout the day, not just at the end. Your team earns points for reaching milestones during the build phase, tracked on a live dashboard visible to the room. Milestones include things like setting up your repository, producing a first working prototype, and demonstrating a complete user journey.

At the end of the build phase, judge pairs visit every team at their tables. Each pair asks a consistent set of questions about what you built, how you used AI tools, and what you would do next. They score against a simple rubric.

Your final score combines your milestone points with the judge review. There are no stage presentations.

## Day structure

| Time | Activity |
|------|----------|
| 08:30 | Arrival, registration, breakfast |
| 09:00 | Welcome and kick-off — challenges walked through, rules, FDE role clarified |
| 09:30 | Problem selection and team planning |
| 10:15 | Lightning talk 1 |
| 10:30 | Morning break |
| 10:45 | Build phase begins |
| 12:30 | Lunch (optional informal check-in to surface blockers) |
| 13:30 | Lightning talk 2 |
| 13:45 | Build phase resumes |
| 15:00 | Build phase closes — prepare your summary and push your work |
| 15:15 | Afternoon break |
| 15:30 | Judge pairs visit every team |
| 16:15 | Prize giving and close |
| 16:30 | Hard finish |

The agenda may shift by 15 to 30 minutes depending on the number of teams. Your event lead will communicate any changes on the day.

## Team formation

Teams are three to five people, pre-assigned before arrival. When you walk in, you already have a group to sit with. Each team is aligned to a Version 1 Forward Deployed Engineer (FDE) who acts as your technical anchor throughout the day. If you registered without a team, you will be placed into one on the day.

## Materials included

This workshop includes:

- `README.md` (this file) — overview and day structure
- `SETUP-GUIDE.md` — what to do before the event
- `participant-handout.md` — quick reference for the day

---
Version: 1.0
Last updated: April 2026
