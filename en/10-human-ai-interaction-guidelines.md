<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# The 18 Human-AI Interaction Principles — A Checklist Applying the Microsoft Research Standard

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/10-human-ai-interaction-guidelines.md)**

**Version**: 1.0.1
**Content hash**: sha256:0624cce98737 (of the body below, excluding the stamp comment, this line, and the version line)

This crystal draws **not from the practical history of any single
project, but from an external global standard as its source** — every
crystal in the 10–20 range follows the same approach: it takes a verified
standard that isn't tied to any one project, confirmed directly against
its primary source.

## Basis (confirmed against primary source)

🟢 Amershi et al. 2019, *Guidelines for Human-AI Interaction* (Microsoft
Research, CHI 2019, [official paper page](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)) — confirmed the 18 guidelines directly against the
original text on the [HAX Design Library](https://www.microsoft.com/en-us/haxtoolkit/).
It's designed to be applicable broadly across AI product families
(chatbots, recommendation systems, LLM-based assistants, etc.), and has
been a widely cited standard checklist in industry since CHI 2019.

## The 18 guidelines (G1–G18)

| # | Guideline | What it means for an AI agent project |
|---|---|---|
| G1 | Make clear what the system can do | Document the agent's actual tool/permission scope so users can know it (e.g., "this task cannot actually send anything, it only produces a draft") |
| G2 | Make clear how well the system can do what it can do | Confidence-grade labeling (things like `confidence_gate`) — mark how reliable each output is |
| G3 | Time services based on context | Hold back automatic notifications/interruptions when the user wouldn't want them (e.g., during focused work) |
| G4 | Show contextually relevant information | Don't pad the output with irrelevant information — don't inflate perceived credibility with irrelevant data |
| G5 | Match relevant social norms | Match tone and format to the conventions of that domain (e.g., professional-advice disclaimers) |
| G6 | Mitigate social biases | Check that outputs don't embed unfounded assumptions about particular groups |
| G7 | Support efficient invocation | Make frequently used tasks runnable with minimal input |
| G8 | Support efficient dismissal | Make it easy to cancel an in-progress task — especially before an irreversible action |
| G9 | Support efficient correction | Provide a structure that lets the user easily fix the AI's result (a partial fix, not a full re-run) |
| G10 | Scope services when in doubt | When a case is ambiguous, don't guess broadly — answer only the part you're confident of, or explicitly ask back |
| G11 | Make clear why the system did what it did | Keep the reasoning (which tool was used and why, what materials were consulted) alongside the result |
| G12 | Remember recent interactions | Don't act inconsistently with prior instructions within the same session/conversation |
| G13 | Learn from user behavior | Provide a structure where the user's preferences and patterns accumulate with repetition |
| G14 | Update and adapt cautiously | Don't hastily generalize learned preferences into broad application (don't rewrite an entire policy from one or two signals) |
| G15 | Encourage granular feedback | Allow asking specifically what was wrong and why, rather than just "thumbs up/down" |
| G16 | Convey the consequences of user actions | Before executing an irreversible action, clearly communicate what its consequences will be |
| G17 | Provide global controls | Let the user adjust system-wide settings (turning off auto-execution, tuning notification frequency, etc.) |
| G18 | Notify users about changes | When system behavior changes (a new rule added, automation scope expanded), inform the user of that fact |

## Mapping to other crystals in this framework

| G# | Related crystal |
|---|---|
| G2 | Criterion 3 (confidence grade) in [01-definition-of-done.md](01-definition-of-done.md) |
| G10, G16 | The unknown-unknowns gating in [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) |
| G11 | Item 8 (preventing unverified tool-execution claims) in [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) |
| G14 | The Evaluator gate (suppressing self-scoring) in [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) |
| G17 | The same spirit as [07-prompt-guardrails/](07-prompt-guardrails/) exposing safeguards as project settings |

This mapping table is itself an interesting finding — principles that the
original project developed independently in practice (at a time when it
wasn't aware of the external standard) overlap substantially with parts
of an already-existing global HCI standard. This isn't "the repo copied
this standard" — it's "the project independently arrived at similar
conclusions by repeatedly experiencing actual user complaints and
incidents," which can itself be read as evidence reinforcing the
standard's validity (though, to be clear, this is an observation made
while compiling this mapping table, not a statistically verified claim —
don't over-interpret it).

## How to adopt this in a project

Don't try to apply all 18 at once. **Using it as a self-check checklist
after executing a task is recommended**: each time you produce an output
or feature, first narrow down "which of these 18 are relevant to this
output" (not all apply — e.g., a purely informational-lookup output only
weakly involves the dismissal/correction concepts in G7–G9), then check
only the relevant items in detail. Forcing yourself to fill in all 18
every single time turns it into rote box-checking.
