<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Determinism and Reproducibility — Why the Same Input Produces a Different Answer, and What to Do About It

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/18-determinism-and-reproducibility.md)**

**Version**: 1.0.0
**Content hash**: sha256:06a5d737806a (of the body below, excluding the stamp comment, this line, and the version line)

"It worked a second ago — why isn't it working now?" is one of the most
common, and most commonly misdiagnosed, questions in an AI agent
project. This crystal separates **why it's non-deterministic** from
**how to make it trustworthy without full determinism**.

## Basis (primary source verified)

🟢 Verified the abstract of "Non-Determinism of 'Deterministic' LLM
Settings" (arXiv:2408.04667) directly — across 5 LLMs and 8 tasks, it
empirically measured **the phenomenon where the same input produces
different output "even under settings expected to be deterministic."**
"Naturally occurring accuracy variance across runs reached up to 15%,"
and the performance gap between the best and worst runs reached up to
70%. The cause the source itself points to is **"co-mingled data in
input buffers" for efficient use of compute resources** — that is,
batching itself. (This session verified only the abstract; it did not
review the full source for the specific mathematical proof of
floating-point non-associativity — a phenomenon known to exist, but
this document does not overstate having verified that level of detail.)

## Why "temperature=0 means deterministic" should be considered wrong

A common misconception: "if temperature=0, you always get the same
answer." In reality, **the infrastructure serving the model (batching,
parallel GPU computation) takes a slightly different floating-point
computation path depending on the order/grouping of requests, producing
variance even in settings that should be deterministic in theory** —
this is exactly the phenomenon the paper above measured empirically.
In other words, "the setting is deterministic" and "it actually behaves
deterministically in production" are different claims, and the latter
needs to be verified separately.

## Three response strategies for when full determinism isn't possible

### 1. Keep core judgments stable; tolerate variation in phrasing
Wording (word choice, ordering) varying slightly from run to run is
generally not a problem. The problem is when the **core judgment
(pass/fail, a numerical conclusion, an action to take)** varies —
distinguish the two, and spend stability-verification resources only on
the latter.

### 2. Buy stability with a majority vote — self-consistency
Independently sampling the same judgment multiple times and taking the
majority vote is more stable than a single run —
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)'s
stage 5 (self-consistency re-scoring) is a concrete pipeline
implementation of this principle. The difference between this crystal
and 04: 04 covers **an evaluation pipeline's cost trade-off** ("only
verify ambiguous cases by majority vote"), while this crystal covers
**the root cause** — "why does the same input produce a different
answer in the first place?"

### 3. Measure the variance itself and log it
Instead of just assuming "it's deterministic," actually run the same
input multiple times and measure the variance (metrics like the paper's
TARr@N/TARa@N — the rate at which the raw output matches across N runs,
and the rate at which the parsed answer matches). This measurement
itself is a concrete application of the "logs, not claims" principle in
[11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md),
and it's the actual measurement method for criterion 4
(reproducibility) in [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md).

## Distinguishing when full determinism matters from when it doesn't

| Situation | How much does determinism matter |
|---|---|
| Output requiring creativity (drafts, brainstorming) | Low — variance can even be useful as diversity |
| Automated judgment run repeatedly (pass/fail, classification) | High — variance directly means a collapse of trust |
| Safety-related judgments (whether to execute an irreversible action) | Very high — must always be combined with self-consistency or a human-check gate |

**What not to do**: shrug off variance in repeated judgments that don't
require creativity as "well, it's AI, can't be helped" — at least one
of the three response strategies above is applicable.

## Related crystals
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
  How to apply self-consistency cost-effectively within an evaluation
  pipeline.
- [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) — Requires
  reproducibility as an item on the quality baseline.
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) —
  Connects to the rule that incident records distinguish "a reproducible
  failure" from "a failure that only occurs probabilistically."
