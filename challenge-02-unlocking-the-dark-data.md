# Challenge 2: Unlocking the dark data

Government produces an enormous amount of guidance, policy, and procedural documentation. Most of it is published. Very little of it is genuinely findable when someone needs it.

This creates a problem for every channel through which citizens interact with government. A helpline adviser searching for guidance before answering a call. A GOV.UK page that should answer a question but links to a 60-page PDF instead. An automated service that cannot give a direct answer because the content it needs to draw on has never been structured. A citizen submitting a freedom of information request to find something that was technically published all along.

The problem is the same regardless of which channel or department you look at: content exists but is not accessible in a form that any system — or any person in a hurry — can easily use.

## The experience today

A citizen wants to know whether they are eligible for a specific type of support. They search on GOV.UK. They find a guidance page that links to a 60-page PDF. The answer is in section 4.2. They do not know that. They start reading. The language is technical. They are not sure the guidance applies to their situation. They call a helpline instead.

The adviser who answers has the same problem. They know guidance exists and roughly where to look. They put the caller on hold and search a shared drive. They find three documents with similar names and different dates. They are not sure which is current. They give the caller an answer based on the version they could find most quickly. It may not be the right one.

A developer building a new service in a different part of government needs to surface eligibility rules to users. The rules are in a series of policy documents. There is no API, no structured data, no way to query the content programmatically. They extract it manually and hard-code it into the service. When the policy changes, the service is out of date before anyone notices.

## The users

**The citizen** — wants a direct answer to a specific question. They do not want to be pointed at a document. They will not read a 60-page PDF to find one paragraph. They want to ask a question and get an answer through whatever channel they are using — a website, a chat interface, a phone call, a letter.

**The frontline adviser or caseworker** — needs the right guidance quickly to do their job correctly. They are not failing to find it because they are not looking — they are failing because the content is not structured in a way that makes it findable under time pressure.

**The developer or service team** — needs policy content in a machine-readable format so they can build services that stay accurate when policy changes, rather than requiring manual updates.

**The policy owner** — publishes guidance and wants it to be used correctly. Currently has no way to know whether it is being found, interpreted correctly, or applied consistently.

## Why this matters

When government information is hard to find, people make avoidable mistakes, contact centres handle avoidable calls, and services give outdated or incorrect answers. The cost falls on citizens and on the public servants trying to help them.

Making content structured and accessible — extracting it from documents, defining how it should be represented, making it queryable — is the foundation of better citizen-facing services across every channel. It is not a glamorous problem, but it is one that almost every department faces and very few have solved.

## Finding data to work with

You have several options. You do not need all of them — start with whichever gets you moving fastest.

**Starter documents in the `challenge-2/` folder.** We have provided two sets of synthetic government documents. Your team can choose to work with either set, or both:

- **Structured files** (`challenge-2/structured_files/`) — 20 text-based documents (HTML, Markdown, plain text) covering two interlocking policy domains (housing and benefits, small business and employment). They vary in structure and metadata quality, with deliberate inconsistencies to discover: stale content marked as current, internal contradictions, hidden supersession relationships, cross-domain references, and metadata gaps.

- **Unstructured files** (`challenge-2/unstructured_files/`) — 23 binary-format documents (Word .docx, PDFs, spreadsheets .xlsx) simulating a real government shared drive. These include HR policies, meeting minutes, ministerial briefing packs, compliance reports, procurement tables, and a staff directory. They have the messy filenames, outdated content, draft documents, missing annexes, and data quality gaps you would find on a real departmental drive.

**Real government content via the GOV.UK Content API.** This is a live API that serves the structured content already published on GOV.UK. You can query it by path, content type, or keyword. It is a good source of real guidance pages to experiment with.

```
https://www.gov.uk/api/content/[any-govuk-path]
```

For example: `https://www.gov.uk/api/content/expenses-and-benefits-a-to-z`

**Real documents from data.gov.uk.** Search https://data.gov.uk for published government documents in a policy area that interests you. Many are available as PDFs or spreadsheets.

**Generate your own synthetic documents.** Use your AI coding tool to create realistic fictional documents to test against:

```
Generate 3 synthetic government guidance documents as plain text.
Each should have: a title, a publication date, an issuing team,
3 to 5 sections with headings, at least one table, and a summary.
Topics: (1) procurement thresholds and approval routes,
(2) staff expenses policy, (3) data sharing between teams.
Make the language realistic — formal, policy-document style.
```

Generate as many as your team needs. Starting with 3 to 5 documents is enough to build and test an extraction pipeline.

---

<details>
<summary><strong>Hint 1 — Explore the problem: who needs this and why?</strong></summary>

