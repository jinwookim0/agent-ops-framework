# Case study: how 15 crystals shaped the Issue Triage Agent

This walks through 15 of agent-ops-framework's 37 crystals, each tied to
a specific, checkable decision made while building the small demo in
this folder. Every file reference below can be opened directly, and
every claim was checked against the actual code and its output rather
than asserted — that's stated once, here, rather than re-argued in every
section below.

If you're new to this framework, read this as an answer to "okay, but
what does actually applying a crystal look like?"

## Why the raw output alone doesn't make the case

Running `triage.py` produces a routing decision per ticket: a category,
a confidence number, a gate. That alone doesn't show what it prevented —
you'd need to already know what a naive version of the same agent would
have done to see the difference. `triage.py`'s `naive_baseline()` makes
that comparison explicit: for each ticket, it states what a version of
this agent without the governance layer (classify, then auto-act on
everything, no exceptions) would have done, and prints it next to the
real decision. Run it, and three of the six fixture tickets trigger a
named harm avoided: a security report auto-closed with no human ever
seeing it, a reporter's raw email and phone number written straight into
a log, an ambiguous ticket guessed at instead of flagged. The other three
route identically either way. That's the expected shape — this
framework's mechanisms should be invisible on easy cases and only kick in
on the ones that would otherwise go wrong.

## Quick map

| # | Crystal | What it changed in this project |
|---|---|---|
| 09 | [Project structure template](../../ko/09-project-structure-template.md) | The whole folder layout (`tasks/` → skill → `shared-context/` → `governance/` → product) instead of one flat script. |
| 01 | [Definition of Done](../../ko/01-definition-of-done.md) | `governance/definition-of-done.md` forces an explicit confidence-grade decision and an "AI comparative advantage" statement that isn't a generic claim. |
| 02 | [Directive registry](../../ko/02-directive-registry.md) | `shared-context/directive-registry.md`: the billing/security/PII rules are looked up, not hardcoded as unexplained `if` branches. |
| 03 | [Epistemic immunity catalog](../../ko/03-epistemic-immunity-catalog.md) | `epistemic-check.md` names the false-precision risk in `confidence` before a reader mistakes it for a calibrated number. |
| 04 | [Eval engineering methodology](../../ko/04-eval-engineering-methodology.md) | `evals/eval-cases.md`: 4 cases with real rubrics, one of them written specifically to catch a regression that already happened once. |
| 05 | [Autonomous agent operating principles](../../ko/05-autonomous-agent-operating-principles.md) | `decide_oversight_gate()` in `triage.py` treats security as a hardcoded branch, not a threshold, because a threshold is something a later tuning pass could silently loosen. |
| 06 | [Self-improving heuristics loop](../../ko/06-self-improving-heuristics-loop.md) | `shared-context/heuristics.md`: two real bug-fix-shaped rules, plus one rejected candidate kept for reference. |
| 07 | [Prompt guardrails](../../ko/07-prompt-guardrails/README.md) | `.claude/hooks/guard-pii-leak.sh`: an adaptation, not a copy, of the same 3-layer defense mechanism, verified with 4 live test cases. |
| 11 | [Observability & agent tracing](../../ko/11-observability-and-agent-tracing.md) | `observability/log-schema.md` + `sample-run.jsonl`: every decision is a structured field, not a sentence. |
| 13 | [Debt & quality bar](../../ko/13-debt-and-quality-bar.md) | `governance/quality-bar.md` marks this skill 🟢 실행완료, not ✅ 공식통과, and names the exact gap. |
| 17 | [AI risk management index](../../ko/17-ai-risk-management-index.md) | This document itself, indirectly — see "Where this project sits in the NIST RMF index" below. |
| 20 | [Decision rights (RACI)](../../ko/20-decision-rights-raci.md) | `governance/raci.md`: Accountable is a named human role in every row, never "the agent." |
| 29 | [Agent cost & budget management](../../ko/29-agent-cost-and-budget-management.md) | `shared-context/cost-log.md` reports a zero-cost run honestly rather than inventing plausible token numbers. |
| 31 | [Synthetic data / memory isolation](../../ko/31-synthetic-data-memory-isolation.md) | `triage.py`'s `--real` guard refuses to run against `sample-tickets.json`, checked live. |
| 37 | [Target-metric-gaming safeguards](../../ko/37-target-metric-gaming-safeguards.md) | `check_trip_wire()` + `epistemic-check.md`'s metric-gaming section name the obvious way to fake a good auto-resolution rate before building around it. |

## 09 — Project structure template

