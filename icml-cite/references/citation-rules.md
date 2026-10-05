# ICML 论文引用规则

来源：ICML 2026 示例论文与作者须知；Foerster，《How to ML Paper》；
Lipton (2018)。年份专属细节见 `icml-venue-facts.md`。

## 格式
- 样式：APA 作者-年份。LaTeX：由 ICML 样式自动加载 `\usepackage{natbib}`；
  使用 `\bibliographystyle{icml2026}`（来自样式包的年份专属 `.bst`）。
- 文中："Samuel (1959) showed ..." → `\citet{samuel1959}`；"... checkers (Samuel,
  1959)" → `\citep{samuel1959}`。多篇：`\citep{a,b,c}` 按时间顺序排列。
- `\citep[e.g.,][]{key}`、`\citep[see][Sec.~3]{key}` 用于前置/后置注。
- 首字母缩写加引用："proximal policy optimization \citep[PPO;][]{schulman2017ppo}"
  或在文中引入首字母缩写后只引用一次。
- 三位及以上作者时，样式会自动生成 "et al."；不要手动在作者字段中输入它。
- 参考文献：无编号的一级标题（由样式处理），按字母顺序排列，完整（尽可能包含页码），一致，作者姓名保持最新。

## BibTeX 规范
- 保护标题中的大写字母：`{B}ayesian`、`{L}ipschitz`、`{MCMC}`、`{GPT}-4`、
  `{T}ransformers`。BibTeX 样式会将未保护的标题单词小写。
- 必需字段：`@inproceedings` author、title、booktitle、year（欢迎包含 pages、publisher）；
  `@article` author、title、journal、year（volume、number、pages）；
  `@misc`/arXiv：author、title、year，以及 eprint/archivePrefix 或 howpublished/url。
- 会议名称一致（统一使用 "Proceedings of the 41st International Conference on
  Machine Learning" 或 "International Conference on Machine Learning"，不要混用）。
- 同一作品只保留一个条目；同一论文不要出现重复的 key。
- 一旦使用，保持 key 稳定；绝不要在未征得合作者同意的情况下重命名他们所依赖的 key。
- 当正式发表版本存在时（会议/期刊），引用正式发表版本，而非 arXiv。

## 匿名性（投稿阶段）
- 自己先前的工作用第三人称："Doe et al. (2024) showed ..."，绝不要写 "our previous
  work showed"。
- 不要从参考文献列表中删除或匿名化自己已发表的论文。
- 投稿所依赖的、自己未发表的工作：以 "Anonymous (2026)" 或样式的匿名形式引用，
  并上传一份匿名副本作为补充材料。
- 不要致谢，不要写资助编号，不要链接到非匿名仓库。

## 引用什么与何时引用（Lipton、Foerster、ICML 审稿人须知）
- 对你自己的实验无法支持的每个论断都要引用；避免你无法引用的宽泛论断。
- 在论文中凡使用先前方法之处都要引用，不仅限于相关工作部分。
- 在相关之处慷慨引用——审稿人很可能就是相关工作的作者——但不要用不相关的工作充数。
- 正确归属功劳，包括已知某个想法的首次出现。
- 绝不要歪曲被引用论文的内容。如果你没有核对过，就不要用它支持特定论断。
- 同期工作（在截止日期前不到两个月公开）在 ICML 中是可选引用的。

## Camera-ready
- 尽可能将 arXiv 替换为正式发表版本。
- 逐项处理 OpenReview 的 "Reference Correctness Check"，对照数据库记录确认每一项。
- 检查编译后的参考文献列表中的大小写。
- 如果承诺过，添加公开代码/数据 URL。
