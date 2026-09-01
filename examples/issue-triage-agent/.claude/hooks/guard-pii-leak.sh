#!/usr/bin/env bash
# PreToolUse hook — blocks a PostTicketComment/ApplyTicketLabel call
# outright if its content still contains a reporter's raw email/phone
# number. Adapted from ko/07-prompt-guardrails/hooks/guard-secrets.sh:
# same 3-layer-defense mechanism (JSON-parse the hook input, fail-closed
# on a parse failure, exit 2 to actually block the tool call rather than
# just warn), applied to a different leak — this project has no secrets
# to worry about (no API keys ever pass through it), but a ticket
# reporter's contact info pasted into a bug report is exactly the kind of
# "looks like normal content, isn't a pattern-matchable secret format"
# leak crystal 07's own README says regex-based guardrails cannot catch
# for secrets, but email/phone shapes ARE regex-matchable — this hook is
# what covers that different, narrower risk for this project specifically
# (see ../../CASE-STUDY.md's crystal-07 section for why this is an
# adaptation, not a verbatim copy).
#
# What this hook does NOT catch (stated honestly, same spirit as
# guard-secrets.sh's own limits section): an email written with the "at"
# spelled out, or a phone number embedded in an image/attachment
# reference, will not match EMAIL_RE/PHONE_RE in triage.py and will pass
# through uncaught — this is the same fundamental regex-detection limit
# guard-secrets.sh documents for secrets, inherited here for PII shapes.
#
# Reuses triage.py's redact_pii() directly (import, not a second copy of
# the regex) — ko/07-prompt-guardrails/README.md's own "확장하는 법"
# section warns that two independently-maintained copies of the same
# detection list is exactly how this kind of guardrail rots.

set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}"

INPUT=$(cat)

block() {
  echo "🚫 guard-pii-leak hook: $1" >&2
  exit 2
}

if ! TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null); then
  block "couldn't parse hook input as JSON — blocking this tool call to be safe (fail-closed)."
fi

case "$TOOL_NAME" in
  PostTicketComment|ApplyTicketLabel)
    CONTENT=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('tool_input',{}); print(d.get('comment_text') or d.get('label_text') or '')" 2>/dev/null)
    if [ -n "$CONTENT" ]; then
      CHECK_OUT=$(mktemp)
      python3 -c "
import sys
sys.path.insert(0, 'skills/triage-incoming-issue')
from triage import redact_pii
content = sys.stdin.read()
redacted = redact_pii(content)
if redacted != content:
    print('raw email/phone-shaped text found in outbound content', file=sys.stderr)
    sys.exit(1)
" <<<"$CONTENT" 2>"$CHECK_OUT"
      if [ $? -ne 0 ]; then
        REASON=$(cat "$CHECK_OUT"); rm -f "$CHECK_OUT"
        block "outbound $TOOL_NAME call contains unredacted contact info — $REASON — call redact_pii() on the content first, or confirm this is intentional and route through a human instead."
      fi
      rm -f "$CHECK_OUT"
    fi
    ;;
esac

exit 0
