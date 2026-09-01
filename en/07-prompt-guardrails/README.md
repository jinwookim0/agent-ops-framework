<!-- translated-from: 2ae1d3292bfb069ca2638579e004c085d3c029ff -->
# Prompt Guardrails — a 3-Layer Defense (Executable Code, Ready to Copy and Use)

> 🌐 **[한국어 원본 보기 (SSOT)](../../ko/07-prompt-guardrails/README.md)**

**Version**: 1.2.0
**Content hash**: sha256:3d61d0981f58 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 verified with an actual live block test (a
publish attempt with a test secret pattern was actually refused; a `git
push` attempt was actually blocked). A 2026-09-01 red-team audit also
confirmed and closed several concrete regex-coverage gaps (PEM private-key
blocks, GitHub/Stripe/Slack tokens, terminal-escape-injection defense,
fail-closed on JSON parse failure — see "Honest limits" below).

Executable code that keeps secrets — passwords, API keys — and personal
data — email addresses, phone numbers, resident registration numbers —
from leaking into an AI agent's prompts, external publications, or git
commits. This folder is **the one document set in this whole collection
that isn't an explanation but code you can copy and use directly** — it's
already at 0% domain knowledge (carried over verbatim from the original).

**Where the actual code lives**: the executable files (`settings.json`,
`hooks/guard-secrets.sh`, `scripts/*.py`, `scripts/*.sh`) are duplicated
here in full, sitting right next to this README (an earlier version of
this note said they weren't — that was a real gap in the ko/en symmetry
this repo otherwise commits to, since it left `en/07-prompt-guardrails/`
visibly incomplete; fixed). The functional code (regex patterns, control
flow) is kept byte-identical to the Korean original in
[`../../ko/07-prompt-guardrails/`](../../ko/07-prompt-guardrails/) —
only comments and human-facing strings (error messages, help text) are
translated. Verified identical: the regex patterns were diffed directly
against the Korean source, and `mask-sensitive-output.py --check` was run
against the same test input in both languages to confirm matching
behavior.

## Why 3 layers — each layer blocks a different failure mode

| Layer | When it fires | What it blocks | Limitation |
|---|---|---|---|
| **Layer 1: Tool blocking** (`settings.json`) | The moment there's an attempt to **read a file** | A sensitive path from ever entering the context (the prompt) in the first place | Can't stop anything once it's already in the context |
| **Layer 2: Active masking** (`scripts/mask-sensitive-output.py`) | When a human (or the AI) **runs a command directly** | Actually substitutes out anything matching a pattern in content already in the context | Doesn't work if you forget to run it — which is why layer 3 exists |
| **Layer 3: Hook enforcement** (`hooks/guard-secrets.sh`) | Automatically, **right before** a publish/commit tool call | Catches it even if a human forgets layer 2, by intercepting the tool call itself and automatically checking/blocking it | Can't see anything that doesn't pass through a tool-call boundary (e.g., text pasted directly into chat) |

The three layers block different failure modes — you shouldn't rely on
just one; all three together are what completes the defense.

## Installation

1. In `settings.json`'s `permissions.deny` list, replace `shared/local/**`
   with whatever directory name this project actually uses for
   local-only sensitive files. The rest (`.env`, SSH/AWS keys) applies
   as-is to most projects.
2. Replace the `Artifact` matcher in `hooks/guard-secrets.sh` with the
   name of whatever external publish/deploy tool this project actually
   uses (if there are several, register multiple hooks or list the
   matchers pipe-separated).
3. Copy the three files (`settings.json` → `.claude/settings.json`,
   `hooks/guard-secrets.sh` → `.claude/hooks/guard-secrets.sh`,
   `scripts/*.py` and `scripts/*.sh` → `scripts/`) to the same relative paths
   in the target project — since `settings.json`'s `command` field points
   at `${CLAUDE_PROJECT_DIR}/.claude/hooks/guard-secrets.sh`, keeping the
   paths exactly as they are is simplest.
4. Immediately after installing, verify it live — create a dummy file
   containing a sensitive pattern, actually attempt to publish/commit it,
   and confirm the block message actually appears (confirm via logs, not
   claims — the same principle as item 8 of
   [03-epistemic-immunity-catalog.md](../03-epistemic-immunity-catalog.md)).
   Delete the dummy file once confirmed.

## Verification status

