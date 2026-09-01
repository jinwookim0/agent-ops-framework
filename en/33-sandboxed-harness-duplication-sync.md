<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Duplicate Harnesses in Sandboxed Executors — When Imports Aren't Available, Duplicate Honestly and Diff Mechanically

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/33-sandboxed-harness-duplication-sync.md)**

**Version**: 1.0.0
**Content hash**: sha256:637a547a219f (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 Directly confirmed that 5+ independent call
sites in the original project actually follow this pattern, and that a diff
script enforcing it has been deployed and reused in production — this is
a direct check against the project's own operating history, not against
an external standard (BLUEPRINT.md section 1, grounding path (a)). Whether
this pattern holds the same way in other sandboxed execution environments
or other teams hasn't been separately confirmed.

## The Problem

Some agent execution environments (workflow scripts, plugin sandboxes, etc.)
don't allow local modules to be `import`ed — every run must be self-contained
in a single independent file. Yet it's common for several execution files to need
the exact same verified logic (e.g., a scoring function, a judgment schema).
Brushing it off with "just copy-paste it" inevitably produces drift — the
original gets fixed and a copy gets forgotten. Relying on a human to remember
"we'll fix them all together later" is a failure pattern this framework has
repeatedly run into (the same lineage as [05-autonomous-
agent-operating-principles.md](05-autonomous-agent-operating-principles.md)'s
"documentation alone doesn't prevent recurrence").

## The Solution — Honest Duplication + Mechanical Diffing

1. **Keep exactly one canonical copy**: write the logic once, in a separate,
   unit-testable library file, and verify it there.
2. **Copy it by hand into each call site**: since imports aren't available,
   paste the canonical content directly into each execution file — this isn't
   a stopgap, it's **the only honest option that actually works within this
   environment's constraint**. Don't pretend it's linked by reference.
3. **Build a script that mechanically diffs each copy against the
   canonical**: after normalizing whitespace, diff each copy against the
   canonical — instead of relying on a human to remember to check, the script
   structurally catches drift at commit time (or at a periodic check). A
   comment saying "copied from X" doesn't substitute for actual verification.

With these three steps in place, the contradiction of "the logic is verified
and tested in only one place, but execution physically exists in multiple
places due to environment constraints" is maintained **without drift**.

## Bonus Benefit — Parameterized Harnesses

When the same kind of run recurs (e.g., an experiment that judges A vs. B),
split the canonical copy itself into "a fixed skeleton + a swappable
payload" — adding a new kind of comparison means swapping in a new payload
(what to compare, the judgment schema) instead of building new skeleton code.
Since the skeleton is verified in only one place (the canonical), adding a new
comparison type doesn't require re-verifying everything from scratch.

## Conditions Under Which This Pattern Applies

- The execution environment forbids or restricts importing local modules
  (conversely, if imports are freely available, this pattern is unnecessary —
  just build a shared module; in that case follow general code-reuse
  principles instead of this crystal).
- The same logic is actually reused in 2 or more places (with only 1 place,
  there's no drift risk to diff against in the first place).

## Related
- [08-module-format.md](08-module-format.md) — the packaging convention for
  moving a single feature to a different project (a different scope from this
  crystal — 08 is about cross-project portability, this one is about
  duplication that arises within the same project due to execution
  constraints).
- [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) —
  the adjacent requirement that results shouldn't diverge when the same logic
  runs in multiple places (this crystal's diff script guarantees one of that
  requirement's preconditions: "the code itself is identical").
