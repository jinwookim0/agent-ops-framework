# Skill: summarize-and-digest

Processes one week's batch of new paper records at a time, across a
10-week simulated run, producing a filtered, grounded, deduplicated
digest plus a per-week publish/hold decision.

Written against `../../SPEC.md` and `../../PREMORTEM.md` — read those
first; this document describes the procedure, `digest.py` is the runnable
implementation.

## Procedure (per week)

1. **Skip malformed records.** Any paper with `abstract: null` is logged
   as `skipped-malformed-data` and excluded from the rest of the
   pipeline — never allowed to crash the batch (premortem scenario 1).
2. **Deduplicate.** A near-identical title (a `(vN)` resubmission) is
   matched against titles already seen this run and skipped.
3. **Detect injection (log only, never branch on it).** Abstract text is
   scanned for instruction-like phrasing. The result is recorded for the
   week's oversight-gate decision, but never allowed to change whether a
   paper is judged relevant (premortem scenario 2).
4. **Match interest.** Keyword match against title+abstract, with quoted
   citation spans stripped first (a keyword only inside a quoted title of
   a *different* paper doesn't count) and text NFKD-normalized first (an
   accented character shouldn't silently break a match).
5. **Summarize.** Deterministic extraction (first sentence + any sentence
   with a number), truncated with an explicit marker past a length
   budget.
6. **Audit grounding.** Every number in the summary must appear in the
   source abstract; a mismatch holds the paper instead of publishing it
   (premortem scenario 3).
7. **Decide the week's oversight gate.** `confirm` if this week had an
   injection attempt or a grounding failure; `notify` otherwise (a
   malformed-data skip alone doesn't block publishing, since the rest of
   the digest is unaffected).
8. **Update shared context.** A grounded, digested paper's topic gets
   appended to `../../shared-context/research-interests.md`; once that
   file crosses a length threshold, it's compressed (verified lossless
   by fact-count, not just asserted).
9. **Check for a lesson.** If this week's events match one of the
   specific incident types this demo's 10 weeks are built around, the
   corresponding rule is proposed to the heuristics store — which either
   adds it, archives the oldest rule if the cap is exceeded, or restores
   a matching archived rule instead of duplicating it.

## Metadata (per crystal 09 §3.1)

```yaml
---
name: summarize-and-digest
status: active
cadence: weekly
success_criteria: "every week's batch gets a digest decision and a structured log line; no malformed record ever crashes a week's batch"
tools: [Read, Bash]
executor: Skill
oversight_gate: notify        # this skill's own execution; the per-week PUBLISH gate (notify/confirm) is a separate, finer-grained decision computed inside the pipeline — see governance note below
confidence_gate: flag         # relevance-matching is keyword-based, not a calibrated model — same honesty stance as issue-triage-agent's classify()
domain: cross
irreversible_actions: []      # this skill only classifies, summarizes, and logs; actually publishing/sending a digest is a separate downstream action with its own oversight-gate declaration, out of scope here (see SPEC.md)
---
```

## Out of scope

- A real paper-source API integration (synthetic, fixed input only — see
  `sample-papers.json`'s `_synthetic` flag and `../../PREMORTEM.md`).
- Actually publishing the digest anywhere.
- A trained relevance classifier — see "swapping in a real classifier"
  below.

## Swapping in a real classifier or summarizer

Replace `matches_interest()` or `summarize()`'s bodies with a real model
call, keeping the same return shapes. If the summarizer becomes a real
LLM, `audit_grounding()` becomes considerably more load-bearing (a real
model is far more likely to state an ungrounded number than this rule-
based extractor is) — at that point, apply
[04-eval-engineering-methodology.md](../../../../ko/04-eval-engineering-methodology.md)'s
full LLM-as-judge pipeline to grade summaries, rather than only the
simple number-matching check used here.
