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

Renamed 2026-09-01 from agent-ops-framework-translation-staleness-check.py
(one-directional only), to support the English-to-Korean contribution
flow a real open-source project needs alongside the Korean-to-English
one. Same detection-only philosophy as every other checker in this
family (BLUEPRINT.md section 4): flags a signal, a human/AI still judges
what to do about it.

Stamp format (first line of a translated file):
  <!-- translated-from: <commit-hash> -->
Whichever file HAS this stamp is the derived translation; whichever file
lacks it is that file's SSOT. Normally ko/NN.md has no stamp and en/NN.md
does (ko is SSOT). A file's ownership CAN be flipped per-file (rare — e.g.
a crystal originated as an English contribution) by moving the stamp onto
the ko/ file instead; this script handles either direction the same way.

Two distinct signals, not conflated:

1. STALE — the SSOT changed after the translation was stamped. Normal,
   low-stakes: re-translate from the current SSOT and re-stamp.
2. DIVERGED — the translation's own body was edited by some commit AFTER
   the commit that last set its current stamp value, without updating
   that stamp. This is the fingerprint of a direct edit landing in the
   translation (e.g. an English contributor's PR) that bypassed the
   normal "re-translate from SSOT, then re-stamp" ritual. Higher-stakes:
   this content must NOT be silently overwritten by blindly re-translating
   from the SSOT (that would discard a real contribution) — a human/AI
   must reconcile it: port the substantive change into the SSOT file,
   then re-translate SSOT -> translation and re-stamp. See
   agent-ops-framework/ko/BLUEPRINT.md section 7 for the full protocol.

Honest limitation on DIVERGED (2026-09-01 red-team review, confirmed by
direct reproduction in an isolated scratch repo): stamp_last_set_ts() only
tracks "when did the stamp *line* last change," not "was that change
actually produced by re-translating from the current SSOT." A commit that
edits *only* the stamp line — re-pointing `translated-from:` at a newer
commit hash without doing any real translation work — resets
stamp_last_set_ts to "now" and silently clears an already-correct DIVERGED
signal, while whatever unreviewed content triggered it in the first place
is left untouched and now invisible to this checker. This is not a
theoretical concern — it was reproduced end to end while auditing this
script. Deliberately not "fixed" by binding the stamp to a content hash
instead of a bare commit hash: that would raise the bar but not close the
gap, since the same untrusted party doing the re-stamping is the one who'd
need to have done the honest re-translation in the first place — so this
is documented as a known limitation of a non-cryptographic, non-signed
stamp rather than treated as a solvable bug. Treat a DIVERGED->clean
transition as informative, not as proof the underlying content was ever
actually reconciled — when in doubt, diff the translation against its SSOT
by hand rather than trusting the signal alone.

BROKEN STAMP — a third signal, distinct from STALE/DIVERGED (added
2026-09-01 after a real incident): a `translated-from` hash is only
meaningful if it points at a commit actually reachable from the current
history. History-rewriting operations (squash, rebase, filter-branch,
BFG) orphan every commit that isn't the tip of the rewrite — any stamp
still pointing at one of those old hashes is now referencing a commit
that no fresh clone of this repo will ever have. This class of bug is
dangerous specifically because it degrades **silently**: `git log -1
--format=%ct <hash>` keeps "succeeding" (returning a plausible-looking
timestamp) for a dangling-but-not-yet-garbage-collected commit object,
so nothing looked wrong locally until the object was actually pruned —
by which point the failure surfaces as a vague "commit lookup failed"
with no indication *why*, long after the squash that caused it. Concretely:
after two squashes in one session, 37 of this repo's 44 translation
stamps were found pointing at a commit (`f50ae882...`, an orphaned
"Initial public release" from a superseded squash) that `git
merge-base --is-ancestor <hash> HEAD` correctly reports is NOT an
ancestor of HEAD, despite `git log` on the same hash still "working."
This checker now verifies reachability explicitly (`is_reachable()`)
instead of trusting a successful `git log` call, and reports any broken
stamp as its own loud, separate bucket rather than folding it into
STALE/DIVERGED (whose timestamp math is meaningless against a stamp
target that isn't real history) or into the quieter "unstamped" bucket
(which reads as "never got a stamp," not "the stamp is now lying").
Run with `--repair` to fix every broken stamp mechanically: each one is
re-pointed at its SSOT file's own actual last-touch commit (verified
reachable by construction, since it's read from `git log` on HEAD's own
history) — see `repair_stamp()`. **Operational rule this incident
established**: any time this repo's history is rewritten (squash/
rebase), immediately run `--repair` as a follow-up commit before doing
anything else — never assume existing stamps survived the rewrite.

