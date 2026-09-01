# Chaos experiment log — research-digest-agent

> Applies [19-chaos-engineering-for-agents.md](../../../ko/19-chaos-engineering-for-agents.md)'s
> 5 principles. Distinct from `../red-team/CHECKLIST.md`: that file covers
> a **malicious** event (someone deliberately attacking the pipeline);
> this file covers an **accidental/environmental** one (an upstream
> source just... breaking), following crystal 19's own distinction from
> crystal 14.

## Experiment 1 — missing abstract field from the paper source

### 1. Steady-state hypothesis (stated before injecting anything)
"In a normal week, every paper in the batch has a non-null `abstract`
field, and the pipeline processes 100% of the papers in a batch without
raising an exception."

### 2. Real-world event modeled
An upstream paper-metadata source returning a record with a missing or
null field is a common, well-documented shape of API degradation — not a
contrived edge case (crystal 19's "real-world events" principle: hardware
failures, malformed responses, sudden zero-budget states).

### 3. Fault injected
`sample-papers.json`'s week 5 batch contains:
```json
{"id": "P-501", "title": "Scalable Retrieval Indexes for Agent Memory", "abstract": null, "source_status": "malformed"}
```
alongside one normal paper (`P-502`) in the same week's batch.

### 4. Blast-radius containment (crystal 19's risk-control section, applied)
- No real external action is triggered by this experiment — the fault is
  a data value in a synthetic fixture, not a live call to a real API.
- The experiment's effect is scoped to week 5's own batch: prior weeks'
  already-written log lines and heuristics are untouched, and the healthy
  paper in the SAME week's batch (`P-502`) still gets digested normally.

### 5. Result (without the null-check — verified with an isolated repro, not just asserted from memory)
`digest.py` was built with the null-check already in place, so this
project never ran a genuinely broken version of the real pipeline. To
back the claim below with evidence rather than assumption, the exact
failure was reproduced in isolation:
```python
paper = {"title": "Scalable Retrieval Indexes for Agent Memory", "abstract": None}
(paper["title"] + " " + paper["abstract"]).lower()
# TypeError: can only concatenate str (not "NoneType") to str
```
Confirmed live: `TypeError`, not a hypothetical. Without a check gating
this operation, that exception would propagate uncaught out of `run_week()`'s
loop over that week's papers, stopping the week's loop entirely — meaning
`P-502`, a perfectly valid paper in the same batch, would also silently
never get digested. This violates the steady-state hypothesis in the
worst possible way: not a partial degradation, but the whole week's batch
silently disappearing.

### 6. Result (after the fix — verified live)
```
Week 5: gate=notify
  reason: a paper was skipped due to malformed source data — the rest of the digest is unaffected, but a human is informed of the gap
  {'id': 'P-501', 'status': 'skipped-malformed-data'}
  {'id': 'P-502', 'status': 'digested', 'matched_keywords': ['retrieval', 'evaluation'], 'summary': '...'}
```
`P-502` is digested normally; `P-501` is explicitly logged as skipped, not
silently dropped or crashed on. The steady-state hypothesis now holds in
its corrected form: "100% of *well-formed* papers in a batch are
processed; malformed ones are explicitly logged, never silently lost and
never allowed to block their batch-mates."

### Continuous re-running (crystal 19 principle 4)
This experiment is now a permanent part of `sample-papers.json` (not a
one-off manual test that gets deleted after use) — every run of
`digest.py` re-exercises this exact fault path, functioning the same way
a regression test would.

### Full incident writeup
See `../postmortems/quality/001-malformed-abstract-fetch-failure.md` for
the blameless postmortem this experiment fed into (crystal 12), including
the 5-whys root-cause analysis and the resulting heuristics-store entry
(crystal 06).
