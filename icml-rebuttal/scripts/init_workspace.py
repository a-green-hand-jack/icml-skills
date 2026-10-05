#!/usr/bin/env python3
"""在论文 LaTeX 根目录旁创建（或补全）.icml/ 工作区。

从不覆盖现有文件。在每个会话开始时安全运行。

用法：
    python init_workspace.py --root path/to/latex/root [--skill icml-write]
"""
import argparse
import datetime
import shutil
import sys
from pathlib import Path

TODAY = datetime.date.today().isoformat()

TEMPLATES = {
    "state.md": f"""# State
- Phase: setup
- Last action ({TODAY}, {{skill}}): 创建工作区
- Next step: 刷新 venue_facts.md 以匹配目标年份，然后开始任务
- Blocking: none
""",
    "claims.md": """# Claims Ledger

格式参见工作区契约。Numbers 表格中的值必须与论文中出现的形式完全一致，
且必须从项目文件中读取，绝不能凭记忆填写。

## Claims

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
""",
    "outline.md": """# Outline

## Abstract draft

## Paragraph outline
<!-- 一行 = 论文中的一个段落 -->

## Figure and table plan

## Page budget (8 pages main body)
""",
    "open_issues.md": "# Open Issues (need a human)\n\n",
    "decisions.md": "# Decisions Log\n\n",
    "citations_log.md": """# Citation Verification Log

| key | status | sources checked | published version | notes |
|-----|--------|-----------------|-------------------|-------|
""",
    "camera_ready.md": "# Camera-Ready Checklist Status\n\n(由 icml-camera-ready 在需要时创建)\n",
}

DIRS = ["reviews", "rebuttal"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="论文的 LaTeX 根目录")
    ap.add_argument("--skill", default="unknown-skill", help="调用技能的名称（用于日志）")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: {root} 不是目录", file=sys.stderr)
        sys.exit(2)
    ws = root / ".icml"
    ws.mkdir(exist_ok=True)

    created, kept = [], []
    for name, text in TEMPLATES.items():
        p = ws / name
        if p.exists():
            kept.append(name)
            continue
        p.write_text(text.replace("{skill}", args.skill), encoding="utf-8")
        created.append(name)

    facts_dst = ws / "venue_facts.md"
    facts_src = Path(__file__).resolve().parent.parent / "references" / "icml-venue-facts.md"
    if facts_dst.exists():
        kept.append("venue_facts.md")
    elif facts_src.exists():
        shutil.copy(facts_src, facts_dst)
        created.append("venue_facts.md (快照副本 - 请为目标年份刷新)")
    else:
        print("WARN: 本脚本旁未找到 icml-venue-facts.md；未创建 venue_facts.md")

    for d in DIRS:
        (ws / d).mkdir(exist_ok=True)

    print(f"Workspace: {ws}")
    if created:
        print("Created: " + ", ".join(created))
    if kept:
        print("Already present (untouched): " + ", ".join(kept))
    gi = root / ".gitignore"
    print("Note: .icml/ 存放工作笔记。在未经审查的情况下，它绝不能被包含在匿名补充 zip 或公开的 camera-ready 仓库中。")
    if gi.exists() and ".icml" not in gi.read_text(encoding="utf-8", errors="ignore"):
        print("Hint: 请考虑是否应将 .icml/ 列入公开仓库的 .gitignore。")


if __name__ == "__main__":
    main()
