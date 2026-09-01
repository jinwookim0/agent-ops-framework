<!-- translated-from: ssot=sha256:9d4acf694edb own=sha256:01a341e7a5e3 -->
# agent-ops-framework Blueprint — What It Is and How It Grows

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/BLUEPRINT.md)**

If `README.md` is the map of "what exists right now," this document covers
"**why it's shaped this way, what criteria the next crystal is admitted
under, and how that admission gets discovered automatically**" — the way
any project keeps its own project-blueprint document describing its
overall structure, this document plays that role for this folder itself.

## 1. Identity — what is a crystal

A crystal is **not a finished spec, but a piece of a living reference
framework**. Three things must always be present together for something to
be a crystal:

1. **Domain-neutral description** — no proper nouns, dates, or user remarks
   specific to a particular project. Only the principle and the procedure
   remain.
2. **Verification-strength labeling** — stated at the top of every document
   as either 🟢 (the primary source's core content directly verified) or 🟡
   (only the skeleton/names verified, with details reconstructed). A
   crystal without this label cannot exist — fabricating a
   plausible-sounding principle without grounding is exactly the failure
   pattern this framework exists to prevent
   ([03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)).
3. **At least one evidentiary path** — either (a) something field-verified
   in some project's actual operating history, with the narrative stripped
   away and only the pattern kept, or (b) the core claims of an external,
   verifiable standard (a paper, an official spec, an industry framework)
   checked against the original source. Without either one, it isn't a
   crystal, just an opinion.

## 2. Admission gate — turning "only the highest quality may exist" into concrete criteria

For a new crystal candidate to actually be admitted, it must clear all 6 of
the gates below. Missing even one means the admission is held (recorded in
REFLECTION-CANDIDATES.md as "held" along with the reason — never quietly
dropped).

| # | Gate | How it's judged |
|---|---|---|
| G1 | Can a verification strength be assigned | Was the primary source actually opened and checked at least once (🟢), or was only the skeleton verified, with that stated explicitly (🟡)? If neither, admission isn't possible |
| G2 | Is domain knowledge minimized | Does the document still stand fully on its own once dates, specific project names, and user quotes are stripped out (see section 1 above)? `RISK-ANALYSIS.md` is the only explicit exception to this gate |
| G3 | Does it meaningfully avoid overlapping with existing crystals | At least one existing crystal must actually be reread and cross-checked (Chesterton's Fence — don't create something new without first confirming why it wasn't already there) |
| G4 | Can it be placed in a category | Does it fit into one of the existing 7 categories, or is it different enough an axis to warrant a new one? Once a category exceeds 6-7 crystals, review whether to split it before adding (README.md, "Principles for when scale grows") |
| G5 | Public-release safety | Re-apply `RISK-ANALYSIS.md`'s 4-question decision tree to the new crystal, to confirm it doesn't drag in the original project's confidential or competitive information |
| G6 | Usage-guide update | Can at least one line be added to `USAGE-GUIDE.md` in the form "in this situation, use this crystal"? If you can't fill that in, it's a sign it's still unclear when this would actually get used in practice |

## 3. Growth process — 4 stages from discovery to integration

```
1. Discovery         The original project keeps evolving and produces new
                      structural patterns along the way — either a person
                      notices, or the automated scanner in section 4 below
                      flags it as a candidate
        ↓
2. Review             Apply the 6 gates in section 2 above one by one.
                      Record pass/hold in REFLECTION-CANDIDATES.md's
                      status column (never skipped silently)
        ↓
3. Extraction         Write the crystal file with the narrative stripped
                      away and only the principle/procedure kept, label
                      its verification strength, assign the next number
        ↓
4. Integration        Add one line to README.md's category table, update
                      USAGE-GUIDE.md, recheck the category's size (review
                      splitting if it exceeds 6-7)
```

## 4. Automation — catching "another project's evolution" without missing it

**The problem**: the original project (or any project that adopts this
framework) keeps evolving, and among all that evolution it's easy to miss
which changes are portable structural patterns — unless a person remembers,
every single time, to look back and check. Simply writing "let's reflect
this later" into a document doesn't prevent the problem from recurring —
this framework's own original project has already learned that the hard
way ([06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)
is grounded in the same problem awareness).

**The part that is automated (discovery only)**: whenever a project other
than this framework itself evolves, entries from its directive/change
history that contain signal words like "principle/rule/system/standard/
guardrail/gate/framework/automation" and are not about this framework
itself get automatically added to the candidate list. The candidate list is
append-only — nothing disappears from it until it has been reviewed.

**Honest limit — this scanner only looks at internal history (confirmed
by a 2026-09-01 red-team review)**: at least one crystal added to this
framework so far (the cost/budget-management axis) wasn't found by the
automated scanner at all — it was found because a user directly asked
"does this satisfy X standard?" The scanner only sweeps the original
project's own directive history; it doesn't do active benchmarking
against external frameworks (agentops.ai-style comparisons) or ask "what
axis are we missing" on its own. This can be a structural source of
confirmation bias — it confirms only what's asked about, while active,
self-initiated discovery stays limited to rehashing internal history.
This is still too few observations to call a pervasive pattern,
but it's left here as a candidate for the next round of expansion:
whether to automate periodic comparison against external frameworks.

**The part deliberately left unautomated (judgment)**: turning a candidate
into an actual crystal — whether it clears the gates in section 2 above —
is not automated. Automating that step would turn the gates into a
rubber-stamp formality and undermine the "only the highest quality may
exist" requirement — separating discovery from execution is a principle
already present elsewhere in this folder
([04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)'s
automated scoring and [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md)'s
debt-prioritization judgment both preserve this same boundary).

**Implementation form when porting**: a project adopting this folder can
treat its own `docs/directive-registry.md`-style document (a table that
accumulates directives/changes by number) as the scan target if it has one,
or fall back to a git commit log or any change-history document if it
doesn't, and apply the same 4-stage process (discover → review → extract →
integrate) as-is — whatever form the scan target takes, the skeleton of
"signal-word match → accumulate candidates → human/AI review" stays the
same.

## 5. Versioning & change management

- Crystal numbers are permanent — even when a crystal is retired, its
  number is never reused (the same "retired" principle already used in
  `02-directive-registry.md`).
- When a crystal's content is updated (e.g., its verification strength
  moves from 🟡 to 🟢), the file is edited directly — this folder does not
  keep a "when and why it was changed" history inside itself (the
  domain-knowledge minimization principle, section 1, G2 above). That
  history lives instead in the change-history document on the side of the
  original project that adopts this folder.
