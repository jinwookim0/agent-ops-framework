<!-- translated-from: ssot=sha256:e869e15a618f own=sha256:97d1499d6d79 -->
# Prompt Guardrails — a 4-Layer Defense (Executable Code, Ready to Copy and Use)

> 🌐 **[한국어 원본 보기 (SSOT)](../../ko/07-prompt-guardrails/README.md)**

**Version**: 1.6.1
**Content hash**: sha256:bbf140f08e00 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟢 verified with an actual live block test (a
publish attempt with a test secret pattern was actually refused; a `git
push` attempt was actually blocked). A 2026-09-01 red-team audit also
confirmed and closed several concrete regex-coverage gaps (PEM private-key
blocks, GitHub/Stripe/Slack tokens, terminal-escape-injection defense,
fail-closed on JSON parse failure — see "Honest limits" below).

Executable code that keeps secrets (passwords, API keys) and personal
data (email addresses, phone numbers, resident registration numbers)
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

## Why 4 layers — each layer blocks a different failure mode

| Layer | When it fires | What it blocks | Limitation |
|---|---|---|---|
| **Layer 1: Tool blocking** (`settings.json`) | The moment there's an attempt to **read a file** | A sensitive path from ever entering the context (the prompt) in the first place | Can't stop anything once it's already in the context |
| **Layer 2: Active masking** (`scripts/mask-sensitive-output.py`) | When a human (or the AI) **runs a command directly** | Actually substitutes out anything matching a pattern in content already in the context | Doesn't work if you forget to run it — which is why layer 3 exists |
| **Layer 3: Hook enforcement** (`hooks/guard-secrets.sh`) | Automatically, **right before** a publish/commit tool call (only inside Claude Code's own Bash tool-call boundary) | Catches it even if a human forgets layer 2, by intercepting the tool call itself and automatically checking/blocking it | Never fires at all if a human runs `git push` directly in a terminal, outside Claude Code |
| **Layer 4: Native git pre-push hook** (`hooks/pre-push-verify.sh`) | The instant `git push` **actually reaches the remote**, invoked by git itself (Claude Code isn't involved) | The path layer 3 can't see (a human pushing directly) plus a channel layer 3 never checks at all: the outgoing commit messages themselves | Silently does nothing if `core.hooksPath` was never configured (see "Installation" step 5); always bypassable with `--no-verify` — a safety net, not an enforced wall |

The four layers block different failure modes — you shouldn't rely on
just one; all four together are what completes the defense.

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
5. To also get layer 4 (the native git pre-push hook), copy
   `hooks/pre-push-verify.sh` over as-is, point `.githooks/pre-push` at
   that file, and run `git config core.hooksPath .githooks` — `.git/hooks/`
   itself isn't version-controlled, so each clone needs this set
   separately; worth writing that command into `CONTRIBUTING.md`'s
   "first thing after cloning" section.

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

**FIXED (2026-09-01, found in a self-review before open-source
release)**: `settings.json`'s `permissions.deny` only covered rsa and
ed25519 among SSH key formats — missing ecdsa/dsa key files
(`*_ecdsa`, `*_dsa`) that can sit outside `~/.ssh/` (e.g. a
project-root deploy key), PKCS#12/Java keystore files (`*.pfx`,
`*.p12`, `*.jks`, `*.keystore`), and `~/.npmrc`/`~/.pypirc`/
`~/.cargo/credentials` — easily overlooked files that hold plaintext
npm/PyPI/Cargo registry auth tokens. Added identically to both the ko
and en `settings.json`.

**FIXED (2026-09-01, found while directly checking whether CI actually
passes)**: `public-repo-check.sh` is `verify.yml`'s only build-blocking
step, but it had no way to mark a match as "reviewed, kept
intentionally" (e.g. the synthetic tickets in
`examples/issue-triage-agent/` deliberately using an RFC 2606
reserved domain) — so CI was failing every single run, permanently,
and that only surfaced when the exit code was checked directly on the
command line. Added `public-repo-check-allowlist.txt` (path:line plus
a reason) and changed the script so only matches NOT on that list block
the build. A whitelisted match still prints, labeled "☑️ reviewed —
whitelisted," rather than disappearing silently — a silent pass would
mean a genuinely new leak landing on the same line as an old, reviewed
one could slip through unnoticed.

