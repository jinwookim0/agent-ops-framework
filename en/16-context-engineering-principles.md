<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Context Engineering Principles — Designing What the Agent Sees

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/16-context-engineering-principles.md)**

**Version**: 1.0.0
**Content hash**: sha256:dfe912598dd8 (of the body below, excluding the stamp comment, this line, and the version line)

Writing a good prompt is different from **designing the entire context an
agent sees at every moment**. This crystal lays out those design
principles — as an AI agent project grows, "what goes into context"
starts to matter more for output quality than "what goes into the
prompt."

## Basis (primary source verified)

🟢 Anthropic, "Effective context engineering for AI agents"
(anthropic.com/engineering), verified directly against the original.
Because it's a hands-on guide published directly by the people who build
Claude-Code-style agents, this is the most "meta" document in this
crystal collection — it's a first-party directive from the organization
that built the very tool this framework runs on.

## Core definition

We use the source's definition of "context engineering" verbatim —
**"the art and science of curating what to put into a limited context
window, from the ever-changing universe of possible information."**
Core principle: **"find the smallest possible set of high-signal tokens
that maximizes the likelihood of getting the outcome you want."** — The
goal isn't to pack in more, it's to pack in less, but precisely the
right things.

## Five practical principles

### 1. System prompts — find the "right altitude"
Between logic that's hardcoded too specifically (brittle) and guidance
that's too vague (ineffective), find the point that provides heuristics
flexible enough to still guide behavior effectively. Use XML tags or
markdown headers to structure sections. **Start with a minimal prompt
and add clarity only when failure cases are found** — don't write a
sprawling document up front that anticipates every exception.

### 2. Tool design — a minimal viable set
Design tools to be self-contained and unambiguous, with no functional
overlap between them. It should be clear which tool to use in which
situation. Curate a **"minimal viable set"** rather than a vast toolbox.
Keep return values token-efficient.

### 3. Examples (few-shot) — canonical, not exhaustive
Instead of an exhaustive list of edge cases, provide **diverse,
canonical examples that effectively illustrate the expected behavior**.

### 4. Dynamic context retrieval — "just in time"
Instead of pre-processing all data into context up front, use a
"just-in-time" strategy with lightweight identifiers (file paths, links,
queries) — the same way a person uses an external indexing system.
Fetch things when they're actually needed.

### 5. Techniques for long-horizon tasks — three of them
- **Compaction**: As you approach the context limit, summarize the
  conversation while preserving structural decisions and discarding
  redundant output.
- **Structured note-taking**: Have the agent maintain memory that
  persists outside the context window.
- **Sub-agent architectures**: Delegate specialized work to dedicated
  agents and receive back only a condensed summary.

### Before compacting: is this document even the kind that compresses?
Not every bloated shared document has the same room to compress. Before
attempting compaction, first distinguish the document's nature —
**history-log-style** documents (the same topic accumulates narratively
across many dates; old trial-and-error can be collapsed into a one-line
conclusion without losing information) and **living-rulebook-style**
documents (a set of live rules that other documents/code reference
directly by number or name, where most sentences are themselves
reference targets and so have essentially no slack to cut) call for
different compression strategies. Treating the latter like the former
leads to repeatedly re-litigating "why isn't this getting smaller," and
forcing a cut breaks references. In practice, when the same
over-threshold warning was tried against both types of document, the
history-log document actually shrank by nearly half, while the
living-rulebook document had only a few percent that could safely be
cut — knowing this distinction in advance would have saved the
re-review time spent on the latter. Also, when compacting a
history-log-style document, if the full account of an incident is
already recorded without loss in another document (e.g., a
postmortem), it's safer to shrink the entry to a pointer to that
document rather than re-narrate it — since the original is preserved
elsewhere, this isn't information loss.

## Relationship to other crystals in this framework

| Principle | Related crystal |
|---|---|
| Minimal high-signal tokens | The "memory ceiling" in [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) — prose lessons that just keep accumulating move in the opposite direction from context engineering (degraded signal-to-noise ratio) |
| Just-in-time retrieval | "Reference long logs via search" in [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) — the same principle as accessing structured logs by relevance-ranked search instead of re-reading everything |
| Sub-agent delegation | The same spirit as the workflow pipeline (parallelization points) in section 3.3 of [09-project-structure-template.md](09-project-structure-template.md) — split off independent sub-tasks so they don't pollute the shared context |
| "Right altitude" for system prompts | The same balance [02-directive-registry.md](02-directive-registry.md) strikes between accumulating every directive verbatim and compressing that down into actual execution guidance (SKILL.md-type files) |

## Where this principle conflicts with another crystal — stated honestly

[02-directive-registry.md](02-directive-registry.md) holds the
principle "accumulate every directive verbatim," while this crystal
holds the principle "put only the smallest possible set of tokens into
context" — on the surface, these look like opposite directions.
**In reality they operate at different layers**: the Directive Registry
preserves the original text **at storage time**, for the sake of
auditability, while this crystal is about **execution time** — loading
into context only the currently relevant portion of what's stored. "Store
everything, but retrieve only what's needed" satisfies both at once
(just-in-time retrieval is exactly the mechanism for this).

## Related documents
- Anthropic, "Effective context engineering for AI agents" —
  anthropic.com/engineering (the original, this crystal's sole primary
  source)
