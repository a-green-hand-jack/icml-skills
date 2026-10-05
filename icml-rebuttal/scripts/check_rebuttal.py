#!/usr/bin/env python3
"""在发布前检查 ICML rebuttal 回复文件。

对每个文件检查：字符数与限制对比、URL（任何 URL；将缩短/非匿名 URL 标记为错误）、
身份字符串、未解决的占位符、claims ledger 中缺失的数字（可选）、空洞承诺、
攻击性措辞和过度道歉。

用法：
    python check_rebuttal.py round1/*.md [--limit 5000] [--names "A B,C D"] [--affils "Univ"]
                             [--ledger .icml/claims.md]
如有任何文件存在 ERROR，退出码为 1。
"""
import argparse
import re
import sys
from pathlib import Path

# 缩短链接服务
SHORTENERS = r"(bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|rebrand\.ly|shorturl\.at|cutt\.ly)"
# 攻击性措辞
COMBATIVE = r"\b(the reviewer (is|was) (wrong|mistaken|incorrect)|clearly (wrong|misunderstood)|obviously|as anyone (can|could) see|failed to (read|notice|understand)|did not (read|bother)|ridiculous|absurd|unfair review|careless(ly)?)\b"
# 承诺模式
PROMISE = r"\bwe will (clarify|discuss|add|include|explain|elaborate|expand|address|revise|fix|update)\b"
# 道歉模式
APOLOGY = r"\b(sorry|apologi[sz]e|apologies)\b"
# 要求改分
SCORE_ASK = r"\b(raise|increase|reconsider|improve) (your|the) (score|rating)\b"


def ledger_values(path):
    """从 claims ledger 中提取所有数值。"""
    vals = set()
    txt = Path(path).read_text(encoding="utf-8")
    if "## Numbers" not in txt:
        return vals
    for line in txt.split("## Numbers", 1)[1].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in ("id", "") and not set(cells[0]) <= set("-"):
            vals.add(cells[1].replace(",", "").rstrip("%"))
    return vals


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--limit", type=int, default=5000)
    ap.add_argument("--names", default="")
    ap.add_argument("--affils", default="")
    ap.add_argument("--ledger")
    a = ap.parse_args()
    idents = [s.strip() for s in (a.names + "," + a.affils).split(",") if s.strip()]
    ledger = ledger_values(a.ledger) if a.ledger and Path(a.ledger).exists() else None
    any_err = False

    for f in a.files:
        text = Path(f).read_text(encoding="utf-8")
        body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        errs, warns = [], []
        n = len(body.strip())
        if n > a.limit:
            errs.append(f"{n} 个字符 > 限制 {a.limit}（需删减 {n - a.limit}）。")
        elif n > 0.95 * a.limit:
            warns.append(f"{n} 个字符：距离限制不到 5%；OpenReview 的计数可能略有差异。")
        for u in re.findall(r"https?://\S+|www\.\S+", body):
            if re.search(SHORTENERS, u) or re.search(r"github\.com/(?!anonymous)|\.edu/~|sites\.google|linkedin|twitter\.com|x\.com/", u):
                errs.append(f"非匿名或缩短的 URL: {u}")
            elif "anonymous" not in u:
                warns.append(f"存在 URL ({u})；审稿人不被要求点击链接——请将内容放入正文中。")
        for idn in idents:
            if re.search(r"(?<![A-Za-z])" + re.escape(idn) + r"(?![A-Za-z])", body, re.I if len(idn) > 4 else 0):
                errs.append(f"出现身份字符串 '{idn}'。")
        if re.search(r"\b(our (previous|prior|earlier) (paper|work)|in our \w+ paper)\b", body, re.I):
            warns.append("可能存在第一人称引用自己先前工作的情况（匿名性问题）。")
        if re.search(r"TODO|TBD|XXX|\[N\?\]|\[RESULT\]|PLACEHOLDER", body):
            errs.append("存在未解决的占位符。")
        for m in re.finditer(PROMISE, body, re.I):
            tail = re.sub(r"\b(Sec|Secs|Fig|Figs|Eq|Eqs|Tab|App|Thm|Def|Prop|Lem|Alg|e\.g|i\.e|et al|cf|vs|No|L)\.", lambda x: x.group(0)[:-1] + "<dot>", body[m.end():])
            rest = re.split(r"(?<=[.!?])\s", tail, maxsplit=1)[0]
            if not re.search(r"[:\"\"]|as follows|namely", rest):
                warns.append(f"承诺缺乏实质内容，位置附近：'...{body[max(0, m.start()-40):m.end()+40].strip()}...'（不要承诺，要落实）。")
        for m in re.finditer(COMBATIVE, body, re.I):
            warns.append(f"攻击性措辞: '{m.group(0)}'")
        if re.search(SCORE_ASK, body, re.I):
            warns.append("请求审稿人更改分数——让证据来做到这一点。")
        ap_n = len(re.findall(APOLOGY, body, re.I))
        if ap_n > 2:
            warns.append(f"{ap_n} 次道歉——最多保留一次，仅在论文确实不清楚的地方。")
        if ledger is not None:
            for num in re.findall(r"(?<![\w.])\d+\.\d+%?", body):
                if num.rstrip("%") not in ledger:
                    warns.append(f"数字 {num} 不在 claims ledger 中——请从其源文件添加或移除它。")
        first = body.strip().splitlines()[0] if body.strip() else ""
        print(f"== {f}: {n} 字符 ({n / a.limit:.0%} 限制)")
        for e in errs:
            print(f"  ERROR {e}")
        for w in warns:
            print(f"  WARN  {w}")
        if not errs and not warns:
            print("  ok")
        any_err |= bool(errs)
    sys.exit(1 if any_err else 0)


if __name__ == "__main__":
    main()
