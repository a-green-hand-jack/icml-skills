# ICML Review Rubric and Report Template

Based on the ICML 2026 Reviewer Instructions (main track). Scales and wording are
year-specific: compare with `.icml/venue_facts.md` §6.

## Contents
1. Reading protocol
2. The four dimensions, as ICML defines them
3. Scales
4. Evidence checklist (soundness)
5. Presentation checklist
6. Report template

## 1. Reading protocol

1. Read title + abstract + Figure 1 only. Write one sentence: what does the paper claim?
   If you cannot, that is a presentation finding.
2. Read the introduction. List the claims and the promised evidence. Note the first
   place you were confused or unconvinced.
3. Look at every figure and table with its caption before reading the text about it.
   Write what you think each shows. Then read the text and compare.
4. Read method and experiments with the claims list in hand. For each claim: which
   experiment supports it? Is it sufficient? What alternative explanation remains?
5. Skim related work: is the closest work compared against or excused?
6. Read limitations. Did the authors name the weaknesses you found?
7. Check the appendix only for things the main text depends on (reviewers are not
   required to read it - if the main text needs it, that is a finding).

## 2. The four dimensions (ICML's own framing, paraphrased)

- **Soundness**: technically correct? Claims supported by theory or experiments? Methods
  appropriate? Proofs correct under reasonable assumptions? Experiments well designed?
  Are the authors honest about strengths and weaknesses? *Judged separately from
  impact*: a modest paper can be fully sound; a high-impact idea must meet the same bar.
- **Presentation**: clear and well structured? Narrative easy to follow? Positioned
  against prior and concurrent work, with differences stated? Could an expert reproduce
  the results from the paper?
- **Significance**: important problem? Advances understanding, capabilities or practice?
  Likely to be built on? Is the breadth of impact appropriate to the contribution? Modest
  or domain-specific gains can still be significant if they unlock directions or are
  practically useful.
- **Originality**: new insights, deeper understanding, important properties of existing
  methods, new tasks/methods/theory/data/perspectives, or well-reasoned novel
  combinations. Originality does not require a new method; careful evaluation that
  yields new insight counts equally.

Also: **Limitations** - authors should be rewarded, not punished, for being upfront
about limitations and potential negative societal impact.

## 3. Scales

Per dimension: 4 excellent, 3 good, 2 fair, 1 poor (fair/poor need a written
justification in strengths and weaknesses).

Overall recommendation:
- 6 Strong Accept - technically flawless, exceptional impact, strong evaluation and
  reproducibility, no unaddressed ethical issues.
- 5 Accept - technically solid, high impact on a sub-area or moderate-to-high on several,
  good-to-excellent evaluation and reproducibility.
- 4 Weak accept - technically solid, advances a sub-area, others likely to build on it,
  but weaknesses (e.g., limited evaluation) limit impact. Use sparingly.
- 3 Weak reject - clear merits, but weaknesses outweigh them; needs revision before
  others can build on it. Use sparingly.
- 2 Reject - e.g., technical flaws, weak evaluation, inadequate reproducibility, or
  writing too poor to understand the key claims.
- 1 Strong Reject - e.g., well-known results, unaddressed ethics, or impossible to tell
  what the contribution is.

Confidence: 5 certain (checked math/details) … 1 educated guess.

## 4. Evidence checklist (soundness)

- Each claim in abstract/intro has a matching experiment or theorem in the main body.
- Claim wording matches evidence strength (no "consistently" for 3 of 5; no "proves"
  for empirical results; scope stated).
- Baselines: strongest reasonable ones, tuned with comparable effort, tuning described.
  Every applicable method from related work is compared or excused.
- Variance: number of runs, error bars defined, differences larger than noise;
  statistical tests where claims rest on small differences.
- Ablations for multi-component methods.
- Alternative explanations: for each headline result, the most obvious confound - is
  it ruled out?
- Data: train/test leakage, contamination (especially for LLM evaluations), selection of
  qualitative examples (cherry-picking disclosed?).
- Compute and hyperparameters reported; code or enough detail to reproduce.
- Theory: assumptions explicit and reasonable; proofs present (appendix ok); theorem
  statements match what the text claims they show.
- Text matches figures/tables (literally check numbers, trends and which line is which).
- Numbers consistent across abstract, intro, tables and text.

## 5. Presentation checklist

- Contribution clear by the end of page 1; method begins by page 2–3.
- Figure 1 conveys the main idea or result; captions stand alone; axes labelled; legible
  in grayscale; colorblind-safe.
- One term per concept; acronyms defined; notation consistent.
- Related work compares and contrasts (methodologically), not a list.
- Background limited to what is needed; boilerplate in the appendix.
- No overclaiming adjectives, hype openers, or LLM-tell phrasing; no dangling
  "we will" promises; no broken references.
- Limitations section exists and is specific.

## 6. Report template

```markdown
# Simulated ICML Review — <paper title> — <date>
Reviewer stance: <fresh context? which materials were read?>

## A. Compliance
### Desk-reject risks
- [CODE] <finding> — <location> — <fix>
### Must fix
### Should fix
### Manual checks done / not done

## B. Review (ICML main-track form)
**Summary.** <3–5 sentences the authors would agree with>

**Claims and evidence.**
| # | Claim (as stated) | Evidence in paper | Sufficient? | Gap |
|---|---|---|---|---|

**Strengths.**
- Soundness: ...
- Presentation: ...
- Significance: ...
- Originality: ...

**Weaknesses.** (each with location and a concrete fix)
1. ...

**Scores.** Soundness x/4 · Presentation x/4 · Significance x/4 · Originality x/4 ·
Overall x/6 · Confidence x/5
Justification for any fair/poor: ...

**Key questions for the authors.** (3–5; say how each answer would change the score)
1. ...

**Limitations.** yes / suggestions: ...

**Other reviewer perspectives.**
- Theory-minded: ...
- Practitioner/baselines: ...
- Neighbouring subfield: ...

## C. Prioritised fix list
| Priority | Issue | Location | Fix type (writing/experiment/citation/human) | Est. effort |
|---|---|---|---|---|
```
