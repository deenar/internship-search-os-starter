---
name: cv-tailor
description: Tailor the candidate's CV for a specific role — reorder and rephrase existing experience to match a JD. Produces a one-page .docx.
---

# CV Tailor

Produces a role-specific CV by selecting, reordering, and rephrasing what's in
`data/profile.json` to match the target role.

## Workflow

1. **Get the JD.** If given a URL (Trackr listing, LinkedIn posting, company careers page), fetch
   it rather than working from the user's paraphrase. If given pasted text, use that directly.
   Identify: role title, firm, key skills/qualities emphasised, and any specific keywords the JD
   repeats (these often map to applicant-tracking-system filters — worth mirroring in wording,
   not just substance).

2. **Confirm a ledger entry exists.** Run `manage_applications.py find --company "<company>"`
   before drafting anything. No match: stop here and get the application logged via
   `application-tracker` first (see CLAUDE.md's Ground rules for skills) — don't draft the CV
   and log it after the fact. Creating the record isn't this skill's job (that's
   `application-tracker`'s), but producing a CV with no ledger entry behind it is a bug, not a
   deferred task.

3. **Read `data/profile.json`.** This is the entire universe of true claims available.

4. **Select and prioritise.** For each JD requirement, find the strongest matching bullet(s) in
   `profile.json`'s `experience` / `responsibilities_and_achievements`. Order sections and bullets
   so the most JD-relevant material appears first. It's fine to omit an experience entry entirely
   if it's not relevant and space is tight (one page) — but never drop education or invent gaps
   that misrepresent the timeline.

5. **Rephrase fairly.** Tighten wording or echo the JD's terminology (e.g. "financial modelling"
   vs "valuation work") when it's a fair restatement. Keep framing honest — academic/
   extracurricular projects stay framed as such (e.g. a schools investment challenge is not a placement).

6. **Flag gaps.** If the JD wants something not in `profile.json`, tell the user directly and
   ask whether to proceed without it or add the experience first.

7. **Generate the document** using the `docx` skill, following `.claude/CLAUDE.md`'s house style
   (one page, UK spelling, action-verb bullets, quantified where the source supports it). Standard
   sections: header (name/email/location), Education, Experience, Responsibilities & Achievements,
   Skills.

8. **Save** to `applications/<company-slug>_<role-slug>/CV_<Company>_<Role>.docx` (create the
   folder if it doesn't exist). Use lowercase-hyphenated slugs (e.g. `goldman-sachs_ib-spring-insight`).

   **Also save a markdown copy** alongside the `.docx`:
   `applications/<company-slug>_<role-slug>/CV_<Company>_<Role>.md`
   This is a plain-text mirror of the same content (same sections, bullets, and wording) for
   embedding in the pipeline dashboard artifact. The `.docx` remains the submission-ready version;
   the `.md` is the viewable-anywhere copy. Generate both from the same content in one pass.

9. **Update the tracker.** Step 2 already confirmed the record exists — call
   `application-tracker`'s update path (`manage_applications.py update --id <id> --cv-path
   "<path>"`) so the ledger stays in sync without the user having to report it back manually.

10. **Report back**: which JD/posting this was tailored against (and its URL/date), which
    experiences were prioritised and why, and any gaps flagged in step 6.

## Notes

- Confirm before overwriting an existing `.docx` at the same path unless the user explicitly
  asked for a re-tailor.
