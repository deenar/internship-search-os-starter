# Internship Search OS — Standing Instructions

This file is read automatically at the start of every session in this project. It applies to
every skill in `.claude/skills/`.

## Who this is for

> **FILL THIS IN** — this paragraph is read at the start of every session and shapes every skill.

[Your name] — [year/stage] [degree] student at [university] (started [Month YYYY], expected
graduation [YYYY]). Targeting [sector, e.g. UK finance] [programme type, e.g. summer internships]
for [Summer YYYY]. Primary sources for roles: [Trackr](https://app.the-trackr.com/uk-finance/summer-internships)
and LinkedIn. Strongest CV themes so far: [one or two lines on what your experience is best at
evidencing — e.g. an investment competition, a research project, a society role].

## Target roles (edit this section to make it yours)

> Narrow this down once you've seen more of the pipeline. Firm-name and sector specificity here
> directly improves how `cv-tailor` and `cover-letter` prioritise which bullets to lead with, and
> how `role-finder` filters Trackr by default.

- **Breadth:** [all Trackr categories, or a subset — Bulge Bracket / Elite Boutique / Middle
  Market IB, Buy-Side, Asset Management, Trading and Quant, Consulting, Big 4, Real Estate,
  Pensions and Insurance, Accounting and Audit, Miscellaneous]
- **Exclusions:** [anything `role-finder` should never surface — e.g. roles whose title contains
  "Quant"/"Quantitative". Judge from the role title text; flag ambiguous cases rather than
  guessing.]
- **Open to:** [e.g. Investment Banking, Equity Research, Asset Management, Sales & Trading]
- **Firm shortlist:** [none yet — add one once a pattern emerges]

## House style for all output

- **CV**: one page, quantified impact where the source data supports it ("10+ students",
  "6-week programme"), action-verb bullets, UK spelling, no fabricated claims. Reorder and
  re-emphasise existing bullets to match a JD's language — never invent new ones.
- **Cover letter**: UK business-letter format, ~300–400 words, 3–4 paragraphs. Must reference
  something *specific* to the firm/programme (a desk, a deal, a stated value, a programme
  structure) — generic "I am passionate about finance" filler is not acceptable. If nothing
  firm-specific is known yet, say so and ask rather than writing filler.
- Always state which JD/posting a tailored CV or letter was written against, and the date, so
  it's clear what it was tailored for and how fresh that's likely to still be.
- Flag uncertainty inline: if a JD implies something (a specific skill, a stated interest) that
  isn't backed by `data/profile.json`, say so rather than quietly filling the gap.
- Dates in UK format (DD Month YYYY).
- **Hyperlinks in markdown output**: always use `[descriptive text](URL)` — never bare URLs.
  Use the page title, person's name, company name, or action as the link text
  (e.g. `[Acme Capital application](https://job-boards.greenhouse.io/...)`,
  `[Jane Doe](https://www.linkedin.com/in/jane-doe/)`).
  This applies to all generated .md files: research briefs, networking intelligence,
  interview prep, application strategies, cover letters, and any other skill output.

## Data sources — priority order

1. **`data/profile.json`** — the master CV. Single source of truth for every claim used in a
   tailored CV or cover letter. Skills read this first and never invent beyond it.
2. **The job posting itself** — Trackr listing, LinkedIn posting, or company careers page. Fetch
   it (WebFetch, or browser tools if it needs a logged-in view) when a URL is given, rather than
   working from the user's paraphrase alone.
3. **`data/applications.json`** and prior entries — check what's already been recorded for a
   firm/programme before re-researching it from scratch.

**Finding new roles**: `role-finder` batch-scans Trackr's public listing and proposes a
shortlist (see that skill and the gotchas below). LinkedIn has no batch-scan equivalent — paste
individual LinkedIn job URLs and `application-tracker` will fetch and log that one posting.

## Known gotchas — external sources

- **Trackr's `Last Year Opening` column is not a deadline.** It's when the equivalent programme
  opened in the *previous* cycle — informational only. Confirmed 2026-07-03 by inspecting the
  live table directly: several rows
  had an empty real `Closing Date`/`Opening Date` and only `Last Year Opening` populated. A naive
  text-scrape of the page conflates these into what looks like one deadline column — don't do
  that. Only `Closing Date` is ever a real deadline; `role-finder` handles this correctly.
- **LinkedIn is out of scope for automated scanning** (explicit decision, 2026-07-03). LinkedIn's
  User Agreement prohibits automated data collection, and crawling its search results risks the
  account being restricted — a different and higher risk than Trackr's public listing page.
  Fetching one specific LinkedIn URL the user pastes (a normal single-page fetch, not crawling) is
  fine and already supported by `application-tracker`.
- **Trackr's summer-internships table needs no login to view** (confirmed 2026-07-03) — don't
  assume an authenticated session is required. If a future run hits a login wall, stop and tell
  the user rather than trying to work around it.

## State & memory conventions

- **Master CV**: `data/profile.json` — one file, the source of truth for all experience/skills/
  achievements. Only ever grows (new experience appended as it happens) — never trim real history
  to fit a one-page CV; trimming for length happens per-tailored-document, not in the source file.
- **Application ledger**: `data/applications.json` — one row per application (company, role,
  source, dates, status, generated document paths, follow-up tracking). Write path is the
  `application-tracker` skill only — don't hand-edit it.
- **Generated documents**: `applications/<company>_<role-slug>/CV_<Company>_<Role>.docx` and
  `CoverLetter_<Company>_<Role>.docx` — one folder per application.
- **Session log**: `.claude/memory/session_log.md` — short append-only log of what was done each
  session, so a fresh session can catch up in one read.

## Dashboard artifact (`dashboard/pipeline.html`) — optional

A claude.ai Artifact page that reads `data/applications.json` live from GitHub via the GitHub MCP
server. Set `REPO.owner` in the file to your GitHub username first (it ships as
`YOUR-GITHUB-USERNAME`). The published page is a **separate copy** from the file in this repo:
after any edit to `dashboard/pipeline.html`, commit and push, then republish the artifact *to its
existing URL* (record that URL in `.claude/memory/` after the first publish) — publishing without
the URL creates a new artifact and orphans the bookmarked one.

## External skills 

Two third-party skills, dropped in by the user rather than built for this project specifically:

### `career-helper`

A large general-purpose career-coaching package (15 capabilities, CC BY-NC 4.0, by Paul Bratcher/
Prosper Consulting — see `.claude/skills/career-helper/README.md` for full attribution). Its own
conventions differ from this project's: it writes to `career-outputs/{role-slug}-*.md` at the
project root rather than `data/applications.json` + `applications/<company>_<role>/`, and it
doesn't know about this project's house style or `data/profile.json`.

**Overlap with this project's own skills** — on any ambiguous request that could mean either,
**stop and ask which one before running either**. If the user names one explicitly (e.g.
"use Career-Helper's ATS rewrite" or "run cv-tailor"), that's unambiguous — just run it.

| This project's skill | Overlapping Career-Helper capability |
|---|---|
| `cv-tailor` | #2 ATS-Optimized CV Rewriting |
| `cover-letter` | (no direct equivalent — Career-Helper doesn't draft cover letters) |
| `application-tracker` / `application-strategy` | #8 Application Strategy & Timeline |
| `role-finder` | (no equivalent — Career-Helper doesn't scan job boards) |
| `company-research` | #3 Company & Role Research |
| `interview-prep` | #4 Interview Preparation |
| `interviewer-perspective` | #4b Interviewer's Perspective Reports |
| `post-interview-coaching` | #6 Post-Interview Coaching & Recovery |
| `networking-intelligence` | #7 Strategic Networking Intelligence |
| `mock-interview` | #15 Mock Interview Simulation |

These local wrapper skills load Career-Helper's supporting prompts and templates but save output
to `applications/<company>_<role>/` (not `career-outputs/`) and read from `data/profile.json`.
They are the preferred path — invoke them by name rather than Career-Helper directly. #11 Offer
Evaluation has no local wrapper yet but could matter if multiple internship offers land at once.

**Capabilities that mostly don't apply to a student internship search** (kept installed as-is per the
"don't hand-edit a third-party licensed package" decision, 2026-07-06 — just won't come up
naturally): #10 Salary Negotiation (framed around senior/full-time comp, not typical for an
internship), #12 LinkedIn Video, #13 Portfolio & Fractional Career, #14 AI Readiness.

**LinkedIn note**: Career-Helper's `networking-strategy.md`/`company-research.md` use
`site:linkedin.com` search-engine queries (via WebSearch), not direct scraping — consistent with
this project's own no-automated-LinkedIn-scraping stance (see Known gotchas below). It explicitly
falls back to asking the user for a screenshot/copy-paste when LinkedIn blocks a direct fetch,
rather than trying to work around the block.

### `the-humanizer`

Generic AI-writing-texture detector and rewriter (blog/LinkedIn/email/Slack). Most relevant use
here: **run it on a drafted cover letter before finalizing**, to catch generic AI-sounding phrasing
that would undercut the "must reference something specific to the firm" house-style rule above.
Not integrated into `cover-letter`'s own workflow automatically — invoke it as a separate pass
when the user wants an extra check, not a mandatory gate on every letter.

## Ground rules for skills

- **Never fabricate** a specific achievement, skill, grade, or experience not present in
  `data/profile.json`. If a JD wants something the profile doesn't support (a language, a prior
  internship, a specific tool), flag the gap explicitly rather than inventing it or implying it.
- **Never submit an application, click "Apply," or send an email autonomously.** This system
  drafts CVs, cover letters, and follow-up emails and tracks status — the user reviews and
  submits/sends everything themselves. Don't revisit this without being asked.
- Every cover letter needs at least one firm/programme-specific detail — if a skill can't find
  one, it should say so and ask rather than ship generic filler.
- When a skill updates `data/`, say explicitly what was written/changed.
- **A `data/applications.json` entry must exist before any skill writes into
  `applications/<company>_<role>/`.** Applies to `company-research`, `application-strategy`,
  `cv-tailor`, `cover-letter`, `interview-prep`, and `networking-intelligence`. Run
  `manage_applications.py find --company "<company>"` first (see `application-tracker`'s
  section (c)). No match found: stop and get the entry logged via `application-tracker` before
  producing any document — don't draft first and log later, and don't quietly proceed without
  one. This isn't these skills' job to fix themselves (`application-tracker` is the sole write
  path, per Data sources above); it's a hard precondition, not a footnote in the final report.
