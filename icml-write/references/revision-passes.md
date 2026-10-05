# Revision Passes

Run the passes in this order. Earlier passes change structure; later passes polish
sentences that survived. Polishing sentences you later delete is wasted work. Log each
completed pass in `.icml/state.md`.

## Pass 1 — Structure (whole paper)

Tools: `python scripts/extract_outline.py main.tex > .icml/reverse_outline.md`

- Read the reverse outline alone. Does it tell the narrative from `claims.md`? Is each
  claim introduced, supported, and discussed?
- Every section and subsection: can you say what goes wrong if it is cut (Nanda)? If not,
  cut or move to the appendix.
- Section roles match `section-guide.md` (no results in method, no method in results,
  background passes the three tests).
- Page budget: intro ≤ ~1 page; method starts by page 2–3.
- Related-work ↔ experiments map is satisfied (every applicable sibling is compared or
  excused).
- Figure 1 exists and communicates the main idea or result.

## Pass 2 — Paragraphs

Reference: `prose-principles.md` §2–4.

- One point per paragraph, matching its TL;DR. First sentence states the point.
- Topic positions form a thread; stress positions carry the new information.
- Transitions are logically true. Gaps → `open_issues.md`, never invented links.
- Results paragraphs say exactly what to look at in the figure/table.

## Pass 3 — Sentences

Tools: `python scripts/lint_prose.py main.tex` (advisory).

- Subject–verb proximity, action in verbs, no empty hedges or intensifiers, no vague
  pronouns, no comparatives without a comparison, no future tense, no anthropomorphism,
  no LLM-tell vocabulary (`prose-principles.md` §7).
- Each lint hit: fix it, or keep it with a reason (log significant ones in
  `decisions.md`). Do not mechanically "fix" passive voice that keeps a paragraph's topic
  in front.

## Pass 4 — Cut

- Aim to delete about one third of the words in the draft (Foerster). First cut words,
  then sentences, then subsections (Farquhar). Stop when text becomes cramped: past a
  point, fewer well-chosen ideas beat compressed ones.
- Remove single-word last lines; reduce whitespace legitimately (tighter wording, merged
  tables, better figure sizing) - never by changing the template's spacing.
- Re-check the page limit with `check_submission.py --pdf`.

## Pass 5 — Consistency

- One term per concept across text, figures, tables and appendix; same symbol meanings.
- Contribution list, abstract, intro and conclusion make the same claims at the same
  strength as `claims.md`.
- Figure/table descriptions in the text are literally true of the figures/tables.
- Tense, spelling variety, citation commands, capitalization of method names.
- Appendix does not contradict the main text.

## Pass 6 — Numbers, references, compliance

Tools:
- `python scripts/check_numbers.py main.tex --ledger .icml/claims.md`
- icml-cite's `check_bib.py` (if installed) or at least confirm every `\cite` key exists
  and is verified in `citations_log.md`.
- `python scripts/check_submission.py --tex main.tex --pdf main.pdf --names "..." --affils "..."`

Everything must pass with no ERROR, or each ERROR must be explicitly waived by the human.

## Light polish (when the user only wants polish)

Run Passes 3, 4 (light), 5 and 6. Still stop and flag gaps rather than inventing links.
