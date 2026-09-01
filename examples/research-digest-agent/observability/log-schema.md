# Log schema — research-digest-agent

> Instantiation of [11-observability-and-agent-tracing.md](../../../ko/11-observability-and-agent-tracing.md),
> using the same field shape as `issue-triage-agent/observability/log-schema.md`
> for consistency across both examples — the unit of observation here is
> a **week**, not a single item, since that's the level at which a
> publish/hold decision is actually made.

Each run of `../skills/summarize-and-digest/digest.py` appends one JSON
line per week to `sample-run.jsonl`.

| Field | Example | Principle |
|---|---|---|
| `gen_ai.operation.name` | `"summarize-and-digest"` | which skill |
| `week` | `4` | which cycle — the unit of oversight in this agent, unlike issue-triage-agent's per-ticket unit |
| `intent` | `"digest week 4's papers"` | intent recorded before the week's papers are processed |
| `tool_calls` | `["matches_interest()", "detect_injection()", ...]` | actual functions run, not a claim |
| `result.papers` | per-paper status + summary + unverified_claims | outcome, not a summary sentence |
| `result.oversight_gate` / `oversight_gate_reason` | `"confirm"` / `"an injection attempt was detected..."` | same reason-not-just-value principle as issue-triage-agent |
| `cost` | `{"tool_calls": 4, "tokens": null, ...}` | FinOps observability — null tokens because the pipeline is rule-based, same honesty stance as issue-triage-agent's cost-log.md |

## What's different from issue-triage-agent's schema, and why

issue-triage-agent logs one line per **ticket**; this logs one line per
**week** (a batch). The reason: issue-triage-agent's oversight gate is a
per-ticket decision (each ticket gets its own routing), but this agent's
oversight gate is a per-digest decision (the whole week's output is
published or held together) — the log's granularity follows the
granularity of the actual decision being made, not a fixed convention
copied from the other example.
