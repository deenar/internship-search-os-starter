---
name: progress-summary
description: Give a summary of internship application progress — status breakdown, upcoming deadlines, applications needing a follow-up, and recent activity. Use when the user asks for a progress summary, status update, "where do things stand", wants to know upcoming deadlines, or wants a periodic check-in on the whole application pipeline. Read-only — use application-tracker to change anything.
---

# Progress Summary

A read-only snapshot of the whole application pipeline in `data/applications.json` — status
counts, what needs action, and what's changed lately. Never modifies `data/applications.json`;
that's `application-tracker`'s job.

## Workflow

1. **Read `data/applications.json`.**

2. **Status breakdown**: count applications by `status`. Lead with this — it's the headline
   number the user wants first, per `.claude/CLAUDE.md`'s house style (conclusion before detail).

3. **Needs action now** (most important section):
   - `targeted`/`drafting` applications with a `deadline` within the next 7 days — flag as
     urgent.
   - Applications matching `followup-drafter`'s due criteria (submitted/online_test, ≥14 days
     since `date_submitted`, no `followup_sent_at`) — flag as "follow-up due", and offer to run
     `followup-drafter` for them.
   - Applications with `status` in `interview`/`assessment_centre` and no `notes` update in the
     last 7 days — flag as worth a manual check-in, since this skill can't see inbox/portal state.

4. **Upcoming deadlines**: list all applications with a `deadline` in the future, soonest first,
   regardless of status — this is the list the user should scan to make sure nothing is about to
   be missed even before drafting starts.

5. **Recent activity**: entries whose most recent `status_history` date falls in the last 7 days
   — a quick "what moved" recap.

6. **Funnel view** (only if there's enough data to be meaningful — skip for <5 applications):
   submitted → online_test → interview → offer conversion, so the user can see where in the
   pipeline things are stalling.

7. **Output** per `output_template.md`.

## Notes

- Keep this fast — it's meant to be run often (weekly, or whenever the user wants a pulse check),
  not a deep-dive on any single application.
- Be direct about anything urgent (deadline in <7 days, overdue follow-up) even if not
  specifically asked — that's the point of a pipeline-level view over checking one application at
  a time.
