<!-- translated-from: 6e950e781878be4cc28ed8b43fc53f97a78cc81b -->
# Disclaimer Template

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/DISCLAIMER.md)**

This file takes the practical convention laid out by
[35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md)
(verified against Google's official open-source publication guidelines —
"include the required disclaimer on side projects regardless of whether
they're work-related") and turns it into wording ready to use directly. If
crystal 35 is the methodology of "why and how" to keep this separation,
this file is **one artifact that methodology produces** — the reason it
isn't in the numbered crystal list, and instead sits at the top level of
the folder alongside `README.md`/`BLUEPRINT.md`, is that this isn't "a
technique to learn" but "wording meant to be posted as-is," so it needs to
be findable on its own, without having to open document 35 first.

## When porting/publishing this folder into another project

Place the wording below at the top of that project's top-level
`README.md` (or, if this folder has itself become a repository root, that
repository's root `README.md`) — just fill in the bracketed part:

> This [folder/repository] is a collection of operating principles derived
> from a personal project, is not the official position of [organization
> name], and does not contain confidential or trade-secret information
> belonging to [organization name].

**What this wording does and doesn't do — honestly**:
- What it does: it honestly tells the reader the nature of this content (a
  personal project, unofficial). As the Google example shows, some
  organizations keep this minimal disclosure as a practice regardless of
  work-relatedness.
- What it doesn't do: this wording alone doesn't complete a legal defense —
  if confidential information really is mixed in, attaching a disclaimer
  doesn't change that fact. It doesn't replace [35](35-personal-oss-employer-confidentiality-separation.md)'s
  two-axis judgment (content independence + whether it's permitted given
  the affiliation relationship), or the actual judgment made in a document
  like `RISK-ANALYSIS.md` — it's the final marker attached after that
  judgment has already been made.

## When porting into a new project

This file itself differs from the operational state files
(REFLECTION-CANDIDATES.md, etc.) that [BLUEPRINT.md](BLUEPRINT.md) section
7 designates as needing to be reset — it isn't that project's execution
history but a **reusable template where only the blanks need filling in**,
so it's safe to copy as-is (passes G2). Just fill in the organization name
inside the brackets to match that project.

## Related
- [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) —
  the methodology this wording came from.
- `RISK-ANALYSIS.md` — the project-specific analysis that judges whether
  it's actually okay to attach this wording (unlike this file, an explicit
  exception that does carry domain knowledge).
