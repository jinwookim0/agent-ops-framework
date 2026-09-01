#!/usr/bin/env bash
# Native git pre-push hook — fires even when a human runs `git push`
# directly in a terminal, without going through Claude Code at all
# (guard-secrets.sh is a PreToolUse hook that only intercepts Claude
# Code's own Bash tool calls, so anything outside that boundary is
# invisible to it — this hook covers that remaining gap, one more point
# at "the moment it actually leaves for the remote." A fourth layer on
# top of the 3-layer defense in README.md's "Why 4 layers").
#
# Two different things this hook blocks, checked separately because
# they come from different reasons:
# 1. **The content of the files being committed**: reuses
#    `public-repo-check.sh` as-is (the same patterns are not copied here
#    a second time — checking file content is already that script's job;
#    this hook just calls it again at a new point in time, "right before
#    push").
# 2. **The messages of the commits being pushed right now**: a different
#    channel from file content, so it needs its own check — e.g. a
#    session link or a local absolute path can end up in a commit
#    message body without ever appearing in any tracked file.
#
# Installing this (when porting this folder into a project):
#   git config core.hooksPath .githooks
#   (symlink or copy .githooks/pre-push to point at this file)
# `.git/hooks/` itself isn't version-controlled by git, so every clone
# has to set this up separately — pointing `core.hooksPath` at a
# version-controlled directory instead means nobody has to remember to
# copy the file by hand (removing the "forgot to install it" failure
# mode entirely).
#
# Honest limitation: this hook, too, only works through `core.hooksPath`
# — if that one git config command is never run on a fresh clone, this
# hook silently does nothing (the same lesson this folder repeats
# elsewhere: a documented rule is powerless the moment someone forgets
# to run it). `--no-verify` can also always skip this hook entirely —
# it's a safety net, not an enforced wall.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

ZERO_SHA="0000000000000000000000000000000000000000"
BLOCK=0

# Commit-message-only patterns — deliberately not merged with the
# file-content patterns (public-repo-check.sh already owns those); kept
# to the minimum that actually caused a real problem in commit messages.
#
# False positive found live, 2026-09-02: the very commit that added this
# hook got blocked by its own check, because its message explained the
# hook ("this hook catches 'Claude-Session:'") by quoting the string
# itself -- not an actual leak, caught on the first real push. A real
# trailer is always followed by the URL, so require that shape too, to
# tell "a sentence describing the pattern" apart from "an actual leak."
check_message() {
  local sha="$1" msg hits
  msg=$(git log -1 --format=%B "$sha")
  hits=$(printf '%s' "$msg" | grep -inE 'claude-session:\s*https://claude\.ai/code/session_|/(Users|home)/[A-Za-z0-9_.-]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----' || true)
  if [ -n "$hits" ]; then
    echo "🚫 Commit $sha's message has a banned pattern:"
    echo "$hits" | sed 's/^/    /'
    BLOCK=1
  fi
}

# git's pre-push hook stdin format: "local-ref local-sha remote-ref remote-sha"
while read -r local_ref local_sha remote_ref remote_sha; do
  [ "$local_sha" = "$ZERO_SHA" ] && continue # deleting a ref — nothing to check
  if [ "$remote_sha" = "$ZERO_SHA" ]; then
    range="$local_sha" # first push of a new branch — check its whole history
  else
    range="$remote_sha..$local_sha"
  fi
  for sha in $(git rev-list "$range" -- 2>/dev/null); do
    check_message "$sha"
  done
done

if [ "$BLOCK" -eq 1 ]; then
  echo "" >&2
  echo "Fix the commit message(s) above (e.g. git filter-branch --msg-filter," >&2
  echo "or git commit --amend if it's a recent commit not yet on origin)," >&2
  echo "then push again." >&2
  exit 1
fi

# File-content checking reuses the existing script — not copied here a
# second time. public-repo-check.sh looks at "every file that would be
# included if committed right now," so re-running it at push time checks
# effectively the same state that's about to be pushed.
#
# Why two candidate paths: a project this folder was ported into keeps
# this script at `scripts/public-repo-check.sh` per the install
# instructions, but the origin repo that authored this crystal
# (agent-ops-framework) itself keeps it in place under
# `ko/07-prompt-guardrails/` — support both layouts.
if [ -f scripts/public-repo-check.sh ]; then
  CHECK_SCRIPT=scripts/public-repo-check.sh
else
  CHECK_SCRIPT=ko/07-prompt-guardrails/scripts/public-repo-check.sh
fi
if ! bash "$CHECK_SCRIPT"; then
  echo "" >&2
  echo "public-repo-check.sh found the items above — blocking the push." >&2
  exit 1
fi

exit 0
