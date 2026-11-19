---
name: cover-letter
description: Draft a firm-specific cover letter grounded in real experience and a concrete detail about the target firm. Produces a .docx.
---

# Cover Letter

Drafts a cover letter evidenced by `data/profile.json` and anchored to something specific about
the target firm/programme. Follows the **Why Firm / Why Role / Why You** three-paragraph
structure recommended by Rare Recruitment for early-careers finance applications.

## Workflow

1. **Get the JD and firm context.** Same as `cv-tailor` — fetch the posting if given a URL. Also
   research the firm for material to use in the "Why this firm?" paragraph (see structure below).
   **If nothing firm-specific can be found, say so and ask the user rather than writing filler**
   — this is a hard requirement, not a nice-to-have.

2. **Confirm a ledger entry exists.** Run `manage_applications.py find --company "<company>"`
   before drafting anything. No match: stop here and get the application logged via
   `application-tracker` first (see CLAUDE.md's Ground rules for skills) — don't draft the letter
   and log it after the fact. Creating the record isn't this skill's job, but producing a letter
   with no ledger entry behind it is a bug, not a deferred task.

3. **Read `data/profile.json`** for the evidence base. Pick experiences that support both the
   "Why this role?" narrative and the "Why you?" evidence paragraph.

4. **Structure** (~400–500 words total, UK business-letter format):

   **Opening sentence** (before the three paragraphs): state year of study, university, degree,
   and the specific programme/role being applied for. One sentence.

   **Paragraph 1 — Why this firm?** (~150 words)
   Signpost clearly in the first sentence that this paragraph is about the firm specifically.
   Include at least 2 of:
   - Networking events attended or people at the firm the applicant has spoken to (ask the user
     if none are known — this is high-value detail that can't be invented)
   - Specific projects, research, deals, or products the firm has produced — use statistics or
     names where possible
   - Industry/functional specialisations the firm is known for and how they align with the
     applicant's experience or interests
   - Culture — mention specific initiatives run by the firm and link them to the applicant's own
     values or experience

   **Paragraph 2 — Why this programme/role?** (~150 words)
   Signpost clearly. Create a **narrative** of how prior experiences led to this specific
   role/programme, or explain what about the programme drew the applicant to it (e.g. rotation
   structure, trading simulation, mentorship). Mention prior work or extracurricular experiences
   where relevant skills were used and enjoyed, connecting them to a career in this division.

   **Paragraph 3 — Why you?** (~150 words)
   Signpost clearly. State the applicant's strongest achievements and skills relevant to finance,
   backed by evidence and numbers (similar style to a CV bullet). Focus on skills particularly
   relevant to the role: problem solving, analytical thinking, leadership, attention to detail,
   communication. Include examples of the applicant personally having a positive impact.

   **Closing sentence**: thank the reader and state availability. Keep to one sentence.

5. **Signposting rule**: the first sentence of each paragraph must clearly indicate whether it's
   about the firm, the role, or the applicant's fit. A reader skimming first sentences only
   should be able to tell the letter's structure.

6. **Never fabricate.** Same rule as `cv-tailor` — every claim must trace to `profile.json`. If
   the letter would be stronger with an experience the profile doesn't contain, flag the gap
   instead of inventing one. Networking contacts and events the user hasn't mentioned cannot be
   invented — ask rather than assume.

7. **Generate the document** using the `docx` skill — UK spelling, standard letter formatting,
   dated. Save to
   `applications/<company-slug>_<role-slug>/CoverLetter_<Company>_<Role>.docx` (same slug
   convention as `cv-tailor`).

   **Also save a markdown copy** alongside the `.docx`:
   `applications/<company-slug>_<role-slug>/CoverLetter_<Company>_<Role>.md`
   This is a plain-text mirror of the same content for embedding in the pipeline dashboard
   artifact. The `.docx` remains the submission-ready version; the `.md` is the viewable-anywhere
   copy. Generate both from the same content in one pass.

8. **Update the tracker.** Step 2 already confirmed the record exists — call
   `manage_applications.py update --id <id> --cover-letter-path "<path>"` the same way
   `cv-tailor` does.

9. **Report back**: the firm-specific details used (and which of the 4 categories they fall
   into), which experiences were cited in each paragraph, and any gap flagged.

## Notes

- Confirm before overwriting an existing cover letter at the same path.
- **Yours faithfully** when the addressee is unknown; **Yours sincerely** when a name is used.
- After drafting, suggest running `/the-humanizer` as a second pass to catch AI texture —
  but don't gate on it automatically.
