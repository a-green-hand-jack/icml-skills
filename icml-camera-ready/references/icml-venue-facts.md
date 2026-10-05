# ICML Venue Facts (snapshot: ICML 2026)

**Snapshot date:** 2026-10-05. **Applies to:** ICML 2026 (Seoul, July 6–11, 2026).
Every number and policy here is year-specific. Before relying on it for a new cycle,
refresh it (see "How to refresh" at the bottom). When this file and the live official
pages disagree, the live pages win.

Official sources this snapshot was built from:
- Author Instructions: https://icml.cc/Conferences/2026/AuthorInstructions
- Call for Papers: https://icml.cc/Conferences/2026/CallForPapers
- Reviewer Instructions: https://icml.cc/Conferences/2026/ReviewerInstructions
- Example paper (PDF): https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- Style files: https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. Format (submission)

| Item | Requirement |
|---|---|
| Main body | **8 pages max** — exceeding it means automatic rejection |
| References, appendices, Impact Statement | Unlimited pages, same single PDF |
| Typesetting | LaTeX only, official `icml2026.sty`, `\usepackage{icml2026}` (no `accepted` option) |
| Layout | Two columns, US Letter (not A4), 10pt Times |
| Style changes | Forbidden. Do not alter the template or compress vertical spacing |
| Submission PDF size | 50 MB (Author Instructions page). The example paper still says 10 MB; follow the Author Instructions page and stay small anyway |
| Abstract | One paragraph, ideally 4–6 sentences. Gross violations must be fixed at camera-ready |
| Title and headings | Content words capitalized, never ALL CAPS. At most three heading levels |
| Figures | Caption **below**; no title inside the graphic; label axes; legend for each curve; vector (PDF/EPS) for plots |
| Tables | Caption **above** |
| Pseudocode | `algorithm` + `algorithmic` environments (supplied with the style files) |
| Citations | APA author–year via `natbib` + `icml2026.bst`. Multiple citations in chronological order. Protect capitals in BibTeX titles: `{B}ayesian`, `{L}ipschitz` |
| Fonts | Example paper asks for Type-1 fonts; 2026 camera-ready notes there is no Type 3 check. Use pdflatex and vector figures; treat Type 3 as a warning |

## 2. Anonymity (double-blind)

- No author names or affiliations visible (the style hides `\icmlauthor` unless `accepted`).
- No acknowledgements, grant numbers, or links to public (non-anonymous) code repositories.
- Refer to your own prior work in the third person. Never write "in our previous work (X, 2024) we showed".
- Do NOT anonymize entries in the reference list, except unpublished own work (e.g., under review elsewhere), which is cited as an anonymous reference and uploaded as anonymized Supplementary Material.
- Prior own papers with substantial overlap must be cited (anonymously) and the differences explained.
- arXiv preprints are allowed, but the submission must not refer to the non-anonymous version, and the work must not be advertised as an ICML submission during review.
- Rebuttal text must also be anonymous (see §6).

## 3. Required and optional sections

- **Impact Statement (required, main track):** unnumbered section at the end of the paper, co-located with Acknowledgements, before References; does not count toward the page limit. When impacts are the standard ones for advancing ML, this sentence may be used verbatim:
  > "This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here."

  Authors are encouraged to say more when warranted; the statement is read if the paper is flagged for ethics review.
- **Acknowledgements:** camera-ready only.
- **Limitations:** not a mandated section at ICML, but reviewers are told to reward, not punish, honest discussion of limitations. Include one.
- **Position paper track (separate track):** title must state the position; abstract states it ("This position paper argues that ..."); position in bold in the introduction; a mandatory **Alternative Views** section in the main body; no Impact Statement required.

## 4. Supplementary material

- Text appendices go in the main PDF (unlimited). Reviewers are not required to read appendices or supplementary material: anything critical must be in the 8 pages.
- Code/data: zip or PDF upload, anonymized (remove names and licenses), or an anonymous GitHub repo on a branch frozen after the deadline (link in a text file inside the zip).
- Code submission is encouraged; reproducibility is considered in decisions.
- No camera-ready supplementary material of any kind.

## 5. Policies relevant to AI-assisted writing

- LLMs may assist writing and research; **authors take full responsibility** for all content, including anything that could be construed as plagiarism or misconduct. Authors are encouraged to describe notable ways LLMs were used in the research methodology.
- LLMs cannot be authors.
- **Prompt injection is forbidden and leads to desk rejection** (text crafted to manipulate LLM reviewers). Organizers run detectors. A Feb 2026 update said prompts merely designed to *detect* reviewer LLM use are not penalized — this skill family still never inserts any hidden or reviewer-directed text.
- Reviewers are told that submitting low-quality AI-generated content ("AI slop") may be misconduct and can be reported.
- Plagiarism in any form is forbidden. Never copy sentences from other papers.
- Dual submission of substantially similar work is forbidden; concurrent ICML submissions with overlapping authors are treated as prior work for each other.

