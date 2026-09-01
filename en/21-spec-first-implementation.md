<!-- translated-from: ssot=sha256:18691f465941 own=sha256:4ac0cd5edd98 -->
# Spec-First Implementation — The Actual Effect of Writing the Plan First and Building to It

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/21-spec-first-implementation.md)**

**Version**: 1.0.1
**Content hash**: sha256:7c7a1377b837 (of the body below, excluding the stamp comment, this line, and the version line)

We don't recommend the approach of "have the AI draw up a plan/design
spec first, then implement to that" just as "good practice" — this
crystal presents **quantitative evidence that it actually works**,
together with **exactly how far that evidence extends**.

## The name — three lineages converge here

This isn't a single technique but a pattern that converged from
different eras and fields:

1. **Plan-and-Solve Prompting** (Wang et al. 2023, [arXiv:2305.04091](https://arxiv.org/abs/2305.04091)) —
   LLM reasoning research. Formalized "plan first, then execute to that
   plan" as a prompting technique.
2. **Self-Planning Code Generation** (Jiang et al. 2023, [arXiv:2303.06689](https://arxiv.org/abs/2303.06689), ACM TOSEM) — Code
   generation research. First extracts a plan from requirements, then
   generates code sequentially following that plan.
3. **Spec-first / test-driven development (TDD)** — A software
   engineering practice (Kent Beck, 2002) that predates LLMs. "Write
   the tests/spec before the implementation."
4. Note: this isn't confined to research — it has already been adopted
   as a **product feature** of actual coding-agent tools (e.g., a
   "plan mode") — worth reading as a real-world adoption case.

## Basis (primary source verified) — actual figures

🟢 Verified both papers directly in the original in this session (not
an estimate).

**Plan-and-Solve (PS+) vs. Zero-shot-CoT** (same model, only the
prompting method differs):

| Benchmark | Zero-shot-CoT | PS+ | 8-shot Manual-CoT (reference) |
|---|---|---|---|
| GSM8K | 56.4% | **59.3%** | 58.4% |
| SVAMP | 69.9% | **75.7%** | 80.3% |
| MultiArith | 83.8% | **91.8%** | 93.6% |

Simply planning first, with no examples (few-shot) at all, gets close
to or exceeds few-shot-level performance.

**Self-Planning Code Generation**: up to a **+25.4%** relative
improvement in Pass@1 over direct code generation, and up to a
**+11.9%** improvement over CoT-based code generation — human
evaluation also confirmed improvement across all three axes of
correctness, readability, and robustness.

## Relationship to other crystals in this framework

| Crystal | Relationship |
|---|---|
| [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) | Stage 1 (Load)'s principle of "fix the criteria first, then look at the execution result" is this crystal's software-verification counterpart |
| [09-project-structure-template.md](09-project-structure-template.md) | This crystal quantitatively backs the principle that "even a one-person project should fix the scaffolding schema first before starting" |
| [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) | The precondition for being able to take on deliberate, considered debt (planning ahead and consciously choosing a shortcut) is exactly this crystal's habit of "plan first" |

## Working ≠ no longer needing verification/iteration — an honest boundary

Both papers **only claim it improves first-attempt quality** — neither
claims that "verification or iteration is no longer needed." Citing
them past this boundary would itself fall under item 2 of
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
(false precision — claiming more strongly than the evidence actually
supports).

**A real-world application case (n=1, not statistical evidence, stated
honestly)**: in one actual build using this framework, where a
plan → design spec → evaluation criteria were finalized before
implementation, **20 of 22 criteria (91%) passed on the very first
round of automated verification**. The direction matches the pattern
in the papers above, but this single case is not generalized into an
effect size. The remaining 2 were actually bugs in the verification
script itself — meaning "writing the spec first" didn't eliminate bugs
outright; diagnosing and fixing the cause still required iteration.

## Scope boundary — don't mix what's verified with what's merely inferred

🟢 The scope the two papers above actually measured: **single
math-problem reasoning** and **single-function-scale code generation**.
🟠 There is **no** evidence that the same effect size carries over into
the context this crystal is set in (a multi-file product build running
from plan → design → data → backend → frontend → evaluation) — the
direction is likely the same, but this is only an inference, not
overstated as a verified fact. As scale grows, the complexity of the
"plan" itself grows too, so there's theoretically also a risk that
errors at the planning stage get amplified even more (a counter-
hypothesis this session did not verify — its existence isn't being
hidden).

## How to apply it

1. Before starting the implementation (code), **write the spec document
   first** — don't just plan within the prompt; leave it as a file so
   the next steps (implementation, evaluation) can reference that file
   (a stronger version than a mere prompting technique — a human can
   also read and verify it later).
2. In the spec, separate at minimum **what you're building (the plan)**
   from **how you'll judge it (the evaluation criteria)** — combining
   them into one reduces the effectiveness of guarding against
   confirmation bias (retroactively tailoring criteria to fit the
   desired result).
3. Don't write the spec and then skip actual verification (crystal
   #4) — this crystal alone only guarantees that "the first attempt is
   better," not that "the result is correct."
