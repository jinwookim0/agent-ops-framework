# Log schema — issue-triage-agent

> Instantiation of [11-observability-and-agent-tracing.md](../../../ko/11-observability-and-agent-tracing.md)'s
> field table for this project, reusing that crystal's OpenTelemetry
> GenAI mapping where it applies.

Each run of `../skills/triage-incoming-issue/triage.py` appends one JSON
line per ticket to `sample-run.jsonl` (or `real-run.jsonl` in `--real`
mode — see crystal 31's isolation rule, enforced in `triage.py`'s
`main()`).

| Field | Example (from `sample-run.jsonl`) | Crystal-11 principle | OpenTelemetry GenAI attribute (crystal 11's mapping) |
|---|---|---|---|
| `gen_ai.operation.name` | `"triage-incoming-issue"` | which task/step | `gen_ai.operation.name` |
| `task_id` | `"TICKET-1046"` | which task/step | — (project-specific, no direct OTel equivalent) |
| `intent` | `"classify and route TICKET-1046"` | intent recorded before action | — (no exact OTel equivalent found — see crystal 11's own honest-limits note on this) |
| `tool_calls` | `["classify()", "apply_directives()", ...]` | actual actions, not a claim | `gen_ai.request.model` / `gen_ai.provider.name` (for an LLM-backed classifier; this demo's calls are plain functions, not model calls) |
| `result` | `{category, confidence, labels, oversight_gate, oversight_gate_reason, body_excerpt_redacted}` | outcome, not a summary | `gen_ai.response.finish_reasons`, `error.type` |
| `timestamp` | `"2026-08-28T16:05:00Z"` | when (anti time-axis-hiding, crystal 03 item 10) | — |
| `cost` | `{"tool_calls": 4, "tokens": null, "note": "..."}` | FinOps observability | `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` (null here because the classifier is rule-based — see `../shared-context/cost-log.md`) |

## Why `body_excerpt_redacted`, not `body_excerpt`

The field name itself states that redaction already happened, rather than
leaving a reader to assume it — a deliberate echo of crystal 07's "verify
live, not by claim" principle applied to a field *name*, not just to the
guardrail code itself: a reviewer scanning log field names alone should
already be able to tell PII handling was considered, without opening
`triage.py`.

## Why `oversight_gate_reason` is a separate field, not folded into `result`'s other fields

Per crystal 01 criterion 5 ("state the reason, not just the gate value") —
a log line that said only `"oversight_gate": "confirm"` would tell a
reviewer *what* happened but not *why this ticket specifically* got that
gate, which matters when auditing whether the gate logic itself is
working as designed (this is exactly what eval case 1 in
`../evals/eval-cases.md` checks).

## Cost/trade-off

This demo logs every ticket's full decision unconditionally rather than
following crystal 11's "summary line always, full detail only for
failing/boundary cases" cost-saving pattern — acceptable at this demo's
scale (a handful of tickets), but a real deployment processing hundreds of
tickets/day should adopt that split rather than logging every field for
every ticket forever.
