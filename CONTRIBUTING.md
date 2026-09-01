# Contributing to agent-ops-framework

Thanks for considering a contribution. This project has a specific bar for
what belongs in it, so please read this before opening a pull request —
it'll save you a round-trip.

## What this project is (and isn't)

`agent-ops-framework` is a collection of **domain-neutral structural
patterns** ("crystals") for AI-agent-managed projects — governance,
quality verification, safety, observability, documentation. It is **not**
a place for:
- Domain-specific content (a particular project's tasks, data, or product
  decisions).
- Unverified opinion dressed up as principle — every crystal states its
  verification strength (🟢/🟡) and traces to either a primary source or a
  documented, field-tested practice.

## Before you propose a new crystal — the gate

Read [`ko/BLUEPRINT.md`](ko/BLUEPRINT.md) section 2 in full. Every new
crystal must clear all six gates:

1. **Verification strength is assignable** (🟢 primary source directly
   checked, or 🟡 skeleton confirmed, details reconstructed).
2. **Domain knowledge is minimized** — the document must stand on its own
   with no dates, project names, or user quotes.
3. **No substantial overlap** with an existing crystal (say which one you
   checked against, and why this is different).
4. **Fits a category**, or justifies a new one, without pushing any
   category past 6-7 entries without considering a split.
5. **Passes the public-safety check** — see [`ko/RISK-ANALYSIS.md`](ko/RISK-ANALYSIS.md)'s
   four-question tree.
6. **Gets a `ko/USAGE-GUIDE.md` line** — "when you're in this situation,
   read this crystal." If you can't write that line, the crystal's
   real-world trigger probably isn't clear yet.

If a candidate doesn't clear all six, it doesn't go in — that's by
design, not an oversight. See [`ko/README.md`](ko/README.md)'s "why
crystal" section for why this bar exists.

## How to propose one

1. Open an issue describing the pattern, its source, and which existing
   crystal you checked it against (gate 3). English is completely fine —
   the six gates (verification, sourcing, non-overlap, categorization,
   safety, a usage trigger) are about the *pattern*, not the language you
   describe it in.
2. If it looks like a fit, draft the crystal following the format of any
   existing file in `ko/` — verification-strength line first, then
   the pattern itself, then an honest "limits" section.
3. **If you read Korean**: submit the Korean original in `ko/` directly
   (translation to `en/` can follow, by you or a maintainer).
   **If you don't** (this is a real, first-class path, not a fallback):
   draft the crystal in English and open your PR against `en/` — write it
   as if `en/` were the canonical file, gates and all. A maintainer who
   reads Korean produces the `ko/` file from your draft as part of review
   (porting the pattern, not just running it through a translator, so the
   gates get checked against what you actually meant) and merges both
   together. You are not expected to personally produce a Korean file to
   get a new crystal accepted — the same honest caveat from the "Language"
   section below applies here too: this reconciliation step depends on a
   maintainer being available, so a first-time English-only proposal may
   sit longer before merging than an edit to an existing crystal would.

## Making a pull request — the actual mechanics

If you haven't opened a PR against a repo you don't have write access to
before, here's the whole flow:

```bash
# 1. Fork this repo on GitHub (the "Fork" button), then clone your fork
git clone https://github.com/<your-username>/agent-ops-framework.git
cd agent-ops-framework

# 2. Create a branch -- don't commit directly on main
git checkout -b add-crystal-my-pattern   # or: fix-broken-link-in-09, etc.

# 3. Make your change, then (if it's an edit to an existing crystal)
#    version-stamp it -- see "Versioning an existing crystal" below

# 4. Commit and push to YOUR fork
git add <the files you changed>
git commit -m "Add crystal: <short description>"
git push origin add-crystal-my-pattern

# 5. Open the PR: GitHub will show a banner on your fork's page, or go to
#    https://github.com/jinwookim0/agent-ops-framework/compare
```

Opening the PR auto-fills `.github/PULL_REQUEST_TEMPLATE.md` — fill it in
honestly; it's the same 6-gate checklist described above, so doing this
carefully is most of the review. A GitHub Actions workflow
(`.github/workflows/verify.yml`) runs this repo's own verification
scripts on your PR automatically — `agent-ops-framework-version-check.py`
and `agent-ops-framework-translation-sync-check.py` are advisory (they
report, they don't block), but `public-repo-check.sh` does fail the build
if it finds something that looks like a leaked secret or personal data in
your diff.

If you want to keep your branch up to date with `main` while your PR is
open: `git fetch upstream main && git rebase upstream/main` (after adding
the original repo as a remote named `upstream` once:
`git remote add upstream https://github.com/jinwookim0/agent-ops-framework.git`).

## Versioning an existing crystal

Every crystal in `ko/` carries a `**버전**` (semantic version) and
`**콘텐츠 해시**` (SHA-256 of its body) right under the title. When you
change a crystal's content:

1. Make your edit.
2. Run `./scripts/agent-ops-framework-version-stamp.py <file> --bump=major|minor|patch`
   — pick the level yourself (there's no default; the tool won't guess for
   you): `major` for a reversed/fundamentally changed principle (rare),
   `minor` for a new mechanism or section added without changing the core
   principle, `patch` for wording/typo/link fixes with no meaning change.
3. Run `./scripts/agent-ops-framework-version-check.py` to confirm the
   stored hash matches the actual content — this needs no git history at
   all, so it works the same way even on a copy of the file living in a
   completely different repository.

## Language

The default source of truth is Korean (`ko/`); `en/` is its translation.
**If you don't read Korean, that's fine — send your PR against `en/`
directly.** Your change won't be silently dropped: `agent-ops-framework-
translation-sync-check.py` detects when a translation file has been
edited independent of the Korean source (flagged `DIVERGED`, distinct
from ordinary `STALE`), and a maintainer reconciles it by porting the
substance of your change into `ko/` and re-translating from there — see
`ko/BLUEPRINT.md` section 7 for the exact protocol. Prose can't be
auto-merged safely across two languages, so this reconciliation is a
manual step, not something CI resolves for you.

**Stated plainly (added after a 2026-09-01 red-team review), because it's
a real cost and not just a formality**: your `en/` PR does not merge as
one atomic action the way a PR against an English-SSOT project's canonical
file would. It sits in `DIVERGED` state — not merged, not rejected, just
pending — until a maintainer who reads Korean does the reconciliation
above. If no such maintainer is actively available, your fix will sit
unmerged for as long as that takes, through no fault of your own. This is
a real, asymmetric cost this project's Korean-SSOT choice places on
contributors who don't read Korean, not a hypothetical one — it's disclosed
here honestly rather than glossed over.

## Maintainers and disputed decisions

This project currently has one maintainer — the repository owner. There is
no review board, no second approver, and no formal dissent process yet;
that's an honest gap for a project soliciting outside contributions (found
in the same 2026-09-01 red-team review), not a deliberate governance
choice. Until this grows past one maintainer:
- **Contact**: open a GitHub issue on this repository — for anything
  sensitive (e.g. a conduct concern), mark it clearly as such in the title.
- **If you disagree with a gate ruling** on your PR (e.g. you think a G5
  public-safety rejection was wrong), say so directly in the PR thread with
  your reasoning. There's no formal appeal path beyond that yet — the
  maintainer's call is final for now, and that limit is stated here
  honestly rather than implied to be more than it is.

## Code of conduct

This project follows [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — the
literal Contributor Covenant v2.1 text, with reports going to this
repository's GitHub issues (see that file's "Enforcement" section).
