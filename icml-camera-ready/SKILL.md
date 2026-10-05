---
name: icml-camera-ready
description: Convert an accepted ICML paper to the final camera-ready version and complete the submission process. Correctly handle de-anonymization (using the accepted style option, author information block, acknowledgments), utilize the extra ninth page to respond to reviewer feedback, check every promise made in the rebuttal, add a conflict-of-interest disclosure statement as needed, upgrade references and fix OpenReview's Reference Correctness Check, write a lay summary, prepare the code link, and complete the formatting checker, forms, and OpenReview fields. Use this skill whenever an ICML paper has been accepted (or the user mentions camera-ready, final version, PMLR, papercheck, lay summary, plain-language summary, de-anonymizing, post-conference revision) — even if they only say "we got in, what now?". Not applicable for pre-decision rebuttals (use icml-rebuttal) or new drafts (use icml-write).
compatibility: Python 3; pdflatex compilation; optional poppler-utils for PDF checking. Uploading, signing forms, and registration are done by the authors.
---

# ICML Camera-Ready

The camera-ready is the version that readers worldwide will see, published alongside the original submission, reviews, and discussions on PMLR. This fact has two consequences: the core content of the paper must remain consistent with what the reviewers saw, and every promise made in the rebuttal is now publicly verifiable.

Communicate with the user in their language. Run
`python scripts/init_workspace.py --root <latex-root> --skill icml-camera-ready`, read
Section 7 of `.icml/venue_facts.md` (refresh for the current year: camera-ready rules change every year) and `.icml/rebuttal/promises.md` (if it exists).

## Basic Rules

- **Do not change the core content of the paper** (claims, main results, methods)
  relative to the reviewed version. Improvements, clarifications, promised additions, and corrections are fine. If the authors want to make substantial changes, flag them and let the authors decide whether Program Chair (PC) approval is needed.
- **Author list:** order can change, but no additions or deletions; must match OpenReview.
  Title changes beyond minor edits require Program Chair permission.
- **Do not fabricate numbers or citations** (same rule as icml-write and icml-cite).
- **Authors handle their own accounts**: uploading, signing forms, registration, filling out
  OpenReview. You are responsible for preparing all materials and giving precise instructions.

## Workflow

Use `references/camera-ready-checklist.md` to track progress in `.icml/camera_ready.md`.

1. **Deadline.** Ask for the camera-ready deadline and related dates for that year (2026:
   camera-ready May 28 AoE, presentation questionnaire May 11). Work backward from the deadline; the formatting checker and forms take time.
2. **Promises.** For every line in `promises.md`, verify it is in the paper (location),
   and is exactly as stated in the rebuttal (same numbers, from the ledger). Report any missing items. If there is no promises file, reconstruct one from the published rebuttal text.
3. **Use the extra page for reviewer feedback.** The main body can expand to up to 9 pages. Prioritize promises and the most common reviewer confusion (run icml-write's paragraph and sentence checks on the revised text). Do not use it for new claims.
4. **De-anonymization.** `\usepackage[accepted]{icml20XX}`; real `\icmlauthor` and
  `\icmlaffiliation` entries matching OpenReview profiles; co-first-author marks;
  `\icmlcorrespondingauthor`; `\printAffiliationsAndNotice{}` (or with
  `{\icmlEqualContribution}`); acknowledgments (unnumbered, before references;
  funding, grant numbers, compute providers, assistants); restore self-citations to first person only if the authors wish; replace anonymous repository links with a public archived repository; remove "Anonymous" placeholders. Ask the authors for exact names, affiliations, and funding text; never guess.
5. **Conflict of Interest Disclosure.** Directly ask the authors whether any author has a financial or other substantial conflict of interest (e.g., the paper evaluates a model built by an author's company). If so, draft a paragraph titled "Conflict of Interest Disclosure" as the last paragraph of the introduction, stating the author's initials, company, and model. If not, include nothing. Industry employment alone does not constitute a conflict of interest. The authors must confirm the final wording.
6. **Impact Statement.** Still required (main conference papers). Revisit it based on review comments or ethics remarks.
7. **References.** If icml-cite's `check_bib.py` is installed, run it; otherwise check entries manually. Fix every item listed by OpenReview under "Reference Correctness Check". Replace arXiv citations with published versions when a peer-reviewed version exists. Protect case; update author names and conference names.
8. **Lay summary.** Use `references/lay-summary-guide.md` to draft; give the authors two versions; let them choose and edit.
9. **Mechanical checks.**
   `python scripts/check_submission.py --tex main.tex --pdf main.pdf --mode camera-ready`
   Then compile cleanly (no `??`), PDF ≤ 20 MB, US Letter, correct title and title case,
   abstract a single paragraph of about 4–6 sentences, vector graphics,
   color-vision-accessibility-friendly figures, remove TL;DR and TODO comments from source code if it will be published.
10. **Official formatting checker.** The author uploads the PDF to the ICML paper checker
    (2026: papercheck.icml.cc) and iterates until it passes; it returns a code for the OpenReview form. Fix all issues it reports; rerun Step 9 after each fix.
11. **OpenReview forms.** Prepare precise text for: title and abstract (exactly matching the PDF;
    use minimal TeX math, no custom macros, use TeX commands for accents), lay summary,
    code URL, author order. List files to upload (PDF, PMLR Publication Agreement signed by the corresponding author). Remind them of the ICML publication license (signed by one author), recording consent for oral presenters, and registration requirements (see venue facts).
12. **Release.** If code/data will be public: remove `.icml/` notes, credentials, internal paths;
    add a license and README; make links long-term archived. Confirm with the authors.

## After the Conference

ICML allows a post-conference revision window for minor corrections. Use the same checks; do not change core content.

## Files

- `scripts/check_submission.py` — compliance checks (`--mode camera-ready`).
- `scripts/init_workspace.py` — shared workspace.
- `references/camera-ready-checklist.md` — full checklist (copy to `.icml/camera_ready.md`).
- `references/lay-summary-guide.md` — how to write a lay summary.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — shared files.
