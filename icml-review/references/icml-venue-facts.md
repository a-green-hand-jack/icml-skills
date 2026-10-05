# ICML 会场事实（快照：ICML 2026）

**快照日期：** 2026-10-05。**适用对象：** ICML 2026（首尔，2026 年 7 月 6–11 日）。
这里的每个数字和政策都是年份特定的。在为新周期依赖它之前，
请先刷新（见底部的 "How to refresh"）。当本文件与实时官方页面冲突时，
以实时页面为准。

本快照构建时参考的官方来源：
- Author Instructions: https://icml.cc/Conferences/2026/AuthorInstructions
- Call for Papers: https://icml.cc/Conferences/2026/CallForPapers
- Reviewer Instructions: https://icml.cc/Conferences/2026/ReviewerInstructions
- Example paper (PDF): https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- Style files: https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. 格式（投稿）

| 项目 | 要求 |
|---|---|
| 主文 | **最多 8 页** — 超过即自动拒稿 |
| 参考文献、附录、影响声明 | 不限页数，同一份 PDF |
| 排版 | 仅限 LaTeX，官方 `icml2026.sty`，`\usepackage{icml2026}`（不加 `accepted` 选项） |
| 布局 | 双栏，US Letter（非 A4），10pt Times |
| 样式修改 | 禁止。不要修改模板或压缩纵向间距 |
| 投稿 PDF 大小 | 50 MB（Author Instructions 页面）。示例论文仍写 10 MB；遵循 Author Instructions 页面并尽量保持小巧 |
| 摘要 | 一段，理想 4–6 句。严重违规必须在定稿时修正 |
| 标题与标题 | 实词首字母大写，禁止全大写。最多三级标题 |
| 图表 | 标题**在下**；图形内部不要有标题；标注坐标轴；每条曲线有图例；绘图使用矢量图（PDF/EPS） |
| 表格 | 标题**在上** |
| 伪代码 | `algorithm` + `algorithmic` 环境（随样式文件提供） |
| 引用 | 通过 `natbib` + `icml2026.bst` 使用 APA 作者–年份格式。多篇引用按时间顺序排列。保护 BibTeX 标题中的大写：`{B}ayesian`、`{L}ipschitz` |
| 字体 | 示例论文要求 Type-1 字体；2026 定稿说明中没有 Type 3 检查。使用 pdflatex 和矢量图；将 Type 3 视为警告 |

## 2. 匿名性（双盲）

- 不显示作者姓名或单位（样式会在非 `accepted` 时隐藏 `\icmlauthor`）。
- 无致谢、资助编号或指向公开（非匿名）代码仓库的链接。
- 以第三人称引用自己之前的工作。不要写 "in our previous work (X, 2024) we showed"。
- 不要对参考文献列表中的条目进行匿名化，除非是你自己未发表的工作（例如，正在其他地方审稿的），这时作为匿名引用并上传匿名补充材料。
- 与自己之前的工作有实质性重叠的必须引用（匿名地）并解释差异。
- 允许 arXiv 预印本，但投稿不能引用非匿名版本，且在审稿期间不得宣传该工作是 ICML 投稿。
- Rebuttal 文本也必须匿名（见 §6）。

## 3. 必需与可选章节

- **影响声明（主轨必需）：** 位于论文末尾的无编号章节，与致谢并列，在参考文献之前；不计入页数限制。当影响是推进 ML 的常规影响时，可以逐字使用以下句子：
  > "This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here."

  作者被鼓励在必要时多说一些；如果论文被标记为伦理审稿，该声明会被阅读。
- **致谢：** 仅限定稿版。
- **局限性：** ICML 不强制要求该章节，但审稿人被指示奖励而非惩罚对局限性的诚实讨论。建议包含一节。
- **立场论文轨道（独立轨道）：** 标题必须表明立场；摘要说明立场（"This position paper argues that ..."）；引言中用粗体标明立场；主文中必须包含 **Alternative Views** 章节；不需要影响声明。

## 4. 补充材料

- 文本附录放在主 PDF 中（不限页数）。审稿人没有义务阅读附录或补充材料：任何关键内容必须在 8 页内。
- 代码/数据：zip 或 PDF 上传，匿名化（移除姓名和许可证），或截稿后冻结分支的匿名 GitHub 仓库（链接放在 zip 内的一个文本文件中）。
- 鼓励提交代码；可重复性会被纳入决策考量。
- 不接受任何定稿版补充材料。

## 5. 与 AI 辅助写作相关的政策

- LLM 可以协助写作和研究；**作者对所有内容负全责**，包括任何可能被认定为抄袭或不当行为的内容。作者被鼓励在研究方法论中说明 LLM 的显著使用方式。
- LLM 不能作为作者。
- **提示注入被禁止，会导致直接拒稿**（旨在操纵 LLM 审稿人的文本）。主办方运行检测器。2026 年 2 月的更新说明，仅用于*检测*审稿人 LLM 使用的提示不会被处罚——但本技能家族仍然从不插入任何隐藏或面向审稿人的文本。
- 审稿人被指示，提交低质量 AI 生成内容（"AI slop"）可能构成不当行为，可以被举报。
- 任何形式的抄袭均被禁止。切勿从其他论文复制句子。
- 禁止实质相似工作的一稿多投；有重叠作者的并发 ICML 投稿对彼此视为先前工作。

