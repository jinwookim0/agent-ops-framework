# Task: triage-incoming-issue

```yaml
---
name: triage-incoming-issue
status: active
cadence: on-demand
success_criteria: "every incoming ticket gets a category, an oversight gate, and a structured log line — no ticket is silently dropped"
tools: [Read, Bash]
executor: Skill
oversight_gate: notify
confidence_gate: flag
domain: cross
irreversible_actions: []
---
```

## Purpose

Classify each incoming support/bug/feature ticket and decide how it should
be routed, without a human having to read every single ticket before
anything happens to it.

## Input

A batch of tickets (see `../skills/triage-incoming-issue/sample-tickets.json`
for the synthetic fixtures this demo ships with): title, body, reporter,
timestamp.

## Output

One routing decision per ticket — category, confidence, extra labels, and
an oversight gate (`notify` / `ask` / `confirm`) — plus one structured log
line per ticket (see `../observability/log-schema.md`).

## Why this task fits AI management (crystal 01's 6-item checklist)

- [x] Structured output — a fixed `{category, confidence, labels,
      oversight_gate, reason}` shape, not free-form prose.
- [x] Repeatable with the same template — every ticket goes through the
      same 5-step procedure (see `SKILL.md`).
- [x] Cumulative context helps — `shared-context/heuristics.md` and
      `shared-context/directive-registry.md` both make later runs better
      without changing the code.
- [x] Structural/reusable pattern, not one-off — the same skill handles
      every ticket, forever, not just today's batch.
- [x] Verification is possible — `evals/eval-cases.md` defines what
      "correct" means well enough to check mechanically.
- [x] A human bottleneck actually exists — reading every incoming ticket
      before anything happens to it does not scale past a handful a day;
      see "AI comparative advantage" below for the specific bottleneck.

## Execution

Run `python3 ../skills/triage-incoming-issue/triage.py` from this folder's
parent, or see the top-level `README.md`'s "try it" section.

## AI comparative advantage (crystal 01 §8 — no generic claims)

The concrete bottleneck: a person triaging a queue of 50 tickets/day has to
re-derive, for each one, "is this the kind of thing that's ever been
special-cased before, and did I remember all of those special cases right
now" — the directive-registry and heuristics files exist precisely because
that recall step degrades with volume and fatigue in a way a file lookup
does not. The comparative advantage is not "AI classifies faster" in the
abstract — it's "a keyword/registry lookup does not forget rule 2 on a
Friday afternoon."

## Out of scope

This task does not decide *what happens after* routing (applying a label,
posting a reply, closing a ticket) — that is a separate, downstream task
with its own oversight-gate and irreversible-action declaration. This task
only classifies + routes + logs.

## Related crystals applied here

See `../CASE-STUDY.md` for the full mapping — this task alone exercises
[09](../../../ko/09-project-structure-template.md) (this file's own
schema), [01](../../../ko/01-definition-of-done.md) (the checklist above),
and [02](../../../ko/02-directive-registry.md)
(`../shared-context/directive-registry.md`, consulted at step 3 of
`SKILL.md`).
