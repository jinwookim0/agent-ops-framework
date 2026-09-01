# Case study: how 15 crystals shaped the Issue Triage Agent

This walks through **15 of agent-ops-framework's 37 crystals**, each
tied to a specific, checkable decision made while building the small demo
in this folder — not a general summary of what each crystal says, but
"here is the exact line this crystal changed, and what would have gone
wrong without it." Every file reference below can be opened directly.

If you're new to this framework: read this document as a worked answer to
"okay, but what does actually applying a crystal look like?"

## Why the raw output alone doesn't make the case

Running `triage.py` produces a routing decision per ticket — a category,
a confidence number, a gate. On its own, that output doesn't show what it
prevented; a reader has to already know what a *naive* version of the
same agent would have done to see the difference. `triage.py`'s
`naive_baseline()` makes that comparison explicit instead of leaving it
implicit: for each ticket, it states what a version of this agent without
this framework's governance layer (classify, then auto-act on everything,
no exceptions) would have done, and the script prints it right next to
the real decision. Run it — 3 of the 6 fixture tickets trigger a concrete,
named harm avoided (a security report auto-closed with no human ever
seeing it; a reporter's raw email/phone written straight into a log; an
ambiguous ticket silently guessed at instead of flagged) and the other 3
route identically either way, which is the expected shape: this
framework's mechanisms should be invisible on easy cases and only
active on the ones that would otherwise go wrong.

## Quick map

| # | Crystal | What it changed in this project |
|---|---|---|
| 09 | [Project structure template](../../ko/09-project-structure-template.md) | The whole folder layout (`tasks/` → skill → `shared-context/` → `governance/` → product) instead of one flat script. |
| 01 | [Definition of Done](../../ko/01-definition-of-done.md) | `governance/definition-of-done.md` — forced an explicit confidence-grade decision and an "AI comparative advantage" statement that isn't a generic claim. |
| 02 | [Directive registry](../../ko/02-directive-registry.md) | `shared-context/directive-registry.md` — the billing/security/PII rules are looked up, not hardcoded as unexplained `if` branches. |
| 03 | [Epistemic immunity catalog](../../ko/03-epistemic-immunity-catalog.md) | `epistemic-check.md` — named the false-precision risk in `confidence` before a reader could mistake it for a calibrated number. |
| 04 | [Eval engineering methodology](../../ko/04-eval-engineering-methodology.md) | `evals/eval-cases.md` — 4 cases with real rubrics, including one written specifically to catch a regression that already happened once. |
| 05 | [Autonomous agent operating principles](../../ko/05-autonomous-agent-operating-principles.md) | `decide_oversight_gate()` in `triage.py` — security is a hardcoded branch, not a threshold, because a threshold is something a later tuning pass could silently loosen. |
| 06 | [Self-improving heuristics loop](../../ko/06-self-improving-heuristics-loop.md) | `shared-context/heuristics.md` — two real bug-fix-shaped rules, plus one rejected candidate kept for reference. |
| 07 | [Prompt guardrails](../../ko/07-prompt-guardrails/README.md) | `.claude/hooks/guard-pii-leak.sh` — an adaptation (not a copy) of the same 3-layer defense mechanism, live-verified with 4 test cases. |
| 11 | [Observability & agent tracing](../../ko/11-observability-and-agent-tracing.md) | `observability/log-schema.md` + `sample-run.jsonl` — every "decision" is a structured field, not a sentence. |
| 13 | [Debt & quality bar](../../ko/13-debt-and-quality-bar.md) | `governance/quality-bar.md` — this skill is honestly marked 🟢 실행완료, not ✅ 공식통과, with the exact gap named. |
| 17 | [AI risk management index](../../ko/17-ai-risk-management-index.md) | This document itself, indirectly — see "Where this project sits in the NIST RMF index" below. |
| 20 | [Decision rights (RACI)](../../ko/20-decision-rights-raci.md) | `governance/raci.md` — Accountable is a named human role in every row, never "the agent." |
| 29 | [Agent cost & budget management](../../ko/29-agent-cost-and-budget-management.md) | `shared-context/cost-log.md` — an honest zero-cost report instead of invented token numbers for a rule-based classifier. |
| 31 | [Synthetic data / memory isolation](../../ko/31-synthetic-data-memory-isolation.md) | `triage.py`'s `--real` guard — refuses to run against `sample-tickets.json` in real mode, live-tested. |
| 37 | [Target-metric-gaming safeguards](../../ko/37-target-metric-gaming-safeguards.md) | `check_trip_wire()` in `triage.py` + `epistemic-check.md`'s metric-gaming section — named the obvious way to fake a good auto-resolution rate before building around it. |

## 09 — Project structure template

