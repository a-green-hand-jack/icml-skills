---
name: icml-review
description: Audit an ICML paper before submission and simulate ICML peer review. Runs mechanical compliance checks (8-page limit, anonymity leaks including PDF metadata, abstract form, Impact Statement, forbidden layout hacks, hidden text that counts as prompt injection, broken references) and then writes a critical review on ICML's actual form - soundness, presentation, significance, originality, key questions, limitations, overall score. Read-only - it reports, it does not edit the paper. Use this skill whenever the user wants an ICML draft checked, critiqued, scored, stress-tested, red-teamed or "reviewed like a reviewer would", wants to know if it is ready to submit, asks what reviewers will attack, or wants a format/anonymity check - even if they only say "take a look at my paper" or "is this ready?". For rewriting use icml-write; for answering real reviews use icml-rebuttal.
compatibility: Python 3. Optional - poppler-utils (pdftotext, pdfinfo, pdffonts) for PDF checks; pdflatex to compile.
---

# ICML Pre-Submission Review

Two jobs: (1) catch everything that can get a paper desk-rejected or quietly marked down
for form, and (2) read the paper the way an ICML reviewer will, then report what they
will say. This skill does not edit the paper. Separating review from writing keeps the
reviewer honest and keeps a clean record of what was found.

Talk to the user in their language; write the review itself in English (it mirrors the
OpenReview form) unless the user asks otherwise.

## Independence matters

The agent that wrote the paper knows what every sentence was meant to say and will not
notice where readers get lost. Farquhar also notes that LLMs lean agreeable and need
repeated pushing to be properly critical. So:
- Prefer running this skill in a **fresh session or a sub-agent** that has not seen the
  drafting conversation. Give it the PDF (or LaTeX) and, at most, `.icml/venue_facts.md`.
  Do not give it `claims.md` or notes for the review pass - reviewers will not have them.
- Read as a busy expert with 5-10 papers to review: title, abstract, Figure 1,
  introduction, figures, then the rest. Note where you would have stopped reading.
- Assume a bold claim is false and look for the hole (Nanda). Then check whether the
  paper already pre-empted it.
- Be specific. Every weakness must point to a location and say what would fix it.

## Step 0 — Setup

Run `python scripts/init_workspace.py --root <latex-root> --skill icml-review`. Read
`.icml/venue_facts.md` (or `references/icml-venue-facts.md` if there is no workspace);
refresh it if the target year differs. Compile the paper if you can, so you review the
PDF reviewers will see.

## Part A — Compliance audit (mechanical)

```bash
python scripts/check_submission.py --tex main.tex --pdf main.pdf \
    --names "First Last,First Last" --affils "University,Lab,Company" \
    [--pristine-sty /path/to/official/icml2026.sty] [--position-track]
```

Ask the user for author names and affiliations (and lab/cluster names, usernames) if you
do not have them; anonymity checks are weak without them. Then do the checks the script
cannot do, listed in `references/compliance-checks.md`: open figures for embedded names,
check supplementary code for identity leaks, read every self-citation, check that the
OpenReview abstract matches, check that nothing reviewers need lives only in the appendix.

If icml-cite is available, also run its `check_bib.py`. Otherwise at least confirm no
`??` or `(?)` in the PDF and no placeholder keys.

Classify findings: **Desk-reject risk** (page limit, anonymity, missing Impact Statement,
hidden text, template modification), **Must fix**, **Should fix**.

## Part B — Simulated ICML review

Read `references/review-rubric.md` and fill its template. In brief:
1. **Summary** the authors would agree with, in your own words.
2. **Claims check**: list the paper's claims (from abstract, intro, contribution list);
   for each, the evidence offered and whether it suffices. This is the heart of
   soundness. Check that text descriptions of figures and tables are literally true.
3. **Strengths and weaknesses** across soundness, presentation, significance,
   originality - with ICML's broad view of originality (new insight into existing
   methods counts) and with soundness judged separately from impact.
4. **Scores** on ICML's scales (1–4 per dimension, overall 1–6, confidence 1–5), each
   "fair"/"poor" justified.
5. **Key questions** (3–5, numbered): questions whose answers would change the score.
   These are the most useful output: they predict the rebuttal.
6. **Limitations** assessment.
7. **Reviewer-type variants**: briefly, how a skeptical theorist, a practitioner who
   wants baselines and compute details, and a reviewer from a neighbouring subfield
   would each react.

Calibration: most submissions are not accepted. Do not give 5–6 unless the paper is
genuinely strong on every dimension; if you find yourself praising everything, go back
and look for the weakest claim.

## Part C — Report and hand-off

Write the report to `.icml/reviews/simulated-<YYYY-MM-DD>.md` (format in the rubric
file) with: compliance findings by severity, the simulated review, and a prioritised fix
list mapping each issue to the place in the paper and to the kind of fix (writing,
experiment, citation, human decision). Add human-only items to `open_issues.md`.
Update `state.md`. Tell the user the three most important things in plain terms and
suggest handing the fix list to icml-write; save the key questions for icml-rebuttal.

Do not edit the paper in this skill, even for trivial fixes - list them instead.

## Files

- `scripts/check_submission.py` — mechanical compliance checks (shared with icml-camera-ready).
- `scripts/init_workspace.py` — create the shared `.icml/` workspace.
- `references/review-rubric.md` — ICML review form, scales, reading protocol, report template.
- `references/compliance-checks.md` — what each check means, how to fix, manual checks.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — shared.
