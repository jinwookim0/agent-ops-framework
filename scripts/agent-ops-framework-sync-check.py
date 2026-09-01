#!/usr/bin/env python3
"""agent-ops-framework-sync-check.py — checks whether the origin document a
crystal was extracted from has changed more recently than the crystal
itself.

The problem this solves: a purely candidate-based scanner (see
agent-ops-framework-reflection-check.py) only catches *new* entries in a
directive/change-history log — it doesn't re-check an existing crystal
when its own origin document is edited afterward. This script closes
that gap by comparing each crystal's last-touched commit against its
mapped origin document's.

**What this script does NOT do (stated honestly)**: "the origin document
changed more recently than the crystal" is a signal, not a conclusion
that "the crystal must be updated." An append-only log-style origin
document (e.g. a directive registry) can keep growing without the
*pattern* a crystal already extracted from it ever changing — new rows
accumulate, but the underlying policy stays the same. Separating
detection (automatic) from "does this actually need updating" judgment
(human/AI) is the same principle this folder already applies elsewhere
(BLUEPRINT.md section 4).

Usage:
  ./scripts/agent-ops-framework-sync-check.py

Exit code: always 0 (advisory report).
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Crystal number -> (origin document, note on how it maps).
# This repository *is* agent-ops-framework itself, published as a
# standalone public repo — there's no separate "origin project document" a
# crystal was pulled out of here (the crystal file already is the final
# form of the content). This map exists for when a project **adopts** this
# folder into itself (BLUEPRINT.md section 7): after porting, that project
# fills this back in with its own origin-document paths, adding one
# "crystal filename": "origin document path within that project" line
# each time it extracts a new crystal.
ORIGIN_MAP = {}

CRYSTAL_DIR = ROOT / "ko"


def last_commit_ts(relpath: str) -> int | None:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", relpath],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out) if out else None


def main() -> int:
    stale = []
    skipped = []
    for crystal_name, origin_relpath in sorted(ORIGIN_MAP.items()):
        crystal_relpath = f"agent-ops-framework/ko/{crystal_name}"
        if not (ROOT / crystal_relpath).exists():
            skipped.append((crystal_relpath, "crystal file not found"))
            continue
        if not (ROOT / origin_relpath).exists():
            skipped.append((crystal_relpath, f"origin {origin_relpath} not found"))
            continue
        o_ts = last_commit_ts(origin_relpath)
        c_ts = last_commit_ts(crystal_relpath)
        if o_ts is None or c_ts is None:
            skipped.append((crystal_relpath, "no git history"))
            continue
        if o_ts > c_ts:
            hours = (o_ts - c_ts) / 3600
            stale.append((crystal_relpath, origin_relpath, hours))

    print("=== agent-ops-framework-sync-check ===")
    if stale:
        print(
            f"\n🔴 {len(stale)} item(s) whose origin changed more recently than the "
            "crystal (whether it needs updating is a judgment call — open both and check):"
        )
        for crystal_relpath, origin_relpath, hours in stale:
            print(
                f"  {crystal_relpath}  <  {origin_relpath}  (origin is {hours:.0f}h more recent)"
            )
    else:
        print("\n✅ No crystal is older than its origin.")

    if skipped:
        print(f"\n⚪ {len(skipped)} item(s) skipped:")
        for path, reason in skipped:
            print(f"  {path}: {reason}")

    print(
        "\nNote: 'origin is more recent' is only a signal. An append-only log-style"
        " origin (e.g. a directive registry) can keep growing without the pattern"
        " already extracted from it ever changing — whether it actually needs"
        " reflecting is a judgment call, not an automatic conclusion."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