Usage:
  ./scripts/agent-ops-framework-translation-sync-check.py
  ./scripts/agent-ops-framework-translation-sync-check.py --repair
     (rewrites every broken stamp's `translated-from` hash to its SSOT
     file's real last-touch commit; run the plain form again afterward
     to see the resulting STALE/DIVERGED picture — --repair only fixes
     broken stamps, it does not also recompute STALE/DIVERGED in the
     same pass)

Exit code: always 0 (advisory report).
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMEWORK_DIR = ROOT
KO_DIR = FRAMEWORK_DIR / "ko"
EN_DIR = FRAMEWORK_DIR / "en"

STAMP_RE = re.compile(r"<!--\s*translated-from:\s*([0-9a-f]{7,40})\s*-->")
STAMP_LINE_PATTERN = r"translated-from: [0-9a-f]{7,40}"


def commit_ts(rev: str) -> int | None:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", rev],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def last_touch_ts(relpath: str) -> int | None:
    """Timestamp of the most recent commit that touched this path at all."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def last_touch_hash(relpath: str) -> str | None:
    """Hash of the most recent commit that touched this path — always
    reachable by construction, since it comes from `git log` walking
    HEAD's own history rather than from a stored, possibly-stale stamp.
    This is what repair_stamp() re-points a broken translated-from stamp
    at."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return out or None


def is_reachable(rev: str) -> bool:
    """True iff `rev` is an ancestor of (or equal to) HEAD — i.e. actually
    part of the history a fresh clone would have. Deliberately NOT the
    same check as "does `git log -1 <rev>` succeed": a commit orphaned by
    a squash/rebase keeps satisfying that weaker check for as long as the
    loose object survives locally (see module docstring's BROKEN STAMP
    section) — `git merge-base --is-ancestor` is the check that actually
    distinguishes real history from a not-yet-garbage-collected leftover."""
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", rev, "HEAD"],
            cwd=ROOT,
            capture_output=True,
        ).returncode
        == 0
    )


def repair_stamp(translation_relpath: str, old_hash: str, new_hash: str) -> None:
    """Rewrites the translated-from line in translation_relpath from
    old_hash to new_hash, touching nothing else in the file (same
    surgical approach as version-stamp.py's header rewriting — replace
    the exact matched line, leave every other byte untouched)."""
    path = ROOT / translation_relpath
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    lines[0] = lines[0].replace(old_hash, new_hash)
    path.write_text("\n".join(lines), encoding="utf-8")


