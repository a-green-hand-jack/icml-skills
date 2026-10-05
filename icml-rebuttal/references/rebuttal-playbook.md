# Rebuttal Playbook

Main source: Devi Parikh, Dhruv Batra & Stefan Lee, "How we write rebuttals" (2020).
Additional points from Aaditya Ramdas's rebuttal checklist and ICML 2026 rules.
Paraphrased; examples written for this skill.

## Contents
1. Audiences and goals
2. Triage table format
3. Ordering and structure
4. Response patterns (by comment type)
5. Tone and phrasing
6. Pitfalls
7. Promises file

## 1. Audiences and goals

- Reviewers: clarify doubts, answer questions, correct misunderstandings, push back on
  mischaracterizations, and show a good-faith effort to use their feedback.
- AC: show good faith, give a fair summary of the reviews, make it obvious which concerns
  were resolved, and help them decide. Newcomers tend to write only for reviewers; the AC
  matters more (debate analogy: you mainly persuade the judges, not your opponent - and
  reviewers are colleagues, not opponents).

## 2. Triage table format (`.icml/rebuttal/triage.md`)

```markdown
| ID | Quote (core) | Type | Severity | Shared with | Evidence / location | Plan | Status |
|----|--------------|------|----------|-------------|---------------------|------|--------|
| R1.1 | "No comparison to MoE-X" | missing baseline | major | R3.2 | Sec 2 excludes it w/o reason | run MoE-X (2 GPU-days) or explain inapplicability | decide |
```

Types: misunderstanding · already-in-paper · missing-experiment · missing-baseline ·
clarity · overclaim · related-work · reviewer-factual-error · minor · out-of-scope.
Severity = how much it drives the decision, not how much effort it needs.

Process (Parikh et al.): itemize everything as soon as reviews arrive (so experiments
start early); brain-dump possible responses per item without worrying about length;
draft complete responses; then cut and prioritise to fit the limits; finally reread the
reviews to make sure nothing important was missed.

## 3. Ordering and structure

- Start positive: summarise what reviewers liked (rebuttals are mostly about negatives;
  do not let the AC forget the strengths).
- Biggest concerns you can answer convincingly first; then less clear-cut ones; minor
  points last or batched ("We will fix all typos noted; thank you.").
- Consolidate shared concerns: answer once, refer to it from other threads.
- If several reviewers missed the same central point, set the stage with a short crisp
  recap of it.
- Keep each response self-contained: re-introduce acronyms and the relevant setup.

## 4. Response patterns

Lead with the direct answer, then the support. Bold or capitalised emphasis on the key
word is fine (Parikh et al.).

- **Yes/no factual question** → "**Yes.** All results average 5 seeds; Table 2 reports
  standard deviations."
- **Already in the paper** → "**This is in Sec. 4.2 (L310–318) and Table 3.** In short:
  <restate>." The pointer establishes the paper was not lacking it; the restatement
  saves the AC a trip.
- **Misunderstanding** → "**Not quite.** <correct statement>. We will rephrase L120 to
  prevent this reading: '<new sentence>'." (Treat it as a writing failure on your side:
  Farquhar - every misreading has a cause in the text.)
- **Missing experiment, run it** → "**We ran this.** <setup in one line>. <result with
  numbers>. <interpretation>. We will add it as Table X." Include negative results
  honestly.
- **Missing experiment, cannot run** → be transparent: why (compute, data access, time,
  venue rules), what evidence partially addresses it, and whether it will be in the
  final version.
- **Missing baseline that is not applicable** → "**<Method> is not applicable here
  because** <assumption it needs that our setting violates>. We will state this in Sec. 2."
- **Overclaim** → concede and narrow: "**We agree the phrasing is too strong.** We will
  revise to '<narrower claim>', which Table 2 supports." Conceding small points builds
  credibility for the big ones.
- **Premise is wrong** → "**We respectfully disagree with the premise.** <evidence>."
- **Related work missing** → give the actual comparison in two or three sentences now
  (don't promise, do), cite it, and say it will be added.
- **Reviewer factual error** → correct it neutrally with evidence; never "the reviewer is
  wrong".
- **Unhelpful or bad-faith review** (human decision) → factual: note which claims are
  unsupported, point to evidence and to other reviewers who disagree; consider a
  confidential AC comment.
- **Helpful extra effort** (typo lists, pointers, detailed suggestions) → thank
  specifically.

Answer the intent: "Why not dataset Z?" may really question the breadth of the
evaluation - answer about Z, then remind them of the datasets already covered.

## 5. Tone and phrasing

- Conversational, concise, courteous. Agree when you can; disagree only with evidence.
  Ramdas suggests most items end in agreement or partial agreement, with real
  disagreement reserved for a few.
- Data over rhetoric: whenever you disagree, ask whether a number can settle it.
- Limited apology: "Sorry for the confusion" once where the paper was unclear; not in
  every reply.
- Thank reviewers once, specifically; no flattery.
- Remember the public record: write every sentence as if the whole community will read it.
- OpenReview renders Markdown and LaTeX math; keep formatting light and test rendering.

## 6. Pitfalls

- Vague promises ("we will clarify", "we will discuss") without the content.
- Burying the answer after paragraphs of context.
- Answering every minor point at length while the decisive concern gets two lines.
- Introducing new claims that the paper cannot support in its final version.
- Reporting experiment results that are not finished, or rounding them generously.
- Links to non-anonymous resources; any identity hint.
- Exceeding the character limit (OpenReview may truncate or reject).
- Asking reviewers to raise scores. Let the evidence do it.
- Copying the reviewer's text at length (quote only the core).

## 7. Promises file (`.icml/rebuttal/promises.md`)

```markdown
| ID | Promised to | Promise | Exact text/result given in rebuttal | Paper location | Status |
|----|-------------|---------|-------------------------------------|----------------|--------|
| P1 | R1, R3 | Add MoE-X baseline | Table in R1 response (acc 81.2±0.3) | Table 2 | pending |
```

icml-camera-ready verifies each row before the final upload.
