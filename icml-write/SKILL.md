---
name: icml-write
description: Draft and revise ICML (International Conference on Machine Learning) papers with a coding agent. Turns a research repo into a claims ledger, an abstract, a paragraph-level outline and a full LaTeX draft in the official icml2026 template, then revises it in structured passes (structure, paragraph flow, sentence clarity, cutting, consistency). Use this skill whenever the user wants to write, draft, outline, restructure, shorten, polish or rewrite any part of an ICML paper - abstract, introduction, method, experiments, related work, limitations, impact statement - or to port a NeurIPS/ICLR/arXiv paper into ICML format or fit a draft into the 8-page limit, even if they only say "write up these results for ICML" or "make my intro better". Use the sibling skills instead for reference search and BibTeX (icml-cite), pre-submission audits and simulated reviews (icml-review), replies to reviewers (icml-rebuttal) and post-acceptance final versions (icml-camera-ready).
compatibility: Works in any coding agent with a shell and Python 3. Optional - pdflatex/latexmk to compile, poppler-utils for PDF checks, network access to refresh venue rules.
---

# ICML Paper Writing

This skill guides a coding agent from "a repo full of results" to a submission-ready ICML
paper, and through revisions of an existing draft. It is one of five sibling skills that
share state through a `.icml/` workspace in the paper project.

Talk to the user in the language they use with you. Write the paper in English
(American spelling unless the user or co-authors prefer British; be consistent).

## What you are and are not here to do

A paper is a short, rigorous, evidence-based story with one to three claims readers care
about (Nanda). The scientists own that story. Your job is to help them find it, check it
against the evidence, lay it out so reviewers can follow it, and do the heavy lifting of
drafting and revising. Experienced writers warn that LLM-drafted text tends to be long,
preachy, generic and recognisably machine-written, and ICML now treats low-quality
AI-generated submissions as potential misconduct. So your value is mostly in
**structure, verification, revision and critique**; when you draft prose, draft it to be
cut, and expect the human to rewrite parts of it.

## Ground rules

These exist because each one has sunk real papers. Follow them even under deadline
pressure, and if a user asks you to break one, explain the risk and let them decide.

1. **Never write a number you did not read from a project file.** Every result in the
   paper must trace to a row in the claims ledger (`.icml/claims.md`), and every ledger
   row to a file and locator. If a number is missing, write `\textbf{[N?]}` and open an
   issue. Do not round differently from the ledger.
2. **Never write BibTeX from memory.** Use the icml-cite skill (or its workflow) to find
   and verify references. Unverified citations become visible placeholders
   (`\citep{PLACEHOLDER_topic_verify}`) plus an `[cite]` open issue.
