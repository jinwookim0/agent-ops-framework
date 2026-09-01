# Example: Research Digest Agent

The second of two worked examples in this repo. Where
[`examples/issue-triage-agent`](../issue-triage-agent/) shows a
**reactive, per-item classifier**, this one shows an **autonomous,
recurring, self-improving agent** — built to cover the crystals the first
example structurally can't.

**What it does**: processes 10 simulated weekly batches of new research
papers in one run, filters them against an interest profile, drafts
grounded summaries, and decides per week whether the digest can
auto-publish or needs a human to review it first — while accumulating
heuristics and context across weeks the way a real recurring deployment
would accumulate them across real calendar weeks.

**What it's for**: not a product to adopt — a worked example to read,
paired with [`examples/issue-triage-agent`](../issue-triage-agent/).
Together the two demos cover 25 of this framework's 37 crystals with
real, checkable code. The real deliverable here is
[`CASE-STUDY.md`](CASE-STUDY.md), which maps 12 crystals (2 of them
deepened facets of crystals the first example already touches, 10
genuinely new) to the exact file/line where each one is doing something.

## Try it

```bash
cd examples/research-digest-agent
python3 skills/summarize-and-digest/digest.py
# or, to also see crystal 18's determinism check:
python3 skills/summarize-and-digest/digest.py --determinism-check
```

No API key, no dependencies beyond the Python standard library. Watch
for the `📝 heuristic` lines (crystal 06's loop actually running — a rule
gets added, later capped/archived, then restored) and the two `gate=confirm`
weeks (4 and 6 — an injection attempt and a fabricated-statistic catch,
respectively).

## Where to start reading

1. [`CASE-STUDY.md`](CASE-STUDY.md) — the crystal-by-crystal map. Start here.
2. [`SPEC.md`](SPEC.md) and [`PREMORTEM.md`](PREMORTEM.md) — written
   *before* the code, read them in that order to see the planning
   process the code was actually built against.
3. [`skills/summarize-and-digest/SKILL.md`](skills/summarize-and-digest/SKILL.md) +
   [`digest.py`](skills/summarize-and-digest/digest.py) — the actual
   logic.
4. [`chaos/EXPERIMENT-LOG.md`](chaos/EXPERIMENT-LOG.md) →
   [`postmortems/quality/001-malformed-abstract-fetch-failure.md`](postmortems/quality/001-malformed-abstract-fetch-failure.md) →
   `shared-context/heuristics.md` — one incident traced end-to-end from
   fault injection, through root-cause analysis, to the resulting lesson.
5. [`red-team/CHECKLIST.md`](red-team/CHECKLIST.md) — a live prompt-
   injection resistance test, run twice under different conditions.
6. [`modules/summarize-and-digest/`](modules/summarize-and-digest/) —
   the portable, dependency-free export (crystal 08), verified to run
   standalone with zero project files present.

## Honest scope

Same disclaimer as `issue-triage-agent`: the filtering/summarization
logic is deliberately rule-based (see `SKILL.md`'s last section for where
a real model would plug in), the paper source doesn't exist (fully
synthetic, fixed input), and the postmortem is explicitly a rehearsed
exercise against a deliberate fault injection, not a real production
incident — labeled as such, not dressed up as something it isn't. What's
real: the code runs, every claim in `CASE-STUDY.md` points at output you
can reproduce yourself, and the module's graceful degradation was
verified by literally running it alone in an empty directory.
