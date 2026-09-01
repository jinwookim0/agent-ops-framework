# Skill: triage-incoming-issue

Reads one incoming ticket (bug report, feature request, question, security
report, or billing dispute) and produces a routing decision: category,
priority signal (via confidence), extra labels, and an oversight gate that
says whether the decision can be applied automatically or needs a human to
confirm it first.

This document describes the procedure; `triage.py` in this same folder is
the actual runnable implementation — read them side by side.

## Procedure

1. **Load the ticket.** Title + body + reporter metadata. No inference
   about the ticket happens before this step.
2. **Classify.** Run the ticket text against the category keyword rules
   (`classify()` in `triage.py`) to get a `(category, confidence)` pair.
   Confidence here is a crude keyword-coverage proxy, not a calibrated
   probability — see the docstring on `classify()` and
   `../../epistemic-check.md`.
3. **Check the directive registry.** Before finalizing routing, check
   `../../shared-context/directive-registry.md` for any standing rule that
   changes the outcome regardless of what the classifier said
   (`apply_directives()`). A directive can only ever *add* to the
   classifier's output (e.g. an extra label) in this implementation — it
   never silently overrides the category itself, so a reader can always
   tell which layer produced which part of the decision.
4. **Decide the oversight gate.** `decide_oversight_gate()` — security is a
   hardcoded always-`confirm` branch, not a confidence threshold; very low
   confidence is always `ask`; everything else is `notify` (see
   `../../governance/raci.md` for who the "human" in `confirm`/`ask`
   actually is).
5. **Redact before logging.** `redact_pii()` strips anything that matches
   an email or phone pattern from the body *before* it goes anywhere —
   the log, and (in a real deployment) any public-facing label or comment.
   This runs unconditionally, not just for tickets already flagged
   billing/PII-suspicious.
6. **Log.** One structured line per ticket via `log_ticket()`, matching
   `../../observability/log-schema.md`.
7. **Check trip wires.** After the whole batch, `check_trip_wire()` flags
   any category that auto-resolved 100% of its tickets with zero
   escalations — a suspiciously perfect result is itself a signal worth
   a look (see `../../epistemic-check.md`'s metric-gaming section).
8. **Report the counterfactual.** `naive_baseline()` doesn't change any
   routing decision — it's a separate function that, per ticket, states
   what a version of this agent *without* steps 3-5 above would have done
   instead, and prints that alongside the real decision. This exists
   because the routing output alone (a category, a confidence number, a
   gate) doesn't self-evidently show what it prevented — a reader has to
   see the alternative to see the value.

## Metadata (per crystal 09 §3.1)

```yaml
---
name: triage-incoming-issue
status: active
cadence: on-demand
success_criteria: "every incoming ticket gets a category, an oversight gate, and a structured log line — no ticket is silently dropped"
tools: [Read, Bash]
executor: Skill
oversight_gate: notify        # this skill's own execution — see governance/raci.md for the *output's* per-category gate, which is a separate, finer-grained decision made inside the skill
confidence_gate: flag         # classifier confidence is a proxy, not calibrated — see epistemic-check.md
domain: cross
irreversible_actions: []      # this skill only classifies and logs; a real deployment's "apply the label" / "post the comment" step is a separate, irreversible action layered on top — see governance/raci.md
---
```

## Out of scope

- Actually calling a ticket-tracker API to apply labels or post comments —
  that would be a second skill downstream of this one's decision, with its
  own `irreversible_actions` entry and its own guardrail hook (see
  `../../.claude/hooks/guard-pii-leak.sh` for the shape that hook would
  take).
- Training or fine-tuning a real classifier — see the docstring on
  `classify()` for where a real model call plugs in.

## Swapping in a real classifier

Replace the body of `classify()` with a call to an LLM (or a trained
model), keeping the same `(category, confidence)` return shape. Nothing
else in this skill needs to change — `apply_directives()`,
`decide_oversight_gate()`, `redact_pii()`, `log_ticket()`, and
`check_trip_wire()` all operate on the output of `classify()`, not its
internals. If the real classifier is an LLM, apply
[04-eval-engineering-methodology.md](../../../../ko/04-eval-engineering-methodology.md)'s
full pipeline (LLM-as-judge scoring, boundary-zone self-consistency) to
grade its output instead of the trivial keyword-coverage proxy used here.
