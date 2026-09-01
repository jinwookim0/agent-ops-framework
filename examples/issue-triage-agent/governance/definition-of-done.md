# Definition of Done — triage-incoming-issue

> Instantiation of [01-definition-of-done.md](../../../ko/01-definition-of-done.md)'s
> 10-item checklist for this specific skill.

| # | Criterion | Status for triage-incoming-issue |
|---|---|---|
| 1 | Metadata completeness | ✅ `tasks/triage-incoming-issue.md` frontmatter has name/status/cadence/success_criteria/tools/executor/oversight_gate/confidence_gate/domain/irreversible_actions all filled in. |
| 2 | Executable procedure, not prose | ✅ `SKILL.md`'s 7 numbered steps map 1:1 to named functions in `triage.py` — not a paragraph description. |
| 3 | Uncertainty-handling principle + confidence grade | ✅ `confidence_gate: flag` on the task, with a one-line reason ("classifier confidence is a proxy, not calibrated") — see `../epistemic-check.md` for the fuller false-precision discussion this grade points to. |
| 4 | Eval cases exist | ✅ `../evals/eval-cases.md` has 4 cases with concrete rubrics (≥ the 2-case minimum). |
| 5 | Oversight-gate reasoning stated | ✅ The task-level gate is `notify` (this skill only classifies + logs, no irreversible action) — the *finer-grained per-category* gate (`security` always `confirm`) is documented separately in `../shared-context/directive-registry.md` row 2 and enforced in `decide_oversight_gate()`. |
| 6 | Preference/context accumulation point (if applicable) | ✅ `../shared-context/heuristics.md` (corrections learned from running the skill) + `../shared-context/directive-registry.md` (standing rules given up front) — two separate accumulation points, not conflated. |
| 7 | Reflected in the root index | ✅ Listed in `../README.md` and in `../CASE-STUDY.md`'s crystal-mapping table. |

Criteria 1-7 are all filled in — this task counts as "done," not "draft,"
per the crystal's "3 or more unfilled = draft" rule.

## 8th — AI comparative advantage

See `../tasks/triage-incoming-issue.md`'s "AI comparative advantage"
section — the concrete bottleneck (rule recall degrading with ticket
volume) is stated there rather than repeated here, per the crystal's
"state it once, in the task file" pattern.

## 9th — actionability

This file itself passes its own self-check questions: strip the specific
names (`triage.py`, `TICKET-1047`, `decide_oversight_gate()`) and what's
left is generic boilerplate — so the criterion is met, not just asserted.
A reader repeating this audit on a different skill knows exactly where to
look (the skill's own `SKILL.md` + the task file's frontmatter), not just
that "a definition of done exists somewhere."

## 10th — content-source motivational bias

Not applicable in the way the crystal frames it (no external news/promo
content is cited anywhere in this skill's design) — noted here explicitly
rather than silently skipped, per the crystal's own guidance that a
criterion which doesn't apply should say so rather than leave a gap that
looks like an oversight.
