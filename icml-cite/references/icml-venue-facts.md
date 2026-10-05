# ICML 会议事实（快照：ICML 2026）

**快照日期：** 2026-10-05。**适用对象：** ICML 2026（首尔，2026 年 7 月 6–11 日）。
此处的每个数字和政策都是年份专属的。在为新周期依赖它之前，
请先刷新（见底部 "How to refresh"）。当本文件与实时官方页面冲突时，
以实时页面为准。

构建本快照时参考的官方来源：
- 作者须知：https://icml.cc/Conferences/2026/AuthorInstructions
- 征稿启事：https://icml.cc/Conferences/2026/CallForPapers
- 审稿人须知：https://icml.cc/Conferences/2026/ReviewerInstructions
- 示例论文（PDF）：https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- 样式文件：https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. 格式（投稿）

| 项目 | 要求 |
|---|---|
| 正文 | **最多 8 页** — 超出即自动拒稿 |
| 参考文献、附录、Impact Statement | 页数不限，在同一单个 PDF 中 |
| 排版 | 仅限 LaTeX，官方 `icml2026.sty`，`\usepackage{icml2026}`（不加 `accepted` 选项） |
| 版式 | 双栏，US Letter（非 A4），10pt Times |
| 样式修改 | 禁止。不要改动模板或压缩纵向间距 |
| 投稿 PDF 大小 | 50 MB（作者须知页面）。示例论文仍写 10 MB；遵循作者须知页面并尽量保持小体积 |
| 摘要 | 一段，理想情况下 4–6 句。严重违规必须在 camera-ready 阶段修正 |
| 标题与各级标题 | 实词首字母大写，不要全部大写。最多三级标题 |
| 图 | 标题放在**下方**；图形内部不要放标题；标注坐标轴；每条曲线都要有图例；绘图使用矢量图（PDF/EPS） |
| 表 | 标题放在**上方** |
| 伪代码 | 使用 `algorithm` + `algorithmic` 环境（随样式文件提供） |
| 引用 | 通过 `natbib` + `icml2026.bst` 实现 APA 作者-年份。多篇引用按时间顺序排列。在 BibTeX 标题中保护大写字母：`{B}ayesian`、`{L}ipschitz` |
| 字体 | 示例论文要求 Type-1 字体；2026 camera-ready 说明不再检查 Type 3。使用 pdflatex 和矢量图；将 Type 3 视为警告 |

## 2. 匿名性（双盲）

- 不显示作者姓名或单位（除非使用 `accepted` 选项，否则样式会隐藏 `\icmlauthor`）。
- 不要致谢，不要写资助编号，不要链接到公开（非匿名）代码仓库。
- 以第三人称引用自己先前的工作。绝不要写 "in our previous work (X, 2024) we showed"。
- 不要对参考文献列表中的条目进行匿名化，未发表的自己工作除外（例如正在其他地方审稿），
  这类工作以匿名引用形式出现，并作为匿名补充材料上传。
- 与自己先前有实质性重叠的论文必须引用（匿名引用），并解释差异。
- 允许 arXiv 预印本，但投稿不得引用非匿名版本，且在审稿期间不得将该工作宣传为 ICML 投稿。
- Rebuttal 文本也必须匿名（见 §6）。

## 3. 必需与可选章节

- **Impact Statement（主赛道必需）：** 位于论文末尾、与 Acknowledgements 相邻、在 References 之前的无编号章节；不计入页数限制。当影响只是推进机器学习的常规影响时，以下句子可逐字使用：
  > "This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here."

  作者被鼓励在适当情况下补充更多内容；若论文被标记为伦理审查，该声明会被阅读。
- **Acknowledgements：** 仅限 camera-ready。
- **Limitations：** ICML 不强制要求该章节，但审稿人被要求奖励而非惩罚对局限性的诚实讨论。建议包含一个。
- **Position paper track（独立赛道）：** 标题必须表明立场；摘要中陈述立场（"This position paper argues that ..."）；引言中以粗体标明立场；正文中必须包含一个 **Alternative Views** 章节；不需要 Impact Statement。

## 4. 补充材料

- 文字附录放在主 PDF 中（页数不限）。审稿人没有被要求阅读附录或补充材料：任何关键内容必须在前 8 页内。
- 代码/数据：以 zip 或 PDF 上传，匿名化（删除姓名和许可证），或在截止日期后冻结分支的匿名 GitHub 仓库（链接放在 zip 内的文本文件中）。
- 鼓励提交代码；可重复性会被纳入录用决策考量。
- 任何类型的 camera-ready 补充材料均不接受。

## 5. 与 AI 辅助写作相关的政策

- LLM 可以协助写作和研究；**作者对所有内容承担全部责任**，包括任何可能被视为抄袭或学术不端的内容。鼓励作者在研究方法中描述使用 LLM 的显著方式。
- LLM 不能作为作者。
- **提示注入被禁止，一经发现直接 desk rejection**（旨在操纵 LLM 审稿人的文本）。组织者会运行检测器。2026 年 2 月的更新指出，仅旨在*检测*审稿人是否使用 LLM 的提示不会被处罚——本 skill 系列仍然从不插入任何隐藏或面向审稿人的文本。
- 审稿人被提醒，提交低质量 AI 生成内容（"AI slop"）可能构成学术不端，可被举报。
- 任何形式的抄袭均被禁止。绝不要从其他论文中复制句子。
- 实质性相似工作的双重投稿被禁止；有重叠作者的同期 ICML 投稿彼此之间被视为已有工作。

