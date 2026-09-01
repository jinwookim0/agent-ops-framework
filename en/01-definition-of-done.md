<!-- translated-from: ssot=sha256:6083e43675d6 own=sha256:38c299cf77ee -->
# Definition of Done — Completion Criteria for AI Agent Work (Domain-Neutral Template)

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/01-definition-of-done.md)**

**Version**: 1.0.2
**Content hash**: sha256:6443abaf7bdc (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 Draws on Scrum's standard Definition of
Done concept, and each of the 10 criteria traces back to a real incident/
recurrence-prevention history in the original project.

Projects where an AI agent keeps producing multiple units of work (tasks/skills/agents)
run into a recurring problem: the bar for "this is done" drifts implicitly from
one piece of work to the next. This document makes that bar explicit as 10
criteria and states the reasoning behind each one — use it as a checklist
directly, both when scaffolding a new project and when auditing existing
completeness.

## Why this is needed

Conventions emerge naturally (frontmatter structure, confirm-needed tags,
eval cases, and so on), but **implicit habit** and **stated criteria** are not
the same thing. The later a piece of work is created, the more likely it is
to skip a convention. Writing the criteria down makes it possible to
mechanically check what's missing when scaffolding new work, lets someone
else later (a person, or an AI in a different session) understand "why it was
built this way," and lets **structural completeness** be verified as a
counterpart to content-quality verification (eval).

## Criteria 1–7 — Structural criteria

| # | Criterion | Rationale |
|---|---|---|
| 1 | **Metadata completeness**: the unit of work (skill/agent/etc.) has its name, status, execution cadence, success criteria, required tools, execution owner, oversight tier, and list of irreversible actions all filled in | Empty fields make it impossible to later know "why it was built this way" |
| 2 | **Actionable procedure**: the steps from input-check → investigation → output → save are written concretely, not as prose | If the procedure exists only as prose, quality swings wildly on each execution |
| 3 | **Uncertainty-handling principle + confidence-tier labeling**: there is a principle that information which can't be verified, or that changes over time, is flagged as "needs confirmation." In addition, each output is assigned a confidence tier (e.g. `none` = already certain from execution logs/source comparison, `flag` = time-sensitive or plausible-looking, `ask` = risky if not confirmed with the user) with a one-line rationale for that value. This is a different axis from "how easy is this action to reverse" (criterion 5) — it's about confidence in the *content*. Outputs tagged `flag` state the applicability conditions alongside the claim (e.g. "no disagreement found across an n-sample comparison") instead of absolute-confidence language like "proven" or "certain" | Without this principle, plausible-but-wrong information gets mixed in — empirically demonstrated. Basis: Amershi et al. 2019, *Guidelines for Human-AI Interaction* (G2/G10 — make the system's degree of confidence clear to the user) |
| 4 | **Eval cases exist**: there are 2 or more eval cases that grade this work's output, plus a concrete rubric. Exception: pure infrastructure that doesn't generate content (e.g. the evaluator itself) is exempt, but the reason must be recorded | The core defense against regression. Evaluating an evaluator with itself is infinite regress, so a practical exception is carved out |
| 5 | **Stated basis for the oversight tier**: if execution happens with no human involvement (`none`), explain in one line or more why it's easy to reverse; if it's notify-only (`notify`) or wait-for-confirmation (`confirm`), state what the irreversible action is. **Rule**: work that recurs periodically and may eventually run unattended (e.g. via cron) cannot use `confirm` (one-off/on-demand work is exempt, since it assumes a human is present at execution time) — if an irreversible action is required, combine `notify` with a safe default such as "leave the final decision as a draft pending confirmation" | Basis: Hadfield-Menell et al. 2017, *The Off-Switch Game* ([arXiv:1611.08219](https://arxiv.org/abs/1611.08219)) — a blocking confirm gate with no human available to respond leads either to deadlock, or to the agent proceeding arbitrarily after waiting for a response that never comes |
| 6 | **A place for preference/context accumulation** (where applicable): there is a store where user preferences and context accumulate across repeated runs, raising quality over time | For anything that isn't a one-off task, accumulation is what drives quality |
| 7 | **Reflected in the root index**: the project-wide index (README, etc.) reflects this piece of work | Work that isn't reflected there can't be discovered even if it exists — this defeats the purpose of project management itself |

If 3 or more criteria are unmet, it's recommended to mark that piece of work
as a "draft" rather than "done."

## Criterion 8 — Basis for AI comparative advantage (a value criterion, not a structural one)

The 7 above ask "is the structure in place." This one asks a different
question — **"why is doing this with AI actually better than a human doing it
directly?"** A useful reference skeleton is the Fitts List (1951, the
standard framework in human factors for first systematizing which tasks
should be assigned to humans vs. machines): humans are strong at judgment,
improvisation, and meaningful pattern recognition; machines are strong at
speed, precision, repetition, measurement, and conditions that exhaust
humans.

**But this is only a skeleton.** Pasting the generic claim "AI is fast and
accurate" into every piece of work is itself an unsupported claim. Each piece
of work must state, in one line, the **specific bottleneck a human actually
experiences** (e.g., "tracking the combinatorics of dependencies across many
items grows too fast for a human to hold in their head"). In areas where
humans are better (value judgments, the emotional nuance of relationships,
etc.), don't force-fit this justification — use the principle "AI organizes,
it does not judge" instead.

**Being honest about this**: most one-line "AI comparative advantage"
statements are not sourced research but plausible reasoning (reasoned
inference) — by Toulmin's model of argument (Claim/Grounds/Warrant), they're
closer to a claim without grounds. That's not inherently bad, but it should
not be treated as equivalent to empirical evidence (use hedged language like
"likely").

## Criterion 9 — Actionability

**Purpose declaration**: the purpose of any AI-produced work must always let
the user come away with at least one of: **① knowledge/insight** (a newly
learned fact), **② decision-making inputs** (evidence/material to inform
judgment, not the conclusion itself), or **③ actionability**
(what to do next, and where/how to look into it).

**Failure pattern**: sentences that merely confirm the existence of a
structure or fact and stop there — "this structure exists," "this process is
underway" — provide no actionability, even when every word is true and
sourced. Don't end with "confirmed / it's possible" — point to exactly where,
what, and with which keywords to look next.

**Self-check questions**:
- [ ] If every proper noun (specific name, number, URL, date) were stripped
      from this document, would the content go empty, or would it still read
      as generic filler — the latter signals insufficient specificity.
- [ ] Does a sentence that ends with "confirmed / it's possible" continue
      into "where / what" to check next, or does it just stop there?
- [ ] If someone else repeated the same investigation, could they tell
      exactly where to start from this document alone?

**Why this doesn't conflict with criterion 3 (uncertainty handling)**:
specificity does not mean "state the unverified as settled" — in fact, the
more specific you get, the more room there is to break down the evidence
hierarchy in finer detail. Lack of specificity and overconfidence are
separate axes.

## Criterion 10 — Accounting for motivational bias in content sources

When citing external content (news, blogs, press releases, etc.), **"this
was actually reported/announced that way" (fact-checked) is a different
question from "that report/announcement is neutral."** Even when individual
facts are quoted accurately, the AI must not carry over the evaluative
framing embedded in them as if it were endorsing that framing itself.

**Self-check questions**:
- [ ] Is the quoted sentence a factual statement of "what happened," or an
      evaluative statement of "and that's good/bad" — if the latter, is it
      made clear whose viewpoint this is?
- [ ] When covering news where the announcing party has an incentive to
      promote it, is that incentive itself made visible to the reader?
- [ ] Does unconfirmed language ("planned," "expected") come across as
      positive regardless of whether it actually materializes — was the
      possibility of cancellation or delay looked into with equal weight?

**An important boundary**: warning that "this content may be promotional"
(flagging verification status) is different from asserting "this party wrote
it this way with promotional intent" (asserting motive) — do the former, not
the latter. Concretely: "this framing comes from [party]'s own announcement
and has not been independently verified" is fine; "[party] emphasized this
angle for promotional purposes" is an unsupported assertion of intent.
**This boundary itself was added after directly experiencing that applying
this very criterion can create a new unsupported assertion** — the lesson
that the act of building a guardrail is itself subject to the same
guardrail.

## When creating new work

Apply these 10 criteria directly in the project's scaffolding procedure (the
steps for creating new work). Criteria 9 and 10 differ in character from the
other 8 (which are set up once, when the work is created) in that they are
content-quality criteria applied **every time an output is produced**, not
only at scaffolding time — bake them into the default eval rubric template.

## Related crystals

- This document covers structural completeness only — for content safety,
  see the prompt guardrails document
  ([07-prompt-guardrails/](07-prompt-guardrails/)); for content-quality
  verification methods, see
  [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md);
  for the scope of autonomous execution, see
  [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
  — these are different axes and are intentionally kept separate rather than
  merged.
