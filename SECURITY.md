# Security Policy

## Reporting a vulnerability

Open a GitHub issue on this repository. If the issue involves an actual
secret, credential, or personal data that's already been exposed (not just
a weakness in the detection code), say so in the title without pasting the
sensitive value itself into the issue, and a maintainer will follow up
privately.

This project currently has one maintainer (see
[`CONTRIBUTING.md`](CONTRIBUTING.md)) and no dedicated security response
team — response time is best-effort, not covered by an SLA.

## What's actually in scope here

Most of this repository is prose (the "crystals" in `ko/`/`en/`) — the
part with real security surface is
[`ko/07-prompt-guardrails/`](ko/07-prompt-guardrails/) (and its `en/`
translation), which is executable code: a set of secret/PII detection
patterns, a `settings.json` deny-list, and a `PreToolUse` hook. That
folder's own README has a **"Honest limits"** section maintained
alongside the code (not duplicated here, to avoid the two drifting apart)
— read it before relying on this code to catch something specific. In
short: it's a low-cost safety net for obvious mistakes, not a substitute
for a real secrets scanner or a security audit, and it says so itself,
repeatedly, in its own comments.

## Known limitation classes (as of the 2026-09-01 red-team review)

These are structural, not fixable by patching a regex — know them going
in rather than assume more coverage than exists:

- **Regex-based detection has a ceiling.** Formatting variants (spelled-out
  emails, unusual separators) and unlisted vendor credential formats will
  always be able to slip past a fixed pattern list — see the detail in
  `ko/07-prompt-guardrails/README.md`.
- **A content hash (`agent-ops-framework-version-check.py`) verifies
  self-consistency, not tamper-resistance** — it catches a forgotten
  version bump, not a deliberate edit made with the same public stamping
  tool.
- **Translation-sync `DIVERGED` detection resets on a bare re-stamp** — it
  tracks when a stamp value last changed, not whether a real re-translation
  happened.
- **This project is early-stage** — none of the above has been exercised
  against real external contributors or an adversarial public audience
  yet. Treat everything above as reviewed-by-design, not
  battle-tested-in-production.

## Why these limitations are documented here instead of left unstated

Writing down a weakness class (not a working exploit string) is standard
practice for a project's own tooling, not a risk in itself — every
credible secret-scanner ships a limitations section, and this repository
isn't a live production system protecting third parties yet. What would
be irresponsible is a ready-to-use bypass payload for a specific pattern;
none of what's written here or in `ko/07-prompt-guardrails/README.md` is
that — it names the *class* of gap so it can be fixed or knowingly
accepted, not a recipe for exploiting it.