## 6. 审稿流程与作者回应（2026）

- 审稿表单维度，每项 1–4 分：**Soundness、Presentation、Significance、Originality**。总体推荐 1–6 分（6 强接收，5 接收，4 弱接收，3 弱拒稿，2 拒稿，1 强拒稿）。置信度 1–5。
- 审稿人被要求：originality 不要求提出新方法（对现有方法的新见解也算）；soundness 与 impact 分开评估；应奖励诚实的局限性讨论。
- 审稿人给出 3–5 条编号的 "key questions"，其答案可能改变他们的评价。
- 同期工作：在全文投稿截止日期前不到两个月公开的工作视为同期工作；作者无需讨论它们。
- **作者回应：** 三轮作者-审稿人讨论（作者 rebuttal、审稿人 follow-up、作者 follow-up），**每轮限 5000 字符**。请在 OpenReview 上确认该限制是按回复/线程计算还是总计。
- 回应期间**不得上传修订版 PDF**。
- 回应必须匿名：不要出现非匿名 URL、不要出现个人网站 URL、不要出现短链接（它们可能记录审稿人 IP）。审稿人不被要求点击外部链接。
- 无需回答每一个细枝末节。按审稿人 ID 组织。保持专业与礼貌。
- 审稿人必须确认回应，并撰写 rebuttal 后的 "Final Justification"，说明 rebuttal 是否解决了他们的顾虑。
- **公开性：** 对于录用论文，原始投稿、匿名审稿、meta-reviews、rebuttal 和讨论将在 OpenReview 上公开。被拒论文可选择公开。将每一次回应都当作会被公开来撰写。

## 7. Camera-ready（2026）

- 截止日期（2026）：5 月 28 日，AoE 23:59。现场展示问卷截止 5 月 11 日。
- `\usepackage[accepted]{icml2026}`；正文**9 页**，随后是 Acknowledgements、Impact Statement、References、Appendices。PDF ≤ 20 MB。US Letter。
- 作者块按 `example_paper.tex` 格式；调用 `\printAffiliationsAndNotice{\icmlEqualContribution}` 或 `\printAffiliationsAndNotice{}`。单位必须与 OpenReview 个人资料一致。
- 作者顺序可以变更；**不得增加或删除**。必须与 OpenReview 一致。
- 标题和摘要只能微调（显著修改标题需 PC 批准）。OpenReview 表单中填写的标题和摘要必须与 PDF 完全一致；TeX 数学公式尽量少用，不要自定义宏，重音符号通过 TeX 命令输入。
- 相对于审稿版本，核心内容必须保持不变（原始投稿会一并发布）。
- **Conflict of Interest Disclosure（2026 年新增）：** 如果存在任何财务/实质性利益冲突（例如，评估某位作者雇主构建的模型），请在引言的**最后一段**添加一个标题为 "Conflict of Interest Disclosure" 的段落。如果没有冲突，则完全省略。单纯的行业雇佣关系不构成冲突。
- 参考文献：正确的书目数据；尽可能将 arXiv 引用替换为正式发表版本；修复 OpenReview 决定中 "Reference Correctness Check" 列出的每一项；在 BibTeX 中保护大写字母。
- 代码/数据：放入公开的归档仓库并在论文中链接；可选择填写 OpenReview 的 "code url" 框。
- **Lay summary**（通俗语言摘要）在 OpenReview 中填写。2026 年指南（与 2025 年相同）：最多 10 句 / 200 词；能被科学记者理解；具体到你认为无法描述任何其他 ICML 论文的程度；把它当作论文的预告片。来源：https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- 运行 ICML 格式检查器（https://papercheck.icml.cc/papercheck.html）直到通过；将返回的 5 位代码填入 camera-ready 表单。
- 表单：PMLR 出版协议（上传，≤10 MB）、ICML 出版发布（由一名作者签署）、口头报告录制发布（口头报告者）。
- 注册：至少一名作者必须注册（现场参会选 Conference 选项；仅论文选 Conference 或 Virtual Pass）。
- 可访问性：色盲友好图形、最新的参考文献作者名与会议名、包容性语言。
- 会议后有一个修订窗口，可在 PMLR 出版前进行小幅修正。

## 8. 关键 2026 日期（供参考的历史日期）

摘要截止 2026 年 1 月 23 日 AoE；全文截止 1 月 28 日 AoE；审稿截止 3 月 12 日；
作者-审稿人讨论 3 月 24 日 – 4 月 7 日；录用通知 4 月 30 日；camera-ready 5 月 28 日。
截止日期严格，不延期。摘要截止后作者名单不可变更。

---

## 如何为新周期刷新本文件

1. 如果你有网络访问，获取当前年份的作者须知、征稿启事、审稿人须知和示例论文（将上方 URL 中的 `2026` 替换为目标年份；若页面 404，请从 https://icml.cc 开始导航）。
2. 将上方每一行与它们进行比对。更新数值，在顶部注明新的快照日期和年份，
   并在 "Changelog" 下列出变更内容。
3. 将刷新后的副本写入项目工作区 `.icml/venue_facts.md`（技能在工作期间读取的是工作区副本）。
4. 如果你无法获取，请明确告知用户："使用 ICML 2026 规则（快照 2026-10-05）；
   请确认它们对你的目标年份仍然适用。" 不要静默假设。

## Changelog
- 2026-10-05: 根据 ICML 2026 官方页面创建初始快照。
