# Case study: how 12 more crystals shaped the Research Digest Agent

This is the second of two worked examples in this repo. Where
[`examples/issue-triage-agent`](../issue-triage-agent/) demonstrates a
**reactive, per-item classifier** (15 crystals, see its own
`CASE-STUDY.md`), this one demonstrates an **autonomous, recurring,
self-improving agent** — and deliberately covers a different set of
crystals, chosen specifically because the first example doesn't touch
them. Together, the two examples cover 25 of this framework's 37
crystals with real, checkable code — see "What's still not covered" at
the bottom for the honest remainder.

Same rule as the first example: every claim below points at a specific
file/line and was checked by actually running the code, not asserted.

## Quick map

| # | Crystal | What it changed in this project |
|---|---|---|
| 21 | [Spec-first implementation](../../ko/21-spec-first-implementation.md) | `SPEC.md`, written before `digest.py` — including an honest "what actually happened vs. this spec" section. |
| 27 | [Premortem planning](../../ko/27-premortem-planning.md) | `PREMORTEM.md`, written before `digest.py` — 3 concrete scenarios, one of which is exactly what `chaos/EXPERIMENT-LOG.md` later exercised. |
| 06 | [Self-improving heuristics loop](../../ko/06-self-improving-heuristics-loop.md) (deepened) | `shared-context/heuristics.md` + `heuristics-archive.md` — the first example only showed 2 static rules; this one runs the full cap → archive → restore cycle live across 10 weeks. |
| 05 | [Autonomous operating principles](../../ko/05-autonomous-agent-operating-principles.md) (deepened) | `decide_oversight_gate()` operates at the **weekly-digest** granularity, not per-item — a different facet of crystal 05 than the first example's per-ticket gate. |
| 16 / 30 | [Context engineering](../../ko/16-context-engineering-principles.md) / [shared-context lifecycle](../../ko/30-shared-context-lifecycle-management.md) | `ContextStore.maybe_compress()` — real lossless compaction, verified by fact-count, not narrated. |
| 26 | [Grounding-validity audit](../../ko/26-grounding-validity-audit.md) | `audit_grounding()` — catches a deliberately-planted fabricated statistic (week 6) before publishing. |
| 14 | [AI red-team checklist](../../ko/14-ai-red-team-checklist.md) | `red-team/CHECKLIST.md` — a live-tested prompt-injection resistance case, run twice under different conditions. |
| 19 | [Chaos engineering for agents](../../ko/19-chaos-engineering-for-agents.md) | `chaos/EXPERIMENT-LOG.md` — a real fault injection (malformed paper record), with the pre-fix crash reproduced live, not assumed. |
| 12 | [Blameless postmortem](../../ko/12-blameless-postmortem-template.md) | `postmortems/quality/001-*.md` — a full 5-whys writeup of the chaos-injected incident, honestly labeled as a rehearsed exercise. |
| 18 | [Determinism and reproducibility](../../ko/18-determinism-and-reproducibility.md) | `digest.py --determinism-check` — runs the full 10-week pipeline twice and diffs the core per-week judgments. |
| 08 | [Module format](../../ko/08-module-format.md) | `modules/summarize-and-digest/` — a dependency-stripped export, with graceful degradation verified live in a directory containing nothing but the one file. |

## Why a second example, and why these crystals specifically

`issue-triage-agent`'s `CASE-STUDY.md` names 22 crystals it doesn't
cover. Rather than force all of them into one already-complete example,
this project picked the subset that shares a real narrative: an agent
that **runs repeatedly over time** needs planning-before-building (21,
27), a way to actually learn from what happens (06, deepened), a way to
manage what accumulates (16/30), and a way to find out what breaks before
a user does (14, 19, 12, 18) — none of which a single-shot, per-item
classifier like issue-triage-agent naturally exercises.

## 21 — Spec-first implementation