Before writing a line of triage logic, this project follows the
crystal's 5-layer architecture: `tasks/triage-incoming-issue.md` defines
what the work is, with the exact YAML schema the crystal specifies
(status, cadence, success_criteria, oversight_gate, confidence_gate,
domain, irreversible_actions — all filled in, none left as placeholders).
`skills/triage-incoming-issue/` is the execution layer underneath it.
`shared-context/` accumulates across runs (directives, heuristics, cost).
`governance/` is how "done" gets judged (DoD, quality bar, RACI). This
`CASE-STUDY.md` and `README.md` are the product layer, aimed at a reader
rather than the agent. Without this structure, the whole thing would
plausibly have been one script with a docstring — the flat shape that
makes "why was this decision made" unanswerable six months later, which
is exactly the problem the crystal exists to prevent.

## 01 — Definition of Done

`governance/definition-of-done.md` instantiates all 10 criteria against
this one skill. Two are worth calling out because they're easy to fake.
Criterion 3 (confidence grade) forced an explicit answer — `flag`, not
`none` — because `classify()`'s confidence numbers are a keyword-coverage
proxy, not a measured probability (see crystal 03 below for where that
distinction matters downstream). Criterion 8 (AI comparative advantage)
forced a specific bottleneck statement instead of "AI is faster": the
bottleneck named is that a person re-deriving "was this ever
special-cased before" from memory degrades with ticket volume in a way a
registry lookup doesn't. Full statement in
`tasks/triage-incoming-issue.md`.

## 02 — Directive registry

`shared-context/directive-registry.md` holds three standing rules:
billing gets an extra label, security never auto-resolves, PII always
gets redacted. In the code, `apply_directives()` and
`decide_oversight_gate()` both comment back to specific registry row
numbers, rather than being unexplained `if` branches a future editor
might "clean up" without realizing they encode a standing decision.
`evals/eval-cases.md` case 4 keeps row 1's "add, never override the
category" rule honest: run `triage.py` and check `TICKET-1046`'s log
line — `category` is `billing` (the classifier's own output), and
`team:finance` sits alongside it as an additional label, not a
replacement category.

## 03 — Epistemic immunity catalog

Applied in two spots. `classify()`'s own docstring names the confidence
proxy as an instance of catalog item 2, false precision — a number with
two decimal places that looks measured but isn't. `epistemic-check.md`
walks through items 2, 6/8, and 9 against this project's actual design
rather than the catalog's own generic examples, and names its own limit
plainly: it was written by the same process that wrote the code it
checks, which the catalog itself would flag as a conflict of interest if
this file pretended otherwise.

## 04 — Eval engineering methodology

`evals/eval-cases.md` has 4 cases, each with a rubric a reader can check
by hand against `sample-run.jsonl` without running any code. Case 3
exists because `shared-context/heuristics.md`'s second rule documents a
real regression — ambiguous tickets silently defaulting to `bug` — so the
eval case is a regression test for a bug that already happened once, the
crystal's "golden dataset" pattern in miniature. The file also says
plainly what the suite doesn't cover (a fifth case for
`check_trip_wire()`) instead of padding the count to look more thorough.

## 05 — Autonomous agent operating principles

`decide_oversight_gate()` treats `security` as a hardcoded
`if category == "security": return "confirm"` branch, not a confidence
threshold like the other categories. A threshold is exactly the kind of
value a later tuning pass — "let's raise the auto-resolve bar to 0.85" —
could silently sweep security tickets into; a hardcoded branch can't be
loosened by accident the same way. This is the crystal's 0th principle
(irreversible actions never get subject to autonomous tuning), expressed
as a code shape rather than a policy statement someone has to remember
to follow. Check `TICKET-1043`'s `naive_baseline()` line in `triage.py`
for what this branch concretely prevents: a security report auto-closed
with no human ever seeing it.

## 06 — Self-improving heuristics loop

`shared-context/heuristics.md` holds two rules in the crystal's format —
imperative rule, concrete reason, what got re-checked afterward — plus
one rejected candidate under "Evaluator-gate rejections": a rule that
looked plausible but failed the crystal's own "would this have changed a
prior decision for the better" test. Keeping the rejected candidate
visible, not just the adopted rules, is part of the point: it shows the
gate actually filtering something rather than rubber-stamping every
proposal.

## 07 — Prompt guardrails

This is the one crystal here the project deliberately didn't copy
verbatim. The original `guard-secrets.sh` blocks secrets — API keys,
credentials — in Artifact publishes and git commits, which this ticket
triage agent never touches. `.claude/hooks/guard-pii-leak.sh` reuses the
mechanism instead: JSON-parse the hook input, fail closed on a parse
error, exit 2 to actually block rather than just warn — pointed at a
different target, a reporter's raw email or phone number in an outbound
ticket comment. It also imports `triage.py`'s `redact_pii()` rather than
duplicating the regex, because the original crystal's own README warns
that two independently maintained copies of the same detection list is
exactly how a guardrail rots. All four behaviors were tested live: a
clean comment passes, a comment with a raw email is blocked with a
reason on stderr, an unrelated tool call passes through untouched, and
malformed hook input fails closed.

