#!/usr/bin/env python3
"""agent-ops-framework-version-stamp.py — bumps a ko/ crystal's semantic
version and recomputes its content hash.

The original single-integer version (`**버전**: 1`) had two problems: (a)
it couldn't convey the nature of a change (a minor wording fix vs. a
fundamental reversal), and (b) there was no mechanical way to verify
someone had actually bumped it. This combines two axes to fix both:

- **Semantic version** (major.minor.patch) — the axis that needs human/AI
  judgment. Tells a project adopting this crystal "how much does this
  change warrant a re-review."
  - major: the principle itself changed or was reversed (rare)
  - minor: a new mechanism/section was added (the principle stays the
    same, only the scope widened)
  - patch: wording/typo/link fixes (no change in meaning)
- **Content hash** (sha256, over the body) — the axis that needs no
  judgment, 100% mechanically reproducible. Computed **independent of
  this repository's git history**, so even a crystal file copied out of
  this repo entirely (the "porting" scenario in BLUEPRINT.md section 7)
  can be diffed byte-for-byte against the original — this is exactly
  what covers the gap left by the git-commit-hash-based `translated-from`
  stamp, which becomes meaningless once a file leaves this repo.

Hash scope: the entire body excluding the two version/hash header lines
(so the hash never has to reference itself).

Usage:
  ./scripts/agent-ops-framework-version-stamp.py <file> --bump=major|minor|patch
  ./scripts/agent-ops-framework-version-stamp.py <file> --recompute-hash-only
     (leaves the version untouched and only recomputes the hash — useful
     for comparing when a hash doesn't match)

This script never decides what counts as a "substantive change" — the
bump level must always be chosen explicitly by whoever calls it (there
is no default, so as not to create a silent automatic judgment).
"""
import argparse
import hashlib
import pathlib
import re
import sys

VERSION_RE = re.compile(r"^\*\*버전\*\*:\s*(\d+)\.(\d+)\.(\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(
    r"^\*\*콘텐츠 해시\*\*:\s*sha256:([0-9a-f]{12})\s*\(.*\)\s*$", re.MULTILINE
)


def compute_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def strip_header(text: str) -> tuple[list[str], int | None, int | None]:
    """Returns (lines, v_idx, h_idx) — lines is the file split on "\n", and
    v_idx/h_idx are the indices of the **버전**/**콘텐츠 해시** lines
    (None if not found), used both to locate them for replacement and to
    exclude them from the hash input.

    Raises SystemExit if either pattern matches more than once — silently
    keeping "last match wins" would let a second, unrelated line that
    happens to match (e.g. a worked-example header quoted elsewhere in the
    file) get bumped/hashed instead of the real header."""
    lines = text.split("\n")
    v_idx = h_idx = None
    v_count = h_count = 0
    for i, line in enumerate(lines):
        if VERSION_RE.match(line):
            v_idx = i
            v_count += 1
        if HASH_RE.match(line):
            h_idx = i
            h_count += 1
    if v_count > 1 or h_count > 1:
        print(
            f"error: **버전**/**콘텐츠 해시** pattern appears more than once in the file "
            f"(version x{v_count}, hash x{h_count}) — cannot mechanically tell which "
            "line is the real header. Remove the duplicate and retry.",
            file=sys.stderr,
        )
        sys.exit(1)
    return lines, v_idx, h_idx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=pathlib.Path)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--bump", choices=["major", "minor", "patch"])
    group.add_argument("--recompute-hash-only", action="store_true")
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8")
    lines, v_idx, h_idx = strip_header(text)
    if v_idx is None or h_idx is None:
        print(
            f"error: couldn't find **버전**/**콘텐츠 해시** lines in {args.file} — "
            "create the header first.",
            file=sys.stderr,
        )
        return 1

    m = VERSION_RE.match(lines[v_idx])
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))

    if args.bump == "major":
        major, minor, patch = major + 1, 0, 0
    elif args.bump == "minor":
        minor, patch = minor + 1, 0
    elif args.bump == "patch":
        patch += 1

    # body = everything except the two header lines
    body_lines = [l for i, l in enumerate(lines) if i not in (v_idx, h_idx)]
    body = "\n".join(body_lines)
    new_hash = compute_hash(body)

    lines[v_idx] = f"**버전**: {major}.{minor}.{patch}"
    lines[h_idx] = f"**콘텐츠 해시**: sha256:{new_hash} (본문 기준, 이 두 줄 제외)"

    args.file.write_text("\n".join(lines), encoding="utf-8")
    print(f"{args.file}: v{major}.{minor}.{patch}, sha256:{new_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
