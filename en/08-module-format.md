<!-- translated-from: ssot=sha256:0248f3a35b7b own=sha256:ea050161bb00 -->
# Module Format — Lifting a Single Feature Straight Into Another Project

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/08-module-format.md)**

**Version**: 1.0.1
**Content hash**: sha256:88f731042a3f (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 A small-scale reproduction of the manifest
concept used by package managers like npm, and several real modules in
the original project were ported and verified using this format.

An individual feature inside a project (a skill or agent) is usually
**tightly coupled** to that project — it references shared context files,
governance documents, and sometimes implicitly assumes other features
exist. So if you copy just the executable file into another project, its
references break (the file is missing) or it quietly degrades (it runs
without context). This document is the **packaging convention** that
solves that problem.

## Why keep it in a location separate from the original

The original is **the real thing running inside the project** (it actually
runs by referencing shared context files, etc.). A module is a
**deployable copy of that original with project dependencies removed or
explicitly declared** — it is managed separately from the original (if you
fix the original, the module must be synced manually; if there's no
automatic sync mechanism, say so honestly).

## Module structure

```
modules/<skill-name>/
├── MODULE.md      # Manifest — format below
├── SKILL.md        # Version with this project's dependencies removed/replaced
├── README.md        # Human-readable install/usage instructions
└── (optional) bundled reference material  # Only the excerpts from documents
                                             # the original referenced that are actually needed
```

## MODULE.md format

```markdown
---
name: <feature name>
version: 1.0.0
source: <origin project>, <origin path>, <export date>
verified: <whether/when the original was formally verified by an eval, and the result>
dependencies: none | <list>
---

## What this is
(One-line description + why it's useful)

## Installation
Copy this folder's executable file (and any bundled reference material)
to the corresponding location in the target project. That's it — no
additional setup.

## Dependencies (stated honestly)
- None: works completely standalone
- Some: if the target project lacks <file/structure>, <specifically what degrades>
  (e.g., "history-based personalization is lost, and it advises from scratch
  every time" — the principle is that it degrades performance without
  crashing; see "Graceful degradation" below)

## Verification status
State plainly the official verification history the original went
through in its project — this doesn't imply the module, once split off,
has been re-verified, so don't overstate it as "this version is also
100% guaranteed."
```

## Principles

1. **Graceful degradation**: If files specific to the original project are
   missing from the target project, the feature must not die or throw an
   error — it should use them when present, and fall back naturally to
   something like "proceeding without history this time" when absent, by
   adjusting the wording accordingly.
2. **Separate bundling from referencing**: From the project documents the
   original referenced, excerpt only the parts actually needed for the
   feature's core behavior and include them in the module folder. Don't
   copy an entire project-wide governance document (e.g., the full set of
   safety guardrails) wholesale — instead, spell out just the needed
   principles directly inside the executable file, or include them as a
   short excerpt file.
3. **A version is a snapshot**: A module is a snapshot at the time it was
   exported — if the original improves later, the module does not
   automatically follow along. Re-export it by request if needed
   (automatic syncing is out of scope for this convention).
4. **Be honest about verification labels**: The "verified" field in
   MODULE.md is a record of what the **original** passed, not a
   re-verification of the split-off module — don't blur this distinction.

## The same principle applies to this crystal collection itself

`agent-ops-framework/` itself is a larger-scale version of this
convention — instead of a single feature, it's the operating approach of
an entire project that has been split off. Principles 3 (a version is a
snapshot) and 4 (be honest about verification labels) apply to this
entire folder as well — each file summarizes the verification history the
original document went through in real practice, while stating explicitly
that this crystallized version itself has not been independently
re-verified.
