# `.icml/` Workspace Contract

The five skills in this family (icml-write, icml-cite, icml-review,
icml-rebuttal, icml-camera-ready) share state through files in the paper
project, never through their individual installation folders.
A skill can be installed individually; the workspace is what connects them.
Each skill must read this contract before operating on the workspace, and
must preserve the formats below so that other skills can parse them.

## Location

`.icml/` sits next to the paper's main `.tex` file (the LaTeX root). If the
paper lives inside a larger research repository, the path is typically
`paper/.icml/`. Created via:

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

This script never overwrites existing files. It is safe to run at the start
of every session.

## Files

| File | Owner (writer) | Readers | Purpose |
|---|---|---|---|
| `state.md` | Every skill | Every skill | Current phase, last action, next step, open checkpoints. Read first, updated last. Enables new sessions to resume. |
| `venue_facts.md` | First skill to run; refreshed per cycle | All skills | Year-specific ICML rules (copied from the skill's `icml-venue-facts.md`, then refreshed) |
| `claims.md` | icml-write (requires human approval) | All skills | **Claims ledger**: every claim in the paper and every reported number, traceable to source files. Single source of truth for numbers. |
| `outline.md` | icml-write | icml-write, icml-review | Abstract draft, one-line-per-paragraph outline, figure plan, page budget |
| `open_issues.md` | Any skill | Human, all skills | Questions only a human can answer: logical gaps, unverifiable citations, claim strength judgments, missing evidence |
| `decisions.md` | Any skill (records human decisions) | All skills | Dated decision log, plus reasonable deviations from style rules |
| `citations_log.md` | icml-cite | icml-cite, icml-review, icml-camera-ready | Per-key verification records |
| `reviews/` | icml-review (simulated), icml-rebuttal (real) | icml-write, icml-rebuttal | `simulated-YYYY-MM-DD.md` from icml-review; `R-<id>.md` for real reviews pasted by the user |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`, `round1/<reviewer>.md`, `round2/...`, `promises.md` |
| `camera_ready.md` | icml-camera-ready | — | Checklist status |

## Formats Parsed by Other Skills

### `claims.md`

Two parts. Keep the headings exactly as shown.

```markdown
## Claims
### C1 — <one-sentence claim>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1, E2 (numbers in the table below); figure/table: fig:main
- Red-team notes: <how this claim could be false; what has been checked>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

Rules: `value` must match exactly the form to be presented in the paper (same rounding).
`verified` is marked `yes` only when the value is read from a source file in this project (not from memory, not copied from a draft).
Numbers from other papers (baseline numbers copied from publications) use source `cite:<bibkey>` and locator `Table 2`, etc.

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] Section 4.2 paragraph 3: Why does warm-up fix instability? The draft currently gives no mechanism. Options: (a) cite X, (b) add ablation, (c) weaken to an observation.
- [x] OI-3 ... resolved on 2026-01-10 → see decisions.md D-4
```

Tags: `[gap]` logical gap, `[cite]` unverified citation, `[claim]` claim strength,
`[evidence]` missing/unverified evidence, `[anon]` anonymity, `[policy]` conference rules issue.

### `decisions.md`

```markdown
- D-4 (2026-01-10, human) Related work placed after experiments.
- D-5 (2026-01-11, agent, rule-deviation) Section 3 paragraph 2 retains passive voice: "Tokens are routed by the gate" keeps "tokens" as the paragraph topic (Gopen & Swan topic-position principle).
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

- Never delete another skill's records; mark them as resolved or superseded.
- Date every record (ISO format). Note the writing skill's name.
- If `.icml/` is missing (e.g., the user brings an old draft directly into rebuttal), run
  `init_workspace.py`, then rebuild only what the current task requires, and log the missing items in `state.md`.
