#!/usr/bin/env python3
"""agent-ops-framework-version-check.py — verifies each ko/ crystal's
stored content hash still matches its actual content, with no git history
required at all.

Originally detected staleness via `git -G` (diff-content search) for
"has the file changed since the version line last changed" — this worked,
but depended on this repository's own git history. Switched to embedding
a **content hash** (sha256, over the body) directly in each crystal's
header instead — this script now uses no git at all: it just compares
the stored hash against a fresh hash of the current body. **A project
that copies a crystal file out of this repo entirely can run this same
script against its own copy** — no git history is needed, which is
exactly the "porting" scenario BLUEPRINT.md section 7 describes.

A hash mismatch means the body changed without the header's version
number being bumped (someone forgot to bump it, or edited the file
directly without going through the stamping script). This is only a
signal — whether the change is substantive enough to warrant a version
bump is still a human/AI judgment call (detection is automatic, judgment
is human — the same principle as BLUEPRINT.md section 4). Use
agent-ops-framework-version-stamp.py to actually bump the version.

**Honest limit — this is a self-consistency check, not a tamper-proofing
mechanism**: this hash only catches "the body changed but the header's
hash/version was left alone." Someone who **deliberately** changes the
content and then re-runs agent-ops-framework-version-stamp.py to
recompute a matching hash passes this check cleanly — both the hash
algorithm and the stamping tool that computes it are public in this repo,
so anyone can regenerate a "correct" hash without any secret (the same
gap as the difference between a checksum and a signature — this hash
carries none of the "who approved this and why" a signature would
prove). So "hash matches = OK" means "the stamping procedure was followed
without forgetting to bump the version," not "this change was reviewed
and approved" — actual review is still a human/AI's job.

Usage:
  ./scripts/agent-ops-framework-version-check.py

Exit code: always 0 (advisory report).
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KO_DIR = ROOT / "ko"

# These two patterns match the literal Korean header fields every crystal
# actually carries (e.g. "**버전**: 1.0.0") — this is the real file format,
# not diagnostic output, so it stays Korean regardless of what language
# this script's own comments/messages use.
VERSION_RE = re.compile(r"^\*\*버전\*\*:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(
    r"^\*\*콘텐츠 해시\*\*:\s*sha256:([0-9a-f]{12})\s*\(.*\)\s*$", re.MULTILINE
)

EXCLUDE = {
    "README.md",
    "BLUEPRINT.md",
    "USAGE-GUIDE.md",
    "DISCLAIMER.md",
    "LANGUAGE-POLICY.md",
    "RISK-ANALYSIS.md",
    "REFLECTION-CANDIDATES.md",
    "GLOSSARY.md",
}


def check_file(relpath: str, f: pathlib.Path):
    text = f.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    v_idx = h_idx = None
    for i, line in enumerate(lines):
        if VERSION_RE.match(line):
            v_idx = i
        if HASH_RE.match(line):
            h_idx = i
    if v_idx is None or h_idx is None:
        return ("unmarked", relpath, None)

    stored_hash = HASH_RE.match(lines[h_idx]).group(1)
    version = VERSION_RE.match(lines[v_idx]).group(1)
    body = "\n".join(l for i, l in enumerate(lines) if i not in (v_idx, h_idx))
    computed_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]

    if computed_hash != stored_hash:
        return ("mismatch", relpath, (version, stored_hash, computed_hash))

    # Found during a red-team audit: BLUEPRINT.md requires that "a crystal
    # without a verification-strength label cannot exist," but 8 crystals
    # actually had no 🟢/🟡 anywhere in their body (the rating existed only
    # in README.md's roll-up table) — a gap where that information vanishes
    # entirely once the file is copied out on its own. Catch this
    # mechanically instead of relying on someone noticing by eye each time.
    # ⚪ is not a valid verification-strength grade (BLUEPRINT.md section 1 —
    # only 🟢/🟡 count) — it's used elsewhere in crystal bodies as a
    # separate "needs checking / unverified" marker, so accepting it here
    # would let a crystal with no real 🟢/🟡 pass this check just because an
    # unrelated ⚪ happens to appear somewhere in its body.
    if not ("🟢" in body or "🟡" in body):
        return ("no_badge", relpath, version)
    return ("ok", relpath, version)


def main() -> int:
    targets = []
    for f in sorted(KO_DIR.glob("*.md")):
        if f.name in EXCLUDE:
            continue
        targets.append((f.relative_to(ROOT).as_posix(), f))
    # Find every crystal that ships with code (an `NN-name/README.md`
    # subdirectory — currently just 07-prompt-guardrails/). This used to
    # hardcode the "07-prompt-guardrails" path, which meant a future crystal
    # subdirectory following the same pattern would silently be skipped
    # unless someone remembered to add another hardcoded line here — exactly
    # the "fix one copy, forget its sibling" failure mode the guardrails
    # README itself warns about.
    for subdir_readme in sorted(KO_DIR.glob("[0-9][0-9]-*/README.md")):
        targets.append((subdir_readme.relative_to(ROOT).as_posix(), subdir_readme))

    mismatches, unmarked, no_badge, ok = [], [], [], []
    for relpath, f in targets:
        status, rel, detail = check_file(relpath, f)
        if status == "mismatch":
            mismatches.append((rel, detail))
        elif status == "unmarked":
            unmarked.append(rel)
        elif status == "no_badge":
            no_badge.append(rel)
        else:
            ok.append((rel, detail))

    print("=== agent-ops-framework-version-check ===")
    if mismatches:
        print(
            f"\n🟡 {len(mismatches)} item(s) whose stored hash doesn't match their "
            "actual content (the body changed without bumping the version — "
            "if this is a substantive change, bump it with version-stamp.py):"
        )
        for rel, (version, stored, computed) in mismatches:
            print(
                f"  {rel}  (header says v{version}/sha256:{stored}, actual body hashes to sha256:{computed})"
            )
    else:
        print(f"\n✅ Every stored hash matches its actual content ({len(ok)} checked).")

    if unmarked:
        print(f"\n⚪ {len(unmarked)} item(s) with no version/hash header:")
        for u in unmarked:
            print(f"  {u}")

    if no_badge:
        print(
            f"\n🔴 {len(no_badge)} item(s) with no verification-strength (🟢/🟡/⚪) mark "
            "anywhere in the body (violates BLUEPRINT.md section 1 — a rating that only "
            "lives in README.md's roll-up table disappears the moment the file is copied out on its own):"
        )
        for rel in no_badge:
            print(f"  {rel}")

    print(
        "\nNote: a hash mismatch is verified 100% mechanically, independent of"
        " git history — this works the same way even for a single crystal file"
        " copied out into another project. Whether the change is substantive"
        " enough to warrant a version bump is still a human/AI judgment call"
        " (for something as small as a typo fix, just re-stamping is fine)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
