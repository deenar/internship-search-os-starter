---
name: application-pipeline
description: Advance an application through its lifecycle. Use when the user names a company to work on or asks what's next for an application.
---

# Application Pipeline

Advances a single application to its next stage by reading its status and proposing the right
skill to run.

## Step 1: Identify the Application

Find the target application in `data/applications.json` by company name, role, or `APP-xxxx` ID —
`manage_applications.py find --company "<company>"` is the reliable way to do this. If the
user's request is ambiguous (e.g. just a company name with multiple entries), list the matches
and ask which one.

**No match found:** don't improvise past this. Working on an application with no ledger entry means research and drafts pile up untracked, and later statuses get skipped. Get the application
logged via `application-tracker` first — gather the required fields (company, role, source,
url) from what the user has already given you (a JD or URL usually supplies most of it) rather
than re-asking for everything — then proceed to Step 2 with the new entry.

Completion: one application identified by ID, company, role, and current status.

## Step 2: Propose the Next Action

Read the application's current `status` and propose the next skill(s) from the table below.
State what's already done (e.g. "CV drafted, cover letter missing") and what comes next.

| Status | What to propose | Transition on completion |
|---|---|---|
| `targeted` | 0. `application-strategy` (optional — for competitive/high-priority applications)<br>1. `company-research`<br>2. `cv-tailor` — produces CV, writes `cv_path`<br>3. `cover-letter` (if role requires one) — produces letter, writes `cover_letter_path`<br>4. `the-humanizer` on cover letter (optional) | Advance to `drafting` when CV exists (+ cover letter if required) |
| `drafting` | Materials are ready. Ask: "Review your CV and cover letter, then confirm when submitted." | Advance to `submitted` on user confirmation |
| `submitted` | 1. `networking-intelligence`<br>2. `followup-drafter` (if ≥14 days since submission with no `followup_sent_at`) | Status unchanged; follow-up tracked |
| `online_test` | No automated skill. Note the status and ask for an update when complete. | Advance to `interview` on user update |
| `interview` | 1. `interview-prep`<br>2. `interviewer-perspective` (optional second pass)<br>3. `mock-interview` (optional practice) | Status unchanged; prep delivered |
| `assessment_centre` | `interview-prep` re-run for AC format — save to same folder | Status unchanged; prep delivered |
| `offer` | Congratulate. Offer evaluation (career-helper #11) if comparing multiple offers. | Terminal |
| `rejected` | `post-interview-coaching` — diagnose, extract lessons, plan recovery. | Terminal |
| `withdrawn` | Already closed. No action to propose. | Terminal |

For `targeted` applications with an approaching `deadline` (< 14 days), flag the urgency
before listing the steps.

Completion: next action(s) stated with reasoning; user has confirmed which to run.

## Step 3: Run the Proposed Skill

Run the confirmed skill. After each skill completes:

- If a document was produced, verify the path was written to `applications.json` (`cv-tailor` and
  `cover-letter` do this themselves; other skills save to `applications/<company>_<role>/`
  directly).
- If all materials for the current stage are complete, propose the status advance and update via
  `application-tracker`:
  ```
  python3 .claude/skills/application-tracker/scripts/manage_applications.py \
    --applications data/applications.json update \
    --id <APP-xxxx> --status <new_status>
  ```

Completion: skill ran, outputs saved to the application folder, status advanced if warranted.

## Step 4: Report

State what was done, what files were created/updated, and what the application should advance to
next.

Completion: current status, files created/updated, and the next step stated explicitly.
