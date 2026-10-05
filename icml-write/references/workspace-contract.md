# The `.icml/` Workspace Contract

All five skills in this family (icml-write, icml-cite, icml-review, icml-rebuttal,
icml-camera-ready) share state through files in the paper project, never through each
other's installation folders. A skill may be installed alone; the workspace is what
connects them. Every skill must read this contract before touching the workspace and
must keep the formats below so the other skills can parse them.

## Location

`.icml/` lives next to the main `.tex` file of the paper (the LaTeX root). If the paper
is inside a larger research repo, that is usually `paper/.icml/`. Create it with:

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

The script never overwrites existing files. Safe to run at the start of every session.

## Files

| File | Owner (writes) | Readers | Purpose |
|---|---|---|---|
| `state.md` | every skill | every skill | Current phase, last action, next step, open checkpoints. Read first, update last. Lets a new session resume. |
| `venue_facts.md` | first skill to run; refresh per cycle | all | Year-specific ICML rules (copied from the skill's `icml-venue-facts.md`, then refreshed) |
| `claims.md` | icml-write (humans approve) | all | **Claims ledger**: the paper's claims and every number the paper reports, each traced to a source file. The single source of truth for numbers. |
| `outline.md` | icml-write | icml-write, icml-review | Abstract draft, one-line-per-paragraph outline, figure plan, page budget |
| `open_issues.md` | any skill | human, all | Questions only a human can answer: logical gaps, unverifiable citations, claim-strength calls, missing evidence |
| `decisions.md` | any skill (records human decisions) | all | Dated log of decisions the human made, plus justified deviations from style rules |
| `citations_log.md` | icml-cite | icml-cite, icml-review, icml-camera-ready | Per-key verification record |
| `reviews/` | icml-review (simulated), icml-rebuttal (real) | icml-write, icml-rebuttal | `simulated-YYYY-MM-DD.md` from icml-review; `R-<id>.md` real reviews pasted by the user |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`, `round1/<reviewer>.md`, `round2/...`, `promises.md` |
| `camera_ready.md` | icml-camera-ready | — | Checklist status |

## Formats other skills parse

### `claims.md`

Two parts. Keep the headings exactly.

```markdown
## Claims
### C1 — <one-sentence claim>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1, E2 (numbers in the table below); figure/table: fig:main
- Red-team notes: <how this could be false; what was checked>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

Rules: `value` is written exactly as it will appear in the paper (same rounding).
`verified` is `yes` only if the value was read from the source file in this project
(not recalled, not copied from a draft). Numbers from other papers (baseline numbers
copied from a publication) use source `cite:<bibkey>` and locator `Table 2` etc.

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] Sec 4.2 para 3: why does warmup fix the instability? Draft currently asserts no mechanism. Options: (a) cite X, (b) add ablation, (c) soften to observation.
- [x] OI-3 ... resolved 2026-01-10 → see decisions.md D-4
```

Tags: `[gap]` logical gap, `[cite]` unverified citation, `[claim]` claim strength,
`[evidence]` missing/unverified evidence, `[anon]` anonymity, `[policy]` venue rule question.

### `decisions.md`

```markdown
- D-4 (2026-01-10, human) Related work goes after experiments.
- D-5 (2026-01-11, agent, rule-deviation) Kept passive voice in Sec 3 para 2: "Tokens are routed by the gate" keeps "tokens" as the paragraph's topic (Gopen & Swan topic position).
```

### `state.md`

```markdown
# State
- Phase: outline (checkpoint 2 pending)
- Last action (2026-01-12, icml-write): drafted outline.md v2
- Next step: wait for human approval of outline.md; then draft Sec 1–3
- Blocking: OI-7, OI-9
```

## Etiquette

- Never delete another skill's records; mark them resolved or superseded.
- Date every entry (ISO format). Name the skill that wrote it.
- If `.icml/` is missing (e.g., a user brings an old draft straight to rebuttal), run
  `init_workspace.py`, then rebuild only what the current task needs and record in
  `state.md` what is missing.
