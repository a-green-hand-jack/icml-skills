# ICML Review Criteria and Report Template

Based on the ICML 2026 reviewer guidelines (main track). Scoring criteria and phrasing are year-specific:
compare with `.icml/venue_facts.md` §6.

## Table of Contents
1. Reading Protocol
2. Four Dimensions, per ICML's Definitions
3. Scoring Rubric
4. Evidence Checklist (Soundness)
5. Presentation Checklist
6. Report Template

## 1. Reading Protocol

1. Read only the title + abstract + Figure 1. Write one sentence: what does this paper claim?
   If you cannot do this, that is a presentation finding.
2. Read the introduction. List the claims and promised evidence. Record the first place you feel confused or unconvinced.
3. Before reading the associated text, look at every figure and table and its caption.
   Write down what you think each figure/table shows. Then read the text and compare.
4. Read the methods and experiments sections with the claims list in hand. For each claim: which experiment supports it?
   Is it sufficient? What alternative explanations exist?
5. Skim related work: is recent work compared or glossed over?
6. Read the limitations. Did the authors state the weaknesses you found?
7. Check the appendix only if the main text depends on it (reviewers are not obligated to read it—if the main text needs it, that is a finding).

## 2. Four Dimensions (ICML's Own Framework, Paraphrased)

- **Soundness**: Is it technically correct? Are claims supported by theory or experiments? Is the method appropriate?
  Are proofs correct under reasonable assumptions? Is the experimental design sound? Did the authors honestly state strengths and weaknesses?
  *Judged independently of impact*: a modest paper can be fully sound; a high-impact idea must meet the same bar.
- **Presentation**: Is it clear and well structured? Is the narrative easy to follow?
  Is it positioned against prior and contemporaneous work with differences explained? Can an expert reproduce the results from the paper?
- **Significance**: Is it an important problem? Does it advance understanding, capability, or practice?
  Might subsequent work build on it? Is the breadth of impact commensurate with the contribution?
  Moderate or domain-specific gains can still be significant if they open a direction or have practical utility.
- **Originality**: New insights, deeper understanding, important properties of existing methods,
  new tasks/methods/theory/data/perspectives, or sufficiently reasoned novel combinations.
  Originality does not require a new method; careful evaluation that yields new insights also counts.

In addition: **Limitations** — authors should be rewarded, not penalized, for candidly stating limitations and potential negative societal impacts.

## 3. Scoring Rubric

Per dimension: 4 Excellent, 3 Good, 2 Fair, 1 Poor (fair/poor requires written justification in strengths/weaknesses).

Overall recommendation:
- 6 Strong Accept — technically flawless, exceptional impact, strong evaluation and reproducibility, no unresolved ethical issues.
- 5 Accept — technically solid, high impact on the subfield or medium-high impact across multiple fields,
  good to excellent evaluation and reproducibility.
- 4 Weak accept — technically solid, advances the subfield, others may build on it,
  but weaknesses (e.g., limited evaluation) constrain impact. Use sparingly.
- 3 Weak reject — clear strengths, but weaknesses outweigh strengths; needs revision before others can build on it.
  Use sparingly.
- 2 Reject — e.g., technical flaws, weak evaluation, insufficient reproducibility, or writing so poor that key claims are unintelligible.
- 1 Strong Reject — e.g., known results, unresolved ethical issues, or unable to tell what the contribution is at all.

Confidence: 5 Certain (checked math/details) … 1 Educated guess.

## 4. Evidence Checklist (Soundness)

- Every claim in the abstract/introduction has a matching experiment or theorem in the main text.
- Claim wording matches evidence strength (do not write "consistently" for 3/5 runs; do not write "proves" for experimental results; state scope).
- Baselines: strongest and most reasonable baselines, tuned with comparable effort, tuning process described.
  Every applicable method from related work is either compared or justified for non-comparison.
- Variance: number of runs, error bar definition, differences larger than noise;
  statistical tests when claims rely on small differences.
- Ablations for multi-component methods.
- Alternative explanations: for every headline result, the most obvious confounding factor — was it ruled out?
- Data: train/test leakage, contamination (especially LLM evaluation), qualitative example selection (was cherry-picking disclosed?).
- Compute and hyperparameters reported; code or sufficient detail to reproduce.
- Theory: assumptions explicit and reasonable; proof exists (appendix acceptable); theorem statements match what the main text claims they show.
- Text matches figures/tables (check numbers, trends, and what each line represents verbatim).
- Numbers are consistent across abstract, introduction, tables, and main text.

## 5. Presentation Checklist

- Contributions are clear before the end of page 1; methods start by pages 2–3.
- Figure 1 conveys the main idea or result; caption is self-contained; axes are labeled; legible in grayscale; colorblind-friendly.
- One term per concept; abbreviations are defined; notation is consistent.
- Related work compares and contrasts (at the methodology level), rather than listing.
- Background is limited to what is needed; boilerplate goes to the appendix.
- No superlative adjectives, hyped openers, or LLM-voice phrasing; no dangling "we will" promises; no broken citations.
- A limitations section exists and is specific.

## 6. Report Template

```markdown
# Simulated ICML Review — <Paper Title> — <Date>
Reviewer stance: <new context? what materials were read?>

## A. Compliance
### Desk-reject risk
- [CODE] <finding> — <location> — <fix>
### Must fix
### Recommended fix
### Completed / incomplete manual checks

## B. Review (ICML Main Track Form)
**Summary.** <3–5 sentences the authors would agree with>

**Claims and Evidence.**
| # | Claim (verbatim) | Evidence in paper | Sufficient? | Gap |
|---|---|---|---|---|

**Strengths.**
- Soundness: ...
- Presentation: ...
- Significance: ...
- Originality: ...

**Weaknesses.** (each with location and specific fix)
1. ...

**Scores.** Soundness x/4 · Presentation x/4 · Significance x/4 · Originality x/4 ·
Overall x/6 · Confidence x/5
Justification for any fair/poor ratings: ...

**Key questions for the authors.** (3–5; explain how each answer would change the score)
1. ...

**Limitations.** Present / Suggested: ...

**Other reviewer perspectives.**
- Theorist: ...
- Practitioner/baseline-focused: ...
- Adjacent subfield: ...

## C. Prioritized Fix List
| Priority | Issue | Location | Fix type (writing/experiment/citation/human) | Estimated effort |
|---|---|---|---|---|
```
