# Writing an ICML Lay Summary

ICML has required accepted papers to submit a lay (plain-language) summary since 2025. The 2026 guidelines repeat the 2025 recommendations; please consult the blog post for that year.

## Requirements (2026)
- At most 10 sentences / 200 words.
- A science journalist should be able to understand it.
- Specific: it must not read like a description that could apply to any other ICML paper.
- Purpose: generate interest from people outside the subfield and broaden the paper's audience — like a trailer for the paper.

## Effective Structure
1. **Everyday problem** (1–2 sentences): describe what is wrong or still unclear in language a non-expert can understand; a concrete scenario is better than an abstract description.
2. **Why it is hard or why existing methods fall short** (1 sentence).
3. **What the authors did** (1–2 sentences): the core idea expressed with an analogy or plain description, without jargon.
4. **What they found** (1–2 sentences): the main result, giving a specific, meaningful number or comparison if possible.
5. **Why it matters** (1–2 sentences): who can use it, what it changes, and an honest statement of limitations if the result could be over-interpreted.

## Rules for the Agent
- Draft from approved claims in `.icml/claims.md`; do not add claims or use stronger wording than the paper supports. Lay readers tend to over-generalize, so state the scope explicitly ("in simulated robots", "for English text").
- Replace every technical term with a functional description ("a model that predicts the next word", not "autoregressive language model"); if a term is essential, explain it in at most five words.
- No hype words (breakthrough, revolutionary, human-like), no anthropomorphic expressions.
- Active voice, short sentences, concrete nouns.
- Count words and sentences before delivery.
- Provide two versions (e.g., one starting with a problem, one starting with a finding) so the authors can choose and edit.

## Self-Check
- Can the reader know what *this* paper discovered, not just its topic?
- Can a journalist quote any sentence without misrepresenting the result?
- Is every number in the ledger?
