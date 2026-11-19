---
name: company-research
description: Research a target company — fundamentals, culture, hiring context, red flags. Use when the user names a company to research or at the targeted stage.
---

# Company Research

Parallel web research on a target company, producing a structured brief for cover letters,
interview prep, and networking outreach.

## Inputs

- Company name (required)
- Job description or role title (strongly recommended — focuses the research)
- Any specific areas the user wants investigated

## Workflow

1. **Confirm a ledger entry exists** — run
   `manage_applications.py find --company "<company>"` before doing anything else. No match:
   stop here and get the application logged via `application-tracker` first (see CLAUDE.md's
   Ground rules for skills) — don't research into a folder with no ledger backing. A match also
   tells you whether `applications/<company>_<role>/research-brief.md` already exists, so you
   don't start from scratch unnecessarily.

2. **Read `data/profile.json`** so the research can flag connections between the user's
   experience and the company's work (e.g. if the company's equity research desk covers a sector
   the user has studied).

3. **Load the research engine.**
   Load @`../career-helper/supporting-prompts/company-research.md` and follow its parallel
   research methodology. Use template @`../career-helper/templates/research-brief-template.md`
   for output structure.

4. **Save output** to `applications/<company>_<role>/research-brief.md` — not to
   `career-outputs/`. Create the application folder if it doesn't exist.

5. **Report** what was found, flag anything that changes the application calculus (red flags,
   upcoming deadlines, key contacts identified), and suggest next steps (CV tailoring, networking
   outreach).

## Completion

Research brief saved to the application folder, key findings stated, next action proposed.
