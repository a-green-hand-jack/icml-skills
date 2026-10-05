# Citation Rules for ICML Papers

Sources: ICML 2026 example paper and author instructions; Foerster, "How to ML Paper";
Lipton (2018). Year-specific details live in `icml-venue-facts.md`.

## Format
- Style: APA author–year. LaTeX: `\usepackage{natbib}` is loaded by the ICML style;
  use `\bibliographystyle{icml2026}` (year-specific `.bst` from the style package).
- In text: "Samuel (1959) showed ..." → `\citet{samuel1959}`; "... checkers (Samuel,
  1959)" → `\citep{samuel1959}`. Several: `\citep{a,b,c}` ordered chronologically.
- `\citep[e.g.,][]{key}`, `\citep[see][Sec.~3]{key}` for pre/post notes.
- Acronym plus citation: "proximal policy optimization \citep[PPO;][]{schulman2017ppo}"
  or introduce the acronym in text and cite once.
- "et al." is produced by the style for three or more authors; do not type it into
  author fields.
- References: unnumbered first-level heading (the style handles it), alphabetical,
  complete (pages where available), consistent, current author names.

## BibTeX hygiene
- Protect capitals in titles: `{B}ayesian`, `{L}ipschitz`, `{MCMC}`, `{GPT}-4`,
  `{T}ransformers`. BibTeX styles lowercase unprotected title words.
- Required fields: `@inproceedings` author, title, booktitle, year (pages, publisher
  welcome); `@article` author, title, journal, year (volume, number, pages);
  `@misc`/arXiv: author, title, year, and eprint/archivePrefix or howpublished/url.
- Consistent venue names (pick "Proceedings of the 41st International Conference on
  Machine Learning" or "International Conference on Machine Learning", not both).
- One entry per work; no duplicate keys for the same paper.
- Keep keys stable once used; never rename a key the co-authors rely on without asking.
- Cite the published version when it exists (conference/journal), not arXiv.

## Anonymity (submission)
- Third person for own prior work: "Doe et al. (2024) showed ...", never "our previous
  work showed".
- Do not remove or anonymize published own papers from the reference list.
- Unpublished own work that the submission depends on: cite as "Anonymous (2026)" or
  the style's anonymous form, and upload an anonymized copy as supplementary material.
- No acknowledgements, no grant numbers, no links to non-anonymous repositories.

## What and when to cite (Lipton, Foerster, ICML reviewer instructions)
- Cite every claim not supported by your own experiments; avoid broad claims you cannot
  cite.
- Cite throughout the paper wherever a prior method is used, not only in related work.
- Cite generously where relevant - reviewers are likely authors of related work - but
  do not pad with irrelevant work.
- Assign credit correctly, including the first instance of an idea when known.
- Never misrepresent what a cited paper says. If you have not checked it, do not use it
  to support a specific claim.
- Concurrent work (public < 2 months before the deadline) is optional at ICML.

## Camera-ready
- Replace arXiv with peer-reviewed versions where possible.
- Work through OpenReview's "Reference Correctness Check" list item by item, confirming
  each against a database record.
- Check capitalization in the compiled reference list.
- Add the public code/data URL if promised.
