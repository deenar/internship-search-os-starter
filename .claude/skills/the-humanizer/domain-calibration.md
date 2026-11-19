# Domain-specific calibration

## Technical (engineering, code, systems)

- Use domain-native vocabulary: "the hot path", "this falls apart at scale", "the footgun here is...", "you'll hit the edge case when..."
- Short sentences when making a definitive claim: "This is O(n²). Don't do it at scale."
- Acknowledge tradeoffs directly, not diplomatically: "The downside is real: you lose..."
- Reference real tool/library names, real version numbers, real error messages when available

## Narrative / blog / essay

- Open with a scene or specific moment, not a thesis
- Let the argument emerge from the evidence rather than being stated up front
- Use sentence fragments deliberately for rhythm. Like this.
- Include one moment of genuine uncertainty or changed mind per 500 words

## Professional / business

- Cut the throat-clearing opener: not "I hope this message finds you well" but just the message
- State the ask or point in sentence 1 or 2
- Use numbers and deadlines: "by Thursday EOD", "the three blockers are..."
- Short paragraphs (2–3 sentences max in email/memo)

## Slack / async team updates

Register collapse is the primary tell for Slack writing. AI writes Slack messages that read like polished status reports. Real Slack has:
- Abbreviations and approximations: `~60%`, `<10min`, `fwiw`, `btw`, `lmk`, `tmrw`
- **Fragment sentences and incomplete clauses throughout** — "hard commits: billing gRPC + pprof thing" not "My main commitments are the billing gRPC work and the pprof investigation"
- **Self-corrections and mid-message second thoughts**: "oh also —" or "wait, actually" signals a human who's thinking while typing, not composing
- **One thought bleeding into the next** — not topic-per-paragraph. Real messages loop back, add something that doesn't fit the structure, trail off.
- Numbers as numerals with approximation markers: `~3-4 days`, `<10min`, not "approximately three to four days"
- Single-word endings work: "lmk" as its own line
- Lowercase throughout, no capitalized paragraph openers except proper nouns
- **The structure must actually break**: accomplishment → caveat → next steps is still AI even with `fwiw` sprinkled in. Add a fourth element that doesn't fit, or loop back to something, or end with a question the message didn't set up.
