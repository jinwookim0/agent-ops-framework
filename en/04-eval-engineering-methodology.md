<!-- translated-from: ssot=sha256:f85891b0fc18 own=sha256:58c06559924c -->
# Eval Engineering Methodology (Domain-Neutral Template)

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/04-eval-engineering-methodology.md)**

**Version**: 1.0.2
**Content hash**: sha256:538a98382af0 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 The core claims of published papers —
LLM-as-judge (Zheng et al. 2023), self-consistency (Wang et al. 2022) —
were checked against the source, and the pipeline itself was field-tested
and repeatedly verified in the original project's real operation.

As the volume of output an AI agent produces — a skill's execution result, a
workflow's output — grows, having a human manually eyeball whether each one
"turned out well" becomes a bottleneck. This document lays out a multi-stage eval
pipeline that organizes three parallel layers: **logic (what and why) /
technical mechanism (how, concretely) / underlying knowledge (what academic
basis it comes from).**

## Overall flow (at a glance)

```
Load (load cases and rubric)
  → Run (the actor actually executes — not simulated)
    → Judge (1st-pass LLM-as-judge grading, met/unmet per rubric item)
      → Zone classification (clear_pass / boundary / clear_fail)
        → [boundary only] Self-consistency re-grading (2 more independent passes + majority vote)
      → askQuality (if boundary cases exist, verify the quality of the question that will be asked of the human)
      → driftWarning (if there are zero boundary cases, check against history for overconfidence)
      → regression (if a past report exists, compare per-case regression)
    → Record (structured log + standard metrics doc, human makes the final call)
```

Each stage depends on the output of the one before it — this is a pipeline,
so a failure partway through (e.g. a missing case file) stops it immediately
with a clear error instead of silently returning empty results.

## Stage-by-stage detail

### 1. Load — fix the cases and rubric first
**Logic**: fixing the criteria first, and only then looking at the execution
results, structurally blocks confirmation bias (fitting the criteria to
whatever result you wanted, after the fact). **Technical mechanism**: read
the case file directly and return it in structured form (input + expected
behavior + rubric). If the file is missing, or there are zero cases, abort
immediately with an error — don't swallow it in a try/catch. **Underlying
knowledge**: for a format that specifies "input + expected behavior" per
case, [promptfoo](https://www.promptfoo.dev/docs/configuration/test-cases/)'s
vars/assert structure is a useful reference. Write rubric items as concrete,
checkable statements rather than vague ones ("should be good").

### 2. Run — the actor actually executes (not simulated)
**Logic**: don't guess "this is presumably how it would behave" — follow the
actual procedure and produce a real output. "A case file exists" and "it
actually passes that case" are different things. **Technical mechanism**: if
the target is a workflow, actually run it; if it's a skill/agent, prompt it
to "read the instruction document and follow the procedure exactly," having
it use real tools. Put a safeguard here — **only when the input itself
demands a real-world action that's genuinely hard to reverse (payment,
sending a message, an account change, etc.)**, treat a response that asks for
confirmation as the final output in its own right. If this scope is drawn
too broadly (e.g. applying it just because a confirmation phrase appears
anywhere in the document), the actor over-hedges even on unrelated cases —
this is a failure pattern confirmed by real incidents, so keep the scope
narrow. **Underlying knowledge**: the side-effect-avoidance principle from
Amodei et al. 2016, "Concrete Problems in AI Safety" — even for evaluation
purposes, causing an irreversible real-world side effect is not acceptable.

### 3. Judge — grade per rubric item (LLM-as-judge)
**Logic**: grading each rubric item independently as met/unmet — rather than
an overall "good/bad" — is what makes it possible to trace afterward exactly
where and why something fell short. **Technical mechanism**: give the judge
the case, input, expected behavior, execution result, and the full rubric
text, and force a structured `{item, met, reason}` output per item. State
anti-bias instructions explicitly in the prompt — **guard against verbosity
bias** ("don't grade more generously just because it's long") and **guard
against the halo effect** ("don't let unrelated items get graded more
generously just because others scored well"). If the judgment depends on the
date, inject "today's date" explicitly — without it, a documented failure
mode is the judge guessing at today's date and mistakenly flagging genuinely
current data as a hallucination. **Underlying knowledge**: the LLM-as-judge
pattern follows Zheng et al. 2023.

### 4. Zone classification — clear_pass / boundary / clear_fail
**Logic**: having a human review every single case makes verification itself
a bottleneck. But automating everything misses ambiguous judgments. The
key tradeoff: **auto-process anything far from the threshold, and only
escalate cases near the threshold (the ambiguous ones) to a human.**
**Technical mechanism**: `rate = number met / total items`. Outside the pass
threshold (e.g. 0.8) ± a margin (e.g. 0.15), auto-finalize as
clear_pass/clear_fail; inside it, mark as boundary and pass it to the next
stage. **Underlying knowledge**: Horvitz 1999's principle of "selectively
requesting intervention" + scalable oversight (a design where a human
doesn't need to review every decision — only the uncertain ones are routed
for intervention). **An honest gap** (keep this note whenever this section is
ported elsewhere): the threshold value itself (e.g. 0.8) is often adopted
straight from conventional software-QA defaults without review — a separate
mechanism is needed to verify whether this value actually correlates with
real output quality.

