<!-- translated-from: ssot=sha256:0c0d29b48282 own=sha256:d9a60c68edf1 -->
# Project Structure Template for AI-Agent-Managed Projects — A Five-Layer Architecture

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/09-project-structure-template.md)**

**Version**: 1.0.1
**Content hash**: sha256:bbb8ea3fce95 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 Draws on the C4 model's (arc42) zoom-level
concept, and the 5-layer structure/13-step order is a post-hoc write-up
of the order (or something close to it) the original project actually
grew in.

This captures both the **overall view (what exists)** and **how to
actually build it (schema and ordering)** — the starting premise of this
template is that an overview alone doesn't let you reconstruct the thing.
It borrows the "zoom levels" (Context → Container → Component) from the
[C4 model](https://arc42.org/overview/).

## 1. Architecture — five layers

```
tasks/          Defines "what work this is" (metadata: oversight grade, confidence
                grade, domain, cadence, etc.)
  ↓ 1:1 mapping
Execution logic layer  A single-run skill if repetitive, or a workflow
                if it's a multi-stage pipeline
  ↓ accumulates into
Shared context layer  Context that builds up across tasks (preferences, history) —
                the reason quality improves with repetition
  ↓ governed by
Governance layer  "How do we judge, and by what standard is something done" —
                DoD/DoR, decision log, directive registry, glossary
  ↓ finished product
Product layer      The finished output shown to the user
```

Each layer scales independently — adding a new task doesn't require
rewriting the governance documents each time (existing DoD/DoR criteria
apply as-is), and adding a new product doesn't touch the task layer's
structure.

## 2. Key concept mapping table

| Axis | Values | Meaning |
|---|---|---|
| Actionability classification | has-an-end / ongoing / reference-material / on-hold | What kind of item this is (a PARA-style classification) |
| Domain | work/life/meta/cross | Whether the task is about work, personal life, infrastructure, or deliberate integration |
| Oversight grade (`oversight_gate`) | none/notify/confirm | Whether execution involves irreversible actions (the **action** axis) |
| Confidence grade (`confidence_gate`) | none/flag/ask | How confident the content of the output is (the **content** axis — different from the action axis) |
| Direction of completion criteria | DoD → DoR | The criteria for "it's fully built" → the criteria for "it's okay to start" (after-the-fact → before-the-fact) |

## 3. Detailed spec per layer — copy this as-is and fill it in; it's meant to be reconstructable

### 3.1 Task definitions — exact schema

Full set of metadata fields (YAML frontmatter):
```yaml
---
name: <task-name>
status: draft | active | paused | done | note
cadence: one-off | daily | weekly | per-sprint | on-demand | as-needed | monthly
success_criteria: "One sentence describing what output counts as success"
tools: [WebSearch, WebFetch, Bash, ...]        # Only the tools actually used
executor: Skill | Workflow | ad-hoc session
oversight_gate: none | notify | confirm         # The irreversibility-of-action axis
confidence_gate: none | flag | ask               # The output-confidence axis (different from oversight_gate)
domain: work | life | meta | cross               # Which area of life/work this belongs to
irreversible_actions: []   # e.g., [overwrite_existing_file, git_commit, git_push, external_send]
---
```
Required body sections (fixed order): `## Purpose` → `## Input` → `## Output`
→ (add `## Accumulated Context` for a repeating task) → `## Why This Task
Is Suited to AI Management` (the 6-item checklist below) → `## Execution`
→ `## AI's Comparative Advantage` (no generalities — at least one concrete
line about a bottleneck a human actually experiences).

**Optional section — Out of scope (to avoid duplication)**: As the number
of tasks grows, the boundaries with adjacent tasks blur ("how is this
different from that other task?"). When there's a task it could
overlap with, name that task in an `## Out of Scope` section and state
explicitly, "This task does not cover X; use <other task name> for X" —
so that when the same question recurs later, this one line answers it
instead of requiring a fresh judgment call each time.

**6-item suitability checklist** — the criteria for screening whether a
new idea should be incorporated as a task:
- [ ] Is the output format structured?
- [ ] Can it be repeated with the same template?
- [ ] Does it decompose into research → draft → verify stages?
- [ ] Is the cost of being wrong low, and is review easy?
- [ ] If it needs current information, can search tools supplement it?
- [ ] Does accumulated preference/context improve quality with repetition?

**Bootstrap procedure**: Copy the template into a new task directory →
fill in the metadata and sections above → write execution logic matching
how it will run → add eval cases (section 3.4) → run a sensitive-data
scan → add one row to the root index with the domain value.

### 3.2 Single-run skill — execution logic (for a repeating single run)

```markdown
---
name: <task-name>
description: One-line description (including trigger condition)
---

## Procedure
1. **Confirm input**: Check the needed information, and ask if something
   is missing. Consult relevant records in shared context if they exist.
2. **Research**: Use search tools when currency matters, and keep the
   sources.
3. (Domain-specific steps)
4. **Produce the output**
5. **Save**: Ask whether to save to the designated path.
6. **Update context**: Propose adding any newly surfaced preferences to
   shared context.

## Principles
- Mark information you're not certain of as "needs confirmation" (don't guess)
- Generalize third-party information instead of using real names; don't
  store sensitive data in the output
```

**P99 rare/high-risk scenario registry (only for applicable domains)**: A
skill that works in a domain touching human safety, health, finances, or
other hard-to-reverse outcomes should keep a separate
`<task-dir>/p99-scenarios.md` file, apart from the body above — it lists
inputs that are low-probability but severe in consequence (signs of a
medical emergency, signs of abuse or self-harm, indicators of fraud, etc.)
and states the rule that **when this scenario is detected, it takes
precedence over the skill's normal procedure**. The reason for a separate
file: it keeps the context for the everyday procedure that runs daily
from getting heavy, while still ensuring the rare-but-needed case isn't
missed — the name borrows the metaphor from SRE's practice of observing
p99 latency (tail-probability, high-severity events), but that doesn't
mean that literature validates this safety-triage mechanism itself.

### 3.3 Multi-stage workflow — execution logic (for pipelines)

**Decision rule versus Skill**: If it's repetitive but finishes in a
single call, use a Skill; if it has multiple stages — research → draft →
independent verification → comparison → finalize — with room for
parallelization, use a Workflow.

```js
export const meta = {                 // Must be a pure literal (no variables/computation)
  name: "task-name",
  description: "...",
  phases: [{ title: "Discover", detail: "..." }, { title: "Digest", detail: "..." }],
};

phase("Discover");
const found = await agent(`...`, { schema: SOME_SCHEMA });

const results = await pipeline(              // Each item passes through the stages independently
  items,
  (item) => agent(`step 1 prompt`, { phase: "Digest", label: `step1:${item.id}` }),
  (prev, item) => parallel([                  // Parallelization point (e.g., independent quantitative/qualitative verification)
    () => agent(`verification A`, { phase: "Digest" }),
    () => agent(`verification B`, { phase: "Digest" }),
  ]).then(([a, b]) => ({ ...prev, a, b })),
);
return { results };
```

**Pitfall (must know when reconstructing this)**: If the workflow
execution tool treats "a script registered by name" differently from "a
script specified directly by path" (i.e., an implementation that reuses a
snapshot taken at registration time during the session, so editing the
file doesn't get picked up), then immediately after an edit you must call
it by direct path specification first and confirm from the output that
the change is reflected, before switching back to calling it by name.

### 3.4 Eval cases — verification

```yaml
---
target_type: skill | workflow
rubric:
  - "Judging criterion sentence 1 — a property this task's output must have"
  - "Judging criterion sentence 2 ..."
pass_threshold: 0.8
---

## Case 1: <scenario name>
### Input
(concrete input value)
### Expected behavior
- (what must come out of this input)
```
The rubric must be "concrete criteria specific to this domain," not
generalities.

### 3.5 Shared context layer

| File | Role |
|---|---|
| Preferences/history file | Preferences (tastes, recurring patterns, etc.) that accumulate across tasks |
| Notification recipients | Not repeated inline, to minimize re-identification fingerprints |
| Persona definitions | (if any) |
| Reusable prompt fragments | |
| Cost usage log | Measured logs (archived once stale) |
| Local-only directory | Where sensitive data is kept out of version-control tracking |

### 3.6 Governance layer — the minimal set actually needed

Not everything is needed all at once — the right order is to **set up the
document for a given kind of debt when that debt starts accumulating**:

| Minimal set | When it becomes necessary |
|---|---|
| Definition of Done | Once tasks exceed 3–5 and "it's done" starts meaning different things to different people |
| Prompt/PII guardrails + scanner | The moment the first task that handles personal data appears (must not be deferred) |
| Eval infrastructure | Once eyeballing output quality every time becomes unwieldy |
| Debt classification scheme | When you need to measure "how much has accumulated unverified" |
| Decision log + directive registry | Once accumulated autonomous judgments and directives make "why did we decide this" recur |
| Architecture Decision Records (ADR) | Once structural design decisions (why this approach) are worth revisiting |
| Postmortem folder set | The moment the first actual incident happens (it's fine to create the folders in advance, empty) |

### 3.7 Productization pipeline

```
1. Raw output (discover→summarize→verify→organize)
        ↓ Restructure for human readability (not an automatic conversion — written by hand)
2. Product HTML (design-token CSS, light/dark support)
        ↓ Publish
3. Actual published URL
        ↓ Index
4. Hub page — stats + card listing
        ↓ Record
5. Per-batch README — what was done, updated stats, remaining backlog
```
The product HTML's CSS is built from a reusable token system — when
making a new product, the practical convention is to copy an existing
file wholesale and change only the content, rather than designing a new
design system every time.

## 4. Step-by-step order for rebuilding from scratch

Later steps are meaningless without the earlier ones:

1. **Project skeleton**: A root index (even just an empty task list
   table), one-off/recurring task templates — without this, you'd have to
   design each task from scratch every time.
2. **Minimal DoD** (3–4 criteria is fine to start) — without a common
   standard for "done," adding more tasks means everything has to be
   redone later.
3. **Build the first 3–5 tasks yourself as single-run skills** (starting
   with simple ones). This is where the schema in 3.1–3.2 gets validated
   in practice.
4. **Prompt/PII guardrails + scanner** — must come before even a single
   task that handles personal data exists (adding it after the fact means
   the far more expensive job of erasing data that's already been
   exposed).
5. **Eval infrastructure** — by now tasks have grown enough that eyeballing
   quality each time is hard. Introduce case-based rubric scoring.
6. **Set up the postmortem folder set in advance** (it's fine to leave it
   empty) — so that when the first actual incident happens, there's
   already a place to record it, and it doesn't get deferred to "we'll
   make one when it happens."
7. **Diversify tasks across domains** (e.g., both work and personal life)
   — introducing the domain axis from the start at this point means you
   don't have to retroactively tag everything later (lesson: an axis
   you'll need later is cheaper to add to the schema from the beginning).
8. **Decision log + directive registry** — the point where you start
   gathering the rationale behind judgments in one place instead of
   leaving it scattered "in commit messages only." Once judgments
   accumulate to 5–10, not having this already starts causing confusion.
9. **ADR** — the point where structural decisions (why this architecture,
   why this field) become worth revisiting (usually around the same time
   as step 8).
10. **Expand to recurring (cadence≠one-off) tasks** — from this point on,
    oversight grades (the rule against `confirm` during unattended
    execution) become practically important.
11. **Build the first product pipeline** (see 3.7) — pick one
    content-accumulating task, strengthen its verification logic, and
    separate the human-facing final output into its own layer. **This
    order matters** — productizing first while verification logic is
    still weak only increases the number of outputs without increasing
    trustworthiness.
12. **Add cross-cutting axes when they become necessary** (confidence
    grade, domain, etc.) — handle retroactive application with a script
    in bulk — don't fix dozens of items by hand one at a time.
13. **Second-order governance** (governance of governance): once the
    number of documents grows, you'll need a priority map, a unified
    glossary, an auto-generated index to prevent re-lookups, and this
    blueprint itself — build it too early and it's excess infrastructure,
    too late and cognitive debt has already piled up.

## 5. How to validate this template

This five-layer structure is a retrospective organization of what
actually formed naturally, in this order (or a similar one), as a real
project grew — it wasn't planned as these 13 steps from the start; there
is an actual history of it being built all at once, "big bang" style, and
then continuously refined afterward. When porting it to a new project,
follow the 13 steps in order, but at each step judge "is this actually
needed right now" — that's the recommendation, to avoid investing in
infrastructure too early (the same principle as the "too early means
excess infrastructure" warning in section 4 [step 13]).
