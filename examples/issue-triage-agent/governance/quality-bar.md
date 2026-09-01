# Debt marker & quality bar — triage-incoming-issue

> Instantiation of [13-debt-and-quality-bar.md](../../../ko/13-debt-and-quality-bar.md)
> for this skill.

## Debt marker

**🟢 실행완료 (ran, output produced) — not yet ✅ 공식통과 (formally
passed)**: `triage.py` has been run against all 6 fixtures in
`sample-tickets.json` and produced the logged output in
`../observability/sample-run.jsonl`, but `../evals/eval-cases.md`'s 4
cases have not been run through a formal judge pipeline (this demo's
classifier is deterministic keyword rules, so "formal judging" would
mostly restate what a direct read of the code already confirms — a
genuine LLM-based classifier would need the real
[04-eval-engineering-methodology.md](../../../ko/04-eval-engineering-methodology.md)
pipeline run for real, not skipped).

Debt classification (Fowler/McConnell quadrant): **prudent-deliberate** —
the "no formal eval run" gap is a conscious choice for a demo project
whose classifier is rule-based and directly readable, not an unnoticed
shortcut. If `classify()` is ever swapped for a real LLM (see `SKILL.md`'s
last section), this debt would need to be reclassified: skipping the
formal eval run on an LLM-backed classifier would become
reckless-deliberate, because the classifier's actual behavior would no
longer be provable by reading the source.

## Service quality bar (5 criteria)

| # | Criterion | Status |
|---|---|---|
| 1 | Input validation | ✅ `main()` exits with a clear error (not a crash) if the tickets file isn't marked `_synthetic` in default mode, or if `--real` is passed with the synthetic fixture file. |
| 2 | Failure handling | 🟠 Partial — malformed JSON or a missing `tickets` key raises Python's own exception with a traceback rather than a purpose-written error message. Acceptable for a demo; a production version should catch and re-raise with context. |
| 3 | Cost control | ✅ Every log line carries a `"cost"` field (see `../shared-context/cost-log.md`) — currently always zero-token since the classifier is rule-based, but the field exists so a future LLM swap doesn't require adding cost tracking after the fact. |
| 4 | Reproducibility | ✅ Deterministic by construction (keyword rules, no randomness, no model call) — running `triage.py` twice on the same fixtures produces byte-identical `sample-run.jsonl` output. |
| 5 | Observability | ✅ See `../observability/log-schema.md` — every ticket produces one structured JSON line, not a prose summary. |

## Using both axes together

Per the crystal's table: this skill currently sits at "동작함" (working) —
🟢 실행완료 + 4/5 quality-bar criteria fully met (criterion 2 partial) — not
yet "완성" (done), which would require a formal eval pass plus closing the
error-handling gap on criterion 2.

## Debt repayment priority

Per the crystal's ordering: this is a demo project with no accumulated
prudent-deliberate debt queue to prioritize against, so the single
open item (criterion 2's partial error handling) is the whole queue — no
prioritization judgment call is actually exercised here. Noted honestly
rather than inventing a queue to demonstrate the ordering logic.
