# Worked examples

Three small demo agents built to show what actually applying this
framework's crystals looks like — structurally, in real code and, for
the third, a real agent — not just described in prose.

| Example | Shape | Crystals covered | Start here |
|---|---|---|---|
| [`issue-triage-agent/`](issue-triage-agent/) | Reactive, per-item classifier (deterministic, no API key needed) | 15 (governance/quality/safety fundamentals) | [`CASE-STUDY.md`](issue-triage-agent/CASE-STUDY.md) |
| [`research-digest-agent/`](research-digest-agent/) | Autonomous, recurring, self-improving loop (deterministic, no API key needed) | 12 more (2 deepened, 10 new — planning, chaos/red-team, context lifecycle, module packaging) | [`CASE-STUDY.md`](research-digest-agent/CASE-STUDY.md) |
| [`escalation-reviewer-agent/`](escalation-reviewer-agent/) | A **real** LLM agent, governed (not a script — see its own README for what "try it" means here) | Same governance principles applied to genuine, non-deterministic AI judgment — including a real, unscripted security finding | [`CASE-STUDY.md`](escalation-reviewer-agent/CASE-STUDY.md) |

The first two cover 25 of this framework's 37 crystals with real,
deterministic code you can run with zero setup. The third is different
in kind, not just content: it's the one place in this repo a real model
was actually invoked (isolated, scoped to its own task only) to produce
genuinely uncertain, non-scripted output — governed by, and tested
against, this same framework's principles. Each `CASE-STUDY.md` names
its own honest remainder rather than claiming full coverage.

Read in this order if you're new here: `issue-triage-agent` (the
simplest shape) → `research-digest-agent` (autonomous/recurring,
still deterministic) → `escalation-reviewer-agent` (what changes once
the judgment step is a real agent instead of code).
