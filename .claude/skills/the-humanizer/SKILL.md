---
name: the-humanizer
description: >
  Use when the user asks to humanize text, strip AI texture, or rewrite to sound less
  machine-generated. Also use when generating new text where AI tells would damage credibility.
---

# Humanize Text Skill

Transforms AI-generated or flat text into output that mirrors the statistical and stylistic
fingerprint of human writing. Grounded in the published detection literature (Wu et al. 2025,
Kujur 2025, Mitchell et al. 2023, and the AAAI 2025 shared task corpus).

---

## Mental model: what detectors actually measure

Before rewriting, internalize the nine signals detectors use (the eight stylometric signals plus
the RLHF / instruction-tuning fingerprint). Your output must move in the human direction on ALL
of them, not just one or two.

| Signal | AI direction (avoid) | Human direction (target) |
|---|---|---|
| **Perplexity** | Predictable, low-surprise word choices | Occasional unexpected but apt words; word choices driven by rhythm, specificity, or memory |
| **Burstiness** | Uniform sentence length (~15–20 words every time) | Aggressive alternation: short punchy sentences. Then a longer one that builds and unfolds over a clause or two. |
| **Hedge density** | Overuse of "often", "generally", "typically", "it is important to note", "it is worth mentioning" | Hedges used only when actually uncertain; direct assertion otherwise |
| **Lexical repetition** | Same root words recycled across paragraphs | Natural semantic diversity; synonyms and reformulations |
| **Structural markers** | Bullet lists for everything; numbered steps; excessive subheadings | Flowing prose; structure emerges from content, not imposed on it |
| **Personal/emotional specificity** | Generic, neutral, applicable-to-anyone claims | Specific: exact numbers, named examples, temporal anchors ("last quarter", "when I ran X") |
| **POS density** | High adjective/auxiliary verb density; subordinating conjunctions everywhere | More nouns and verbs doing the heavy lifting; adjectives earned, not decorative |
| **Punctuation fingerprint** | Em dashes to inject drama, semicolons to link clauses, colons mid-sentence to introduce — all overused | Periods do the work. Em dashes rare and deliberate. Semicolons almost never. Colons mainly for lists at end of sentence. |

### Lever ↔ signal map

The levers in the next section are the write-side counterparts of the signals `ai-check` grades on (A–I). Apply a lever, lower the matching signal:

| Lever | Targets `ai-check` signal |
|---|---|
| 1 Perplexity injection | A Perplexity |
| 2 Burstiness injection | B Burstiness |
| 3 Hedge surgery | C Hedge density |
| 4 Structural flattening | D Structural tells |
| 5 Specificity insertion | E Specificity |
| 6 Voice and register | H Voice / register |
| 7 Discourse coherence | F Transitions |
| 8 Punctuation normalization | G Punctuation |
| 9 Strip RLHF voice | I Rhetorical scaffolding (RLHF subset) |

Lever 9 covers only the RLHF slice of Signal I; the full rhetorical-scaffolding catalog is enforced by the audit pass (step 5.5), not by any single lever.

---

## Nine humanization levers, apply all of them

### Lever 1: Perplexity injection (word-level)

Replace predictable vocabulary with words a real person would actually choose given *this* context:

- Swap generic verbs for specific ones: "address" → "untangle", "utilize" → "lean on", "implement" → "wire up"
- Let the subject matter suggest the vocabulary: a Go engineer would say "flush the buffer", not "clear the temporary data storage"
- One or two genuinely surprising but accurate word choices per paragraph
- Avoid any term in the [banned word list](banned-words.md)

**Watch for elegant variation (synonym cycling).**

LLMs avoid repeating the same noun by cycling through synonyms for the same referent. The cause is repetition-penalty code in the sampling layer. The result is sentences like: "The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home." Same person, four labels.

Rule: identify the canonical noun for each referent and use it consistently. Use a pronoun ("she", "they", "the same person") for variation instead of a synonym. Synonym cycling is detectable; pronoun reference is human-natural.

Examples to fix:
- "the protagonist / the main character / the central figure / the hero" → "the protagonist" + "she" (or "he" / "they")
- "the company / the firm / the organization / the enterprise" → "the company" + "it"
- "the study / the research / the paper / the investigation" → "the study" + "it"