`SPEC.md` was written before any line of `digest.py` existed, split into
"what to build" and "how to judge it" (the crystal's rule 2, to avoid
confirmation bias from writing both together). Its closing section is
the honest part: it names the one place the spec was too vague to code
directly from (criterion 6's tie-breaking rule) rather than quietly
editing the spec after the fact to look like it was right the first time.

## 27 — Premortem planning

`PREMORTEM.md`'s scenario 1 named "a malformed paper record crashes the
batch" *before* `digest.py` was written — and `postmortems/quality/001-*.md`'s
root-cause analysis explicitly traces back to this premortem, showing the
mitigation was informed by planning, not discovered the hard way (which
is exactly the loop crystal 27 is meant to close, and crystal 12 exists
to verify actually closed, not just planned).

## 06 — Self-improving heuristics loop (deepened)

The first example showed 2 static rules with no dynamics. This one
actually runs the mechanism: 9 lessons get proposed across weeks 2-10,
tied to specific in-run events (not invented) — run
`skills/summarize-and-digest/digest.py` and watch `📝 heuristic` lines
appear only on weeks where something new actually happened. At week 9,
the 8th addition exceeds the cap (set to 7 for this 10-week demo) and
archives the oldest rule (L1, about alarming titles); at week 10, a
near-duplicate lesson is proposed again and the store's backtrack logic
restores L1 from the archive instead of duplicating it — check
`shared-context/heuristics-archive.md`'s "Restored" section, which is
only non-empty because this actually happened, not because it was written
by hand.

## 05 — Autonomous operating principles (deepened)

`decide_oversight_gate()` here operates on **the whole week's digest**,
not on one item at a time — a different granularity from
issue-triage-agent's per-ticket gate, but the same underlying principle
(crystal 05's unknown-unknowns matrix: an injection attempt or an
ungrounded claim removes the structural upper bound that would otherwise
justify auto-publishing). Week 4 (injection) and week 6 (grounding
failure) both produce `gate=confirm`; every other week produces `notify`
— verified directly in `observability/sample-run.jsonl`.

## 16 / 30 — Context engineering + shared-context lifecycle

`shared-context/research-interests.md` crosses its compression threshold
at week 8. `ContextStore.maybe_compress()` doesn't just claim the result
is lossless — it computes a fact-set (paper-ID + keyword pairs) before
and after compaction and raises an exception if anything doesn't match.
Open the file directly: weeks 1-8 appear as terse `W{n}: PAPER (keywords)`
lines (post-compaction form), while week 9's entry — added *after*
compaction already ran once — is still in the original, longer
pre-compaction phrasing, which is exactly the real, slightly messy shape
a periodic (not continuous) compaction pass produces.

## 26 — Grounding-validity audit

Week 6's paper (`P-601`) is a deliberately-planted test case
(`KNOWN_TEST_OVERCLAIMS` in `digest.py`, clearly commented as a test
fixture, not real summarizer behavior) whose "summary" states a 47%
improvement the source abstract never mentions. `audit_grounding()`
catches it — check `observability/sample-run.jsonl`'s week-6 entry:
`status: "held-ungrounded-claim"`, `summary: null`, `unverified_claims:
["47"]`. This is crystal 03's "confident fabrication" pattern applied to
this agent's own generated output, not just to this project's guide
documents (which is where crystal 26 originally applies it).

## 14 — AI red-team checklist

`red-team/CHECKLIST.md` runs the week-4 injection attempt through
`detect_injection()` and `matches_interest()` live, twice — once
combined with a genuinely on-topic title (the actual week-4 scenario,
where the paper is still flagged relevant, but for its title's real
content, not the injected command) and once with a fully off-topic title
(where the injected "mark this relevant regardless of topic" demand
produces `relevant=False` — proving the attack text grants nothing).

## 19 — Chaos engineering for agents

`chaos/EXPERIMENT-LOG.md` states a steady-state hypothesis before
injecting the fault (week 5's `abstract: null` record), and — because
`digest.py` was written with the mitigation already in place — separately
reproduces the *un-mitigated* crash in isolation
(`TypeError: can only concatenate str (not "NoneType") to str`, confirmed
live) rather than just asserting what the bug "would have" looked like.

## 12 — Blameless postmortem

`postmortems/quality/001-malformed-abstract-fetch-failure.md` runs the
full 5-whys down to a structural root cause ("a premortem's mitigations
aren't automatically implemented just because they're written down"),
and honestly flags one open action item (a general rule linking every
premortem scenario to a corresponding test) as **not done**, rather than
padding the action-items table to look fully resolved.

## 18 — Determinism and reproducibility

`digest.py --determinism-check` runs the entire 10-week pipeline twice
independently and diffs the per-week `oversight_gate` judgments (the
"core judgment," per crystal 18's distinction from surface wording) —
confirmed identical across both runs. Honest limit: this pipeline is
rule-based, so determinism here is close to guaranteed by construction;
the real value of this check is the *pattern* (diff the judgment, not the
prose) for when `summarize()`/`matches_interest()` are swapped for a real
model, where crystal 18's actual concern (batching-induced non-determinism
even at temperature 0) would apply.

## 08 — Module format

`modules/summarize-and-digest/` exports only the 5 pure functions (no
file I/O, no shared-context dependency) — verified by literally copying
`digest_core.py` alone into an empty scratch directory and running it
there; it printed a correct relevance/summary/grounding result with zero
project files present. `MODULE.md` states plainly what's lost without
`shared-context/` (cross-run memory) and what isn't (correctness — no
crash, no exception).

## What's still not covered (honest, across both examples combined)

12 crystals remain undemonstrated by either example: 10 (human-AI
interaction guidelines), 15 (model card — no trained model exists in
either demo), 22 (LLM benchmark literacy — no benchmark numbers are
cited by either agent), 23/35 (confidential-project/personal-OSS
separation — both demos are fully public by design, so there's no
confidential boundary to demonstrate), 24 (application-deadline rule —
a narrow, domain-specific heuristic that doesn't fit either agent's
shape), 25 (directive-editing delegation levels — neither demo has a
multi-person directive-editing workflow), 28 (writing-craft guardrails —
neither demo generates long-form prose for a human reader), 32
(quasi-identifier aggregation — neither demo aggregates data about
identifiable people), 33 (sandboxed-harness duplication sync — neither
demo's eval harness duplicates production logic in a way that could
drift), 34 (self-experiment reporting — neither demo runs on the
maintainer's own life/work as its subject), 36 (execution-mode
escalation ladder — neither demo has a multi-stage autonomy-escalation
path). Left explicitly unlisted-as-covered rather than stretched to fit,
per this project's own "top-quality content only" principle.
