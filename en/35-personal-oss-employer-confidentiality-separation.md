<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Separating Personal OSS Work From Employer Confidentiality — What to Filter Out, and How

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/35-personal-oss-employer-confidentiality-separation.md)**

**Version**: 1.0.0
**Content hash**: sha256:26e425dc225c (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 The general legal frame (the definition of a
trade secret, the two-part test) was verified against the primary source at
Cornell Law School's Legal Information Institute. The practical procedure
(pre-publication scrubbing + review process + separating personal vs. work
projects + a mandatory disclaimer) was verified against Google's official
open-source publication guidelines.

If [23-confidential-project-protection.md](23-confidential-project-protection.md)
runs in the direction of "keeping this project's own confidential material
from accidentally being pushed," this crystal runs in the **opposite
direction** — it covers the procedure for making sure that output originally
intended for publication (a personal open-source project, a technical blog
post, a document in this very framework) doesn't unconsciously end up mixed
with **confidential information or trade secrets belonging to one's
employer**.

## Basis

### 1. The General Definition of a Trade Secret — Two Elements That Apply Regardless of Jurisdiction

Verified via Cornell LII: for information to be protected as a trade secret,
it must satisfy **both** of two requirements — (1) **independent economic
value derived from being secret** (not generally known, and not readily
ascertainable through proper means by others), and (2) **the owner has
actually taken reasonable measures to keep it secret**. If either requirement
is absent, it isn't legally a trade secret — for example, if it's a
combination of already widely known techniques, or if the company hasn't
really treated the information as secret (e.g., it was already covered in a
public presentation), it's likely not protected. This definition is the
common backbone of both U.S. federal law (the Defend Trade Secrets Act) and
the Uniform Trade Secrets Act adopted by most states, so it can be applied
first as **a general test** that sits above the statutes of any particular
jurisdiction (e.g., California Labor Code Section 2870-type provisions) —
jurisdiction-specific provisions are treated as additional protections/
exceptions layered on top of this general test.

### 2. The Practical Procedure — Google's Official Open-Source Publication Guidelines

Verified via Google's publication guidelines (its official open-source
documentation site): before an employee can open-source code, it goes through
(a) a step to **scrub company confidential information from the code and
comments** prior to publication, (b) a step to run automated tools (linters,
etc.) that catch compliance issues, and (c) **a formal approval process**
(a lightweight process for personal projects, a heavier one when there's any
connection to work). And the guidelines explicitly state the principle that
**"a mandatory disclaimer is included in side projects regardless of whether
they're work-related"** — handling the "this is a personal project, not the
company's official position" statement with standard boilerplate rather than
re-deciding it every time.

## Core Mechanisms

### 1. Judge Along Two Separate Axes (Don't Mix Them)
- **Axis A — the originality of the content itself**: is this a combination
  of already-public academic/industry knowledge, or is it a design, figure,
  or piece of customer information unique to the employer? This is an axis
  you can evaluate yourself simply by looking at the content.
- **Axis B — whether it's permitted given the employment relationship**: does
  the employment contract or the employer's policy allow this publication?
  This is an axis you cannot answer without checking the contract/internal
  policy — even if Axis A comes back "low originality (looks safe)," Axis B is
  not skipped. Both must pass to be a publication candidate.

### 2. Make Pre-Publication Scrubbing an Explicit Step, Not "an Occasional Look-Over"
Don't leave review to human memory — make it a fixed step in the publication
pipeline, covering both an automated scanner (for pattern-matchable material)
and final human judgment (for what patterns can't catch, e.g., combination
risks of the [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md)
kind).

### 3. Branch Review Intensity by Work-Relatedness
First judge "is this at all related to work," and route purely personal
projects to a lighter process while anything overlapping with work — even
slightly — goes through a heavier process (formal approval, etc.) — forcing
every publication through the same heavy process makes execution impossible,
while treating everything lightly misses real risk.

