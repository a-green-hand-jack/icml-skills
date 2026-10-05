# Section Guide for ICML Papers

Sources: Farquhar (2024), Foerster ("How to ML Paper - A brief Guide"), Nanda (2025),
Lipton (2018), Ethan Perez ("Easy Paper Writing Tips"), ICML 2026 author instructions.
Paraphrased; the decisions below are defaults, not laws.

## Contents
1. Reading order and where to spend effort
2. Title
3. Abstract
4. Figure 1
5. Introduction
6. Background vs. Related Work vs. Problem Setting
7. Method
8. Experimental setup and results
9. Limitations / Discussion / Conclusion
10. Impact Statement
11. Appendix
12. Figures and tables
13. Default section order

## 1. Reading order and where to spend effort

Readers meet a paper as: title → abstract → first-page figure → introduction → other
figures → (maybe) the rest. Reviewers form views early. Spend roughly equal effort on the
abstract, the introduction, the figures, and everything else combined (Nanda; Perez,
quoting Malik). In the 8-page ICML format, anything a reviewer needs to judge correctness
must be in the main body: reviewers are not required to read appendices.

## 2. Title

Content words capitalized, never all caps; TeX math sparingly; no custom macros. Aim for a
title that states the finding or the method's distinctive idea. Avoid puns that hide the
topic.

## 3. Abstract (one paragraph, about 4–6 sentences)

Goals: casual readers get the main insight; experts can decide whether to read on;
someone who read it years ago can recall the paper.

Default formula (Farquhar; Foerster and Lipton give close variants):
1. What you achieved ("We introduce / prove / show ..."). After this sentence the reader
   should already sense the contribution.
2. Why this is hard and important (situates it; a cold-start reader learns the subfield).
3. How you do it - a teaser with the keywords a specialist would skim for.
4–5. The evidence: main theorem or main empirical result, with the most remarkable number.
(Optional) 6. Implication / standard of evidence ("establishes", "provides evidence that").

Rules:
- Delete any opening sentence that could be prepended to any ML paper (Lipton).
- Do not tease; put the headline number in the abstract.
- Define any unavoidable jargon; prefer plain words.
- Two short sentences beat one long one; two medium-long sentences should be questioned.
- The OpenReview abstract field must match the PDF exactly (no custom macros).

## 4. Figure 1

Many readers look only at Figure 1. In ICML's two-column layout it belongs at the top of
the right column on page 1, across from the abstract. It should convey the core idea, the
approach, or the most compelling result - ideally something that would work as the first
image of a social-media thread. Its caption must stand alone: what is shown, how to read
it, the takeaway.

## 5. Introduction (about 1 page, never more than 1.5)

Default paragraph plan (merge Farquhar, Foerster, Nanda):
1. **Problem and why it matters** - specific, not field-level hype. Cite to establish the
   problem is real and people care. Optionally one sentence previewing the answer.
2. **Why it is hard / what prior work leaves open** - only the key prior work, cited
   generously; detailed prior work belongs in its own section.
3. **What we do** - the approach, its rough shape, and how it differs from the closest work.
4. **Evidence** - what kind of evidence follows and how seriously to take each claim; what
   evidence not to expect.
5. **Impact** - what readers should take away or do differently.
6. **Contribution list** - 2–4 bullets, each at most two lines in two-column format,
   each a concise claim with a pointer to its evidence (section/figure).
7. **(Camera-ready only, if applicable)** "Conflict of Interest Disclosure" paragraph,
   which must be the last paragraph of the introduction.

Avoid: misrepresenting prior work; a long literature recap; "LLMs have achieved remarkable
success" openers; "In Section 3 we will show" roadmaps that add nothing (a short roadmap is
fine if sections are unusual). Do not fear repeating the key claims in varied words -
repetition helps complex ideas stick.

## 6. Background vs. Related Work vs. Problem Setting

