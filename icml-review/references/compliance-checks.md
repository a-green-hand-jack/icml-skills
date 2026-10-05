# 合规性检查：含义、修复方法与人工检查项

`check_submission.py` 的代码及其含义。脚本中的严重级别是默认值；
人工可以用理由豁免一个 WARN（记录在 `decisions.md` 中）。

| Code | 含义 | 修复方法 |
|---|---|---|
| STYLE-MISSING / STYLE-ACCEPTED-IN-SUBMISSION / STYLE-NOT-ACCEPTED | ICML 样式包使用错误 | 投稿用 `\usepackage{icml20XX}`，定稿版用 `[accepted]` |
| PAPER-A4, PDF-PAGESIZE | 不是 US Letter | 移除 a4paper；重新编译 |
| LAYOUT-HACK | 模板间距/布局被修改 | 移除；改为删减文字。修改模板是拒稿理由 |
| HIDDEN-TEXT, INJECTION-PHRASE | 不可见或面向审稿人/LLM 的文本 | 彻底移除。提示注入 = 直接拒稿 |
| PLACEHOLDER | 残留 TODO/TBD/占位引用 | 解决或移除 |
| ABSTRACT-PARAGRAPHS / ABSTRACT-SENTENCES | 摘要不是一段 / 不是约 4–6 句 | 合并；精简 |
| TITLE-ALLCAPS / TITLE-CASE | 标题大小写 | 仅大写实词 |
| IMPACT-MISSING / IMPACT-AFTER-REFS / IMPACT-IN-APPENDIX / IMPACT-NUMBERED | 影响声明缺失或位置错误 | 在参考文献前使用无编号的 `\section*{Impact Statement}` |
| POSITION-ALT-VIEWS | 立场论文轨道缺少 "Alternative Views" | 在主文中添加该节 |
| ACK-IN-SUBMISSION | 匿名版本中出现致谢 | 定稿前移除 |
| ANON-NAME / ANON-PDF-NAME | 文本中出现作者/单位字符串 | 移除或改写；第三方引用条目中的命中是可接受的 |
| ANON-SELFREF | "our previous work" 式自引 | 改用第三人称重写 |
| ANON-URL | 非匿名 URL（GitHub、个人主页、短链接） | 替换为匿名仓库（如 anonymous.4open.science）或补充材料上传 |
| ANON-FUNDING | 资助/经费文本 | 定稿前移除 |
| ANON-PDFMETA | PDF 元数据中的作者 | 移除 `pdfauthor`，清空元数据；也检查图表 PDF |
| ANON-HEADER | 首页未显示匿名作者块 | 检查样式选项和 `\icmlauthor` 用法 |
| BIB-MISSING / BIBSTYLE | 参考文献缺失或样式错误 | `\bibliographystyle{icml20XX}` + natbib |
| CAPTION-FIG-POSITION / CAPTION-TAB-POSITION | 标题位置 | 图：标题在下。表：标题在上 |
| STY-MODIFIED | 样式文件与官方版本不同 | 恢复官方文件 |
| PDF-PAGE-LIMIT | 主文超过页数限制（启发式） | 目视确认；删减 |
| PDF-BROKEN-REF / PDF-BROKEN-CITE | `??` 或 `(?)` | 修复标签/key；重新运行 bibtex 和 latex 两次 |
| PDF-SIZE | 超过文件大小限制 | 压缩栅格图像；优先使用矢量图 |
| PDF-TYPE3 / PDF-UNEMBEDDED | 字体问题 | 使用 pdflatex；将图表导出为嵌入字体的 PDF |
| CR-* | 定稿版特有 | 见 icml-camera-ready |

## 脚本无法完成的人工检查项

匿名性
- 打开每个图表文件：坐标轴标签、水印、文件路径、用户名、机构
  logo、作者实验室独有的数据集名称、显示姓名的截图。
- 图表和图像文件元数据（PDF Author/Creator、PNG/JPG 的 EXIF）。
- 补充代码：页眉中的作者姓名、LICENSE 文件、`.git` 目录、
  绝对路径（`/home/<user>/`）、集群或存储桶名称、wandb/HF 用户名、
  显示路径的 notebook 输出。匿名 GitHub 链接必须位于 zip 内的一个文本文件中，
  且所在分支在截稿后冻结。
- 自引用以第三人称撰写，且不会 suspiciously 过度出现。
- 任何链接材料中都没有提及该论文是 ICML 投稿。

内容
- 审稿人评判正确性所需的一切都在前 8 页内。
- OpenReview 摘要和标题与 PDF 一致。
- 如果工作存在特定风险，影响声明不应只是套话。
- 研究方法论中显著使用了 LLM 的应予以说明（ICML 鼓励这样做）。
- 一稿多投：没有实质相似的版本正在其他地方审稿。

格式
- 页边距内没有文字；没有宽内容溢出栏外（检查公式和表格）。
- 图表在打印尺寸和灰度模式下清晰可读。
- 标题最多三级；标题首字母大写。
