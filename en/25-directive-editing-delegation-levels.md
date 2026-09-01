<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Authority to Edit the Directives Themselves — Explicitly Tiering How Much Is Delegated to AI

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/25-directive-editing-delegation-levels.md)**

**Version**: 1.0.0
**Content hash**: sha256:e9cb0d497aa4 (of the body below, excluding the stamp comment, this line, and the version line)

🟢 **Verification strength**: Delegation Levels — verified against the
original text of Jürgen Appelo, *Management 3.0* (2011)'s Delegation Poker
framework (7 levels: Tell→Sell→Consult→Agree→Advise→Inquire→Delegate).
One-way/two-way door decisions — the concept originates in Amazon's Bezos
1997 shareholder letter, redefined in the 2016 letter (the principle that
easily reversible and hard-to-reverse decisions should be handled at
different speeds).

## Why it's needed

[02-directive-registry.md](02-directive-registry.md) covered how to
cumulatively index directives/principles. But there are cases where the
registry **itself** may be edited by AI — when wording is unclear, when
scattered content needs consolidating, or when a one-off judgment call
needs to be generalized into a repeatable procedure. The problem is that
treating "may AI edit a directive" as a binary (yes/no) doesn't hold up in
practice — some edits are clearly safe, and others clearly require human
confirmation. This crystal defines the gradations in between.

## Mechanism — three delegation tiers

Before editing a directive, check the following three questions **in
order**:

1. **Does this edit change only "how" (mechanism), not "what" (intent)?**
   Clarifying wording, consolidating scattered content into one place, or
   generalizing a one-off judgment call into a repeatable procedure only
   changes "how" — the outcome the user wanted stays the same.
2. **Is it reversible, with no external impact?** (The one-way/two-way door
   test — if it can be fully reverted via version control and has zero
   impact outside this repo, it's a two-way door.)
3. **Does it leave absolute principles (security, privacy, reliability,
   etc.) untouched, is it not a directive that directly quotes a statement
   about the user themselves (preferences, facts, personal context), and
   does it not change the product's own purpose/scope (i.e., "what to
   build")?**

| Outcome | Delegation tier | Handling |
|---|---|---|
| All 3 are yes | **Tier 1** | Edit immediately, no separate notification needed |
| 1 and 2 are yes, 3 is partially triggered (minor expansion of a threshold, scope, etc.) | **Tier 2** | Edit, but notify explicitly |
| Even one is clearly no | **Tier 3** | Human confirmation required before editing |

## Why this order

The three questions are **progressively heavier filters** — question 1
(intent unchanged) is the cheapest and screens out the most cases,
question 2 (reversibility) confirms physical revertibility, and question
3 (absolute principles, personal statements, product scope) is the
heaviest, final line of defense. Checking the light filters first means
you reach the heavy judgment call (question 3) without wasted effort.

## Mapping to standard frameworks

This is a different axis of the same problem that
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
already covers — "when may AI act without human confirmation"
(oversight_gate). Crystal 05 covers delegation over **executing actions**;
this crystal covers delegation over **editing the directive documents
themselves**. The closest standard concept is Delegation Poker's 7 levels,
but this crystal reuses this framework's existing 3-tier gate vocabulary
(immediate/notify/confirm) instead of inventing a new one — the same
reuse principle as [08-module-format.md](08-module-format.md).

## What actual conflicts confirmed — numbering isn't an automatic tiebreaker

When a real conflict arises within the directive registry that touches an
absolute principle (question 3 above), the rule "the lower-numbered entry
in the table wins" is never applied mechanically — a human is always
consulted directly. Irreversible or high-impact decisions (e.g. actions
like rewriting history that are hard to undo) are never auto-processed
based on a delegation-tier determination alone. This means the table's
ranking functions more as "a gauge of how severe the conflict is" than as
an automatic ruling.

## Related
- [02-directive-registry.md](02-directive-registry.md) — the target this
  crystal covers editing authority for.
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  delegation over "executing actions" (this crystal covers delegation over
  "editing directives," a different axis of the same problem).
- [20-decision-rights-raci.md](20-decision-rights-raci.md) — the RACI
  principle that "A (accountable party) is always human" points in the
  same direction as this crystal's question 3 (absolute principles,
  personal statements, product scope).
