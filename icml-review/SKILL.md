---
name: icml-review
description: Audit an ICML paper before submission and simulate an ICML peer review. Run mechanical compliance checks (8-page limit, anonymity leakage including PDF metadata, abstract formatting, impact statement, prohibited layout tricks, hidden text treated as prompt injection, broken citations), then write a review following ICML's actual criteria—soundness, presentation, significance, originality, key questions, limitations, overall score. Read-only: it reports problems, it does not edit the paper. Use this skill whenever the user wants to check an ICML draft, critique it, score it, stress-test it, red-team it, or "review it like a reviewer", wonders if it is ready for submission, asks what a reviewer would attack, or wants a format/anonymity check—even if they only say "take a look at my paper" or "is it ready?". For rewriting, use icml-write; for responding to real reviews, use icml-rebuttal.
compatibility: Python 3. Optional—poppler-utils (pdftotext, pdfinfo, pdffonts) for PDF checks; pdflatex for compilation.
---

# ICML Pre-Submission Review

Two tasks: (1) catch everything that could get the paper desk-rejected or quietly downgraded for formatting issues, and (2) read the paper like an ICML reviewer and report what they would say. This skill does not edit the paper. Separating review from writing keeps the review objective and creates a clear record of findings.

Communicate with the user in their language; the review report itself is written in English (it mimics an OpenReview form) unless the user requests otherwise.

## Independence is Critical

The agent that wrote the paper knows the intent behind every sentence, so it will not notice where readers get confused. Farquhar also notes that LLMs tend to agree with others and need repeated prompting to engage in genuine critique. Therefore:
- Run this skill preferably in a **new session or sub-agent that has not seen the drafting conversation**. Give it the PDF (or LaTeX) and at most `.icml/venue_facts.md`. Do not give it `claims.md` or reviewer notes—a real reviewer would not have these materials.
- Read like a busy expert with 5–10 papers to review: title, abstract, Figure 1, introduction, figures and tables, then the rest. Note where you would stop reading.
- Assume a bold claim is wrong and look for holes (Nanda). Then check whether the paper has already preemptively responded to it.
- Be specific. Every weakness must point to a location and explain how to fix it.

## Step 0 — Preparation

Run `python scripts/init_workspace.py --root <latex-root> --skill icml-review`. Read
`.icml/venue_facts.md` (or `references/icml-venue-facts.md` if no workspace exists);
refresh it if the target year differs. Compile the paper if possible, so you review the PDF that reviewers will see.

## Part A — Compliance Audit (Mechanical Checks)

```bash
python scripts/check_submission.py --tex main.tex --pdf main.pdf \
    --names "First Last,First Last" --affils "University,Lab,Company" \
    [--pristine-sty /path/to/official/icml2026.sty] [--position-track]
```

If you do not know the author names and affiliations (as well as lab/cluster names, user names), ask the user;
without this information, anonymity checks will be weak. Then perform the checks the script cannot do, listed in
`references/compliance-checks.md`: open figure files to check for embedded names,
check supplementary code for identity leakage, read every self-citation, confirm the OpenReview abstract matches,
confirm that nothing reviewers need is only in the appendix.

If icml-cite is available, also run its `check_bib.py`. Otherwise, at least confirm there are no `??` or `(?)` in the PDF,
and no placeholder citation keys.

Classify findings as: **Desk-reject risk** (page limit, anonymity, missing impact statement,
hidden text, template modification), **Must fix**, **Recommended fix**.

## Part B — Simulated ICML Review

Read `references/review-rubric.md` and fill out its template. Brief instructions:
1. **Summary**: Write a summary in your own words that the authors would agree with.
2. **Claims check**: List the paper's claims (from the abstract, introduction, contribution list);
   for each claim, check whether the provided evidence is sufficient. This is the core of soundness.
   Check whether the figure captions are literally true.
3. **Strengths and weaknesses**: Cover soundness, presentation, significance,
   originality—using ICML's broad definition of originality (new insights into existing methods also count),
   and judging soundness separately from impact.
4. **Scores**: Follow ICML's scale (1–4 per dimension, 1–6 overall, 1–5 confidence),
   with written justification for every "fair"/"poor" rating.
5. **Key questions** (3–5, numbered): Questions whose answers would change the score.
   These are the most useful output: they predict the rebuttal.
6. **Limitations** assessment.
7. **Reviewer-type variants**: Briefly describe how a skeptical theorist,
   a practitioner wanting baselines and compute details, and a reviewer from an adjacent subfield would each react.

Calibration: Most submissions are not accepted. Do not give 5–6 unless the paper is genuinely strong on every dimension;
if you find yourself praising everything, go back and find the weakest claim.

## Part C — Report and Handoff

Write the report to `.icml/reviews/simulated-<YYYY-MM-DD>.md` (format in the rubric file),
including: compliance findings sorted by severity, the simulated review, and a prioritized fix list
mapping each issue to a location in the paper and a fix type (writing, experiment, citation, human decision).
Add items that can only be handled by a human to `open_issues.md`.
Update `state.md`. Tell the user the three most important things in plain language,
and suggest handing the fix list to icml-write; reserve key questions for icml-rebuttal.

Do not edit the paper for even the smallest fix in this skill—list them instead.

## Files

- `scripts/check_submission.py` — Mechanical compliance checks (shared with icml-camera-ready).
- `scripts/init_workspace.py` — Creates the shared `.icml/` workspace.
- `references/review-rubric.md` — ICML review form, scoring rubric, reading protocol, report template.
- `references/compliance-checks.md` — Meaning of each check, how to fix it, manual checklist items.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — Shared files.
