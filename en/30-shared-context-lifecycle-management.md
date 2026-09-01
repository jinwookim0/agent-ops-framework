<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Shared Context Lifecycle Management — Compaction, Archiving, and Session Restarts

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/30-shared-context-lifecycle-management.md)**

**Version**: 1.0.0
**Content hash**: sha256:3dd01b4ab60a (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 Core mechanisms verified against primary sources
(papers, official documentation); concrete thresholds (warning/urgent ratios,
etc.) are generalized from patterns repeatedly validated in real-world
operation.

If [16-context-engineering-principles.md](16-context-engineering-principles.md)
covers "how to structure the context window within a session," this crystal
is one level up — it covers **how to manage a shared context file that keeps
accumulating across many sessions as it continues to grow**, and **what's
needed for the next session to recover to an equivalent level even when
compaction loses information**. Where [06-self-improving-heuristics-
loop.md](06-self-improving-heuristics-loop.md)'s "memory cap" principle
applies to a single rule list, this crystal generalizes it to a project's
entire family of shared context files.

## Basis

- 🟢 **MemGPT** (Packer et al., 2023, [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)) —
  verified against the primary source. Core metaphor: "when the main context
  (the desk) fills up, evict older items to external storage (the warehouse),
  and retrieve them again when needed." This crystal's "date-boundary
  archiving + retrieval fallback" axis maps directly onto it.
- 🟢 **Anthropic, "Effective context engineering for AI agents"** (2025-09-29,
  official engineering blog) — already a source for [crystal 16](16-context-engineering-principles.md),
  but this crystal draws on two principles that 16 doesn't yet cover: (1)
  **"recall first, precision later"** — it's safer for compaction to first
  cast a wide net over what might be relevant, and leave precise narrowing to
  a later step. (2) **Deleting tool call results is the lowest-risk target for
  reduction during compaction** — because it's rare to benefit from re-reading
  an old raw lookup result.
- 🟢 Official Claude Code Best Practices — a warning to the effect that "a
  bloated rules document causes the AI to actually ignore instructions" (a
  citation already verified in [26-grounding-validity-audit.md](26-grounding-validity-audit.md), reused here).

## Core Mechanisms

### 1. Ratio-Based Dual Thresholds
Set two stages — warning and urgent — based on **a ratio relative to a
baseline**, rather than an absolute line/byte count (e.g., warning at 1.0x
baseline, urgent at 1.5x) — because "appropriate size" differs per file,
forcing a single absolute value on everything is too early for some files and
too late for others. This is the same idea as MemGPT's own dual 70%/100%
warning/eviction thresholds.

### 2. Lossless Compression First
The default for compaction is not "summarize to shrink" but **preserve all
facts, figures, dates, and decisions, and strip only the connective narrative
(conjunctions, explanatory sentences)**. Information loss is deferred to
mechanisms 3–5 below (separating by date boundary, splitting files), not
allowed to occur in the compaction step itself — this ordering shuts off the
risk that "summarizing shortens it but drops details that can't be
reconstructed."

### 3. Judging Compression Headroom by Document Type
Even among documents that are "compaction targets," a **log-type document**
(append-only, past entries never change again) and an **active rulebook-type
document** (the currently valid rules themselves are the body) differ in how
much compression headroom they have — a log-type document can safely have its
older half cut off wholesale at a date boundary and archived, but cutting a
rulebook-type document that way risks slicing off "rules that are currently in
effect," so only sentence-level compression (deduplication, condensing
phrasing) applies to it.

### 4. Date-Boundary Archiving
When a log-type document exceeds its threshold, don't summarize — instead
**move the older half (or everything before a given date) intact into a
separate archive file** — zero information loss. The current file stays
lightweight by keeping only recent entries, and if a past entry is ever
needed, it can always be re-read since the archive path is known.

### 5. Read-Frequency-Based File Splitting
If, out of several sections within one file, **a specific section is actually
referenced by only a few consumers (or just one)**, split that section into a
separate file — the "core" file that every session reads stays small, while
details needed only in specific contexts are opened only when that context
actually calls for them. This isn't compaction but **redesigning the access
path** — the information stays intact and only "is it loaded by default"
changes.

### 6. Search as a Safety Net for Compaction
Even when compaction/splitting removes some information from the default load
path, **as long as the record itself isn't deleted and stays searchable**, it
can be retrieved later at no cost (without an LLM call) once actually needed —
e.g., a deterministic script that parses a timestamped, append-only log and
scores entries on two signals — recency and relevance (string-match count) —
returning only the top K. The key is that this works with grep-level
computation alone, no embeddings or LLM calls needed — the "safety net" for
compaction costs almost nothing by itself.

### 7. A Fixed-Order Bootstrap at Session Start
Session compaction (conversation summarization) only works as long as the
session isn't interrupted — **when a brand-new session starts with "continue
where we left off," a compacted summary simply doesn't exist.** To bridge
this gap without relying on compaction, fix **a small set of state files that
are always read in the same order at session start** (e.g., current progress
→ preferences/context → quality/verification status → content index). Why the
order matters: information from earlier files becomes the context for
interpreting later files — changing the order can change the picture that
gets reconstructed even from reading the same files.

## What Survives Compaction vs. What's at Risk

| Type | Does it survive compaction (summarization)? |
|---|---|
| Explicit decisions, figures, dates | Generally preserved (summarization models tend to prioritize preserving structured facts) |
| The user's original request, verbatim | Generally preserved |
| Process-level nuance (e.g., detailed reasons why an approach was abandoned) | At risk — likely to be lost the more it's compressed; must be written explicitly into the file to survive |
| Raw output of tool calls (full text of past lookup results) | A safe target for reduction during compaction (basis #2 above) — cheap to re-look-up if lost |

## Honest Limitations

- The concrete thresholds (warning at 1.0x / urgent at 1.5x, etc.) and the
  file-splitting examples come from a single project's operational data, so
  they're not numbers that transplant as-is — each project needs to re-set its
  own baseline to fit its rewrite frequency and file characteristics.
- The table of what compaction actually preserves/loses reflects direct
  observation of one compaction engine (Claude Code itself); there's no
  external verification that it generalizes to every LLM compaction
  implementation.

## Related
- [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) —
  the memory-cap principle applied to a single rule list (a scaled-down
  version of this crystal).
- [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) —
  the design of "what to log so it's searchable" is a prerequisite for
  mechanism 6.
- [16-context-engineering-principles.md](16-context-engineering-principles.md) —
  five principles for structuring the context window within a session. This
  crystal differs in covering the axis that cuts across sessions.
