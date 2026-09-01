# Skill (module form): summarize-and-digest

> Project-dependency-stripped version of
> `../../skills/summarize-and-digest/SKILL.md`, per
> [08-module-format.md](../../../../ko/08-module-format.md). Read
> `MODULE.md` in this folder first.

## Procedure (core, no shared-context required)

1. Skip any paper record with a null/missing `abstract`.
2. Deduplicate near-identical resubmissions (`is_duplicate()`).
3. Detect (log-only) instruction-like text in the abstract
   (`detect_injection()`) — never let it affect relevance or gating.
4. Match against your project's own interest-keyword list
   (`matches_interest()`).
5. Summarize with an explicit truncation marker past a length budget
   (`summarize()`).
6. Audit that every number in the summary is grounded in the source
   (`audit_grounding()`).

## What you lose without `shared-context/`

- No cross-run heuristics accumulation — each run starts with the same
  fixed rules baked into `digest_core.py`'s functions; a bug discovered
  in production won't automatically get remembered anywhere unless you
  add your own equivalent of the original's `HeuristicsStore`.
- No research-interests history — every run filters fresh against
  whatever keyword list you pass in, with no accumulated topic memory
  across weeks.

Neither of these causes a crash — see `digest_core.py`'s own
`if __name__ == "__main__"` block, which runs the full core pipeline with
zero shared-context files present, verified live (see `../../CASE-STUDY.md`).

## Out of scope in this module form

The oversight-gate logic (`decide_oversight_gate()` in the original), the
weekly-loop orchestration, and all governance artifacts (SPEC.md,
PREMORTEM.md, red-team/chaos/postmortem docs) are specific to how this
particular project decided to use these functions — they aren't
"portable" in the crystal 08 sense (a different project would reasonably
make different oversight-gate calls), so they're intentionally not part
of this module. Bring the pure functions here; design your own governance
around them the way `../../CASE-STUDY.md` documents this project doing.
