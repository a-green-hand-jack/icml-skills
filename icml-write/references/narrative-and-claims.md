# Narrative and Claims

Sources: Neel Nanda, "Highly Opinionated Advice on How to Write ML Papers" (Alignment
Forum, 2025); Sebastian Farquhar, "How to Write ML Papers" (2024); Zachary Lipton,
"Heuristics for Scientific Writing" (2018); ICML 2026 Reviewer Instructions. Paraphrased
and adapted for an agent; read the originals for nuance.

## Contents
1. What a narrative is
2. Compressing a project into claims
3. Claim strength must match evidence
4. What counts as good evidence
5. Red-teaming the narrative
6. Novelty and positioning
7. Questions to put to the human at Checkpoint 1

## 1. What a narrative is

A paper communicates a small number of claims and the evidence for them. Readers rarely
retain more than a few sentences from a paper, so choose those sentences deliberately.
The narrative answers three questions:

- **What?** One to three specific, concrete claims that fit one coherent theme. A grab-bag
  of unrelated findings is much harder to understand, remember and praise.
- **Why believe it?** Rigorous evidence that a skeptical, engaged expert would accept.
- **So what?** The motivation (which problem, why it matters) and the impact (what a reader
  should do or believe differently).

The goal is that the reader *understands* the claims, *remembers* them, and *believes* the
evidence supports them. Everything in the paper exists to serve those claims; a section
or paragraph that does not is a candidate for the appendix or deletion.

Examples of well-formed claims:
- "Method X outperforms the strongest tuned baselines on task Y under metric Z."
- "Behaviour A of the model is substantially explained by mechanism B."
- "Technique C fails in setting D whenever conditions E and F hold."

## 2. Compressing a project into claims

Projects end as a mess of results, dead ends and half-understood effects. To compress:

1. List everything the project learned. Mark which items are hard or non-obvious.
2. For each item: how comfortable would the authors be defending it to a hostile expert?
3. Ask which results someone would find most exciting, and why anyone outside the team
   should care.
4. Group the defensible, interesting items into at most three claims under one theme.
5. Explicitly de-prioritise the rest (appendix, future work, or nothing). If you do not
   choose what to drop, the reader will drop something at random - possibly the key point.

Agent technique: write the compressed version three ways - a one-sentence summary, a
five-sentence abstract, and the contribution bullet list. Where the three disagree, the
story is not settled yet. Bring the disagreement to Checkpoint 1.

A good sign that writing can start: the authors have learned something insightful and
it can be made legible to someone else. A bad sign: the "claim" is "we tried X and here
are some numbers".

## 3. Claim strength must match evidence

Use one of these levels per claim in the ledger and phrase the paper accordingly:

| Level | Meaning | Typical phrasing | Evidence needed |
|---|---|---|---|
| existence-proof | X happens in at least one case | "we find a case where", "can" | One trustworthy, carefully checked example |
| narrow | X holds in specified settings | "on A and B, under metric M" | Strong evidence within the stated scope |
| systematic | X holds broadly | "across N datasets / scales / models" | Many diverse settings, variance reported |
| hedged | Evidence suggests X | "suggests", "provides evidence that" | Real but incomplete evidence; say what is missing |
| theorem | X is guaranteed under assumptions | "Theorem 1 shows" | A proof, assumptions stated formally |

Rules for the agent:
- Stronger claims make better papers only if the evidence carries them. Overclaiming is
  the most common reason expert readers dismiss a paper.
- Lipton's "hostages to fortune": no sentence should be falsifiable by a qualified reader
  in isolation. "Outperforms on most datasets" invites a counterexample; state the count.
- A claim you are not sure about is better omitted than asserted; an omission rarely
  causes rejection, an indefensible sentence can.
- Opinions are allowed in the introduction and discussion only when labelled as such.
- Hedging is not a substitute for calibration: pick the level first, then drop empty
  hedges ("may", "can") that add no information.

## 4. What counts as good evidence

Nanda's and the ICML reviewer form's standards, condensed:

- **Experiments that distinguish hypotheses.** An experiment is valuable when its outcome
  would differ depending on which explanation is true.
- **Reliability.** How surprised would the authors be if the result were an artefact of a
  bug, noise or misunderstanding? Investigate the most uncertain parts. Re-derive a key
  result through a different path when possible.
- **Noise.** Report the number of runs and what the error bars are (std vs standard error
  vs CI). Results within noise are not results.
- **Strong baselines.** Showing a method "works" is weak; showing it beats the strongest
  reasonable alternatives, tuned with comparable effort, is the real claim. Agents and
  authors alike tend to tune the new method more than the baseline - check.
- **Ablations.** If the method changes A, B and C, show the effect of each.
- **Quality over quantity.** One decisive experiment beats many weak ones; but several
  *qualitatively different* lines of evidence pointing the same way are more robust than
  many near-duplicates.
- **Cherry-picking and post-hoc analysis.** Say how qualitative examples were selected;
  include random examples where possible. Distinguish predictions made before seeing the
  data from explanations constructed after.
- **Reproducibility.** Enough detail (in the paper plus appendix) for an expert to
  reimplement; code submission is encouraged at ICML and considered in decisions.

## 5. Red-teaming the narrative

For each claim, write in the ledger's red-team notes:
- The most likely way the claim is wrong even though the reported numbers are right.
- The alternative explanation a reviewer will raise ("is this only because of X?").
  Lipton: if you can anticipate the question and know the answer, put it in the paper; if
  you do not know the answer and "no" would be damning, run the experiment.
- What evidence a reader should *not* expect from this paper, and why that is acceptable.

Unresolved red-team items become `[evidence]` or `[claim]` open issues.

## 6. Novelty and positioning

- Be explicit about what is new and what is borrowed. The same paper reads as arrogant
  or as a modest contribution depending on how this is stated.
- Never blur prior work into your contribution; never misrepresent prior work to make
  yours look better - reviewers notice and it poisons goodwill.
- ICML's reviewer instructions define originality broadly: new insight into existing
  methods, careful evaluation, removing restrictive assumptions, or a novel combination
  with well-argued reasoning all count. If the contribution is of this kind, say so
  plainly rather than dressing it up as a new method.
- If prior work was flawed and your paper fixes it, explain the flaw professionally and
  without commenting on the authors.

## 7. Questions to put to the human at Checkpoint 1

Pick the ones that apply; be specific to the project.
- "I propose these N claims at these strength levels. Is this the story you want?"
- "Result R is the strongest; result S is fragile because ... Keep S, narrow it, or drop it?"
- "Baseline B was tuned with K trials vs M for ours. Re-tune, or disclose?"
- "This finding was post-hoc. Can we frame it as an observation, or test it fresh?"
- "Which reviewer community is this for (e.g., optimization vs. applications)?"
- "What should a reader do differently after reading this paper?"
