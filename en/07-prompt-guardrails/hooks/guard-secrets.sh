#!/usr/bin/env bash
# PreToolUse hook — actually blocks password/API-key-style sensitive
# patterns right before an Artifact/external-publish tool call, and right
# before a git commit/push.
#
# Why a hook is needed at all: a warn-only scanner or an active-masking
# script has a real limitation — it only works if a person (or the AI)
# remembers to run it. A hook intercepts the tool call itself
# automatically, so "forgot to run it" structurally can't happen anymore.
#
# What this hook blocks: the file_path content right before a publish tool
# (Artifact, etc.), and the entire set of files about to be committed right
# before git commit/push (reuses public-repo-check.sh). Both cases block
# the tool call itself with exit 2 — stderr becomes the block reason the
# agent sees.
#
# What this hook does NOT block (stated honestly): text a person pastes
# directly into chat, or content that only prints to the screen via Bash
# output and never becomes a file/commit/publish — these never cross a
# tool-call boundary, so this hook can't see them. Not a perfect defense —
# it's the last checkpoint at the point content actually leaves the system.
#
# A narrower limit within the Bash path itself (found in a 2026-09-01
# red-team review — a different kind of limit than the paragraph above, so
# called out separately): even under the Bash matcher, all this hook
# actually checks is whether the command *string* contains the literal
# substring "git commit"/"git push" (see the grep -qE below). That cuts
# both ways:
#   - Under-detection (bypass): a git alias, a wrapper script/function, or
#     any non-git exfiltration path within the same Bash tool boundary
#     (curl, scp, aws s3 cp, gh release upload, npm publish, docker push,
#     ...) is invisible to this hook — "inside the tool-call boundary"
#     does NOT mean "this hook sees everything in it"; it only recognizes
#     one specific command shape.
#   - Over-detection (false positive): conversely, a command that never
#     actually runs git commit/push at all can still trip this hook if
#     that literal substring merely appears as text inside it (e.g. a
#     grep search for the words "git commit", or an echo/comment
#     containing that phrase) — this happened for real during this very
#     audit, where an unrelated grep call got blocked by the
#     confidential-paths check downstream (reproduced live). Both
#     directions come from the same root cause: literal substring
#     matching, not actually parsing/understanding the command — this
#     can't be fully eliminated, so treat this hook as a safety net for
#     the narrow git-commit/push case specifically, not as general
#     coverage of every way Bash could leak content.
#
# When porting: change the matcher name ("Artifact") to whatever publish/
# deploy tool this project actually uses. If there are several, either
# pipe-list the matchers in settings.json or register multiple hooks.

set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}"

INPUT=$(cat)

block() {
  echo "🚫 guard-secrets hook: $1" >&2
  exit 2
}

# Fix from a 2026-09-01 red-team review: if the JSON parse itself failed
# (malformed input, etc.), TOOL_NAME used to silently become an empty
# string and, since the case below has no wildcard branch, the tool call
# would just pass through (fail-open) — at a security checkpoint, a parse
# failure must not be treated the same as "this tool legitimately isn't
# Artifact/Bash" (which should pass through, as before). Only an actual
# parse failure is blocked explicitly (fail-closed); a successful parse
# whose tool_name is simply absent/different still passes through as before.
if ! TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null); then
  block "Could not parse hook input as JSON — blocking this tool call for safety."
fi

case "$TOOL_NAME" in
  Artifact)
    FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
    if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
      # Created at an unpredictable path via mktemp (found in a 2026-09-01
      # red-team review: this used to write to a PID-predictable path in a
      # world-writable directory, /tmp/guard-secrets-artifact.$$ — a
      # symlink-preemption setup on a shared multi-user host).
      ARTIFACT_ERR=$(mktemp)
      if ! python3 scripts/mask-sensitive-output.py "$FILE_PATH" --check 2>"$ARTIFACT_ERR"; then
        REASON=$(cat "$ARTIFACT_ERR"); rm -f "$ARTIFACT_ERR"
        block "Found a sensitive pattern in the publish target ($FILE_PATH) — $REASON — check directly with scripts/mask-sensitive-output.py and try again."
      fi
      rm -f "$ARTIFACT_ERR"
    fi
    ;;
  Bash)
    COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
    if echo "$COMMAND" | grep -qE '\bgit\s+(commit|push)\b'; then
      GIT_CHECK_OUT=$(mktemp)
      if ! bash scripts/public-repo-check.sh >"$GIT_CHECK_OUT" 2>&1; then
        REASON=$(cat "$GIT_CHECK_OUT"); rm -f "$GIT_CHECK_OUT"
        block "public-repo-check.sh found a sensitive pattern right before git commit/push:
$REASON
Fix the file or drop it from staging, then try again."
      fi
      rm -f "$GIT_CHECK_OUT"
    fi
    ;;
esac

exit 0
