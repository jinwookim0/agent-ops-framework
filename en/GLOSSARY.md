<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# Glossary — What This Folder's Recurring Terms Mean

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/GLOSSARY.md)**

Several documents in this folder keep reusing the same words, but each
word's definition usually lives scattered inside whichever document
introduced it first — without a single place to look, "what exactly does
this project mean by this word" has to be reconstructed by cross-checking
several documents every time. This document invents no new definitions —
each entry just points to where the term is actually defined, and calls
out the difference between word pairs that are close enough in meaning to
get conflated in practice (e.g., "story" and "domain knowledge"). This is
useful for the same reason to a human reader and to an AI agent reading
this folder — instead of reconstructing terminology from several documents
every time, either can check here once.

## Crystal
The unit this folder is made of — not a finished spec, but a
domain-neutral reference fragment stripped down to just its principle and
procedure. Defined in: [BLUEPRINT.md](BLUEPRINT.md) section 1.

## "Crystal" vs. the collective metaphor
The Korean original uses two related words: `크리스탈` ("crystal," the
loanword) for an individual document, and `결정체` (a native-Korean word
also meaning "crystal") for the folder-wide metaphor itself ("a crystal
keeps its structure after the liquid it grew in is gone"). English
doesn't need this split — "crystal" does both jobs — but if you're
reading the Korean source and see both words, they aren't two different
concepts. Defined in: [README.md](README.md) "Why crystal?"

## Story
Not the principle or procedure a crystal holds, but **the incidental
information attached to the specific incident that principle came from**
— dates, proper nouns specific to a particular project or organization,
verbatim quotes from a particular user, or the "which question was this
written in response to" circumstances behind a document's creation. This
is what a crystal strips away; the general rationale for *why* the rule
is needed in the first place is not "story" and stays. **This is a
different axis from "domain knowledge"** — see the next entry.

## Domain knowledge / domain-neutral
"Domain knowledge" is what a project **actually deals with** — its data,
its users, its business logic, the specific decisions unique to that
project. This is a different axis from "story": story is the incidental
history of *how a principle came to exist*; domain knowledge is the
actual content of *what the project is about*. A crystal must have
**neither** (domain-neutral, and free of story) — but treating these as
one and the same, "stuff about that project," makes it easy to strip one
and miss the other: for example, removing dates and names while leaving
in "this project originally came out of an organization that does this
kind of work" (domain knowledge) untouched. Defined in:
[BLUEPRINT.md](BLUEPRINT.md) section 1, gate G2; [README.md](README.md)
"What this is."

## SSOT (Single Source of Truth)
When the same content exists in more than one language or copy, this is
the one file that's actually edited — every other copy is a derived
translation/snapshot. Korean (`ko/`) is this folder's default SSOT.
Defined in: [LANGUAGE-POLICY.md](LANGUAGE-POLICY.md),
[BLUEPRINT.md](BLUEPRINT.md) section 7.

## Verification strength (🟢/🟡/⚪)
An honest badge stating how thoroughly a crystal's cited evidence was
actually checked. 🟢 = the primary source's core content directly
verified; 🟡 = only the skeleton/names verified, with details
reconstructed. ⚪ is not a verification-strength grade at all — it's a
separate marker meaning "needs checking / unverified" used elsewhere in
crystal bodies; when mechanically checking whether a crystal's body
carries a badge, only 🟢/🟡 count. Defined in:
[BLUEPRINT.md](BLUEPRINT.md) section 1.

## Gates (G1-G6)
The six admission criteria a new crystal must clear to actually be added.
Defined in: [BLUEPRINT.md](BLUEPRINT.md) section 2.

## STALE / DIVERGED
The two distinct signals
`agent-ops-framework-translation-sync-check.py` reports. STALE = the SSOT
changed after the translation was stamped (low-stakes, just re-translate
and re-stamp). DIVERGED = the translation file itself was edited without
updating its stamp (higher-stakes — that change must be ported into the
SSOT first). Defined in: [BLUEPRINT.md](BLUEPRINT.md) section 7.

## Origin project
The living project outside this folder that these crystals were actually
extracted from — not this folder itself. When a crystal's body says
"in the original project...," it always means this outside project.

## Reflection candidate
A pattern an automated scanner flags, from the origin project's (or any
project reusing this folder's own) ongoing evolution, as possibly worth
turning into a new crystal here. Not a crystal itself — it still has to
clear the gates. Defined in:
[REFLECTION-CANDIDATES.md](../ko/REFLECTION-CANDIDATES.md),
[BLUEPRINT.md](BLUEPRINT.md) section 4.

## Detection vs. judgment
A design principle shared by this folder's automation scripts —
automating the discovery that something changed (detection) while always
leaving whether that change actually needs action (judgment) to a
human/AI. Defined in: [BLUEPRINT.md](BLUEPRINT.md) section 4.

## Porting
Copying this folder (or a single crystal file) wholesale into a different
project. Defined in: [BLUEPRINT.md](BLUEPRINT.md) section 7.

## Related
- [README.md](README.md) — overview of this whole folder
- [BLUEPRINT.md](BLUEPRINT.md) — where most of the terms above are actually defined
- [USAGE-GUIDE.md](USAGE-GUIDE.md) — how to use this by situation
