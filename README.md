# ICML 论文写作 Skill Family

面向 coding agent（Claude Code 等）的一组 ICML 论文 skill，覆盖从研究仓库到 camera-ready 的完整周期。
基于 ICML 2026 官方规则（快照日期 2026-10-05）以及 Nanda、Farquhar、Foerster、Gopen & Swan、
Lipton、Perez、Parikh/Batra/Lee 等人的写作建议整理而成。

## 五个 skill

| Skill | 何时触发 | 核心产出 | 强制停下等人的点 |
|---|---|---|---|
| `icml-write` | 从仓库起草、修改已有稿、迁移到 ICML 格式 | 主张账本、段落大纲、带 `% TL;DR` 注释的正文 | ① 主张与摘要 ② 大纲、图表规划、页数预算 ③ 逻辑断层的真实解释 |
| `icml-cite` | 找文献、生成 BibTeX、核对参考文献 | 核验过的 `.bib` 与核验日志 | 无法核验的引用是否保留 |
| `icml-review` | 投稿前自查、模拟审稿 | 合规报告 + ICML 审稿表格式的模拟审稿 | 无（只读，不改稿） |
| `icml-rebuttal` | 收到审稿意见后 | 意见分类表、各轮回复、承诺清单 | 回应策略；是否指出审稿人失范；任何新实验结果 |
| `icml-camera-ready` | 录用后 | 去匿名化终稿、lay summary、提交清单 | 利益冲突声明；作者与单位信息 |

## 共享状态：`.icml/` 工作区

五个 skill 互不引用对方的安装目录，而是通过论文项目里的 `.icml/` 目录共享状态
（详见任一 skill 的 `references/workspace-contract.md`）：

- `claims.md`：主张账本。论文中每个数字都必须能追溯到项目里的结果文件。
- `outline.md`、`open_issues.md`（只有人能回答的问题）、`decisions.md`（人的决定与风格规则的例外理由）
- `citations_log.md`、`reviews/`、`rebuttal/`（含 `promises.md`）、`camera_ready.md`、`state.md`
- `venue_facts.md`：当年 ICML 规则。每个新周期必须刷新。

任何 skill 启动时都会运行 `scripts/init_workspace.py`，它只补缺、从不覆盖。

## 安装

使用 [`skills` CLI](https://github.com/vercel-labs/skills)（需要 Node.js），**在论文仓库的根目录**按需安装：

```bash
cd <你的论文仓库>

# 查看仓库里有哪些 skill
npx skills add a-green-hand-jack/icml-skills --list

# 只装当前阶段需要的 skill，例如写稿阶段：
npx skills add a-green-hand-jack/icml-skills --skill icml-write icml-cite icml-review -a claude-code
# 收到审稿意见后再加：
npx skills add a-green-hand-jack/icml-skills --skill icml-rebuttal -a claude-code

# 一次装全部五个
npx skills add a-green-hand-jack/icml-skills --skill '*' -a claude-code
```

- **每个 skill 都可以单独安装。** 每个 skill 目录自带所需的 `references/` 和 `scripts/`，不依赖其他
  skill 是否安装；它们之间只通过论文仓库里的 `.icml/` 共享状态。
- `-a` 指定 agent：`claude-code` 装到 `.claude/skills/`，其他常用值有 `codex`、`cursor`、`opencode`、
  `gemini-cli`；省略时 CLI 会自动检测或询问。
- 安装会在仓库根目录生成 `skills-lock.json`，记录每个 skill 的来源与版本。建议把它和 skill 目录
  一起提交，合作者 clone 后即可使用同一版本。
- 更新：`npx skills update -p`；卸载：`npx skills remove icml-cite`。
- 没有 Node.js 时，可以手动复制单个 skill：`cp -r icml-review <你的论文仓库>/.claude/skills/`。

**不建议加 `-g` 全局安装**，原因如下：

- 这些 skill 的触发描述刻意写得很宽（例如“看一下我的论文”“清理我的 bib”“make my intro better”）。
  全局安装后，它们会在与 ICML 无关的项目里抢触发。
- `icml-venue-facts.md` 绑定某一年的 ICML 规则。项目级安装让每篇论文锁定自己投稿周期的版本，
  更新一个仓库不会影响另一篇还在审稿或 rebuttal 中的论文。

依赖：Python 3（脚本只用标准库）。建议安装 TeX Live（pdflatex、bibtex）和 poppler-utils
（pdftotext、pdfinfo、pdffonts）；没有时相关检查会跳过并提示。`icml-cite` 需要访问
dblp.org、api.semanticscholar.org、export.arxiv.org、doi.org；不能联网时会明确降级为占位符，
绝不凭记忆补全引用。

不要与覆盖面很宽的通用论文 skill（如 davila7 的 `ml-paper-writing`）同时安装，避免抢触发。

## 维护

- **年份相关的规则只在 `_shared/references/icml-venue-facts.md` 修改**，然后运行
  `bash sync_shared.sh` 分发到各 skill。`workspace-contract.md`、`init_workspace.py`、
  `check_submission.py` 同理。
- 修改脚本后运行 `bash tests/run_tests.sh`（41 项回归测试；夹具中的 `icml2026.sty`
  是测试用桩文件，不是官方样式，切勿用于真实论文）。
- `tests/eval-prompts.md` 列出了用于评估 skill 行为（而不只是脚本）的测试提示词。

## 已知局限

- 合规检查是启发式的：页数判断依赖 PDF 文本中的结尾标题；匿名检查需要提供作者名与机构名。
  最终仍需官方 paper checker 和人工通读。
- `cite_lookup.py` 的线上 API 在构建环境中无法联网实测，只用模拟响应测试了解析逻辑；
  首次使用时请确认几个查询能正常返回。
- 写作参考材料以实证类论文为主；理论论文请补充课题组自己的规范。
- Position track 只做了最基本的支持（Alternative Views 检查、无 Impact Statement）。

## 主要来源

ICML 2026 Author Instructions / Call for Papers / Reviewer Instructions / example paper / Lay Summaries 博文；
Neel Nanda, *Highly Opinionated Advice on How to Write ML Papers* (2025)；
Sebastian Farquhar, *How to Write ML Papers* (2024)；Jakob Foerster, *How to ML Paper - A brief Guide*；
Gopen & Swan, *The Science of Scientific Writing* (1990)；Zachary Lipton, *Heuristics for Scientific Writing* (2018)；
Ethan Perez, *Easy Paper Writing Tips*；Parikh, Batra & Lee, *How we write rebuttals* (2020)。
各 skill 中的内容均为转述改写，示例为自编。
