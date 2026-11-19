---
name: followup-drafter
description: Draft a follow-up email for an internship application that's been submitted with no response for a while. Use when the user asks for a follow-up email, wants to check which applications are due a follow-up, or asks "should I chase X yet". Drafts text only — this project has no email-sending capability, so the user always sends it themselves.
---

# Follow-up Drafter

Drafts follow-up email text for applications sitting in `submitted` (or `online_test`) status
with no update for a while. **This skill never sends anything** — there is no email-sending tool
connected in this project (confirmed with the user 2026-07-03). It only produces text for the
user to copy, review, and send themselves.

## Workflow

1. **Read `data/applications.json`.** An application is due a follow-up if:
   - `status` is `submitted` or `online_test` (don't chase before submission, and don't chase
     something already at `interview`+ — that's a different conversation with the firm, not a
     status-check follow-up), and
   - `followup_sent_at` is null (don't draft a second follow-up without being asked), and
   - it's been ≥14 days since `date_submitted` (or since `followup_due` if set — that field lets
     the user or `application-tracker` override the default window per application).
2. If the user asked generally ("what needs a follow-up") rather than naming one application,
   list every match from step 1 with company/role/days-since-submitted, and ask which to draft
   for (or draft for all of them if the user says so).
3. **Draft the email** — short (under 150 words), professional, UK tone:
   - Reference the specific role and the date applied.
   - State continued interest specifically (not "just checking in") — tie back to one concrete
     reason from the original cover letter/CV if one exists at `cover_letter_path`.
   - Ask a direct, low-friction question: current stage of the process / expected timeline.
   - No need to ask for a name/contact — if a contact isn't in `notes`, keep it addressed to the
     recruitment team/generic greeting rather than inventing a name.
4. **Present the draft to the user as text** — don't write it to a file unless asked; this is
   short-lived content meant to be copied into an email client.
5. **After the user confirms they've sent it**, update the tracker:
   ```
   python3 ../application-tracker/scripts/manage_applications.py \
     --applications ../../../../data/applications.json update \
     --id <APP-xxxx> --followup-sent-at <YYYY-MM-DD>
   ```
   Don't set `followup_sent_at` before the user confirms it was actually sent — this skill has no
   way to verify sending itself.

## Notes

- If `application-tracker` set a `followup_due` date explicitly (e.g. because the posting stated
  a specific response timeline), honour that over the 14-day default.
- Never draft a follow-up for a `rejected`/`withdrawn`/`offer` application — there's nothing to
  chase.
