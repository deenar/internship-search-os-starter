---
name: pipeline-refresh
description: Rebuild and republish the internship pipeline dashboard artifact with the latest application data, documents, and deadlines. Use when the user says "refresh the dashboard", "update the artifact", "rebuild the pipeline", or after any batch of application/document changes.
---

# Pipeline Refresh

Rebuilds the pipeline dashboard artifact from the current state of
`data/applications.json` and all associated `.md` documents, then republishes to
the existing artifact URL. This is the only skill that touches the artifact — other
skills produce the data it consumes.

## Data sources

Read these in order:

1. **`data/applications.json`** — the application ledger. Every application becomes an
   entry in the `APPS` array. Map fields directly:
   - `id`, `company`, `role`, `source`, `deadline`, `status`, `date_found`, `notes`
   - `url` → goes into the `APP_URLS` lookup object
   - `cv_path` → `cv: true/false` (non-null = true)
   - `cover_letter_path` → `cl: true/false` (non-null = true)

2. **`career-outputs/<slug>-*.md`** — career-helper outputs (company research, networking
   intelligence, interview prep). Match to applications by slug (the `<slug>` prefix
   corresponds to the company/role slug in applications.json). Each file becomes an entry
   in the `DOCS` object under the application's id.

   Mapping convention:
   - `*-research-brief.md` → `docs: ["research"]`, key `research` in DOCS
   - `*-networking-intelligence.md` → `docs: ["networking"]`, key `networking` in DOCS
   - `*-interview-prep.md` → `docs: ["interview"]`, key `interview` in DOCS

3. **`applications/<company>_<role>/*.md`** — markdown copies of tailored CVs and cover
   letters (produced by `cv-tailor` and `cover-letter` skills). If present, add as
   `cv_md` and `cl_md` keys in DOCS for that application, and make them available as
   tabs in the detail panel.

   Matching convention:
   - `CV_*.md` → key `cv_md` in DOCS, tab label "CV"
   - `CoverLetter_*.md` → key `cl_md` in DOCS, tab label "Cover Letter"

## What to rebuild

The artifact is a single self-contained HTML file. Only the **data sections** inside the
`<script>` block change on refresh — never modify the CSS, HTML structure, markdown
parser, or rendering logic unless the user explicitly asks for a UI change.

Data sections to regenerate:

- `const TODAY = new Date(YYYY, M, D);` — set to today's date (month is 0-indexed)
- `const APPS = [...]` — rebuild from applications.json
- `const DOCS = {}; DOCS["APP-XXXX"] = {...}` — rebuild from .md files. **Embed the full
  markdown content** of each file as a JS string (escape backticks, newlines, quotes).
  Do NOT condense or summarise — the full content includes external links (LinkedIn
  profiles, source citations, company pages) that the markdown parser renders as
  clickable `<a>` tags.
- `const APP_URLS = {...}` — rebuild from application `url` fields
- Header date display (`<span class="header-date">`) — update to today
- Footer snapshot date — update to today

## Embedding .md content

When reading `.md` files to embed as JS strings:

1. Read the full file content
2. Escape for JS string literal: `\` → `\\`, `"` → `\"`, newlines → `\n`, backticks
3. Assign as: `DOCS["APP-XXXX"].research = "...escaped content...";`
4. Preserve ALL markdown links — these render as clickable external links in the detail
   panel. The artifact's CSP does not block `<a href>` navigation, only embedded
   resource requests.

## Publishing

Republish to the **same artifact URL** so the user's bookmark/link stays valid. Use the
Artifact tool with the `url` parameter pointing to the existing artifact. The current
URL is stored in the session — if not available, use `Artifact action: "list"` to find
the pipeline artifact by title "Internship Pipeline".

The artifact file lives at (or should be written to):
`/tmp/claude-0/-home-user-internship-search-os/*/scratchpad/pipeline.html`
(use the scratchpad directory for the current session).

## When NOT to use this

- Don't run this automatically after every single application change — it's meant to be
  invoked explicitly or on a schedule, not as a post-hook on every tracker update.
- If the user asks for a UI change (new column, different layout, new view), that's a
  separate task — this skill only refreshes data.
