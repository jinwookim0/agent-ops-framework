<!-- translated-from: ssot=sha256:497099c4f933 own=sha256:867453b26394 -->
# Getting Started — the step-by-step path to actually adopting this in your project

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/GETTING-STARTED.md)**

If [USAGE-GUIDE.md](USAGE-GUIDE.md) organizes this framework by five
perspectives — planning, design, implementation, improvement, reference —
this document runs along a different axis: **the literal, in-order
procedure for someone bringing this folder into their project for the
first time**. Keep using USAGE-GUIDE.md for perspective-based explanations
and its reference table ("what to read for this situation") — this
document doesn't replace either. It's a one-time checklist for the first
pass only.

**Prerequisite**: this framework isn't for "any project that uses AI
somewhere" — it targets the narrower scope [README.md](README.md)
defines: **a project where an AI agent handles multiple tasks
autonomously and repeatedly**. The whole folder is overkill for a single
one-off question-answer feature. If that's not your situation, skip past
this. Otherwise, keep reading.

**At a glance**: Step 0 (bring it in) → Step 1 (reset state files) →
Step 2 (install and verify the guardrails) → Step 3 (add the rest only
as needed, in order) → Step 4 (grow it with your own project's cases) →
Step 5 (don't call it done until it's verified). Everything below adds
detail as you go — if you just need to know what to do right now, this
one line is enough.

## Step 0 — Bring the folder in: decide copy vs. clone-and-reference first

**Option A — copy (recommended, the default path)**: copy this
repository wholesale, or attach it as a submodule. Place it at your
project's root as `agent-ops-framework/` (or whatever name you prefer) —
the relative-path links inside each crystal (e.g.
`02-directive-registry.md`) and the path constants in the scanner scripts
assume this folder structure stays intact, so the simplest approach is to
not split the folder up. Everything from Step 1 on assumes this option.

**Option B — clone it elsewhere and only reference the path**: clone
this repository to a separate location and just tell your AI agent's
prompt/`CLAUDE.md` to "consult this path when making decisions." No
vendoring, and a later `git pull` keeps you on the newest crystals. Two
cases this doesn't cover: **① [07-prompt-guardrails/](07-prompt-guardrails/)
is executable code** — the Claude Code hook (the `command` path in
`settings.json`) and the git `pre-push` hook only work by invoking an
actual local file in your project, so merely "referencing" a cloned path
never runs; copy this one locally per Step 2 below regardless of which
option you pick here. **② Documents meant to be filled in with your own
project's directives and discoveries**, like
[02-directive-registry.md](02-directive-registry.md) and
[01-definition-of-done.md](01-definition-of-done.md) — keep only
pointing at the cloned reference and it stays someone else's repo
forever, so once a crystal reaches Step 4 below, copy it in and make it
your project's own. Mixing the two is fine: copy 07 in always, start
everything else as a clone-reference, and switch individual crystals to
a local copy once you actually need to edit or extend them.

## Step 1 — Reset the three operational state files (don't skip this)

The crystal files (`NN-*.md`) are all domain-neutral, so copying them
verbatim is safe. But the files below carry **the origin project's own
execution history**, and dragging them along as-is means your new
project starts day one with someone else's history mixed in (full
rationale in [BLUEPRINT.md](BLUEPRINT.md) section 7):

