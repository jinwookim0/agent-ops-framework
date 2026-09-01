<!-- translated-from: ssot=sha256:6ef20ffbec9f own=sha256:de043f2c1f07 -->
# Writing Craft Guardrails — Removing the "AI Smell"

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/28-writing-craft-guardrails.md)**

**Version**: 1.3.0
**Content hash**: sha256:dda0ea91259f (of the body below, excluding the stamp comment, this line, and the version line)

Text output produced by an AI agent is usually **factually correct but no
fun to read**. [01-definition-of-done.md](01-definition-of-done.md) and
[03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) cover
"is the content accurate" — this crystal covers an entirely different axis:
**how accurate content is delivered**. Accuracy and readability are not
substitutes for each other.

## Self-diagnosis — by actual measurement, not guesswork

Don't judge "this sounds AI-generated" by impression. Across the entire
body of output, count specific opening phrases and stock expressions
(e.g. "simply put," "to be honest," "the key point is"). **If the exact
same phrase repeats, word for word, across a large share of the output
(empirically, a signal worth flagging is when it exceeds half), it's no
longer a meaningful signal — it's become wallpaper.** The repetition itself
is what distinguishes "this phrase was actually needed here" from "it was
written out of habit."

## Grounding (verified against primary sources)

🟢 George Orwell, "Politics and the English Language" (1946) — the most
practical of the 6 rules: never use a metaphor, simile, or other figure of
speech which you are used to seeing in print / never use a long word where
a short one will do / if it is possible to cut a word out, always cut it
out / use the active voice where you can.

🟢 Paul Graham, "Writing, Briefly" / "The Age of the Essay" — "Writing
doesn't just communicate ideas; it generates them" (writing should
discover ideas while being written, not just list conclusions already
reached), "Essays should aim for maximum surprise" (restating something
the reader already knew is a failure).

🟢 Strunk & White, *The Elements of Style* — brevity ("Omit needless
words"), preferring the active voice, stating things in positive form,
using concrete and specific language, placing emphasis in the sentence's
strong closing position, and maintaining parallel structure.

🟢 William Zinsser, *On Writing Well* — "Clutter is the disease of
American writing," "Writing improves in direct ratio to the number of
things we can keep out of it," and the importance of finding your own
voice.

🟢 Kurt Vonnegut, "How to Write With Style" — of the 7 rules, especially:
"Find a subject you care about" / "Have the guts to cut" / "Sound like
yourself" (a sentence that could appear anywhere is a sign it has no
voice) / "Pity the readers" (write as if the reader doesn't know your
background context).

🟢 Guy Kawasaki, "The 10/20/30 Rule" — for presentation decks specifically:
no more than 10 slides, no more than 20 minutes of presenting, font no
smaller than 30pt (forcing enough white space that each slide holds a
single idea, not a paragraph of sentences).

## Translationese — the gap this crystal used to admit and leave open

The "Honest limitations" section below used to say plainly that all 6
sources above come from the English prose tradition, and that
translationese critique needed its own separately verified source. Here
it is:

🟢 Kim Soon-young (Professor, Dept. of English Interpretation &
Translation, Dongguk University), "번역투 문장 in English-to-Korean
Translation," *Sae Gugeo Saenghwal* Vol. 22, No. 1 (Spring 2012),
National Institute of Korean Language — read in full. She quotes Kim
Jeong-woo's (2007: 61) definition directly: translationese is "a textual
trait where traces of being a translation, rather than an original, show
up repeatedly and consistently." Her three categories of real
English-to-Korean examples:

1. **Syntax-level: carrying over English's possessive "have."**
   "She has a book under her arm" rendered literally as "그녀는 책을
   옆구리에 가지고 있다" reads awkwardly — "그녀는 책을 옆구리에
   끼고 있다" is natural. Same trap for "She has a sweet voice": not
   "그녀는 아름다운 목소리를 가지고 있다" but "그녀는 목소리가
   아름답다" (Lee Geun-hee 2005).
2. **Syntax-level: overusing the passive ("be... by...").** English
   reaches for the passive to obscure an agent or emphasize a victim or
   beneficiary; Korean doesn't force the same active/passive distinction,
   so the passive isn't required. "The thief was caught by a brave
   citizen" rendered as "그 강도는 용감한 시민에 의하여 붙잡혔다" is
   stiff — "그 강도는 용감한 시민한테(에게) 붙잡혔다" is natural (Kim
   Jeong-woo 1996).