Foerster's distinction is the cleanest:
- **Background = academic ancestors**: concepts and prior work the reader needs to
  understand your method. Include something only if it is (a) essential, (b) not your
  contribution, (c) unfamiliar to many readers (Farquhar's three tests). Keep it brief;
  move boilerplate formalisms (e.g., the standard MDP definition) to an appendix.
- **Problem Setting / Formalism**: notation and assumptions your method uses; flag unusual
  assumptions. A separate section only if the setting itself is a contribution.
- **Related Work = academic siblings**: other attempts at the same problem. Compare and
  contrast - how do their assumptions or methods differ, and why does that matter here?
  Organize methodologically ("One line of work assumes A [refs]; we assume B because ..."),
  never paper-by-paper ("X et al. did ... Y et al. did ...").
- **Rule:** if a sibling method is applicable to your problem setting, it must appear as a
  baseline; if not, say in one sentence why it is not applicable.

Placement: put Related Work early (Section 2) only when the paper is motivated by a gap or
flaw in specific prior work; otherwise after the results, so the reader reaches your
contribution sooner. Record the choice in `decisions.md`.

Citations throughout (Lipton): cite prior methods wherever you use them, not only in the
related-work section. Cite generously when relevant - reviewers may be the authors.

## 7. Method

Someone who knows the problem and background, and trusts your experiments, should be able
to read only this section and know what you do and why. State the final design; put the
journey (alternatives you tried) in an appendix with a pointer ("we use cosine similarity;
Appendix B.2 compares alternatives"). Pseudocode in `algorithm`/`algorithmic`. List
hyperparameters (main ones here, full lists in the appendix). The method should start on
page 2 and virtually never after page 3.

## 8. Experimental setup and results

Setup: the concrete instantiation of the problem, datasets, baselines (and how they were
tuned), metrics, compute, seeds. Enough for an expert to roughly reimplement; full detail
in the appendix.

Results: give each claim (or each experiment) its own subsection. Each subsection:
1. A signpost sentence: what this experiment shows and which claim it supports.
2. How it connects to the main contribution.
3. The setting, briefly, with an appendix pointer.
4. Exactly what to look at: name the lines, rows or points in the figure/table that
   support the claim ("the orange curve stays below ... after step 2k").
5. Statistics: number of runs, error-bar meaning, significance where relevant.

Double-check that every textual description of a figure or table is literally true of it.
Reviewers frequently find text that misdescribes its own figures.

Include ablations, hyperparameter sensitivity, fairness of comparisons, and failure cases.

## 9. Limitations / Discussion / Conclusion

- **Limitations**: be honest and specific - ICML reviewers are instructed to reward
  upfront limitations. Also explain why a limitation does not undermine the main claims
  when that is true. Frame "future work" as limitations (Farquhar).
- **Discussion**: implications, takeaways, open questions - only if there is something
  worth saying.
- **Conclusion**: optional and short (2–4 sentences). Under page pressure, shrink it first.

## 10. Impact Statement (required for the ICML main track)

Unnumbered section after the conclusion, before references, alongside acknowledgements;
not counted in the page limit. The official boilerplate sentence may be used when the
work raises only the generic societal implications of ML research. Prefer a specific
statement when the work touches surveillance, persuasion, bio/cyber capabilities,
privacy, fairness, dual use, or deployed systems - ethics reviewers read it if the paper
is flagged. Never use it to restate contributions.

## 11. Appendix

Everything that is useful but not essential: full proofs, extended setups and
hyperparameters, extra results, more examples, a glossary of terms, alternatives tried.
Appendices are held to a lower polish standard but must not contradict the main text.
Nanda suggests an appendix for tacit knowledge (what was hard, what failed, practical
advice) - valuable for readers, and a good place for honest detail.

## 12. Figures and tables

- Decide the single takeaway before plotting; design the plot to make that takeaway
  visible (highlight the key line, fade others, annotate).
- Axis labels and tick labels at least as large as body text; legend for every curve.
- Vector PDF for plots. No title inside the graphic - the caption does that job.
- Captions: figure below, table above (ICML). State what is shown, how to read it
  (is higher better?), and the takeaway; 1–3 lines when possible (Lipton).
- Colorblind-safe palettes (e.g., viridis, Okabe–Ito); avoid red/green as the only
  contrast; check grayscale readability. Heatmaps: sequential scale from white at zero
  for nonnegative data; diverging scale with white at zero for signed data.
- Tables: `booktabs`, consistent decimals, units in headers, ↑/↓ for metric direction,
  bold the best value only when the difference exceeds noise; report ± with its meaning.
- A reader should get the story from the figures alone, and also from the text alone
  (Lipton).

## 13. Default section order

1 Introduction → 2 Background (and Problem Setting) → 3 Method → 4 Experimental Setup →
5 Results → 6 Related Work → 7 Limitations and Conclusion → Impact Statement (unnumbered)
→ References → Appendix. Move Related Work to Section 2 when the motivation depends on it.