Before writing any code, use your AI coding tool to understand what "findable" actually means for real users trying to get an answer from government content.

```
I am designing a system to make government guidance documents
searchable and usable. Walk me through the experience of a
citizen trying to find out whether they qualify for a specific
benefit, starting from GOV.UK. Where does the experience break
down? What do they need that they are not getting?
```

```
A frontline adviser is on a call and needs to find the right
policy guidance quickly. The guidance is spread across Word
documents and PDFs on a shared drive. Walk me through what that
looks like. Where does time get spent? What could go wrong if
they use the wrong version?
```

```
A developer is building a service that needs to surface
eligibility criteria from a policy document. The document is a
PDF. What are their options? What are the risks of each approach?
```

</details>

<details>
<summary><strong>Hint 2 — Possible directions and design questions</strong></summary>

The challenge has two distinct layers. The first gets you something working. The second is where the real design thinking happens.

**The extraction layer** — getting text, structure, and metadata out of document formats that were not designed to be read by machines. PDF and Word documents do not expose their structure in a standard way. Getting headings, sections, tables, and metadata out cleanly is the foundation everything else sits on.

**The schema layer** — deciding how to represent extracted content so something else can use it. This is a design problem. A schema that stores raw text is less useful than one that preserves document structure. A schema designed with a specific consumer in mind — a search interface, a chat system, a caseworker tool — is more useful still. Think about: who reads this output? What question are they trying to answer? What do they need to get a useful response?

Consider also: what channel is your citizen or official using to interact with government? The schema that powers a search results page is different from the one that powers a voice interface or a caseworker decision support tool. Picking a specific channel and designing your schema for it will produce a more interesting result than a generic document store.

</details>

<details>
<summary><strong>Hint 3 — A starting point with specific prompts</strong></summary>

If your team wants a concrete direction, here is one approach.

Start by defining your output schema — this shapes everything else:

```
I need a JSON schema for structured government document content
that could power a search or question-answering interface. Each
document should capture: title, publication date, issuing team,
a list of sections (each with heading and body text), any tables
as structured data, and a list of keywords. Generate the schema
and one example document in that format.
```

Then generate some documents to work with (or use the GOV.UK Content API):

```
Generate 5 synthetic government guidance documents as plain text
covering: (1) travel and expenses policy, (2) procurement
thresholds, (3) data protection guidance for staff, (4) flexible
working policy, (5) incident reporting procedure. Each should
have a title, date, 4 sections with headings, and one table.
```

Then build extraction:

```
Write a Python function that takes a plain text document and
returns a structured dictionary matching this schema:
[paste your schema]. Extract the title from the first line,
identify section breaks by heading patterns, and extract any
tables as lists of rows.
```

Then build a simple search interface:

```
I have a list of extracted documents as JSON objects. Build a
search function that takes a query string and returns the top 5
matching documents with the most relevant passage highlighted.
Keyword matching is fine for a demo.
```

</details>

## What does a good outcome look like?

By the end of the day, you should be able to show: a set of documents whose content has been extracted and structured, a way to query or search that content, and a clear explanation of who benefits and how. If you can also show what the output schema would enable — the chat interface, the search page, the service that stays up to date when policy changes — that is a strong demo.

## Challenge 2 wiki evaluation harness

The repository also includes an evaluator for the generated Challenge 2 wiki. It is intended for comparing how Codex, Gemini CLI, and Claude Code answer the same source-backed questions when instructed to use only the local wiki.

Key files:

- `challenge-2/wiki/evaluation-benchmark.md` — 100 questions, gold answers, rubrics, and the summative scoring regime.
- `challenge-2/tools/run_wiki_eval.py` — CLI harness that sends selected questions to Codex, Gemini CLI, and Claude Code.
- `challenge-2/tools/wiki_eval_mcp.py` — stdio MCP-compatible audit layer for controlled wiki read/search and answer recording.
- `challenge-2/tools/summarise_wiki_eval.py` — leaderboard summariser for completed scoring sheets.
- `challenge-2/evaluation/README.md` — operational instructions and output inventory.

Dry-run smoke test:

```bash
python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --run-id smoke
```

Each run writes prompts, captured answers, scoring sheets, an event ledger, source register, audit card, integrity manifest, and a zipped DSAP-style audit bundle under `challenge-2/evaluation/runs/<run-id>/`.

## Useful references

- GOV.UK Content API — https://content-api.publishing.service.gov.uk
- data.gov.uk — https://data.gov.uk
- Office for National Statistics publication archives — https://www.ons.gov.uk

---
Version: 1.2
Last updated: April 2026
