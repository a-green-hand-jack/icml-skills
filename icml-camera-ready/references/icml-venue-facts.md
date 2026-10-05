# ICML Venue Facts (Snapshot: ICML 2026)

**Snapshot date:** 2026-10-05. **Applies to:** ICML 2026 (Seoul, July 6–11, 2026).
All numbers and policies here are year-specific. To reuse in a new cycle,
please refresh first (see "How to refresh" at the bottom). When this file
conflicts with the official online page, the online page prevails.

Official sources used to build this snapshot:
- Author instructions: https://icml.cc/Conferences/2026/AuthorInstructions
- Call for papers: https://icml.cc/Conferences/2026/CallForPapers
- Reviewer instructions: https://icml.cc/Conferences/2026/ReviewerInstructions
- Example paper (PDF): https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- Style files: https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. Format (Submission)

| Item | Requirement |
|---|---|
| Main text | **At most 8 pages** — exceeding this triggers automatic rejection |
| References, appendix, impact statement | Unlimited pages, merged into a single PDF |
| Typesetting | LaTeX only, official `icml2026.sty`, `\usepackage{icml2026}` (do not use `accepted` option) |
| Layout | Two-column, US Letter (not A4), 10pt Times |
| Style modifications | Prohibited. Do not alter the template or compress vertical spacing |
| Submission PDF size | 50 MB (author instructions page). The example paper still says 10 MB; follow the author instructions page and keep it small |
| Abstract | One paragraph, ideally 4–6 sentences. Serious violations must be corrected at the camera-ready stage |
| Title and heading levels | Title case for content words, no ALL CAPS. At most three heading levels |
| Figures | Captions **below**; no titles inside the figure; label axes; every curve needs a legend; use vector formats (PDF/EPS) |
| Tables | Titles **above** |
| Pseudocode | `algorithm` + `algorithmic` environments (provided with the style file) |
| Citations | Use `natbib` + `icml2026.bst` APA author–year format. Multiple citations in chronological order. Protect capitals in BibTeX titles: `{B}ayesian`, `{L}ipschitz` |
| Fonts | The example paper requires Type-1 fonts; the 2026 camera-ready instructions no longer check for Type 3. Use pdflatex with vector graphics; treat Type 3 as a warning |

## 2. Anonymity (Double-blind)

- Do not display author names or affiliations (the style hides `\icmlauthor` when the `accepted` option is absent).
- No acknowledgments, grant numbers, or links to public (non-anonymous) code repositories.
- Cite your own previous work in the third person. Do not write "In our previous work (X, 2024), we proved ..."
- Entries in the reference list **do not** need to be anonymized, except for unpublished work from your group (e.g., under review at another conference), which should be cited anonymously and uploaded in the anonymized supplementary material.
- Submissions with substantial overlap with prior papers must (anonymously) cite them and explain the differences.
- arXiv preprints are allowed, but the submission must not cite a non-anonymous version, and the work must not be publicized as an ICML submission during review.
- Rebuttal text must also be anonymous (see §6).

## 3. Required and Optional Sections

- **Impact Statement (required for main track):** An unnumbered section placed at the end of the paper, parallel to acknowledgments and before references; does not count toward the page limit. If the impact is merely conventional progress advancing the field of machine learning, the following sentence may be used verbatim:
  > "This research aims to advance the field of machine learning. Our work may lead to a variety of potential societal impacts, and we do not believe it is necessary to highlight any particular one here."

  Authors are encouraged to elaborate when appropriate; if the paper is flagged for ethics review, this statement will be read.
- **Acknowledgments:** Allowed only at the camera-ready stage.
- **Limitations:** ICML does not mandate this section, but reviewers are instructed to reward rather than penalize honest discussions of limitations. It is recommended to include one.
- **Position Paper Track (separate track):** The title must indicate a position; the abstract must state the position ("This position paper argues ..."); the introduction must highlight the position in bold; the body must contain an **Alternative Views** section; no impact statement is required.

## 4. Supplementary Material

- Text appendices go in the main PDF (unlimited pages). Reviewers are **not required** to read appendices or supplementary material: any critical content must be included within the 8-page main text.
- Code/data: Upload as zip or PDF, anonymized (remove names and licenses), or provide an anonymous GitHub repository branch frozen after the deadline (place the link in a text file inside the zip).
- Code submission is encouraged; reproducibility is factored into the decision.
- No supplementary material of any kind is accepted for the camera-ready version.

## 5. Policy on AI-Assisted Writing

- LLMs may assist with writing and research; **authors bear full responsibility** for all content, including anything that may be deemed plagiarism or misconduct. Authors are encouraged to describe significant LLM usage in the Methods section.
- LLMs cannot be listed as authors.
- **Prompt injection is prohibited and will result in direct rejection** (text intended to manipulate LLM reviewers). Organizers will run detectors. The February 2026 update clarifies that prompts used solely to *detect* whether a reviewer uses an LLM will not be penalized — this skill family still never inserts any hidden or reviewer-facing text.
- Reviewers are informed that submitting low-quality AI-generated content ("AI slop") may constitute misconduct and can be reported.
- Plagiarism in any form is prohibited. Do not copy sentences from other papers.
- Dual submission of substantially similar work is prohibited; parallel ICML submissions by the same author are treated as prior work to each other.

