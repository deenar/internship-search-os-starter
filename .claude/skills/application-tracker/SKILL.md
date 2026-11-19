---
name: application-tracker
description: Log a new internship application or update an existing one's status. The write path for data/applications.json — use progress-summary for read-only reporting.
---

# Application Tracker

Records application state into `data/applications.json` so `progress-summary` and
`followup-drafter` always work off accurate data. Owns this file exclusively — rows are never
deleted (status changes to `rejected`/`withdrawn` instead).

## a) Add a new application

1. **Gather required fields** — don't proceed on assumptions:
   - `company`, `role` (exact title), `source` (`trackr`/`linkedin`/`company_site`/`other`),
     `url`, `deadline` if stated, `location` if known.
   - If the user gives a URL without details, fetch the posting to confirm
     company/role/deadline before logging.
2. **Check for duplicates** — the script rejects matching company+role, but mention it to the
   user (they likely mean `update`).
3. **Run the script**:
   ```
   python3 manage_applications.py --applications ../../../../data/applications.json add \
     --company "<Company>" --role "<Role>" --source <source> \
     --url "<url>" [--location "<City>"] [--deadline <YYYY-MM-DD>] [--date-found <YYYY-MM-DD>] \
     [--notes "<free text>"]
   ```
4. **Report** the new `id` and offer to run `application-pipeline`.

## b) Update an existing application

1. **Identify the application** — ask for the `id` if more than one entry matches the company.
2. Valid `--status` values: `targeted` → `drafting` → `submitted` → `online_test` →
   `interview` → `assessment_centre` → `offer` / `rejected` / `withdrawn`. Non-linear jumps
   are valid.
3. **Run the script**:
   ```
   python3 manage_applications.py --applications ../../../../data/applications.json update \
     --id <APP-xxxx> [--status <status>] [--date <YYYY-MM-DD>] [--deadline <YYYY-MM-DD>] \
     [--role "<Role>"] [--location "<City>"] \
     [--cv-path "<path>"] [--cover-letter-path "<path>"] \
     [--followup-due <YYYY-MM-DD>] [--followup-sent-at <YYYY-MM-DD>] \
     [--notes-append "<free text>"]
   ```
   `--date` applies to the status change (defaults to today); auto-populates `date_submitted`
   on first `submitted`. `cv-tailor` and `cover-letter` call this with `--cv-path`/
   `--cover-letter-path` themselves.

   `--role`/`--location` correct a mis-recorded title or backfill a missing city — use these
   rather than hand-editing the JSON when a posting turns out to have a longer or more precise
   title than what was first logged (a Trackr row often carries a generic title the real JD
   later expands). Neither touches `status` or `status_history`.
4. On `submitted`: suggest `--followup-due` two weeks out. On `offer` or `rejected`:
   acknowledge it directly.
5. **Report** exactly what the script printed.

## c) Check whether an application already exists

Every other skill that writes into `applications/<company>_<role>/` must run this before
producing any document (see CLAUDE.md's Ground rules for skills). Cheaper and more reliable
than eyeballing `data/applications.json` directly.

```
python3 manage_applications.py --applications ../../../../data/applications.json find \
  --company "<Company>" [--role "<Role>"]
```

Exits non-zero with no output on no match — treat that as "no ledger entry yet," not as a
tool failure to report and move past.

## Testing

`tests/test_manage_applications.py` — run with
`python3 -m unittest tests/test_manage_applications.py -v` after any script change.
