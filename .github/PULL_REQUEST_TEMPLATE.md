## What kind of change is this?

- [ ] New crystal proposal
- [ ] Edit to an existing crystal (typo, wording, dead link, outdated info)
- [ ] Change to `07-prompt-guardrails/` (the executable code)
- [ ] Change to a `scripts/agent-ops-framework-*.py` tool
- [ ] Translation only (`en/` ↔ `ko/` sync)
- [ ] Something else (describe below)

## What does this change, and why?

<!-- One or two sentences. If this fixes an open issue, write "Closes #123". -->

## If this is a new crystal: the 6-gate self-check

(See `ko/BLUEPRINT.md` section 2 for the full explanation of each gate —
this is intentionally the same checklist a maintainer will apply during
review, so you can catch a likely rejection before asking for someone's
time.)

- [ ] **G1 — Verification strength assignable**: I opened the primary
      source myself at least once (🟢), or explicitly marked what's only
      skeleton-verified (🟡). I did not invent a plausible-sounding
      citation.
- [ ] **G2 — Domain knowledge minimized**: no dates, project names, or
      quotes specific to where this pattern came from — a reader with zero
      context on my project can use this as-is.
- [ ] **G3 — No substantial overlap**: I checked against at least one
      existing crystal and can say which one and why this is different
      (name it in the description above).
- [ ] **G4 — Fits a category**: it fits one of the existing categories in
      `ko/README.md`, or I'm proposing a new one and explaining why.
- [ ] **G5 — Passes the public-safety check**: I ran `ko/RISK-ANALYSIS.md`'s
      4-question decision tree against this content.
- [ ] **G6 — Has a usage trigger**: I can write one line for
      `ko/USAGE-GUIDE.md` in the form "when you're in this situation, read
      this crystal."

## If this is an edit to an existing crystal

- [ ] I ran `./scripts/agent-ops-framework-version-stamp.py <file>
      --bump=major|minor|patch` and picked the level myself (no default —
      see `CONTRIBUTING.md`).
- [ ] I ran `./scripts/agent-ops-framework-version-check.py` and it's
      clean for the file(s) I touched.

## Language

- [ ] I read Korean and edited `ko/` directly (translation to `en/` can
      follow, by me or a maintainer).
- [ ] I don't read Korean and this PR is against `en/` — I understand this
      lands in a `DIVERGED` state until a maintainer reconciles it into
      `ko/` (see `CONTRIBUTING.md`'s "Language" section for why, and the
      honest cost of that wait).

## Anything a reviewer should know that isn't obvious from the diff?

<!-- Optional. Delete this section if there's nothing to add. -->
