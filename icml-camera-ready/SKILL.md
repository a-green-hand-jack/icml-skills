---
name: icml-camera-ready
description: Turn an accepted ICML paper into its final camera-ready version and get it through the submission steps. De-anonymizes correctly (accepted style option, author block, acknowledgements), uses the extra ninth page to address reviewer feedback, checks every promise made in the rebuttal, adds the Conflict of Interest Disclosure when needed, upgrades references and fixes OpenReview's Reference Correctness Check, writes the lay summary, prepares the code link, and walks through the format checker, forms and OpenReview fields. Use this skill whenever an ICML paper has been accepted (or the user mentions camera-ready, final version, PMLR, papercheck, lay summary, plain-language summary, de-anonymizing, or the post-conference revision) - even if they only say "we got in, what now?". Not for pre-decision rebuttals (icml-rebuttal) or new drafts (icml-write).
compatibility: Python 3; pdflatex to compile; optional poppler-utils for PDF checks. Uploading, signing forms and registering are done by the authors.
---

# ICML Camera-Ready

The camera-ready is the version the world reads, published in PMLR next to the original
submission, the reviews and the discussion. Two consequences shape this skill: the
paper's essential content must stay what reviewers saw, and every promise made in the
rebuttal is now publicly checkable.

Talk to the user in their language. Run
`python scripts/init_workspace.py --root <latex-root> --skill icml-camera-ready`, read
`.icml/venue_facts.md` §7 (refresh it for the current year: camera-ready rules change
yearly) and `.icml/rebuttal/promises.md` if present.

## Ground rules

- **Do not change the paper's essential content** (claims, main results, method)
  relative to the reviewed version. Improvements, clarifications, promised additions
  and corrections are fine. If the authors want a substantive change, flag it and let
  them decide whether it needs PC approval.
- **Author list:** order may change, no additions or removals; it must match OpenReview.
  Title changes beyond small edits need program-chair permission.
- **No invented numbers or references** (same rules as icml-write and icml-cite).
- **The authors handle accounts**: uploading, signing forms, registering, filling
  OpenReview. You prepare everything and give exact instructions.

## Workflow

Track progress in `.icml/camera_ready.md` using `references/camera-ready-checklist.md`.

1. **Deadlines.** Ask for the year's camera-ready deadline and related dates (2026:
   camera-ready May 28 AoE, presentation questionnaire May 11). Work backwards; the
   format checker and forms take time.
2. **Promises.** For each row in `promises.md`, verify it is in the paper (location),
   matching what the rebuttal said (numbers identical, from the ledger). Report anything
   missing. If no promises file exists, reconstruct one from the posted rebuttal text.
3. **Reviewer feedback with the extra page.** The main body may grow to 9 pages. Use it
   for the promised items and the most common reviewer confusions first (run the
   icml-write paragraph and sentence passes on changed text). Don't spend it on new
   claims.
4. **De-anonymize.** `\usepackage[accepted]{icml20XX}`; real `\icmlauthor` and
   `\icmlaffiliation` entries matching OpenReview profiles; equal-contribution markers;
   `\icmlcorrespondingauthor`; `\printAffiliationsAndNotice{}` (or with
   `{\icmlEqualContribution}`); acknowledgements (unnumbered, before references;
   funding, grant numbers, compute providers, helpers); restore self-references to the
   first person only if the authors want; replace anonymous repo links with the public
   archival repository; remove "Anonymous" placeholders. Ask the authors for exact
   names, affiliations and funding text; never guess.
5. **Conflict of Interest Disclosure.** Ask the authors directly whether any author has
   a financial or other substantive conflict (e.g., the paper evaluates a model built by
   an author's employer). If yes, draft the paragraph titled "Conflict of Interest
   Disclosure" as the last paragraph of the introduction, naming author initials,
   employer and model. If no, include nothing. Industry employment alone is not a
   conflict. The authors must confirm the final wording.
6. **Impact Statement.** Still required (main track). Revisit it in light of reviews or
   ethics comments.
7. **References.** Run icml-cite's `check_bib.py` if installed; otherwise check the
   items manually. Fix every item OpenReview lists under "Reference Correctness Check".
   Replace arXiv citations with peer-reviewed versions where they exist. Protect
   capitalization; update author names and venues.
8. **Lay summary.** Draft it using `references/lay-summary-guide.md`; give the authors
   two variants; they choose and edit.
9. **Mechanical checks.**
   `python scripts/check_submission.py --tex main.tex --pdf main.pdf --mode camera-ready`
   then compile cleanly (no `??`), PDF ≤ 20 MB, US Letter, title and headings
   capitalized, abstract one paragraph of about 4–6 sentences, vector plots,
   colorblind-safe figures, TL;DR and TODO comments removed from the source if it will
   be released.
10. **Official format checker.** The authors upload the PDF to the ICML paper checker
    (2026: papercheck.icml.cc) and iterate until it passes; it returns a code for the
    OpenReview form. Fix whatever it reports; re-run step 9 after each fix.
11. **OpenReview form.** Prepare exact text for: title and abstract (matching the PDF
    exactly; TeX math sparingly, no custom macros, accents as TeX commands), lay
    summary, code URL, author order. List the files to upload (PDF, PMLR publication
    agreement signed by the corresponding author). Remind them of the ICML publishing
    release (one author signs), recording release for oral presenters, and
    registration requirements (see venue facts).
12. **Release.** If code/data go public: remove `.icml/` notes, credentials, internal
    paths; add a license and README; make the link archival. Confirm with the authors.

## After the conference

ICML allows a post-conference revision window for small corrections. Use the same
checks; do not change essential content.

## Files

- `scripts/check_submission.py` — compliance checks (`--mode camera-ready`).
- `scripts/init_workspace.py` — shared workspace.
- `references/camera-ready-checklist.md` — the full checklist (copy into `.icml/camera_ready.md`).
- `references/lay-summary-guide.md` — how to write the lay summary.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — shared.
