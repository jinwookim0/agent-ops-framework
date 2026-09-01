<!-- translated-from: ssot=sha256:7603bb94ea55 own=sha256:caa8dfa4d5f4 -->
# agent-ops-framework — A Collection of Structural Crystals for Operating AI-Agent Projects

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/README.md)**

## What this is

Projects where an AI agent manages multiple tasks usually mix together
**domain content** (what the project actually deals with — every project has
its own) with the **operating practices** that produce that content
(governance, quality bars, guardrails, self-improvement loops).

This folder extracts only the latter — it holds **only the structural
patterns** that work the same way no matter which domain or project you
attach them to. "What this project dealt with" is not in here; what's left
is **the process itself** — things like "how do you define when a task is
done," "how do you accumulate and index directives," "how do you catch the
pattern where an AI says something plausible but wrong," and "how do you
enforce that secrets never leak into a prompt."

## Why "crystal"

Principles like these usually grow out of real incidents, corrections, and
hands-on experience — that narrative is itself part of what makes them
credible ("this wasn't invented out of thin air, it came out of a real
incident"). But that narrative is entangled with dates, proper nouns
specific to one project, and details of a particular incident, so carrying
it over as-is into another project leaves behind references that no longer
fit. Every document in this folder is a **"crystal" version — the narrative
stripped away, leaving only the pattern**: the general rationale for why the
rule is needed stays, while project-specific instances like "in this
project we got this particular case wrong twice" are compressed into
generalized examples or dropped entirely.

**This principle applies to this README itself** — the list below carries
no dates or "which question this was written in response to"
origin-narrative. That kind of narrative (when, why, and under what request
this document came to exist) belongs on the original project's own
directive-history document, not in this folder, which is meant to travel to
other projects.

## The number is the order it was added, not its importance — priority lives here instead

The number (`NN-`) on each crystal below is a **permanent ID recording the
order it was added**, not a ranking of importance — this isn't an
oversight, it's a deliberate design choice: keeping the number a stable
identifier means nothing breaks — not the links where one crystal
references another (like `[05-...](05-...)`), not references from
projects that adopt this folder, and not citations by number in documents
like `directive-registry.md` ([BLUEPRINT.md](BLUEPRINT.md) section 5 —
the same principle ADRs, RFCs, and this folder's own
[02-directive-registry.md](02-directive-registry.md) use: IDs must be
stable and must not carry meaning). Instead, "what to look
at first" is shown separately, as a priority list below — it supplies
ordering information without renumbering anything.

**What to look at first when introducing this into a new project (roughly
in this order)**:
1. [07-prompt-guardrails/](07-prompt-guardrails/) — must come **before**
   the first task that touches personal data (adding it after the fact
   means erasing something already exposed — a much more expensive job).
2. [01-definition-of-done.md](01-definition-of-done.md) — once tasks start
   exceeding 3-5.
3. [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
   once the AI starts running repeatedly without human confirmation.
4. [02-directive-registry.md](02-directive-registry.md) — once directives
   and decisions pile up and "why did we decide this again" starts
   recurring.
5. [09-project-structure-template.md](09-project-structure-template.md) —
   when designing or redesigning the project structure itself.
6. [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) and
   [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) —
   the first time output credibility/quality needs to be measured
   systematically.

The remaining crystals are worth reading once the "why this is needed"
opening of each document actually applies to your own project — there's no
need to bring all of them in at once ([USAGE-GUIDE.md](USAGE-GUIDE.md)'s
"Planning perspective" walks through the same ordering in more detail). We
don't rank all 37 crystals into one master priority order — what's needed
first genuinely differs project to project, and forcing a single overall
ranking would hide that difference rather than help.

## Organization — by topic

Each crystal can be read and used independently on its own — they reference
each other, but you don't have to read them in order. **Verification
strength** indicates how thoroughly the primary sources a document cites
have been checked (🟢 the primary source's core content directly verified /
🟡 only the skeleton/names verified, with details reconstructed by the
document itself — stated explicitly in every document so as not to overstate
confidence). This per-document verification-strength labeling is a
deliberate design choice — even well-known precedents in the same lineage
(e.g., The Twelve-Factor App) only claim collective authority for the whole
set of principles ("seen across hundreds of real-world cases") without
labeling the evidentiary strength of each individual principle. This folder
goes one step further in honesty than that convention, by not hiding,
document by document, how far the verification actually went.

**What this rating actually measures, and doesn't (clarified by a
2026-09-01 red-team review)**: 🟢/🟡 measures **citation fidelity** — was
the primary source the document cites actually opened and checked —
**not whether following this crystal actually produces a better
outcome (efficacy).** These are different questions, and efficacy
verification (e.g. comparing a team that used a crystal against one that
didn't) is a much more expensive kind of evidence that even the external
standards this framework itself cites (RACI, Amershi et al. 2019, NIST
AI RMF, etc.) don't provide either — so this folder doesn't demand it.
Also worth stating plainly: this rating is **self-assigned by the same
AI session that wrote the claim** — it was not verified after the fact
by an independent person or a different model ("self-grading," in other
words). Elsewhere in this folder (e.g. [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)'s
Evaluator gate, [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)'s
self-consistency re-scoring) already requires a mechanism that
structurally suppresses self-grading — this folder is honest that the
admission review for a crystal itself (Gate G1) doesn't yet apply that
same mechanism — a candidate for the next round of expansion.

### Governance & Decision-making — who decides what, and when

| File | Covers | Verification strength |
|---|---|---|
| [02-directive-registry.md](02-directive-registry.md) | How to accumulate and index directives/principles with priority and triggers | 🟢 |
| [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) | Principles for when an autonomously-executing AI agent should stop and when it should keep going | 🟢 |
| [17-ai-risk-management-index.md](17-ai-risk-management-index.md) | An index that rearranges the rest of the crystals under the NIST AI RMF's four functions (Govern/Map/Measure/Manage) | 🟡 only the function names verified against the source; details reconstructed |
| [20-decision-rights-raci.md](20-decision-rights-raci.md) | Responsibility allocation (RACI) when several people share the same AI agent | 🟢 |
| [24-application-deadline-rule.md](24-application-deadline-rule.md) | A rule that puts a deadline on applying research/investigation ideas, so they don't sit indefinitely in "someday" | 🟢 |
| [25-directive-editing-delegation-levels.md](25-directive-editing-delegation-levels.md) | A three-level delegation scale for judging whether an AI may edit the directive documents themselves | 🟢 |

### Quality & Verification — judging completeness & the bar — is it done, how good is it

Split off once it reached 7 crystals (see "Principles for when scale
grows" below) — this axis focuses on "the standard of completion/quality
itself."

| File | Covers | Verification strength |
|---|---|---|
| [01-definition-of-done.md](01-definition-of-done.md) | 10 criteria for judging that "this task is fully done" | 🟢 |
| [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) | A debt-classification scheme plus 5 minimum quality baselines | 🟢 |
| [21-spec-first-implementation.md](21-spec-first-implementation.md) | The quantitative effect, and the limits, of writing a spec first and implementing exactly to it | 🟢 both source papers verified (including the numbers) |

### Quality & Verification — measurement & evidence interpretation — how do you measure and trust that judgment

This axis focuses on "how do you design the measurement itself, and how
much do you trust its results."

| File | Covers | Verification strength |
|---|---|---|
| [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) | An eval-design pipeline for verifying output quality without regressions, plus risk-tiered verification that scales verification strength to the target's risk level | 🟢 |
| [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) | What causes the same input to yield a different answer, and how to handle it | 🟢 abstract verified (not the full original text — stated explicitly in the document) |
| [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md) | How to read credibility, contamination, and absolute-vs-relative framing when handed an LLM benchmark number | 🟢 5 benchmark papers verified against the source |
| [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md) | How to honestly report a self-experiment (hypothesis testing) that has no predefined test case, across three elements: qualitative, quantitative, and confidence | 🟡 the sample-size principle verified against the source; the confidence-marker system is an original design |
| [37-target-metric-gaming-safeguards.md](37-target-metric-gaming-safeguards.md) | Why optimizing a proxy metric breaks its correlation with the true goal (Goodhart's law), and countermeasures like multiple metrics and trip wires | 🟢 verified against the source (all of Amodei et al. 2016's mitigations, DeepMind's real-world examples) |

### Safety & Security — defending against information leakage — what leaks and how

Split off once it reached 7 crystals (see "Principles for when scale grows"
below) — this axis focuses on "through what channel does information leak."

| File | Covers | Verification strength |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | Executable code implementing a 3-layer defense against secrets/personal data leaking into prompts or externally (copy-paste ready) | 🟢 verified with an actual live block test |
| [23-confidential-project-protection.md](23-confidential-project-protection.md) | Protecting project-level confidentiality that pattern-matching can't catch, by enforcing it at the git push level | 🟢 |
| [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md) | How to prevent synthetic inputs used for evals from getting mixed into permanent memory files as if they were real history | 🟡 generalized from an actual incident in the original project |
| [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md) | The risk that individually-safe information becomes a re-identification/targeting risk once combined (quasi-identifier aggregation), and how to respond | 🟡 concept definitions verified against the source; Sweeney's original paper itself not cross-checked |
| [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) | How to scrub, review, and disclose so an employer's confidential information doesn't bleed into content you intend to publish | 🟢 general trade-secret definitions verified against Cornell LII source; practical procedures verified against Google's official guidelines source |

### Safety & Security — defending judgment & reasoning — what goes wrong

This axis focuses on "how does AI/human judgment or reasoning go
plausibly-but-wrong."

| File | Covers | Verification strength |
|---|---|---|
| [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) | A catalog of 12 types of "plausible but fake" reasoning that AI/humans produce, plus how to verify against them | 🟢 |
| [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) | A checklist for defending against adversarial threats (prompt injection, etc.) | 🟢 |
| [26-grounding-validity-audit.md](26-grounding-validity-audit.md) | A procedure for periodically re-checking the citations in an already-written guide document against their original sources | 🟢 |

### Incident Response & Resilience — how do you handle failure

| File | Covers | Verification strength |
|---|---|---|
| [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) | A standard blameless-postmortem template | 🟢 |
| [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md) | Deliberately experimenting with contingency failures before an incident happens (a different axis from red-teaming and postmortems) | 🟢 |
| [27-premortem-planning.md](27-premortem-planning.md) | A technique for pre-assuming failure on a plan not yet executed (the mirror image of a postmortem), plus risk-proportional trigger design | 🟢 core mechanism verified against the source; the psychological lineage (1989) only at skeleton level (🟡) |

### Observability & Self-learning — how do you record and learn from execution results

| File | Covers | Verification strength |
|---|---|---|
| [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) | A loop where an agent records, organizes, and caps "what worked" on its own | 🟢 |
| [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) | Designing agent execution to be shown through logs, not claims | 🟡 the folder's own principles are settled; details of the external standard (OpenTelemetry) explicitly noted as unverified |
| [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md) | Handling token/API call cost and limits (prompt-caching economics, distinguishing limit signals, avoiding parallel-batch waste) | 🟢 caching mechanism verified against official API documentation source; the rest generalized from real operational patterns |
| [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md) | Managing a shared context file that grows across sessions through compaction, archiving, and search, and restoring an equivalent level of context when a session restarts | 🟢 core mechanism verified against MemGPT and official Anthropic documentation sources |

### Interaction & Documentation — what and how do you show people

| File | Covers | Verification strength |
|---|---|---|
| [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) | A checklist of 18 human-AI interaction principles (Amershi et al. 2019) | 🟢 |
| [15-model-card-template.md](15-model-card-template.md) | A 9-section template for documenting an AI capability itself (Mitchell et al. 2019) | 🟢 |
| [16-context-engineering-principles.md](16-context-engineering-principles.md) | 5 principles for designing an agent's context window (Anthropic) | 🟢 |
| [28-writing-craft-guardrails.md](28-writing-craft-guardrails.md) | Self-diagnosis and checklists for removing the "AI smell" from output text (Orwell/Graham/Strunk & White/Zinsser/Vonnegut/Kawasaki) | 🟢 |

### Structure & Reuse — how do you assemble and move projects/features

| File | Covers | Verification strength |
|---|---|---|
| [08-module-format.md](08-module-format.md) | A packaging convention that lets you move a single feature to another project immediately | 🟢 |
| [09-project-structure-template.md](09-project-structure-template.md) | A 5-layer structure for AI-agent-managed projects, plus a 13-step rebuild sequence | 🟢 |
| [33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md) | How to honestly duplicate verified logic and mechanically cross-check it in execution environments where local imports aren't possible | 🟢 |
| [36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md) | A 4-rung, signal-based ladder for escalating the level of parallelization — from a single session, to a subagent, to a pipeline, to separate execution | 🟡 verified through repeated use within the original project (a record of passing evals), no external cross-check |

## Principles for when scale grows

Once you pass 20 crystals, a point arrives where this folder itself needs
the same "memory cap" principle that
[06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)
applies to self-learning rules — adding without limit conflicts with the
"smallest possible high-signal token set" principle in
[16-context-engineering-principles.md](16-context-engineering-principles.md).
**Every time a new expansion candidate comes up for review**: (1) check
whether it actually overlaps with an existing crystal, (2) check whether
verifiable primary sources exist for it, (3) if it doesn't fit any category
in this table, decide whether to create a new category or whether it's out
of scope. Once a category exceeds 6-7 crystals, it's time to split it.
**Quality & Verification and Safety & Security already organize their
tables along two axes each** — the numbers stayed the same; only the
table's category membership was divided ([BLUEPRINT.md](BLUEPRINT.md)
section 5's split rule). Quality & Verification splits into "judging
completeness" (01, 13, 21 — 3) vs. "measurement/evidence interpretation"
(04, 18, 22, 34, 37 — 5); Safety & Security splits into "defending
against information leakage" (07, 23, 31, 32, 35 — 5) vs. "defending
judgment & reasoning" (03, 14, 26 — 3) — neither axis is at 6-7 yet, so
no further split is needed. **Governance & Decision-making hasn't been
split and has reached the 6-7 boundary at 6 (02, 05, 17, 20, 24, 25)** —
the next time a candidate comes up for addition to this category, decide
whether to split first (e.g., "governance of knowledge/directives
themselves" vs. "governance of execution autonomy").

## Usage · Blueprint · Risk Analysis

- [BLUEPRINT.md](BLUEPRINT.md) — what this folder itself is, what criteria
  (an admission gate) a new crystal must pass to be added, and how those
  admission candidates get discovered automatically.
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — what and how to use when introducing
  this framework into a new project, across five perspectives: planning,
  design, implementation, improvement, and reference.
- [REFLECTION-CANDIDATES.md](../ko/REFLECTION-CANDIDATES.md) — an accumulated
  list of candidates automatically discovered, during another project's
  evolution, as patterns worth reflecting back into this folder (output of
  `scripts/agent-ops-framework-reflection-check.py`).
- [RISK-ANALYSIS.md](../ko/RISK-ANALYSIS.md) — an analysis of the actual risk of
  open-sourcing this folder, judged against the original project it came
  from. **This document alone is the explicit exception that carries
  narrative specific to the original project** — it isn't a crystal meant
  to be carried as-is into other projects, but a supplementary document
  that judges "whether it's okay to publish, in this particular case."
- [DISCLAIMER.md](DISCLAIMER.md) — a disclaimer template attached as-is at
  actual publication time. Why it isn't in the numbered crystal list: this
  isn't a methodology to learn but an artifact meant to be posted directly,
  so it needs to be findable on its own ([35](35-personal-oss-employer-confidentiality-separation.md)
  is the methodology behind it).
- [LANGUAGE-POLICY.md](LANGUAGE-POLICY.md) — the runtime configuration
  that decides which of the Korean (SSOT) or English translation an AI
  reads (default, tiers, exceptions).
- [GLOSSARY.md](GLOSSARY.md) — what this folder's recurring terms
  (crystal, story, domain knowledge/domain-neutral, SSOT, gate,
  STALE/DIVERGED, ...) actually mean, in one place.

## What this folder is not

- It does not replace the original project's domain content — that remains
  the project's actual, real-world output.
- It is not a fully separate project that has been independently
  re-verified — the source documents **summarize the record** of
  field-verification (failures found, recurrence-prevention measures) that
  happened inside the original project; this folder itself has not been
  independently re-verified on its own (applied the same way as the
  "verification labels are shown honestly" principle in
  [08-module-format.md](08-module-format.md)).
- Its scope differs from things like `modules/` (packaging that pulls a
  single feature out on its own) — this folder extracts **the operating
  practices of an entire project, not a single feature**.
