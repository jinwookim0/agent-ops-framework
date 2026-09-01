<!-- translated-from: ssot=sha256:a49ec9f9ac1b own=sha256:7b2ac5c66411 -->
# Execution-Mode Escalation Ladder — When to Move Up to Parallel or Split Execution

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/36-execution-mode-escalation-ladder.md)**

**Version**: 1.0.2
**Content hash**: sha256:d5c335eb4e7a (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟡 Field-tested through repeated use inside a single skill in the source project (has a passing eval-case record), but whether this exact four-tier ladder holds up in other projects or teams hasn't been checked — no external standard was compared against; this is an internally repeated, verified practice from within this one project.

When an AI agent receives a task, deciding "keep going in the current mode (single session, sequential) or escalate to parallel/split execution" by gut feel goes wrong in both directions — always staying sequential means even obviously independent subtasks get handled slowly, and always reaching for parallelism first just adds setup cost and scatters context, making things less accurate. This crystal defines an explicit ladder: **the default is always the cheapest option, and you move up one step at a time only when a concrete signal appears.**

## The four levels

| Level | What it does | When |
|---|---|---|
| L0. Single session, sequential | Keep doing what you're already doing | **Default** — if none of the signals below are present, this is the right answer |
| L1. In-session subagent | Delegate an independent exploration/research/review task and just take the result | When the subtask is light and one-off |
| L2. Multi-stage pipeline tooling | Orchestrate a multi-stage pipeline + parallel fan-out + verification in code | When the subtask has multiple stages and each stage needs verification |
| L3. Fully separated parallel execution environment | Physically run separate sessions in parallel, in isolated branches/isolated workspaces | When working on mutually unrelated projects/features at the same time |

Higher levels are more powerful but cost more to set up — **start at L0, and move up one step only when the signals below appear.**

## Four signals that justify escalating — without at least one, don't escalate

1. Does the task at hand actually split into **three or more mutually independent subtasks**?
2. Have you started a **long-running task** and are you just **waiting** for the result — running it in the background but not doing anything else while you wait, when you could?
3. Would being wrong be **expensive**, and is the judgment still relying on **only one perspective**?
4. Are you bouncing between **two unrelated tasks/contexts** in the same session, re-explaining the context each time?

**What not to do**: for a discussion that needs continuous context (gradually refining a design through conversation), for narrowly and deeply polishing a single task step by step, or for quickly exchanging a series of small edits — forcibly splitting these across multiple sessions/agents scatters context and makes things **slower and less accurate.** The right frame isn't "parallelize = always better," it's "parallelize only when a specific signal is present."

## Accuracy lever (usable right away at L0, no escalation needed)

Judging alone means you can't see your own blind spots — for an important output, having yourself (or a separate execution unit) "try to refute this result" is the cheapest accuracy lever usable directly within L0, without escalating.

## Creativity lever — multiple independent attempts, then synthesize ("judge panel")

Sequential dialogue tends to anchor on the first idea. **The more open-ended a design/planning/brainstorming question is** (no single correct answer), the more genuinely creative the result when you deliberately produce independent drafts from different perspectives (e.g., completeness-first / risk-first / user-first) and then compare and synthesize them. Conversely, this is overkill for something with a clearly correct answer, like a bug fix — don't use it there.

**How this differs from self-consistency in [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) (G3)**: self-consistency uses majority voting across parallel runs to reduce noise on a **verifiable judgment**, while this lever deliberately creates different perspectives to avoid anchoring on the first idea for an **open-ended output with no verifiable answer** — the purposes (variance reduction vs. perspective diversification) are close to opposite.

## Decision flow

```
New task received
  ├─ Is it a separate task unrelated to the current session's context? → L3
  ├─ 3+ independent subtasks that need stage-by-stage verification? → L2
  ├─ Independent subtasks that are light and one-off? → L1
  ├─ An open-ended design/planning/brainstorming question with no single right answer? → judge panel (multiple independent attempts → synthesize)
  └─ None of the above → stay at L0 (remember: parallelizing isn't always better)

+ If a long-running task is already underway: don't wait — keep handling other requests in the meantime.
+ Once a result comes back, if the output matters for accuracy: consider verifying it once more from a separate perspective.
```

## How this differs from crystal 09 (G3)

The "Skill vs. Workflow" decision criterion in section 3.3 of [09-project-structure-template.md](09-project-structure-template.md) is a narrower judgment — **which format to write a single piece of execution logic in** (a single call vs. a multi-stage pipeline) — and L2 of this ladder corresponds exactly to that point. This ladder covers a broader question: **whether to go to parallel/split execution at all**, judged from signals at the moment a task is received. It also includes L3 (fully separated parallel execution environment), which crystal 09 doesn't cover.

## Honest limits

- The four-tier ladder structure itself has been field-tested through repeated use inside a single skill in the source project (has a passing eval-case record) — but since it's the design of a single skill, whether these exact level boundaries are optimal for other projects hasn't been verified. The signals themselves (number of independent subtasks, cost of waiting, number of perspectives in the judgment, frequency of context-switching) generalize, but a specific threshold like "3 or more" may need to be re-tuned by each project to fit its own situation.

## Related
- [09-project-structure-template.md](09-project-structure-template.md) — the narrower decision corresponding to L2 (Skill vs. Workflow format).
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) — self-consistency (parallelism with the opposite purpose: variance reduction).
- [16-context-engineering-principles.md](16-context-engineering-principles.md) — why subagent delegation doesn't pollute context (the basis for L1).
- [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md) — the risk of parallel batches amplifying quota exhaustion (a cost-side warning for escalation).
