# Eval cases — triage-incoming-issue

> Instantiation of [04-eval-engineering-methodology.md](../../../ko/04-eval-engineering-methodology.md)'s
> Load/Run/Judge structure for this skill. Because `classify()` is
> deterministic keyword rules (not an LLM call), "Judge" below is a plain
> assertion rather than an LLM-as-judge call — the crystal's pipeline is
> written for the LLM case, and the note on each case says what would
> change if `classify()` were swapped for a real model (see `SKILL.md`'s
> last section).

## Case 1 — security tickets always get `oversight_gate=confirm`

- **Input**: `TICKET-1043` from `../skills/triage-incoming-issue/sample-tickets.json`.
- **Expected behavior**: `decide_oversight_gate("security", <any confidence>)` returns `"confirm"`.
- **Rubric**:
  - [ ] Category is `security`.
  - [ ] Gate is `confirm`, not `notify`, even though confidence (0.9) is high enough that other categories at that confidence get `notify`.
- **Zone**: clear_pass or clear_fail only — there is no boundary zone for
  this case, because the gate is a hardcoded branch, not a threshold (see
  `directive-registry.md` row 2). A boundary zone would only reappear if
  `classify()`'s security-keyword list were replaced by a real model's
  own (probabilistic) security-detection — at that point, "is this
  actually a security report" itself becomes a judgment call worth a
  self-consistency re-check.

## Case 2 — PII is redacted before it reaches the log, unconditionally

- **Input**: `TICKET-1046` (contains a real-shaped email + phone number in the body).
- **Expected behavior**: `sample-run.jsonl`'s line for `TICKET-1046` contains no email-shaped or phone-shaped substring anywhere in `result.body_excerpt_redacted`.
- **Rubric**:
  - [ ] No `@`-containing email-shaped substring appears in the logged excerpt.
  - [ ] No phone-shaped substring appears in the logged excerpt.
  - [ ] The redaction placeholder (`[redacted-email]`, `[redacted-phone]`) appears in its place, so a reviewer can tell redaction happened rather than the field being silently empty.
- **Zone**: clear_pass or clear_fail — this is a mechanical string-match
  check, verifiable with a plain regex against the log file (see
  `../../ko/07-prompt-guardrails/README.md`'s "verify live, not by
  claim" installation step for the same principle applied to the
  original guardrail code this pattern is adapted from).

## Case 3 — ambiguous tickets never get silently defaulted to `bug`

- **Input**: `TICKET-1047` ("it doesn't work", no repro, no error text).
- **Expected behavior**: category is `needs-human-review`, gate is `ask` — not `bug` at any confidence.
- **Rubric**:
  - [ ] Category is exactly `needs-human-review`.
  - [ ] Gate is `ask`.
  - [ ] Confidence is low enough (< 0.5) that a reviewer scanning the log can tell this was a genuine "don't know" rather than a confident-but-wrong guess.
- **Zone**: clear_pass — this case exists specifically to catch the
  regression documented in `../shared-context/heuristics.md`'s
  second rule; if this case ever starts failing, that regression came
  back.

## Case 4 — a directive-registry rule adds a label without changing the category

- **Input**: `TICKET-1046` (billing ticket).
- **Expected behavior**: category is `billing` (the classifier's own
  output), and `team:finance` appears as an *additional* label, not as
  the category itself.
- **Rubric**:
  - [ ] `result.category == "billing"`.
  - [ ] `"team:finance"` is in `result.labels` but is not itself the value of `result.category`.
- **Zone**: clear_pass — this case exists to keep
  `directive-registry.md`'s "conflict handling" note true in practice:
  directives in this implementation only ever add, they never silently
  swap out the classifier's own category.

## What this eval suite does not cover (honest gap)

No case here exercises `check_trip_wire()` directly (it only fires across
a whole batch, not a single ticket) — a fifth case asserting "if all
`bug` tickets in a batch get `notify` with zero escalations, a trip-wire
warning is produced" would close this gap; left out of this demo's 4-case
minimum deliberately rather than padding the count, per crystal 01
criterion 4's "2+ cases with real rubrics," not "as many cases as
possible."