### 4. Keep the Mandatory Disclaimer as Standard Boilerplate, in a Separate File
Rather than rewording it every time something is published, settle on **one
standard boilerplate** to reuse for the disclaimer that conveys "this content
is a personal opinion/personal project, not the official position of my
employer, and contains no confidential information or trade secrets belonging
to my employer" — this doesn't complete a legal defense (a disclaimer alone
doesn't excuse an actual confidentiality leak), but it honestly informs the
reader of this content's nature, and it's a practical device that avoids
re-deciding the wording every time. **This standard boilerplate belongs in a
separate, unnumbered file** — not inside this methodology document (in this
repo, `DISCLAIMER.md`) — because a methodology document (the why/how) and a
deliverable (text to be posted as-is) are found via different paths: the
former is looked up and read when a judgment call is needed, while the latter
needs to be copy-pasted right before publishing. Mixing them into one file
forces anyone looking for the latter to read through all of the former.

## Enforcement Mechanism — Technically Blocking a Push When Something Is Ambiguous

The four mechanisms above are judgment methods, not enforcement devices — if
the principle of "a human reviews it" is only ever written down in a
document, this framework reproduces the very trap it has repeatedly hit
before: "documentation alone doesn't prevent recurrence." Two devices that
actually enforce this are put in place together:

1. **Use a human-confirmation gate for ambiguous judgments**: when Axis B
   (whether it's permitted given the employment relationship) is uncertain,
   reuse the human-confirmation mechanism already in place (`oversight_gate:
   confirm` in [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) /
   [09-project-structure-template.md](09-project-structure-template.md)) — don't invent a new approval process.
2. **Technically block the push itself before that confirmation actually
   happens**: keep a "pending-review" list file (the same hook that [23-confidential-project-
   protection.md](23-confidential-project-protection.md)
   already uses to block already-confirmed confidential paths, but **a
   different list**), and have a pre-push hook block any commit touching a
   path on that list from going out to the remote. Once a human finishes
   review and judges it safe, they remove that line from the list themselves —
   requiring a human to edit the list file (not the code) to unblock it
   prevents the AI from unilaterally deciding "this is now safe" and
   bypassing the gate (local commits are allowed; only the push to the remote
   is blocked — there's no need to block version control itself). This is the
   same design philosophy — the three-tier escalation of "primary guidelines →
   secondary active masking → tertiary hook enforcement" already established
   by [07-prompt-guardrails/](07-prompt-guardrails/) — applied to this domain
   (Axis B judgment).

## How This Differs From Crystal 23 (G3)

[23-confidential-project-protection.md](23-confidential-project-protection.md)
uses a hook to forcibly block paths **this project itself created** that have
already been classified as "confidential" (direction: blocking inside → out).
This crystal is the procedure for judging whether confidential information
**attributable to a third party (the employer)** has unconsciously been mixed
into content **intended for publication** (direction: figuring out what got
mixed in, first). The former is an enforcement mechanism applied after
classification is finished; the latter is the methodology for the
classification itself — they're complementary and don't overlap.

## Honest Limitations

- This document is not legal advice — it provides "items to check and a
  general test," not a substitute for a final judgment specific to a
  particular jurisdiction or contract.
- Only Google's case was verified against a primary source — this document
  doesn't claim, as a generalization, that other organizations use a similar
  process (scrub + approve + disclaimer). That said, the scaffold of
  "scrub confidential information, then publish" connects logically to
  requirement 2 of trade secret law (reasonable measures to maintain
  secrecy), so it can be viewed as a procedure that flows naturally from
  legal requirements rather than from one particular corporate culture.

## Related
- [23-confidential-project-protection.md](23-confidential-project-protection.md) —
  the opposite direction (forced blocking of material already classified as
  confidential).
- [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md) —
  shares scrubbing-step methodology in that it's a risk pattern-matching
  can't catch.
- `RISK-ANALYSIS.md` — a case applying this crystal's general principle to one
  actual project (the one explicit exception to G2 in this document).
