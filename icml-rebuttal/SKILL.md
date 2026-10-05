---
name: icml-rebuttal
description: Plan and write ICML author responses (rebuttals) to real reviews on OpenReview. Itemizes every reviewer comment, separates misunderstandings from real weaknesses, plans any additional experiments, drafts per-reviewer replies and a summary for the area chair within ICML's limits (three discussion rounds, 5000 characters each, no links that break anonymity, no revised PDF), and tracks every promised change for the camera-ready. Use this skill whenever the user has received ICML reviews or meta-reviews, pastes reviewer comments, asks how to respond to reviewers, wants a rebuttal or follow-up reply drafted or shortened, or is deciding which reviewer concerns to concede or contest - even if they only say "the reviews are out" or "help me answer R2". Not for simulated pre-submission reviews (icml-review).
compatibility: Python 3 for the length/anonymity checker. Running new experiments needs the user's compute; this skill never invents their results.
---

# ICML Rebuttal

The rebuttal has two audiences. Reviewers read your paper to varying depth and may have
forgotten or misread details. The area chair (AC) knows the paper even less and may read
only the reviews and your responses. The goal is to clarify and convince both - and,
above all, to make it easy for the AC to decide (Parikh, Batra & Lee). A useful test: a
neutral third party should be able to tell whether each concern was addressed from the
rebuttal alone, without opening the paper or the reviews.

At ICML (2026 rules; check `.icml/venue_facts.md`): three discussion rounds (author
response, reviewer follow-up, author follow-up), each limited to 5000 characters; no
revised PDF during the response period; no non-anonymous, personal or shortened URLs
(reviewers are not expected to follow links anyway); no need to answer every minor
point; organize by reviewer ID; be professional. For accepted papers, the reviews and
the whole discussion become public, and reviewers write a post-rebuttal justification
saying whether you addressed their concerns.

Talk to the user in their language; write the responses in English.

## Ground rules

1. **No invented results.** You may design experiments and write the code to run them.
   You may not write a number into a response until the run has finished and the number
   is in a file. Unrun experiments are described as such, honestly.
2. **The human decides strategy.** What to concede, what to contest, whether to run a
   requested experiment, and whether to tell the AC that a review is unfair are the
   authors' calls. Prepare options; do not decide.
3. **Never accuse reviewers of bad faith on your own initiative.** If the authors want to
   flag a review that ignores the paper or is unsubstantiated, help them phrase it
   factually and politely, preferably in a confidential comment to the AC if the
   platform allows it.
4. **Anonymity holds.** No names, affiliations, identifying links, or "our previous
   paper X". Anonymous repos only, and only if useful (reviewers need not open them).
5. **Nothing hidden or reviewer-model-directed** in responses either.
6. **Don't promise - do.** Since no revised PDF can be uploaded, put the actual new text,
   numbers or proof sketch into the response, and record that it will be added to the
   paper. Every promise goes into `.icml/rebuttal/promises.md`.

## Step 0 — Setup

Run `python scripts/init_workspace.py --root <latex-root> --skill icml-rebuttal`. Save
each review as `.icml/reviews/R-<reviewerID>.md` (scores included) and the
meta-review/AC messages if any. Read `.icml/claims.md`, `state.md`, any earlier
simulated review (it often predicted the questions), and the paper. If no workspace
existed, note in `state.md` that the ledger is missing and verify numbers directly from
the paper and the results files.

## Step 1 — Itemize (triage table)

Build `.icml/rebuttal/triage.md` with one row per distinct comment (follow
`references/rebuttal-playbook.md` §2): ID (R1.3), quote of the core of the comment, type
(misunderstanding / already in paper / missing experiment / missing baseline /
clarity / claim too strong / related work / factual error by reviewer / minor / out of
scope), severity for the decision, which reviewers share it, possible responses, evidence
available (paper location, ledger number, new experiment needed), and owner.

Then summarize for the user: scores and confidence per reviewer; the 2–4 concerns that
actually drive the decision; shared concerns; quick wins; where the paper really is
weak. Be candid - a rebuttal cannot fix everything, and pretending otherwise wastes the
window.

## Step 2 — Decide (human checkpoint)

Present a strategy proposal and wait for the authors:
- for each major concern: concede-and-fix, clarify, contest-with-evidence, or
  acknowledge-as-limitation, with your recommendation;
- additional experiments worth running in the window, with estimated cost, and what
  result would be persuasive (be explicit that results may not favour the paper);
- what to deprioritise.

Record decisions in `decisions.md`.

## Step 3 — Experiments (if any)

Write and run (or hand the user) the code; log results to files; add them to the claims
ledger (as new numbers, `verified: yes` only when read from output). Report negative or
mixed results honestly and discuss with the authors how to present them. Reviewers and
ACs reward transparency; a hidden negative result that surfaces later is far worse.

## Step 4 — Draft responses

Follow `references/rebuttal-playbook.md`. Per reviewer, in priority order (biggest
concern you can answer well first):
- open with a one-line thanks and the reviewer's positive points if any,
- quote the core of each concern briefly, then answer it **directly in the first
  words** ("Yes, ...", "No, ...", "Not quite: ...", "We ran this: ..."), then the
  evidence, then context,
- point to the exact paper location when the answer is already there, and restate it
  so the response is self-contained,
- answer the intent behind the question, not only its letter,
- use data instead of argument wherever possible,
- end with what will change in the paper.

Also draft a short **general response** (if the platform/thread structure allows a
comment visible to all reviewers and the AC): strengths reviewers agreed on, shared
concerns and how they were addressed, summary of new results. Keep each piece within its
character limit.

## Step 5 — Check and finalize

Run `python scripts/check_rebuttal.py .icml/rebuttal/round1/*.md --limit 5000
--names "..." --affils "..."`. It counts characters, flags URLs, identity strings, empty
promises ("we will ...") without content, combative phrases, apology overuse and
unresolved placeholders. Then reread each response as the AC: is the answer to every
major concern clear in the first line? Show drafts to the user for approval before they
post; the user posts them (you do not submit anything on OpenReview yourself unless the
user explicitly asks and the environment allows it).

## Later rounds

For the author follow-up round: read the reviewer's follow-up, answer only what is new,
acknowledge changed scores graciously, and do not re-argue settled points. If a reviewer
did not engage, a short polite note restating the key resolved concern can help the AC.

## After decisions

Keep `promises.md` current; icml-camera-ready reads it and checks that each promised
change landed in the final version. If the paper is rejected, the triage table and
promises become the revision plan for the next venue (icml-write).

## Files

- `scripts/check_rebuttal.py` — length, anonymity and tone checks for response files.
- `scripts/init_workspace.py` — shared workspace.
- `references/rebuttal-playbook.md` — principles, triage format, response patterns,
  phrasing, pitfalls.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — shared.