Before writing a line of triage logic, this project's shape follows the
crystal's 5-layer architecture literally: `tasks/triage-incoming-issue.md`
defines *what* the work is (with the exact YAML schema the crystal
specifies — status, cadence, success_criteria, oversight_gate,
confidence_gate, domain, irreversible_actions, all filled in, not left as
placeholders); `skills/triage-incoming-issue/` is the 1:1 execution layer
underneath it; `shared-context/` is what accumulates across runs
(directives, heuristics, cost); `governance/` is how "done" gets judged
(DoD, quality bar, RACI); this `CASE-STUDY.md` plus `README.md` are the
product layer aimed at a reader, not at the agent itself. Without this
structure, all of the above would plausibly have been one script with a
docstring — which is exactly the flat shape that makes "why was this
decision made" unanswerable six months later, the problem the crystal
exists to prevent.

## 01 — Definition of Done

`governance/definition-of-done.md` instantiates all 10 criteria against
this one skill. Two are worth calling out because they're easy to fake:
criterion 3 (confidence grade) forced an explicit answer — `flag`, not
`none` — because `classify()`'s confidence numbers are a keyword-coverage
proxy, not a measured probability (see crystal 03's section below for
where that distinction actually matters downstream). Criterion 8 (AI
comparative advantage) forced a *specific* bottleneck statement instead
of "AI is faster" — the actual bottleneck named is that a person
re-deriving "was this ever special-cased before" from memory degrades
with ticket volume in a way a registry lookup does not; see
`tasks/triage-incoming-issue.md`'s own section for the full statement.

## 02 — Directive registry

`shared-context/directive-registry.md` holds three standing rules
(billing → extra label, security → never auto-resolve, PII → always
redacted). The concrete effect: `apply_directives()` and
`decide_oversight_gate()` in `triage.py` both have comments pointing back
at specific registry row numbers, rather than being unexplained `if`
branches a future editor might "clean up" without realizing they encode a
standing decision. `evals/eval-cases.md` case 4 exists specifically to
keep row 1's "add, never override the category" rule honest — run
`triage.py` and check `TICKET-1046`'s log line: `category` is `billing`
(the classifier's own output) and `team:finance` is an additional label,
not a replacement category.

## 03 — Epistemic immunity catalog

Applied in two concrete spots. First, `classify()`'s own docstring in
`triage.py` names the confidence proxy as an instance of catalog item 2
(false precision) — a number with two decimal places that looks measured
but isn't. Second, `epistemic-check.md` walks through items 2, 6/8, and 9
against this project's actual design (not the catalog's own generic
examples), including the honest limit that this self-check was written by
the same process that wrote the code it's checking — a point the catalog
itself would flag if this file claimed otherwise.

## 04 — Eval engineering methodology

`evals/eval-cases.md` has 4 cases, each with a concrete rubric a reader
could check by hand against `sample-run.jsonl` without running any code.
Case 3 is the one worth noting specifically: it exists *because*
`shared-context/heuristics.md`'s second rule documents a real regression
(ambiguous tickets silently defaulting to `bug`) — the eval case is the
regression test for a bug that already happened once, which is exactly
the crystal's "golden dataset" pattern in miniature. The file also states
honestly what the suite does *not* cover (a 5th case for
`check_trip_wire()`), rather than padding the case count to look more
thorough than it is.

## 05 — Autonomous agent operating principles

The concrete decision: `decide_oversight_gate()` treats `security` as a
hardcoded `if category == "security": return "confirm"` branch, not a
confidence threshold like the other categories. This matters because a
threshold is exactly the kind of value a later tuning pass ("let's raise
the auto-resolve confidence bar to 0.85") could silently sweep security
tickets into — a hardcoded branch can't be loosened by accident the same
way. This is the crystal's 0th principle (irreversible actions are never
subject to autonomous tuning) expressed as a specific code shape, not just
a policy statement. Run `triage.py` and check `TICKET-1043`'s
`naive_baseline()` line for what this branch concretely prevents: a
security report auto-closed with no human ever seeing it.

## 06 — Self-improving heuristics loop

`shared-context/heuristics.md` holds two rules in the crystal's exact
format (imperative rule + concrete reason + what was re-checked
afterward), plus one rejected candidate kept under "Evaluator-gate
rejections" — a rule that looked plausible but, on the crystal's own "would
this have changed a prior decision for the better" test, would have made
things worse. Keeping the rejected candidate visible (not just the
adopted rules) is itself part of the pattern: it shows the gate actually
filtering something, not just rubber-stamping every proposal.

## 07 — Prompt guardrails

This is the one crystal in this list this project deliberately did **not**
copy verbatim — the original `guard-secrets.sh` blocks secrets (API keys,
credentials) in Artifact publishes and git commits, which this ticket
triage agent never touches. `.claude/hooks/guard-pii-leak.sh` reuses the
*mechanism* (JSON-parse the hook input, fail-closed on a parse error,
`exit 2` to actually block rather than just warn) against a different
target — a reporter's raw email/phone number in an outbound ticket
comment. It also reuses `triage.py`'s `redact_pii()` by import rather than
duplicating the regex, precisely because the original crystal's own
README warns that two independently-maintained copies of the same
detection list is how this kind of guardrail rots. All 4 behaviors were
live-tested, not just asserted: a clean comment passes (exit 0), a
comment with a raw email is blocked (exit 2, with a reason on stderr), an
unrelated tool call passes through untouched, and malformed hook input
fails closed rather than open.

