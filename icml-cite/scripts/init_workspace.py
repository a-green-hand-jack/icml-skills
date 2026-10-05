#!/usr/bin/env python3
"""在论文 LaTeX 根目录旁边创建（或补全）`.icml/` 工作区。

永远不会覆盖现有文件。每次会话开始时安全运行。

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
- Last action ({TODAY}, {{skill}}): created workspace
- Next step: refresh venue_facts.md for the target year, then start the task
- Blocking: none
""",
    "claims.md": """# Claims Ledger

See the workspace contract for the format. Values in the Numbers table must be written
exactly as they appear in the paper and must be read from a project file, never recalled.

## Claims

## Numbers
| id | value | unit | source | locator | verified |
|----|-------|------|--------|---------|----------|
""",
    "outline.md": """# Outline

## Abstract draft

## Paragraph outline
<!-- one line = one paragraph in the paper -->

## Figure and table plan

## Page budget (8 pages main body)
""",
    "open_issues.md": "# Open Issues (need a human)\n\n",
    "decisions.md": "# Decisions Log\n\n",
    "citations_log.md": """# Citation Verification Log

| key | status | sources checked | published version | notes |
|-----|--------|-----------------|-------------------|-------|
""",
    "camera_ready.md": "# Camera-Ready Checklist Status\n\n(created by icml-camera-ready when needed)\n",
}

DIRS = ["reviews", "rebuttal"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="论文的 LaTeX 根目录")
    ap.add_argument("--skill", default="unknown-skill", help="调用 skill 的名称（用于日志）")
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
        created.append("venue_facts.md (snapshot copy - refresh it for the target year)")
    else:
        print("WARN: icml-venue-facts.md 未在脚本旁边找到；未创建 venue_facts.md")

    for d in DIRS:
        (ws / d).mkdir(exist_ok=True)

    print(f"Workspace: {ws}")
    if created:
        print("Created: " + ", ".join(created))
    if kept:
        print("Already present (untouched): " + ", ".join(kept))
    gi = root / ".gitignore"
    print("Note: .icml/ holds working notes. It must never be included in an anonymous "
          "supplementary zip or a public camera-ready repo without review.")
    if gi.exists() and ".icml" not in gi.read_text(encoding="utf-8", errors="ignore"):
        print("Hint: consider whether .icml/ should be listed in .gitignore for public repos.")


if __name__ == "__main__":
    main()
