#!/usr/bin/env bash
# A low-cost scanner that sweeps this repository to check whether it would
# be fine to flip it to public right this moment.
#
# Usage: ./public-repo-check.sh
# Only checks files tracked by git (untracked local-only files are excluded
# since they can't be pushed in the first place).
#
# Perfect detection isn't possible — this is "a safety net that filters out
# obvious mistakes," not the whole of a security audit. A clean result
# doesn't replace a human taking one more look.
#
# This script only warns (a person still has to fix it by hand). If you
# actually need to substitute (mask) content, use mask-sensitive-output.py
# — the two share the same patterns, so review both whenever you change
# either one. For blocking at the source (never letting it be read in the
# first place), see settings.json's permissions.deny.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

FOUND=0
# --cached: files already added to git / --others --exclude-standard: not
# yet added but not excluded by .gitignore either, so they'd be included if
# committed now. In other words, this looks at "every file that would be
# included if you committed right now."
# Captured with -z (NUL-delimited) into a temp file — a plain shell
# variable can't hold embedded NULs, so it has to be a file. mktemp gives
# it an unpredictable path, cleaned up on exit.
FILELIST=$(mktemp)
trap 'rm -f "$FILELIST"' EXIT
git ls-files -z --cached --others --exclude-standard > "$FILELIST"

check() {
  local label="$1" pattern="$2"
  local hits
  # Found in a 2026-09-01 red-team review: this used to pass the file list
  # to xargs as a space-separated string, so a filename containing a space
  # (e.g. "secret file.txt") silently dropped out of scanning via word
  # splitting (reproduced live). xargs -0 against the NUL-delimited list
  # keeps a filename with spaces/newlines as a single argument, always.
  hits=$(xargs -0 grep -InE "$pattern" < "$FILELIST" 2>/dev/null || true)
  # Terminal/ANSI escape-injection defense (found in a 2026-09-01 red-team
  # review): a matched line carries the scanned file's own content
  # verbatim — if an attacker-controlled file contains ESC bytes, this
  # warning itself could be visually tampered with/hidden on screen. Strip
  # C0 control characters other than \t/\n.
  hits=$(printf '%s' "$hits" | LC_ALL=C tr -d '\000-\010\013-\037\177')
  if [ -n "$hits" ]; then
    echo "⚠️  $label"
    echo "$hits" | sed 's/^/    /'
    echo
    FOUND=1
  fi
}

echo "=== public-repo-check: $(date '+%Y-%m-%d') ==="
echo

check "Home directory absolute path (/Users/<name>/ or /home/<name>/)" '/(Users|home)/[A-Za-z0-9_.-]+/'
check "Email address" '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
# Note: a fixed-digit-count numeric pattern like a phone number tends to
# false-positive on partial matches inside longer digit strings — things
# like a SEC EDGAR document ID or a news article ID. Matching without a
# boundary catches those too, inside a string like "0001018724...". To
# only catch a real phone number (an independent token, not flanked by
# other digits), always require a non-digit boundary on both sides (the
# pattern below is a South Korean mobile-number format example — adapt it
# to your own country/format).
check "South Korean mobile number pattern (010-xxxx-xxxx, including space/dot separators)" '(^|[^0-9])01[0-9][-. ]?[0-9]{3,4}[-. ]?[0-9]{4}([^0-9]|$)'
# A separator (hyphen/dot/space) is still required, not made fully
# optional — allowing full omission produced a real false positive against
# this repo's own content (a 13-digit physics constant literal, the
# Rydberg constant, in an unrelated file; 2026-09-01 red-team self-test) —
# the false-positive cost outweighed the extra detection value.
check "Resident registration number pattern (xxxxxx-x......, hyphen/dot/space separator)" '(^|[^0-9])[0-9]{6}[-. ][1-4][0-9]{6}([^0-9]|$)'
check "Common secret-key pattern (api_key/secret/token/password = ...)" '(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*[\"'"'"']?[A-Za-z0-9_/+=-]{8,}'
# PEM private-key block — the highest-impact secret type, and the
# label+separator pattern above structurally can't catch it (found in a
# 2026-09-01 red-team review). The BEGIN marker alone on one line is
# enough signal that a private key is present, so a plain line-based
# grep is sufficient here.
check "PEM private-key block start marker (-----BEGIN ... PRIVATE KEY-----)" '\-\-\-\-\-BEGIN [A-Z ]*PRIVATE KEY\-\-\-\-\-'
check "Cloud/service token pattern (AWS/OpenAI/Stripe/GitHub/Slack)" '(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|sk_live_[A-Za-z0-9]{16,}|pk_live_[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})'
# Honest limit: the above only catches a handful of known vendor
# prefixes — GCP/Azure credentials, connection-string-style credentials
# (scheme://user:pass@host), and secret labels in a language other than
# English still slip through (not trying to be an exhaustive list).

if [ "$FOUND" -eq 0 ]; then
  echo "✅ No unusual patterns found. (Doesn't replace a human taking one more look.)"
  exit 0
else
  echo "Check the items above, and if they're actually sensitive, remove or generalize the value and run this again."
  exit 1
fi
