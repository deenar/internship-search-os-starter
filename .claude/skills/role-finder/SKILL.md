---
name: role-finder
description: Scan Trackr for new UK finance internship roles and propose a shortlist. Use when the user wants to find new roles or check what's opened recently.
---

# Role Finder (Trackr)

**Scans** the public Trackr summer-internships table, triages untracked roles by temporal
urgency, and proposes a shortlist. This skill only proposes; `application-tracker` is the write
path.

Requires Claude-in-Chrome browser tools (`navigate`, `javascript_tool`, `tabs_context_mcp`).

## Workflow

1. **Build the dedup set.** Read `data/applications.json` — every existing `company + role` pair
   (lowercased). Completion: set populated before navigation.

2. **Navigate** to `https://app.the-trackr.com/uk-finance/summer-internships`. If a login wall
   appears, stop and tell the user.

3. **Confirm scope** (if not already stated this session): which categories to include (default:
   all) and whether to restrict to "2027" programme names (default: include both, flag
   ambiguity). Read [`trackr-structure.md`](trackr-structure.md) for triage bucket definitions
   and DOM layout. Completion: user has confirmed or accepted defaults.

4. **Run the extraction script.** Open [`extraction_script.js`](extraction_script.js), substitute
   the dedup set into `trackedPairs`, apply any category filter, and run via `javascript_tool`.
   Completion: structured results returned with per-bucket counts.

5. **Present one collapsed table**, ordered: `upcoming` → `open_rolling` → `overdue` →
   `opening_soon`. Columns: Type | Company | Programme | Category | Date(s) | Link.
   - State bucket counts (including `closed` and `unannounced_later`) so the user sees what's
     excluded.
   - Flag `possible_ineligible: true` rows inline.
   - Cross-check near-match programme titles against already-tracked companies (the typo-dedup
     gotcha in `trackr-structure.md`).
   Completion: every triaged result accounted for — presented, flagged, or excluded with counts.

6. **Ask which to add.** Accept a list, range, or "all of these."

7. **Add each selected role** via `application-tracker`'s script:
   ```
   python3 .claude/skills/application-tracker/scripts/manage_applications.py \
     --applications data/applications.json add \
     --company "<Company>" --role "<Programme Name>" --source trackr \
     --url "<trackr_company_url>" [--deadline <closing_date>] \
     --notes "Trackr: category=<category>; stage=<latest_stage>; rolling=<rolling>; process=<process>; last cycle opened <last_year_opened>. <original Notes column text>"
   ```
   Only pass `--deadline` when `closing_date` is non-null. Completion: every selected role
   added without error.

8. **Report**: how many added, and remind the user that `trackr_company_url` is Trackr's
   reference page — they may need the firm's actual application portal for drafting.