The original confirmed the following live, in an actual project: (1)
attempting to publish a file containing a secret pattern is actually
blocked by the hook (`exit 2`, the tool call itself gets refused), (2) a
clean file passes through with no false positive, (3) a non-matching tool
name lets the hook pass through immediately (`exit 0`). This verification
was **done in the original project** — it has not been re-verified after
installing this crystal version into another project. Be sure to
re-verify live after installation, following step 4 above (the same
principle as `module-format.md`'s "show verification labels honestly").

## Honest limits (confirmed by a 2026-09-01 red-team audit)

This code is "a safety net that filters out obvious mistakes," not a
complete security audit — each file's own header comment already says
this, but a three-lens red team (technical/security/cost; AI-specific/
bias; value/philosophical) checked for concrete instances. What got
fixed vs. what's only documented:

**FIXED (this audit)**: added PEM private-key block detection (the
existing label+separator "secret key" pattern structurally couldn't
catch it — the highest-impact secret type there is), added GitHub/
Stripe/Slack token patterns, broadened the phone-number/resident-
registration-number separator (space/dot now recognized too), added
terminal/ANSI escape-injection defense to `public-repo-check.sh` (found
the point where attacker-controlled file content gets echoed straight
to the screen and stripped control characters), switched
`guard-secrets.sh` from fail-open to fail-closed on a JSON parse
failure, added `*.key`/`.netrc`/`.git-credentials`/`~/.kube`/
`~/.docker`/`~/.config/gcloud` to `settings.json`'s `permissions.deny`,
closed a filename-with-spaces bypass in `public-repo-check.sh` (a
filename containing a space silently dropped out of scanning via word
splitting — reproduced live) by switching to NUL-delimited listing
(`-z`/`xargs -0`), and replaced `guard-secrets.sh`'s predictable
`/tmp/*.$$` temp-file paths (a symlink-preemption risk on a shared
multi-user host) with `mktemp`.

**DOCUMENTED ONLY (structural limits that can't be fully closed — know
these going in)**:
- **The fundamental limit of regex detection**: spelling out an email
  address ("at" instead of "@") or using Unicode homoglyphs defeats it.
  GCP/Azure credentials, connection-string-style credentials (`scheme://
  user:pass@host`), and secret labels in a language other than English
  still slip through — keeping up with every vendor format is a losing
  race, so this isn't trying to be an exhaustive list.
- **`guard-secrets.sh`'s git-hook scope is narrower than its name
  suggests**: it only matches the **literal strings** `git commit`/
  `git push` — within the same Bash tool call, a `curl`/`scp`/`npm
  publish`/`docker push`, or a git invocation routed through an alias,
  is never scanned at all. The existing "can't see anything outside a
  tool-call boundary" disclosure never separately stated that this
  in-boundary scope itself is narrow.
- **The content hash is a self-consistency check, not tamper-proofing**:
  the stamping tool is public, so if someone who actually changed the
  content also re-runs the stamp, the hash comes back "matching" — it
  catches "forgot to bump the version," not "deliberately used the tool
  to re-stamp anyway."
- **The translation-sync DIVERGED signal resets with a single re-stamp**:
  `agent-ops-framework-translation-sync-check.py` only tracks when the
  stamp value itself last changed, so re-stamping without actually
  re-translating clears the signal — the same fundamental limit as the
  distinction between a checksum and a signature.
- **Fragile to git history rewrites**: commit-hash-based stamps all go
  meaningless at once after a rebase/squash/history cleanup (e.g. using
  BFG to purge a secret that was committed by mistake — exactly the kind
  of remediation this scanner might prompt). **Confirmed by a real
  incident and partially mitigated, 2026-09-01**: two squashes in one
  session left 37 of 44 `translated-from` stamps in this repo pointing
  at a commit no longer reachable from HEAD — `git log -1
  --format=%ct <hash>` kept "succeeding" (returning a plausible-looking
  timestamp) for the dangling, not-yet-garbage-collected commit object,
  so nothing looked wrong locally for a while. Added a
  `git merge-base --is-ancestor`-based reachability check plus a
  `--repair` flag to `agent-ops-framework-translation-sync-check.py` to
  detect and fix this mechanically — but that's automating the recovery
  after the fact, not making history rewriting itself safe: running
  `--repair` as an immediate follow-up commit after any rewrite is still
  an operational rule a human has to actually follow
  (`docs/directive-registry.md` row 1).
- **Drift between the live deployment and this template**: the actually
  deployed `.claude/hooks/guard-secrets.sh` has confidential-path-
  blocking logic (`confidential-paths.txt`/`pending-human-review-
  paths.txt`) that this template doesn't — copying this folder wholesale
  into a new project won't bring that capability along.

This list existing isn't a reason to distrust this code — stating
plainly what's been checked and what hasn't is this whole framework's
principle, applied here the same way as everywhere else.

## How to extend

You need to add the same regex to both `PATTERNS`
(mask-sensitive-output.py) and the `check(...)` calls
(public-repo-check.sh) — the two files independently maintain the same
detection list, so fixing only one and forgetting the other leaves a hole
in the defense (this warning is already written in a comment at the top
of each file). If a project has patterns of its own that come up often
(e.g., a specific internal-system token format), add them the same way.
