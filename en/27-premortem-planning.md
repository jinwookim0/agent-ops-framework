<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Premortem — Assuming Failure Before Execution, as a Technique

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/27-premortem-planning.md)**

**Version**: 1.0.1
**Content hash**: sha256:7bd58fbaadbd (of the body below, excluding the stamp comment, this line, and the version line)

If [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)
is a procedure for learning from something that **has already happened**,
this crystal is its mirror image — applied to **a plan not yet executed**,
pulling the same learning effect forward, before the incident happens.

## Grounding (verified against the primary source)

🟢 Verified against the original text of Gary Klein, ["Performing a Project
Premortem,"](https://hbr.org/2007/09/performing-a-project-premortem)
*Harvard Business Review* (2007). Quoting the core mechanism
directly from the source:

> "Unlike a typical critiquing session, in which project team members are
> asked what might go wrong, the premortem operates on the assumption
> that the 'patient' has died, and so asks what did go wrong."

The reason this technique works lies in the **tense** of the question.
"What might go wrong?" (future/hypothetical) sounds like worrying about
something that hasn't happened yet, which makes people socially cautious.
"What did go wrong?" (past/already-a-fact) presupposes the patient is
already dead, so voicing a concern isn't pessimism — it's simply an
autopsy. Klein states the motivation directly, in the original text:

> "Projects fail at a spectacular rate. One reason is that too many
> people are reluctant to speak up about their reservations during the
> all-important planning phase."

The premortem isn't a tool for surfacing new information — it's closer to
a device that creates **social permission to voice concerns people already
had**.

🟡 A lineage Klein himself acknowledged — this formalizes an older
psychological concept, "prospective hindsight" (Mitchell, Russo &
Pennington, 1989, *Journal of Behavioral Decision Making*, "Back to the
Future: Temporal Perspective in the Explanation of Events"), into a
practical procedure. Its existence and the paper's title were confirmed
only via secondary sources (encyclopedia-type citations); the original
paper's specific effect sizes (quantitative figures) were not verified —
kept honestly at 🟡 to avoid overstating.

## When to use it — proportional to risk, not mandatory for everything

The definition of a premortem itself ("a plan not yet executed") narrows
its applicable scope. In any project, the points where a "new plan is
being adopted" are limited — roughly at approving an architecture/tooling
decision document, or scaffolding a new task/feature. Even then, **running
it every time on a plan that's easily reversible and low-risk turns it
into a checkbox ritual** — this is exactly the same logic as the "make
verification strength proportional to risk" principle in
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md).

**Design rule**: don't invent a new threshold. If the project already has
a risk-tier classification (e.g. Crystal 04's risk-tiered verification, or
an oversight gate that determines whether an action needs human
confirmation), reuse that signal directly as the premortem trigger —
apply it only to plans already classified as high-risk/irreversible, and
skip low-risk/reversible plans.

## Minimum bar

Draw out at least **3** concrete scenarios. One could be a fluke, two
could be coincidence, but a pattern starts to show at three. A vague
one-liner like "we might run out of budget" doesn't count — it has to go
down to the concrete mechanism ("at which stage, why, and which conditions
have to coincide for this to fail").

## Standard procedure

```markdown
## Premortem

"Assume this plan has failed by [point in time] — why did it fail?"

1. [Scenario 1 — concrete mechanism]
   Mitigation: [a structural response; "we'll be careful"-type mental
   resolutions don't count]
2. [Scenario 2]
   Mitigation: ...
3. [Scenario 3]
   Mitigation: ...
```

Each scenario must come with a mitigation attached — just listing risks
and stopping there only creates anxiety and fixes nothing (the same
principle as [Crystal 12](12-blameless-postmortem-template.md)'s "a
postmortem with no action items is incomplete").

## Why this matters especially for AI agent projects

AI agents are prone to optimism bias even more easily than humans are —
the moment a computation finishes (e.g. the moment comparing several
alternatives lands on a "best" one) is precisely the moment confidence
peaks, and if that moment moves straight into execution without a
premortem, it hardens unchallenged. **Automatically attaching a premortem
to the moment a computation finishes** (e.g. requiring a premortem
immediately on the top-ranked option once several alternatives have been
compared) structurally blocks this trap.

## Applying this principle to itself

The decision to adopt this crystal is itself a not-yet-executed plan, so
it's subject to its own premortem: (1) Risk of ritualization — filling in
3 perfunctory lines every time and moving on. Mitigation: grade the
premortem's "concreteness" (a vague scenario vs. one that pins down an
actual mechanism) as part of the verification step itself. (2) Risk that
the risk classification itself is wrong, silently causing the trigger to
never fire. Mitigation: periodically spot-check the risk classifier itself
(see Crystal 04's "the verification tool's own scope management"). (3)
Risk that spreading this across multiple procedure documents means it
gets forgotten and skipped. Mitigation: bake it in as a checklist item
directly in the procedure template itself, rather than relying on memory.

## Related
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) — the mirror image (something already executed)
- [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) — the risk-proportional judgment logic this reuses
- [21-spec-first-implementation.md](21-spec-first-implementation.md) — pairs with writing a spec first: the spec covers "what to build," the premortem covers "why it might fail"
