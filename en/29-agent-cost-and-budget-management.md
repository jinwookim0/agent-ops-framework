<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Agent Cost & Budget Management — A Different Axis From Observability

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/29-agent-cost-and-budget-management.md)**

**Version**: 1.0.0
**Content hash**: sha256:919848cd253f (of the body below, excluding the stamp comment, this line, and the version line)

If [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md)
covers how to log "what happened," this crystal covers **"what it cost, why it
suddenly got expensive, and how to handle limits."** This is the third axis
commercial AgentOps platforms commonly claim (alongside observability and
debugging) — previously it hung off the observability crystal as a side field;
here it gets split out on its own.

## Basis

🟢 Claude's official API documentation (prompt caching) — verified against the
primary source. The cache reuses a prompt prefix up to a designated breakpoint,
with a TTL of either a default 5 minutes or an explicit 1 hour (the 1-hour
option costs 2x the base price). The response's `usage` object reports three
fields: `cache_creation_input_tokens` (tokens newly written to cache),
`cache_read_input_tokens` (tokens read from cache), and `input_tokens` (tokens
after the last breakpoint, unrelated to the cache). **The cache TTL is counted
from when a request "starts," and includes the time spent generating the
response** — to reuse the immediately preceding cache, the next request must
start within the TTL after that response finishes. A cache hit costs roughly
1/10th of the base input price.

## Core Mechanism 1 — Keeping Sessions Long Increases Caching Gains

Restarting sessions frequently forces the cache to be refilled from scratch
each time — conversely, continuing a conversation within the same session
keeps reusing an already-filled cache. Operating with long-lived sessions is
therefore a rational choice from a caching standpoint (though a long idle gap
that exceeds the TTL expires the cache and erases this gain, which should also
be factored in).

## Core Mechanism 2 — Resource Limits Come in Multiple, Distinct Kinds

Token-usage limits and API-call-count limits (e.g., number of calls to an
external search tool) can exist simultaneously as **separate constraints** —
having headroom on one gives no guarantee of headroom on the other. And a
"limit reached" error is not a transient failure — it's a **signal**: retrying
will keep failing for the same reason until the reset time. The correct
response is to **stop and report to the user**, not retry. If the observed
reset time keeps shifting, that's a sign this is likely **a rolling window
based on recent usage**, not "one fixed daily reset" — don't assume that once
you're past a reset time you're safe from then on.

## Core Mechanism 3 — Parallel Batches Amplify Hitting a Limit

If several heavy calls are fired off in parallel at once and one of them hits
an account-level limit (session usage, rate limit, etc.), every other call
already in flight and waiting fails for the same reason all at once — this is
not an individual defect but structural waste at the moment of firing. The
mitigation: as soon as any limit-related error pattern ("session limit",
"rate limit," etc.) is detected, immediately stop and report instead of
firing any more pending runs — retrying is only meaningful after the reset
time (usually specified in the error message).

## Core Mechanism 4 — Cost Splits by "Internal Stage," Not "Surface Category"

Even workflows that look like the same surface type (e.g., both labeled
"research") can differ in actual cost by several multiples depending on
whether they internally use external search/discovery stages, or how many
pipeline stages they run. Don't guess cost from the category name alone —
measure it by logging actual tokens/calls consumed (the "cost (optional)"
field in [crystal 11](11-observability-and-agent-tracing.md) is where this
measurement belongs).

## Principles — Five Ways to Cut Re-verification and Budget Waste

1. **For structurally clear fixes, start with low-cost static checks**: if a
   bug has a clear cause (e.g., "a specific field is missing from the
   output"), confirming the fix doesn't always require full re-verification
   (which can run into the hundreds of thousands to millions of tokens) — first
   confirm with a low-cost, code-review-level check (tens of thousands of
   tokens), and defer full re-verification to when it's actually needed (e.g.,
   right before deployment).
2. **When multiple defects are found, batch the fixes and re-verify once**:
   re-verifying the whole thing immediately after fixing each individual
   defect multiplies the re-verification cost by the number of defects.
3. **If a hard budget cap is needed, use the tool's explicit budget
   mechanism** — if one exists, turn it on (the default is usually unlimited,
   so it must be explicitly enabled). If none exists, this crystal's "Core
   Mechanism 3" (stop-and-report) is the minimal soft safeguard.
4. **Keep lossless compression as a standing rule for frequently-read shared
   context files** — as a file that every run reads in full before starting
   grows, the cost of every run grows along with it. Merge repeated narration
   of the same topic into a single conclusive line, preserving facts, numbers,
   decisions, and open questions while trimming explanatory prose (the
   standard for "lossless": cross-check every core fact before and after
   compression to confirm preservation).
5. **State the applicability condition inside a conditional scoring/spec item
   from the start** — this pre-empts a recurring failure across multiple
   targets where an item that should score "not applicable" instead gets
   wrongly scored as "not met" because its condition was never stated.

## Honest Limitations

Concrete figures like specific token counts or cost-growth rates are empirical
values the original project observed over a particular period on a particular
account, so there's no basis to claim they generalize as-is to other
projects, models, or workloads — that's why this crystal contains no concrete
numbers, only patterns. Causal claims like "this type of task is more
expensive than that type" are logical inferences drawn from observed
structure, not conclusions confirmed through falsification experiments across
other combinations.

## Related
- [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) —
  where the "cost" field this crystal covers originally lived, and how to log
  measured values
- [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) — the principle of
  scaling verification strength to risk shares the same direction as this
  crystal's "reduce re-verification waste" principle
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
  risk-tiered verification, a companion mechanism that structurally lowers
  re-verification cost
