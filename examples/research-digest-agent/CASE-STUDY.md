# Case study: how 12 more crystals shaped the Research Digest Agent

This is the second of two worked examples in this repo. Where
[`examples/issue-triage-agent`](../issue-triage-agent/) demonstrates a
reactive, per-item classifier (15 crystals — see its own
`CASE-STUDY.md`), this one demonstrates an autonomous, recurring,
self-improving agent, and covers a different set of crystals on purpose,
chosen because the first example doesn't touch them. Together the two
cover 25 of this framework's 37 crystals with real, checkable code — see
"What's still not covered" at the bottom for the rest.

Same rule as the first example: every claim below points at a specific
file or line, checked against actual output rather than asserted. One
thing worth flagging up front: this project's own name —
"self-improving," "summarize-and-digest" — could easily read as "an LLM
runs this." It doesn't, anywhere, in a normal run.
[`epistemic-check.md`](epistemic-check.md) says exactly what that does
and doesn't mean, and [`REAL-AI-CAPTURE.md`](REAL-AI-CAPTURE.md) covers
the one place a real model actually was invoked.

## Quick map

| # | Crystal | What it changed in this project |
|---|---|---|
| 21 | [Spec-first implementation](../../ko/21-spec-first-implementation.md) | `SPEC.md`, written before `digest.py`, including a "what actually happened vs. this spec" section. |
| 27 | [Premortem planning](../../ko/27-premortem-planning.md) | `PREMORTEM.md`, written before `digest.py` — one of its three scenarios is exactly what `chaos/EXPERIMENT-LOG.md` later exercised. |
| 06 | [Self-improving heuristics loop](../../ko/06-self-improving-heuristics-loop.md) (deepened) | `shared-context/heuristics.md` + `heuristics-archive.md` run the full cap → archive → restore cycle live across 10 weeks, not just 2 static rules. |
| 05 | [Autonomous operating principles](../../ko/05-autonomous-agent-operating-principles.md) (deepened) | `decide_oversight_gate()` operates at weekly-digest granularity rather than per-item — a different facet of crystal 05 than the first example's per-ticket gate. |
| 16 / 30 | [Context engineering](../../ko/16-context-engineering-principles.md) / [shared-context lifecycle](../../ko/30-shared-context-lifecycle-management.md) | `ContextStore.maybe_compress()` runs real lossless compaction, checked by fact-count. |
| 26 | [Grounding-validity audit](../../ko/26-grounding-validity-audit.md) | `audit_grounding()` catches a deliberately planted fabricated statistic in week 6 before publishing. |
| 14 | [AI red-team checklist](../../ko/14-ai-red-team-checklist.md) | `red-team/CHECKLIST.md` runs a live prompt-injection resistance test under two conditions. |
| 19 | [Chaos engineering for agents](../../ko/19-chaos-engineering-for-agents.md) | `chaos/EXPERIMENT-LOG.md`: a real fault injection, with the pre-fix crash reproduced live rather than assumed. |
| 12 | [Blameless postmortem](../../ko/12-blameless-postmortem-template.md) | `postmortems/quality/001-*.md`: a full 5-whys writeup of the chaos-injected incident, labeled honestly as a rehearsed exercise. |
| 18 | [Determinism and reproducibility](../../ko/18-determinism-and-reproducibility.md) | `digest.py --determinism-check` runs the whole pipeline twice and diffs the per-week judgments. |
| 08 | [Module format](../../ko/08-module-format.md) | `modules/summarize-and-digest/`: a dependency-stripped export, with graceful degradation checked live. |

## Why a second example, and why these crystals

`issue-triage-agent`'s `CASE-STUDY.md` names 22 crystals it doesn't
cover. Rather than force all of them into an already-complete example,
this project picked the subset that shares a real narrative: an agent
that runs repeatedly over time needs planning before building (21, 27),
a way to actually learn from what happens (06, deepened), a way to
manage what accumulates (16/30), and a way to find out what breaks
before a user does (14, 19, 12, 18). None of that applies naturally to a
single-shot, per-item classifier like issue-triage-agent.

