# `.icml/` 工作区契约

本技能族中的五个技能（icml-write、icml-cite、icml-review、icml-rebuttal、
icml-camera-ready）通过论文项目中的文件共享状态，而从不通过彼此的安装文件夹。
一个技能可以单独安装；工作区才是连接它们的纽带。每个技能在操作工作区前
必须阅读本契约，并必须保持以下格式，以便其他技能能够解析。

## 位置

`.icml/` 位于论文主 `.tex` 文件（LaTeX 根目录）的同级目录。若论文位于
更大的研究仓库内部，通常路径为 `paper/.icml/`。通过以下命令创建：

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

该脚本永远不会覆盖已有文件。在每次会话开始时运行都是安全的。

## 文件

| 文件 | 所有者（写入方） | 读取方 | 用途 |
|---|---|---|---|
| `state.md` | 每个技能 | 每个技能 | 当前阶段、最后操作、下一步、开放检查点。最先读取，最后更新。让新会话能够恢复。 |
| `venue_facts.md` | 首个运行的技能；按周期刷新 | 所有技能 | 年度特定的 ICML 规则（从技能的 `icml-venue-facts.md` 复制，随后刷新） |
| `claims.md` | icml-write（需人类批准） | 所有技能 | **声明账本**：论文中的所有声明及报告的每个数字，均可追溯至源文件。数字的唯一真实来源。 |
| `outline.md` | icml-write | icml-write、icml-review | 摘要草稿、每段一行的提纲、图表计划、页数预算 |
| `open_issues.md` | 任意技能 | 人类、所有技能 | 仅人类能回答的问题：逻辑缺口、无法验证的引用、声明强度判断、缺失证据 |
| `decisions.md` | 任意技能（记录人类决策） | 所有技能 | 带日期的决策日志，以及样式规则的合理偏离 |
| `citations_log.md` | icml-cite | icml-cite、icml-review、icml-camera-ready | 逐条键的验证记录 |
| `reviews/` | icml-review（模拟）、icml-rebuttal（真实） | icml-write、icml-rebuttal | `simulated-YYYY-MM-DD.md` 来自 icml-review；`R-<id>.md` 为用户粘贴的真实审稿意见 |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`、`round1/<reviewer>.md`、`round2/...`、`promises.md` |
| `camera_ready.md` | icml-camera-ready | — | 检查清单状态 |

## 其他技能解析的格式

### `claims.md`

两部分。保持标题完全不变。

```markdown
## Claims
### C1 — <一句话声明>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1, E2（下表中的编号）；figure/table: fig:main
- Red-team notes: <该声明如何可能为假；已检查的内容>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

规则：`value` 必须与论文中将要呈现的形式完全一致（相同的舍入）。
`verified` 仅在值是从本项目源文件中读取时（而非凭记忆、非从草稿复制）才标记为 `yes`。
来自其他论文的数字（从出版物复制的基线数字）使用 source `cite:<bibkey>` 与 locator `Table 2` 等。

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] 第 4.2 节第 3 段：为什么 warm-up 能修复不稳定性？草稿目前未给出机制。选项：(a) 引用 X，(b) 添加消融实验，(c) 弱化为观察结果。
- [x] OI-3 ... 已于 2026-01-10 解决 → 见 decisions.md D-4
```

标签：`[gap]` 逻辑缺口，`[cite]` 未验证引用，`[claim]` 声明强度，
`[evidence]` 缺失/未验证证据，`[anon]` 匿名性，`[policy]` 会议规则问题。

### `decisions.md`

```markdown
- D-4 (2026-01-10, human) 相关工作放在实验之后。
- D-5 (2026-01-11, agent, rule-deviation) 第 3 节第 2 段保留被动语态：“Tokens are routed by the gate”保持“tokens”作为段落主题（Gopen & Swan 主题位置原则）。
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

- 切勿删除其他技能的记录；将其标记为已解决或已取代。
- 每条记录标注日期（ISO 格式）。注明写入的技能名称。
- 若 `.icml/` 缺失（例如用户直接将旧草稿带入反驳阶段），运行
  `init_workspace.py`，然后仅重建当前任务所需的内容，并在 `state.md` 中记录缺失项。
