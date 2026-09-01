<!-- translated-from: ssot=sha256:7109e8bbecfc own=sha256:42e1a67798b6 -->
# Decision Rights Allocation — When Multiple People Share the Same AI Agent

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/20-decision-rights-raci.md)**

**Version**: 1.0.0
**Content hash**: sha256:ea1132cc690a (of the body below, excluding the stamp comment, this line, and the version line)

The crystals so far, especially
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md),
have covered "**when** the AI can act without a human check." This
crystal is a different axis — given that output, **who among multiple
people holds what authority**. It's unnecessary for a one-person
project, but becomes necessary the moment a team starts sharing the
same AI agent tooling.

## Basis (primary source verified)

🟢 The RACI matrix (Responsibility Assignment Matrix) — verified
directly against Wikipedia and the PMBOK Guide (5th edition, 2013).
Four roles:

- **R (Responsible)**: The person(s) who actually complete the work
  (can be more than one).
- **A (Accountable)**: The person **ultimately answerable for whether
  the deliverable was completed correctly** — approves and delegates
  the work. **Core rule**: "there must be exactly one Accountable per
  task/deliverable."
- **C (Consulted)**: Those whose opinion is sought (usually experts),
  two-way communication.
- **I (Informed)**: Those kept informed of progress, one-way
  communication (usually notified only upon completion).

A technique standardized and recognized by the Project Management
Institute (PMI), widely used to define roles and responsibilities in
cross-departmental collaboration.

## How to apply RACI when an AI agent produces the output

As AI agents increasingly take on the R (Responsible) role, how the
other three roles (A/C/I) are distributed **among people** actually
matters more, not less — the AI doing the work doesn't make the
question "who is accountable" disappear.

| Role | Who holds it once an AI agent is introduced |
|---|---|
| **R** | The AI agent (produces the actual deliverable) — though a person can also hold R concurrently (e.g., a human further refining the AI's output) |
| **A** | **Must always be a specific human** — an AI cannot be Accountable. "The AI made it that way" does not substitute for final accountability. Principle 0 of this framework's [05](05-autonomous-agent-operating-principles.md) ("irreversible actions still get asked about first") is, in effect, a concrete application of this rule that "A is always human" |
| **C** | Domain experts (for deliverables needing specialized advice — legal, medical, financial, etc.) — for areas touched by item 4 of [01-definition-of-done.md](01-definition-of-done.md) (professional-advice disclaimer), consider putting an actual expert in the C role |
| **I** | The remaining stakeholders affected by the deliverable |

## Why "A is always human" is a non-negotiable rule

Applying RACI's core rule ("exactly one Accountable") to AI agents, the
most common failure is **implicitly letting it default to "the AI is in
charge"** — without explicit assignment, when an incident occurs you
end up in a state where "no one was ultimately accountable."
[12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)'s
rule "don't close the loop with 'the AI made a mistake'" is exactly the
after-the-fact response to this problem — RACI prevents the problem
**structurally, in advance**.

## How this crystal differs from #05 and #10 — different axes

| | Question asked | When it applies |
|---|---|---|
| [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) | **When** can the AI act without a human check (time/gating axis) | Automatic-vs-manual judgment before execution |
| [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) G10 | When uncertain, how does the AI narrow its own service **scope** (the AI's own behavior axis) | The moment the AI generates a response |
| **This crystal (20)** | Given that output, **among people**, who is responsible/consulted/informed (organizational axis) | Project/team structure design time |

All three crystals cover the same broad topic — "authority and
responsibility around AI output" — but 05 and 10 address the
**AI-versus-human** boundary, while this crystal addresses the
**human-versus-human** boundary, so they don't actually overlap.

## Scaling from a one-person project to a team project

A one-person project (the default structure that
[09-project-structure-template.md](09-project-structure-template.md)
assumes) implicitly has that one person as both R and A on everything —
there's little need to spell out RACI. This crystal becomes necessary
the moment two or more people start sharing the same agent
configuration, governance documents, or shared context — especially
start by explicitly assigning A for shared resources multiple people
can touch simultaneously, such as
[02-directive-registry.md](02-directive-registry.md) (who has authority
to finalize a given directive) and changes to
[07-prompt-guardrails/](07-prompt-guardrails/) configuration (who has
authority to relax a guardrail rule).

## Related crystals
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  Principle 0, the basis for "A is always human."
- [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) —
  The after-the-fact response to an actual incident that occurred
  because A was unclear.
