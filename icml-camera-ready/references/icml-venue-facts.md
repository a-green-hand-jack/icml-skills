# ICML 会议事实（快照：ICML 2026）

**快照日期：** 2026-10-05。**适用于：** ICML 2026（首尔，2026年7月6–11日）。
此处的每个数字和政策都是年份特定的。在为新周期依赖它之前，
请先刷新它（参见底部的 "How to refresh"）。当此文件与实时官方页面不一致时，
以官方页面为准。

此快照基于以下官方来源构建：
- 作者指南：https://icml.cc/Conferences/2026/AuthorInstructions
- 征稿启事：https://icml.cc/Conferences/2026/CallForPapers
- 审稿人指南：https://icml.cc/Conferences/2026/ReviewerInstructions
- 示例论文（PDF）：https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- 样式文件：https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. 格式（投稿阶段）

| 项目 | 要求 |
|---|---|
| 正文 | **最多 8 页** — 超出将被自动拒稿 |
| 参考文献、附录、影响声明 | 不限页数，在同一单个 PDF 中 |
| 排版 | 仅限 LaTeX，官方 `icml2026.sty`，`\usepackage{icml2026}`（不使用 `accepted` 选项） |
| 版式 | 双栏，US Letter（非 A4），10pt Times |
| 样式修改 | 禁止。不要修改模板或压缩垂直间距 |
| 投稿 PDF 大小 | 50 MB（作者指南页面）。示例论文仍写 10 MB；遵循作者指南并保持文件尽量小 |
| 摘要 | 一个段落，理想情况下 4–6 句话。严重违规必须在 camera-ready 阶段修复 |
| 标题和标题 | 实词首字母大写，从不全大写。最多三级标题 |
| 图表 | 图注在**下方**；图形内部无标题；标注坐标轴；每条曲线需图例；绘图使用矢量图（PDF/EPS） |
| 表格 | 表题在**上方** |
| 伪代码 | `algorithm` + `algorithmic` 环境（随样式文件提供） |
| 引用 | 通过 `natbib` + `icml2026.bst` 使用 APA 作者-年份格式。多篇引用按时间顺序排列。保护 BibTeX 标题中的大写：`{B}ayesian`，`{L}ipschitz` |
| 字体 | 示例论文要求 Type-1 字体；2026年 camera-ready 说明没有 Type 3 检查。使用 pdflatex 和矢量图；将 Type 3 视为警告 |

## 2. 匿名性（双盲）

- 不显示作者姓名或单位（样式会在没有 `accepted` 时隐藏 `\icmlauthor`）。
- 无致谢、拨款编号或指向公开（非匿名）代码仓库的链接。
- 以第三人称提及自己的先前工作。不要写 "in our previous work (X, 2024) we showed"。
- 不要对参考文献列表中的条目进行匿名化，除非是未发表的自己作品（例如，正在其他地方审稿的），此类作品作为匿名引用，并以匿名化形式作为补充材料上传。
- 与自己有实质性重叠的先前论文必须被引用（匿名地），并解释差异。
- arXiv 预印本允许，但投稿不得引用非匿名版本，且不得在审稿期间宣传该作品为 ICML 投稿。
- Rebuttal 文本也必须匿名（见 §6）。

## 3. 必需和可选章节

- **影响声明（Impact Statement，主会论文必需）：** 位于论文末尾的不编号章节，与致谢放在一起，在参考文献之前；不计入页数限制。当影响只是推进机器学习领域的常规影响时，可以逐字使用以下句子：
  > "This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here."

  鼓励作者在必要时写更多；如果论文被标记为伦理审查，该声明会被阅读。
- **致谢：** 仅在 camera-ready 阶段。
- **局限性（Limitations）：** ICML 不强制要求此章节，但审稿人被要求奖励而非惩罚对局限性的诚实讨论。请包含一个。
- **立场论文 track（独立 track）：** 标题必须表明立场；摘要陈述立场（"This position paper argues that ..."）；引言中以粗体标明立场；正文中强制包含 **Alternative Views** 章节；不需要影响声明。

## 4. 补充材料

- 文本附录放在主 PDF 中（不限页数）。审稿人没有义务阅读附录或补充材料：任何关键内容必须在 8 页之内。
- 代码/数据：zip 或 PDF 上传，匿名化（移除姓名和许可证），或一个在截止日期后冻结分支的匿名 GitHub 仓库（链接放在 zip 内的文本文件中）。
- 鼓励提交代码；可复现性会被纳入决策考量。
- 无任何形式的 camera-ready 补充材料。

## 5. 与 AI 辅助写作相关的政策

- LLM 可以辅助写作和研究；**作者对所有内容承担全部责任**，包括任何可能被视为抄袭或不当行为的内容。鼓励作者在研究方法论中描述使用 LLM 的显著方式。
- LLM 不能作为作者。
- **提示注入（prompt injection）被禁止并导致桌面拒稿**（为操纵 LLM 审稿人而设计的文本）。组织者运行检测器。2026年2月的更新表示，仅用于*检测*审稿人是否使用 LLM 的提示不会被处罚 — 本技能族仍然从不插入任何隐藏或面向审稿人的文本。
- 审稿人被提醒，提交低质量 AI 生成内容（"AI slop"）可能构成不当行为，可以被举报。
- 任何形式的抄袭均被禁止。不要从其他论文复制句子。
- 禁止实质性相似工作的双重投稿；作者重叠的同期 ICML 投稿被视为彼此的先前工作。

