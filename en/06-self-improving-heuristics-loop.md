<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Self-Improving Tool-Use Rules — A Miniature Toolformer Loop (Domain-Neutral Template)

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/06-self-improving-heuristics-loop.md)**

**Version**: 1.0.2
**Content hash**: sha256:92be3f059a52 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 The core idea of the Toolformer paper
(Schick et al. 2023, [arXiv:2302.04761](https://arxiv.org/abs/2302.04761))
was checked against the source. 🟡 The Evaluator gate applies the
self-grading-suppression concept from the Reflexion paper — only the
concept's name and intent were confirmed, not a sentence-by-sentence
check against the Reflexion text itself; the gate's concrete
implementation is this crystal's own design.

This is a way of reproducing the core idea of the Toolformer paper (Schick
et al. 2023, [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)) —
"keep only the attempts that helped, discard the rest" —
without actually retraining the model, as a **miniature policy where the
document updates itself.** Before starting new work, first skim this
document; after finishing, add exactly one line for any lesson that actually
changed a subsequent decision — don't log every attempt (otherwise this
document itself becomes noise).

## Why this counts as "learning"

A typical project document is written deliberately by a human. This one is
different — entries are created **only from actual failures or
discoveries encountered.** Each rule is not "this seems like it would be
good" but a record of "this actually wasn't done this way, a problem
actually occurred, this was the fix, and it actually resolved it once
applied."

## Rule-writing format

```markdown
- **[A concrete rule that changes the next decision — imperative form]** Reason:
  [what actually went wrong, how it was discovered, and the result actually
  confirmed after the fix]
```

- Write rules in the **imperative** ("do X," "don't do X") — they need to be
  searchable and directly applicable later.
- The reason section holds **an actual incident, not a generalization** —
  not "it's better to do it this way," but "this wasn't done this way, and
  this actually happened as a result."
- Where possible, include **the result reconfirmed after the fix** — don't
  stop at "fixed it"; confirm all the way to "ran it again after the fix and
  it was actually resolved" — this is the core of the loop (the same spirit
  as ReAct's observe-then-verify-next-action cycle).

## Update rules

- **Only add a lesson that actually changed a subsequent decision** (no
  guesses or generalizations).
- **When an old rule no longer applies, don't delete it — mark it "Updated:
  no longer applies (date, reason)"** so why it changed stays traceable.

## The evaluator gate — a structure that suppresses self-grading

Before adding a new rule, a **separate step — not the same "self" that ran
the experiment/task — reopens only the raw data (logs, actual execution
results)** and answers the following question with Yes/No plus a cited
source:

> "If this rule had been known *before* the experiment started, would it
> actually have led to different behavior?"

If No, don't add it — this is a gate that structurally suppresses
self-grading, i.e. the AI judging for itself that "this was an important
lesson" (an application of the self-evaluation mechanism from the Reflexion
paper).

## Memory cap — an active-rule ceiling of 10–12

Cap the number of active rules at 10–12 (an application of the Reflexion
paper). Once that's exceeded:

1. **Merge two rules that share the same root cause into one.**
2. **Move the least-recently-referenced rule out to a separate archive
   document**, noting in one line why it was retired.

**Backtrack condition** (an application of the Tree of Thoughts paper): if a
lesson substantively identical to one that was moved to the archive gets
re-proposed within a short window and passes the evaluator gate as a Yes
again, that's a signal it was "retired too early" — instead of creating a
new entry, mark it "Restored (date, reason)" in the archive and move it back
into the main body. Track the count of these "misjudged then restored" cases
itself, and use it as evidence for whether the cap should be raised later.

**Code vs. prose asymmetric design** (an observation from the Voyager
paper): executable-code-form skills (reusable library functions, etc.) are
deliberately left uncapped — since executability and automated testing are
already a verification gate, unlimited accumulation is safe (the same design
as Voyager's "library of executable code skills"). Prose lessons like this
document, by contrast, have no verification gate (if the writing sounds
plausible, it just piles up), so a cap is needed — this is deliberately
using different memory policies for different content types within the same
project, not a claim that one approach is always correct.

## Example categories of rules that actually accumulate (generalized)

Categories worth referencing when porting this in — the actual rules must
come from each project's own real incidents, but these are the types that
come up often:

- **Hidden gotchas in tool/API usage**: behavior not documented anywhere
  (e.g. a particular call style reuses a snapshot taken at session
  registration time, so edits don't get reflected) — discoverable only
  through hands-on measurement.
- **The trust boundary of automated aggregation logic**: when an
  automatically-aggregated result looks extreme or off, make it a habit to
  directly cross-check the raw data rather than trusting the aggregation
  code itself. Apply the same skepticism to the judge and to your own
  aggregation code alike. (The same spirit as item 8 in
  [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  confirm a tool call's result as a log, not as a claim.)
- **The break-even point for reusable harnesses**: only invest up front in
  building something as a reusable harness when you're confident it will be
  used at least twice — turning even one-off work into reusable form every
  time is over-engineering.
- **Hidden crash points from null/error propagation**: when using a
  structure that absorbs a failed task in parallel execution so the whole
  run doesn't halt (e.g. something in the `Promise.allSettled` family), if
  the absorbed result later gets used downstream under the assumption "no
  failure occurred," it crashes outside the point where the failure was
  absorbed — "this function call itself is safe" doesn't guarantee how its
  result gets used later.
- **Transient infrastructure instability**: a given error can shift which
  step it fails at on each retry, rather than always failing at the same
  step — don't give up after a single retry failure, but on repeated
  failures, spacing retries out over time can be effective.

## Related crystals

- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  the higher-level autonomous-execution principles this loop belongs to
  (mapping the concepts of the three papers — CoT, ReAct, and Toolformer —
  to, respectively, recording predictions up front, taking the next action
  based on observation, and this document's self-learning).