## 6. Review Process and Author Response (2026)

- Review form dimensions, each 1–4 points: **Soundness, Presentation, Significance, Originality**. Overall recommendation 1–6 points (6 strong accept, 5 accept, 4 weak accept, 3 weak reject, 2 reject, 1 strong reject). Confidence 1–5 points.
- Reviewer instructions: originality does not require proposing a new method (new insights into existing methods also count); soundness and impact are assessed separately; honest discussions of limitations should be rewarded.
- Reviewers provide 3–5 numbered "key questions" whose answers could change the review.
- Concurrent work: work made public within two months before the full-paper deadline is considered concurrent; authors need not discuss it.
- **Author response:** Three rounds of author–reviewer discussion (author rebuttal, reviewer follow-up, author follow-up), **each round limited to 5,000 characters**. Please confirm on OpenReview whether this limit is per reply/thread or total.
- **No revised PDF may be uploaded** during the response period.
- Responses must be anonymous: no non-anonymous URLs, personal website URLs, or short links (they may log reviewer IP). Reviewers are not required to access external links.
- There is no need to respond to every trivial question. Organize by reviewer number. Keep it professional and polite.
- Reviewers must acknowledge responses and write a "final justification" after the rebuttal, stating whether the rebuttal addressed their concerns.
- **Publicity:** For accepted papers, the original submission, anonymous reviews, meta-review, rebuttal, and discussion will be public on OpenReview. Rejected papers may opt in to be public. Write every response assuming it will be made public.

## 7. Camera-Ready (2026)

- Deadline (2026): May 28, AoE 23:59. Presentation questionnaire deadline May 11.
- `\usepackage[accepted]{icml2026}`; main text **9 pages**, followed by acknowledgments, impact statement, references, appendix. PDF ≤ 20 MB. US Letter.
- Author block follows `example_paper.tex`; call `\printAffiliationsAndNotice{\icmlEqualContribution}` or `\printAffiliationsAndNotice{}`. Affiliations must match the OpenReview profile.
- Author order may be adjusted; **authors may not be added or removed**. Must match OpenReview.
- Title and abstract may only be modified slightly (significant title changes require PC permission). The title and abstract entered in the OpenReview form must match the PDF exactly; minimal TeX math is allowed, no custom macros, accents entered via TeX commands.
- Core content must remain unchanged relative to the reviewed version (the original submission will be published alongside).
- **Conflict of Interest Disclosure (new for 2026):** If any financial/substantial conflict of interest exists (e.g., evaluating a model built by an author's employer), add a paragraph titled "Conflict of Interest Disclosure" in the **last paragraph of the introduction**. Omit entirely if there is no conflict. Pure industry employment does not constitute a conflict.
- References: correct bibliographic data; replace arXiv citations with peer-reviewed versions where possible; fix entries listed under "Reference Correctness Check" in the OpenReview decision; protect capitals in BibTeX.
- Code/data: place in a public archival repository and link in the paper; optionally fill in the OpenReview "code url" field.
- **Lay summary** is entered in OpenReview. 2026 guidance (same as 2025): at most 10 sentences / 200 words; understandable by a science journalist; specific enough that it could not describe any other ICML paper; think of it as a paper trailer. Source: https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- Run the ICML format checker (https://papercheck.icml.cc/papercheck.html) until no errors remain; enter the 5-digit code it returns in the camera-ready form.
- Forms: PMLR publication agreement (upload, ≤10 MB), ICML publication license (signed by one author), oral presentation video license.
- Registration: at least one author must register (in-person attendance selects Conference option; publication-only selects Conference or Virtual Pass).
- Accessibility: color-vision-friendly figures, up-to-date reference names and conference names, inclusive language.
- A post-conference revision window allows minor corrections before PMLR publication.

## 8. Key Dates for 2026 (Historical Reference)

Abstract deadline January 23, 2026 AoE; full paper January 28, 2026 AoE; review deadline March 12; author–reviewer discussion March 24 – April 7; notification April 30; camera-ready May 28. Deadlines are strict, no extensions. Author list cannot change after the abstract deadline.

---

## How to Refresh This File for a New Cycle

1. If you have internet, obtain the year's author instructions, call for papers, reviewer instructions, and example paper (replace `2026` in the URLs above with the target year; if the page 404s, navigate from https://icml.cc).
2. Diff each item in the table above against the official page. Update the numbers, note the new snapshot date and year at the top, and list changes under "Changelog".
3. Write the refreshed copy into the project workspace at `.icml/venue_facts.md` (skills read the workspace copy during a project).
4. If unobtainable, explicitly tell the user: "Using ICML 2026 rules (snapshot 2026-10-05); please confirm they still apply to your target year." Never assume silently.

## Changelog
- 2026-10-05: Initial snapshot created from ICML 2026 official pages.
