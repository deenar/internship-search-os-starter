---
name: mock-interview
description: Run a realistic mock interview simulation with feedback. Use when the user wants to practise before an interview or test their prep answers.
---

# Mock Interview

Interactive interview simulation — the practice step after written interview prep.

## Inputs

- Role and company (required)
- Interview stage (required)
- Interviewer persona and difficulty preferences (the supporting prompt presents options)
- Existing interview prep (check `applications/<company>_<role>/interview-prep.md`)

## Workflow

1. **Read any existing interview prep** at `applications/<company>_<role>/interview-prep.md`
   and `data/profile.json`.

2. **Load the simulation engine.**
   Load @`../career-helper/supporting-prompts/mock-interview.md` and run the interview
   interactively.

3. **After the mock**, provide structured feedback — per-question assessment, STAR compliance,
   overall impression, and specific improvements. Completion: every question answered has
   individual feedback, and at least one concrete improvement is actionable before the real
   interview.
