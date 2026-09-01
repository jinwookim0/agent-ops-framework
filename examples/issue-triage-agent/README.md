# Example: Issue Triage Agent

A small, runnable demo project built to show a first-time reader of
**agent-ops-framework** what its crystals actually look like once applied
to a real (if intentionally small) agent — not just described in the
abstract.

**What it does**: reads a batch of incoming support tickets (bug reports,
feature requests, questions, security reports, billing disputes),
classifies each one, decides whether the routing decision can be applied
automatically or needs a human to confirm it first, redacts any contact
info found in the ticket body before it's logged, and writes one
structured log line per ticket.

**What it's for**: not a product to adopt — a worked example to read. The
real deliverable is [`CASE-STUDY.md`](CASE-STUDY.md), which walks through
15 of this framework's 37 crystals and points at the exact file/line in
this small project where each one is actually doing something, not just
mentioned in passing.

## Try it

```bash
cd examples/issue-triage-agent
python3 skills/triage-incoming-issue/triage.py
```

No API key, no dependencies beyond the Python standard library — the
classifier is intentionally rule-based (see
[`skills/triage-incoming-issue/SKILL.md`](skills/triage-incoming-issue/SKILL.md)'s
last section for why, and for exactly where a real LLM call would plug
in). Output goes to stdout and to
[`observability/sample-run.jsonl`](observability/sample-run.jsonl).

**What the output actually means**: a table shows every ticket's routing
decision, with a `Harm avoided?` column pointing at which ones needed one
of this framework's governance mechanisms — the counterfactual (what a
naive, auto-act-on-everything version would have done instead) is what's
worth reading, not the classification labels by themselves:

```
Ticket       Category            Conf  Gate     Labels                 Harm avoided?
-----------  ------------------  ----  -------  ---------------------  -------------
TICKET-1042  bug                 0.85  notify   bug                    —
TICKET-1043  security            0.90  confirm  security               ⚠️ yes
TICKET-1044  feature-request     0.80  notify   feature-request        —
TICKET-1045  question            0.75  notify   question               —
TICKET-1046  billing             0.80  notify   billing, team:finance  ⚠️ yes
TICKET-1047  needs-human-review  0.20  ask      needs-human-review     ⚠️ yes

=== what this run actually demonstrates ===
3 concrete harm(s) avoided out of 6 ticket(s) — the other tickets routed the same way a
naive version would have, which is the point: this framework's mechanisms are supposed to
be invisible on the easy cases and only change behavior on the ones that would otherwise
go wrong.
  - [TICKET-1043] a naive always-auto-act agent would have closed this security report on
    its own (confidence 0.90 clears any reasonable auto-approve bar) — no human would have
    seen it unless they went looking
  - [TICKET-1046] a naive agent logs the raw ticket body — this reporter's email/phone
    would sit in plaintext in a log file
```

Three tickets out of six actually needed one of these mechanisms; the
other three routed identically either way — that's not a weak result, it's
the expected shape: governance should be invisible until the one ticket
that needed it shows up. See [`CASE-STUDY.md`](CASE-STUDY.md) for which
crystal is responsible for each of the three interventions above.

## Where to start reading

1. [`CASE-STUDY.md`](CASE-STUDY.md) — the crystal-by-crystal map. Start here.
2. [`skills/triage-incoming-issue/SKILL.md`](skills/triage-incoming-issue/SKILL.md) +
   [`triage.py`](skills/triage-incoming-issue/triage.py) — the actual
   logic, read side by side.
3. Everything else in this folder is one crystal's template, filled in
   for real: [`tasks/`](tasks/), [`shared-context/`](shared-context/),
   [`governance/`](governance/), [`evals/`](evals/),
   [`observability/`](observability/), [`.claude/`](.claude/), and
   [`epistemic-check.md`](epistemic-check.md).

## Honest scope

This is a demo, not a reference implementation to copy wholesale — the
classifier is deliberately simple (keyword rules, not a trained model),
the "ticket tracker" it routes tickets to/from doesn't exist (no real API
calls happen), and several files describe illustrative fixture content
rather than a real project's actual operating history (each says so where
that applies). What's real: the code runs, the guardrail hook actually
blocks what it claims to block (verified live — see
[`CASE-STUDY.md`](CASE-STUDY.md)'s crystal-07 section), and the crystal
mapping is not aspirational — every claim in `CASE-STUDY.md` points at a
specific file and can be checked directly.