3. **Inflection-level: mapping English plural -s onto "들" by
   reflex.** "There are new ideas and methods" rendered as "새로운
   아이디어들과 방법들이 있다" is awkward — "여러 가지 남다른 생각과
   방법이 있다" is natural (Lee Geun-hee 2005). Korean's "들" isn't a
   plain plural marker; it adds its own sense of "several different
   kinds," so mapping it onto every English plural can distort meaning
   (Kim Jeong-woo 1996).
4. **Preposition-level: literal "concerning/from/by."** "그 사람으로부터
   잘잘못을 들은 다음..." reads more naturally as "그 사람에게서
   잘잘못을 들은 다음..." (example from Kim Jeong-woo 2007). The paper
   notes these prepositional calques have become common enough to sound
   familiar — familiarity is a sign the translationese has already spread
   widely, not a reason to accept it.

The paper's own conclusion, carried over here: translationese isn't
always bad — sometimes deliberately keeping a foreign flavor, for a
concept Korean has no native word for, is the right call. The actual
problem is failing to distinguish a translator's deliberate choice from
translationese produced unconsciously, with no thought for context. This
crystal always targets the latter.

🟡 **Referenced but not directly opened**: Lee O-deok, *우리글 바로쓰기*
(1992, Hangilsa, 5 volumes) — a well-known Korean critique of
Japanese-influenced and Western-influenced sentence patterns. Confirmed
to exist and roughly what it argues, via a Wikipedia summary only; this
crystal hasn't checked the original text directly.

## Pronoun translationese — filling in "he," "she," "it," "you" the way English does

A pattern the user pointed out directly: English grammar needs a pronoun
subject in nearly every sentence, but natural Korean re-fills that slot
with a concrete noun (a name, a title, a role) or drops it from context
entirely. Translate English pronouns literally and Korean ends up with
"그는," "그녀는," "그것은," "당신은" showing up far more often than the
English original's own pronoun density would predict.

🟡 Chen Pei-Chen & Lee Seong-Ju, "'그녀' as a Translated Word: Inventing a
Third-Person Female Pronoun in Colonial-Era Taiwan and Korea," *Korean
Literature Research* No. 69 (2022), pp. 541-581 — confirmed via the
paper's KCI abstract page; the full text wasn't opened. The abstract
itself states that "그녀" ("she") entered Korean specifically to meet a
translation need during language modernization — newspapers and
literature tested and coined the word, following the same path Japanese
took in coining "彼女" to correspond to Western "she." So "그녀" itself
started out as a product of translationese. (Several linguistics papers
also note that even "그" only settled into its modern third-person-pronoun
role after early-20th-century modern fiction, a claim repeated often
enough to be worth flagging, though this crystal hasn't opened those
papers directly.)

