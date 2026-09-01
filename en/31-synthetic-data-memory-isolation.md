<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Synthetic Data ↔ Persistent Memory Isolation — When Fake Eval Inputs Masquerade as Real History

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/31-synthetic-data-memory-isolation.md)**

**Version**: 1.0.0
**Content hash**: sha256:5f822bb88a52 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟡 Generalized purely from a real incident in the
original project. It belongs to the same lineage as software engineering's
general "separate test data from production data" principle, but this
document itself hasn't cross-checked that general literature against its
primary sources.

## The Problem

When an agent has **both** (a) an eval harness that actually runs a skill,
and (b) a persistent memory file (preference/history log) that accumulates
real interactions with the user, this incident can occur structurally: the
eval harness feeds a synthetic scenario into the skill while "pretending to be
the user," and the skill, simply carrying out its normal behavior of
"recording newly surfaced facts to persistent memory," ends up **storing the
synthetic input indistinguishably from actual user history**. Repeat the eval
enough times and events that never happened accumulate as if they "happened"
repeatedly — the deeper problem isn't so much that something untrue got
stored, but that **there's no longer a way to tell whether what's stored is
real or synthetic**.

## Why This Is a Separate Axis

This is different both from the guardrails that block pattern-matchable
secrets (API keys, emails) from leaking ([07-prompt-
guardrails/](07-prompt-guardrails/)) and from the guard against
project-wide confidential information ([23-confidential-project-
protection.md](23-confidential-project-protection.md)) — what leaks here
isn't a secret but **a fact whose provenance is contaminated**. Regex can't
catch it — a sentence produced by the eval harness is formatted identically to
one an actual user really said.

## Response Principles

1. **Structurally mark that this is an eval run** — merely writing "this is a
   test" into the prompt isn't enough (natural-language instructions can be
   dropped or ignored). Where possible, design the harness so that the eval
   execution path itself has no write permission to the persistent memory
   file, or can only write to a separate, isolated path (a test-only copy).
2. **Check the path before writing**: build a step into the skill's "context
   update" stage that, right before writing to the real production path,
   verifies whether the current run originated from the eval harness — without
   this check, the skill itself has no way to distinguish an eval run from a
   real one.
3. **On discovery, correct with an annotation rather than deleting**: when a
   contaminated record is found, don't silently delete it — instead note "this
   entry was found on review dated YYYY-MM-DD to be synthetic input from an
   eval run, and has been corrected." Deleting silently breaks the audit trail
   (who changed what, when, and why) — the same principle as "record it, don't
   hide it" in [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md).
4. **Periodic cross-checking**: occasionally scan the persistent memory file
   for specificity that could only plausibly come from a real interaction
   (an exact date, details only the user would know) — sentences produced by
   an eval harness tend to be more generic or have a templated feel, so while
   full automation is hard, a human eye tends to catch them fairly well.

## The Exact Conditions Under Which This Problem Occurs (to Prevent Overapplication)

Both of the following conditions must hold **simultaneously** for this risk to
actually apply — if only one holds, it doesn't:
- The agent has an eval/test harness that runs a skill end-to-end (a
  structure with simple unit tests that verify only a single function doesn't
  count).
- The skill's normal behavior itself includes the side effect of "writing
  facts surfaced during execution to persistent memory" (a skill that behaves
  like a pure function — input to output only, leaving no state behind —
  doesn't count).

## Related
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
  the design of the eval harness itself. This crystal is the additional
  isolation rule needed when that harness targets **a skill that leaves side
  effects**.
- [07-prompt-guardrails/](07-prompt-guardrails/) — isolation of
  pattern-matchable secrets/PII (a different target from this crystal — that
  one is about "format," this one is about "provenance").
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) —
  the basis for correcting a discovered contaminated record via annotation
  instead of deletion.