def stamp_last_set_ts(relpath: str) -> int | None:
    """Timestamp of the most recent commit that changed the stamp line's
    VALUE (added/removed a line matching the pattern) — not just any commit
    that touched the file. Uses -G (diff-content regex search), not -S,
    because the string "translated-from:" itself never changes — only the
    hash after it does, which -S's occurrence-count logic would miss."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "-G", STAMP_LINE_PATTERN, "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


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


def process_pair(rel_a: str, rel_b: str, buckets: dict, repair: bool = False) -> None:
    """Runs the STALE/DIVERGED check for one (path, path) pair -- order
    doesn't matter, since ownership (which side is the SSOT) is determined
    from which file actually carries the `translated-from` stamp, not from
    argument position. Appends results into the shared `buckets` dict so
    every pair (both the ko//en/ mirrored ones and EXTRA_PAIRS) reports
    through the same STALE/DIVERGED/broken_stamp/unstamped/missing_pair/ok
    accounting. When repair=True, a broken stamp is rewritten in place
    instead of only being reported (see repair_stamp())."""
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

    if has_b and not has_a:
        ssot_relpath, translation_relpath, stamp_match = (rel_a, rel_b, has_b)
    elif has_a and not has_b:
        ssot_relpath, translation_relpath, stamp_match = (rel_b, rel_a, has_a)
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

    old_hash = stamp_match.group(1)
    if not is_reachable(old_hash):
        if repair:
            new_hash = last_touch_hash(ssot_relpath)
            if new_hash is None:
                buckets["broken_stamp"].append((translation_relpath, old_hash, None))
                return
            repair_stamp(translation_relpath, old_hash, new_hash)
            buckets["broken_stamp"].append((translation_relpath, old_hash, new_hash))
        else:
            buckets["broken_stamp"].append((translation_relpath, old_hash, None))
        # Not falling through to STALE/DIVERGED below: their timestamp math
        # is meaningless against a stamp target that isn't real history —
        # re-run this script (without --repair) after repairing to get a
        # trustworthy STALE/DIVERGED read on this pair.
        return

    ssot_ts = last_touch_ts(ssot_relpath)
    translation_ts = last_touch_ts(translation_relpath)
    stamp_target_ts = commit_ts(stamp_match.group(1))
    stamp_set_ts = stamp_last_set_ts(translation_relpath)

    if (
        ssot_ts is None
        or translation_ts is None
        or stamp_target_ts is None
        or stamp_set_ts is None
    ):
        buckets["unstamped"].append(translation_relpath + " (commit lookup failed)")
        return

    is_stale = ssot_ts > stamp_target_ts
    is_diverged = translation_ts > stamp_set_ts

    if is_diverged:
        # DIVERGED takes priority even if SSOT also moved on (is_stale
        # true at the same time) -- checked first, not elif'd after
        # STALE, precisely so a real un-reconciled translation edit is
        # never silently reported as "just STALE, re-translate" (see
        # module docstring: STALE and DIVERGED must not be conflated).
        hours = (translation_ts - stamp_set_ts) / 3600
        buckets["diverged"].append((translation_relpath, ssot_relpath, hours, is_stale))
    elif is_stale:
        hours = (ssot_ts - stamp_target_ts) / 3600
        buckets["stale"].append((translation_relpath, ssot_relpath, hours))
    else:
        buckets["ok"].append(translation_relpath)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--repair",
        action="store_true",
        help="rewrite every broken (unreachable) translated-from stamp to point at its SSOT file's real last-touch commit",
    )
    args = ap.parse_args()

    if not EN_DIR.exists():
        print("=== agent-ops-framework-translation-sync-check ===")
        print(
            "\n⚪ agent-ops-framework/en/ not found — no translations yet, nothing to check."
        )
        return 0

    buckets = {
        "stale": [],
        "diverged": [],
        "broken_stamp": [],
        "unstamped": [],
        "missing_pair": [],
        "ok": [],
    }

    for en_file in sorted(EN_DIR.rglob("*.md")):
        rel_ko, rel_en = pair_relpaths(en_file)
        process_pair(rel_ko, rel_en, buckets, repair=args.repair)

    for rel_a, rel_b in EXTRA_PAIRS:
        if (ROOT / rel_a).exists() or (ROOT / rel_b).exists():
            process_pair(rel_a, rel_b, buckets, repair=args.repair)

    stale, diverged, broken_stamp = (
        buckets["stale"],
        buckets["diverged"],
        buckets["broken_stamp"],
    )
    unstamped, missing_pair, ok = (
        buckets["unstamped"],
        buckets["missing_pair"],
        buckets["ok"],
    )

    print("=== agent-ops-framework-translation-sync-check ===")

    if broken_stamp:
        verb = "Repaired" if args.repair else "Found"
        print(
            f"\n🔴 BROKEN STAMP — {verb} {len(broken_stamp)} item(s) whose translated-from hash "
            "is NOT reachable from HEAD (almost certainly orphaned by a squash/rebase — see "
            "this script's module docstring's 'BROKEN STAMP' section):"
        )
        for translation_relpath, old_hash, new_hash in broken_stamp:
            if new_hash:
                print(
                    f"  {translation_relpath}: {old_hash[:12]} -> {new_hash[:12]} (repaired)"
                )
            else:
                print(
                    f"  {translation_relpath}: {old_hash[:12]} (unreachable — re-run with --repair, or investigate manually if that fails)"
                )
        if not args.repair:
            print("  -> run with --repair to fix these automatically.")

    if stale:
        print(
            f"\n🔴 STALE — {len(stale)} item(s) where the SSOT changed more recently than "
            "the translation (whether re-translation is needed: check both directly):"
        )
        for translation_relpath, ssot_relpath, hours in stale:
            print(
                f"  {translation_relpath}  <  {ssot_relpath}  (SSOT is {hours:.0f}h more recent)"
            )

    if diverged:
        print(
            f"\n🟠 DIVERGED — {len(diverged)} item(s) where the translation was edited "
            "directly without re-stamping (do NOT overwrite by blindly re-translating — "
            "a human must judge whether/how to reconcile):"
        )
        for translation_relpath, ssot_relpath, hours, also_stale in diverged:
            note = (
                " — the SSOT also changed in the meantime (STALE also true)"
                if also_stale
                else ""
            )
            print(
                f"  {translation_relpath}  (edited directly {hours:.0f}h after its stamp was set, "
                f"SSOT: {ssot_relpath}){note} — port this change into the SSOT first, then re-translate and re-stamp"
            )

    if not stale and not diverged:
        print(f"\n✅ No STALE or DIVERGED items ({len(ok)} checked).")

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
        " signals are not interchangeable."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
