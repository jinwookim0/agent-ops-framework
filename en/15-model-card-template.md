<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# System/Model Card Template — Documenting "What This AI Does," Not "How the Project Is Run"

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/15-model-card-template.md)**

**Version**: 1.0.1
**Content hash**: sha256:77a5119bcac0 (of the body below, excluding the stamp comment, this line, and the version line)

Most of the crystals so far (01–14) have covered **how to run a project**.
This crystal asks a different question — **how do you tell users exactly
what this AI agent/feature does, how far it can be trusted, and where it
can go wrong?**

## Basis (primary source verified)

🟢 Mitchell et al. 2019, *Model Cards for Model Reporting* (Google,
FAT* 2019) — [arXiv:1810.03993](https://arxiv.org/abs/1810.03993) verified directly against the original. Quoting the core motivation verbatim from the
source: "to clarify the intended use cases of machine learning models
and minimize their usage in contexts for which they are not well
suited."

## The 9 sections proposed by the source (list verified against the original)

1. **Model Details** — Basic information about the model (developing
   organization, version, type, training approach, references, contact
   info).
2. **Intended Use** — The originally intended use cases and users, along
   with explicitly **out-of-scope use cases**.
3. **Factors** — Factors that may cause performance to vary
   (demographic groups, environmental conditions, technical attributes,
   etc.).
4. **Metrics** — What metrics were used to measure performance and why
   those metrics were chosen.
5. **Evaluation Data** — The datasets used for evaluation, their
   provenance, and preprocessing.
6. **Training Data** — The data used for training (disclosed as fully
   as possible, or at minimum its characteristics if full disclosure
   isn't possible).
7. **Quantitative Analyses** — Quantitative performance broken down by
   group (not just an overall average, but by subgroup — the same
   principle as item 9, "micro-macro inversion," in
   [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)).
8. **Ethical Considerations** — Ethical risks to consider when using the
   model.
9. **Caveats and Recommendations** — Areas needing further testing,
   known limitations, and recommendations for improvement.

## Applying this to AI agent projects — shifting the unit from "model" to "feature/task"

The source assumes you're documenting a single trained ML model. In AI
agent projects, you typically aren't training the model itself, so
**shift the documentation unit from "model" to "an individual
feature/task this project provides"**:

| Original section | Reinterpreted as an AI agent feature card |
|---|---|
| Model Details | Which tools/models this feature uses, when it was built, who maintains it |
| Intended Use | What this feature does, and **what it explicitly does not do** (e.g., "not investment advice," "not legal advice") |
| Factors | Conditions under which this feature's results may vary (input language, domain, data freshness) |
| Metrics | The pass criteria from [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) |
| Evaluation Data | What evaluation cases were used to verify it |
| Training Data | (Where applicable) the nature of the shared context/history data this feature draws on |
| Quantitative Analyses | Pass rates broken down by case type (don't show only the overall average) |
| Ethical Considerations | The sensitive judgment calls this feature touches (financial, health, legal, etc.) and their limits |
| Caveats and Recommendations | [Known-limitations section — a format other crystals such as 04 and 11 already use] |

## The key is spelling out "unintended use"

The most frequently overlooked part of the original is the "unintended
use" portion of Intended Use — many documents only write "here's what
it can do" and never write "don't use it for this." Item 10 of
[01-definition-of-done.md](01-definition-of-done.md) (content-source
motivational bias) and G1 of
[10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md)
("clarify what the system can do") already move in this direction, but
the Model Card complements them by structurally forcing you to also
spell out, symmetrically, **what the system does not do**.

## A practical shortened version — when all 9 sections are too much

Filling out all 9 sections for every small feature can be overkill. At
minimum, fill in: **Intended Use (what it does + doesn't do) + Metrics
(pass criteria) + Caveats (known limitations)** — reserve the full nine
sections for features that grow larger in scope or higher in
sensitivity.

## Related crystals
- [01-definition-of-done.md](01-definition-of-done.md) — This crystal's
  "Metrics/Evaluation Data" section overlaps with DoD criterion 4
  (evaluation cases) — cross-reference instead of duplicating the
  content.
- [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) — Where
  "Ethical Considerations" meets threat modeling.
