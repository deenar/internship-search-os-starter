---
name: interviewer-perspective
description: Flip interview questions to the interviewer's side — what they assess and red flags they watch for. Use as a second pass after interview-prep.
---

# Interviewer's Perspective

**Flips** interview questions to the interviewer's viewpoint — what they're evaluating behind
each question.

## Inputs

- Job description (required)
- `data/profile.json`
- Company research brief (if available)
- Interview stage

## Workflow

1. **Read `data/profile.json`** and any existing interview prep at
   `applications/<company>_<role>/interview-prep.md`.

2. **Load the perspective engine.**
   Load @`../career-helper/supporting-prompts/interviewer-perspective-guide.md` and use
   template @`../career-helper/templates/interviewer-perspective-template.md`.

3. **Save output** to `applications/<company>_<role>/interviewer-perspective.md`.
   Completion: perspective report covers every major question type from the interview-prep
   document.
