<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Project-Level Confidentiality Protection — What Pattern-Based Secret Detection Can't Catch

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/23-confidential-project-protection.md)**

**Version**: 1.0.0
**Content hash**: sha256:4461c04da6b8 (of the body below, excluding the stamp comment, this line, and the version line)

🟢 **Verification strength**: extracted from the original project's actual
operational history, confirmed live-blocking an actual `git push` attempt.

## Why it's needed

The three-tier guardrail in [07-prompt-guardrails/](07-prompt-guardrails/)
blocks sensitive information that's **identifiable by pattern** — emails,
API keys, passwords. But there are cases with zero personal-data patterns
present (even when only fictional data is used) where **the business plan
or implementation itself must not be exposed** — for example, a product
concept not yet publicly announced, or a business model that must not
reach competitors. Pattern matching can't catch this — the judgment that
"this entire folder is confidential" is a human decision that can only be
made by actually reading the content.

## Mechanism

1. **Designation**: list the paths to be classified as confidential, one
   per line, in a list file (e.g. `confidential-paths.txt`). When a new
   confidential project starts, just add a line to this list — no code
   changes needed.
2. **Enforcement point**: `git commit` is not blocked (local version
   control is allowed) — enforcement applies **only to `git push`**. If the
   commit history contains an unpushed commit that touched one of those
   paths, the push to the remote is blocked.
3. **How it's determined**: within the range being pushed
   (`origin/<branch>..HEAD` if a remote branch exists, otherwise the entire
   history), check whether any file matching a listed path was touched. If
   even one match is found, the push is blocked.
4. **Preventing bypass**: it's designed so the block cannot be bypassed by
   editing code — a human must manually delete the line from the list file
   for the push to go through. This is deliberate friction meant to prevent
   accidental leaks, not a replacement for a human's final decision. Once
   you've genuinely confirmed something is safe to release, delete the line
   from the list and try again.

## Difference from Crystal 07 (pattern-based guardrails) — a different axis

| | What it blocks | Enforcement point |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | **Patterns** of secret values (API key formats, email formats, etc.) — determinable via regex without reading content | Prompt submission, commit, push |
| This crystal | Whether an **entire project/path** is confidential — determined solely by human judgment, not pattern | `git push` only |

The two mechanisms don't overlap and are complementary: Crystal 07 covers
"what's secret and identifiable by format," and this crystal covers "what
can't be known by format and must be designated by a human."

## Side effects — stated honestly

If the local repository is several commits ahead of the remote, and even
one of those commits touched a confidential path, **every subsequent push
will fail to go through** — including the latest changes that didn't touch
the confidential path (because the scope isn't per-commit, but "the entire
range about to be pushed"). If this happens, history cleanup or a separate
branch strategy needs to be discussed with a human — this mechanism itself
doesn't make that call for you.

## Minimal implementation

```bash
# Inside a hook that intercepts git push (pre-push hook, or a pre-command-execution hook):
if echo "$COMMAND" | grep -qE '\bgit\s+push\b' && [ -f confidential-paths.txt ]; then
  RANGE="HEAD"
  git rev-parse --verify origin/main >/dev/null 2>&1 && RANGE="origin/main..HEAD"
  while IFS= read -r CPATH; do
    [ -z "$CPATH" ] && continue
    if [ -n "$(git log --name-only --pretty=format: "$RANGE" -- "$CPATH")" ]; then
      echo "Blocked: confidential path ($CPATH) is included in the push range — delete that line from confidential-paths.txt and try again" >&2
      exit 2
    fi
  done < confidential-paths.txt
fi
```

## Related
- [07-prompt-guardrails/](07-prompt-guardrails/) — pattern-based secret
  blocking (a different axis).
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  operating principle #0 (always confirm before irreversible actions) —
  this mechanism's "bypass prevention" design shares the same spirit.
- [20-decision-rights-raci.md](20-decision-rights-raci.md) — the setup
  where a human designates what's confidential and AI only enforces it is
  on the same axis as the "A is always human" principle.
