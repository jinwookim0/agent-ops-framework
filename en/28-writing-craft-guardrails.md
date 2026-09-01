<!-- translated-from: ssot=sha256:9431d3fe68e4 own=sha256:65a1585c0c49 -->
# Writing Craft Guardrails — Removing the "AI Smell"

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/28-writing-craft-guardrails.md)**

**Version**: 1.1.0
**Content hash**: sha256:6f61771927ec (of the body below, excluding the stamp comment, this line, and the version line)

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
linguistically generalized finding. There are also approaches like
Steven Pinker's *The Sense of Style*, which re-examines the validity of
such rules from a linguistics foundation, but this crystal hasn't
verified that book's specific prescriptions (🟡, only the book's stated
goal was confirmed).

## Related
- [01-definition-of-done.md](01-definition-of-done.md) — this crystal
  looks at "does it read well," not "is it done" — the two don't
  substitute for each other
- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  the content-accuracy axis; this crystal is the delivery axis
