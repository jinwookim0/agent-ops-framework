<!-- translated-from: ssot=sha256:c616e3fa2a18 own=sha256:db667fff9f3d -->
# Self-Experiment Reporting Standard — Qualitative + Quantitative + Confidence, plus Pre-registration and Process Tracing

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/34-self-experiment-reporting-standard.md)**

**Version**: 1.0.0
**Content hash**: sha256:87af7ef4bf1e (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟡 The sample-size principle (saturation curve) is confirmed against the primary source — 🟢. The five-tier confidence-marker scheme itself is this framework's own design, not a direct comparison against an external standard (e.g., the GRADE evidence-quality framework used in medical research) — marked 🟡 to avoid overstating it.

This covers how an agent should report the results when it runs an **informal, one-off experiment** to test some technique or bias of its own — not a regression evaluation against fixed cases and a rubric, but the kind of experiment run because "I was curious whether this is actually true."

## How this differs from crystal 04 and crystal 18 (G3)

[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) is a pipeline for **regression-testing an output against fixed cases and a rubric**, and [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) covers **why the same input produces different answers**. This crystal is neither — it's about how to honestly report a **self-directed experiment** with no predefined cases, where the agent forms and tests its own hypothesis. All three deal with "trustworthy evidence," but at different points: 04 is output quality, 18 is the root cause of non-determinism, and this crystal is the reporting format for ad-hoc experiments.

## The three required elements — all must be present for something to count as an "experiment"

### 1. Qualitative narrative
Explain in prose what was observed, why it matters, and what the numbers actually mean. Don't just list numbers and stop.

### 2. Quantitative measurement
Express the observation as real numbers (sample size n, ratios/counts, confidence intervals where applicable) — compute these with an actual tool, don't eyeball them.

**Principle for setting sample size (n) — observe the saturation curve directly**: Use the saturation pattern measured by the Self-Consistency paper (Wang et al. 2022, [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)) — as the number of reasoning paths increases from 5→10→40, the improvement shrinks and eventually flattens out — as a reference principle for designing sample size. Instead of fixing n arbitrarily, increase it one step at a time and find the point where "the verdict stops changing." **This is not a mandatory rule** — it's overkill for a single binary check (does this work or not), and is recommended only for multi-stage, comparative experiments (comparing the effect size of A vs. B).

### 3. Confidence rating — must always be stated as a separate, explicit section

| Marker | Meaning | Criterion |
|---|---|---|
| 🟢 High | Multiple independent replications + sufficient sample size + controlled design (confounds excluded) | Generally n is large, or repeated experiments consistently point the same direction |
| 🟡 Medium | Replicated, but the sample is small or controls are incomplete | |
| 🟠 Low | A single attempt, or a known methodological flaw (e.g., ceiling effect) | |
| ⚪ Unrated | Confidence has not yet been assessed (left honestly blank, not invented) | |
| N/A (exception) | An experiment intentionally meant to be a qualitative observation only (quantification is inherently inappropriate) | Should be rare — don't overuse |

**Core principle**: whether "an effect exists or not" (the result) and "how much this result can be trusted" (confidence) are different axes. A null result can still have high confidence (if it came from a well-designed, large sample where there genuinely was no difference), and a strong effect can have low confidence (if n=1 and the observation wasn't controlled) — don't conflate the strength of a result with its confidence.

## Two extended elements — only for multi-stage experiments or ones whose design changed mid-run

### 4. Pre-registration
Write down the hypothesis and expected result **before** running the experiment. This is a procedure for preventing a post-hoc "I knew it all along" narrative once the actual result is in — keep the prediction as written even if it turns out wrong (if you only keep predictions that turned out right, the whole procedure becomes pointless). Can be skipped for a single observational check.

### 5. Process tracing (Thought → Action → Observation)
If the investigation or experiment went through multiple stages where an intermediate observation changed the next step (e.g., the first-round result looked strange so you reopened the source, or you found a design flaw and redesigned), record that flow briefly in order — reporting only the final conclusion erases "why the design changed the way it did." Can be skipped for a simple experiment that ran exactly as originally designed.

## When confidence is bound to come out low

When the sample is fundamentally limited by circumstance (e.g., the sample is capped by whatever events actually happened during a single day's session), don't try to artificially inflate the confidence rating — write it honestly as low, and leave "how confidence could be raised" as a candidate for the next experiment. Running a small-sample experiment and honestly labeling it as such is better than not running it at all — the only thing to avoid is exaggerating without labeling it.

## Related
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) — regression verification based on fixed cases and a rubric (a different target than this crystal).
- [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) — the root cause of non-determinism (adjacent background for the reporting format this crystal covers).
- [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) — "always attach a real log next to a claim," the same spirit as element 2 (quantitative measurement).
