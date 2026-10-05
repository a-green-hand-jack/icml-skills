# ICML Venue Facts（ICML 会场事实）（snapshot: ICML 2026）

**Snapshot date:** 2026-10-05. **Applies to:** ICML 2026（首尔，2026 年 7 月 6–11 日）。
此处的每个数字和政策都是年度特定的。在新的周期依赖它之前，
请刷新它（见底部"How to refresh"）。当本文件与实时官方页面不一致时，
以实时页面为准。

构建本快照时参考的官方来源：
- Author Instructions: https://icml.cc/Conferences/2026/AuthorInstructions
- Call for Papers: https://icml.cc/Conferences/2026/CallForPapers
- Reviewer Instructions: https://icml.cc/Conferences/2026/ReviewerInstructions
- Example paper (PDF): https://media.icml.cc/Conferences/ICML2026/Styles/example_paper.pdf
- Style files: https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip

---

## 1. Format（格式）（submission）

| Item | Requirement |
|---|---|
| Main body | **最多 8 页** — 超出将自动拒稿 |
| References, appendices, Impact Statement | 不限页数，同一 PDF |
| Typesetting | 仅限 LaTeX，官方 `icml2026.sty`，`\usepackage{icml2026}`（不使用 `accepted` 选项） |
| Layout | 双栏，US Letter（非 A4），10pt Times |
| Style changes | 禁止。不得改动模板或压缩垂直间距 |
| Submission PDF size | 50 MB（Author Instructions 页面）。示例论文仍写 10 MB；遵循 Author Instructions 页面并尽量保持小巧 |
| Abstract | 一段，理想 4–6 句。严重违规必须在 camera-ready 阶段修正 |
| Title and headings | 实词首字母大写，禁止全大写。最多三级标题 |
| Figures | Caption **在下方**；图形内部不得有标题；标注坐标轴；每条曲线需有图例；绘图使用矢量格式（PDF/EPS） |
| Tables | Caption **在上方** |
| Pseudocode | `algorithm` + `algorithmic` 环境（随样式文件提供） |
| Citations | 通过 `natbib` + `icml2026.bst` 使用 APA author–year 格式。多条引用按时间顺序排列。在 BibTeX 标题中保护大写：`{B}ayesian`、`{L}ipschitz` |
| Fonts | 示例论文要求 Type-1 字体；2026 camera-ready 说明不再检查 Type 3。使用 pdflatex 和矢量图；将 Type 3 视为警告 |

## 2. Anonymity（匿名性）（double-blind）

- 不显示作者姓名或单位（样式会在未使用 `accepted` 时隐藏 `\icmlauthor`）。
- 不得出现 acknowledgements、资助编号或指向公开（非匿名）代码仓库的链接。
- 用第三人称引用自己先前的工作。禁止写 "in our previous work (X, 2024) we showed"。
- 不要对参考文献列表中的条目进行匿名化，除非是自己的未发表工作（例如正在别处审稿），此时以匿名引用形式列出，并作为匿名 Supplementary Material 上传。
- 与自己先前有实质性重叠的论文必须（匿名地）引用，并解释差异。
- arXiv preprints 允许，但投稿不得引用非匿名版本，且不得在审稿期间将该工作宣传为 ICML 投稿。
- Rebuttal 文本也必须匿名（见 §6）。

## 3. Required and optional sections（必需与可选章节）

- **Impact Statement（主赛道必需）：** 放在论文末尾的 unnumbered section，与 Acknowledgements 放在一起，位于 References 之前；不计入页数限制。当影响仅限于推动机器学习领域发展的常规影响时，可以逐字使用以下句子：
  > "This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here."

  作者被鼓励在有必要时写更多；如果论文被标记为 ethics review，该声明会被阅读。
- **Acknowledgements：** 仅限 camera-ready。
- **Limitations：** ICML 不强制要求该章节，但审稿人被要求奖励（而非惩罚）对局限性的诚实讨论。建议包含。
- **Position paper track（独立赛道）：** 标题必须表明立场；摘要中声明立场（"This position paper argues that ..."）；引言中以粗体表明立场；正文中必须包含 **Alternative Views** 章节；不需要 Impact Statement。

## 4. Supplementary material（补充材料）

- Text appendices 放在主 PDF 中（不限页数）。审稿人不强制阅读 appendices 或 supplementary material：任何关键内容必须在前 8 页中。
- Code/data：zip 或 PDF 上传，匿名化（移除姓名和许可证），或在截稿后冻结分支的匿名 GitHub 仓库（在 zip 内的文本文件中提供链接）。
- 鼓励提交代码；可重复性会被纳入决定考量。
- Camera-ready 阶段不允许任何 supplementary material。

## 5. Policies relevant to AI-assisted writing（与 AI 辅助写作相关的政策）

- LLM 可以协助写作和研究；**作者对所有内容负全部责任**，包括任何可能被认定为抄袭或不当行为的内容。鼓励作者在研究方法论中描述使用 LLM 的显著方式。
- LLM 不能作为作者。
- **Prompt injection 被禁止，会导致 desk rejection**（旨在操纵 LLM 审稿人的文本）。组织者会运行检测器。2026 年 2 月的更新说明，仅用于*检测*审稿人是否使用 LLM 的 prompts 不会被处罚——但本技能家族仍然不会在文本中插入任何隐藏或面向审稿人的内容。
- 审稿人被提醒，提交低质量 AI 生成内容（"AI slop"）可能构成不当行为，可以被举报。
- 任何形式的抄袭均被禁止。禁止从其他论文复制句子。
- 禁止实质性相似工作的 dual submission；有重叠作者的同期 ICML 投稿彼此视为 prior work。

