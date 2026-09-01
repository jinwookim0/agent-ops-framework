<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Debt Classification Scheme and Quality Baseline — Applying the Technical Debt Framework

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/13-debt-and-quality-bar.md)**

**Version**: 1.0.0
**Content hash**: sha256:6a61f2125d2f (of the body below, excluding the stamp comment, this line, and the version line)

If you don't track how much has piled up under "we'll fix it later,"
a project keeps growing while nobody notices that actual reliability
stays flat or declines. This crystal lays out **how to classify debt by
kind** and **the minimal quality baseline for judging whether a service
is actually usable in practice**.

## 1. Debt classification — applying the Fowler/McConnell quadrant

## Basis (confirmed against primary source)

🟢 Confirmed against the original text of Martin Fowler,
"TechnicalDebtQuadrant" (martinfowler.com/bliki) — quoting directly the
two axes first distinguished by Steve McConnell: **reckless vs.
prudent** (is the short-term gain clear) × **deliberate vs. inadvertent**
(did the team consciously choose it).

| | Deliberate | Inadvertent |
|---|---|---|
| **Reckless** | "We're going fast without caring about quality" — knowingly taking a shortcut while underestimating the long-term cost | Messy code that arises from not knowing better design practices — the team doesn't even realize debt is accumulating |
| **Prudent** | "We'll go this way now and pay it back later" — consciously taking a shortcut to hit a deadline, with a repayment plan in place | Realizing only after a year of actually building it, "this is how it should have been designed" — unavoidable even for excellent teams, and should be expected |

**Application to AI agent projects**: "Shipping without eval cases" is
reckless-deliberate debt (it can be upgraded to prudent-deliberate if
there's a repayment plan); "we didn't know there was a hidden bias in the
judging logic" is inadvertent debt (whether it counts as reckless or
prudent is decided after the fact by how quickly a system existed to
catch that bias).

## 2. Standard debt markers — five levels

| Marker | Meaning |
|---|---|
| ✅ Formally passed | Actually passed a defined verification procedure (eval cases, etc.) |
| 🟢 Executed | Actually run and produced a result, but hasn't gone through a formal verification procedure yet |
| 🟠 Partially verified | Only partially checked (a sample, not exhaustive, etc.) |
| ⚪ Not run | Never actually run even once (design only) |
| N/A | This item simply doesn't apply to this target |

**Debt-rate calculation**: The proportion of items that are not `✅
Formally passed`. This ratio is the input that drives steps 1–2
("how to set priorities") in
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
(prioritize verification over new work once debt exceeds a threshold).

## 3. Service quality baseline — a minimum of 5 criteria

This is a different axis from debt (debt = whether it's been verified;
this = **whether it's actually at production-service level**):

| # | Criterion | How to check |
|---|---|---|
| 1 | **Input validation**: doesn't crash on unexpected input (empty values, malformed format, extreme values) | Deliberately feed it anomalous input and test |
| 2 | **Failure handling**: on failure, doesn't silently produce an empty result — leaves a clear error/cause | Deliberately cut off a dependency and run it |
| 3 | **Cost control**: execution cost (tokens/API calls/time) has a cap, or at minimum is measured and logged | Check the cost field in the execution log |
| 4 | **Reproducibility**: results don't vary wildly for the same input each time (need not be fully deterministic, but the core judgment stays stable) | Run the same input multiple times and check the variance of results |
| 5 | **Observability**: execution results are left as a verifiable log, not just a claim of "it went well" | See [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) |

## 4. Using the two axes together

```
        Verified? (debt)          Production-level? (quality baseline)
"Done"       = ✅ Formally passed    +  all 5 criteria met
"Working"    = 🟢 Executed           +  some of the 5 criteria met (state which are missing)
"At risk"    = ⚪ Not run, or running repeatedly and automatically without verification
```

Collapsing the two axes into one fails to distinguish different problems
like "it's verified, but it actually crashes often" from "it's stable,
but there are no eval cases for it."

## 5. How to prioritize debt repayment

Not all discovered debt gets paid off immediately — this connects to the
"the ultimate beneficiary is the user" principle in
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md):
a "needs verification" list produced by an internal diagnostic tool is
not, by itself, a queue to be auto-executed. Repayment priority order:

1. **Prudent-deliberate debt first** (the kind that had a repayment plan)
   — paying it off as planned builds trust in itself.
2. **Items judged "reproduced twice" in
   [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)**
   — confirmed as a pattern, not a coincidence.
3. Handle the rest systematically only once the debt rate crosses a
   threshold.

## References
- Ward Cunningham's original "technical debt" metaphor (1992) — the
  original concept that reframed debt not as "a bad thing" but as "a
  choice that accrues interest."
- Martin Fowler, TechnicalDebtQuadrant (martinfowler.com/bliki) — the
  primary source for the quadrant above.
