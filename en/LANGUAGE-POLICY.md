<!-- translated-from: ssot=sha256:ae6546a4db24 own=sha256:e02f55e7934b -->
# Language Reference Policy — How an AI Decides Which Language Version to Read

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/LANGUAGE-POLICY.md)**

This file is **configuration for the AI agents that consume this framework, not for people** — a person should just read whichever language they're comfortable with. It exists so that when an AI needs to read a crystal (e.g., while introducing this folder into a new project and consulting its principles), it doesn't have to re-decide **every single time** whether to open the Korean original (`NN-*.md`) or the English translation (`en/NN-*.md`) first.

## Default

```
default_reference_language: ko   # The SSOT is always Korean — see BLUEPRINT.md section 7
```

Only the project adopting this folder can change this value — for example, if a team's working language is primarily English, it's fine to flip this to `en`. **Changing this field does not change the SSOT itself** (which file actually gets edited) — this is a "read priority" setting, not a "write target" setting (never confuse this with the SSOT principle in BLUEPRINT.md section 7).

## The decision order an AI actually follows — tiers and exceptions

Once you know which crystal you need to read, decide in this order — earlier conditions always override later ones:

| Order | Condition | Action |
|---|---|---|
| 0 (always highest priority) | No `en/` translation file exists for this crystal at all | Read the Korean original unconditionally — there's no other option |
| 0 (always highest priority) | An `en/` translation file exists, but `agent-ops-framework-translation-sync-check.py` (BLUEPRINT.md section 7) has flagged it STALE | Read the Korean original (SSOT) unconditionally — a stale translation can be a misleading source |
| 0 (always highest priority) | The same script flagged it DIVERGED (the translation was edited directly without a stamp update — e.g. a PR from an English-only contributor) | Default to reading the Korean original, but **explicitly recognize the English side may carry a real, not-yet-reconciled contribution** — for anything precision matters for, open both and compare. Surface this state to a human so BLUEPRINT.md section 7's reconciliation procedure (fold it into the SSOT, then retranslate) can run |
| 1 (default) | Neither exception above applies | Read whichever language `default_reference_language` points to (Korean by default) |
| 2 (efficiency exception) | The project/session you're currently working in has English as its primary language, even if `default_reference_language` is still `ko` | It's fine to read the English version first if the translation is up to date — this saves the cost of mentally translating Korean into English every time. **However**: when quoting directly, or copying an exact number, URL, or arXiv ID, cross-check against the Korean original (the SSOT) — there's always a risk that a number or proper noun got mistranslated in the process |

## What this policy must never let slip

- **Any citation where accuracy matters (numbers, URLs, paper IDs, code identifiers) is always cross-checked against the SSOT (Korean) at the end, regardless of which language you chose to read first** — tier 2 (the efficiency exception) is about "what may be read first," not about "what may be trusted."
- This file itself, like BLUEPRINT.md section 7, is a domain-free configuration file — safe to copy as-is into a new project. Only the `default_reference_language` value should be re-decided to fit that project's actual needs.

## Related
- [BLUEPRINT.md](BLUEPRINT.md) section 7 — the SSOT principle and the design of the translation-staleness detection mechanism.
