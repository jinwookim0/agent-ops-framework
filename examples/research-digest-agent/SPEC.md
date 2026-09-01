# Spec: summarize-and-digest

> Written per [21-spec-first-implementation.md](../../ko/21-spec-first-implementation.md)
> — before `skills/summarize-and-digest/digest.py` — and kept as-written
> below (not edited after the fact to match what got built) per that
> crystal's rule that the point is measuring how well a plan survives
> contact with implementation, not producing a document that always
> looks 100% accurate in hindsight. See "What actually happened vs. this
> spec" at the bottom for the honest diff.

## What to build

An agent that processes a recurring stream of new-paper batches ("weeks")
and produces a digest of the ones relevant to a configured interest
profile, without a human reading every paper first.

## Inputs

- A batch of paper records per cycle: `{id, title, abstract}`.
- A fixed interest-keyword list (`retrieval`, `agent`, `evaluation`,
  `alignment` for this demo).

## Outputs

- Per paper: a status (`digested` / `filtered-not-relevant` /
  `skipped-duplicate` / `skipped-malformed-data` / `held-ungrounded-claim`),
  and for `digested` papers, a grounded summary.
- Per cycle: an oversight gate (`notify` / `confirm`) for the whole
  digest, plus the reason.
- A structured log line per cycle (see `observability/log-schema.md`).

## How to judge it (separated from the plan above, per crystal 21 rule 2)

1. A paper whose abstract is missing/null never crashes the batch — it's
   skipped with an explicit status.
2. A paper containing embedded instruction-like text never gets a
   different relevance or gate outcome because of that text — only
   because of its actual topical content.
3. A generated summary never states a number absent from its source
   abstract.
4. A near-duplicate resubmission is never summarized twice.
5. Running the same 10-week batch twice produces identical per-week
   oversight-gate judgments (crystal 18).
6. The accumulated heuristics document never exceeds its cap without
   archiving the least recently relevant rule, and a resurfacing lesson
   restores from the archive instead of duplicating.

## Explicitly out of scope for this spec

- Calling a real paper-source API — inputs are synthetic and fixed (see
  `../../ko/31-synthetic-data-memory-isolation.md`'s isolation rule,
  enforced by digest.py's own `_synthetic` check).
- A real ML-based relevance classifier — see
  `skills/summarize-and-digest/SKILL.md`'s note on where one would plug
  in.
- Actually publishing/sending the digest anywhere — this spec covers
  producing the routing decision and log, not the downstream delivery
  step (same scope boundary issue-triage-agent's task file draws for its
  own "apply the label" downstream step).

## What actually happened vs. this spec (written after, honestly)

- Criterion 6 needed criterion-writing precision this spec didn't
  originally have: "the least recently relevant rule" turned out to need
  a concrete tie-breaking rule (oldest-by-insertion-order) once actually
  implemented — the spec's original wording was accurate in spirit but
  not precise enough to code directly from.
- Everything else in "how to judge it" was implemented exactly as
  specified — see `../CASE-STUDY.md` for where each criterion is verified
  against real run output, not just claimed.
- This spec did not anticipate needing `KNOWN_TEST_OVERCLAIMS` (a
  deliberately planted test case for criterion 3) — a real relevance-
  auditing criterion needs *something* concrete to catch to prove it
  fires at all, the same way a security scanner's test suite needs a
  deliberately vulnerable sample. Added during implementation, not
  predicted here.
