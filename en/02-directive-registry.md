<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Directive Registry — How to Accumulate and Index User Directives (Domain-Neutral Template)

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/02-directive-registry.md)**

**Version**: 1.0.1
**Content hash**: sha256:c045d19ca1f8 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 A variant of the ADR (Architecture Decision
Record) practice, refined through 100+ real directives/decisions
accumulated in the original project.

Working with an AI agent across many sessions creates a recurring problem:
the AI forgets, or re-asks about, directives the user gave or principles
that were already settled in the past ("wasn't this already decided?"). The
Directive Registry is **a table that accumulates every user directive and
settled principle, one line at a time, along with its priority and its
re-application trigger.**

## Why this is needed

- As sessions get longer and directives pile up, it's not viable to expect a
  human to remember and check every time whether "does this judgment now
  conflict with a principle the user settled earlier?"
- Indexing the directives themselves lets the AI search first, before making
  a new judgment call — "was there already a rule for this?"

## What this document is not

- It is **not a log of individual judgment-call instances** (what was
  decided this particular time and how) — that's the role of a separate
  document (a decision log). This table records **the directives that serve
  as the basis for judgment calls**, not the calls themselves.
- It is **not a chronological execution log**. This table is not
  time-ordered — it's a "snapshot of current priorities as of now." That's
  different from a log that just keeps appending.

## Table format

| # | Column | Description |
|---|---|---|
| 1 | **Number** | Registration order. A lower number does not automatically win (see "Handling conflicts" below) |
| 2 | **Directive/principle (bold) + what was actually done** | Not just what was settled, but which actual files/structures were changed while implementing it — this prevents "words with no follow-through" |
| 3 | **Re-application trigger** | When this directive should be pulled back out and applied ("the next time a similar situation arises") |
| 4 | **Original user directive text** | Quoted verbatim, not paraphrased — so it can later be checked for whether "the AI distorted the original intent when transcribing it" |
| 5 | **Confidence level** | How firm this directive is (e.g. 🟢 explicitly confirmed / 🟡 applied by inference, needs reconfirmation) |

## Handling conflicts — the number is not an automatic tiebreaker

When multiple principles apply at once to a situation, don't mechanically
apply "the lower number wins." The table's ranking functions more as **a
gauge of how seriously a conflict should be handled once found** — a
conflict touching the highest-tier principles (absolute ones like security
or privacy) is escalated directly to the user for confirmation. Irreversible
or high-impact decisions (e.g. an action as hard to undo as rewriting
history) are also not resolved by ranking alone — they're explicitly
confirmed with the user.

## When to add a new row

- When the user proposes a new principle while seeking confirmation-style
  agreement ("do you agree?")
- When the AI itself judges and creates a new operating rule (in this case,
  record the AI's own reasoning in place of a quoted original, since there
  is none)
- When an exception or correction is discovered while applying an existing
  principle (add a new row, or update the existing row — don't delete it,
  keep it as a "correction history")

## Preventing bloat

This table keeps growing — once it passes a few dozen rows: (1) keep it in a
searchable form (a single file, structured to be easy to grep), (2) don't
delete directives that are genuinely stale and no longer apply — mark them
"Retired (date, reason)" so why they changed stays traceable, and (3) keep a
separate lightweight index for the human-facing priority map (which document
to check when) so this table itself stays focused on its role as the raw
source the AI consults via search.

## Minimal implementation

```markdown
| # | Directive/Principle | Re-application trigger | User's original text | Confidence |
|---|---|---|---|---|
| 1 | **[Title] — [what was actually done]** | [when to pull this back out] | "[verbatim quote]" | 🟢 |
```

When adopting this into a new project, just carry over this table format and
start filling row 1 with that project's actual directives — there's no need
to retroactively backfill past history.
