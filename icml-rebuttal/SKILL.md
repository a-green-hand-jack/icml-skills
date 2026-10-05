---
name: icml-rebuttal
description: Plan and draft ICML author rebuttals against real OpenReview reviews. List each reviewer's comments line by line, distinguish misunderstandings from genuine weaknesses, plan any additional experiments needed, draft per-reviewer responses and an Area Chair (AC) summary, strictly abide by ICML limits (three discussion rounds, 5000 characters per round, no links that break anonymity, no uploaded revised PDFs), and track every promised revision to ensure it is implemented in the final version. Use this skill when the user has received ICML reviews or meta-reviews, pasted reviewer comments, asked how to respond to reviewers, wants to draft or trim a rebuttal or follow-up response, or is deciding which reviewer concerns to concede or contest—even if they only say "the reviews are out" or "help me reply to R2". Not for pre-submission mock review (icml-review).
compatibility: Python 3, used for length/anonymity checks. Running new experiments requires the user's own compute; this skill never fabricates experimental results.
---

# ICML Rebuttal

A rebuttal has two audiences. Reviewers read papers with varying depth and may have forgotten or misread details. Area Chairs (ACs) know even less about the paper and may only read the reviews and your response. The goal is to clarify and persuade both—and most importantly, to make it easy for the AC to reach a decision (Parikh, Batra & Lee). A useful sanity check: a neutral third party should be able to tell, from the rebuttal alone, whether each concern has been addressed, without opening the paper or the reviews.

At ICML (2026 rules; check `.icml/venue_facts.md`): three discussion rounds (author response, reviewer follow-up, author follow-up), 5000-character limit per round; no revised PDF may be uploaded during the response period; no non-anonymous, personalized, or shortened URLs (reviewers are not expected to click links anyway); you do not need to answer every trivial detail; organize by reviewer ID; stay professional. For accepted papers, the reviews and the entire discussion become public, and reviewers write a post-rebuttal note stating whether you addressed their concerns.

Communicate with the user in the user's language; write rebuttals in English.

## Ground Rules

1. **Do not fabricate results.** You may design experiments and write running code. But do not write numbers into the response before the experiment has run and the values have been written to a file. Experiments that have not been run should be described honestly as not yet run.
2. **Strategy is a human decision.** What to concede, what to contest, whether to run experiments requested by reviewers, and whether to flag an unfair review to the AC—these are author decisions. Prepare options; do not decide for the author.
3. **Never accuse reviewers of bad faith on your own initiative.** If the author wants to flag a review that ignores the paper or lacks basis, help them express it factually and politely, preferably through a confidential comment to the AC if the platform allows.
4. **Stay anonymous.** No names, affiliations, identifiable links, or "our previous work X". Anonymous repositories only, and only when useful (reviewers do not have to open them).
5. **Do not include hidden content or text directed at reviewer models in the response.**
6. **Do not promise—deliver.** Because a revised PDF cannot be uploaded, put actual new text, figures, or proof sketches directly into the response, and record that these will be added to the paper. Write every promise into `.icml/rebuttal/promises.md`.

## Step 0 — Preparation

Run `python scripts/init_workspace.py --root <latex-root> --skill icml-rebuttal`. Save each review as `.icml/reviews/R-<reviewerID>.md` (including scores), and save any meta-review / AC message as well. Read `.icml/claims.md`, `state.md`, any earlier mock reviews (they often predicted issues), and the paper itself. If the workspace does not exist, note in `state.md` that the ledger is missing and verify numbers directly from the paper and results files.

## Step 1 — Line-by-line Triage (Triage Table)

Build `.icml/rebuttal/triage.md`, one row per independent comment (follow `references/rebuttal-playbook.md` §2): ID (R1.3), core quote of the comment, type (misunderstanding / already-in-paper / missing-experiment / missing-baseline / clarity / overclaim / related-work / reviewer-factual-error / minor / out-of-scope), severity of impact on the decision, which reviewers share the concern, possible response, available evidence (paper location, ledger number, whether a new experiment is needed), owner.

Then summarize for the user: each reviewer's score and confidence; the 2–4 concerns that truly affect the decision; shared concerns; easy fixes; genuine weaknesses of the paper. Be honest—a rebuttal cannot solve everything, and pretending otherwise wastes precious time.

## Step 2 — Decision (Human Checkpoint)

Propose a strategy and wait for the author to confirm:
- For each major concern: concede and correct, clarify, rebut with evidence, or acknowledge as a limitation, with your recommendation;
- Additional experiments worth running within the time window, estimated cost, and what result would be convincing (state clearly that the result may not favor the paper);
- What can be deprioritized.

Record decisions in `decisions.md`.

## Step 3 — Experiments (if any)

Write and run (or hand to the user to run) code; record results to files; add them to the claims ledger (as new numbers, mark `verified: yes` only when read from output). Report negative or mixed results honestly and discuss with the author how to present them. Reviewers and ACs reward transparency; hidden negative results surfacing later are far worse.

## Step 4 — Drafting Responses

Follow `references/rebuttal-playbook.md`. Process reviewers separately, ordered by priority (tackle the biggest concerns you can answer best first):
- Open with a sentence of thanks, and mention any positive remarks from the reviewer,
- Briefly quote the core of each concern, then answer with **the first sentence directly** ("Yes, ...", "No, ...", "Not quite: ...", "We ran this: ..."), followed by evidence and then context,
- When the answer is already in the paper, point to the exact location and restate it so the response is self-contained,
- Answer the intent behind the question, not just the literal wording,
- Substitute data for argumentation whenever possible,
- End with what changes will be made in the paper.

Also draft a short **overall response** (if the platform / thread structure allows one comment visible to all reviewers and the AC): strengths acknowledged by all reviewers, shared concerns and how they are addressed, summary of new results. Ensure every part stays within the character limit.

## Step 5 — Check and Finalize

Run `python scripts/check_rebuttal.py .icml/rebuttal/round1/*.md --limit 5000 --names "..." --affils "..."`. It counts characters, flags URLs, identity strings, empty promises ("we will ...") without substance, combative wording, excessive apologies, and unresolved placeholders. Then reread each response from the AC's perspective: is the answer to each major concern clear in the first line? Show the draft to the user for approval before posting; let the user post it themselves (do not submit on OpenReview on the user's behalf unless explicitly asked and the environment allows).

## Subsequent Rounds

For the author follow-up round: read the reviewer follow-ups, answer only what is new, graciously acknowledge score changes, and do not rehash settled issues. If a reviewer did not participate, a short polite note restating the key concerns already resolved can help the AC.

## After the Decision

Keep `promises.md` updated; icml-camera-ready will read it and check that every promised revision has been implemented in the final version. If the paper is rejected, the triage table and promises become a revision plan for the next venue (icml-write).

## Files

- `scripts/check_rebuttal.py` — Length, anonymity, and tone checks for response files.
- `scripts/init_workspace.py` — Shared workspace setup.
- `references/rebuttal-playbook.md` — Principles, triage format, response patterns, wording, pitfalls.
- `references/icml-venue-facts.md`, `references/workspace-contract.md` — Shared files.
