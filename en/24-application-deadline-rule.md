<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Application Deadline Rule — Research Should Always Come With an Application Deadline

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/24-application-deadline-rule.md)**

**Version**: 1.0.0
**Content hash**: sha256:7c35f9365c3b (of the body below, excluding the stamp comment, this line, and the version line)

🟢 **Verification strength**: extracted directly from this repo's own
operational practice; the rule's effectiveness has itself been empirically
confirmed across 3 rounds of reapplication.

## Why it's needed

If you keep accumulating knowledge/research (papers, research summaries,
investigation reports) while vaguely postponing "we'll apply it someday,"
the knowledge keeps piling up while actual application barely grows — the
same structure as buying ingredients for the fridge without ever cooking,
until they eventually expire and get thrown out. The core observation is
that without a deadline, this gap doesn't shrink on its own.

## Mechanism

Every "application idea" produced by a piece of research/investigation
output is explicitly assigned one of the following three states:

| State | Meaning |
|---|---|
| `pending` | Not yet executed — the default |
| `done` | Actually reflected in code/docs/product |
| `archived` | Confirmed as deferred — must always come with a one-line reason |

**Core rule**: if an application idea is still `pending` after a certain
number of batches have passed (this repo uses "roughly 10 new outputs" —
the exact number matters less than "while this many new outputs have
accumulated"), it must be either (1) actually executed, or (2) explicitly
converted to `archived`. It is never left indefinitely in a "someday"
state.

**Rescans cover everything**: this rule isn't applied only when new output
is added — the entire accumulated list is periodically rescanned to check
for anything that's missed its deadline. Attending only to new items while
neglecting older ones is the most common failure pattern.

## Measured effect

Having actually applied this rule 3 times, a significant portion of the
items that had been sitting in `pending` state each round were either (a)
executed as small, reusable code/utilities, or (b) honestly converted to
`archived` with a concrete reason (e.g. "a real A/B comparison is needed
and that's not yet feasible at this scale," "this was a one-off judgment
call that couldn't be turned into a reusable function," "the production
wiring isn't in place yet"). **Archiving itself counts as success** — the
point of this rule is to explicitly record "we didn't execute this"
instead of hiding it.

## Failures this rule prevents

Pending items that accumulate without a deadline are dangerous in two
ways:
1. **Invisible debt**: even if the execution rate is low, just glancing at
   the list creates the illusion that "something is being done."
2. **The more dangerous case — items that never get tracked at all**: an
   idea that's merely mentioned in passing, without even being marked
   `pending`, doesn't fall under this rule's scope at all. "A pending item
   that missed its deadline" is less dangerous than "something that was
   never tracked in the first place" — which is why the rescan process
   must also include "find items with no marker at all."

## Minimal implementation

```
"Application" section of each research output:
- [ ] Idea A → pending (proposed: YYYY-MM-DD)
- [x] Idea B → done (`path/to/implementation`)
- [~] Idea C → archived (reason: couldn't be turned into a reusable function at this scale)

Regular rescan: grep across the "application" sections of all output to
surface items where "proposed date is N batches old but still pending,"
and flag them for processing.
```

## Related
- [01-definition-of-done.md](01-definition-of-done.md) — the criteria for
  "done" (this crystal complements it by capping not whether something is
  done, but how long it's allowed to take to get there).
- [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) — the debt
  classification system (this rule can be seen as putting a deadline on
  one specific category of debt: "unverified application ideas").
