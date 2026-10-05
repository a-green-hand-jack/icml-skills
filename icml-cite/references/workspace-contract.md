# `.icml/` 工作区契约

本系列全部五个 skill（icml-write、icml-cite、icml-review、icml-rebuttal、
icml-camera-ready）通过论文项目中的文件共享状态，从不通过彼此的安装目录。
单个 skill 可以单独安装；工作区才是连接它们的纽带。每个 skill 在接触工作区之前
必须阅读本契约，并保持以下格式，以便其他 skill 能够解析。

## 位置

`.icml/` 位于论文主 `.tex` 文件（LaTeX 根目录）旁边。如果论文在一个更大的研究仓库内部，
通常是 `paper/.icml/`。通过以下命令创建：

```bash
python <skill-dir>/scripts/init_workspace.py --root <latex-root>
```

该脚本永远不会覆盖现有文件。每次会话开始时安全运行。

## 文件

| 文件 | 所有者（写入方） | 读取方 | 用途 |
|---|---|---|---|
| `state.md` | 每个 skill | 每个 skill | 当前阶段、最后操作、下一步、待处理检查点。首先阅读，最后更新。让新会话能够续接。 |
| `venue_facts.md` | 首个运行的 skill；每周期刷新 | 全部 | 年份专属的 ICML 规则（从 skill 的 `icml-venue-facts.md` 复制，随后刷新） |
| `claims.md` | icml-write（人类审批） | 全部 | **论断账本**：论文中的论断和报告的每个数字，都追溯到源文件。数字的唯一真实来源。 |
| `outline.md` | icml-write | icml-write、icml-review | 摘要草稿、每段一行的大纲、图的计划、页数预算 |
| `open_issues.md` | 任意 skill | 人类、全部 | 只有人类能回答的问题：逻辑漏洞、无法验证的引用、论断强度判断、缺失证据 |
| `decisions.md` | 任意 skill（记录人类决策） | 全部 | 带日期的人类决策日志，以及偏离样式规则的合理理由 |
| `citations_log.md` | icml-cite | icml-cite、icml-review、icml-camera-ready | 每个 key 的验证记录 |
| `reviews/` | icml-review（模拟）、icml-rebuttal（真实） | icml-write、icml-rebuttal | icml-review 的 `simulated-YYYY-MM-DD.md`；用户粘贴的真实审稿 `R-<id>.md` |
| `rebuttal/` | icml-rebuttal | icml-camera-ready | `triage.md`、`round1/<reviewer>.md`、`round2/...`、`promises.md` |
| `camera_ready.md` | icml-camera-ready | — | 检查清单状态 |

## 其他 skill 会解析的格式

### `claims.md`

两部分。保持标题完全一致。

```markdown
## Claims
### C1 — <一句话概括的论断>
- Strength: systematic | existence-proof | narrow | hedged | theorem
- Status: proposed | approved | revised | dropped
- Evidence: E1, E2（下表中的编号）；figure/table: fig:main
- Red-team notes: <该论断可能如何被推翻；已检查过什么>

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
| N1 | 92.1 | % | results/main_seed_avg.json | ours.test_acc.mean | yes |
| N2 | 0.4 | % | results/main_seed_avg.json | ours.test_acc.std | yes |
```

规则：`value` 必须与论文中将要呈现的形式完全一致（相同的舍入）。
`verified` 仅在从本项目源文件读取该值时为 `yes`（不是回忆来的，也不是从草稿复制来的）。
来自其他论文的数字（从出版物复制的基线数字）使用 `cite:<bibkey>` 作为 source，
locator 为 `Table 2` 等。

### `open_issues.md`

```markdown
- [ ] OI-7 (icml-write, 2026-01-12) [gap] Sec 4.2 para 3: why does warmup fix the instability? Draft currently asserts no mechanism. Options: (a) cite X, (b) add ablation, (c) soften to observation.
- [x] OI-3 ... resolved 2026-01-10 → see decisions.md D-4
```

标签：`[gap]` 逻辑漏洞，`[cite]` 未验证引用，`[claim]` 论断强度，
`[evidence]` 缺失/未验证证据，`[anon]` 匿名性，`[policy]` 会议规则问题。

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

- 绝不要删除其他 skill 的记录；将它们标记为已解决或已取代。
- 每条记录都标注日期（ISO 格式）。注明写入该记录的 skill。
- 如果 `.icml/` 缺失（例如用户直接将旧草稿带入 rebuttal），先运行 `init_workspace.py`，
  然后仅重建当前任务所需的内容，并在 `state.md` 中记录缺失了什么。
