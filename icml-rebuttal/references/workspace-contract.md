# The `.icml/` Workspace Contract（`.icml/` 工作区契约）

All five skills in this family（icml-write、icml-cite、icml-review、icml-rebuttal、
icml-camera-ready）share state through files in the paper project，never through each
other's installation folders。A skill may be installed alone；the workspace is what
connects them。Every skill must read this contract before touching the workspace and
must keep the formats below so the other skills can parse them。

## Location（位置）

`.icml/` lives next to the main `.tex` file of the paper（the LaTeX root）。If the paper
is inside a larger research repo，that is usually `paper/.icml/`。Create it with：

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

The script never overwrites existing files。Safe to run at the start of every session。

## Files（文件）

| File | Owner（writes）（写入方） | Readers（读取方） | Purpose |
|---|---|---|---|
| `state.md` | every skill | every skill | 当前阶段、最后操作、下一步、待解决检查点。首先阅读，最后更新。让新会话能够恢复。 |
| `venue_facts.md` | first skill to run；refresh per cycle | all | 年度特定的 ICML 规则（从技能的 `icml-venue-facts.md` 复制，然后刷新） |
| `claims.md` | icml-write（humans approve） | all | **Claims ledger**：论文的所有 claims 及其报告的每个数字，每个都追溯到源文件。数字的唯一事实来源。 |
| `outline.md` | icml-write | icml-write、icml-review | 摘要草稿、每段一行的 outline、图表计划、页数预算 |
| `open_issues.md` | any skill | human、all | 只有人类能回答的问题：逻辑缺口、无法核实的引用、claim-strength 判断、缺失证据 |
| `decisions.md` | any skill（records human decisions） | all | 人类做出的决策的带日期日志，以及对样式规则的合理偏离 |
| `citations_log.md` | icml-cite | icml-cite、icml-review、icml-camera-ready | Per-key verification record |
| `reviews/` | icml-review（simulated）、icml-rebuttal（real） | icml-write、icml-rebuttal | `simulated-YYYY-MM-DD.md` from icml-review；`R-<id>.md` real reviews pasted by the user |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`、`round1/<reviewer>.md`、`round2/...`、`promises.md` |
| `camera_ready.md` | icml-camera-ready | — | Checklist status |

## Formats other skills parse（其他技能解析的格式）

### `claims.md`

Two parts。Keep the headings exactly。

```markdown
## Claims
### C1 — <one-sentence claim>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1、E2（下方表格中的数字）；figure/table: fig:main
- Red-team notes: <该 claim 如何可能不成立；已检查的内容>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

Rules：`value` 必须与论文中将出现的形式完全一致（相同的 rounding）。
`verified` 仅在值是从本项目中的源文件读取时才标记为 `yes`（非回忆、非从草稿复制）。
来自其他论文的数字（从出版物复制的 baseline 数字）使用 source `cite:<bibkey>` 和 locator `Table 2` 等。

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] Sec 4.2 para 3: why does warmup fix the instability? Draft currently asserts no mechanism. Options: (a) cite X, (b) add ablation, (c) soften to observation.
- [x] OI-3 ... resolved 2026-01-10 → see decisions.md D-4
```

Tags：`[gap]` 逻辑缺口，`[cite]` 未核实引用，`[claim]` claim strength，
`[evidence]` 缺失/未核实证据，`[anon]` 匿名性，`[policy]` 会场规则问题。

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

## Etiquette（礼仪）

- Never delete another skill's records；mark them resolved or superseded。
- Date every entry（ISO format）。Name the skill that wrote it。
- If `.icml/` is missing（e.g.，a user brings an old draft straight to rebuttal），run
  `init_workspace.py`，then rebuild only what the current task needs and record in
  `state.md` what is missing。
