<!-- translated-from: ssot=sha256:279908309083 own=sha256:0df82eec6b30 -->
# Writing Craft Guardrails — Removing the "AI Smell"

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/28-writing-craft-guardrails.md)**

**Version**: 1.0.0
**Content hash**: sha256:5b60ce1c3016 (of the body below, excluding the stamp comment, this line, and the version line)

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

## Honest limitations

Most of the principles this crystal cites come from the English prose
tradition — writing-critique traditions in other languages (e.g. critiques
of translationese) need their own primary sources verified separately per
project; this crystal doesn't verify those on your behalf. There are also
approaches like Steven Pinker's *The Sense of Style*, which re-examines the
validity of such rules from a linguistics foundation, but this crystal has
not verified that book's specific prescriptions (🟡, only the book's stated
goal was confirmed).

## Related
- [01-definition-of-done.md](01-definition-of-done.md) — this crystal
  looks at "does it read well," not "is it done" — the two don't
  substitute for each other
- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) —
  the content-accuracy axis; this crystal is the delivery axis
