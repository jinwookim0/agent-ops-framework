<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Quasi-Identifier Combination Risk — Individually Safe Information Becomes Identifying When Aggregated

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/32-quasi-identifier-aggregation-risk.md)**

**Version**: 1.0.0
**Content hash**: sha256:b5da80de3619 (of the body below, excluding the stamp comment, this line, and the version line)

**Verification strength**: 🟡 The term "quasi-identifier" and the core claim
that "attributes with no identifying power individually can gain identifying
power in combination, and there's no clean mathematical boundary between
identifying and non-identifying attributes" were verified directly against
the Wikipedia article's primary text (quotes confirmed via WebFetch). However,
this document itself is also relying on secondary sources for Latanya
Sweeney's work rather than Sweeney's original papers directly — and a
specific statistic commonly cited alongside this concept (the well-known
figure that a small number of quasi-identifier combinations can uniquely
identify most of a population) could not be confirmed in this verification
pass and was therefore left out of this document. The practical application
framework (why regex scanners can't catch this, the need for a human
checklist) is generalized from a real incident in the original project.

## Basis

A concept established by the lineage of Latanya Sweeney's k-anonymity
research: information that is by itself uniquely identifying — like a name or
a national ID number — is called an "identifier"; information that by itself
applies to many people — like age, zip code, or gender — but **when a few are
combined, narrows down to a specific individual**, is called a
"quasi-identifier." The key finding: combinations of just a few
quasi-identifiers (e.g., birthdate, gender, and area of residence) can in
practice uniquely single out an individual within a population set, and
there's no binary boundary at all between "this attribute is identifying" and
"this attribute isn't" — every attribute is potentially identifying, depending
on the rarity of its value and whatever auxiliary background data an attacker
might separately hold.

## Why Regex and Pattern Scanners Can't Catch This

Automated scanners like [07-prompt-guardrails/](07-prompt-guardrails/) catch
personal information with a **fixed format** (email addresses, API keys, phone
number patterns). Quasi-identifier combination risk arises not from format but
from **a combination of meaning and context** — "an exact income figure,"
"family composition," and "a specific period's travel-absence schedule" are
each an ordinary-looking sentence individually, and none trip a regex. But
when several of these appear **together in one document**, whoever reads that
document (or whoever encounters it if it's accidentally exposed) can narrow it
down to re-identify a specific person, or — if the information has real-time
relevance, like an absence schedule — it can lead to **targeting risk** (e.g.,
knowing when a home will be empty). Recognizing this limitation of automated
scanners, this category needs to be covered by **a checklist a human reviews
directly**.

## Combination Patterns That Are Warning Signs (Examples, Not an Exhaustive List)

- Exact amounts (income/assets) + family composition + approximate
  residence/work area
- A specific absence (travel) period + typical residence patterns
- Health/allergy details + age bracket + affiliation (employer/school)

The common thread: this risk keeps recurring **because each item alone reads
as "just background information," giving no reason to feel it should be
filtered out.**

## Response Principles

1. **Re-read from a combination perspective**: before storing/publishing a
   document, scan for "how many quasi-identifiers appear together in this one
   document" — at the level of the whole document, not sentence by sentence.
   This risk doesn't show up under a sentence-level scan.
2. **Use the worst-case exposure scenario as a litmus test**: judge with the
   falsifiable question, "would it be fine if this document were exposed right
   now, whether by a platform bug or by accident?" — this question actually
   resolves to yes/no, unlike a vague standard like "let's be careful."
3. **Keep only summarized numbers/dates**: preserving the document's purpose
   (understanding preferences/patterns) usually survives replacing an exact
   amount with a range (e.g., "in the low millions") or an exact travel date
   with something like "this quarter" — lower precision only to the point
   where precision and risk stop being proportional.
4. **Use automation only as a signal; the final judgment is human**: fully
   automated detection of quasi-identifier combination is generally hard
   (it requires contextual understanding) — accept up front that this
   category is outside the coverage of automated scanners, and put it
   explicitly into a periodic review checklist so a human doesn't miss it.

## Related
- [07-prompt-guardrails/](07-prompt-guardrails/) — pattern-matchable, formal
  secrets/PII (a category this crystal doesn't cover — mutually
  complementary).
- [23-confidential-project-protection.md](23-confidential-project-protection.md) —
  protecting confidential information at the project/path level (a different
  target scope — this crystal focuses specifically on the "combination" risk
  of personal data).
- [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md) —
  an adjacent safety crystal dealing with the same "persistent memory file,"
  but along a different contamination axis (provenance).
