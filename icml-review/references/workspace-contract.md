# `.icml/` 工作区合约

本家族中的五个技能（icml-write、icml-cite、icml-review、icml-rebuttal、
icml-camera-ready）通过论文项目中的文件共享状态，从不通过彼此的安装文件夹。
一个技能可以单独安装；工作区是连接它们的纽带。每个技能在触碰工作区之前
必须阅读本合约，并保持以下格式，以便其他技能能解析它们。

## 位置

`.icml/` 位于论文主 `.tex` 文件旁边（LaTeX 根目录）。如果论文位于更大的研究仓库中，
通常是 `paper/.icml/`。用以下命令创建：

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

该脚本从不覆盖现有文件。每次会话开始时安全运行。

## 文件

| 文件 | 拥有者（写入方） | 读取方 | 用途 |
|---|---|---|---|
| `state.md` | 每个技能 | 每个技能 | 当前阶段、上次操作、下一步、开放的检查点。最先读取，最后更新。让新会话可以恢复。 |
| `venue_facts.md` | 第一个运行的技能；每周期刷新 | 全部 | 年份特定的 ICML 规则（从技能的 `icml-venue-facts.md` 复制，然后刷新） |
| `claims.md` | icml-write（人工审批） | 全部 | **主张台账**：论文的主张和报告的每个数字，每个都追溯到源文件。数字的唯一真实来源。 |
| `outline.md` | icml-write | icml-write、icml-review | 摘要草稿、每段一行的大纲、图表计划、页数预算 |
| `open_issues.md` | 任何技能 | 人工、全部 | 只有人工能回答的问题：逻辑缺口、无法验证的引用、主张强度判断、缺失证据 |
| `decisions.md` | 任何技能（记录人工决策） | 全部 | 人工所做决策的带日期日志，以及对样式规则的合理偏离 |
| `citations_log.md` | icml-cite | icml-cite、icml-review、icml-camera-ready | 每个 key 的验证记录 |
| `reviews/` | icml-review（模拟）、icml-rebuttal（真实） | icml-write、icml-rebuttal | icml-review 的 `simulated-YYYY-MM-DD.md`；用户粘贴的真实评审 `R-<id>.md` |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`、`round1/<reviewer>.md`、`round2/...`、`promises.md` |
| `camera_ready.md` | icml-camera-ready | — | 检查清单状态 |

## 其他技能解析的格式

### `claims.md`

两部分。保持标题完全不变。

```markdown
## Claims
### C1 — <一句话主张>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1, E2（下表中的编号）；figure/table: fig:main
- Red-team notes: <这怎么可能是错的；检查了什么>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

规则：`value` 必须与论文中出现的完全一致（相同舍入）。
`verified` 仅在值是从本项目源文件中读取的（不是回忆的，不是从草稿复制的）时才为 `yes`。
来自其他论文的数字（从出版物复制的基线数字）使用源 `cite:<bibkey>` 和定位符 `Table 2` 等。

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] Sec 4.2 para 3: why does warmup fix the instability? Draft currently asserts no mechanism. Options: (a) cite X, (b) add ablation, (c) soften to observation.
- [x] OI-3 ... resolved 2026-01-10 → see decisions.md D-4
```

标签：`[gap]` 逻辑缺口，`[cite]` 未验证引用，`[claim]` 主张强度，
`[evidence]` 缺失/未验证证据，`[anon]` 匿名性，`[policy]` 会场规则问题。

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

## 礼仪

- 永远不要删除其他技能的记录；将它们标记为已解决或已取代。
- 每条记录标注日期（ISO 格式）。注明写入它的技能。
- 如果 `.icml/` 缺失（例如，用户直接带着旧草稿来找 rebuttal），运行
  `init_workspace.py`，然后仅重建当前任务所需的内容，并在 `state.md` 中记录缺少什么。