| File | What to do |
|---|---|
| `REFLECTION-CANDIDATES.md` | Keep only the header (scanner description); empty the table |
| `.reflection-checkpoint` | Delete it, or reset it to 0 |
| The scanner scripts' `ORIGIN_MAP` (`agent-ops-framework-sync-check.py`) | Holds the origin project's file paths — refill it with your own project's document paths |
| `DISCLAIMER.md` | (Exception) safe to copy verbatim — just fill in the blank (your organization's name) |
| `RISK-ANALYSIS.md` | Don't reuse it — borrow only **the frame** (the 4 questions + decision tree) and write your own project's public-safety judgment from scratch |

## Step 2 — Install 07-prompt-guardrails first (before your first task touching personal data)

This one isn't a principle document — it's **working code you copy and
run**. In order:

1. Copy `07-prompt-guardrails/settings.json` → `.claude/settings.json`,
   `07-prompt-guardrails/hooks/guard-secrets.sh` →
   `.claude/hooks/guard-secrets.sh`, and
   `07-prompt-guardrails/scripts/*` → `scripts/`.
2. In `settings.json`'s `permissions.deny`, replace `shared/local/**`
   with whatever directory name your project actually uses for
   local-only sensitive files.
3. In `guard-secrets.sh`, change the `Artifact` matcher to the name of
   whatever external publish/deploy tool your project actually uses.
4. **Verify it live** — create a dummy file containing a sensitive
   pattern, actually attempt to publish or commit it, and confirm the
   block message actually fires. A config file being syntactically
   correct is not the same claim as it actually working. Delete the
   dummy file once confirmed.
5. (Optional) For the fourth layer of defense (the native git pre-push
   hook), copy `07-prompt-guardrails/hooks/pre-push-verify.sh`, point
   `.githooks/pre-push` at it, and run
   `git config core.hooksPath .githooks`.

The full install procedure, the 4-layer defense structure, and its known
limits live in
[07-prompt-guardrails/README.md](07-prompt-guardrails/README.md).

## Step 3 — Bring in the rest only as they become needed, in this order

Don't install everything at once — that's premature infrastructure in
its own right. Add crystals one at a time, in this order, only once each
one's actual trigger condition applies to your project:

1. **[01-definition-of-done.md](01-definition-of-done.md)** — once you
   pass 3–5 tasks and "this counts as done" starts meaning something
   different to different people. Use the 10 criteria as a checklist,
   as-is.
2. **[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)** —
   once the agent starts running repeatedly without a human checking
   every step.
3. **[02-directive-registry.md](02-directive-registry.md)** — once
   decisions pile up and you catch yourself asking "wait, why did we
   decide that?" Start filling row 1 with your own project's actual
   directives.
4. **[09-project-structure-template.md](09-project-structure-template.md)** —
   when you're designing (or redesigning) the project's structure
   itself. If a project already exists, don't force its existing
   folders into the 5-layer shape — ask first whether that layer is
   actually needed right now. Section 4's 13-step rebuild order works
   as a timeline for "what becomes necessary when."
5. **[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)**
   and **[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)** —
   the first time output quality needs serious measurement instead of
   eyeballing it.
6. **Every other crystal** — only once that document's own "why this
   matters" section actually applies to your situation. The trigger
   should be "this debt/problem actually happened," not "this feature
   would be nice to have."

## Step 4 — Don't stop at copying: grow it with your own project's cases

Each crystal is designed as a living document, not a static template.
The moment your first real failure or discovery shows up after porting
one in, add it right there:

- [03](03-epistemic-immunity-catalog.md) and
  [06](06-self-improving-heuristics-loop.md) — grow the catalog with
  cases you actually found.
- [02-directive-registry.md](02-directive-registry.md) — add a row every
  time a new directive shows up (the same table you reset in Step 1).
- [07-prompt-guardrails/](07-prompt-guardrails/)'s `PATTERNS`/`check(...)`
  lists — add a regex the moment you spot a sensitive-data pattern that's
  common in your project (an internal token format, say).

At the same time, **guard against bloat** — follow the "avoid bloat"
sections in [02](02-directive-registry.md) and
[06](06-self-improving-heuristics-loop.md) so these documents don't grow
without ever being pruned.

## Step 5 — Don't call it "adopted" until you've verified it

Copying a file and never actually using it once isn't adoption. For
example, the guardrails in Step 2 require a live publish/commit attempt
as part of installation, not just a config that looks right (Step 2,
item 4). The same distinction applies to every other crystal: "I copied
the document" and "I've actually applied this bar/procedure at least
once in this project" are different claims — keep them separate.

## From here on

This document ends here — from now on, reach for
[USAGE-GUIDE.md](USAGE-GUIDE.md)'s reference table ("situation you're in
→ crystal to read") as your index whenever a new situation comes up.

## Related documents

- [README.md](README.md) — the full overview of this folder and the map
  of all 37 crystals.
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — the five perspectives (planning,
  design, implementation, improvement, reference) plus the
  situation-based reference table.
- [BLUEPRINT.md](BLUEPRINT.md) — what this folder itself is, the gates a
  new crystal must clear, and section 7's porting/reset procedure (the
  basis for Step 1 above).
