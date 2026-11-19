# Advanced techniques (optional, when stakes are high)

The nine core levers are pure-rule. 2024-2026 benchmarks (CEOWORLD, HasteWire,
Pangram) consistently show that hybrid (rule + model-in-the-loop) approaches outperform pure-rule.
When the stakes warrant the extra cost, layer one or more of these on top.

## Advanced 1: Detector-scored best-of-N

Generate 3 to 5 variants of the humanized output. Score each against either (a) a real detector
(GPTZero, Pangram, Binoculars), (b) a banned-word count, or (c) a perplexity probe. Pick the
lowest-scoring variant. Source: arXiv 2506.07001 (detector-guided adversarial paraphrasing, 87.88%
average TPR reduction across 8 detectors).

## Advanced 2: Iterative paraphrase pass

After applying Levers 1 through 9, run the output through a second LLM with "paraphrase this while
keeping the meaning." Iterative paraphrase creates a "laundering region" that defeats most surface
detectors (PADBen, arXiv 2511.00416). Diminishing returns past 2 passes.
Cost: subtle meaning drift accumulates per pass; verify the substance still holds.

## Advanced 3: Writer-profile distillation pre-step

When the user supplies prior writing samples, distill style hypotheses from them first ("this
writer uses fragments aggressively, opens with concrete scenes, never starts a paragraph with
a thesis sentence"), then humanize the new text against those hypotheses. Source: HyPerAlign
(arXiv 2505.00038). More effective than raw few-shot.

## Advanced 4: Self-rewrite distance sanity check

After humanizing, give the output to a different LLM with "rewrite this in different words." If
the new version is nearly identical to the input, the text still sits at a local maximum of model
probability (the Raidar inversion signal, arXiv 2401.12970) and reads as AI. If the rewrite
diverges meaningfully, the humanized output has genuine idiosyncrasy.

## Advanced 5: Embedding-guided synonym swap (when implementable)

Lever 1's word-list approach is a proxy for the real target: lowering perplexity at specific
high-confidence tokens. Embedding-guided substitution (arXiv 2501.18998) picks synonyms that
explicitly lower Fast-DetectGPT scores. When tooling is available, prefer it over the static
word-list.

## Advanced 6: Disfluency injection (casual register only)

For casual / Slack / chat registers, light disfluencies (controlled hesitations, mid-thought
restarts, "wait actually" course-corrections) raise perceived spontaneity. Source: arXiv 2412.12710.
Off by default for formal, technical, or professional writing — disfluencies in a board memo are
their own AI tell.

## What NOT to do (documented dead ends)

- **Homoglyph injection (SilverSpeak, arXiv 2406.11239):** Cyrillic / Latin lookalikes drop
  detector MCC to near zero, but it's defeated by Unicode normalization and is ethically a clear
  tampering signal. Skip.
- **Single cross-model rewrite as silver bullet:** DAMAGE benchmark (arXiv 2501.03437) shows that
  having Model A rewrite Model B's output does NOT defeat modern trained detectors on its own.
- **Watermark stripping:** Out of scope for stylistic humanization. Tools exist (RLCracker
  arXiv 2509.20924, De-mark arXiv 2410.13808) but live in a separate problem space.
