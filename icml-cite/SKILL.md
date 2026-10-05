---
name: icml-cite
description: 为 ICML 论文查找、验证和管理参考文献，避免虚构引用。搜索 DBLP、Semantic Scholar、arXiv 和 Crossref，以编程方式获取 BibTeX，将 arXiv 条目升级为其正式发表版本，对照 LaTeX 源文件检查 .bib（缺失的 key、重复项、未保护的大写字母、不完整字段），并保留验证日志。当 ICML 论文需要引用、相关工作参考文献、BibTeX 条目、文献清理、确认引用的论文是否存在或是否如文中所述、ICML 的 APA/natbib 引用格式、匿名自引，或 camera-ready 阶段的 Reference Correctness Check 修复时，请使用该 skill——即使用户只说“给这加个引用”或“清理我的 bib”。绝不要凭记忆编写 BibTeX。
compatibility: Python 3 标准库。查找需要联网访问 dblp.org、api.semanticscholar.org、export.arxiv.org 和 doi.org；若无法联网，该 skill 会将引用标记为占位符。
---

# ICML 引用

语言模型会记错参考文献：错误的作者、错误的年份、错误的会议，以及根本不存在的论文。提交中的虚构或错误引用属于学术不端行为，且 ICML 现已在 camera-ready 阶段运行自动参考文献检查器。本 skill 使每条引用都可追溯到数据库记录。

使用用户的语言与其交流。本 skill 与其同级 skill 共享 `.icml/` 工作区；首先运行 `python scripts/init_workspace.py --root <latex-root> --skill icml-cite`，格式说明见 `references/workspace-contract.md`。

## 原则

**绝不要凭记忆编写或编辑 BibTeX 条目。** 每条条目必须来自数据库响应（DBLP、Crossref 通过 DOI、arXiv、Semantic Scholar）或用户提供的文件。如果无法获取，插入一个显眼的占位符并告知用户：

```latex
\citep{PLACEHOLDER_sparse_moe_routing}  % UNVERIFIED: need a source for "router collapse"
```

并将 `[cite]` 项添加到 `.icml/open_issues.md` 中。占位符是诚实的；一个看似合理但编造的引用则不是。

## 工作流程：添加引用

1. **明确你需要它支持什么。** 写下该引用支持的确切论断（"没有负载均衡时会出现路由崩溃"）。引用支持论断，而不是主题。
2. **搜索。** `python scripts/cite_lookup.py search "query terms" [--year-from 2020]` 会搜索 DBLP（最适合计算机科学会议，包括 ICML/PMLR、NeurIPS、ICLR 通过 OpenReview）和 Semantic Scholar。添加 `--source arxiv` 以搜索预印本。在断定一篇论文不存在之前，尝试多种措辞和作者名。
3. **确定正确的记录。** 匹配标题、第一作者和年份。当正式发表版本和 arXiv 版本同时存在时，优先选择前者（ICML 在 camera-ready 阶段要求这样做；Foerster：Google Scholar 通常默认显示 arXiv 版本）。注意 workshop 版本和同名后续论文。
4. **获取 BibTeX。** `python scripts/cite_lookup.py bibtex --dblp <key>` 或 `--doi <doi>` 或 `--arxiv <id>`。将结果原封不动地粘贴到 `.bib` 中，然后仅做以下编辑：将引用 key 设为项目约定格式、用花括号保护标题中的大写字母（`{B}ayesian`、`{MCMC}`、`{T}ransformer`）、删除样式不需要的字段（abstract、keywords）。绝不要手动修改作者、年份、会议或页码。
5. **核实论断。** 如果该论断很重要（它支持一个论点、一个基线数字或一个定义），通过查找结果输出或论文页面阅读摘要或相关章节，确认它确实如文中所述。如果无法访问，将该引用记录为 `existence-verified, claim-unverified` 并告知用户。
6. **记录**到 `.icml/citations_log.md`：key、状态（`verified` / `existence-only` / `placeholder`）、已检查的源、是否存在正式发表版本、备注。

## 工作流程：审计参考文献

运行 `python scripts/check_bib.py main.tex refs.bib`。它会报告：
- `.bib` 中缺失的被引用 key，以及未使用的条目，
- 重复条目（同一标题或同一 DOI/arXiv id 在不同 key 下），
- 条目缺失其类型所必需的字段，
- 仅 arXiv 或 CoRR 条目（可升级至正式发表版本的候选），
- BibTeX 会将其小写的标题大写字母（未保护的首字母缩写和专有名词），
- 仍然存在的占位符 key，
- 使用普通 `\cite`（ICML 使用 natbib：`\citet` 与 `\citep`）。

然后核实每个尚未在 `citations_log.md` 中的条目，优先核实支持摘要、引言和实验部分中论断的条目，以及每个基线。对于 arXiv 条目，运行 `python scripts/cite_lookup.py published "<title>"` 以查找正式发表版本。

## ICML 专属规则

详细说明见 `references/citation-rules.md`。要点：
- 通过 `natbib` 和 `\bibliographystyle{icml20XX}` 实现 APA 作者-年份格式。当作者作为句子的语法成分时，使用 `\citet{}`，否则使用 `\citep{}`；多个引用按时间顺序排列。
- 匿名提交：以第三人称引用自己已发表的工作，仿佛是由他人撰写的；不要在参考文献列表中对已发表的条目进行匿名化。自己未发表的工作（例如，正在其他地方审稿）以匿名方式引用，并作为匿名补充材料上传。
- 在截止日期前不到两个月公开的工作属于 ICML 的同期工作；引用它们是可选的。
- Camera-ready：尽可能将 arXiv 引用替换为正式发表版本；修复 OpenReview "Reference Correctness Check" 中的每一项；保持作者姓名最新。

## 相关工作支持

当 icml-write 请求相关工作时，为每个候选返回：已验证的 BibTeX、一句话说明该论文做什么（来自其摘要，用自己的话概括），以及它与项目的关系（同一问题 / 同一技术 / 基线候选）。按方法论脉络分组，使相关工作部分能够进行比较和对比，而不是罗列论文。标记任何适用于该问题设定的方法：icml-write 必须要么与其进行比较，要么说明为什么不适用。

## 离线时

如果查找失败（无网络），明确告知用户，保留已有的已验证条目，为新条目添加占位符，并列出它们。即使对于著名论文也不要"凭记忆补全"——著名论文正是自信地记错细节的地方（错误的年份、arXiv 版本与会议版本混淆）。

## 文件

- `scripts/cite_lookup.py` — 搜索 / bibtex / 正式发表版本查找（仅标准库）。
- `scripts/check_bib.py` — 对照 LaTeX 源文件进行参考文献审计。
- `scripts/init_workspace.py` — 创建共享的 `.icml/` 工作区。
- `references/citation-rules.md` — ICML 引用格式、匿名性、BibTeX 规范。
- `references/workspace-contract.md`、`references/icml-venue-facts.md` — 共享文件。