3. **Never paper over a logical gap.** When revising exposes a missing link ("why does X
   cause Y?"), do not invent a plausible mechanism. Gopen & Swan show that restructuring
   prose routinely uncovers such gaps, and that the reviser can only *guess* the author's
   intent. Write the gap into `open_issues.md` with options (cite, add experiment,
   soften to an observation) and let the human choose.
4. **Never add hidden or reviewer-directed text** (white text, tiny fonts, instructions
   to LLMs). Prompt injection means desk rejection.
5. **Never modify `icml2026.sty`, margins, fonts or vertical spacing** to gain space. It
   is forbidden and checked. Cut words instead.
6. **Never de-anonymize.** No names, affiliations, acknowledgements, grant numbers,
   non-anonymous repo links, or first-person references to the authors' prior work in a
   submission. Watch for leaks from the repo: usernames in paths, cluster names in
   figure files, `pdfauthor` metadata.
7. **Never copy sentences from other papers**, including related work you are
   summarising. Write from scratch; quote verbatim only with quotation marks and citation.
8. **Stop at the checkpoints below.** Do not write full prose before the human has
   approved the claims and the outline.

## Step 0 — Set up and orient (every session)

1. Find the LaTeX root (or where it will live, usually `paper/`). Run
   `python scripts/init_workspace.py --root <latex-root> --skill icml-write`.
2. Read `references/workspace-contract.md` once per project, then read `.icml/state.md`
   to see where the project is. Resume from there instead of starting over.
3. Check `.icml/venue_facts.md`. If it is still the bundled ICML 2026 snapshot and the
   user targets another year, refresh it as described at its end. If you cannot fetch
   the official pages, tell the user which year's rules you are using.
4. Work out which entry point applies:
   - **From a repo** (no draft yet) → Phase 1.
   - **Existing draft** → "Revising an existing draft" below.
   - **Porting from another venue** → "Porting to ICML" below.
   - **A narrow request** ("tighten the abstract", "rewrite related work") → do it
     directly, but still apply the ground rules and the relevant pass from
     `references/revision-passes.md`, and log anything you could not verify.

## Phase 1 — Understand the project

Read the README, results directories, configs, logs, notebooks, any notes or existing
`.bib`. Write a short digest into `.icml/outline.md` under a `## Project digest` heading:
the problem, the method, what was run, what the results files contain, which results look
strongest, which look fragile.

Then check the evidence before building a story on it (Nanda: many published papers are
basically false because nobody re-checked the key experiment). For each candidate
headline result: find the raw output it comes from; check seeds/runs and variance; check
the baseline was tuned with comparable effort; note anything surprising. Record what you
checked under the red-team notes. If a key number cannot be traced, that is an
`[evidence]` open issue, not something to smooth over.

## Phase 2 — Compress into claims (Checkpoint 1)

Read `references/narrative-and-claims.md`. Then:

1. Fill the claims ledger: one to three claims that form a coherent theme, each with a
   strength level (existence-proof, systematic, narrow, hedged, theorem) matched to the
   evidence, the numbers that support it, and red-team notes (how the claim could be
   false while the evidence is true).
2. Fill the Numbers table for every result the paper will quote, read from files.
3. Draft the abstract in `outline.md` (formula in `references/section-guide.md`). Writing
   the abstract first exposes a weak story early (Foerster).
4. Draft a one-paragraph "why should anyone care" and a list of what the paper will
   *not* claim.

**CHECKPOINT 1 — stop.** Present, in the user's language: the proposed claims with
strength levels, the abstract draft, the key evidence for each claim, the weakest points
you found, and two or three specific questions (e.g. "Claim 2 holds on 3 of 5 datasets -
narrow it, or run the other two?"). Do not proceed until the human approves or edits the
claims. Record the outcome in `decisions.md`, set claim status to `approved`, update
`state.md`.

## Phase 3 — Outline (Checkpoint 2)

In `outline.md`:

1. **Paragraph outline**: one line per paragraph, each line a complete sentence stating
   the paragraph's single point (Foerster). Group by section using the section roles in
   `references/section-guide.md`.
2. **Section order decisions**: where related work goes (early only if the paper's
   motivation depends on a gap in prior work), whether a separate problem-setting section
   is needed (only if the setting itself is new).
3. **Related-work ↔ experiments map**: for every method named in related work that is
   applicable to the problem setting, either the experiment that compares against it or
   the one-line reason it is not applicable (Foerster's "compare and contrast" rule).
4. **Figure and table plan**: Figure 1 first (it sits top-right of page 1 across from the
   abstract in ICML's two-column layout; many readers look at nothing else). For each
   figure: the single takeaway, the data source, what the reader should look at.
5. **Page budget** for 8 pages: roughly 1 page intro including Figure 1; method starting
   on page 2 and never after page 3 (Farquhar); experiments as the bulk; limitations and
   conclusion short. Material that does not earn main-body space goes to an appendix
   list - but anything reviewers need to judge correctness must stay in the 8 pages.

**CHECKPOINT 2 — stop.** Show the outline, figure plan and page budget. Ask about the
choices you were least sure of. Record decisions. After approval you may draft without
further stops, logging questions in `open_issues.md` as you go.

## Phase 4 — Draft

1. **Template.** Use the official style package for the target year (2026:
   `icml2026.zip`). Copy the whole package, compile the untouched example once, then
   write into it. If you cannot download it, ask the user to place it in the project;
   never recreate the style file. Submission uses `\usepackage{icml2026}` without
   `accepted`.
2. **TL;DR comments.** Above every paragraph, keep its outline line as a comment:
   `% TL;DR: <one sentence>`. This keeps the draft and outline in sync, lets
   `scripts/extract_outline.py` rebuild a reverse outline at any time, and lets
   co-authors review flow quickly. Keep them until camera-ready.
3. **Numbers.** Prefer macros generated from the ledger (`\newcommand{\nMainAcc}{92.1}`
   in a `numbers.tex`) for headline results, so a rerun updates the paper in one place.
   Otherwise copy values exactly from the ledger.
4. **Section by section**, following `references/section-guide.md`. Compile often. Keep
   the Impact Statement as an unnumbered section before the references.
5. **Counter your own defaults while drafting**: open sections with the specific point,
   not with field-level context ("LLMs have achieved remarkable success..."); prefer
   concrete numbers over adjectives; one point per paragraph; no "we will"; no
   rhetorical questions; no bulleted prose in the body except the contribution list;
   no summary sentence restating the paragraph; no "novel", "significant", "crucial",
   "comprehensive" unless backed by a number or comparison.
6. **Theory content**: state every assumption formally before the theorem, give the
   intuition next to the statement, and move full proofs to the appendix with a proof
   sketch in the body. The bundled writing sources are mostly about empirical papers;
   ask the user for their group's conventions on theory papers.

## Phase 5 — Revise in passes

Read `references/revision-passes.md` and run the passes in order: structure → paragraph →
sentence → cut → consistency → numbers & references. Use the scripts:

- `python scripts/extract_outline.py main.tex` — reverse outline from TL;DR comments;
  flags paragraphs without a TL;DR and TL;DRs whose paragraph drifted.
- `python scripts/lint_prose.py main.tex` — advisory sentence-level lint (filler,
  hedges, intensifiers, vague pronouns, future tense, anthropomorphism, citation
  commands, US/UK spelling mix). It is a checklist generator, not an oracle.
- `python scripts/check_numbers.py main.tex --ledger .icml/claims.md` — every decimal,
  percentage and multiplier in the source must match a ledger value.
- `python scripts/check_submission.py --tex main.tex --pdf main.pdf --names "..."` —
  mechanical ICML compliance (page limit, anonymity, abstract, Impact Statement,
  layout hacks, hidden text, broken references).

When two style rules conflict, use `references/source-conflicts.md`. You may break a
style rule when you can state why the rule exists and why this case differs; log the
reason in `decisions.md` (Gopen & Swan and Foerster both insist the principles are not
mechanical rules).

## Phase 6 — Hand-off

Before calling a draft done: compile cleanly; all scripts run with no ERROR; every
`[N?]` and placeholder is either resolved or listed in `open_issues.md`; `state.md`
says what is left. Then recommend running **icml-review** in a fresh session or
sub-agent: a reviewer who did not write the text sees what readers will stumble on, and
you, having written it, will not. Summarise for the user: what changed, what you could
not verify, which human decisions are pending.

## Revising an existing draft

1. Init the workspace. Build the ledger *from the draft*: extract the claims from the
   abstract and contribution list, and every number from the text and tables. Mark all
   numbers `verified: no` until matched to project files; ask the user where results
   live if they are not in the repo.
2. Add TL;DR comments to every paragraph by summarising what it currently says, then run
   `extract_outline.py`. The reverse outline usually shows the structural problems
   faster than reading the prose.
3. Ask what the user wants: a light polish (sentence and cut passes only), a structural
   revision (all passes), or a specific section. For anything beyond a polish, confirm
   the claims (Checkpoint 1) before rewriting.
4. Preserve the authors' voice and terminology unless they ask otherwise. Show
   substantial rewrites as a diff or side by side, not silently.

## Porting to ICML from another venue

Start from a fresh copy of the ICML template and move content, not preambles. Then: cut
to 8 pages (cut words and merge experiments before moving essential evidence to the
appendix); switch citation style to APA author-year (`natbib` + `icml20XX.bst`, `\citet`
vs `\citep`); add the Impact Statement; remove checklists or sections specific to the old
venue; re-anonymize; if the paper was rejected before, address the old reviews in the
text but never mention the previous submission.

## Reference files

- `references/workspace-contract.md` — `.icml/` files and formats. Read once per project.
- `references/icml-venue-facts.md` — ICML 2026 rules snapshot (refresh per year).
- `references/narrative-and-claims.md` — finding the story, claim strength, evidence
  standards, red-teaming. Read in Phase 2.
- `references/section-guide.md` — what each section must do, abstract and intro
  formulas, figures, related work vs background, impact statement. Read in Phases 3–4.
- `references/prose-principles.md` — Gopen & Swan reader-expectation principles with ML
  examples, plus Lipton, Perez and Foerster sentence-level heuristics. Read for the
  paragraph and sentence passes.
- `references/revision-passes.md` — ordered revision passes with checklists.
- `references/source-conflicts.md` — how to resolve disagreements between the sources.
