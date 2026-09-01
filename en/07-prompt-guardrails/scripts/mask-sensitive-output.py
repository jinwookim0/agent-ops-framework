#!/usr/bin/env python3
"""mask-sensitive-output.py — active masking tool for right before content
goes into a prompt or leaves the system.

`public-repo-check.sh` only **warns** when it finds a sensitive pattern in
a file about to be committed (a person still has to fix it by hand). This
script reuses the same pattern-detection logic but **actually substitutes
(masks)** matches — for cases like external publishing, content about to
be pasted somewhere, or anything else where "this file's content is about
to go straight into a prompt or out of the system" needs an immediate
substitution, not just a warning.

**What this tool does and doesn't do (stated honestly)**:
- Does: actually substitutes the same regex patterns `public-repo-check.sh`
  uses (email addresses, phone numbers, resident registration numbers,
  home-directory paths, secret keys, cloud credentials) to produce a
  masked copy.
- Doesn't: this is not perfect PII detection — being regex-based, it
  misses sensitive information that doesn't match a pattern (e.g. a
  person's name, an address, narrative personal details). It doesn't
  replace a human's final check (the same disclaimer as
  `public-repo-check.sh`).

Usage:
  python3 mask-sensitive-output.py <file>          # masked result to stdout
  python3 mask-sensitive-output.py <file> --out <output path>
  cat file | python3 mask-sensitive-output.py -    # stdin also supported
  python3 mask-sensitive-output.py <file> --report # just a masking summary (counts) to stderr
  python3 mask-sensitive-output.py <file> --check  # prints no content;
                                                    # exits 1 if anything matched (for use in a hook)
"""
import argparse
import re
import sys

# Same detection logic as public-repo-check.sh — to keep one side from
# being fixed while the other is forgotten, always review both files
# together whenever either one changes.
# Order matters (re-ordered 2026-09-01 after a red-team test caught a real
# bug): mask() substitutes patterns in sequence into the same text buffer,
# so if a narrow numeric pattern (phone/RRN) ran first, it could chew up
# just the digit run that happens to sit inside a token/secret string and
# replace it with "[MASKED:...]" — which then broke a later, more specific
# pattern (a cloud token, say) from ever recognizing that string as one
# contiguous token. The observed failure mode: a GitHub PAT with a
# coincidental 10-digit run inside it got partially masked as a "phone
# number", and the surrounding real token characters were left in plaintext
# because the cloud/service-token pattern could no longer match a broken
# string. Fix: substitute the structurally wider, more specific patterns
# (PEM block, cloud token, labeled secret key) first so they claim their
# span before the narrow numeric patterns (phone, RRN) run on what's left.
PATTERNS = [
    ("home directory path", re.compile(r"/(Users|home)/[A-Za-z0-9_.-]+/")),
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    (
        "secret key",
        re.compile(
            r"(api[_-]?key|secret|token|password)[\s]*[:=][\s]*[\"']?[A-Za-z0-9_/+=-]{8,}",
            re.IGNORECASE,
        ),
    ),
    # PEM-format private key block — the highest-impact secret type there is,
    # and the label+separator "secret key" pattern above structurally can't
    # catch it (found in a 2026-09-01 red-team review; DOTALL to match the
    # whole multi-line block).
    (
        "PEM private-key block",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    (
        "cloud/service token",
        re.compile(
            r"(AKIA[0-9A-Z]{16}"  # AWS access key ID
            r"|sk-[A-Za-z0-9]{20,}"  # OpenAI-style
            r"|sk_live_[A-Za-z0-9]{16,}"  # Stripe live secret key
            r"|pk_live_[A-Za-z0-9]{16,}"  # Stripe live publishable key
            r"|gh[pousr]_[A-Za-z0-9]{20,}"  # GitHub PAT (ghp_/gho_/ghu_/ghs_/ghr_)
            r"|xox[baprs]-[A-Za-z0-9-]{10,})"  # Slack token
        ),
    ),
    (
        "phone number",
        re.compile(r"(?<![0-9])01[0-9][-. ]?[0-9]{3,4}[-. ]?[0-9]{4}(?![0-9])"),
    ),
    # Broadened separator (hyphen/dot/space) and added the same
    # digit-boundary guard the phone-number pattern already has — writing
    # the number with a dot or space instead of a hyphen used to slip
    # through entirely (found in a 2026-09-01 red-team review; this is an
    # ordinary formatting variant, not an adversarial bypass). The separator
    # itself stays **required** (not made fully optional) — testing this
    # with a fully-optional separator against the repo's own content
    # produced a real false positive (a 13-digit physics constant literal,
    # the Rydberg constant, in an unrelated file) — the false-positive cost
    # of matching bare 13-digit runs outweighs the extra detection value,
    # so that case is deliberately not covered.
    (
        "resident registration number",
        re.compile(r"(?<![0-9])[0-9]{6}[-. ][1-4][0-9]{6}(?![0-9])"),
    ),
]
# Honest limit (2026-09-01 red team): the patterns above only catch a
# handful of known vendor prefixes — GCP service-account JSON, Azure
# connection strings/SAS tokens, label-free connection-string-style
# credentials (scheme://user:pass@host), and secret labels in a language
# other than English (e.g. a Korean-language variable name) still slip
# through — keeping up with every vendor token format is a losing race,
# so this isn't trying to be an exhaustive list (see the "doesn't do"
# section above).


def mask(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for label, pattern in PATTERNS:
        text, n = pattern.subn(f"[MASKED:{label}]", text)
        if n:
            counts[label] = n
    return text, counts


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("input", help="path to the file to mask, or '-' for stdin")
    ap.add_argument(
        "--out", help="path to write the masked result to (default: stdout)"
    )
    ap.add_argument(
        "--report",
        action="store_true",
        help="print only a masking summary (count per label) to stderr",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="print no content anywhere; exit 1 if any pattern matched "
        "(exit 0 = clean) — for use where content must never be logged, like a hook",
    )
    args = ap.parse_args()

    raw = (
        sys.stdin.read()
        if args.input == "-"
        else open(args.input, encoding="utf-8").read()
    )
    masked, counts = mask(raw)

    if args.check:
        if counts:
            summary = ", ".join(f"{label} x{n}" for label, n in counts.items())
            print(f"⚠️  Found sensitive patterns: {summary}", file=sys.stderr)
            return 1
        return 0

    if counts:
        summary = ", ".join(f"{label} x{n}" for label, n in counts.items())
        print(f"⚠️  Masked: {summary}", file=sys.stderr)
    else:
        print(
            "✅ No patterns to mask found (not perfect detection — doesn't replace a human check).",
            file=sys.stderr,
        )

    if args.report:
        return 0

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(masked)
        print(f"→ saved to {args.out}", file=sys.stderr)
    else:
        print(masked)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
