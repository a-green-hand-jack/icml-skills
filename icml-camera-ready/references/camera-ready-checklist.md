# Camera-Ready Checklist (ICML 2026 baseline — verify against the current year)

Copy into `.icml/camera_ready.md` and tick items as they are verified (not as they are
"probably done").

## Timeline
- [ ] Camera-ready deadline and AoE time noted (2026: May 28, 11:59pm AoE)
- [ ] In-person presentation questionnaire submitted (2026: by May 11) — authors
- [ ] Registration by at least one author (Conference option for in-person; Conference or Virtual Pass for proceedings-only) — authors

## Content
- [ ] Every item in `promises.md` present and identical to the rebuttal
- [ ] Main body ≤ 9 pages; extra space used for reviewer feedback, not new claims
- [ ] Essential content unchanged vs. reviewed version (diff the PDFs/abstract)
- [ ] Conflict of Interest Disclosure: asked authors; added as last paragraph of the intro if applicable; omitted otherwise
- [ ] Impact Statement present (main track), unnumbered, before references
- [ ] Acknowledgements added (unnumbered, before references), wording approved by authors
- [ ] Limitations still accurate after changes

## Authors and front matter
- [ ] `\usepackage[accepted]{icml20XX}`
- [ ] Names, order, affiliations match OpenReview profiles; no additions/removals
- [ ] Equal-contribution marks and `\printAffiliationsAndNotice{...}` render correctly
- [ ] Corresponding author(s) and emails
- [ ] Running title fits (use `\icmltitlerunning{}` if needed)
- [ ] Title change (if any) is small or approved by PCs

## References
- [ ] Reference Correctness Check items from the OpenReview decision fixed
- [ ] arXiv citations replaced with published versions where possible
- [ ] Capitalization protected; names and venues current; no duplicates
- [ ] No `??` / `(?)`

## Format
- [ ] US Letter; official style unmodified; no spacing hacks
- [ ] PDF ≤ 20 MB; appendices included in the same PDF (no camera-ready supplementary)
- [ ] Title/headings: content words capitalized, not all caps
- [ ] Abstract: one paragraph, ~4–6 sentences
- [ ] Citation font size equals body text
- [ ] Vector graphics for plots; accessible colors; inclusive language
- [ ] `check_submission.py --mode camera-ready` has no ERROR
- [ ] ICML paper checker passed; 5-letter code recorded — authors

## Code and data
- [ ] Public archival repository; link in the paper; "code url" field on OpenReview
- [ ] Repo cleaned (no `.icml/` notes, secrets, internal paths); license; README

## OpenReview form — authors submit
- [ ] Title and abstract text exactly match the PDF (no custom macros; TeX accents)
- [ ] Lay summary (≤ 10 sentences / 200 words in 2026)
- [ ] Camera-ready PDF uploaded
- [ ] PMLR Publication Agreement signed by corresponding author and uploaded (≤ 10 MB)
- [ ] ICML Publishing Release signed (one author); Recording Release (oral presenters)
