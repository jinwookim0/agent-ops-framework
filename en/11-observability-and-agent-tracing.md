<!-- translated-from: ssot=sha256:cc6872f58e7a own=sha256:252914b66b68 -->
# Observability — How to Keep Agent Execution From Being Left as Claims Instead of Logs

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/11-observability-and-agent-tracing.md)**

**Version**: 1.0.2
**Content hash**: sha256:70ec8e3a755c (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 (re-verified 2026-09-01) The framework's
own principles (separating intent from observation, structured logging)
are settled and based on the ReAct pattern, and the external standard
(OpenTelemetry's GenAI semantic conventions,
github.com/open-telemetry/semantic-conventions-genai) was checked
directly against the source this time, including actual attribute names
(`gen_ai.operation.name`, `gen_ai.usage.input_tokens`, etc.) — an
earlier version of this document couldn't confirm this, since that
repository was inaccessible while mid-migration.

Whether an AI agent's statement that it "completed" something and whether
that tool call actually happened can be two separate things (item 8 in
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)).
This crystal lays out **observability design principles** that
structurally prevent that problem.

## Core principles — three axes

### 1. Record intent before the action, and observation after it

The heart of the ReAct pattern (Thought→Action→Observation) is to
explicitly record "why I'm taking this action" **before** the action, and
to separately record "what actually happened" **after** the action.
Separating these two lets you:
- Reconstruct after the fact "why we judged it that way at the time"
  (distinct from post-hoc rationalization — see item 7 in
  [03](03-epistemic-immunity-catalog.md)).
- When an action fails, distinguish "the intent was right but execution
  failed" from "the intent itself was wrong to begin with."

### 2. Always cite the actual log next to a "completed" statement

Put the claim and the evidence in the same place — instead of writing
"the tests passed," attach the actual test-run output (pass count, fail
count) right next to it. This isn't just for human-readable reports —
**another AI agent that later references this result must apply the same
standard** — if only the summarized claim gets reused, the original
verification is lost.

### 3. Structured logs are far more useful later than free-text logs

If you keep execution logs only as prose ("it went fine," "no problems"),
later aggregation, search, and regression comparison become impossible.
At minimum, structure and record the following fields:

| Field | Example | Why it's needed |
|---|---|---|
| Which task/step this was | Task identifier | Needed later to compare the same step across runs (regression detection) |
| What was intended | "Verify 3 cases" | Prevents post-hoc rationalization (item 7 in [03](03-epistemic-immunity-catalog.md)) |
| What was actually done (tool calls) | Tool name + input summary | The core of the "logs, not claims" principle |
| What the result was | Success/failure + concrete figures | So a human doesn't have to re-verify by eye |
| When | Timestamp | Prevents concealing the time axis (item 10 in [03](03-epistemic-immunity-catalog.md)) |
| Cost (optional) | Tokens/time/number of API calls | FinOps observability — connects to [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) |

## An emerging standard worth watching — OpenTelemetry's GenAI semantic conventions

OpenTelemetry is developing semantic conventions (a standardized log
schema) for generative-AI (GenAI)/agent execution in a separate
repository (github.com/open-telemetry/semantic-conventions-genai) — 🟢
re-verified 2026-09-01 against the actual spans/attributes:

| This crystal's field | Actual OpenTelemetry attribute |
|---|---|
| Which task/step this was | `gen_ai.operation.name` (the span name itself follows `"{operation.name} {request.model}"`) |
| What was actually done | `gen_ai.request.model`, `gen_ai.provider.name` |
| What the result was | `gen_ai.response.finish_reasons`, `error.type` |
| Cost (optional) | `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` |

**Honest limit**: this mapping was drawn after the fact from this
crystal's own independently-derived fields — it doesn't mean this
crystal was originally designed to follow the OpenTelemetry standard.
No exact match was found in this re-verification for the "what was
intended" and "when" fields (deeper documentation digging might turn
one up). If you actually need a standardized schema, first implement
the three principles above on your own, then open this repository's
latest documentation directly to align field names — this crystal
doesn't substitute for the full standard document.

## Connecting to regression detection

Once structured logs accumulate, you can automatically compare a new
execution result against past logs to determine "did this get worse than
last time" — step 8 (regression) of
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)
is an example of implementing this principle as a concrete pipeline
stage. Observability design has value on its own even without an eval
pipeline — it lets you answer "what changed since last week" by log
search alone when a human asks.

## The tradeoff with cost (stated honestly)

Structuring and recording everything makes the logs themselves bloat. A
compromise that works in practice: (1) keep only a one-line summary in
the standing log after every run, and (2) preserve detailed logs (full
input/output) separately only for failed or ambiguous (boundary) cases —
the same spirit as the tradeoff in [04](04-eval-engineering-methodology.md)
of "spend the extra cost only on boundary cases." The problem of the log
file itself continuing to grow can be handled with the same "memory cap +
archive" pattern from
[06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md).