🟡 Park Cheong-hui, "A Statistical Approach to Ellipsis in Korean and
English — Focusing on Subject and Object Omission," *Eomun Nonjip* No. 66
(2012), pp. 171-192 — confirmed via the paper's KCI abstract page, not the
full text. Its reported numbers: Korean drops the subject 67.82% of the
time and the object 13.78% of the time; English drops the subject only
31.5% of the time and the object 7.67% of the time. (The paper's own
English-language abstract gives a slightly different figure, 69.22%, for
the Korean subject-drop rate — a small internal discrepancy in the source
itself, disclosed here rather than silently picking one number; settling
which figure is final would mean reading the paper's body text.) Modern
linguistics not uncommonly calls Korean a "null-subject language" for
this reason.

**Application**: when a Korean sentence starts with "그는/그녀는/그것은/
당신은," ask first whether that slot could hold the original name or noun
again, or be dropped from context entirely — if the sentence still reads
clearly either way, cut the pronoun. "당신" ("you") in particular often
reads as stiff or distancing in Korean; mechanically translating "you
should..." as "당신은 ~해야 한다" is a classic tell.

## Confirmed in practice — a well-known open-source project reached the same conclusions independently

A question worth asking: has any real GitHub repository actually applied
guidelines like these well, not just stated them? Yes. The two cases
below reached almost the same rules as this crystal's cited papers,
entirely on their own, from practical experience rather than academic
research — theory and practice cross-confirming each other, which
doesn't happen often.

🟢 The official Kubernetes documentation repository (`kubernetes/website`,
CC BY 4.0), in its Korean localization guide
(kubernetes.io/ko/docs/contribute/localization_ko/) — read directly in
the original. Its "avoid translationese" section gives this table
(excerpted):

| Translationese | Natural phrasing |
| --- | --- |
| 되어지다 (double passive) | 되다 |
| a pig **with** short legs (짧은 다리를 가진 돼지) | a short-legged pig (다리가 짧은 돼지) |
| he picked up a spoon with **his** hand and ate **his** rice (그는 그의 손으로... 그의 밥을 먹었다) | he picked up a spoon and ate (그는 손으로 숟가락을 들어 밥을 먹었다) |
| there are pear**s**, apple**s**, and peach**es** at the store (배들, 사과들, 복숭아들) | there are pears, apples, peaches at the store (배, 사과, 복숭아들) |

Three of these four examples overlap almost exactly with three of the
categories this crystal cites from Kim 2012 (the literal possessive
calque, the overused passive, the mechanical "들"). One of the largest
open-source projects in the world independently ran into the same
problems, in practice, with no reference to any academic paper, and
landed on the same fixes.

🟢 GitHub's own official documentation repository (`github/docs`, prose
content under CC BY 4.0, code samples separately under MIT), in its
"Writing content to be translated" guide — read directly in the
original. It states two rules: (1) "Lots of stacked
modifiers can lead to incorrect translations because it's not easy to
determine what modifies what" — exactly the modifier-stacked-between-
subject-and-verb problem this project's own history section below
names. (2) "Vague nouns and pronouns can make it unclear who or what you
are referring to, especially when that content has to be translated" —
the same concern as the pronoun section above.

**Application**: these two cases are a different kind of evidence than
Kim 2012, Chen & Lee 2022, or Park 2012 — practical rules from
large-scale, real-world projects, not academic theory. When looking for
grounding for a new crystal or a practical guide, it's worth checking not
just academic papers but how an already well-run, large open-source
project solves the same problem — these two happened to.

## The other direction — carrying Korean structure into English (this project's own history)

