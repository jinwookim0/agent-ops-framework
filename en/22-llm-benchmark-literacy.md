<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# How to Read LLM Benchmarks — What They Measure, What They Miss, and How Much to Trust Them

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/22-llm-benchmark-literacy.md)**

**Version**: 1.0.1
**Content hash**: sha256:a5397712d4ea (of the body below, excluding the stamp comment, this line, and the version line)

[21-spec-first-implementation.md](21-spec-first-implementation.md) cited a
number like "GSM8K 56.4%→59.3%" as supporting evidence — this crystal
answers the next question: **how should you read that number itself, and
how much should you trust it?** Citing a benchmark's name is not the same
as knowing what it measures and what it doesn't.

## 1. A Map of the Major Benchmarks — Verified Against Primary Sources

🟢 All of the following were verified directly against the original papers
while writing this crystal.

| Benchmark | What it measures | Scale/format | Source |
|---|---|---|---|
| **GSM8K** | Grade-school-level multi-step arithmetic reasoning | 8,500 word problems | Cobbe et al. 2021 (OpenAI), [arXiv:2110.14168](https://arxiv.org/abs/2110.14168) |
| **MMLU** | Multiple-choice knowledge and problem-solving across 57 subjects (math, history, law, medicine, etc.) | Aggregated across 57 subjects | Hendrycks et al. 2020, [arXiv:2009.03300](https://arxiv.org/abs/2009.03300) |
| **HumanEval** | Single-function-scale code generation (scored via pass@k) | Pairs of function signature + docstring + test cases | Chen et al. 2021 (OpenAI Codex paper), [arXiv:2107.03374](https://arxiv.org/abs/2107.03374) |
| **SWE-bench** | Resolving real GitHub issues via codebase edits | 2,294 instances, drawn from 12 real open-source repositories | Jimenez et al. 2023, [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) |
| **MT-Bench / Chatbot Arena** | Multi-turn conversation quality (by human preference) | Crowdsourced pairwise-comparison votes (3K expert votes + 30K conversations) | Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685) |

## 2. Two Fundamentally Different Kinds of Benchmark — Why Their Trustworthiness Differs

### (A) Static answer-key benchmarks (GSM8K, MMLU, HumanEval, SWE-bench)
A fixed set of problems plus a fixed set of correct answers/test cases.
**Advantage**: reproducible, cheap to score. **Fatal weakness**:
**contamination** — if benchmark problems are already present in a model's
pretraining data, the benchmark ends up measuring "memorization" rather
than "reasoning."

🟢 Empirical evidence (verified against Yang et al., arXiv:2311.04850): in
public pretraining datasets (RedPajama-Data-1T, StarCoder-Data), **8–18%
of HumanEval problems were already present.** More seriously, simple
string-matching detection methods (n-gram overlap) **can be easily evaded
just by paraphrasing or translating the problem** — the paper even
documents a case where a 13B-scale model overfit on lightly reworded
benchmark data and mimicked GPT-4-level performance.

### (B) Dynamic human evaluation (Chatbot Arena)
There is no fixed problem set — humans vote in real time on comparisons
between two models' answers. **Advantage**: contamination is structurally
impossible (the problems themselves keep being generated fresh).
**Weakness**: high cost, and questions about the representativeness of the
sample (who is voting).

🟢 Empirical evidence (verified against Zheng et al. 2023): when GPT-4 is
used as the judge, it agrees with human judgments **more than 80% of the
time** — which is on par with the rate at which humans agree with each
other. In other words, the fact that LLM judges aren't perfect is also
confirmed to be simply because human judges were never perfect to begin
with.

**Bottom line**: when handed a citation of a type-(A) benchmark number,
always add "could this model have seen this exact problem during
training?" to your list of doubts. Type-(B) benchmarks carry low
contamination risk, but separately question "does this voting sample
actually represent the real user base?"

## 3. What Benchmarks Can Never Cover

- **Tasks with no single correct answer**: creative work, strategic
  judgment, value judgments, the emotional nuance of relationships — every
  benchmark above presupposes a task with one fixed correct answer. This is
  the same boundary that criterion 8 of
  [01-definition-of-done.md](01-definition-of-done.md) already covers: "in
  domains where humans are better, don't force in a justification for AI's
  comparative advantage."
- **Task scale/context**: HumanEval operates at the scale of a **single
  function**. A real multi-file software project (the scale addressed by
  this framework's
  [09-project-structure-template.md](09-project-structure-template.md), for
  example) differs in both difficulty and failure modes. SWE-bench was
  built to close this gap, but even so, its own paper openly admits that
  **even the top-performing model had a very low resolve rate** (Claude 2
  resolved 1.96% at the time of publication) — meaning real-world software
  engineering is far harder than function-level benchmarks suggest.
- **The interpretation trap of benchmark saturation**: once a baseline is
  already high, as with MultiArith (83.8%→91.8%), the remaining errors
  might not be "easy cases that were missed by chance" but rather "only the
  genuinely hard residual cases left" — meaning the same percentage-point
  gain on a saturated benchmark can represent a harder achievement than an
  equal percentage-point gain earlier on. You cannot compare the two ranges
  as equally weighted just by looking at the raw numbers.

## 4. Absolute vs. Relative Improvement — the Most Common Misreading

The "Pass@1 up to +25.4%" cited by Crystal 21 is a **relative
improvement**, not an absolute percentage point (pp) figure — meaning that
if the baseline was 40%, it translates to 40%×1.254 ≈ 50.2% (an absolute
+10.2pp), not "jumping from 40% to 65%" (Crystal 21's own text did in fact
correctly label it as a "relative improvement" — this isn't a case that
needs correcting, but is kept here as an example of the risk that **even
with accurate labeling, when both kinds (absolute and relative) appear
mixed within a single document, a reader skimming through can still easily
miss the distinction**). By contrast, GSM8K's "56.4%→59.3%" is an
**absolute pp difference** (59.3−56.4 = 2.9pp, which converts to roughly
+5.1% in relative terms). **Get in the habit of stating explicitly, every
time you cite a number, whether it's absolute or relative** (this belongs
to the same family of traps as item 2, "false precision," in
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) — a
number that looks precise can actually deepen misunderstanding when what
it's measuring is unclear).

## 5. Checklist for When You're Handed a New Benchmark Number

- [ ] **Is it a static benchmark or dynamic human evaluation?** — if
      static, add contamination risk to your list of doubts.
- [ ] **Is it an absolute pp figure or a relative % figure?** — distinguish
      the two and rewrite the claim accordingly.
- [ ] **Does the paper report sample size, confidence interval, and
      whether runs were repeated?** — if not, note explicitly that there's
      no basis for judging whether the difference is larger than noise.
- [ ] **How close is this benchmark's task scale/distribution to the
      real-world context you're now trying to make a judgment about?** —
      don't pull a single-function-scale benchmark number in as evidence
      for building a multi-file project (the same principle as the "scope
      boundary" section of
      [21-spec-first-implementation.md](21-spec-first-implementation.md)).
- [ ] **Is there separate evidence that improved benchmark rank actually
      translates into a better real-world user experience**, or are you
      mistaking the benchmark improvement itself for the ultimate goal
      (connects to the "the end beneficiary is the user" principle in
      [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
      — topping a benchmark is not the goal; user outcomes are the goal).

## Related crystals
- [21-spec-first-implementation.md](21-spec-first-implementation.md) —
  supplied the citation this crystal actually had to go back and reread.
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
  apply the contamination/sample/absolute-vs-relative traps covered here
  when designing evaluations for this repo/project's own work.
- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  the difference between a number that merely looks precise and one that
  has actually been verified (item 2).
