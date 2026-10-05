# Camera-Ready 检查清单（ICML 2026 基准版本 — 请针对当年进行核实）

复制到 `.icml/camera_ready.md` 中，并在逐项核实后打勾（不是在"大概完成了"时打勾）。

## 时间线
- [ ] 已记录 camera-ready 截止日期和 AoE 时间（2026年：5月28日，11:59pm AoE）
- [ ] 已提交线下演讲问卷（2026年：5月11日前）— 作者
- [ ] 至少有一名作者完成注册（线下参会选择 Conference 选项；仅发表论文选择 Conference 或 Virtual Pass）— 作者

## 内容
- [ ] `promises.md` 中的每一项都在论文中，且与 rebuttal 完全一致
- [ ] 正文 ≤ 9 页；额外空间用于回应审稿人反馈，而非提出新声明
- [ ] 核心内容与审稿版本相比未改变（对比 PDF/摘要）
- [ ] 利益冲突披露声明：已询问作者；如适用则作为引言最后一段添加；否则省略
- [ ] 影响声明（Impact Statement）已包含（主会论文），不编号，在参考文献之前
- [ ] 致谢已添加（不编号，在参考文献之前），措辞已获作者批准
- [ ] 局限性（Limitations）在修改后仍然准确

## 作者与首页信息
- [ ] `\usepackage[accepted]{icml20XX}`
- [ ] 姓名、顺序、单位与 OpenReview 个人资料匹配；无添加/删除
- [ ] 共同贡献标记和 `\printAffiliationsAndNotice{...}` 正确渲染
- [ ] 通讯作者及邮箱
- [ ] 短标题合适（如需使用 `\icmltitlerunning{}`）
- [ ] 标题更改（如有）幅度小或已获 PCs 批准

## 参考文献
- [ ] OpenReview 决定中的 Reference Correctness Check 项已修复
- [ ] 在可能的情况下，arXiv 引用已替换为已发表版本
- [ ] 大小写已保护；姓名和会议名称已更新；无重复
- [ ] 无 `??` / `(?)`

## 格式
- [ ] US Letter；官方样式未修改；无间距hack
- [ ] PDF ≤ 20 MB；附录包含在同一 PDF 中（无 camera-ready 补充材料）
- [ ] 标题/标题：实词首字母大写，非全大写
- [ ] 摘要：一个段落，约 4–6 句话
- [ ] 引文字号等于正文字号
- [ ] 图表使用矢量图；配色可访问；语言具有包容性
- [ ] `check_submission.py --mode camera-ready` 无 ERROR
- [ ] ICML 论文检查器已通过；已记录 5 位字母代码 — 作者

## 代码和数据
- [ ] 公开存档仓库；链接在论文中；OpenReview 的 "code url" 字段已填写
- [ ] 仓库已清理（无 `.icml/` 笔记、密钥、内部路径）；含许可证；含 README

## OpenReview 表格 — 作者提交
- [ ] 标题和摘要文本与 PDF 完全一致（无自定义宏；TeX 重音符号）
- [ ] Lay summary（2026年：≤ 10 句话 / 200 词）
- [ ] 已上传 camera-ready PDF
- [ ] PMLR 出版协议已由通讯作者签署并上传（≤ 10 MB）
- [ ] ICML 出版许可已签署（一名作者）；oral 演讲者签署录制许可