Everything above runs English-to-Korean. This project has the opposite
risk too, since `ko/` is the source of truth and `en/` is a translation:
carrying Korean clause order and modifier placement straight into
English. There's no outside academic source for this
direction — it's backed by this project's own incident history instead
(BLUEPRINT.md section 1's grounding path (b): the origin project's own
operating history). Found and fixed on 2026-09-01:
- A Korean-style stack of modifiers wedged between subject and verb,
  turning an English sentence into a maze (crystal 17's English version
  had "crystals that would be distorted... — [a long list] — are
  deliberately left outside").
- A compressed Korean modifier forced into an awkward hyphenated
  compound (e.g. "the actually-wanted outcome").
- A subject mismatch, where Korean's dropped subject got attached to the
  wrong noun in English (e.g. "Instead of consulting each document
  separately, the goal is to see...").

## Reference for good style — actual examples, not just a rulebook

A list of rules alone doesn't capture "what it should sound like." Draw
the following techniques from actually well-written pieces (essays,
well-regarded blogs, encyclopedia-style commentary on prose style):

1. **Open with a concrete scene** — start with a specific event or scene,
   rather than an abstract summary ("This piece covers X").
2. **Name your concepts** — giving a recurring idea a memorable name
   (like Tim Urban's "Die Progress Unit") gives readers a handle to refer
   back to it.
3. **Handle big ideas in a casual voice** — formality and depth are not
   correlated.
4. **Build up concepts gradually** — don't front-load the conclusion; add
   the next piece once the reader is ready to understand it.

## Specific anti-patterns (repeatedly observed)

1. **Obligatory metaphors** — a metaphor that would make just as much
   sense pasted onto any unrelated content. If it's not specific to this
   particular content, it's a template, not writing.
2. **Repeating the same skeleton** — output within the same series
   repeats an identical structure, word for word. If you can't explain why
   the structure has to be the same, write a new structure that actually
   fits the content.
3. **A list with no argument** — laying out bullet points is a
   verification log, not writing. If you can't distill "so what is this
   actually saying" into a single sentence, it isn't writing yet.
4. **Hedging standing in for voice** — if a sentence is still
   understandable after cutting connective stock phrases and softening
   language, cut them (a direct application of Orwell's "cut if you can"
   rule).

## Self-check checklist

- [ ] Can you state this piece's "surprise" in a single sentence
      (Graham)? — if not, it's still a verification log, not writing.
- [ ] Is the metaphor/expression specific to this content, or would it
      still make sense swapped onto something else? — if the latter, cut
      it.
- [ ] Is the sentence still understandable after cutting connective stock
      phrases (Orwell)? — if so, cut them.
- [ ] Is there a sentence still in passive voice that could be active
      (Strunk & White, Orwell)?
- [ ] If this piece's structure is identical, word for word, to other
      output in the same series, can you explain why it has to be
      identical?
- [ ] If you took a single sentence out of this piece on its own, would it
      still be recognizable as something this project wrote (Vonnegut,
      "Sound like yourself")?
- [ ] Did you write assuming the reader doesn't have this background
      knowledge (Vonnegut, "Pity the readers")?
- [ ] **(Slide-format output only)** Does each slide hold a single idea
      rather than a paragraph of sentences (Kawasaki 10/20/30)?
- [ ] **(Korean output)** Is a "~을 가지고 있다"-style phrase actually
      carrying over English's possessive "have"? Check whether "~이
      있다/딸리다" reads more naturally (Kim 2012).
- [ ] **(Korean output)** Does a "~에 의해 ~되다"-style passive sentence
      keep its meaning in the active voice? If so, use the active voice
      (Kim 2012).
- [ ] **(Korean output)** Can a literal "~에 관하여/~로부터/~에 의해"
      prepositional calque unfold into a natural particle like
      "~에게서/~에서/~으로" (Kim 2012)?
- [ ] **(Korean output)** For a sentence starting with "그는/그녀는/
      그것은/당신은" — does it still make sense with the original noun
      restated, or with the pronoun dropped entirely? If so, drop it
      (Chen & Lee 2022, Park 2012).
- [ ] **(English output translated from Korean)** Is there a Korean-style
      stack of modifiers wedged between the subject and the verb? If you
      have to read to the end of the sentence before you know what the
      subject is actually doing, restructure it.
- [ ] **(Either language)** When writing the same content in both
      languages, did you copy one sentence's order or clause structure
      directly into the other? Check whether each version reads
      naturally on its own, without looking at the other one first.

## When to apply this

This checklist isn't a one-time audit meant to sweep through everything
that already exists — it's a **pre-publish check for whatever you're
writing or editing right now**. Apply it to the actual diff, not to
crystals that already carry a verification badge: when you add a new
crystal or genuinely edit an existing one's body (translations
included), run it against that change. A full sweep of everything
already published is a separate, explicitly scoped effort (for example,
picking one batch of crystals and working through them in sequence) —
not something this checklist runs on every time by default.

## Honest limitations

**The English-to-Korean direction is now backed by a primary source**
(the "Translationese" section above, Kim 2012) — no longer an
acknowledged gap. That said, this crystal hasn't opened the studies Kim
2012 itself cites (Kim Jeong-woo 1996/2007, Lee Geun-hee 2005, Lee
Hee-jae 2009) — the 🟢 only covers what's within Kim 2012's own citations.
Lee O-deok's *우리글 바로쓰기* is confirmed to exist with roughly the
right argument (🟡), not opened directly. **The Korean-to-English
direction** (found in this project's own `ko/` → `en/` translations) is
backed only by this project's own incident history, not an outside
academic source — it's a real, fixed case from this project, not a
linguistically generalized finding. **Both sources in the pronoun
section (Chen & Lee 2022, Park 2012) are also 🟡** — author,
bibliographic details, and core claim confirmed via their KCI abstract
pages, not the full text. Park 2012 itself carries an
internal discrepancy, disclosed above rather than resolved: the Korean
subject-drop rate reads 67.82% in the body but 69.22% in the paper's own
English abstract, and settling which is final would need the body text.
There are also approaches like Steven Pinker's *The Sense of Style*,
which re-examines the validity of such rules from a linguistics
foundation, but this crystal hasn't verified that book's specific
prescriptions (🟡, only the book's stated goal was confirmed). **The two
open-source sources in "Confirmed in practice" were read directly in the
original (🟢), but "these two are the best examples out there" was never
itself checked** — they're two cases found by search that happen to fit
this crystal's argument well, not the result of surveying every major
open-source project's language guidelines and comparing them.

## Per-source copyright and ethics review

Requested directly: separately from whether the "Grounding" sources
above are accurate (already checked), is it actually safe to record
each one, verbatim quotes included, in this public repository? The
standard applied: the three tests Korean copyright law's Article 28
(quotation of a published work) uses — (1) is the quote subordinate to
this crystal's own writing (not the other way around), (2) is it the
minimum needed, (3) is the source fully credited — plus the separate
principle that facts, statistics, and ideas themselves were never
copyrightable material in the first place.

| Source | What was actually carried over | Copyright status | Why it's safe |
|---|---|---|---|
| Orwell (1946) | 2 of 6 rules, quoted as short phrases | Public domain in life+70 countries (UK etc., since 2021); US status not directly confirmed | A handful of short phrases, not a substitute for the essay's own argument — subordinate and minimal |
| Graham | Two quoted sentences | Author holds copyright; no separate open license found | Two sentences only, fully credited, for commentary — safe regardless of license |
| Strunk (1918 original) | Short phrases like "Omit needless words" | Confirmed public domain in the US (full text distributed via Project Gutenberg) | Public domain, so the quotation test doesn't even apply — though citing it under the common name "Strunk & White" is worth flagging: the actual quoted wording is Strunk's 1918 original, not E.B. White's still-copyrighted 1959 revision |
| Zinsser (1976) | Two quoted sentences | Author died 2015; copyright still active | Two sentences only, fully credited |
| Vonnegut (1980) | Titles of 4 of 7 rules (a few words each) | Held by International Paper Co., actively rights-managed (many reprints carry "reprinted with permission") | Only rule titles were quoted — short, low in original expression, not the essay's actual prose |
| Kawasaki (2005) | The rule itself (10 slides / 20 minutes / 30pt), described, not quoted | Held by Kawasaki personally | A numeric rule is a fact/idea, not expression — never copyrightable to begin with |
| Lee O-deok (1992) | No quote at all — only a Wikipedia-sourced summary | Original never opened; copyright status not checked | Nothing was carried over from the book itself — this was never a quotation |
| Kim 2012 | One definition sentence + 4 example pairs | Published by NIKL, but authored by an outside professor — no KOGL open-license mark found on this issue's colophon | Meets all three Article 28 tests (detailed in the answer this table follows) — safe independent of whether KOGL applies |
| Chen & Lee (2022) | The abstract's core claim, summarized in this crystal's own words | KCI abstract page; full text not opened | No sentence from the abstract was quoted verbatim — facts and ideas aren't copyrightable material |
| Park (2012) | Statistics only | KCI abstract page; full text not opened | Numbers and statistics are facts, not copyrightable expression |
| Kubernetes localization guide | A 4-row example table, reproduced as-is | CC BY 4.0 — reuse explicitly permitted | The license itself permits this; source (repo, URL, license) credited |
| GitHub docs | Two rules, quoted verbatim | Prose content under CC BY 4.0 (code separately under MIT) | The license itself permits this |
| Pinker, *The Sense of Style* | Nothing (title and topic only) | N/A | Nothing was carried over from the book |

**Conclusion**: every source where actual text was carried over (Orwell,
Graham, Strunk, Zinsser, Vonnegut, Kim 2012, Kubernetes, GitHub docs) is
(a) a handful of sentences or fewer, (b) fully credited, and (c)
subordinate to this crystal's own, much longer discussion — meeting
Article 28's test (or the more permissive terms of an explicit CC BY
license). Sources where only facts, statistics, or ideas were carried
over (Chen & Lee, Park, Lee O-deok, Kawasaki, Pinker) were never
copyrightable material to begin with. Nothing here raises a privacy,
defamation, or harmful-information concern — every source is either a
published academic paper, publicly available writing advice, or
official open-source project documentation (Chen & Lee 2022 covers a
historically sensitive period — Japanese colonial rule — but the only
thing carried over from it is a single, neutral linguistic fact about
that period, not any judgment about the period itself).

**Honest limitations**: this review is this crystal's own applied
judgment, not legal advice. Whether Orwell's essay is still under
copyright in the US, and whether Kim 2012 actually falls under NIKL's
KOGL open-use policy, were both left unconfirmed — the underlying
copyright notices weren't directly available to check. Both quotations
are short enough, though, that Article 28's own test is met regardless
of how either question resolves.

## Related
- [01-definition-of-done.md](01-definition-of-done.md) — this crystal
  looks at "does it read well," not "is it done" — the two don't
  substitute for each other
- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  the content-accuracy axis; this crystal is the delivery axis
