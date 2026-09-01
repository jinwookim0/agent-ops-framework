# Decision rights — issue-triage-agent

> Instantiation of [20-decision-rights-raci.md](../../../ko/20-decision-rights-raci.md)
> for this project. Relevant the moment more than one person relies on
> this agent's output — a single maintainer running it solo doesn't need
> this table (per the crystal's own scoping note), but this demo assumes
> a small team, since that is the realistic point at which a project
> actually reaches for this crystal.

| Decision / output | R (does the work) | A (accountable — exactly one human) | C (consulted) | I (informed) |
|---|---|---|---|---|
| Classifying a ticket + assigning category/confidence | `triage-incoming-issue` skill (AI) | On-call engineer for that rotation | — | Reporter (via auto-applied label, once downstream tooling exists) |
| Applying the `notify`-gated routing decision (label, no reply posted) | Skill (AI) | On-call engineer | — | Team channel (batch summary) |
| Resolving an `ask`-gated ticket (`needs-human-review`) | On-call engineer | On-call engineer | Skill's own log line (as reference, not as a vote) | — |
| Resolving a `confirm`-gated ticket (`security` category) | Security lead | Security lead | On-call engineer, skill's log line | Whole team once resolved |
| Adding/editing a row in `../shared-context/directive-registry.md` | Whoever proposes the change | Project maintainer | On-call engineer (practical impact) | Whole team |
| Loosening a guardrail in `../.claude/hooks/guard-pii-leak.sh` | Whoever proposes the change | Security lead | Project maintainer | Whole team |

## Why "A" is never the AI, anywhere in this table

Every row's Accountable column names a person, never "the skill" or "the
agent" — this is not a stylistic choice, it is
[05](../../../ko/05-autonomous-agent-operating-principles.md)'s 0th
principle ("irreversible actions still get confirmed first") made
concrete at the level of who signs off, per crystal 20's core rule that
Accountable must be exactly one human. The `confirm` gate on `security`
tickets (directive-registry row 2) is this rule showing up as code, not
just as a table entry — the two are the same commitment stated twice, in
two different documents, deliberately.

## How this differs from the oversight-gate logic in `triage.py`

`decide_oversight_gate()` answers *when* the AI may act without a human in
the loop (the row/column axis is time — before or after action). This
table answers a different question: once someone is in the loop at all,
*which specific human* matters most — a question that only bites once
more than one person could plausibly be that human (a whole on-call
rotation, not "whoever is around"). The two are companion mechanisms, not
duplicates, exactly as crystal 20 describes its relationship to crystal 05.
