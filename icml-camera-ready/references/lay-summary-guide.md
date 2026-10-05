# Writing the ICML Lay Summary

ICML has required a lay (plain-language) summary for accepted papers since 2025. The
2026 guidance repeated the 2025 advice; check the current year's blog post.

## Requirements (2026)
- At most 10 sentences / 200 words.
- A science journalist should be able to understand it.
- Specific: it must not read like it could describe any other ICML paper.
- Purpose: interest people outside the subfield and widen the paper's reach - like a
  trailer for the paper.

## Structure that works
1. **The everyday problem** (1–2 sentences): what goes wrong or is unknown, in terms a
   non-specialist recognises. Concrete setting beats abstraction.
2. **Why it is hard or why existing approaches fall short** (1 sentence).
3. **What the authors did** (1–2 sentences): the core idea as an analogy or plain
   description, no jargon.
4. **What they found** (1–2 sentences): the main result with one concrete, meaningful
   number or comparison where possible.
5. **Why it matters** (1–2 sentences): who could use it, what it changes, and an honest
   limit if the result could be over-read.

## Rules for the agent
- Draft from the approved claims in `.icml/claims.md`; do not add claims or stronger
  wording than the paper supports. Lay audiences over-generalise easily, so state scope
  plainly ("in simulated robots", "for English text").
- Replace each technical term with what it does ("a model that predicts the next word",
  not "an autoregressive language model"); if a term is essential, explain it in five
  words or fewer.
- No hype words (breakthrough, revolutionary, human-like) and no anthropomorphism.
- Active voice, short sentences, concrete nouns.
- Count words and sentences before handing over.
- Provide two variants (e.g., one leading with the problem, one with the finding) and
  let the authors choose and edit.

## Self-check
- Would a reader know what *this* paper found, not just its topic?
- Could a journalist quote any sentence without misrepresenting the result?
- Is every number in the ledger?