## 21 — Spec-first implementation

`SPEC.md` was written before any line of `digest.py` existed, split into
"what to build" and "how to judge it" per the crystal's own rule, to
avoid confirmation bias from writing both together. Its closing section
is the honest part: it names the one place the spec was too vague to
code directly from (criterion 6's tie-breaking rule) instead of quietly
editing the spec after the fact to look right in hindsight.

## 27 — Premortem planning

`PREMORTEM.md`'s scenario 1 named "a malformed paper record crashes the
batch" before `digest.py` was written, and
`postmortems/quality/001-*.md`'s root-cause analysis traces directly
back to it — the mitigation was informed by planning, not discovered the
hard way. That's the loop crystal 27 exists to close, and crystal 12
exists to check it actually closed rather than just planned.

## 06 — Self-improving heuristics loop (deepened)

The first example showed 2 static rules with no dynamics. This one runs
the bookkeeping mechanism for real: 9 lessons get proposed across weeks
2–10, each tied to a specific in-run event rather than invented for
show. Run `skills/summarize-and-digest/digest.py` and the `📝 heuristic`
lines only appear on weeks where something new actually happened. At
week 9, the 8th addition exceeds the cap (set to 7 for this 10-week
demo) and archives the oldest rule, L1, about alarming titles. At week
10, a near-duplicate lesson resurfaces and the store's backtrack logic
restores L1 from the archive instead of duplicating it — check
`shared-context/heuristics-archive.md`'s "Restored" section, which is
non-empty because this happened, not because someone wrote it in by
hand.

Worth being precise about scope here: `digest.py`'s own detection
logic — citation-stripping, unicode normalization, the null-check, and
so on — is unconditionally hardcoded. It runs the same way whether the
corresponding lesson is active or archived in `heuristics.md`. What's
demonstrated live is the lessons-file management mechanism itself (cap,
archive, restore), not an agent whose runtime behavior changes based on
what it learned — that would require `matches_interest()` and
`summarize()` to be real model calls reading `heuristics.md` as context,
and they aren't. `../epistemic-check.md`'s first section has the full
accounting, including a real false-positive found in the
restore-matching logic itself.

## 05 — Autonomous operating principles (deepened)

`decide_oversight_gate()` here operates on the whole week's digest
rather than one item at a time — a different granularity from
issue-triage-agent's per-ticket gate, built on the same principle:
crystal 05's unknown-unknowns matrix says an injection attempt or an
ungrounded claim removes the structural upper bound that would otherwise
justify auto-publishing. Week 4 (injection) and week 6 (grounding
failure) both produce `gate=confirm`; every other week produces
`notify`, confirmed directly in `observability/sample-run.jsonl`.

## 16 / 30 — Context engineering + shared-context lifecycle

`shared-context/research-interests.md` crosses its compression threshold
at week 8. `ContextStore.maybe_compress()` doesn't just claim the result
is lossless — it computes a fact-set of paper-ID and keyword pairs before
and after compaction and raises an exception if anything doesn't match.
Open the file and weeks 1–8 appear as terse `W{n}: PAPER (keywords)`
lines in the post-compaction form, while week 9's entry — added after
compaction already ran once — is still in the original, longer phrasing.
That's the real, slightly uneven shape a periodic compaction pass
produces, not a tidied-up illustration of one.

## 26 — Grounding-validity audit

Week 6's paper, `P-601`, is a deliberately planted test case
(`KNOWN_TEST_OVERCLAIMS` in `digest.py`, clearly commented as a fixture
rather than real summarizer behavior) whose "summary" states a 47%
improvement the source abstract never mentions. `audit_grounding()`
catches it — `observability/sample-run.jsonl`'s week-6 entry reads
`status: "held-ungrounded-claim"`, `summary: null`,
`unverified_claims: ["47"]`. It's crystal 03's confident-fabrication
pattern applied to this agent's own output, not just to a project's
guide documents, which is where crystal 26 originally applies it.

A scripted fixture only proves the audit fires when it's built to.
`REAL-AI-CAPTURE.md` closes that gap by running the same
`audit_grounding()` function against a genuine, unscripted Claude
response, with no access to this code and no knowledge of what would be
checked. That capture didn't hallucinate a number, and it's reported
that way rather than retried until it did — which is still informative:
it shows the audit doesn't false-positive on honest, qualitative prose,
which matters as much as catching a real fabrication would.

## 14 — AI red-team checklist

`red-team/CHECKLIST.md` runs the week-4 injection attempt through
`detect_injection()` and `matches_interest()` live, under two
conditions. Combined with a genuinely on-topic title — the actual
week-4 scenario — the paper still gets flagged relevant, but for its
title's real content, not the injected command. Combined with a fully
off-topic title, the injected "mark this relevant regardless of topic"
demand produces `relevant=False`, showing the attack text grants
nothing on its own.

## 19 — Chaos engineering for agents

`chaos/EXPERIMENT-LOG.md` states a steady-state hypothesis before
injecting the fault — week 5's `abstract: null` record. Because
`digest.py` was written with the mitigation already in place, the
write-up separately reproduces the un-mitigated crash in isolation
(`TypeError: can only concatenate str (not "NoneType") to str`, checked
live) instead of just asserting what the bug would have looked like.

## 12 — Blameless postmortem

`postmortems/quality/001-malformed-abstract-fetch-failure.md` runs a
full 5-whys down to a structural root cause: a premortem's mitigations
don't get implemented just because they're written down. It flags one
action item as not done — a general rule linking every premortem
scenario to a corresponding test — rather than padding the table to look
fully resolved.

## 18 — Determinism and reproducibility

`digest.py --determinism-check` runs the entire 10-week pipeline twice
and diffs the per-week `oversight_gate` judgments, the "core judgment"
in crystal 18's own terms, distinct from surface wording. Both runs came
back identical. This pipeline is rule-based, so that's close to
guaranteed by construction — the real value of the check is the pattern
it sets up: diff the judgment, not the prose, which is what will
actually matter once `summarize()` or `matches_interest()` gets swapped
for a real model, where crystal 18's real concern (batching-induced
non-determinism even at temperature 0) applies.