- When a category is split, the number stays fixed and only the category
  membership in README.md's table moves — external links referencing a
  crystal (`NN-filename.md`) don't break.

## 6. The same standard applies to this document too

This document is not a crystal but a governance document for this folder
(the same standing as `RISK-ANALYSIS.md` — outside the crystal list), but
G2 (domain-knowledge minimization) still applies to it in full — it does
not cite dates, a particular session's user remarks, or a specific crystal
number as an example. The conditions under which this document is judged
to have gone stale are the same as the "consistency-maintenance rule" in
[09-project-structure-template.md](09-project-structure-template.md): when
the gate criteria actually change, when the growth-process stages
themselves change, or when the automated scanner's design changes.

## 7. Porting into a new project — copy the whole folder, then reset

The crystal files in this folder (`NN-*.md`) are safe to copy as-is — they
have passed G2 (domain-knowledge minimization). But **two operational
state files inside the folder carry the original project's execution
history and must not be carried over as-is**:

- **`REFLECTION-CANDIDATES.md`**: this is a **work log** accumulating rows
  of candidates pulled from the original project's directive registry —
  it's not a crystal but a history of "what was reviewed," so carrying it
  into a new project turns it, itself, into domain knowledge (the
  narrative of the original project's specific directives and decisions).
  In a new project, reset this file down to just its header (the
  scanner's description plus an empty table).
- **`.reflection-checkpoint`**: a state value recording "how far the scan
  got last time," expressed as a number from the original project's
  directive registry — since a new project starts its own directive
  registry from 0, this file should also be deleted or reset to 0.
- **The path constants in the scanner scripts**
  (`agent-ops-framework-reflection-check.py`,
  `agent-ops-framework-sync-check.py`,
  `agent-ops-framework-translation-sync-check.py`) **can be left as-is**
  — they're designed on the assumption that, like `docs/directive-
  registry.md`, a new project keeps its own directive registry and
  crystals at the same relative path (`agent-ops-framework/ko/`) (this
  presupposes that the project being ported into also adopts this
  folder's own conventions — see [02](02-directive-registry.md)).
  `ORIGIN_MAP` (the original-to-crystal mapping used by sync-check) holds
  the original project's file paths and **must be refilled with the new
  project's own original-document paths** — this too is domain knowledge.
- **`RISK-ANALYSIS.md`**: this document is itself the explicit exception
  (section 1 above), so it retains the original project's actual judgments
  (content-risk assessment, etc.) — a new project should reuse only its
  **framework (the 4 questions plus the decision tree)** and refill the
  actual answers with its own situation.
- **`DISCLAIMER.md`**: unlike the three above, this file **is safe to copy
  as-is** — it's a reusable template where only the blanks (the affiliated
  organization's name) need filling in, and it carries none of the
  original project's execution history (passes G2). This is called out
  explicitly in this list so it isn't mistakenly wiped along with the
  other three, which get treated differently.

Skipping this reset means the new project's "domain-neutral structural
crystals" start day one already carrying the original project's history
mixed in — a case where G2 held for each individual crystal but broke at
the level of the folder's overall state.

**Language (the single source of truth is pinned to the Korean version)**:
actually publishing this folder to a wider audience may eventually call for
an English translation. But **while the folder is still actively growing
(as now, with crystals continuously being added, revised, and split)**,
maintaining two languages at once creates, structurally, exactly the kind
of drift (the original and the translation diverging) that this folder's
own `sync-check.py` exists to prevent — translation would incur an ongoing
maintenance cost of having to follow every edit to the original.
**Decision**: translation is not maintained continuously in parallel; it is
done as a **one-time snapshot job**, at the point this actually gets
extracted/published into a separate repository — until then, only this
document (the single source) keeps being revised.

**Translation sync is detected bidirectionally by
`agent-ops-framework-translation-sync-check.py`.** Even after a
translation is made once, the SSOT keeps changing — instead of a person
having to remember and check whether "the translation has fallen behind
the SSOT," the same design as `sync-check.py` (comparing the source
document's recent commits against the corresponding crystal) gets applied
to translated files too: each translated file records, as a stamp, which
SSOT commit it was translated from, and when the SSOT changes after that
the script raises one of two distinct signals (it does not automatically
retranslate — discovery is automated, judgment is human, the same
principle as BLUEPRINT section 4):

- **STALE**: the SSOT changed after the stamped commit — common and
  low-stakes, just retranslate from the current SSOT and re-stamp.
- **DIVERGED**: the translation file **itself** was edited directly
  without updating its stamp — for example, a contributor who can't read
  Korean editing `en/NN.md` via a PR produces exactly this signal.
  **Unlike STALE, this must never simply be overwritten** — it means the
  translation side is carrying a real contribution (a fixed mistranslation,
  a better explanation, a newly spotted defect) that hasn't been folded
  back in yet.

**Genuinely bidirectional flow — from "never edit the translation
directly" to "editing it is fine, but it must always flow back into the
SSOT."** An earlier version of this section forbade direct edits to the
translation. But being genuinely open source means a contributor who
can't read Korean still needs to be able to contribute meaningfully —
discarding their PR against `en/` as "against the rules" amounts to
blocking the contribution. So the rule changes: **direct edits are
allowed, but a reconciliation procedure requires that edit to flow back
into the SSOT**:

1. When a DIVERGED signal appears (from the script above), review what
   actually changed.
2. If the change is genuinely valid (a mistranslation fix, an
   improvement), **apply it to the SSOT first** (e.g. `ko/NN.md`) — don't
   just leave the translation's change in place and move on.
3. Once the SSOT is committed with that change, retranslate the
   translation file from that new commit and update its stamp to point
   at it.
4. **Why this isn't auto-merged**: prose doesn't three-way-merge safely
   the way code does — two language versions can naturally phrase things
   differently, so a mechanical merge easily breaks meaning. So this
   mechanism's job isn't "resolve the conflict automatically," it's
   "point precisely at where a conflict might be, so a human/AI doesn't
   have to diff two full documents from scratch every time."

**In rare cases, a single file's SSOT can be flipped.** For example, if a
particular crystal originated from an English-speaking contributor's
own independent research, it's fine for that one file to have `en/` as
its SSOT and `ko/` as the translation — just put the stamp on the other
file (whichever file carries the stamp is the translation; the one
without a stamp is the SSOT — `translation-sync-check.py` recognizes
this direction automatically). This is the exception, not the default —
the default is still that Korean is the SSOT.

**Which language the AI reads is pulled out into a separate config
file**: this document (BLUEPRINT.md) covers the **policy and rationale**
— "why the SSOT is Korean, and how the translation is managed." "Which
file the AI reading this framework should actually open right now, in
this moment" isn't something to work out from scratch every time — it's
spelled out as a default plus tiers and exceptions in
[LANGUAGE-POLICY.md](LANGUAGE-POLICY.md). The reason the rationale
document and the runtime configuration are kept separate is the same
spirit as the lesson section 4 of this document already made — that
"writing it down in a document alone doesn't prevent recurrence": rather
than making the AI read the policy and re-derive the reasoning every
time, a decision rule it can reference directly is put in place instead.

## Related
- [README.md](README.md) — the map of what currently exists.
- [LANGUAGE-POLICY.md](LANGUAGE-POLICY.md) — the runtime configuration
  that decides which of the Korean or English version an AI reads.
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — which crystal to read for which
  situation.
- [GLOSSARY.md](GLOSSARY.md) — an index of what this document's (and this
  whole folder's) recurring terms (crystal, story, domain
  knowledge/domain-neutral, SSOT, gate, ...) actually mean — most entries
  point back to where sections 1, 2, 4, and 7 of this document define them.
- [RISK-ANALYSIS.md](../ko/RISK-ANALYSIS.md) — public-release safety judgment
  (the basis for G5).
- [REFLECTION-CANDIDATES.md](../ko/REFLECTION-CANDIDATES.md) — the accumulated
  list of automatically discovered admission candidates (the output of
  section 4).