**ADDED (2026-09-01, prompted by "shouldn't this very repo actually be
using its own crystal 07")**: layer 3 (`guard-secrets.sh`) only fires
inside Claude Code's own Bash tool-call boundary — a human running `git
push` directly in a terminal never triggers it at all. Added
`hooks/pre-push-verify.sh`, a native git pre-push hook, as layer 4 to
close that path. It (a) scans the messages of the commits actually being
pushed for session links, local absolute paths, and PEM-key patterns —
the commit message is a different channel than file content, one
`public-repo-check.sh` was never checking, and (b) re-invokes
`public-repo-check.sh` itself for file content rather than
re-implementing the same patterns a third time. This gap surfaced only
after this session ran into the exact failure mode itself, for an
unrelated reason (a session-link trailer had landed in every commit
message) — the same real-incident grounding (Gate G1) this framework
asks of everything else.

**FIXED (2026-09-01, found while live-testing the pre-push hook above —
the most serious finding this session)**: `public-repo-check.sh` (both
ko and en) has used `grep -InE` for its pattern checks all along —
capital `-I` means "treat binary files as not matching," not
case-insensitive matching (that's lowercase `-i`). So this script has
been matching its secret-key pattern **case-sensitively** since it was
first written. Reproduced live: a file containing
`API_KEY=abcd1234567890xyz` came back exit 0 (clean) — its sibling
script, `mask-sensitive-output.py`, sets `re.IGNORECASE` on the exact
same pattern and catches it correctly (confirmed exit 1). This is this
same file's own "How to extend" section's warning — "the two files
maintain the same detection list independently, so fixing one and
forgetting the other opens a gap" — actually happening, just via a typo
rather than a forgotten update. Fixed to lowercase `-inE`; re-ran the
`API_KEY=...` test (now exit 1) and a full scan of this repo (no new
false positives) to confirm. The new `pre-push-verify.sh` had copied
the exact same typo into its own commit-message check — fixed there
too. If it hadn't been caught, the layer 4 defense just added above
would have missed its own name: "Claude-Session:" starts with a capital
letter, and that check's pattern was written in lowercase.

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
- **Used to be fragile to git history rewrites — resolved by a ground-up
  redesign, 2026-09-01**: this item was originally filed as a structural
  limit that couldn't be fully closed; correcting that here, since it
  actually was closed. What happened: two squashes in one session left
  37 of 44 `translated-from` stamps in this repo pointing at a commit no
  longer reachable from HEAD — `git log -1 --format=%ct <hash>` kept
  "succeeding" (returning a plausible-looking timestamp) for the
  dangling, not-yet-garbage-collected commit object, so nothing looked
  wrong locally for a while. **First response** (a `git merge-base
  --is-ancestor`-based reachability check plus a `--repair` flag)
  automated detection and recovery, but left the root problem standing —
  history rewriting itself was still unsafe, and "a human has to
  remember to run `--repair` after every rewrite" is exactly the pattern
  this folder criticizes elsewhere (a documented rule is powerless the
  moment someone forgets to run it — the same lesson behind this
  README's own layer-2-vs-layer-3 distinction above). **Actual fix**:
  redesigned the `translated-from` stamp from a git commit hash to a
  **content hash** (sha256 of the SSOT's body + sha256 of the
  translation's own body — the same mechanism
  `agent-ops-framework-version-check.py` already used for ko/ crystals'
  own self-consistency) so it no longer references any git object at
  all — no squash, rebase, or force-push can break it. Verified live, not
  just argued: reproducing the same squash in a scratch clone broke
  37/44 stamps before the redesign and 0/44 after. Full rationale in
  `scripts/agent-ops-framework-translation-sync-check.py`'s "Why
  content-hash, not commit-hash" section.
- **Drift between the live deployment and this template**: the actually
  deployed `.claude/hooks/guard-secrets.sh` has confidential-path-
  blocking logic (`confidential-paths.txt`/`pending-human-review-
  paths.txt`) that this template doesn't — copying this folder wholesale
  into a new project won't bring that capability along.

That this list exists isn't a reason to distrust this code — stating
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
