<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Blameless Postmortem Template — Based on Google SRE Practice

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/12-blameless-postmortem-template.md)**

**Version**: 1.0.0
**Content hash**: sha256:875e23b68c96 (of the body below, excluding the stamp comment, this line, and the version line)

It's inevitable that an AI agent will make mistakes (hallucination, a
wrong judgment call, a safeguard malfunctioning, etc.). The problem isn't
the mistake itself — it's **whether the same mistake repeats**. This
crystal adapts Google SRE's blameless postmortem culture for AI agent
projects.

## Basis (confirmed against primary source)

🟢 Confirmed against the original text of the Google SRE Book,
"Postmortem Culture: Learning from Failure"
(sre.google/sre-book/postmortem-culture) — quoting its three core
principles directly:

1. **Blamelessness**: "A blameless postmortem is written assuming that
   everyone involved in an incident had good intentions and did the right
   thing based on the information they had."
2. **System-focused improvement**: "You can't 'fix' people, but you can
   fix systems and processes to better support people."
3. **Learning, not punishment**: Writing a postmortem is "not a
   punishment — it's a learning opportunity for the entire organization."

## Why this matters especially for AI agent projects

Incidents in human-built systems tend to drift toward "who made the
mistake," but incidents involving an AI agent fall into that trap even
more easily — the sentence "the AI got it wrong" fixes nothing (it's just
as unproductive as blaming a person). You have to trace it down to
**which prompt/workflow/verification step let the mistake through** for
recurrence prevention to be possible.

## Standard template

```markdown
# Postmortem: <one-line summary>

## Summary
What happened, in 3–5 sentences.

## Impact
Who/what was affected, and to what extent (scope, duration, severity).

## Root cause (5 Whys or an equivalent depth)
Repeat "why?" at least 3–5 times, going down to the structural cause
rather than the surface-level one.
Example: "The judgment was wrong" → "Why?" → "It didn't know the date" →
"Why?" → "Today's date wasn't injected into the prompt" → "Why?" → "At
design time, no one anticipated the judge would need date-dependent
reasoning" (structural cause: it wasn't on the failure-mode list at the
design stage)

## Timeline
A time-stamped factual record from discovery of the incident through the
response taken after discovery (no speculation mixed in).

## What went well
What actually helped during the incident response (so it can be reused
next time).

## What didn't go well
Points that failed structurally (referring to process, design, and
verification steps — not naming a person or a specific AI run).

## Action items
| Action | Owner (person or automation) | Completion criterion | Status |
|---|---|---|---|
| ... | ... | ... | not started/in progress/done |

Each action item must actually contribute to "preventing recurrence" — a
"we'll be more careful" style resolution of intent is not accepted as an
action item (only structural, code, or process changes count).
```

## AI-agent-specific rules

1. **Don't stop at "the AI made a mistake"** — always trace down to "which
   stage (prompt design, verification pipeline, safeguard scope) let this
   mistake through."
2. **Record reproducibility** — note whether the same mistake reproduces
   with the same input (a deterministic failure) or occurs only
   probabilistically (see the related determinism principle) — a mistake
   that doesn't reproduce needs a different kind of defense (sampled
   verification, after-the-fact audits).
3. **The "reproduced twice" rule**: When an incident with the same root
   cause actually happens a second time, that's a signal it's a pattern,
   not a coincidence — at this point, escalate from a stopgap fix to a
   structural correction (adding a guardrail, changing the process).
   (Same principle as "how the catalog grows" in
   [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
   — only things that actually recur get folded into the structure.)
4. **Connect it to the classification scheme** — a recurring pattern
   discovered in a postmortem gets registered in the debt classification
   in [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md), so you
   can track "how many incidents of this kind are currently unresolved."

## Suggested folder structure

```
postmortems/
  quality/     Content quality incidents (hallucination, wrong judgment, etc.)
  safety/      Safeguard bypasses/malfunctions
  cost/        Unexpected cost spikes (FinOps)
  README.md    "How many postmortems exist so far" + a recent-summary index
```
The reason to split folders by incident type: the nature of the
recurrence-prevention action differs by type (quality incidents call for
prompt/verification improvements, safety incidents for stronger
guardrails, cost incidents for budget/alert tuning) — mixing them into
one list makes prioritization hard. It's fine to create these folders
empty in advance — that way, the moment the first incident actually
happens, there's already a place to record it, instead of it getting
deferred to "we'll make one when it happens."
