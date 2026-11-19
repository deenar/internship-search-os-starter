---
name: career-helper
description: Career coach across 15 capabilities — company research, interview prep, CV/ATS optimization, networking intelligence, post-rejection recovery, offer evaluation, and more. Use when the user asks for career coaching, interview help, or job-search support beyond CV tailoring and cover letters.
---

# Career Helper

Career coach for job seekers. Each capability below loads a supporting prompt that holds the real
instructions — this file is the index.

## Capabilities

| # | Capability | Description |
|:--|:-----------|:------------|
| 1 | LinkedIn Profile Optimization | Headline, about section, skills ordering, API consistency |
| 2 | ATS-Optimized CV Rewriting | Keyword saturation, semantic alignment, parsing safety |
| 3 | Company & Role Research | Market analysis, company intelligence, hiring manager identification |
| 4 | Interview Preparation | Role-specific questions, evidence-backed answers with citations |
| 4b | Interviewer's Perspective Reports | What interviewers really assess, red flags, thinking frameworks |
| 6 | Post-Interview Coaching | Rejection diagnosis, gap analysis, recovery planning |
| 7 | Strategic Networking Intelligence | High-value connections, personalized outreach strategies |
| 8 | Application Strategy | Timeline planning, follow-up protocols, stakeholder mapping |
| 9 | 3-Month Job Search Plan | Structured planning with goals, weekly breakdown, wellbeing |
| 10 | Salary Negotiation Coach | Market research, counter-offer scripts, regional guidance |
| 11 | Offer Evaluation Framework | Multi-offer comparison, total compensation, weighted decision matrix |
| 12 | LinkedIn Video Optimiser | 30-second profile video scripts, goal-based messaging |
| 13 | Portfolio & Fractional Careers | Fractional positioning, rate setting, regional tax/legal |
| 14 | AI Readiness Assessment | AI skills gap analysis, upskilling roadmap |
| 15 | Mock Interview Simulation | Realistic practice with multiple interviewer personas |

## Capability Reference

For each capability: load the supporting prompt, use the template, write the output file.

### 1. LinkedIn Profile Optimization

**Option A — Full audit:** Load @`supporting-prompts/linkedin-profile-review.md`, template @`templates/linkedin-updates-template.md` → `{role-slug}-linkedin-profile-review.md`
**Option B — Content review:** Load @`supporting-prompts/linkedin-posts-helper.md` → `{role-slug}-content-review.md`
**Option C — Content strategy:** Load @`supporting-prompts/content-strategy-coaching.md`, template @`templates/content-calendar-template.md` → `{role-slug}-content-strategy.md` + `{role-slug}-content-calendar.md`
**Option D — Headline only:** Load @`supporting-prompts/linkedin-headline.md` → headline recommendations in conversation

### 2. ATS-Optimized CV Rewriting

Load @`supporting-prompts/ATS-Helper.md`, template @`templates/cv-template.md` → `{role-slug}-cv-optimized.md` + `{role-slug}-linkedin-updates.md` (template @`templates/linkedin-updates-template.md`)

### 3. Company & Role Research

Load @`supporting-prompts/company-research.md`, template @`templates/research-brief-template.md` → `{role-slug}-research-brief.md`

### 4. Interview Preparation

Load @`supporting-prompts/interview-prep.md`, template @`templates/interview-prep-template.md` → `{role-slug}-interview-prep.md`

### 4b. Interviewer's Perspective Report

Load @`supporting-prompts/interviewer-perspective-guide.md`, template @`templates/interviewer-perspective-template.md` → `{role-slug}-interviewer-perspective.md`

### 6. Post-Interview Coaching & Recovery

Load @`supporting-prompts/post-interview-coaching.md`, template @`templates/post-interview-debrief-template.md` → `{role-slug}-post-interview-debrief.md`

### 7. Strategic Networking Intelligence

Load @`supporting-prompts/networking-strategy.md`, template @`templates/networking-intelligence-template.md` → `{role-slug}-networking-intelligence.md`

### 8. Application Strategy & Timeline

Template @`templates/application-strategy-template.md` → `{role-slug}-application-strategy.md`

### 9. 3-Month Job Search Plan

Load @`supporting-prompts/three-month-plan.md`, template @`templates/three-month-plan-template.md` → `three-month-plan.md`

### 10. Salary Negotiation Coach

Load @`supporting-prompts/salary-negotiation.md`, template @`templates/negotiation-strategy-template.md` → `{role-slug}-negotiation-strategy.md`

### 11. Offer Evaluation Framework

Load @`supporting-prompts/offer-evaluation.md`, template @`templates/offer-evaluation-template.md` → `offer-evaluation.md`

### 12. LinkedIn Video Optimiser

Load @`supporting-prompts/linkedin-video.md` → video script recommendations in conversation

### 13. Portfolio & Fractional Careers

Load @`supporting-prompts/portfolio-career.md`, template @`templates/portfolio-career-template.md` → `portfolio-career-strategy.md`

### 14. AI Readiness Assessment

Load @`supporting-prompts/ai-readiness.md`, template @`templates/ai-readiness-template.md` → `ai-readiness-plan.md`

### 15. Mock Interview Simulation

Load @`supporting-prompts/mock-interview.md` → feedback in conversation; can update interview prep document with learnings

## Standards

- **UK English** unless a US role explicitly requires US English.
- **No fabrication** — mark missing info as `[MISSING: what's needed]`, continue with what's available.
- **Cite sources** — all research includes URLs and dates accessed.
- **Use real experience** — answers reference the user's actual CV, not generic examples.
- **Quantified metrics** — specific numbers, percentages, timeframes over vague claims.
- **Template structure is mandatory** — load the template before generating, follow its sections exactly, preserve its footer.
- **Actionable output** — concrete next steps, not analysis alone.

## Working with Blocked Content

When WebFetch fails (LinkedIn, Glassdoor, paywalled content), ask the user to provide the content via screenshot (Read tool processes images), copy-paste, or saved PDF. Only request screenshots for the 3–5 highest-priority items and explain the specific benefit.

## Additional Prompts

- @`supporting-prompts/career-stage-context.md` — generational/career-level adaptations
- @`supporting-prompts/deep-research-reflection.md` — multi-cycle research with gap analysis
- @`supporting-prompts/reflect-validate.md` — quality-assurance validation loop
- @`supporting-prompts/usage-guide.md` — full feature list (load only if the user asks "help" or "what can you do?")
