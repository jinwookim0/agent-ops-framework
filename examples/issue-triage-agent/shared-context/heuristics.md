# Self-improving heuristics — issue-triage-agent

> Instantiation of [06-self-improving-heuristics-loop.md](../../../ko/06-self-improving-heuristics-loop.md)'s
> format. These entries simulate lessons that would accumulate after
> running this skill against real ticket batches for a while — they are
> illustrative fixture content for this demo, written in the same
> mandatory/rule + reason format the crystal specifies, not a real
> operating history.

## Active rules

- **Do not auto-escalate a ticket to a higher-severity category just
  because the title contains an urgency word ("urgent", "critical",
  "asap") if the body has no concrete repro steps.** Reason: an earlier
  version of the keyword rules bumped anything with "urgent" in the title
  straight to `bug`/high-confidence, which mis-routed three plain
  questions that happened to say "urgent" in the subject line and paged
  an on-call engineer for nothing. Re-checked after removing urgency
  words from the confidence calculation entirely (confidence is now
  driven only by category-keyword coverage + repro-signal presence, see
  `../skills/triage-incoming-issue/triage.py`'s `REPRO_SIGNALS`) — the
  same three ticket types now correctly land as `question`, not `bug`.

- **A one-line ticket with no error text, no feature name, and no
  question mark should go to `needs-human-review` (`ask`), not default to
  `bug` at low confidence.** Reason: "bug" being the most common category
  meant a genuinely empty-signal ticket (see `TICKET-1047` in
  `sample-tickets.json`) used to get silently classified as a low-priority
  bug and then never looked at again — nobody was ever told it needed a
  human, because a `bug` label with a plausible-looking (if low)
  confidence doesn't visually stand out as "unresolved." Fixed by making
  `needs-human-review` its own explicit fallback category tied to
  `confidence_gate: ask`, rather than letting the most common category
  absorb the ambiguous cases by default.

## Evaluator-gate rejections (kept for reference — not promoted to a rule)

- *Proposed*: "If a ticket mentions a competitor's product name, always
  route to `feature-request` (assume it's a comparison ask)." *Evaluator
  gate verdict*: **No** — re-reading the two tickets that prompted this
  suggestion, both were actually bug reports that happened to mention a
  migration from a competitor's product as context, not comparison
  requests. Knowing this "rule" in advance would have caused a
  misclassification, not prevented one — rejected before promotion to an
  active rule, per crystal 06's "would this have changed a prior decision
  for the better" gate.

## Memory cap note

Two active rules is well under the crystal's 10-12 rule cap — no merge or
archive step needed yet. When this file approaches the cap, the oldest
unreferenced rule gets moved to an archive file with a one-line reason,
per the crystal's "memory cap" section.