## 11 — Observability & agent tracing

`observability/log-schema.md` documents 7 fields, mapped to the
crystal's own OpenTelemetry attribute table where one exists — and
marked honestly where it doesn't; `intent` and `task_id` have no clean
OTel equivalent, the same gap the crystal itself names. The field worth
noting is `oversight_gate_reason`, kept separate from `oversight_gate`
itself, so `sample-run.jsonl` never just says "confirm" without also
saying why this specific ticket got that gate. That's what makes eval
case 1 checkable by reading the log instead of re-running the code.

## 13 — Debt & quality bar

`governance/quality-bar.md` marks this skill 🟢 실행완료 (ran, produced
real output) — deliberately not ✅ 공식통과 (formally passed), because no
formal judge pipeline has run against `evals/eval-cases.md`'s cases yet,
only direct code inspection. That's a reasonable state for a
deterministic rule-based classifier, but the file also notes that this
classification would have to move to reckless-deliberate debt if
`classify()` were ever swapped for a real LLM, since the classifier's
behavior would no longer be provable by reading the source alone.

## 17 — AI risk management index

This case study doesn't instantiate crystal 17 directly — it's an index
crystal, not a template one — but every governance artifact here maps
into its Govern/Map/Measure/Manage structure. `governance/raci.md` and
`shared-context/directive-registry.md` are Govern. `evals/eval-cases.md`
and `epistemic-check.md`'s false-precision note are Map, naming what's
uncertain. `observability/log-schema.md` and `governance/quality-bar.md`
are Measure. `heuristics.md`'s correction loop and
`.claude/hooks/guard-pii-leak.sh` are Manage. Naming that mapping here is
itself an application of crystal 17: it means a reader doesn't have to
re-derive on their own which of a project's scattered documents cover
which NIST function.

## 20 — Decision rights (RACI)

`governance/raci.md`'s six rows never name the agent as Accountable —
every row's A column is a human role, on-call engineer or security lead
or project maintainer. The `security` category's hardcoded `confirm`
gate in `triage.py` (crystal 05, above) and this table's "security lead
is Accountable for a `confirm`-gated ticket" row are the same commitment
stated twice — once in code, once as an organizational table. That
redundancy is deliberate: a table alone can't stop a lenient tuning pass
from creeping in, and code alone doesn't tell a new team member who to
actually page.

## 29 — Agent cost & budget management

`shared-context/cost-log.md` reports the unglamorous truth: this demo's
classifier is rule-based, so its real per-ticket cost is zero tokens,
visible directly in `sample-run.jsonl`'s `"cost": {"tokens": null, ...}`
field. Rather than invent a believable token count for a workload that
doesn't call a model, the file explains where cost would actually
reappear if `classify()` were swapped for a real LLM — boundary-case
self-consistency re-scoring, specifically, at 3x the cost of a plain
call.

## 31 — Synthetic data / memory isolation

`triage.py`'s `main()` refuses to run in `--real` mode against
`sample-tickets.json`, and refuses default (eval) mode against anything
not explicitly marked `_synthetic: true` — both directions of the
crystal's isolation rule. Tested live: running `./triage.py --real` with
no other arguments, which would default to the synthetic fixture file,
produces an explicit error and exit code 1 instead of a silent write
into `real-run.jsonl`.

## 37 — Target-metric-gaming safeguards

The obvious metric to optimize here is "% of tickets auto-resolved
without a human," and the obvious way to game it is to guess confidently
on ambiguous tickets instead of routing them to `needs-human-review`.
`epistemic-check.md`'s metric-gaming section names this directly, and two
mechanisms push back on it: `evals/eval-cases.md` case 3 acts as a
counter-metric (a classifier gaming the auto-resolution rate this way
fails that case outright), and `check_trip_wire()` flags any category
that hits a suspiciously perfect 100%-auto-resolved rate in a single run
rather than treating a high number as automatically good news.

## What's honestly out of scope

This demo doesn't exercise every crystal it plausibly could. There's no
chaos engineering (19) or blameless postmortem (12) here — nothing has
failed, since there is no production and no fault was ever injected into
this agent; see
[`examples/research-digest-agent/`](../research-digest-agent/) for both,
demonstrated live on a different agent. There's no model card (15) since
`classify()` isn't a trained model, and no confidential-project
separation (23) since this whole project is public by design. Crystals
were chosen for depth over count — 15 crystals doing real, checkable work
beats 37 represented by a token paragraph each.
