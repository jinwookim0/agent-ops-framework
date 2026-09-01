# Log schema — escalation-reviewer-agent

> Instantiation of [11-observability-and-agent-tracing.md](../../../ko/11-observability-and-agent-tracing.md),
> consistent with the other two examples' schemas but reflecting this
> project's two-stage structure: a real subagent produces `captures/*.json`,
> then `harness/audit_capture.py` (deterministic) produces
> `real-run.jsonl` from those captures.

| Field | Example | Principle |
|---|---|---|
| `gen_ai.operation.name` | `"review-escalated-ticket (audit pass)"` | labeled "(audit pass)" specifically to distinguish this log from the real judgment step itself — this line is the deterministic auditor's output, not the model's |
| `ticket_id` | `"TICKET-E04"` | which ticket |
| `result` | the real, parsed capture (category/confidence/reasoning/oversight_gate) | outcome, not a summary — the model's actual words, not paraphrased |
| `findings` | `["SECURITY GAP...", ...]` | what the deterministic audit found — empty list means no findings, not "not checked" |
| `fence_deviation` | `true`/`false` | whether the raw response violated the "JSON only, no other text" instruction — tracked explicitly rather than silently normalized away |

## Why two files, not one

`captures/*.json` is the **raw record of what actually happened** —
never edited, never regenerated, dated. `observability/real-run.jsonl`
is **derived, re-creatable output** — running `harness/audit_capture.py`
again regenerates it from the same captures and produces the same
result (the harness itself is deterministic, even though the captures it
audits are not). This mirrors the same "raw evidence vs. derived report"
separation `research-digest-agent/chaos/EXPERIMENT-LOG.md` draws between
a fault injection and its postmortem.
