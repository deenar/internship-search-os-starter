---
name: post-interview-coaching
description: Diagnose a rejection — stage-specific gap analysis, pattern tracking, and recovery plan. Use when the user gets rejected or an interview didn't go well.
---

# Post-Interview Coaching

**Diagnoses** a rejection — where and why — and turns it into actionable lessons with forward
momentum.

## Inputs

- Which stage the rejection happened (application / recruiter screen / HM screen / technical / final)
- The role applied for (check `data/applications.json` for the entry)
- What happened — questions asked, how they answered, their sense of how it went
- Any feedback received (even generic "went another direction")

## Workflow

1. **Read `data/profile.json`** for the "What's Still True" evidence anchor and
   `data/applications.json` for the application history (rejection count, pattern context).

2. **Load the coaching engine.**
   Load @`../career-helper/supporting-prompts/post-interview-coaching.md` and use template
   @`../career-helper/templates/post-interview-debrief-template.md`.

3. **Save output** to `applications/<company>_<role>/post-interview-debrief.md`.

4. **Update the tracker** — if not already done, update the application status to `rejected`:
   ```
   python3 .claude/skills/application-tracker/scripts/manage_applications.py \
     --applications data/applications.json update \
     --id <APP-xxxx> --status rejected
   ```

5. **Suggest next steps** — if a skill gap was identified, offer to update interview prep for
   similar roles; if a signal gap, suggest mock interview practice.

## Completion

Debrief saved, application status updated to rejected, lessons extracted, next action proposed.
