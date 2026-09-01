# Cost log — issue-triage-agent

> Instantiation of [29-agent-cost-and-budget-management.md](../../../ko/29-agent-cost-and-budget-management.md)'s
> principles for this demo project.

## Current state (honest, not projected)

This demo's classifier (`triage.py`) is rule-based, not an LLM call — so
its real per-run cost is effectively zero tokens (see the `"cost"` field
on every log line in `../observability/sample-run.jsonl`: `"tokens":
null, "note": "rule-based classifier — no LLM tokens spent"`). The cost
crystal is still relevant here for two reasons, laid out below rather than
invented numbers for a workload this demo doesn't actually run.

## Where cost would actually show up if `classify()` were swapped for an LLM

Per crystal 29's "cost is decided by internal steps, not the outward
category" mechanism: a naive single-call classifier (one prompt, one
ticket, one category back) costs roughly one input-token-count's worth of
prompt per ticket. The moment `evals/eval-cases.md`'s LLM-as-judge
pipeline is added on top (crystal 04's boundary-case self-consistency
re-scoring), *boundary* tickets specifically start costing 3x a plain
classification call — this is why crystal 04 scopes that extra cost to
boundary cases only, not every ticket. A batch of 6 tickets like this
demo's fixture set would look cheap either way; the real cost curve shows
up at the volume a real deployment processes (hundreds/day), which this
demo does not attempt to simulate with invented numbers.

## Principles actually applied in this demo

1. **Structural fix before re-verification, not the other way round**
   (crystal 29, principle 1): when the classifier fix landed (see
   `heuristics.md`'s "one-line ticket" entry), it was checked by re-running
   `triage.py` once against the 6-ticket fixture set (a few cents'
   worth of compute either way, and free here since it's rule-based) —
   not by inventing a full production-scale re-verification pass for a
   change this localized.
2. **Batch defects, batch re-verification** (crystal 29, principle 2):
   both the "urgent" bug and the "one-line ticket" fix (see
   `heuristics.md`) were made and verified together in one `triage.py` run,
   not as two separate re-runs.
3. **Hard budget mechanism**: not applicable to this rule-based demo (no
   external API is called) — if `classify()` is swapped for a real LLM,
   crystal 29's guidance is to turn on whatever budget mechanism the
   calling tool provides rather than relying only on the soft
   stop-and-report pattern below.
4. **Rate-limit / quota signal handling** (crystal 29, mechanism 2): this
   demo has no external API to rate-limit against, but the pattern it
   would follow is documented in `../.claude/hooks/guard-pii-leak.sh`'s
   comments for the one external-facing call this project's *design*
   assumes exists (posting a comment back to the ticket tracker).

## Related

- [11-observability-and-agent-tracing.md](../../../ko/11-observability-and-agent-tracing.md) —
  the `"cost"` field on every log line originates from this crystal, not
  this one.
- `../observability/log-schema.md` — where that field is documented for
  this project specifically.