## 6. 审稿流程与作者回复（2026）

- 审稿表单维度，每项评分 1–4：**Soundness、Presentation、Significance、Originality**。总体推荐 1–6（6 强接收，5 接收，4 弱接收，3 弱拒稿，2 拒稿，1 强拒稿）。置信度 1–5。
- 审稿人被提醒：原创性不要求新方法（对现有方法的新见解也算）；soundness 与影响分开评估；应奖励诚实的局限性讨论。
- 审稿人给出 3–5 个编号"关键问题"，其答案可能改变他们的评估。
- 同期工作：在全文投稿截止日期前不到两个月公开的作品视为同期；作者无需讨论它们。
- **作者回复：** 三轮作者-审稿人讨论（作者 rebuttal、审稿人跟进、作者跟进），**每轮限制 5000 字符**。在 OpenReview 上核实限制是按回复/线程还是总计。
- **回复期间不能上传修订后的 PDF**。
- 回复必须匿名：无非匿名 URL、无个人网站 URL、无短链接（它们可能记录审稿人 IP）。审稿人不期望访问外部链接。
- 无需回答每一个小问题。按审稿人 ID 组织。保持专业和礼貌。
- 审稿人必须确认回复并撰写 rebuttal 后的 "Final Justification"，说明 rebuttal 是否解决了他们的顾虑。
- **公开性：** 对于接收的论文，原始投稿、匿名化审稿意见、meta-review、rebuttal 和讨论将发布在 OpenReview 上。被拒论文可选择加入。将每一次回复都当作会被公开一样来写。

## 7. Camera-ready（2026）

- 截止日期（2026年）：5月28日，11:59pm AoE。线下演讲问卷截止 5月11日。
- `\usepackage[accepted]{icml2026}`；正文 **9 页**，随后是致谢、影响声明、参考文献、附录。PDF ≤ 20 MB。US Letter。
- 作者信息块按照 `example_paper.tex`；调用 `\printAffiliationsAndNotice{\icmlEqualContribution}` 或 `\printAffiliationsAndNotice{}`。单位必须与 OpenReview 个人资料匹配。
- 作者顺序可以更改；**不能添加或删除**。必须与 OpenReview 匹配。
- 标题和摘要只能小幅更改（重大标题更改需要 PC 许可）。OpenReview 表格中输入的标题和摘要必须与 PDF 完全一致；允许少量 TeX 数学公式，不使用自定义宏，重音符号通过 TeX 命令输入。
- 核心内容必须相对于审稿版本保持不变（原始投稿将一并发布）。
- **利益冲突披露声明（2026年新增）：** 如果存在任何财务/实质性利益冲突（例如，评估某作者所在公司构建的模型），在引言的**最后一段**添加标题为 "Conflict of Interest Disclosure" 的段落。如果没有利益冲突，则完全省略。仅有行业雇佣关系不构成利益冲突。
- 参考文献：正确的书目数据；在可能的情况下将 arXiv 引用替换为已发表版本；修复 OpenReview 决定中 "Reference Correctness Check" 下列出的条目；保护 BibTeX 中的大小写。
- 代码/数据：放入公开存档仓库并在论文中链接；可选填写 OpenReview 的 "code url" 框。
- **Lay summary**（通俗语言摘要）在 OpenReview 中输入。2026年指南（与2025年相同）：最多 10 句话 / 200 词；科学记者应能理解；具体到你无法用它描述任何其他 ICML 论文的程度；将其视为论文的预告片。来源：https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- 运行 ICML 格式检查器（https://papercheck.icml.cc/papercheck.html）直到通过；将返回的 5 位字母代码填入 camera-ready 表格。
- 表格：PMLR 出版协议（上传，≤10 MB）、ICML 出版许可（一名作者签署）、oral 演讲者的录制许可。
- 注册：至少一名作者必须注册（线下参会选择 Conference 选项；仅发表论文选择 Conference 或 Virtual Pass）。
- 可访问性：色觉无障碍友好的图表、最新的书目姓名和会议名称、包容性语言。
- 允许一个会后修订窗口，在 PMLR 出版前进行小幅修正。

## 8. 2026 年关键日期（供参考）

摘要截止 2026年1月23日 AoE；全文截止 2026年1月28日 AoE；审稿截止 3月12日；作者-审稿人讨论 3月24日 – 4月7日；通知 4月30日；camera-ready 5月28日。截止日期严格，无延期。作者列表在摘要截止后不能更改。

---

## 如何为新的周期刷新此文件

1. 如果你有网络访问权限，获取当年的作者指南、征稿启事、审稿人指南和示例论文（将上面 URL 中的 `2026` 替换为目标年份；如果页面 404，从 https://icml.cc 开始导航）。
2. 将上面的每一行与它们进行对比。更新数值，在顶部注明新的快照日期和年份，并在 "Changelog" 下记录更改内容。
3. 将刷新后的副本作为 `.icml/venue_facts.md` 写入项目工作区（技能在工作期间读取的是工作区副本）。
4. 如果你无法获取，明确告诉用户："使用 ICML 2026 规则（快照 2026-10-05）；请确认它们对你的目标年份仍然适用。"不要静默假设。

## Changelog
- 2026-10-05: 从 ICML 2026 官方页面创建初始快照。
