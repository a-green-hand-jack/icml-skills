# ICML Citation Rules

Sources: ICML 2026 sample paper and author instructions; Foerster, "How to ML Paper";
Lipton (2018). Year-specific details are in `icml-venue-facts.md`.

## Format
- Style: APA author-year. LaTeX: `\usepackage{natbib}` is loaded automatically by the ICML style;
  use `\bibliographystyle{icml2026}` (the year-specific `.bst` from the style package).
- In-text: "Samuel (1959) showed ..." → `\citet{samuel1959}`; "... checkers (Samuel,
  1959)" → `\citep{samuel1959}`. Multiple: `\citep{a,b,c}` in chronological order.
- `\citep[e.g.,][]{key}`, `\citep[see][Sec.~3]{key}` for pre/post-notes.
- Acronyms with citation: "proximal policy optimization \citep[PPO;][]{schulman2017ppo}"
  or introduce the acronym in the text and cite only once.
- For three or more authors, the style automatically generates "et al."; do not type it manually in the author field.
- References: unnumbered first-level heading (handled by the style), alphabetically ordered, complete (include page numbers when possible), consistent, author names kept up to date.

## BibTeX Specifications
- Protect uppercase letters in titles: `{B}ayesian`, `{L}ipschitz`, `{MCMC}`, `{GPT}-4`,
  `{T}ransformers`. BibTeX styles will lowercase unprotected title words.
- Required fields: `@inproceedings` author, title, booktitle, year (pages, publisher welcome);
  `@article` author, title, journal, year (volume, number, pages);
  `@misc`/arXiv: author, title, year, and eprint/archivePrefix or howpublished/url.
- Consistent conference names (use either "Proceedings of the 41st International Conference on
  Machine Learning" or "International Conference on Machine Learning" uniformly, do not mix them).
- Keep only one entry per work; do not duplicate keys for the same paper.
- Keep keys stable once used; never rename a key that collaborators depend on without their consent.
- When a published version exists (conference/journal), cite the published version, not arXiv.

## Anonymity (Submission Stage)
- Cite your own prior work in the third person: "Doe et al. (2024) showed ...", never write "our previous
  work showed".
- Do not remove or anonymize your own published papers from the reference list.
- Unpublished work of your own that the submission relies on: cite anonymously as "Anonymous (2026)" or in the style's anonymous form,
  and upload an anonymous copy as supplementary material.
- No acknowledgments, no grant numbers, no links to non-anonymous repositories.

## What and When to Cite (Lipton, Foerster, ICML reviewer instructions)
- Cite every claim that your own experiments cannot support; avoid broad claims you cannot cite.
- Cite prior methods wherever they are used in the paper, not only in the related-work section.
- Be generous with citations where relevant—reviewers are likely authors of the related work—but do not pad with irrelevant work.
- Properly attribute credit, including the first known appearance of an idea.
- Never misrepresent the content of a cited paper. If you have not checked it, do not use it to support a specific claim.
- Concurrent work (made public less than two months before the deadline) is optional to cite for ICML.

## Camera-Ready
- Replace arXiv with published versions whenever possible.
- Address every item in the OpenReview "Reference Correctness Check", confirming each against database records.
- Check capitalization in the compiled reference list.
- If promised, add public code/data URLs.
