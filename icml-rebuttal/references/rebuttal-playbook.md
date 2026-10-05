# Rebuttal Playbook（回复手册）

Main source: Devi Parikh, Dhruv Batra & Stefan Lee, "How we write rebuttals" (2020).
Additional points from Aaditya Ramdas's rebuttal checklist and ICML 2026 rules.
Paraphrased; examples written for this skill.

## Contents（目录）
1. Audiences and goals（受众与目标）
2. Triage table format（分类表格式）
3. Ordering and structure（排序与结构）
4. Response patterns（by comment type）（回复模式，按评论类型）
5. Tone and phrasing（语气与措辞）
6. Pitfalls（常见陷阱）
7. Promises file（承诺文件）

## 1. Audiences and goals（受众与目标）

- Reviewers：澄清疑问、回答问题、纠正误解、反驳误读，并展示善意利用反馈的努力。
- AC：展示善意、对审稿意见给出公正总结、让哪些关切已解决一目了然，并帮助他们做决定。Newcomers 往往只写给 reviewers 看；AC 更重要（辩论类比：你主要说服的是 judges，而非对手——而且 reviewers 是同事，不是对手）。

## 2. Triage table format（`.icml/rebuttal/triage.md`）（分类表格式）

```markdown
| ID | Quote (core) | Type | Severity | Shared with | Evidence / location | Plan | Status |
|----|--------------|------|----------|-------------|---------------------|------|--------|
| R1.1 | "No comparison to MoE-X" | missing baseline | major | R3.2 | Sec 2 excludes it w/o reason | run MoE-X (2 GPU-days) or explain inapplicability | decide |
```

Types: misunderstanding · already-in-paper · missing-experiment · missing-baseline ·
clarity · overclaim · related-work · reviewer-factual-error · minor · out-of-scope。
Severity = 对决定的影响程度，而非所需工作量。

Process（Parikh 等）：收到审稿意见后立即逐条列出（以便实验尽早启动）；对每条不加顾虑地快速写下可能的回应；起草完整回复；然后裁剪并排序以适应限制；最后重读审稿意见确保没有遗漏重要内容。

## 3. Ordering and structure（排序与结构）

- Start positive：总结审稿人认可的优点（rebuttals 大多关注负面；不要让 AC 忘记论文的优点）。
- Biggest concerns you can answer convincingly first；然后是证据不那么充分的；次要问题放在最后或批量处理（"We will fix all typos noted; thank you."）。
- Consolidate shared concerns：回答一次，在其他 threads 中引用。
- 如果多位审稿人遗漏了同一个 central point，先用简短清晰的回顾做铺垫。
- Keep each response self-contained：重新介绍缩写和相关设定。

## 4. Response patterns（回复模式）

Lead with the direct answer，then the support。对关键词使用 bold 或 capitalised emphasis 是可行的（Parikh 等）。

- **Yes/no factual question** → "**Yes.** All results average 5 seeds; Table 2 reports standard deviations."
- **Already in the paper** → "**This is in Sec. 4.2 (L310–318) and Table 3.** In short: <restate>." 引用表明论文并不欠缺；重述节省了 AC 翻查的时间。
- **Misunderstanding** → "**Not quite.** <correct statement>. We will rephrase L120 to prevent this reading: '<new sentence>'."（将其视为作者方的写作失误：Farquhar — 每一次误读都有文本上的原因。）
- **Missing experiment, run it** → "**We ran this.** <setup in one line>. <result with numbers>. <interpretation>. We will add it as Table X." 诚实包含负面结果。
- **Missing experiment, cannot run** → 保持透明：原因（算力、数据获取、时间、会场规则）、哪些证据部分回应了它、以及是否会在最终版本中补充。
- **Missing baseline that is not applicable** → "**<Method> is not applicable here because** <assumption it needs that our setting violates>. We will state this in Sec. 2."
- **Overclaim** → 让步并收窄："**We agree the phrasing is too strong.** We will revise to '<narrower claim>', which Table 2 supports." 在小点上让步能为大点建立可信度。
- **Premise is wrong** → "**We respectfully disagree with the premise.** <evidence>."
- **Related work missing** → 现在用两三句话给出实际比较（不要承诺，要落实），cite it，并说明会加入论文。
- **Reviewer factual error** → 用证据中立地纠正；绝不用 "the reviewer is wrong"。
- **Unhelpful or bad-faith review**（human decision）→ 实事求是：指出哪些 claims 缺乏支持，point to evidence and to other reviewers who disagree；考虑向 AC 提交 confidential comment。
- **Helpful extra effort**（typo lists、 pointers、detailed suggestions）→ 具体致谢。

Answer the intent："Why not dataset Z?" 可能实际上是在质疑评估的广度——先回答 Z，然后 remind them of the datasets already covered。

## 5. Tone and phrasing（语气与措辞）

- Conversational、concise、courteous。能同意时就同意；只在有证据时才反对。
  Ramdas 建议大多数条目以同意或部分同意结尾，真正的反对只保留给少数情况。
- Data over rhetoric：每当你要反对时，先问一个数字能否解决问题。
- Limited apology："Sorry for the confusion" 在论文确实不清楚的地方用一次；不要在每条 reply 里都道歉。
- Thank reviewers once，specifically；不要 flattery。
- 记住公开记录：把每句话都当作整个社区都会阅读来写。
- OpenReview 渲染 Markdown 和 LaTeX math；保持格式简洁并测试渲染效果。

## 6. Pitfalls（常见陷阱）

- Vague promises（"we will clarify"、"we will discuss"）没有实质内容。
- Burying the answer after paragraphs of context.
- Answering every minor point at length while the decisive concern gets two lines.
- Introducing new claims that the paper cannot support in its final version.
- Reporting experiment results that are not finished，或对结果进行 generous rounding。
- Links to non-anonymous resources；任何 identity hint。
- Exceeding the character limit（OpenReview 可能截断或拒稿）。
- Asking reviewers to raise scores。Let the evidence do it.
- Copying the reviewer's text at length（只引用核心部分）。

## 7. Promises file（`.icml/rebuttal/promises.md`）（承诺文件）

```markdown
| ID | Promised to | Promise | Exact text/result given in rebuttal | Paper location | Status |
|----|-------------|---------|-------------------------------------|----------------|--------|
| P1 | R1, R3 | Add MoE-X baseline | Table in R1 response (acc 81.2±0.3) | Table 2 | pending |
```

icml-camera-ready 在上传最终版本前会逐行核实。