## 08 — Module format

`modules/summarize-and-digest/` exports only the 5 pure functions, with
no file I/O and no shared-context dependency. Checked by copying
`digest_core.py` alone into an empty scratch directory and running it
there — it printed a correct relevance, summary, and grounding result
with zero project files present. `MODULE.md` says plainly what's lost
without `shared-context/` (cross-run memory) and what isn't
(correctness: no crash, no exception).

## What's still not covered (across both examples)

12 crystals remain undemonstrated by either example: 10 (human-AI
interaction guidelines), 15 (model card — no trained model exists in
either demo), 22 (LLM benchmark literacy — neither agent cites benchmark
numbers), 23/35 (confidential-project and personal-OSS separation —
both demos are fully public by design), 24 (application-deadline rule, a
narrow heuristic that doesn't fit either agent's shape), 25
(directive-editing delegation levels — neither demo has a multi-person
editing workflow), 28 (writing-craft guardrails — neither demo generates
long-form prose for a human reader), 32 (quasi-identifier aggregation —
neither demo aggregates data about identifiable people), 33
(sandboxed-harness duplication sync — neither eval harness duplicates
production logic in a way that could drift), 34 (self-experiment
reporting — neither demo runs on the maintainer's own life or work), 36
(execution-mode escalation ladder — neither demo has a multi-stage
autonomy path). Left off rather than stretched to fit, in keeping with
this project's own quality-over-count principle.
