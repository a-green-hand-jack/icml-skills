#!/usr/bin/env python3
"""Check ICML rebuttal response files before posting.

For each file: character count vs limit, URLs (any; flags shortened/non-anonymous ones
as errors), identity strings, unresolved placeholders, numbers missing from the claims
ledger (optional), empty promises, combative phrasing and apology overuse.

Usage:
    python check_rebuttal.py round1/*.md [--limit 5000] [--names "A B,C D"] [--affils "Univ"]
                             [--ledger .icml/claims.md]
Exit code 1 if any file has an ERROR.
"""
import argparse
import re
import sys
from pathlib import Path

SHORTENERS = r"(bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|rebrand\.ly|shorturl\.at|cutt\.ly)"
COMBATIVE = r"\b(the reviewer (is|was) (wrong|mistaken|incorrect)|clearly (wrong|misunderstood)|obviously|as anyone (can|could) see|failed to (read|notice|understand)|did not (read|bother)|ridiculous|absurd|unfair review|careless(ly)?)\b"
PROMISE = r"\bwe will (clarify|discuss|add|include|explain|elaborate|expand|address|revise|fix|update)\b"
APOLOGY = r"\b(sorry|apologi[sz]e|apologies)\b"
SCORE_ASK = r"\b(raise|increase|reconsider|improve) (your|the) (score|rating)\b"


def ledger_values(path):
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
            errs.append(f"{n} characters > limit {a.limit} (cut {n - a.limit}).")
        elif n > 0.95 * a.limit:
            warns.append(f"{n} characters: within 5% of the limit; OpenReview counting may differ slightly.")
        for u in re.findall(r"https?://\S+|www\.\S+", body):
            if re.search(SHORTENERS, u) or re.search(r"github\.com/(?!anonymous)|\.edu/~|sites\.google|linkedin|twitter\.com|x\.com/", u):
                errs.append(f"Non-anonymous or shortened URL: {u}")
            elif "anonymous" not in u:
                warns.append(f"URL present ({u}); reviewers are not expected to follow links - put the content in the text.")
        for idn in idents:
            if re.search(r"(?<![A-Za-z])" + re.escape(idn) + r"(?![A-Za-z])", body, re.I if len(idn) > 4 else 0):
                errs.append(f"Identity string '{idn}' appears.")
        if re.search(r"\b(our (previous|prior|earlier) (paper|work)|in our \w+ paper)\b", body, re.I):
            warns.append("Possible first-person reference to own prior work (anonymity).")
        if re.search(r"TODO|TBD|XXX|\[N\?\]|\[RESULT\]|PLACEHOLDER", body):
            errs.append("Unresolved placeholder.")
        for m in re.finditer(PROMISE, body, re.I):
            tail = re.sub(r"\b(Sec|Secs|Fig|Figs|Eq|Eqs|Tab|App|Thm|Def|Prop|Lem|Alg|e\.g|i\.e|et al|cf|vs|No|L)\.", lambda x: x.group(0)[:-1] + "<dot>", body[m.end():])
            rest = re.split(r"(?<=[.!?])\s", tail, maxsplit=1)[0]
            if not re.search(r"[:\"“]|as follows|namely", rest):
                warns.append(f"Promise without content near: '...{body[max(0, m.start()-40):m.end()+40].strip()}...' (don't promise, do).")
        for m in re.finditer(COMBATIVE, body, re.I):
            warns.append(f"Combative phrasing: '{m.group(0)}'")
        if re.search(SCORE_ASK, body, re.I):
            warns.append("Asks the reviewer to change the score - let the evidence do that.")
        ap_n = len(re.findall(APOLOGY, body, re.I))
        if ap_n > 2:
            warns.append(f"{ap_n} apologies - keep at most one, where the paper was genuinely unclear.")
        if ledger is not None:
            for num in re.findall(r"(?<![\w.])\d+\.\d+%?", body):
                if num.rstrip("%") not in ledger:
                    warns.append(f"Number {num} not in claims ledger - add it from its source file or remove it.")
        first = body.strip().splitlines()[0] if body.strip() else ""
        print(f"== {f}: {n} chars ({n / a.limit:.0%} of limit)")
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