## 6. 审稿流程与作者回应（2026）

- 审稿表维度，每项 1–4 分：**严谨性（Soundness）、表达（Presentation）、重要性（Significance）、原创性（Originality）**。总体推荐 1–6 分（6 Strong Accept、5 Accept、4 Weak accept、3 Weak reject、2 Reject、1 Strong Reject）。置信度 1–5。
- 审稿人被指示：原创性不要求新方法（对现有方法的新洞察也算）；严谨性独立于影响力评估；应奖励诚实的局限性讨论。
- 审稿人给出 3–5 条编号的 "key questions"，其答案可能改变他们的评估。
- 同期工作：在全文截稿前不到两个月公开的工作视为同期；作者不需要讨论它们。
- **作者回应：** 三轮作者–审稿人讨论（作者 rebuttal、审稿人跟进、作者跟进），**每轮限制 5000 字符**。在 OpenReview 上核实该限制是按回复/线程还是总计。
- **回应期间不能上传修订版 PDF**。
- 回应必须匿名：无非匿名 URL、无个人网站 URL、无短链接（它们可以记录审稿人 IP）。审稿人不期望点击外部链接。
- 不需要回答每一个小问题。按审稿人 ID 组织。保持专业礼貌。
- 审稿人必须确认回应并撰写 rebuttal 后的 "Final Justification"，说明回应是否解决了他们的顾虑。
- **公开性：** 对于被接收的论文，原始投稿、匿名审稿意见、元审稿、rebuttal 和讨论将在 OpenReview 上公开。被拒论文可以选择公开。将每一次回应都当作会公开来写。

## 7. 定稿版（2026）

- 截稿（2026）：5 月 28 日，AoE 23:59。现场展示问卷截止 5 月 11 日。
- `\usepackage[accepted]{icml2026}`；主文 **9 页**，后跟致谢、影响声明、参考文献、附录。PDF ≤ 20 MB。US Letter。
- 作者块按 `example_paper.tex`；调用 `\printAffiliationsAndNotice{\icmlEqualContribution}` 或 `\printAffiliationsAndNotice{}`。Affiliations 必须与 OpenReview 个人资料匹配。
- 作者顺序可以更改；**不得增减**。必须与 OpenReview 一致。
- 标题和摘要只能小幅更改（重大标题更改需 PC 许可）。OpenReview 表单中输入的标题和摘要必须与 PDF 完全一致；谨慎使用 TeX 数学，不使用自定义宏，重音符号通过 TeX 命令输入。
- 相对于审稿版本，核心内容必须保持不变（原始投稿将一并发布）。
- **利益冲突披露（2026 年新增）：** 如果存在任何财务/实质性利益冲突（例如，评估作者雇主构建的模型），在引言**最后一段**添加标题为 "Conflict of Interest Disclosure" 的段落。如果没有冲突则完全省略。单纯的行业就业不构成冲突。
- 参考文献：正确的书目数据；尽可能用同行评审版本替换 arXiv 引用；修复 OpenReview 决定中 "Reference Correctness Check" 下所列项目；保护 BibTeX 中的大写。
- 代码/数据：放入公共存档仓库并在论文中链接；可选填写 OpenReview "code url" 框。
- **Lay summary**（通俗语言摘要）在 OpenReview 中输入。2026 年指南（与 2025 年相同）：最多 10 句 / 200 词；科学记者能理解；具体 enough 以至于无法描述任何其他 ICML 论文；将其视为论文的预告片。来源：https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- 运行 ICML 格式检查器（https://papercheck.icml.cc/papercheck.html）直到通过；将其返回的 5 位代码输入定稿表单。
- 表单：PMLR Publication Agreement（上传，≤10 MB）、ICML Publishing Release（由一名作者签署）、oral 演讲者的 Recording Release。
- 注册：至少一名作者必须注册（现场参会选 Conference；仅论文集选 Conference 或 Virtual Pass）。
- 无障碍性：色盲友好图表、最新的参考文献姓名和会场名称、包容性语言。
- 会后有修订窗口，允许在 PMLR 出版前进行小幅修正。

## 8. 关键 2026 日期（历史参考，用于定位）

摘要截稿 2026-01-23 AoE；全文 2026-01-28 AoE；审稿截止 3 月 12 日；作者–审稿人讨论 3 月 24 日 – 4 月 7 日；通知 4 月 30 日；定稿 5 月 28 日。截稿严格，不延期。作者名单在摘要截稿后不能更改。

---

## 如何为新周期刷新本文件

1. 如果你有网络访问权限，获取当年的 Author Instructions、Call for Papers、Reviewer Instructions 和示例论文（将上面 URL 中的 `2026` 替换为目标年份；如果页面 404，从 https://icml.cc 开始导航）。
2. 将上面每一行与它们进行对比。更新数值，在顶部注明新的快照日期和年份，并在 "Changelog" 下列出变更内容。
3. 将刷新后的副本写入项目工作区 `.icml/venue_facts.md`（技能在工作期间读取的是工作区副本）。
4. 如果你无法获取，明确告诉用户："使用 ICML 2026 规则（快照 2026-10-05）；请确认它们对你的目标年份仍然适用。" 不要静默假设。

## 变更日志
- 2026-10-05: 从 ICML 2026 官方页面提取的初始快照。