### 4.5. Scale verification strength to target risk (risk-tiered verification)
**Logic**: applying the same verification strength to every target is
inefficient — a target where being wrong is easy to undo (an output with
almost no factual claims) shouldn't cost the same as a target where being
wrong causes real harm (financial, legal, medical, safety). This takes the
"spend little on the clear cases, more on the ambiguous ones" principle from
stages 5–6 and raises it one level further, from the per-case level to the
**per-target** level.
**Technical mechanism**: declare a risk tier per target (e.g. a three-level
light/standard/heavy scale), and have the grading pipeline read that tier to
adjust whether/how strongly the stages below run — at light, skip stages
like self-consistency and adversarial spot-checks entirely; at heavy,
increase the number of skeptic passes. **However, the principle that a
boundary verdict always goes to a human stays in force regardless of
tier** — what gets skipped is only "the stage where the grading pipeline
tries to re-confirm on its own," not the scalable-oversight principle of
"ask a human when it's ambiguous." The tier itself is determined by a
deterministic rule from signals that already exist (the output's stated
confidence level, a list of risk factors, etc.), with final adoption still
confirmed by a human/AI reviewing the results (separating discovery from
judgment — the same principle other crystals in this framework share).
**Underlying knowledge**: this runs in the same direction as risk-based
testing in software QA (concentrating verification resources on targets
where failure-likelihood × impact is highest). As evidence for how widely
this principle is already adopted in practice, consider risk-tiered
regulatory frameworks for AI systems (e.g. multi-tier regulatory frameworks
where lower risk levels carry almost no requirements, while higher levels
require a risk-management system, data governance, and accuracy assurance) —
this shows that "scaling governance requirements to risk level" is already a
proven practice at large scale.

### 5. Self-consistency re-grading — boundary cases only
**Logic**: the risk of a grade being unstable is highest for ambiguous
(boundary) cases. Spend extra cost only there to raise confidence, without
spending extra on cases that are already clear. **Technical mechanism**: for
each boundary case, run 2 more independent judge calls in parallel
(explicitly instructed not to reference the prior grading result), and take
a per-item majority vote across the original 1 + these 2 = 3 votes total. If
there's no guarantee the three calls return rubric items in the same order
every time, **match by item text, not array position** (position-matching
risks incorrectly comparing judgments whose order got shuffled).
**Underlying knowledge**: Wang et al. 2022's (arXiv:2203.11171)
self-consistency — sampling multiple independent reasoning paths and taking
a majority vote produces a more stable final answer than a single path.
Applying this to every case would triple the cost, so it's restricted to
boundary cases to balance cost against reliability.

### 6. askQuality — verify the quality of the question that will be asked of a human
**Logic**: if boundary cases exist, a human needs to be asked — but asking an
unanswerable question like "it's ambiguous, what should we do?" gives the
human no material to judge with. **Technical mechanism**: gather the unmet
items and their reasons, instruct the model to "write an answerable question
that includes candidate causes and options," and have it judge for itself
whether that standard is met. If there are no boundary cases, skip this call
entirely to save cost. **Underlying knowledge**: Hadfield-Menell et al. 2017,
"The Off-Switch Game" — the paper's core point that creating a situation
where a human can intervene is itself central to safety design. Here it's
applied not just to "provide the opportunity to intervene," but also to
verify whether that intervention takes the actual form of a valid,
answerable question.

### 7. driftWarning — if there are zero boundary cases, check for "overconfidence"
**Logic**: if every run comes back clear with never a single boundary case,
that looks good on the surface but may actually mean "the opportunity for
human intervention has disappeared entirely" — that's a risk in its own
right. **Technical mechanism**: only when boundary count is 0, look through
past reports to check "has there really been zero boundary cases across
recent runs." If there's too little historical data, it's judged too early
to call and skipped. **Underlying knowledge**: applies the logic of the
Off-Switch Game in reverse — the signal "there has never been a single
intervention request" can itself be overconfidence.