## 6. Review process and author response (2026)

- Review form dimensions, each scored 1–4: **Soundness, Presentation, Significance, Originality**. Overall recommendation 1–6 (6 Strong Accept, 5 Accept, 4 Weak accept, 3 Weak reject, 2 Reject, 1 Strong Reject). Confidence 1–5.
- Reviewers are told: originality does not require a new method (new insight about existing methods counts); soundness is assessed separately from impact; honest limitations should be rewarded.
- Reviewers give 3–5 numbered "key questions" whose answers could change their evaluation.
- Concurrent work: works made public less than two months before the full-paper deadline are concurrent; authors are not required to discuss them.
- **Author response:** three rounds of author–reviewer discussion (author rebuttal, reviewer follow-up, author follow-up), **each limited to 5000 characters**. Verify on OpenReview whether the limit applies per reply/thread.
- **No revised PDF** can be uploaded during the response period.
- Responses must be anonymous: no non-anonymized URLs, no personal-website URLs, no shortened URLs (they can log reviewer IPs). Reviewers are not expected to follow external links.
- No need to answer every minor point. Organize by reviewer ID. Be professional and polite.
- Reviewers must acknowledge the response and write a post-rebuttal "Final Justification" stating whether the rebuttal addressed their concerns.
- **Publicity:** for accepted papers, the original submission, anonymized reviews, meta-reviews, rebuttal and discussion are published on OpenReview. Rejected papers may opt in. Write every response as if it will be public.

## 7. Camera-ready (2026)

- Deadline (2026): May 28, 11:59pm AoE. In-person presentation questionnaire due May 11.
- `\usepackage[accepted]{icml2026}`; main body **9 pages**, followed by Acknowledgements, Impact Statement, References, Appendices. PDF ≤ 20 MB. US Letter.
- Author block per `example_paper.tex`; call `\printAffiliationsAndNotice{\icmlEqualContribution}` or `\printAffiliationsAndNotice{}`. Affiliations must match OpenReview profiles.
- Author order may change; **no additions or removals**. Must match OpenReview.
- Title and abstract may change only slightly (significant title changes need PC permission). Title and abstract entered in the OpenReview form must match the PDF exactly; TeX math allowed sparingly, no custom macros, accents via TeX commands.
- Essential content must remain unchanged relative to the reviewed version (the original submission is published alongside).
- **Conflict of Interest Disclosure (new in 2026):** if any financial/substantive conflict exists (e.g., evaluating a model built by an author's employer), add a paragraph titled "Conflict of Interest Disclosure" as the **last paragraph of the introduction**. Omit it entirely if there is no conflict. Mere industry employment is not a conflict.
- References: correct bibliographic data; replace arXiv citations with peer-reviewed versions where possible; fix items listed under "Reference Correctness Check" in the OpenReview decision; protect capitalization in BibTeX.
- Code/data: put in a public archival repository and link it in the paper; optionally fill the OpenReview "code url" box.
- **Lay summary** (plain-language summary) entered in OpenReview. 2026 guidance (same as 2025): at most 10 sentences / 200 words; understandable by a science journalist; specific enough that it could not describe any other ICML paper; think of it as a trailer for the paper. Source: https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- Run the ICML format checker (https://papercheck.icml.cc/papercheck.html) until clean; enter the 5-letter code it returns in the camera-ready form.
- Forms: PMLR Publication Agreement (uploaded, ≤10 MB), ICML Publishing Release (signed by one author), Recording Release for oral presenters.
- Registration: at least one author must register (Conference option for in-person; Conference or Virtual Pass for proceedings-only).
- Accessibility: color-blind-safe figures, up-to-date bibliography names and venues, inclusive language.
- A post-conference revision window allows small corrections before PMLR publication.

## 8. Key 2026 dates (historical, for orientation)

Abstract deadline Jan 23, 2026 AoE; full paper Jan 28, 2026 AoE; reviews due Mar 12; author–reviewer discussion Mar 24 – Apr 7; notification Apr 30; camera-ready May 28. Deadlines are strict, no extensions. The author list cannot change after the abstract deadline.

---

## How to refresh this file for a new cycle

1. If you have network access, fetch the current year's Author Instructions, Call for Papers, Reviewer Instructions and example paper (replace `2026` in the URLs above with the target year; if a page 404s, start from https://icml.cc and navigate).
2. Diff every row above against them. Update values, note the new snapshot date and year at the top, and list what changed under "Changelog".
3. Write the refreshed copy to the project workspace as `.icml/venue_facts.md` (the workspace copy is what the skills read during a project).
4. If you cannot fetch, tell the user explicitly: "Using ICML 2026 rules (snapshot 2026-10-05); please confirm they still hold for your target year." Do not silently assume.

## Changelog
- 2026-10-05: initial snapshot from ICML 2026 official pages.
