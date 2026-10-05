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

- Reviewers: clarify doubts, answer questions, correct misunderstandings, rebut misreadings, and demonstrate good-faith effort to use the feedback.
- AC: demonstrate good faith, give a fair summary of the reviews, make it obvious which concerns have been resolved, and help them reach a decision. Newcomers often write only for reviewers; the AC matters more (debate analogy: you are primarily persuading the judges, not the opponents—and reviewers are colleagues, not opponents).

## 2. Triage table format (`.icml/rebuttal/triage.md`)

```markdown
| ID | Quote (core) | Type | Severity | Shared with | Evidence / location | Plan | Status |
|----|--------------|------|----------|-------------|---------------------|------|--------|
| R1.1 | "No comparison to MoE-X" | missing baseline | major | R3.2 | Sec 2 excludes it w/o reason | run MoE-X (2 GPU-days) or explain inapplicability | decide |
```

Types: misunderstanding · already-in-paper · missing-experiment · missing-baseline ·
clarity · overclaim · related-work · reviewer-factual-error · minor · out-of-scope.
Severity = impact on the decision, not the amount of work required.

Process (Parikh et al.): list every comment immediately upon receiving the reviews (so experiments can start early); for each, quickly write a possible response without hesitation; draft the full response; then trim and reorder to fit the limit; finally reread the reviews to ensure nothing important was missed.

## 3. Ordering and structure

- Start positive: summarize strengths the reviewer acknowledged (rebuttals focus mostly on negatives; do not let the AC forget the paper's merits).
- Biggest concerns you can answer convincingly first; then those with weaker evidence; minor issues last or batched ("We will fix all typos noted; thank you.").
- Consolidate shared concerns: answer once and reference in other threads.
- If multiple reviewers missed the same central point, preface with a short, clear recap.
- Keep each response self-contained: reintroduce abbreviations and relevant setup.

## 4. Response patterns

Lead with the direct answer, then the support. Bold or capitalised emphasis on key words is acceptable (Parikh et al.).

- **Yes/no factual question** → "**Yes.** All results average 5 seeds; Table 2 reports standard deviations."
- **Already in the paper** → "**This is in Sec. 4.2 (L310–318) and Table 3.** In short: <restate>." The citation shows the paper is not deficient; the restatement saves the AC from looking it up.
- **Misunderstanding** → "**Not quite.** <correct statement>. We will rephrase L120 to prevent this reading: '<new sentence>'." (Treat it as a writing failure on the author's side: Farquhar—every misreading has a textual cause.)
- **Missing experiment, run it** → "**We ran this.** <setup in one line>. <result with numbers>. <interpretation>. We will add it as Table X." Include negative results honestly.
- **Missing experiment, cannot run** → Be transparent: reason (compute, data access, time, venue rules), what evidence partially addresses it, and whether it will be added in the final version.
- **Missing baseline that is not applicable** → "**<Method> is not applicable here because** <assumption it needs that our setting violates>. We will state this in Sec. 2."
- **Overclaim** → Concede and narrow: "**We agree the phrasing is too strong.** We will revise to '<narrower claim>', which Table 2 supports." Conceding on small points builds credibility for big ones.
- **Premise is wrong** → "**We respectfully disagree with the premise.** <evidence>."
- **Related work missing** → Give the actual comparison in two or three sentences now (do not promise, deliver), cite it, and state it will be added to the paper.
- **Reviewer factual error** → Correct neutrally with evidence; never use "the reviewer is wrong".
- **Unhelpful or bad-faith review** (human decision) → Stick to facts: point out which claims lack support, point to evidence and to other reviewers who disagree; consider submitting a confidential comment to the AC.
- **Helpful extra effort** (typo lists, pointers, detailed suggestions) → Thank specifically.

Answer the intent: "Why not dataset Z?" may actually be questioning the breadth of evaluation—answer Z first, then remind them of the datasets already covered.

## 5. Tone and phrasing

- Conversational, concise, courteous. Agree when you can; oppose only when you have evidence.
  Ramdas recommends that most items end with agreement or partial agreement, reserving real disagreement for a minority of cases.
- Data over rhetoric: whenever you are about to oppose, ask whether a number can settle it.
- Limited apology: use "Sorry for the confusion" once, only where the paper was genuinely unclear; do not apologize in every reply.
- Thank reviewers once, specifically; no flattery.
- Remember the public record: write every sentence as if the entire community will read it.
- OpenReview renders Markdown and LaTeX math; keep formatting simple and test the rendering.

## 6. Pitfalls

- Vague promises ("we will clarify", "we will discuss") without substance.
- Burying the answer after paragraphs of context.
- Answering every minor point at length while the decisive concern gets two lines.
- Introducing new claims that the paper cannot support in its final version.
- Reporting experiment results that are not finished, or generous rounding of results.
- Links to non-anonymous resources; any identity hint.
- Exceeding the character limit (OpenReview may truncate or reject).
- Asking reviewers to raise scores. Let the evidence do it.
- Copying the reviewer's text at length (quote only the core part).

## 7. Promises file (`.icml/rebuttal/promises.md`)

```markdown
| ID | Promised to | Promise | Exact text/result given in rebuttal | Paper location | Status |
|----|-------------|---------|-------------------------------------|----------------|--------|
| P1 | R1, R3 | Add MoE-X baseline | Table in R1 response (acc 81.2±0.3) | Table 2 | pending |
```

icml-camera-ready checks this line by line before uploading the final version.
