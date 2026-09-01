<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Grounding Validity Audit — Periodically Revisiting Our Own Guidance Documents

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/26-grounding-validity-audit.md)**

**Version**: 1.0.0
**Content hash**: sha256:9e4483dc9230 (of the body below, excluding the stamp comment, this line, and the version line)

🟢 **Verification strength**: extracted directly from this repo's own
operational practice; the methodology's effectiveness has itself been
empirically confirmed across 2 actual audits.

## Why it's needed

Guidance, guardrail, and standards documents usually cite something
alongside a "Source:" label. The problem is that not everything behind
that label carries the same level of trust — a citation directly verified
against a primary source, a citation that just carries forward a "widely
believed" claim, and a principle built purely from this project's own
experience can all be sitting behind the same "Source:" label. This
crystal is an audit procedure that **periodically reopens and
cross-checks against the original sources** the citations already written
into existing guidance documents. Where
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
covers "what kinds of false grounding exist," this crystal covers "the
procedure for finding and fixing false grounding that may already be
present in our own existing documents" — a catalog versus an audit, that's
the difference.

## Mechanism — three-tier classification

Every claim cited in a guidance document is classified into one of the
following three tiers:

| Tier | Meaning | How it's determined |
|---|---|---|
| **Primary-verified** | The original source was opened directly and confirmed to actually support the claim | Cross-checked against the original |
| **Secondary citation, unverified** | Grounding exists, but the original source couldn't be located, or it's contested | Not cross-checked against the original |
| **Ungrounded, self-observed** | A principle built purely from this project's actual experience, with no external grounding | N/A |

**Being ungrounded isn't bad** — it's fine as long as it's labeled exactly
as such. The real problem is stating something ungrounded as if it were a
"general principle," with unwarranted certainty.

## Audit procedure

1. Decide which documents to audit (all guidance/guardrail/standards
   documents, or start with the most recently updated ones).
2. For each citation, open the primary source (paper, official
   documentation, spec) directly and cross-check it.
3. Mark it with one of the three tiers above.
4. **Correct any misattribution or distortion immediately** — even if the
   underlying principle is still useful, "who actually claimed this" must
   be accurate.

## Measured effect — what the two audits actually turned up

1. **Correcting a misattribution**: a rule of thumb — "there's little
   marginal benefit past N repetitions" — had been cited as coming from
   the empirical results of a specific paper. Reopening the original
   source revealed that the paper actually measured the opposite direction
   (continued improvement with more repetitions). The fix: the rule of
   thumb itself was kept, but its grounding was relabeled — not as a
   nonexistent paper's empirical finding, but as "this project's own
   policy," based on a general principle (in the vein of Goodhart's law —
   that a metric turned into a target distorts itself).
2. **A citation "believed to exist" that actually didn't**: one document
   was believed to cite a well-known theory (something in the vein of
   Amdahl's law), but cross-checking the entire file and its edit history
   directly showed the concept had never actually appeared in it — it
   wasn't a case of "cited incorrectly," but the fact was that "no citation
   had ever existed in the first place." That said, the mechanism the
   document describes turned out to be conceptually identical to the
   actual theory, so a genuine citation was newly added this time.

Both cases are the result of applying the principle "don't uncritically
graft in even authoritative sources" to **this project's own past output**
— the key point of this crystal is that the audit target is not external
material, but the project itself.

## Efficiency considerations

To avoid weighing down the guidance documents themselves, audit results
are kept in a separate audit file (or audit log), and only a minimal tier
marker is left in the original guidance document — writing the full
cross-check process for every citation directly into the original document
would conflict with the "smallest possible high-signal token set"
principle in
[16-context-engineering-principles.md](16-context-engineering-principles.md).

## Related
- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  a catalog of "what kinds of false grounding exist" (this crystal is the
  audit procedure that applies that catalog to the project's own existing
  documents).
- [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md) — how to
  read the trustworthiness of a cited number itself (applies the same
  "don't take a citation at face value" spirit as this crystal, to the
  specific domain of benchmark numbers).
