#!/usr/bin/env python3
"""agent-ops-framework-translation-sync-check.py — checks translation sync
between agent-ops-framework/ko/ (the default SSOT) and agent-ops-framework/en/
in BOTH directions, so a contribution that lands directly in en/ (e.g. from
an English-speaking contributor who doesn't read Korean) isn't silently
discarded the next time ko/ changes. Also covers a handful of root-level
pairs outside that mirrored-folder structure (see EXTRA_PAIRS below) — so
far just the top-level landing-page README.md/README.ko.md pair, which
lives at the repo root instead of under ko//en/ so README.md can render as
GitHub's default repo homepage.

REDESIGNED 2026-09-01 to stop using git commit hashes at all (see
"Why content-hash, not commit-hash" below) — this is the second design of
this stamp. First design (git-commit-hash-based, renamed 2026-09-01 from
agent-ops-framework-translation-staleness-check.py, one-directional only)
is retired; if you're looking at a file still carrying the old
`<!-- translated-from: <40-hex-char-commit-hash> -->` format, it predates
this redesign and needs re-stamping with `--restamp`.

Stamp format (first line of a translated file):
  <!-- translated-from: ssot=sha256:<12-hex> own=sha256:<12-hex> -->
Whichever file HAS this stamp is the derived translation; whichever file
lacks it is that file's SSOT. Normally ko/NN.md has no stamp and en/NN.md
does (ko is SSOT). A file's ownership CAN be flipped per-file (rare — e.g.
a crystal originated as an English contribution) by moving the stamp onto
the ko/ file instead; this script handles either direction the same way.

`ssot=` is a content hash (sha256, first 12 hex chars) of the SSOT file's
full text, taken at the moment this translation was last (re-)stamped.
`own=` is the same kind of hash of the translation's OWN body (excluding
its own first line — the stamp itself — for the same self-reference
reason version-stamp.py excludes its own header lines from its hash).

Two distinct signals, not conflated:

1. STALE — the SSOT's current content hash no longer matches `ssot=`
   (the SSOT changed after the translation was stamped). Normal,
   low-stakes: re-translate from the current SSOT and re-stamp.
2. DIVERGED — the translation's own current content hash no longer
   matches `own=` (the translation's body was edited directly since it
   was last stamped, without going through the stamping tool). This is
   the fingerprint of a direct edit landing in the translation (e.g. an
   English contributor's PR) that bypassed the normal "re-translate from
   SSOT, then re-stamp" ritual. Higher-stakes: this content must NOT be
   silently overwritten by blindly re-translating from the SSOT (that
   would discard a real contribution) — a human/AI must reconcile it:
   port the substantive change into the SSOT file, then re-translate
   SSOT -> translation and re-stamp. See
   agent-ops-framework/ko/BLUEPRINT.md section 7 for the full protocol.

Why content-hash, not commit-hash (the actual incident that forced this
redesign, 2026-09-01): the first version of this stamp embedded a git
commit hash and used `git log`/timestamps to compute STALE/DIVERGED. That
design is NOT robust to history rewriting BY CONSTRUCTION — any
squash/rebase/filter-branch/BFG run (and, just as commonly, an everyday
GitHub "Squash and merge" on a PR) orphans every commit that isn't the
rewrite's tip, and any stamp still pointing at one of those old hashes
now references a commit no fresh clone will ever have. This wasn't a
hypothetical: after two squashes in one session, 37 of 44 stamps in this
repo were found pointing at an orphaned commit — and it was invisible
locally for a while, because `git log -1 --format=%ct <hash>` keeps
"succeeding" against a dangling-but-not-yet-garbage-collected commit
object. A first fix added a `git merge-base --is-ancestor` reachability
check plus a `--repair` flag — genuinely useful as a stopgap, but still
reactive: it detects breakage faster, it doesn't stop the breakage from
happening every time history gets rewritten, which for a repo that might
someday take PRs via GitHub's default squash-merge button means *every
single merge*, not a rare maintenance event. Content hashes have no such
failure mode: they don't reference any git object, so no git operation of
any kind — squash, rebase, force-push, even deleting all of history and
starting over — can ever invalidate one. This mirrors the design
`agent-ops-framework-version-check.py` already uses successfully for
ko/'s own **콘텐츠 해시** self-consistency field (see that script's
docstring) — this redesign just extends the same already-proven pattern
to the cross-language sync problem instead of running two different
staleness mechanisms side by side, one robust and one not.

What's lost in the trade (stated honestly, not hidden): a commit hash let
a human run `git show <hash>` to see exactly what the SSOT looked like at
stamp time, and let this script report a precise "X hours staler" figure
from real commit timestamps. A content hash can't do either directly —
this script now makes a **best-effort, git-log-based** attempt at an
approximate "how long ago" figure purely for human-readable reporting
(see `approx_hours_since_content_changed()`), but that lookup is
explicitly allowed to fail (e.g. after a squash makes the exact historical
blob hard to find) without affecting the STALE/DIVERGED boolean at all —
the correctness of the signal itself never depends on git working.

Honest limitation on DIVERGED, unchanged from the previous design: a
content hash proves the translation's body differs from what it was at
last stamp time, not that a re-stamp was done honestly. Someone who edits
the translation AND re-runs `--restamp` in the same breath clears the
DIVERGED signal without any real reconciliation happening — the same gap
as the difference between a checksum and a signature. Treat a
DIVERGED->clean transition as informative, not as proof the underlying
content was ever actually reconciled — when in doubt, diff the
translation against its SSOT by hand rather than trusting the signal
alone.

Usage:
  ./scripts/agent-ops-framework-translation-sync-check.py
  ./scripts/agent-ops-framework-translation-sync-check.py --restamp <translation-relpath>
     (re-stamps ONE translation file with fresh ssot=/own= hashes — run
     this right after actually finishing a translation or re-translation,
     never as a way to silence a DIVERGED signal without reconciling it)
  ./scripts/agent-ops-framework-translation-sync-check.py --restamp-all
     (re-stamps EVERY tracked pair — intended for one-time migration from
     the old commit-hash stamp format, or for bulk-blessing a batch of
     translations you've already confirmed are in sync by hand; it does
     NOT check anything before writing, so never use it as a shortcut to
     make a real DIVERGED/STALE signal disappear without actually
     reconciling the content first)

Exit code: 0 normally. STALE/DIVERGED remain advisory (0) — whether a
signal needs action is a human judgment call (BLUEPRINT.md section 4),
and this hasn't changed. --restamp/--restamp-all also exit 0 on success.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMEWORK_DIR = ROOT
KO_DIR = FRAMEWORK_DIR / "ko"
EN_DIR = FRAMEWORK_DIR / "en"

STAMP_RE = re.compile(
    r"<!--\s*translated-from:\s*ssot=sha256:([0-9a-f]{12})\s+own=sha256:([0-9a-f]{12})\s*-->"
)
# Matches the retired git-commit-hash stamp format, purely to give a
# clear, specific error message when one is found instead of a generic
# "unstamped" — a leftover old-format stamp needs --restamp, not a fresh
# translation from scratch.
OLD_FORMAT_STAMP_RE = re.compile(r"<!--\s*translated-from:\s*[0-9a-f]{7,40}\s*-->")


def sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def ssot_content_hash(path: pathlib.Path) -> str:
    """Content hash of the SSOT file's full text — no line exclusions,
    since the SSOT file doesn't carry a stamp referencing its own hash
    (only the translation does). Deliberately includes the SSOT's own
    **버전**/**콘텐츠 해시** header lines when it has them (most ko/NN
    crystals do): those lines only change when the SSOT's own content
    meaningfully changed (version bumps are reserved for substantive
    changes, per this project's convention), so coupling to them is a
    feature, not noise — a version bump alone is enough to correctly
    flag the translation STALE, even before anyone diffs the prose."""
    return sha12(path.read_text(encoding="utf-8", errors="replace"))


def own_content_hash(path: pathlib.Path) -> str:
    """Content hash of the translation's own body, excluding its own
    first line (the stamp itself) — same self-reference-avoidance
    principle as version-stamp.py excluding its header lines from its
    own hash: a stamp cannot include a hash of itself."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    body = "\n".join(lines[1:]) if lines else text
    return sha12(body)


def approx_hours_since_content_changed(relpath: str) -> float | None:
    """Best-effort, git-log-based estimate of how long ago a path's
    content last changed, for human-readable reporting ONLY — never
    consulted for the STALE/DIVERGED boolean itself, so if this fails
    (missing history, shallow clone, squash having buried the exact
    historical blob) the signal stays correct and this just prints
    "(unknown)" instead of an hours figure."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", relpath],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        if not out:
            return None
        import time

        return (time.time() - int(out)) / 3600
    except Exception:
        return None


def pair_relpaths(en_file: pathlib.Path) -> tuple[str, str]:
    rel = en_file.relative_to(EN_DIR)
    ko_file = KO_DIR / rel
    return (
        ko_file.relative_to(ROOT).as_posix(),
        en_file.relative_to(ROOT).as_posix(),
    )


# Root-level pairs outside the ko//en/ mirrored-folder structure -- so far
# just the top-level landing-page README, which was split into README.md
# (English) / README.ko.md (Korean) rather than living under ko//en/ like
# every other document, since it needs to render as GitHub's default repo
# homepage. pair_relpaths() can't derive this one from a shared relative
# path, so it's listed explicitly instead. Same stamp convention applies:
# whichever file has the `translated-from` comment is the translation.
EXTRA_PAIRS = [
    ("README.md", "README.ko.md"),
]


def restamp(ssot_relpath: str, translation_relpath: str) -> None:
    """Writes a fresh ssot=/own= stamp onto translation_relpath's first
    line, computed against the CURRENT content of both files. Does not
    check anything first — call sites decide when that's appropriate
    (see module docstring's --restamp/--restamp-all usage notes)."""
    ssot_path = ROOT / ssot_relpath
    translation_path = ROOT / translation_relpath
    new_ssot_hash = ssot_content_hash(ssot_path)
    new_own_hash = own_content_hash(translation_path)
    text = translation_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    lines[0] = (
        f"<!-- translated-from: ssot=sha256:{new_ssot_hash} own=sha256:{new_own_hash} -->"
    )
    translation_path.write_text("\n".join(lines), encoding="utf-8")


def process_pair(
    rel_a: str, rel_b: str, buckets: dict, restamp_targets: set | None = None
) -> None:
    """Runs the STALE/DIVERGED check for one (path, path) pair -- order
    doesn't matter, since ownership (which side is the SSOT) is
    determined from which file actually carries the `translated-from`
    stamp, not from argument position. Appends results into the shared
    `buckets` dict so every pair (both the ko//en/ mirrored ones and
    EXTRA_PAIRS) reports through the same STALE/DIVERGED/old_format/
    unstamped/missing_pair/ok accounting. If restamp_targets is given and
    this pair's translation path is in it, restamp() runs instead of
    (not in addition to) the STALE/DIVERGED check."""
    file_a, file_b = ROOT / rel_a, ROOT / rel_b
    text_a = (
        file_a.read_text(encoding="utf-8", errors="replace") if file_a.exists() else ""
    )
    text_b = (
        file_b.read_text(encoding="utf-8", errors="replace") if file_b.exists() else ""
    )
    first_a = text_a.splitlines()[0] if text_a.splitlines() else ""
    first_b = text_b.splitlines()[0] if text_b.splitlines() else ""

    has_a = STAMP_RE.search(first_a)
    has_b = STAMP_RE.search(first_b)
    old_a = OLD_FORMAT_STAMP_RE.search(first_a) if not has_a else None
    old_b = OLD_FORMAT_STAMP_RE.search(first_b) if not has_b else None

    if has_b and not has_a:
        ssot_relpath, translation_relpath, stamp_match = (rel_a, rel_b, has_b)
    elif has_a and not has_b:
        ssot_relpath, translation_relpath, stamp_match = (rel_b, rel_a, has_a)
    elif old_a or old_b:
        # A retired git-commit-hash stamp -- needs --restamp, not silent
        # treatment as "never got a stamp at all" (unstamped), since that
        # would mask that this pair WAS being tracked under the old design.
        translation_relpath = rel_a if old_a else rel_b
        if restamp_targets is not None and translation_relpath in restamp_targets:
            ssot_relpath = rel_b if old_a else rel_a
            restamp(ssot_relpath, translation_relpath)
            buckets["restamped"].append(translation_relpath)
        else:
            buckets["old_format"].append(translation_relpath)
        return
    elif not has_a and not has_b:
        buckets["unstamped"].append(rel_b)
        return
    else:
        # both stamped — ambiguous ownership, needs a human to fix by hand
        buckets["unstamped"].append(f"{rel_b} (both sides stamped — ownership unclear)")
        return

    if not (ROOT / ssot_relpath).exists():
        buckets["missing_pair"].append((translation_relpath, ssot_relpath))
        return

    if restamp_targets is not None and translation_relpath in restamp_targets:
        restamp(ssot_relpath, translation_relpath)
        buckets["restamped"].append(translation_relpath)
        return

    stored_ssot_hash, stored_own_hash = stamp_match.group(1), stamp_match.group(2)
    current_ssot_hash = ssot_content_hash(ROOT / ssot_relpath)
    current_own_hash = own_content_hash(ROOT / translation_relpath)

    is_stale = current_ssot_hash != stored_ssot_hash
    is_diverged = current_own_hash != stored_own_hash

    if is_diverged:
        # DIVERGED takes priority even if SSOT also moved on (is_stale
        # true at the same time) -- checked first, not elif'd after
        # STALE, precisely so a real un-reconciled translation edit is
        # never silently reported as "just STALE, re-translate" (see
        # module docstring: STALE and DIVERGED must not be conflated).
        hours = approx_hours_since_content_changed(translation_relpath)
        buckets["diverged"].append((translation_relpath, ssot_relpath, hours, is_stale))
    elif is_stale:
        hours = approx_hours_since_content_changed(ssot_relpath)
        buckets["stale"].append((translation_relpath, ssot_relpath, hours))
    else:
        buckets["ok"].append(translation_relpath)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = ap.add_mutually_exclusive_group()
    group.add_argument(
        "--restamp",
        metavar="TRANSLATION_RELPATH",
        help="re-stamp one translation file with fresh content hashes (run after actually finishing a translation)",
    )
    group.add_argument(
        "--restamp-all",
        action="store_true",
        help="re-stamp every tracked pair -- for migrating off the old commit-hash format, or bulk-blessing already-confirmed-in-sync content. Checks nothing first.",
    )
    args = ap.parse_args()

    if not EN_DIR.exists():
        print("=== agent-ops-framework-translation-sync-check ===")
        print(
            "\n⚪ agent-ops-framework/en/ not found — no translations yet, nothing to check."
        )
        return 0

    restamp_targets = None
    if args.restamp:
        restamp_targets = {args.restamp}
    elif args.restamp_all:
        restamp_targets = "ALL"  # sentinel: every translation_relpath matches

    class AllSet:
        def __contains__(self, item):
            return True

    if restamp_targets == "ALL":
        restamp_targets = AllSet()

    buckets = {
        "stale": [],
        "diverged": [],
        "old_format": [],
        "restamped": [],
        "unstamped": [],
        "missing_pair": [],
        "ok": [],
    }

    for en_file in sorted(EN_DIR.rglob("*.md")):
        rel_ko, rel_en = pair_relpaths(en_file)
        process_pair(rel_ko, rel_en, buckets, restamp_targets=restamp_targets)

    for rel_a, rel_b in EXTRA_PAIRS:
        if (ROOT / rel_a).exists() or (ROOT / rel_b).exists():
            process_pair(rel_a, rel_b, buckets, restamp_targets=restamp_targets)

    stale, diverged, old_format, restamped = (
        buckets["stale"],
        buckets["diverged"],
        buckets["old_format"],
        buckets["restamped"],
    )
    unstamped, missing_pair, ok = (
        buckets["unstamped"],
        buckets["missing_pair"],
        buckets["ok"],
    )

    print("=== agent-ops-framework-translation-sync-check ===")

    if restamped:
        print(f"\n✅ Restamped {len(restamped)} item(s) with fresh content hashes:")
        for r in restamped:
            print(f"  {r}")

    if old_format:
        print(
            f"\n🔴 OLD FORMAT — {len(old_format)} item(s) still carry the retired "
            "git-commit-hash stamp (see module docstring) — re-run with --restamp "
            "for these specifically once you've confirmed they're actually in sync:"
        )
        for f in old_format:
            print(f"  {f}")

    if stale:
        print(
            f"\n🔴 STALE — {len(stale)} item(s) where the SSOT's content hash no longer "
            "matches the stamp (whether re-translation is needed: check both directly):"
        )
        for translation_relpath, ssot_relpath, hours in stale:
            age = (
                f"{hours:.0f}h ago (approx.)"
                if hours is not None
                else "unknown time ago"
            )
            print(
                f"  {translation_relpath}  <  {ssot_relpath}  (SSOT content changed {age})"
            )

    if diverged:
        print(
            f"\n🟠 DIVERGED — {len(diverged)} item(s) where the translation's own content "
            "no longer matches its stamp (edited directly without re-stamping — do NOT "
            "overwrite by blindly re-translating; a human must judge whether/how to reconcile):"
        )
        for translation_relpath, ssot_relpath, hours, also_stale in diverged:
            age = (
                f"{hours:.0f}h ago (approx.)"
                if hours is not None
                else "an unknown time ago"
            )
            note = (
                " — the SSOT also changed in the meantime (STALE also true)"
                if also_stale
                else ""
            )
            print(
                f"  {translation_relpath}  (content changed {age}, SSOT: {ssot_relpath}){note}"
                " — port this change into the SSOT first, then re-translate and re-stamp"
            )

    if not stale and not diverged and not old_format:
        print(f"\n✅ No STALE, DIVERGED, or old-format items ({len(ok)} checked).")

    if unstamped:
        print(f"\n⚪ {len(unstamped)} item(s) with an undeterminable stamp:")
        for f in unstamped:
            print(f"  {f}")

    if missing_pair:
        print(f"\n⚠️ {len(missing_pair)} item(s) with no counterpart file:")
        for translation_relpath, ssot_relpath in missing_pair:
            print(f"  {translation_relpath} -> {ssot_relpath} not found")

    print(
        "\nNote: STALE and DIVERGED are both only signals — whether something actually"
        " needs reflecting requires opening the diff and judging it. STALE usually just"
        " needs a re-translation, but DIVERGED means a real contribution sits in the"
        " translation that will be lost unless it's ported into the SSOT first — the two"
        " signals are not interchangeable. Both are content-hash based now, so unlike the"
        " retired design, NO git history operation (squash/rebase/force-push) can ever by"
        " itself create a false OLD FORMAT or corrupt these two signals."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