### 8. regression — compare against past runs to check for a decline
**Logic**: looking only at "did it pass this time" can hide a case that got
worse than last time but is still showing as a "pass" — missing the
regression. **Technical mechanism**: find the most recent past report for
the same target, and compare it against this run's results by case name. If
there's a regression (e.g. clear_pass → boundary), include it in the
warning. If case names have been refactored and no longer match, don't force
a comparison. **Underlying knowledge**: the "golden-dataset-based regression
testing" concept — the case files themselves are already the golden
dataset, and the "did it get worse than last time" comparison sits on top of
that.

**Don't automatically treat a signal that "looks like" a regression as a
defect — check first whether the case itself has simply gone stale**: a
case's premise (e.g. "this idea doesn't yet exist in this project," "this
resource doesn't yet exist") can be broken as the project grows — a premise
that was true when the case was written can stop being true once that thing
actually comes to exist in the project in the meantime. In that situation,
the judged target (the actor) responded correctly to the new situation
(e.g., correctly detecting a duplicate) — it's the case that's still grading
against a stale expected behavior and wrongly flags it as a "regression."
**This means the golden dataset itself needs maintenance** — cases whose
correct answer depends on project state rather than code are especially
vulnerable to this. When a regression warning appears: (1) read the actual
output of the judged target directly to first check "does the situation the
case expected still hold true," and (2) if the premise is broken, replace
the case to match the new premise rather than fixing the judged target (note
why it was replaced, and which replacement number this is, in the case file
itself, so the same investigation doesn't have to be repeated next time).

### 9. Record — a human reviews it and reflects it in standard metrics docs
**Logic**: even if verification itself is automated, for its results to be
usable as the basis for deciding "what to do next," they need to land
somewhere standardized. **Technical mechanism**: log an execution summary to
a structured log. After that, a human reads the results and reflects them
into the standard quality metrics document (and, where needed, a root-cause
record) — this last step is deliberately not automated (if only the numbers
are kept and the "why" isn't recorded, the next person repeats the same
mistake).

## Explicitly manage the coverage-checking tool's own scope, too

Having an automated coverage-checking script that "finds targets whose code
is newer than their last verification and flags them as needing
re-verification" creates an implicit assumption that the set of files the
script sweeps equals "the entire set of verification targets." This
assumption tends to break as the project grows — as internal-use harnesses
that the verification system built to inspect and study itself (judge-bias
experiment scripts, regression-test fixtures, etc.) pile up under the same
directory and file-extension conventions, the coverage-checking script
wrongly flags those, too, as "unverified user-facing targets." **Underlying
knowledge**: this isn't a problem with judge quality — it's a **scoping
problem in the checking script itself**. No matter how accurate the grading
is, feeding it the wrong targets from the start just accumulates noise.
**Technical mechanism**: set up a consistent naming/registration convention
that distinguishes user-facing output from internal system tooling (e.g.,
only list things formally registered as actual work items, or isolate
internal tools under a separate suffix/directory), and have the
checking script follow that convention to skip internal tools from the
start. Reusing an existing naming convention to filter this way, instead of
hardcoding individual files into an exception list after the fact, holds up
much longer — it doesn't need to be touched again every time a new internal
tool is added.

## Known limitations (stated honestly)

- **Halo effect**: if the actor and the judge share the same model family,
  they may share formatting conventions, which theoretically leaves a risk
  that unrelated items get graded too generously — anti-bias instructions
  are put in the prompt, but empirically testing this by cross-checking with
  a different model as judge is separate work still to be done.
- **A "pass" from this pipeline is a first-pass filter, not final
  verification** — the LLM judge itself can misjudge, and while the
  boundary/askQuality path builds in a structure for human intervention,
  it isn't perfect.
- **Deliberately not running CI (a full automatic run on every change) is
  also a valid option** — if the full case set runs automatically every
  time the instruction document is edited, cost becomes uncontrolled.
  Instead, regression detection (stage 8) provides a minimal safety net.

## When adopting this in a new project

These stages are the pipeline skeleton — the grading threshold (0.8, etc.)
and its margin are being carried over without a mechanism that validates the
value itself, so it's recommended to design, from the very start of
adoption, a way to track "does this value actually correlate with real
output quality." If this pipeline repeatedly turns out to catch its own
flaws (the judge's date-ignorance, case-design defects, incorrectly scoped
safeguards, etc.), that recurrence is itself a signal of this
methodology's core point — that the verification tool is also a target of
verification. It's recommended to record such self-discovery cases in the
project's own postmortems (in the same spirit as the "how the catalog grows"
section of
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)).