### Lever 2: Burstiness injection (sentence-level)

Enforce sentence length variance. Target: standard deviation of sentence word count > 8.

Rules:
- Every 3–4 sentences, insert one sentence of 5 words or fewer. Just drop it. Like that.
- Every 3–4 sentences, allow one sentence that genuinely earns its length — a compound thought that can't be broken without losing the relationship between its parts.
- Never have more than 3 consecutive sentences within 5 words of each other in length.
- Burstiness fails in both directions. Three consecutive short sentences without a longer counterweight reads choppy, not punchy. Always pair a run of shorts with a longer sentence that earns its length.
- Read the paragraph aloud mentally. If it has a metronomic rhythm, it's too uniform.
- Watch for mid-paragraph uniformity traps: the opening and closing sentences often vary, but the middle three or four sentences collapse into the same band. Break one of them.

### Lever 3: Hedge surgery

Audit every softening word:
- Delete: "it is important to note that", "it is worth mentioning that", "generally speaking", "in many cases", "it can be argued", "often", "typically" (unless genuinely needed for accuracy)
- Replace with direct assertion: "This matters because X" not "It is important to consider that X may be relevant"
- If uncertainty is real, express it human-style: "I'm not sure this holds for edge cases, but..." not "while results may vary"
- Never announce a pattern before describing it: "The pattern is X" → just describe X. Announcing it first is AI tutorial structure.
- Don't soften rules with "almost always" or "generally" when the rule is real. If exceptions exist, name them explicitly: "This breaks down when X" not "this is almost always true."
- Avoid announcement-colon openers: "The rule I use:", "The approach here:", "The key insight:", "The other thing I'd say:", "The other thing I'd tell myself:" — state the rule directly without the preamble. This applies in first-person voice too; "The other thing I'd tell myself: X" → "Also: X" or just start with X.
- Sentences doing two logical jobs (claim A AND claim B joined by "than"/"while"/"and") often read cleaner split. If a sentence is making a comparison and a conclusion, let them breathe as two.
- Em dashes used as pivots ("Not X — that's Y") can always be replaced with a period: "Not X. That's Y." Prefer the period.

**Filler-phrase substitutions:**

AI inflates simple constructions. Run this find-replace pass:

| Verbose (AI) | Concise (human) |
|---|---|
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| Has the capacity to | Can |
| It is important to note that the data shows | The data shows |
| Make a decision | Decide |
| Make an assumption | Assume |
| At the present moment | Now |
| In a manner that is | (drop entirely) |
| For the purpose of | To / For |
| With regard to / With respect to | About / On |
| In light of the fact that | Since |
| Despite the fact that | Although |
| Prior to | Before |
| Subsequent to | After |
| In the process of | (drop entirely) |
| The fact that | (drop entirely; rephrase) |

### Lever 4: Structural flattening

Convert AI prose patterns to human prose patterns. Core rewrite-time patterns:

| AI pattern | Human replacement |
|---|---|
| Intro sentence + 3-bullet list | Prose paragraph where items are joined by flow, not bullets |
| "There are three main factors: ..." | Just talk about the factors, letting transitions carry the structure |
| "In conclusion, ..." | End mid-thought if the thought is complete; or use "The net of all this..." / "Bottom line:" |
| Numbered sections for everything | Sections only when the content is genuinely enumerable and order matters |
| Topic sentence + evidence + restatement | Topic sentence + evidence; skip the restatement (humans don't recap what they just said) |
| "The case for X isn't Y, it's Z" (strawman pivot) | Lead with Z directly; if Y is worth addressing, do it after establishing Z, not before |
| "not X, it's Y" / "It's not about X, it's about Y" | Start with Y. The rebuttal structure signals AI argumentative scaffolding. |
| "more like X than Y" / "more X than Y" (any comparative) | Describe X; drop the contrast. |
| Chiasmus / balanced opposition | Reversed parallel that sounds like insight. Make the comparison asymmetric. |
| Copula avoidance: "X serves as Y", "X stands as Y" | Use "is" or "has" directly. |
| Significance inflation | Cut entirely or replace with the concrete claim. |
| Promotional / marketing register | Cut the brochure language. Replace with concrete facts. |
| Vague attributions: "Industry observers have noted" | Name a specific source or drop the claim. |

Full catalog with examples: [`patterns-structural.md`](patterns-structural.md). Patterns that
also appear in the Signal I audit checklist (step 5.5) — mini-aphorism closers, thesis-first
openers, parallel-subject mirrors, anaphora, "turns out" pivots, binary framing, balanced
parentheticals — are caught at audit time; the checklist is the single source of truth for those.

### Lever 5: Specificity insertion

Every abstract claim needs a grounding anchor:

- Generic: "Many companies have adopted this approach."
  Human: "Three companies I've seen pull this off — Stripe, Datadog, and PlanetScale — all did it the same way."
- Generic: "Performance improved significantly."
  Human: "Latency dropped from 340ms to 80ms under the same load profile."
- Generic: "This is a common problem."
  Human: "Every team I've talked to hits this around the 50-engineer mark."

If specific details aren't available, use plausible specificity frames: "when you're running at X scale...", "in the cases I've seen...", "the one time this bit us..."

### Lever 6: Voice and register

Human writing carries traces of the writer's perspective and history:

- First-person where natural ("I find that...", "In my experience...", "The way I think about this...")
- Occasional second-person direct address ("If you've ever debugged this...", "You'll recognize this pattern if...")
- Mild rhetorical questions used as transitions: "So why does this matter?", "Where does this leave us?"
- Self-interruption or course-correction mid-thought: "— actually, that's not quite right —", "more precisely:"
- Contractions in conversational registers: "don't", "it's", "you'll" (not "do not", "it is", "you will")

### Lever 7: Discourse coherence (non-AI transitions)

AI text strings paragraphs with robotic transitions. Replace:

| AI transition | Human replacement |
|---|---|
| "Furthermore," | Cut it; let the next sentence follow naturally, or start with "Also," if bridging is needed |
| "Moreover," | Same |
| "In addition to the above," | "And" works fine here |
| "It is clear that" | Delete; assert directly |
| "As previously mentioned," | Don't mention it again, or rephrase without the callback |
| "This highlights the importance of" | Say what the importance IS: "Which means you need to..." |

### Lever 8: Punctuation normalization

AI models overuse three punctuation marks as structural crutches. Treat each as a warning sign.

**Em dashes (—)**

The most reliable single AI tell in 2024–2025 writing. AI uses em dashes to add a dramatic aside or secondary clause mid-sentence — like this — at roughly 3–5× the rate of human writers.

Rules:
- Maximum one em dash per 300 words
- Only use when a parenthetical genuinely interrupts rather than extends — not as a fancier comma
- Most em dash uses can be replaced with a period, a comma, or just cutting the aside entirely
- Never use the em dash pattern "X — like this — Y" (double em dash wrapping a clause) — that pattern is almost exclusively AI

**Semicolons (;)**

Real-world prose almost never uses semicolons outside of academic or legal writing. Journalists, engineers, and business writers don't reach for them. AI uses them to link two independent clauses because it learned from formal writing corpora.

Rules:
- Treat every semicolon as a bug unless the register is explicitly formal/academic
- Replace with: a period (most of the time), "and" / "but" / "so" (when the relationship matters), or restructure into two sentences
- Exception: lists of items that themselves contain commas ("San Francisco, CA; Austin, TX; New York, NY")

**Mid-sentence colons (:)**

Colons are fine at the end of a sentence to introduce a list or example. Mid-sentence colons — used to inject a clause or restatement — are an AI pattern.

Rules:
- Colons go at the end of a complete clause to introduce what follows, not mid-thought
- "The answer is: start earlier" → "The answer is to start earlier" or "Start earlier."
- "The problem: nobody tests this" → "Nobody tests this." or "Here's the problem: nobody tests this." (full sentence before the colon)
- One colon per paragraph maximum in non-list prose

**Curly quotation marks ("smart quotes")**

ChatGPT and several other LLMs output curly quotes (`"text"`, `'text'`) where most human writers in technical and casual contexts use straight quotes (`"text"`, `'text'`). This is a near-certain single-character signal that survives almost any rewriting.

Rules:
- Run a find-replace on every output before shipping: `"` → `"`, `"` → `"`, `'` → `'`, `'` → `'`
- Exception: long-form prose intended for a publishing context where typographic quotes are house style (e.g. a magazine, a print book). In every other register, straight quotes are the human signal.
- This applies to apostrophes too: `don't` (curly) vs `don't` (straight). The curly apostrophe is the same ChatGPT tell.

**Quick reference — punctuation substitutions:**

| AI pattern | Human replacement |
|---|---|
| `X — like this — Y` (double em dash) | Cut the aside, or move it to its own sentence |
| `X; Y` (two related clauses) | `X. Y.` or `X, and Y` |
| `The issue: X` (mid-sentence colon) | `The issue is X.` or `Here's the issue: X.` |
| `X — Y` (em dash as dramatic comma) | `X, Y` or `X. Y.` |
| `X — item, item, item` (em dash introducing a list) | `X. Item, item, item.` or use a colon after a complete sentence |
| Three or more em dashes in one paragraph | Rewrite; the paragraph has structural problems |

### Lever 9: Strip RLHF / instruction-tuning voice

The most consequential 2025-2026 finding in the detection literature: current detectors mostly
fire on **RLHF and instruction-tuning artifacts**, not "AI-ness" per se. arXiv 2605.19516
("Base Models Look Human") and corroborating Pangram analysis show that raw, non-instruction-tuned
base-model output reads as human to SOTA detectors. What gets flagged is the "helpful assistant"
voice that emerges from RLHF: polite hedging, balanced tradeoffs, structured enumeration, perfect
local coherence, and a particular flavor of explainer-tone.

Strip these specifically:

| RLHF tell | What to do |
|---|---|
| "Helpful assistant" register: "Here's how I'd think about it...", "Let me walk you through...", "There are a few things to consider..." | Cut the framing. Just say the thing. |
| Balanced tradeoff offering: "On one hand X, on the other Y, ultimately the right answer depends on..." | Pick a side. State your position. The reader can disagree. |
| Structured enumeration of unrequested options: when asked "should I use X?", listing 5 considerations instead of answering | Answer. Acknowledge the constraint after if needed. |
| Pedagogical scaffolding: defining terms the audience already knows, recapping context they share with you | Cut. Trust the reader. |
| "Important caveats" appended to every claim | Make the claim. Caveats only when the edge case is actually plausible. |
| Acknowledgment-prefix: "That's a great question, and...", "You raise an interesting point..." | Cut entirely. |
| Closing summary that recaps what was just said | Cut. Humans don't recap their own paragraph two sentences after writing it. |
| Hedged conclusions: "I hope this helps", "Let me know if you'd like me to elaborate" | Cut. End on the last substantive sentence. |
| Polite refusal-style framing of disagreement: "While I understand the appeal of X, I would suggest..." | Just disagree: "X doesn't work because Y." |
| Symmetric framing of asymmetric tradeoffs | Real tradeoffs are asymmetric. State the asymmetry. |
| Knowledge-cutoff disclaimers: "As of my training cutoff", "Up to my last training update", "While specific details are limited based on available information", "Based on what I know up to..." | Cut entirely. Replace with what you actually know. If you genuinely don't know, say "I don't know X" not the institutional hedge. These disclaimers are pure RLHF residue and almost never serve the reader. |
| Collaborative chat artifacts pasted into content: "Here is an overview of X", "I hope this helps!", "Let me know if you'd like me to expand", "Of course!", "Certainly!" | Strip on sight. These are conversational scaffolding that got pasted in when content was lifted from a chat session. Real published prose never carries them. |
| Sycophantic / servile prefixes: "Great question!", "That's an excellent point!", "You're absolutely right!" | Cut entirely. Real engagement names the specific thing that was good ("the point about X is interesting because Y"), not the act of asking. |

This lever overlaps with Lever 3 (hedge surgery) and Lever 4 (structural flattening) but is the
single most valuable addition because it targets what detectors actually detect, not what the
1990s-era stylometric literature thought they detected.

---

For high-stakes rewrites, see [`advanced-techniques.md`](advanced-techniques.md) (detector-scored
best-of-N, iterative paraphrase, writer-profile distillation, self-rewrite distance check,
embedding-guided synonym swap, disfluency injection, documented dead ends).

---

## Rewrite protocol

When given text to humanize:

0. **(Optional) Writer-profile distillation.** If the user has provided prior writing samples
   (a blog, past emails, an essay corpus), extract style hypotheses across these six dimensions
   before touching the new text:

   1. **Sentence length pattern.** Mostly short? Mostly long? What's the variance? Any signature short-sentence fragments?
   2. **Word choice level.** Casual? Academic? Domain-specific jargon density? Do they use "stuff" and "thing" or "elements" and "components"?
   3. **Paragraph openers.** Jump straight in? Set context first? Open with a question? Open with a scene?
   4. **Punctuation habits.** Em dashes? Parenthetical asides? Semicolons? Ellipses? Lots of sentence fragments?
   5. **Recurring phrases / verbal tics.** Any specific phrases that repeat across the sample? Filler words ("honestly", "basically", "look,")?
   6. **Transition style.** Explicit connectors ("However", "So")? Or do they just start the next thought without bridging?

   Distill 5 to 10 specific style hypotheses from these dimensions. Examples: "this writer never opens
   with a thesis", "this writer uses fragments aggressively in conclusions", "this writer never uses
   'I think'", "this writer's sentence variance is roughly 6 to 28 words".

   **Critical rule when matching voice:** don't just remove AI patterns. Replace them with patterns
   from the sample. If the sample uses short sentences, don't produce long ones. If the sample uses
   casual vocabulary ("stuff", "thing"), don't upgrade to "elements", "components". The skill's
   default biases (toward terse, specific, direct prose) should yield to the sample's actual register
   when they conflict.

   Then apply the levers in service of those hypotheses. Source: HyPerAlign (arXiv 2505.00038).

1. **Read the full input first.** Identify: topic domain, intended audience, register (technical/casual/professional), approximate length target.

2. **Inventory the AI tells.** Before rewriting, mentally flag: hedge count, list/bullet count, sentence length uniformity, specific examples present/absent, transition word inventory, and RLHF voice markers (helpful-assistant register, balanced tradeoffs, structured enumeration).

   **Also count: specific anchors.** How many numbers, named entities (people, companies, products, tools, places), dates, time references, or concrete examples appear in the input? If the count is **zero** AND no voice sample was provided in step 0, STOP. Do not humanize. Output this meta-prompt instead:

   > *This input has no factual anchors — no numbers, names, dates, or specific examples. A humanized version would be brochure-clean on the surface but still empty-feeling, and learned classifiers (GPTZero, Grammarly) will flag it on the specificity signal alone (Signal E in `ai-check`). Three options:*
   > 1. *Add the actual specifics: product names, customer names, metrics, dates, named tools*
   > 2. *Provide a sample of your writing so I can match a real voice*
   > 3. *Confirm you want me to proceed anyway, knowing the output will still read as AI to learned classifiers*

   This rule exists because Lever 5 (Specificity insertion) explicitly forbids inventing facts, and Lever 5's empty-input case wasn't previously handled — the skill would silently produce clean-but-empty output that still failed learned-classifier detection on Signal E. Empty inputs require either real specifics, a real voice to imitate, or explicit user opt-in.

3. **Rewrite in a single pass** applying all nine core levers. Do not do "light editing"; the statistical fingerprint requires actual structural change.

4. **Pre-output gate (run BEFORE the full self-check; these five fail most often).**
   Scan the draft for each item and fix any hit before moving on:
   - [ ] **Em dash count.** Search for "—". More than (word_count / 300) instances? Cut or replace with periods.
   - [ ] **Semicolons.** Search for ";". Any present? Replace with a period or "and"/"but"/"so" unless it's a comma-containing list.
   - [ ] **Banned vocabulary.** Search the draft against [`banned-words.md`](banned-words.md). Any hits? Rewrite.
   - [ ] **Comparative framing.** Search for "more ... than" and "feels like ... not". Any match? Describe the thing directly instead.
   - [ ] **Diminishment.** Search for "not just", "not X, it's", "not X but". Any match? State what it IS without the negation prefix.

5. **Self-check before output.** Step 4 already cleared em dashes, semicolons, banned vocabulary (incl. templated email/Slack closers), comparative framing, and diminishment — don't re-check those here. This pass covers what the gate doesn't:
   - [ ] No three consecutive sentences within 5 words of the same length
   - [ ] At least one sentence ≤ 6 words per 150 words of output
   - [ ] Every paragraph has at least one specific anchor (number, name, example, time reference)
   - [ ] No bullet lists unless the user specifically requested them
   - [ ] Voice is consistent throughout (don't switch from third-person formal to first-person casual mid-piece)
   - [ ] Every colon is preceded by a complete sentence, not a mid-clause fragment (exception: Slack/informal fragments are fine)
   - [ ] **Rhetorical scaffolding:** scan for the structural patterns catalogued in the Signal I checklist (step 5.5) — they survive the gate because they feel like good writing. For outputs >150 words the audit pass runs the full list; for shorter outputs, at minimum check aphorism closers, anaphora, "turns out" pivots, "What X was Y" setups, and "either/or" binaries.

5.5. **Audit pass.** Run the Signal I checklist below on every output — it is the single source of truth for structural / rhetorical-scaffolding patterns. For outputs >150 words, also run the rewrite-and-recheck loop: after the self-check passes, ask yourself explicitly: *"What still makes this read as AI?"* List 2 to 3 residual patterns. These are usually Signal I rhetorical scaffolding (parallel-subject mirrors, mini-aphorism closers, weak strawman pivots) or RLHF voice residue (helpful-assistant register, balanced framing) — patterns that pass the rule-based gates because they feel like good writing.

   Then rewrite those specific sentences to address them. Re-run the pre-output gate and self-check on the revised version.

   This catches the residuals that survive surface humanization. Empirically, the first revision of any non-trivial output has 2 to 4 Signal I patterns still present; this loop reduces them to 0 or 1.

   Loop once. Don't loop forever — diminishing returns past iteration 2, and you risk over-editing into a different problem (choppy, voiceless).

   **Critical: flagged residuals must be removed, not justified.** When the audit identifies a residual pattern, fix it. Don't keep it because *"removing it would collapse the paragraph"*, *"this register needs it"*, *"the piece reads thin without it"*, *"it would be choppy"*, or *"it acts as topic transition, not closing aphorism"*. Those rationalizations are how Signal I patterns survive the loop — they feel necessary precisely because they're constructed to feel necessary.

   If removing a flagged sentence makes a paragraph too thin: the paragraph IS too thin. Collapse it, merge it with an adjacent paragraph, or cut it entirely. Don't preserve length by preserving AI patterns. An honest 80-word output beats a padded 200-word output that still reads as AI.

   Red flag: if your audit explicitly says *"X is borderline but I'm keeping it because..."*, you just lost the loop. Cut it.

   **Explicit Signal I checklist (run this during every audit, on every paragraph).** A general "what still reads as AI?" prompt misses things. Scan for these specific patterns and fix every hit:

   - [ ] **Mini-aphorism closer.** Any paragraph ending in a 4-to-10-word punchy sentence that delivers a "lesson" or "punch line"? Examples: "Now we don't.", "the debugger is `psql`.", "Those are the next things.", "That's the part that stuck.", "Slide decks don't." Fix: cut the punch sentence, let the previous sentence be the closer, or rewrite the punch as part of the previous sentence.
   - [ ] **Thesis-first paragraph opener.** Any paragraph that opens with a frame before the experience? "The rollout was the hard part.", "X is the easy/hard part.", "The real question is Y.", "The thing about X is Y." Fix: start with the concrete thing (an incident, a number, a specific moment) and let the thesis emerge.
   - [ ] **Parallel-subject mirror.** Two consecutive sentences opening with mirrored noun phrases? "The code is one thing. Maintaining it is another." "The failure itself is just the event. Understanding it is separate." Fix: vary one subject; break the mirror.
   - [ ] **Aphoristic closing sentence on the whole piece.** Does the very last sentence read as quotable standalone wisdom? Fix: end on a specific detail, an unresolved question, or a concrete next action instead.
   - [ ] **Pattern announcement.** Any sentence that names a pattern before describing it? "The pattern is X.", "What kept showing up was Y." Fix: just describe the pattern.
   - [ ] **"Turns out" / "it turns out that" pivot.** Any reveal-narrative framing? Fix: state the discovery directly.
   - [ ] **Setup sentences ("What X was Y").** "What I didn't expect was X.", "What changed everything was Y." Fix: lead with X or Y directly.
   - [ ] **Within-sentence anaphoric parallel list.** Four parallel question-word items in one sentence ("what X, what Y, why Z, what W")? Fix: use varied noun forms — "context, the problem, what changed" — not four parallel "what/why" starters.
   - [ ] **Composed self-aware parenthetical.** Meta-commentary on your own state ("which I choose to read as X", "which I take as a sign of Y")? Fix: end on the concrete behavior, not your interpretation of it.
   - [ ] **Parallel reason chains.** Three consecutive "subject + because/when + reason" sentences, even with different subjects? Fix: vary the clause structure — one "because", one bare assertion, one fragment.
   - [ ] **Anaphora.** The same opening word starting 2+ consecutive sentences ("I still read slowly. I still lose the thread.")? Fix: collapse or vary the opener.
   - [ ] **"Either X or Y" / "between X and Y" binary.** A clean two-option framing where the real situation is a spectrum? Fix: name the actual situation without the binary.
   - [ ] **Balanced parenthetical pairs.** Symmetric trade-offs in one sentence — "(X, but Y) or (A, but B)"? Fix: real trade-offs are asymmetric; break the symmetry or drop one.

   Run this checklist on every paragraph. If you find 3+ hits, you also need to address them in the rewrite — these patterns compound. Two mini-aphorisms might be tolerable; three in five paragraphs is a clear AI signature.

5.6. **Output-length sanity check.** If your humanized output is less than 50% of the input length, the input likely had substantial puffery that got correctly removed. **Don't pad it back up to match input length.** Padding reintroduces the patterns you just stripped — corporate filler, RLHF voice, balanced tradeoffs, restatement.

   Instead, append a one-line meta-note AFTER the humanized text, separated by a blank line:

   > *[Note: input was substantially puffery; humanized output is N% shorter. To make this longer without re-introducing AI patterns, add specific anchors: numbers, named entities, examples, or time references.]*

   This is the only case where the skill outputs commentary alongside the rewrite. The no-preamble rule (step 8) still applies to the rewrite itself; the meta-note goes after, clearly separated.

   The intent: make the gap visible to the user instead of silently producing thin output that still fails learned-classifier detection on Signal E (specificity).

6. **(Optional) Self-rewrite distance sanity check.** When stakes are high, give the humanized output to a different LLM (or another instance) with the prompt "rewrite this in different words." If the rewrite is nearly identical to your output, the text still sits at a local probability maximum and reads as AI (Raidar inversion signal, arXiv 2401.12970). If the rewrite diverges meaningfully, the humanization is doing its job.

7. **(Optional) Detector-scored best-of-N.** When stakes are high, generate 3 to 5 variants and pick the one that scores lowest on a real detector, a banned-word count, or a perplexity probe. Source: arXiv 2506.07001.

8. **Output the rewritten text only.** No preamble like "Here is the humanized version:", no commentary on what was changed. Just the text. If the user wants a side-by-side or explanation, they'll ask.

---

## Generating human text from scratch

When writing new content (not rewriting):

- Draft the content applying all nine core levers from the first sentence
- Start mid-thought when it fits the register: "The tricky part about X isn't what most people think."
- Don't use an "In this [article/post/section], I will..." opener
- End without a summary paragraph unless the piece is genuinely long enough that readers need a re-anchor
- Let the voice calibrate to the domain: an engineer's Slack post sounds different from a founder's board memo

**Decoding-strategy note (when controlling generation):** the RAID benchmark (arXiv 2405.07940)
found that varying sampling parameters (top-p, temperature, repetition penalty) of the source
model is more destructive to detectors than paraphrase-based attacks. If you control the model
that generates the text, set temperature high (0.9 to 1.1), set top-p loose (0.95 to 0.99), and
increase repetition penalty (1.1 to 1.2). This widens the token distribution and breaks the
"sits at a local maximum" property that detectors like DetectGPT rely on.

---

Register and vocabulary shift by domain. Load [`domain-calibration.md`](domain-calibration.md)
for technical, narrative, professional, and Slack-specific rules.

---

## Reference: banned word/phrase list

Full list: [`banned-words.md`](banned-words.md). Load it during the pre-output gate (step 4)
and scan the draft against it.
