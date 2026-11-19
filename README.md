# Internship Search OS

A personal pipeline for finding, tracking, and applying to internships — built on Claude Code
skills. Fork it, fill in your own profile, and start applying.

## What this is

A set of Claude Code skills that work together as an application pipeline. You talk to Claude in
natural language; the skills handle the structured work — scanning job boards, tailoring CVs,
drafting cover letters, tracking deadlines, prepping for interviews.

> **What it won't do:** submit applications, send emails, or click "Apply" on any portal. You
> review and submit everything yourself. Documents are drafted, never sent.

The pipeline tracks each application through these stages:

```
targeted → drafting → submitted → online_test → interview → assessment_centre → offer
```

Applications can also be `withdrawn` or `rejected` at any point. Nothing is ever deleted from
the ledger.

## Project structure

```
.claude/
  CLAUDE.md              ← standing instructions, house style, target roles
  skills/                ← one folder per pipeline step
  memory/                ← session log
data/
  profile.json           ← your master CV (source of truth)
  applications.json      ← application ledger
applications/            ← generated CVs & cover letters per application
CONTEXT.md               ← domain glossary
```

## Setup — make it yours

> **New here? Read [GUIDE.md](GUIDE.md) first** — a step-by-step getting-started guide. This
> copy ships clean: the ledger is empty, `applications/` is empty, and `profile.json` holds
> placeholders. Steps 3 and 5 below are already done.

### 1. Fork & clone

```bash
git clone <your-fork-url>
cd internship-search-os
```

Open the folder in Claude Code. The skills load automatically.

### 2. Replace `data/profile.json`

This is the single source of truth for every claim in your CVs and cover letters. Replace the
sample data with your own education, experience, skills, and achievements. Keep the same JSON
structure — the skills read specific fields.

```json
{
  "personal": {
    "name": "Your Name",
    "email": "you@example.com",
    "phone": null,
    "linkedin": "linkedin.com/in/you",
    "location": "London, UK"
  },
  "education": [ ... ],
  "experience": [ ... ],
  "responsibilities_and_achievements": [ ... ],
  "skills": { "technical": [...], "interests": [...], "certifications": [...] }
}
```

Every bullet in every experience entry should be something you can defend in an interview. The
skills will never invent beyond what's here — they'll flag gaps instead.

### 3. Clear the application ledger

Reset `data/applications.json` to an empty state:

```json
{
  "schema_version": 1,
  "as_of": "2026-07-09",
  "applications": [],
  "notes": []
}
```

### 4. Edit `.claude/CLAUDE.md`

This file is loaded at the start of every session. Update these sections:

- **Who this is for** — your name, university, year, graduation date, what you're targeting
- **Target roles** — which sectors, firm types, and categories to scan for. This directly
  controls how `role-finder` filters Trackr and how `cv-tailor` prioritises bullets
- **House style** — adjust CV format, cover letter structure, or tone preferences to match your
  own

### 5. Delete the sample applications folder

