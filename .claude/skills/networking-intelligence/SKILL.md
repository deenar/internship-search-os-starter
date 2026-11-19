---
name: networking-intelligence
description: Identify 8-12 strategic contacts at a target company with personalised outreach messages. Use when the user wants to network into a company or at the submitted stage.
---

# Networking Intelligence

Parallel web research to identify high-value connections at a target company, tiered by
warmth and strategic value.

## Inputs

- Company name and target role (required)
- `data/profile.json` (for connection angles — shared university, interests, experience)
- Application status (check `data/applications.json`)

## Workflow

1. **Confirm a ledger entry exists** — run
   `manage_applications.py find --company "<company>"`. No match: stop and get the application
   logged via `application-tracker` first (see CLAUDE.md's Ground rules for skills).

2. **Read `data/profile.json`** for background context that shapes connection angles.

3. **Load the networking engine.**
   Load @`../career-helper/supporting-prompts/networking-strategy.md` and use template
   @`../career-helper/templates/networking-intelligence-template.md`.

4. **Save output** to `applications/<company>_<role>/networking-intelligence.md`.

5. **Report** the top 3-5 contacts with the strongest connection angles and suggested
   outreach timing. Completion: every identified contact has a tier, an angle, and a
   message draft.