## 6. Review process and author response（审稿流程与作者回复）（2026）

- Review form dimensions，每项 1–4 分：**Soundness, Presentation, Significance, Originality**。Overall recommendation 1–6（6 Strong Accept，5 Accept，4 Weak accept，3 Weak reject，2 Reject，1 Strong Reject）。Confidence 1–5。
- 审稿人须知：originality 不要求提出新方法（对现有方法的新见解也算）；soundness 与 impact 分开评估；应奖励对局限性的诚实讨论。
- 审稿人给出 3–5 条编号的 "key questions"，其答案可能改变他们的评价。
- Concurrent work：在全文截稿前不到两个月公开的工作视为 concurrent；作者无需讨论它们。
- **Author response：** 三轮作者–审稿人讨论（作者 rebuttal、审稿人跟进、作者跟进），**每轮限制 5000 字符**。在 OpenReview 上核实限制是按 reply/thread 计算还是总计。
- **回复期间不得上传修改后的 PDF**。
- 回复必须匿名：不得出现非匿名 URL、个人主页 URL、缩短 URL（它们可能记录审稿人 IP）。审稿人不被要求访问外部链接。
- 无需回答每个细枝末节。按审稿人 ID 组织。保持专业与礼貌。
- 审稿人必须确认回复并撰写 post-rebuttal "Final Justification"，说明 rebuttal 是否回应了他们的关切。
- **Publicity：** 对于被接收的论文，原始投稿、匿名审稿意见、meta-reviews、rebuttal 和讨论将在 OpenReview 上公开。被拒论文可选择加入。将每条回复当作会被公众阅读来写。

## 7. Camera-ready（2026）

- Deadline（2026）：5 月 28 日，AoE 时间 23:59。In-person presentation questionnaire 截止 5 月 11 日。
- `\usepackage[accepted]{icml2026}`；正文 **9 页**，随后是 Acknowledgements、Impact Statement、References、Appendices。PDF ≤ 20 MB。US Letter。
- Author block 按 `example_paper.tex`；调用 `\printAffiliationsAndNotice{\icmlEqualContribution}` 或 `\printAffiliationsAndNotice{}`。Affiliations 必须与 OpenReview profiles 一致。
- 作者顺序可以调整；**不得增删作者**。必须与 OpenReview 一致。
- 标题和摘要只能微调（大幅修改标题需 PC 批准）。OpenReview 表单中输入的标题和摘要必须与 PDF 完全一致；TeX 数学公式允许少量使用，禁止自定义宏，重音符号通过 TeX 命令输入。
- 核心内容相对于审稿版本必须保持不变（原始投稿会一并发布）。
- **Conflict of Interest Disclosure（2026 年新增）：** 如果存在任何财务/实质性利益冲突（例如，评估作者雇主构建的模型），在引言**最后一段**添加标题为 "Conflict of Interest Disclosure" 的段落。若不存在冲突则完全省略。单纯的行业就业不构成利益冲突。
- References：修正书目数据；尽可能用同行评审版本替换 arXiv 引用；修正 OpenReview 决定中 "Reference Correctness Check" 下列出的条目；在 BibTeX 中保护大写。
- Code/data：放入公共存档仓库并在论文中链接；可选填写 OpenReview "code url" 框。
- **Lay summary**（plain-language summary）在 OpenReview 中填写。2026 年指导（与 2025 年相同）：最多 10 句 / 200 词；科学记者能看懂；具体到你认为无法描述任何其他 ICML 论文的程度；将其视为论文的 trailer。Source: https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/
- 运行 ICML 格式检查器（https://papercheck.icml.cc/papercheck.html）直至无警告；在 camera-ready 表单中输入其返回的 5 位代码。
- Forms：PMLR Publication Agreement（上传，≤10 MB）、ICML Publishing Release（由一位作者签署）、Recording Release for oral presenters。
- Registration：至少一位作者必须注册（线下参会选 Conference 选项；仅 proceedings 选 Conference 或 Virtual Pass）。
- Accessibility：色盲友好图表、最新的文献作者与会议名称、包容性语言。
- A post-conference revision window 允许在 PMLR 出版前进行小的修改。

## 8. Key 2026 dates（关键日期）（historical, for orientation）

摘要截稿 2026 年 1 月 23 日 AoE；全文截稿 1 月 28 日 AoE；审稿意见截止 3 月 12 日；作者–审稿人讨论 3 月 24 日 – 4 月 7 日；通知 4 月 30 日；camera-ready 5 月 28 日。截稿严格，不延期。作者名单在摘要截稿后不得更改。

---

## How to refresh this file for a new cycle（如何为新的周期刷新本文件）

1. 如果你有网络访问，获取当前年度的 Author Instructions、Call for Papers、Reviewer Instructions 和 example paper（将上述 URL 中的 `2026` 替换为目标年份；如果页面 404，从 https://icml.cc 开始导航）。
2. 将上述每一行与它们进行比对。更新数值，在顶部注明新的 snapshot date 和 year，并在 "Changelog" 下列出变更内容。
3. 将刷新后的副本写入项目工作区，作为 `.icml/venue_facts.md`（技能在工作期间读取的是工作区副本）。
4. 如果你无法获取，请明确告诉用户："当前使用 ICML 2026 规则（snapshot 2026-10-05）；请确认它们对你的目标年份仍然适用。"不要默默假设。

## Changelog
- 2026-10-05：根据 ICML 2026 官方页面创建初始快照。
