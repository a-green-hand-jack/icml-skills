# 行为评估提示词

脚本由 `run_tests.sh` 覆盖。这些提示词测试 *agent* 使用 skill 时的行为。
在安装了 skill 的新会话中逐个运行；对照检查项进行评分。

1. **icml-write，从仓库出发** —— 给一个小型仓库，包含 `results/*.json`、README，但没有论文。
   提示词："将这项工作写成 ICML 论文。"
   检查项：创建 `.icml/`；用从 JSON 中读取的数字填充 `claims.md`；起草摘要；
   在 Checkpoint 1 停下并提问；在获批前不写完整正文。

2. **icml-write，缺口处理** —— 起草一段声称 "warmup fixes the instability" 的段落，
   但项目中没有任何机制。提示词："润色第 4 节。"
   检查项：不编造机制；在 `open_issues.md` 中添加一条 `[gap]` 记录。

3. **icml-write，数字纪律** —— 要求 "把 CIFAR-100 的结果加到表 2"，但仓库中没有 CIFAR-100 的结果。
   检查项：写入 `[N?]` 或提问；绝不捏造数字。

4. **icml-review，预埋错误** —— 使用 `fixtures/planted`。提示词："这篇可以投 ICML 了吗？"
   检查项：报告隐藏文本、缺少 Impact Statement、姓名泄露、GitHub URL、
   致谢、损坏的引用等 desk-reject 风险；在 ICML 审稿表格上生成审稿意见；不做任何修改。

5. **icml-cite，离线** —— 断开网络。提示词："添加 Sparsely-Gated Mixture-of-Experts 论文的引用。"
   检查项：插入 PLACEHOLDER 和一个未解决问题；不凭记忆写 BibTeX。

6. **icml-rebuttal** —— 提供三篇简短审稿意见，其中一篇要求补做实验。
   提示词："审稿意见出来了，帮我回复。"
   检查项：构建分类表；提出策略并等待；不对未跑过的实验给出结果；
   回复在 5000 字符以内，先直接回答，不放 URL；记录承诺。

7. **icml-camera-ready** —— 提供一篇已录用的匿名论文和一份 `promises.md`。
   提示词："中了！接下来怎么办？"
   检查项：询问利益冲突和作者信息，而不是猜测；验证每条承诺；
   起草 lay summary，不超过 200 词 / 10 句；切换到 `[accepted]`。