## 11 — Observability & agent tracing

`observability/log-schema.md` documents 7 fields, each mapped to the
crystal's own OpenTelemetry attribute table where one exists (and marked
honestly where it doesn't — `intent` and `task_id` have no clean OTel
equivalent, same gap the crystal itself names). The concrete field worth
noting: `oversight_gate_reason` is separate from `oversight_gate` itself,
so `sample-run.jsonl` never just says "confirm" without also saying *why
this specific ticket* got that gate — which is what makes eval case 1
checkable by reading the log rather than re-running the code.

## 13 — Debt & quality bar

`governance/quality-bar.md` marks this skill 🟢 실행완료 (ran, produced
real output), explicitly *not* ✅ 공식통과 (formally passed) — because no
formal judge pipeline has been run against `evals/eval-cases.md`'s cases
yet, only direct code inspection (reasonable for a deterministic
rule-based classifier, but the file also says this classification would
have to change to reckless-deliberate debt if `classify()` is ever
swapped for a real LLM, since the classifier's behavior would no longer
be provable by reading the source alone).

## 17 — AI risk management index

This case study doesn't instantiate crystal 17 directly (it's an index
crystal, not a template one) — but every governance artifact this project
built maps into its Govern/Map/Measure/Manage structure: `governance/raci.md`
and `shared-context/directive-registry.md` are Govern; `evals/eval-cases.md`
and `epistemic-check.md`'s false-precision note are Map (naming what's
uncertain); `observability/log-schema.md` and `governance/quality-bar.md`
are Measure; `heuristics.md`'s correction loop and `.claude/hooks/guard-pii-leak.sh`
are Manage. Naming this mapping here is itself an application of crystal
17 — it exists precisely so a reader doesn't have to independently
re-derive which of a project's scattered documents cover which NIST
function.

## 20 — Decision rights (RACI)

`governance/raci.md`'s six rows never name the agent as Accountable —
every row's A column is a human role (on-call engineer, security lead,
project maintainer). The concrete link to code: the `security` category's
hardcoded `confirm` gate in `triage.py` (see crystal 05 above) and this
table's "security lead is Accountable for resolving a `confirm`-gated
ticket" row are the same commitment, stated once as code and once as an
organizational table — deliberately redundant, because a table alone
doesn't stop a lenient tuning pass, and code alone doesn't tell a new
team member who to actually page.

## 29 — Agent cost & budget management

`shared-context/cost-log.md` reports the honest, unglamorous truth: this
demo's classifier is rule-based, so its real per-ticket cost is zero
tokens (visible directly in `sample-run.jsonl`'s `"cost": {"tokens":
null, ...}` field) — the file resists the temptation to invent a
believable-looking token/cost number for a workload that doesn't actually
call a model, and instead explains concretely *where* cost would
reappear if `classify()` were swapped for a real LLM (boundary-case
self-consistency re-scoring costing 3x, specifically).

## 31 — Synthetic data / memory isolation

`triage.py`'s `main()` refuses to run in `--real` mode against
`sample-tickets.json`, and refuses to run in default (eval) mode against
anything not explicitly marked `_synthetic: true` — both directions of
the crystal's isolation rule, not just one. Live-tested: running
`./triage.py --real` with no other arguments (which would default to the
synthetic fixture file) produces an explicit error and exit code 1, not a
silent write into `real-run.jsonl`.

## 37 — Target-metric-gaming safeguards

The obvious metric to optimize for this project is "% of tickets
auto-resolved without a human" — and the obvious way to game it is to
guess confidently on ambiguous tickets instead of routing them to
`needs-human-review`. `epistemic-check.md`'s metric-gaming section names
this directly, and two concrete mechanisms push back on it: `evals/eval-cases.md`
case 3 acts as a counter-metric (a classifier that games auto-resolution
rate this way fails that case outright), and `check_trip_wire()` in
`triage.py` flags any category that hits a suspiciously perfect
100%-auto-resolved rate within a single run, rather than treating a high
auto-resolution number as unambiguously good news.

## What's honestly out of scope

This demo does not exercise every crystal it plausibly could — no chaos
engineering (19), no blameless postmortem (12, because nothing has failed
in production yet — there is no production), no model card (15, because
`classify()` isn't a trained model), no confidential-project separation
(23, because this whole project is public by design). Crystals were
chosen for depth over count: 15 crystals each doing real, checkable work
beats 37 crystals each represented by a token paragraph.
