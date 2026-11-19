# Trackr DOM Structure & Triage Buckets

Disclosed reference for [`role-finder`](SKILL.md). Read this at step 3 (triage classification)
and step 4 (extraction script).

## Table structure

URL: `https://app.the-trackr.com/uk-finance/summer-internships`

15 columns: `My Status, Company Name, Programme Name, Opening Date, Closing Date, Latest Stage,
Last Year Opening, Process, Info & Test Prep, Rolling, CV, Cover Letter, Written Answers,
Sponsors Visa, Notes`.

Category section headers (`Bulge Bracket`, `Elite Boutique`, `Middle Market`, `Buy-Side`, `Asset
Management`, `Trading and Quant`, `Consulting`, `Big 4`, `Real Estate`, `Pensions and Insurance`,
`Accounting and Audit`, `Miscellaneous`, `Promoted`) are single-cell `<tr>` rows interleaved with
15-cell data rows — track "current category" as you walk the table.

Date format: `DD Mon YY` (e.g. `02 Jul 25`).

## Triage buckets

Classify every untracked row into one of five temporal buckets before presenting. Compare dates
against today's ISO date — sort by urgency, not by raw date string.

| Bucket | Condition | Urgency |
|---|---|---|
| `upcoming` | Real `Closing Date`, still future | Highest — sort soonest-first |
| `open_rolling_no_deadline` | Real `Opening Date` ≤ today, no `Closing Date` | High — accepting applications now |
| `overdue_vs_last_year` | No real dates, but `Last Year Opening` + 1 year < today | Medium — "should" have opened by now; check firm's careers page directly |
| `opening_soon` | Same estimate falls within the next 30 days | Low — watch list |
| `unannounced_later` | Everything else | Background — don't surface in full, just counts |

To compute the estimate: parse `Last Year Opening` (`DD Mon YY`), then set year+1
(e.g. `02 Jul 25` → estimated `2026-07-02`).

## Dedup gotcha

Trackr's own programme-name text can have a typo (e.g. "Quantitative Reseacher" missing an "r")
that won't match a corrected spelling used when the role was first logged. When a result looks
suspiciously similar to an already-tracked company+role (same company, near-identical programme
name), flag it as a likely duplicate rather than re-adding it blind.
