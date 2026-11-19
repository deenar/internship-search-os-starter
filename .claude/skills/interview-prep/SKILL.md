---
name: interview-prep
description: Prepare for an upcoming interview — role-specific questions, STAR answers from real experience, and questions to ask. Use when an interview is coming up or the user wants to practise.
---

# Interview Prep

Generates tailored interview preparation grounded in `data/profile.json` and existing company
research for this application.

## Inputs

- Company name and role (required)
- Interview stage — recruiter screen, hiring manager, technical, panel, final (required)
- Known interviewer names/roles (if available)
- Company research brief (check `applications/<company>_<role>/research-brief.md` first)

## Workflow

1. **Confirm a ledger entry exists** — run
   `manage_applications.py find --company "<company>"`. No match: stop and get the application
   logged via `application-tracker` first (see CLAUDE.md's Ground rules for skills) — reaching
   interview stage without a logged application is itself a sign the ledger has drifted from
   reality, worth surfacing to the user.

2. **Read `data/profile.json`** and existing company research at
   `applications/<company>_<role>/research-brief.md`. If no research exists, offer to run
   `company-research` first.

3. **Load the prep engine.**
   Load @`../career-helper/supporting-prompts/interview-prep.md` and follow its question
   generation strategy. Use template
   @`../career-helper/templates/interview-prep-template.md` for output structure.

4. **Save output** to `applications/<company>_<role>/interview-prep.md`.

5. **Suggest next steps:** `interviewer-perspective` for a deeper read on what interviewers
   assess, or `mock-interview` for practice under pressure.

## Completion

Interview prep document saved to the application folder with 15-20 role-specific questions,
STAR answers, and questions to ask.

## TODO: Ledger Integration

The dashboard currently auto-discovers documents by scanning the folder for hardcoded filenames.
To make this more robust, skills should update `data/applications.json` with explicit document paths
after creating files (e.g., `interview_prep_path`, `assessment_prep_path`). This requires:

1. Extending `manage_applications.py` to support additional document path fields, or
2. Having skills update the JSON directly via Python

See the issue: Dashboard shouldn't be the source of truth for what documents exist.
