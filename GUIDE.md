# Internship Search OS — Getting Started Guide

A set of Claude Code skills that act as your internship-application assistant. You talk to
Claude in plain English ("what's new on Trackr?", "tailor my CV for this role", "prep me for my
interview") and it finds roles, keeps a tracker of every application, drafts tailored CVs and
cover letters, and gets you ready for interviews.

**It never applies or sends anything for you.** It drafts documents and keeps the tracker up to
date. You check everything, then submit and send it yourself.

---

## 1. What you need

| Thing | Why | Required? |
|---|---|---|
| A Claude account with Claude Code (Pro or Max) | Runs everything | Yes |
| [Claude desktop app](https://claude.ai/download) (Code tab) or the `claude` CLI | Where you chat with it | Yes |
| Python 3 (already on most Macs: run `python3 --version` to check) | Runs the application tracker | Yes |
| Git | Keeps a history of your files | Recommended |
| Claude in Chrome extension | Lets `role-finder` scan Trackr automatically | Optional |
| A GitHub account | Only for the optional live dashboard | Optional |

## 2. Set up (about 20 minutes)

### Step 1: Put the folder somewhere sensible

Unzip or clone it into, for example, `~/Developer/internship-search-os`. Then open it in Claude
Code: in the desktop app, go to the **Code** tab and choose this folder. In a terminal, run:

```bash
cd ~/Developer/internship-search-os
```

```bash
claude
```

### Step 2: Fill in your master CV in `data/profile.json`

**This is the most important step.** Every CV and cover letter is built only from what's in this
file. Claude won't invent experience; if a job asks for something that isn't here, it tells you
instead of making it up.

The easiest way to fill it in is to ask Claude to do it:

> Here's my current CV [paste it, or drag in the PDF/Word file]. Fill in data/profile.json from
> it. Keep the existing structure, don't invent anything, and ask me about anything unclear.

Then read through the result yourself. Every bullet should be something you could defend in an
interview. Add things that aren't on your CV yet (societies, competitions, projects, online
courses). The skills choose which items to show for each application, so a long list here is
fine.

### Step 3: Tell it who you are in `.claude/CLAUDE.md`

Open `.claude/CLAUDE.md` and fill in the two sections marked with `[brackets]` at the top:

- **Who this is for**: your name, degree, university, year, graduation date, what you're
  aiming for (e.g. "UK finance summer internships for Summer 2027").
- **Target roles**: which sectors to look at, anything to exclude, firms you're keen on.

You can also ask Claude to do this: *"Help me fill in the Who this is for and Target roles
sections of CLAUDE.md. Ask me questions."*

The rest of the file is the "house style" (one-page CVs, UK spelling, UK date format, cover
letters of 300–400 words that mention something specific about the firm). Change it if you want
something different.

### Step 4 (optional): Start a git history

```bash
git init && git add -A && git commit -m "Initial setup"
```

This lets you undo mistakes and see what changed. Claude can make commits for you if you ask.

### Step 5 (optional): Install Claude in Chrome

`role-finder` reads the [Trackr UK finance table](https://app.the-trackr.com/uk-finance/summer-internships)
in a browser. Install the Claude in Chrome extension and connect it to Claude Code. Without it,
everything else still works; you just add roles yourself by pasting job links.

## 3. Everyday use

You don't need to remember any commands. Just say what you want. You can also type `/` followed
by a skill name to run that skill directly.

### Find roles

> What's new on Trackr?   *(or `/role-finder`)*

It scans Trackr, leaves out roles you're already tracking, ranks the rest by how urgent they
are, and shows you a table. You choose which ones to add to your tracker.

Found a role elsewhere (LinkedIn, a careers site)? Paste the link:

> Add this to my tracker: https://…

### Work on an application

> Work on my [Company] application   *(or `/application-pipeline`)*

It checks how far that application has got and suggests the next step. A typical order is:

1. **`company-research`**: what the firm does, recent news, culture, things to mention.
2. **`cv-tailor`**: a one-page `.docx` CV aimed at that job description.
3. **`cover-letter`**: a `.docx` letter that mentions something specific about the firm.
4. **`the-humanizer`** (optional): rewrites phrasing that sounds AI-written.

Everything for that application is saved to `applications/<company>_<role>/`.

**When you've submitted it yourself, tell Claude:** *"I submitted the [Company] application
today."* This marks it as submitted and starts the follow-up timer.

### Keep track

> Where do things stand?   *(or `/progress-summary`)*

Shows how many applications are at each stage, deadlines in the next 7 days, and which ones are
due a follow-up.

> Which applications should I chase?   *(or `/followup-drafter`)*

Drafts follow-up emails for you to send yourself.

### Interviews and assessments

| Say… | Skill |
|---|---|
| "Prep me for my [Company] interview" | `interview-prep`: likely questions, plus STAR answers built from your profile |
| "What is the interviewer looking for?" | `interviewer-perspective`: what each question is really testing |
| "Give me a mock interview" | `mock-interview`: a live practice round with feedback |
| "Who should I network with at [Company]?" | `networking-intelligence`: people to contact, with draft messages |
| "I got rejected by [Company]" | `post-interview-coaching`: what went wrong and what to do next |

### Update the tracker as things happen

Just say what happened: *"[Company] sent me an online test"*, *"I have an interview with
[Company] on 3 December"*, *"Rejected by [Company]"*. The application stages are:

```
targeted → drafting → submitted → online_test → interview → assessment_centre → offer
```

(plus `withdrawn` / `rejected`). Nothing is ever deleted, so rejections stay on record and help
you spot patterns.

## 4. Where your stuff lives

| File / folder | What it is | Edit by hand? |
|---|---|---|
| `data/profile.json` | Your master CV | Yes. Add to it whenever you do something new |
| `data/applications.json` | Your application tracker | **No.** Ask Claude to update it |
| `applications/<company>_<role>/` | Tailored CVs, letters, research, prep | Yes, it's your output |
| `.claude/CLAUDE.md` | Your details, target roles, house style | Yes |
| `.claude/memory/session_log.md` | Short notes on what each session did | Claude keeps it |
| `.claude/skills/` | The skills themselves | Only if you want to change how a skill works |

## 5. Rules worth knowing

- **Nothing made up.** If a job wants a skill you don't have in `profile.json`, Claude will
  point out the gap rather than hide it. You can add the skill to your profile (if it's true) or
  go ahead without it.
- **No generic cover letters.** If Claude can't find something specific about the firm, it will
  ask you instead of writing filler.
- **Every application is in the tracker before any documents are made**, so nothing gets lost.
- **LinkedIn is never scraped automatically**, because that can get your account restricted.
  Pasting a single LinkedIn job link is fine.
- **You submit everything yourself.**

## 6. Optional: live dashboard

`dashboard/pipeline.html` is a web page that reads your tracker from GitHub and shows it as a
board. To use it:

1. Push this folder to a **private** GitHub repo called `internship-search-os`.
2. In `dashboard/pipeline.html`, replace `YOUR-GITHUB-USERNAME` (it appears twice) with your
   GitHub username.
3. Ask Claude: *"Publish dashboard/pipeline.html as an artifact and save its URL to memory."*

Use a private repo. Your tracker and CV details go in it.

## 7. Tips

- **Keep `profile.json` up to date.** After each new society role, competition or course, tell
  Claude: *"Add this to my profile: …"*
- **Start a new chat for each task.** `.claude/memory/session_log.md` carries context between
  chats, so you don't need one very long conversation.
- **Read every document before sending it.** Claude drafts; you're the one who signs it.
- **Something wrong?** Say so (e.g. "that cover letter is too generic", "don't lead with that
  bullet"). If you want a change to stick for every future session, ask Claude to add it to
  `.claude/CLAUDE.md`.

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| A skill doesn't seem to exist | Make sure Claude Code is opened **in this folder**. Skills load from `.claude/skills/` |
| "No ledger entry found" | Expected. Add the application first (paste the job link), then try again |
| `role-finder` can't open Trackr | Check Claude in Chrome is installed and connected, or paste job links yourself |
| Tracker script errors | Check `python3 --version` works. To test the script, run `python3 -m unittest tests/test_manage_applications.py -v` |
| CV runs over one page | Ask: "Trim this to one page; drop the least relevant items" |

---

Includes two third-party skills: **career-helper** (CC BY-NC 4.0, by Paul Bratcher / Prosper
Consulting; see `.claude/skills/career-helper/README.md`) and **the-humanizer**. Free for
personal, non-commercial use.
