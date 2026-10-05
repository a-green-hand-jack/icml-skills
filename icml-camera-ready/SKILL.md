---
name: icml-camera-ready
description: 将已接收的 ICML 论文转换为最终 camera-ready 版本并完成提交流程。正确处理去匿名化（使用 accepted 样式选项、作者信息块、致谢），利用额外的第九页回应审稿人反馈，检查 rebuttal 中做出的每一项承诺，按需添加利益冲突披露声明，升级参考文献并修复 OpenReview 的 Reference Correctness Check，撰写 lay summary，准备代码链接，并完成格式检查器、表格和 OpenReview 字段的填写。只要 ICML 论文已被接收（或用户提及 camera-ready、final version、PMLR、papercheck、lay summary、plain-language summary、de-anonymizing、post-conference revision），就使用此技能——即使他们只说 "we got in, what now?"。不适用于决策前的 rebuttal（使用 icml-rebuttal）或新草稿（使用 icml-write）。
compatibility: Python 3; pdflatex 编译; 可选 poppler-utils 进行 PDF 检查。上传、签署表格和注册由作者完成。
---

# ICML Camera-Ready

camera-ready 是世界读者将看到的版本，与原始投稿、审稿意见和讨论一起发表在 PMLR 上。这一事实带来两个后果：论文的核心内容必须与审稿人看到的保持一致，并且 rebuttal 中做出的每一项承诺现在都可以被公开验证。

使用用户的语言与他们交流。运行
`python scripts/init_workspace.py --root <latex-root> --skill icml-camera-ready`，阅读
`.icml/venue_facts.md` 第7节（针对当前年份刷新：camera-ready 规则每年变化）以及 `.icml/rebuttal/promises.md`（如果存在）。

## 基本规则

- **不要更改论文的核心内容**（声明、主要结果、方法）
  相对于审稿版本。改进、澄清、承诺的补充内容和修正都是可以的。如果作者想要进行实质性更改，请标记出来并让他们决定是否需要程序委员会主席（PC）批准。
- **作者列表：** 顺序可以更改，但不能添加或删除；必须与 OpenReview 匹配。
  除小幅编辑外的标题更改需要程序委员会主席许可。
- **不要编造数字或引用**（与 icml-write 和 icml-cite 的规则相同）。
- **作者自行处理账户**：上传、签署表格、注册、填写
  OpenReview。你负责准备所有材料并给出精确的操作说明。

## 工作流程

使用 `references/camera-ready-checklist.md` 在 `.icml/camera_ready.md` 中跟踪进度。

1. **截止日期。** 询问当年的 camera-ready 截止日期和相关日期（2026年：
   camera-ready 5月28日 AoE，演讲问卷 5月11日）。倒推安排；格式检查器和表格需要时间。
2. **承诺。** 对 `promises.md` 中的每一行，验证它是否在论文中（位置），
   并且与 rebuttal 中所说的完全一致（数字相同，来自台账）。报告任何缺失项。如果没有 promises 文件，则从已发布的 rebuttal 文本中重建一个。
3. **利用额外页面处理审稿人反馈。** 正文最多可扩展到 9 页。优先用于承诺项和最常见的审稿人困惑（对修改后的文本运行 icml-write 的段落和句子检查）。不要把它用于新的声明。
4. **去匿名化。** `\usepackage[accepted]{icml20XX}`；真实的 `\icmlauthor` 和
   `\icmlaffiliation` 条目与 OpenReview 个人资料匹配；共同第一作者标记；
   `\icmlcorrespondingauthor`；`\printAffiliationsAndNotice{}`（或带
   `{\icmlEqualContribution}`）；致谢（不编号，在参考文献之前；
   资助、拨款编号、计算资源提供方、协助人员）；仅在作者希望时恢复自我引用为第一人称；将匿名仓库链接替换为公开的存档仓库；移除 "Anonymous" 占位符。向作者询问准确的姓名、单位和资助文本；切勿猜测。
5. **利益冲突披露声明。** 直接向作者询问是否有任何作者存在财务或其他实质性利益冲突（例如，论文评估了某作者所在公司构建的模型）。如果有，在引言的最后一段起草标题为 "Conflict of Interest Disclosure" 的段落，写明作者姓名首字母、公司和模型。如果没有，则不包含任何内容。仅有行业雇佣关系不构成利益冲突。作者必须确认最终措辞。
6. **影响声明（Impact Statement）。** 仍然需要（主会论文）。根据审稿意见或伦理评论重新审视它。
7. **参考文献。** 如果已安装 icml-cite 的 `check_bib.py`，则运行它；否则手动检查条目。修复 OpenReview 在 "Reference Correctness Check" 下列出的每一项。在存在同行评审版本时，将 arXiv 引用替换为已发表版本。保护大小写；更新作者姓名和会议名称。
8. **Lay summary。** 使用 `references/lay-summary-guide.md` 起草；给作者两个版本；由他们选择和编辑。
9. **机械检查。**
   `python scripts/check_submission.py --tex main.tex --pdf main.pdf --mode camera-ready`
   然后干净地编译（没有 `??`），PDF ≤ 20 MB，US Letter，标题和标题大小写正确，
   摘要为一个约 4–6 句话的段落，矢量图，
   色觉无障碍友好的图表，如果源代码将被发布，则从中移除 TL;DR 和 TODO 注释。
10. **官方格式检查器。** 作者将 PDF 上传到 ICML 论文检查器
    （2026年：papercheck.icml.cc）并迭代直到通过；它会返回一个用于 OpenReview 表格的代码。修复它报告的所有问题；每次修复后重新运行第 9 步。
11. **OpenReview 表格。** 为以下内容准备精确文本：标题和摘要（与 PDF 完全一致；
    少用 TeX 数学公式，不使用自定义宏，重音符号用 TeX 命令），lay summary，
    代码 URL，作者顺序。列出要上传的文件（PDF、由通讯作者签署的 PMLR 出版协议）。提醒他们注意 ICML 出版许可（一名作者签署）、oral 演讲者的录制许可以及注册要求（参见 venue facts）。
12. **发布。** 如果代码/数据将公开：移除 `.icml/` 笔记、凭证、内部路径；
    添加许可证和 README；使链接可长期存档。与作者确认。

## 会议结束后

ICML 允许一个会后修订窗口进行小幅修正。使用相同的检查；不要更改核心内容。

## 文件

- `scripts/check_submission.py` — 合规性检查（`--mode camera-ready`）。
- `scripts/init_workspace.py` — 共享工作区。
- `references/camera-ready-checklist.md` — 完整检查清单（复制到 `.icml/camera_ready.md`）。
- `references/lay-summary-guide.md` — 如何撰写 lay summary。
- `references/icml-venue-facts.md`、`references/workspace-contract.md` — 共享文件。
