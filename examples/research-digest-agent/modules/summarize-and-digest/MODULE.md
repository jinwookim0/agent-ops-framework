---
name: summarize-and-digest
version: 1.0.0
source: agent-ops-framework/examples/research-digest-agent, skills/summarize-and-digest/, exported 2026-09-01
verified: the original was verified by direct execution against 10 synthetic weekly batches (see ../../skills/summarize-and-digest/ and ../../CASE-STUDY.md) — not by a formal eval suite, and not re-verified in this exported form (see "Verification status" below)
dependencies: none for the core filtering/summarization/audit functions; degrades gracefully without shared-context files (see below)
---

## What this is

The paper-filtering, summarization, and grounding-audit core of the
research-digest-agent demo, packaged per
[08-module-format.md](../../../../ko/08-module-format.md) so it can be
dropped into a project that has no `shared-context/` or `observability/`
folders at all — useful the moment someone wants just the filtering
logic without adopting this whole example's governance scaffolding.

## Installation

Copy `SKILL.md` (this folder's version, not the original's) and
`digest_core.py` into the target project. That's it — no shared-context
setup required for the core functions to work.

## Dependencies (honestly)

- **None** for `matches_interest()`, `detect_injection()`, `summarize()`,
  `audit_grounding()`, `is_duplicate()` — these are pure functions, no
  file I/O, no project-specific paths. They were already written this
  way in the original (see `../../skills/summarize-and-digest/digest.py`)
  — not refactored for this export, just re-packaged.
- **Optional, with graceful degradation**: the original's `HeuristicsStore`
  and `ContextStore` classes read/write `shared-context/heuristics.md` and
  `shared-context/research-interests.md`. This module ships without
  them — a target project that doesn't have a `shared-context/` folder
  loses cross-run self-improvement and interest-accumulation (every run
  starts stateless, filtering only by the fixed keyword list passed in),
  but does **not** crash: `digest_core.py` never imports or references
  either class or file path — the degradation is designed in, not caught
  as an exception.

## Verification status

The original was run directly against 10 synthetic weekly batches with
its own live-verified test cases (red-team injection resistance, chaos
fault injection, grounding-audit catch, determinism check — see
`../../CASE-STUDY.md`). **This exported module has not been independently
re-verified** — per crystal 08's own rule, "verified" describes the
origin's history, not a re-run of this specific exported copy. Re-run the
live checks in `../../red-team/CHECKLIST.md` and
`../../chaos/EXPERIMENT-LOG.md` against your own target environment before
relying on this module in anything real.
