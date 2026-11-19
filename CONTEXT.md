# Internship Search OS

A personal pipeline for finding, tracking, and applying to UK finance summer internships. The system drafts documents and tracks status — it never submits applications or sends emails on the user's behalf.

## Language

### The pipeline

**Application**:
A tracked opportunity at a specific firm for a specific programme. Created when a role is added to the ledger, regardless of whether any documents have been drafted or anything has been submitted. One application per firm-programme pair.
_Avoid_: Job, opportunity, listing

**Profile**:
The master record of the candidate's experience, education, skills, and achievements (`data/profile.json`). Single source of truth for every claim in a tailored CV or cover letter. Grows over time; never trimmed at source — trimming for length happens per-document.
_Avoid_: CV (ambiguous — could mean the master record or a tailored output), resume

**Tailored CV**:
A one-page document derived from the Profile, reordered and re-emphasised to match a specific job description. Lives in `applications/<company>_<role-slug>/`. Never contains claims absent from the Profile.
_Avoid_: Resume, master CV (that's the Profile)

**Cover Letter**:
A firm-specific letter (~300–400 words) that references at least one concrete detail about the target firm or programme. Generic filler is not acceptable — if no firm-specific detail is known, the skill asks rather than shipping filler.
_Avoid_: Covering letter, motivation letter

**Ledger**:
The application tracking file (`data/applications.json`). One entry per Application, append-only — withdrawn or rejected applications stay with updated status, never deleted. Written only by the `application-tracker` skill.
_Avoid_: Tracker, spreadsheet, database

### Application lifecycle

**Targeted**:
The role has been identified and added to the Ledger as worth pursuing. This is the candidate's decision to target a role — it does not imply the employer has shortlisted the candidate.
_Avoid_: Shortlisted (ambiguous — sounds like the employer acted), not started, found

**Drafting**:
CV and/or Cover Letter are being prepared for this Application.

**Submitted**:
The candidate has manually submitted the application through the firm's portal. The system drafted the documents; submission is always a human action.

**Withdrawn**:
The candidate decided not to pursue this Application. The entry stays in the Ledger with this status.

### Role discovery

**Trackr**:
The primary external job board ([app.the-trackr.com](https://app.the-trackr.com/uk-finance/summer-internships)). Public, no login required. The `role-finder` skill batch-scans it.
_Avoid_: The Trackr, Tracker

**Source**:
Where a role was originally discovered — currently `trackr` or `linkedin`. Recorded per Application in the Ledger.

**Last Year Opening**:
A Trackr-specific column showing when the equivalent programme opened in the *previous* recruitment cycle. Informational only — not a deadline, not an opening date for the current cycle. Only the `Closing Date` column on Trackr is ever a real deadline.
_Avoid_: Deadline, opening date (when referring to this column)

**Rolling**:
The firm reviews applications as they arrive rather than waiting for a fixed deadline to close. Most roles on Trackr are marked rolling. Recorded in Application notes, not as a structured field.

### Programme types

**Summer Internship**:
A paid placement (typically 8–12 weeks, June–August) for penultimate-year students. The main target of this pipeline and the primary conversion path to a full-time offer.
_Avoid_: Placement (ambiguous — could be industrial year)

**Spring Week**:
A short (typically 1-week) insight programme, usually for first-year students. Distinct from a Summer Internship — earlier in the recruitment timeline and less competitive, but also less directly convertible to an offer.
_Avoid_: Insight day (different — usually a single day, not a week)

**Penultimate Year**:
The second-to-last year of an undergraduate degree — the year most banks target for Summer Internship recruitment. For a 3-year degree starting 2025, penultimate year is 2026–2027 and the internship itself is Summer 2027.
_Avoid_: Second year (correct for a 3-year degree but ambiguous for 4-year degrees)
