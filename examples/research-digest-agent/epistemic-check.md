# Epistemic self-check — research-digest-agent

> Applies [03-epistemic-immunity-catalog.md](../../ko/03-epistemic-immunity-catalog.md)
> to this project's own design, per that crystal's own guidance to
> instantiate the catalog against real, concrete cases. Parallel to
> `../issue-triage-agent/epistemic-check.md` — read that file's "What
> 'skill' and 'self-improving' actually mean here" section first; this
> file doesn't repeat it, only the parts specific to this project.

## What "skill" and "self-improving" actually mean here (and don't)

Same gap as `issue-triage-agent`, worth stating for this project
specifically since it's the one whose name (`summarize-and-digest`) most
directly implies a model doing the summarizing: **`summarize()`,
`matches_interest()`, and `audit_grounding()` are all deterministic,
rule-based Python — no LLM executes anywhere in a normal run of
`digest.py`.**

The mechanism this most directly affects is `HeuristicsStore`: the
cap/archive/restore cycle `CASE-STUDY.md` documents running across weeks
2-10 is real, tested code — but `digest.py`'s actual detection logic
(the citation-stripping, the unicode normalization, the null-check, etc.)
is unconditionally hardcoded, identical regardless of whether the
corresponding lesson is currently active or archived in
`shared-context/heuristics.md`. This is not a shortcut — it's faithful
to crystal 06's actual design (a document a *future session* reads before
touching this code, not a live feature-flag store this code reads from
itself) — but it does mean the "self-improving loop" demonstrated here is
better described as **"the mechanics of managing a growing lessons file
are real and tested"** than **"this agent modifies its own runtime
behavior based on what it has learned."** The latter would require
`summarize()`/`matches_interest()` to actually be model calls that read
`heuristics.md` as part of their own context — which is exactly the gap
`REAL-AI-CAPTURE.md` partially closes for one specific mechanism
(grounding-audit), by testing it against a genuine, unscripted model
response instead of only the scripted fixture in `KNOWN_TEST_OVERCLAIMS`.

## Applying crystal 03 directly

**Item 2 (false precision)** — `summarize()`'s output can read like a
model "understood" the paper, but it's literally "first sentence + any
sentence containing a digit." Nothing in this project's output
(`observability/sample-run.jsonl`, the printed tables) claims otherwise,
but a reader skimming only the final digest — not this file or
`SKILL.md` — could reasonably mistake the summarizer's fluency for
comprehension it doesn't have.

**Item 6 (confident fabrication)** — the actual risk this item warns
about (a model asserting something it never checked) doesn't exist in
the *rule-based* pipeline (there's nothing to "assert" beyond simple
extraction), but becomes real the moment `summarize()` is swapped for a
model per `SKILL.md`'s last section. `REAL-AI-CAPTURE.md` is a first,
honest data point on this specific risk — one clean capture, explicitly
not claimed to generalize (models are non-deterministic; see crystal 18).

**A limit in `HeuristicsStore._similar_archived_index()` itself, found
and confirmed live while writing this file** — the "does this new lesson
match an archived one" check is `len(shared distinctive words) >= 3`
with no stopword filtering, which is crude by construction. Verified
with an actual false positive, not just a hypothetical:
```python
s.archived = [("Do not let an alarming/urgent-sounding title override the interest-keyword filter.", "...")]
s._similar_archived_index("Do not let the confidence score override the interest-keyword filter decision.")
# -> 0 (matched!)
```
These are two **genuinely different concerns** (a title's alarm-language
vs. a confidence score, both "overriding the interest-keyword filter")
that share 6 words — including function words like "do," "not," "let" —
purely from similar sentence structure. In a real deployment, proposing
the second (confidence-score) rule for the first time would incorrectly
restore the unrelated archived title-alarm rule instead of adding a new,
distinct one — silently discarding a genuinely new lesson under the
wrong label. This wasn't exercised by any of the 10 demo weeks (week 10's
restore was deliberately worded to overlap with week 2's original lesson
on purpose) — a real deployment would need at minimum a stopword filter,
and likely a proper similarity metric, not raw shared-word counting.

## Honest limit of this whole self-check

Same limit as `issue-triage-agent/epistemic-check.md`'s closing section:
written by the same process that wrote the code, not an independent
review. The word-overlap limit above was caught while writing this file
specifically *because* the exercise of writing an honest self-check
surfaced it — which is itself a small, real demonstration of why this
crystal recommends doing this instantiation at all, rather than trusting
that "we already thought about honesty in the code comments" was enough.