Remove the `applications/` subfolders (these are someone else's drafted documents). The skills
will recreate the folder structure as you apply.

```bash
rm -rf applications/*/
```

### 6. Install Claude-in-Chrome

The `role-finder` skill uses browser tools to scan Trackr. Install the Claude-in-Chrome
extension and connect it to Claude Code. Without it, every other skill still works — you just
can't auto-scan the job board.

## The skills

### Discovery

| Skill | What it does |
|---|---|
| `role-finder` | Scans Trackr for new roles, triages by urgency, proposes a shortlist |
| `application-tracker` | Logs a new application or updates status. The only write path to the ledger |

### Preparation

| Skill | What it does |
|---|---|
| `company-research` | Deep-dive on a target company — culture, hiring context, red flags |
| `application-strategy` | Tactical plan for a specific application — timeline, risks, stakeholders |
| `cv-tailor` | Reorders and rephrases your profile to match a JD. Produces a one-page .docx |
| `cover-letter` | Drafts a firm-specific letter with the Why Firm / Why Role / Why You structure |
| `the-humanizer` | Checks a draft for AI-sounding phrasing and rewrites flagged sections |
| `application-pipeline` | Advances an application to its next stage — proposes which skill to run next |

### Interview & follow-up

| Skill | What it does |
|---|---|
| `interview-prep` | Role-specific questions, STAR answers from your real experience |
| `mock-interview` | Interactive simulation with feedback — the practice step after prep |
| `networking-intelligence` | Finds strategic contacts at a target company with outreach messages |
| `followup-drafter` | Drafts follow-up emails for applications with no response after 14+ days |

### Monitoring

| Skill | What it does |
|---|---|
| `progress-summary` | Status breakdown, upcoming deadlines, what needs action now |
| `post-interview-coaching` | After a rejection — diagnose, extract lessons, plan recovery |

## A typical session

**Scanning for new roles** — Say *"What's new on Trackr?"* or `/role-finder`. The skill opens
Trackr in Chrome, extracts every untracked role, classifies them by urgency (has a deadline?
open and rolling? overdue vs last year's cycle?), and presents a table. You pick which to add.
Each one gets logged to `applications.json` as `targeted`.

**Working on an application** — Say *"Work on my BlackRock application"* or
`/application-pipeline`. The skill reads the application's current status and proposes the next
step: company research, CV tailoring, cover letter, or humanizer pass. Each skill saves its
output to `applications/blackrock_summer-internship/` and updates the ledger.

**Checking progress** — Say *"Where do things stand?"* or `/progress-summary`. You get a status
breakdown (how many targeted, drafting, submitted, etc.), urgent deadlines within 7 days, and
applications that are due a follow-up.

**Preparing for an interview** — Say *"Prep me for my Citadel interview"*. The skill pulls the
JD, your tailored CV, and company research to generate role-specific questions with STAR-format
answers drawn from `profile.json`. Follow up with `/mock-interview` for a live practice round.

## Rules the skills enforce

- **No fabrication.** Every claim in a CV or cover letter must trace back to `profile.json`. If
  a JD wants something your profile doesn't have, the skill flags the gap — it never invents
  experience.
- Cover letters must include at least one firm-specific detail. No generic "I am passionate
  about finance" filler.
- The application ledger is append-only. Rejected and withdrawn entries stay — nothing is
  deleted.
- Only `application-tracker` writes to `applications.json`. Don't hand-edit it.
- `profile.json` only grows. Per-document trimming for page limits happens in each tailored CV,
  not in the source file.
- LinkedIn is not scraped. Paste a specific URL and `application-tracker` will fetch that one
  posting.

## Customising further

**Changing target sectors** — Edit the **Target roles** section in `.claude/CLAUDE.md`. List
which Trackr categories to include or exclude. The quant-exclusion pattern (filtering by role
title text) can be adapted for any sector you want to skip.

**Changing the cover letter structure** — The default is Rare Recruitment's three-paragraph
format (Why Firm / Why Role / Why You). Edit `.claude/skills/cover-letter/SKILL.md` to change
the structure, paragraph count, or word target. The skill follows whatever's written there.

**Adding a new job board** — `role-finder` is Trackr-specific. To add another source, duplicate
the skill folder, write a new extraction script for that board's DOM, and update the `source`
field in the `add` command. The valid sources are defined in `manage_applications.py`'s
`VALID_SOURCES` list.

**Non-UK markets** — The system is UK-focused by default (UK spelling, UK business-letter
format, Trackr's UK finance table). To adapt: change the house style in `CLAUDE.md`, point
`role-finder` at a different URL or job board, and update date formats and letter conventions in
`cover-letter/SKILL.md`.

**Non-finance internships** — The skills themselves are sector-agnostic — they tailor CVs, draft
cover letters, and track applications regardless of industry. The finance-specific parts are in
`CLAUDE.md` (target sectors, Trackr categories), `role-finder` (Trackr URL), and the
quant-exclusion filter. Update those and the system works for any internship search.

## Prerequisites

- **Claude Code** — CLI, desktop app, or web app. The skills are just markdown files; Claude
  reads them automatically.
- **Claude-in-Chrome** *(optional)* — needed only for `role-finder`'s Trackr scanning.
  Everything else works without it.
- **Python 3** — the `application-tracker` script runs via Python. No dependencies beyond the
  standard library.
- **Git** — for version control. The project is a git repo by default.

## Testing

`tests/test_manage_applications.py` covers the `application-tracker` write path (ID sequencing,
duplicate rejection, status validation, notes handling):

```bash
python3 -m unittest tests/test_manage_applications.py -v
```

---

Built on the Agent Skills open format. Skills are folders of markdown — readable, forkable, no
lock-in.
