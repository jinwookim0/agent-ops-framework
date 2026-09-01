# Epistemic self-check — issue-triage-agent

> Applies [03-epistemic-immunity-catalog.md](../../ko/03-epistemic-immunity-catalog.md)
> and [37-target-metric-gaming-safeguards.md](../../ko/37-target-metric-gaming-safeguards.md)
> to this specific project's design, per those crystals' own guidance to
> instantiate the catalog against real, concrete cases rather than leave
> it abstract.

## Applying crystal 03 (epistemic immunity catalog)

**Item 2 (false precision)** — `classify()`'s confidence numbers (0.9,
0.85, 0.2, ...) look like calibrated probabilities but are a crude
keyword-coverage proxy (see the function's own docstring). Every place
this project surfaces `confidence`, it is labeled as a proxy rather than
presented as measured — `tasks/triage-incoming-issue.md`'s
`confidence_gate: flag` exists specifically to keep this honest at the
metadata level, not just in a comment buried in the code.

**Item 6 (confident fabrication) / item 8 (fabricated tool-use claims)** —
the risk in a *real* deployment of this skill is an LLM classifier that
writes something like "based on similar past tickets, this is almost
certainly a duplicate" without having actually queried ticket history.
This demo's rule-based classifier can't do that (it has no ticket-history
lookup to fabricate having done), but the risk is real the moment
`classify()` is swapped for a real model per `SKILL.md`'s last section —
any claim like "similar to ticket X" must be backed by an actual lookup
result logged alongside it, not asserted from the model's own training
data.

**Item 9 (Simpson's paradox) applied to this project's own metrics** — if
a future dashboard reports "95% of tickets auto-resolved this week," that
aggregate could hide a subgroup where one category (say, `billing`) is
being auto-resolved incorrectly at a much higher rate than the aggregate
suggests. `check_trip_wire()` in `skills/triage-incoming-issue/triage.py`
is a first, narrow defense against exactly this — it flags a
100%-auto-resolved category specifically instead of only ever looking at
the batch-wide rate.

## Applying crystal 37 (target-metric-gaming safeguards)

**The metric this project would obviously be tempted to optimize**: "%
of tickets auto-resolved without human intervention" (a stand-in for
"triage saved a human this much time"). Per crystal 37's core warning,
optimizing this number directly is exactly how it stops measuring what it
was meant to measure — a classifier that routes every ambiguous ticket to
`needs-human-review` (correct behavior, per `heuristics.md`'s second
rule) makes this number look *worse*, while a classifier that guesses
confidently on ambiguous tickets makes it look *better* while actually
producing more misrouted tickets.

**Mechanisms actually applied here, mapped to crystal 37's list**:

1. **Multiple rewards** — this project never optimizes auto-resolution
   rate alone. `evals/eval-cases.md` case 3 exists specifically as a
   counter-metric: a classifier that games the auto-resolution rate by
   guessing on ambiguous tickets fails case 3 outright.
2. **Trip wires** — `check_trip_wire()`, described above.
3. **Careful engineering** — the "5 minutes: what's the cheapest way to
   fake a good result here" exercise crystal 37 recommends, applied to
   this project's own design, surfaces an obvious answer: default every
   ambiguous ticket to a cheap, plausible-looking category instead of
   `needs-human-review`. That is exactly the failure
   `heuristics.md`'s second rule documents having actually occurred and
   fixed — the red-team exercise and the real bug converged on the same
   finding.
4. **Adversarial reward functions** — not implemented in this demo (it
   would mean a second, independent classifier whose only job is to
   contest the first one's confident calls) — named here as an honest gap
   rather than silently skipped, per crystal 37's own framing of these as
   4 mechanisms to weigh, not all mandatory.

## What "skill" and "self-improving" actually mean here (and don't)

Raised directly by a user question during this project's own build, worth
answering as honestly in the file as it was answered in conversation:
**`classify()` is 100% deterministic, rule-based Python — no LLM or any
other model executes at runtime, anywhere in this demo.** Two terms this
project uses could easily be misread as claiming otherwise:

- **"Skill"** is [09-project-structure-template.md](../../ko/09-project-structure-template.md)'s
  structural vocabulary for "a reusable execution unit an AI-agent-managed
  project is organized around" — it does not assert that machine
  intelligence runs inside that unit. A `SKILL.md` + a plain function is
  a completely valid skill in this framework's sense; `SKILL.md`'s own
  "swapping in a real classifier" section exists precisely because the
  logic inside is deliberately a placeholder for where a model would go,
  not a claim one is already there.
- **`shared-context/heuristics.md`** is not read by `triage.py` at
  runtime — the fixes it documents (e.g., the ambiguous-ticket-defaults-
  to-ask fix) are permanently hardcoded in `decide_oversight_gate()`
  regardless of what this file says. This is not a shortcut taken for
  this demo — it is faithful to [06-self-improving-heuristics-loop.md](../../ko/06-self-improving-heuristics-loop.md)'s
  actual original design: that crystal says a human/AI *reads this file
  before starting new work*, the same way a future session modifying
  `triage.py` would read this file first — it was never designed as a
  runtime dependency-injection mechanism for the code it documents. The
  real, transferable value here is narrower than "the code learns from
  itself": it's (a) institutional memory that stops a future edit from
  silently reintroducing an already-fixed bug, and (b) `check_trip_wire()`'s
  bookkeeping pattern being genuinely reusable regardless of what
  triggered any specific rule.

See `../research-digest-agent/REAL-AI-CAPTURE.md` for the one place in
either example a real model was actually invoked, once, specifically to
close part of this gap for the grounding-audit mechanism.

## Honest limit of this whole self-check

This file was written alongside the code it evaluates, by the same
process that wrote the code — it is not an independent red-team pass.
Per crystal 03's own catalog (item 6, applied reflexively): a
self-authored epistemic-check file claiming to have caught every gap in
its own design is exactly the kind of confident-sounding claim that
deserves the same skepticism this file recommends applying to everything
else. The one gap this file names as unclosed (mechanism 4, above) is
real; there may be others an independent reviewer would find that this
process, by construction, cannot see.
