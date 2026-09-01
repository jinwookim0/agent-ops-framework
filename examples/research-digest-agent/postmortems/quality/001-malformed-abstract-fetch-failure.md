# Postmortem: malformed paper record could have crashed a whole week's batch

> Instantiation of [12-blameless-postmortem-template.md](../../../../ko/12-blameless-postmortem-template.md)'s
> template. **Honesty note**: this is a rehearsed postmortem written
> against a chaos-engineering exercise (`../../chaos/EXPERIMENT-LOG.md`),
> not a report of a real production incident — this demo project has no
> production deployment. The template, the 5-whys depth, and the
> structural-fix requirement are applied exactly as they would be for a
> real incident; only the trigger (a deliberate fault injection, not an
> organic failure) differs, and that difference is stated here rather
> than presented as something it isn't.

## Summary

A chaos-engineering fault injection (`../../chaos/EXPERIMENT-LOG.md`,
experiment 1) simulated an upstream paper-metadata source returning a
record with `abstract: null`. Without an explicit guard, this shape of
data would have raised an uncaught `TypeError` inside the per-week
processing loop, potentially losing every other paper in that week's
batch, not just the malformed one.

## Impact

None in production (no production deployment exists) — impact stated
here as what it *would have been*: one entire week's digest missing,
with no distinguishing signal between "nothing relevant this week" and
"the pipeline silently failed this week," which is a worse failure mode
than an obviously broken run because it looks like a normal empty result.

## Root cause (5 Whys)

1. **Why would the pipeline have crashed?** — A string operation
   (`.lower()`) was called on `paper["abstract"]` without checking it
   for `None` first.
2. **Why was there no null-check?** — The original implementation (this
   demo's first draft) assumed every paper record in `sample-papers.json`
   would always have both `title` and `abstract` populated, since the
   fixture file is fully within this project's own control.
3. **Why was that assumption made?** — `../../PREMORTEM.md` (written
   before implementation) already named "a malformed paper record crashes
   the batch" as scenario 1 — but naming a risk in a premortem and
   actually coding the corresponding guard are two different steps, and
   the first implementation pass covered the happy path first.
4. **Why didn't anything catch the gap between the premortem and the
   code?** — No automated check existed at that point verifying that
   every premortem scenario has a corresponding, exercised test case.
5. **Structural root cause**: a premortem's mitigations are not
   automatically implemented just because they're written down — the
   actual code path needs an explicit test (the chaos experiment) that
   fails until the mitigation is really coded, closing the loop between
   planning and implementation.

## Timeline

- Premortem scenario 1 written, naming this exact failure mode, before
  any code existed.
- `digest.py` first draft written with the null-check already included
  (informed directly by the premortem, not independently rediscovered).
- Chaos experiment 1 run to verify the mitigation actually works, not
  just that it was written.
- This postmortem and the corresponding `heuristics.md` entry (see
  below) written to close the loop for future changes to this pipeline.

## What went well

- The premortem process (crystal 27) had already identified this exact
  failure mode before implementation — the fix was informed by planning,
  not discovered the hard way in a real incident.
- The chaos experiment gave a live, reproducible way to confirm the fix
  actually works, rather than trusting that writing a null-check was
  sufficient.

## What didn't work

- Writing a risk down (in the premortem) and actually testing that its
  mitigation is coded are two separate steps — this project had no
  mechanism forcing the second step to happen, only the discipline of
  doing it deliberately this time.

## Action items

| Action | Owner | Done when | Status |
|---|---|---|---|
| Add an explicit null-check on `abstract` before any string operation | this session | `digest.py` skips malformed records with a logged status instead of raising | ✅ done |
| Add a permanent chaos test case (not a one-off manual check) for this fault | this session | `sample-papers.json` week 5 contains this exact fault, re-exercised on every run | ✅ done |
| Add the corresponding heuristic to `shared-context/heuristics.md` | this session (automated by `digest.py` itself) | Rule "A paper record with a missing/null abstract field must be skipped and logged, never crash the week's whole batch." is present | ✅ done |
| Add a general rule: every premortem scenario gets a corresponding chaos-experiment or eval case before the skill is marked done | not yet assigned | a checklist item exists in `governance`-equivalent docs for future skills built in this project | ⬜ not started — noted as a real gap, not swept under the rug |

The last item is intentionally left open — closing it here would be
exactly the kind of "processed the finding, added a checkbox, moved on"
behavior this project's own `05-autonomous-agent-operating-principles.md`
warns against when internal diagnostic findings aren't things a real user
asked for yet.
