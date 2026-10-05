---
name: icml-review
description: 在投稿前审计 ICML 论文并模拟 ICML 同行评审。运行机械合规性检查（8 页限制、匿名性泄露包括 PDF 元数据、摘要格式、影响声明、禁止的布局技巧、视为提示注入的隐藏文本、损坏的引用），然后按照 ICML 的实际评审标准撰写评审意见——严谨性、表达、重要性、原创性、关键问题、局限性、总体分数。只读——它报告问题，不编辑论文。每当用户想要检查 ICML 初稿、进行批判、打分、压力测试、红队测试或"像审稿人一样评审"、想知道是否准备好投稿、询问审稿人会攻击什么，或想要格式/匿名性检查时，使用此技能——即使他们只说"看一下我的论文"或"准备好了吗？"。改写请使用 icml-write；回复真实评审意见请使用 icml-rebuttal。
compatibility: Python 3。可选 — poppler-utils (pdftotext, pdfinfo, pdffonts) 用于 PDF 检查；pdflatex 用于编译。
---

# ICML 投稿前评审

两项工作：(1) 捕获所有可能导致论文被 desk-rejected（直接拒稿）或因格式问题被悄悄降分的问题，(2) 像 ICML 审稿人一样阅读论文，然后报告他们会说什么。此技能不编辑论文。将评审与写作分开，既能让评审保持客观，也能清晰记录发现的问题。

用用户的语言与他们交流；评审报告本身用英文撰写（它模拟 OpenReview 表格），除非用户另有要求。

## 独立性至关重要

撰写论文的 agent 知道每句话的意图，因此不会注意到读者在哪里感到困惑。Farquhar 也指出，LLM 倾向于赞同他人观点，需要反复推动才能进行真正的批判。因此：
- 最好在一个**未见过起草对话的新会话或子 agent** 中运行此技能。给它 PDF（或 LaTeX），最多再提供 `.icml/venue_facts.md`。不要给它 `claims.md` 或评审用的笔记——审稿人不会有这些材料。
- 像一位忙碌的专家一样阅读，手头有 5–10 篇论文要审：标题、摘要、图 1、引言、图表，然后是其余部分。记录你会在哪里停止阅读。
- 假设一个大胆的主张是错的，然后寻找漏洞（Nanda）。再检查论文是否已经预先回应了它。
- 要具体。每个弱点必须指出位置，并说明如何修复。

## 第 0 步 — 准备

运行 `python scripts/init_workspace.py --root <latex-root> --skill icml-review`。读取
`.icml/venue_facts.md`（如果没有工作区则读取 `references/icml-venue-facts.md`）；
如果目标年份不同，则刷新它。如果可能，编译论文，这样你审阅的就是审稿人将看到的 PDF。

## A 部分 — 合规性审计（机械检查）

```bash
python scripts/check_submission.py --tex main.tex --pdf main.pdf \
    --names "First Last,First Last" --affils "University,Lab,Company" \
    [--pristine-sty /path/to/official/icml2026.sty] [--position-track]
```

如果你不知道作者姓名和 affiliations（以及实验室/集群名称、用户名），向用户询问；
没有这些信息，匿名性检查会很弱。然后做脚本无法做的检查，列在
`references/compliance-checks.md` 中：打开图表检查嵌入的姓名，
检查补充代码中的身份泄露，阅读每一条自引，确认 OpenReview 摘要是否匹配，
确认审稿人需要的内容没有只存在于附录中。

如果 icml-cite 可用，同时运行它的 `check_bib.py`。否则至少确认 PDF 中没有 `??` 或 `(?)`，
也没有占位引用 key。

对发现进行分类：**Desk-reject 风险**（页数限制、匿名性、缺少影响声明、
隐藏文本、模板修改）、**必须修复**、**建议修复**。

## B 部分 — 模拟 ICML 评审

阅读 `references/review-rubric.md` 并填写其模板。简要说明：
1. **Summary**：用你自己的话写一个作者会同意的内容摘要。
2. **Claims check**：列出论文的主张（来自摘要、引言、贡献列表）；
   对每个主张，检查提供的证据是否充分。这是严谨性的核心。
   检查图表的文字描述是否完全属实。
3. **Strengths and weaknesses**：涵盖严谨性、表达、重要性、
   原创性——采用 ICML 对原创性的宽泛定义（对现有方法的新洞察也算），
   并且将严谨性与影响力分开评判。
4. **Scores**：按照 ICML 的评分标准（每个维度 1–4，总体 1–6，置信度 1–5），
   每个 "fair"/"poor" 都要给出理由。
5. **Key questions**（3–5 个，编号）：答案会改变分数的问题。
   这些是最有用的输出：它们预测了 rebuttal。
6. **Limitations** 评估。
7. **Reviewer-type variants**：简要说明怀疑派理论家、
   想要基线和计算细节的实践者、以及来自相邻子领域的审稿人各自会如何反应。

校准：大多数投稿不会被接收。除非论文在每个维度上真正很强，否则不要给 5–6；
如果你发现自己什么都夸，回去找最弱的主张。

## C 部分 — 报告与交接

将报告写入 `.icml/reviews/simulated-<YYYY-MM-DD>.md`（格式见 rubric 文件），
内容包括：按严重程度排列的合规性发现、模拟评审、以及一个优先级排序的修复列表，
将每个问题映射到论文中的位置和修复类型（写作、实验、引用、人工决策）。
将只能由人工处理的事项添加到 `open_issues.md`。
更新 `state.md`。用通俗语言告诉用户三件最重要的事，
并建议将修复列表交给 icml-write；将关键问题留给 icml-rebuttal。

在此技能中，即使是最小的修复也不要编辑论文——把它们列出来。

## 文件

- `scripts/check_submission.py` — 机械合规性检查（与 icml-camera-ready 共享）。
- `scripts/init_workspace.py` — 创建共享的 `.icml/` 工作区。
- `references/review-rubric.md` — ICML 评审表、评分标准、阅读协议、报告模板。
- `references/compliance-checks.md` — 每个检查的含义、如何修复、人工检查项。
- `references/icml-venue-facts.md`、`references/workspace-contract.md` — 共享文件。
