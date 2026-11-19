---
name: application-strategy
description: Tactical plan for a specific application — timeline, stakeholder map, risks. Optional at targeted, before the standard research-CV-cover-letter sequence.
---

# Application Strategy

Front-loads strategic thinking for competitive or high-priority applications where the default
pipeline sequence isn't enough.

## Workflow

1. **Confirm a ledger entry exists** — run
   `manage_applications.py find --company "<company>"`. No match: stop and get the application
   logged via `application-tracker` first (see CLAUDE.md's Ground rules for skills). Otherwise
   note the entry's deadline and check for existing research at
   `applications/<company>_<role>/research-brief.md`.

2. **Use the strategy template.**
   Template @`../career-helper/templates/application-strategy-template.md` for output structure.
   No dedicated supporting prompt — draws on company research if available.

3. **Save output** to `applications/<company>_<role>/application-strategy.md`.

4. **Report** the recommended approach sequence, key risks, and suggested timeline. Propose
   advancing to the pipeline's standard sequence with the strategy's priorities informing
   emphasis.
