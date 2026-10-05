#!/usr/bin/env python3
"""Check ICML rebuttal response files before posting.

For each file, check: character count against the limit, URLs (any URL; flag shortened/non-anonymous URLs as errors),
identity strings, unresolved placeholders, numbers missing from the claims ledger (optional), empty promises,
combative wording, and excessive apologies.

Usage:
    python check_rebuttal.py round1/*.md [--limit 5000] [--names "A B,C D"] [--affils "Univ"]
                             [--ledger .icml/claims.md]
Exit code is 1 if any file has an ERROR.
"""
import argparse
import re
import sys
from pathlib import Path

# URL-shortening services
SHORTENERS = r"(bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|rebrand\.ly|shorturl\.at|cutt\.ly)"
# Combative wording
COMBATIVE = r"\b(the reviewer (is|was) (wrong|mistaken|incorrect)|clearly (wrong|misunderstood)|obviously|as anyone (can|could) see|failed to (read|notice|understand)|did not (read|bother)|ridiculous|absurd|unfair review|careless(ly)?)\b"
# Promise pattern
PROMISE = r"\bwe will (clarify|discuss|add|include|explain|elaborate|expand|address|revise|fix|update)\b"
# Apology pattern
APOLOGY = r"\b(sorry|apologi[sz]e|apologies)\b"
# Score-change request
SCORE_ASK = r"\b(raise|increase|reconsider|improve) (your|the) (score|rating)\b"


def ledger_values(path):
    """Extract all numeric values from the claims ledger."""
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
            errs.append(f"{n} characters > limit {a.limit} (trim {n - a.limit}).")
        elif n > 0.95 * a.limit:
            warns.append(f"{n} characters: within 5% of the limit; OpenReview's count may differ slightly.")
        for u in re.findall(r"https?://\S+|www\.\S+", body):
            if re.search(SHORTENERS, u) or re.search(r"github\.com/(?!anonymous)|\.edu/~|sites\.google|linkedin|twitter\.com|x\.com/", u):
                errs.append(f"Non-anonymous or shortened URL: {u}")
            elif "anonymous" not in u:
                warns.append(f"URL present ({u}); reviewers are not expected to click links—please place the content in the body.")
        for idn in idents:
            if re.search(r"(?<![A-Za-z])" + re.escape(idn) + r"(?![A-Za-z])", body, re.I if len(idn) > 4 else 0):
                errs.append(f"Identity string '{idn}' found.")
        if re.search(r"\b(our (previous|prior|earlier) (paper|work)|in our \w+ paper)\b", body, re.I):
            warns.append("Possible first-person reference to own prior work (anonymity issue).")
        if re.search(r"TODO|TBD|XXX|\[N\?\]|\[RESULT\]|PLACEHOLDER", body):
            errs.append("Unresolved placeholders present.")
        for m in re.finditer(PROMISE, body, re.I):
            tail = re.sub(r"\b(Sec|Secs|Fig|Figs|Eq|Eqs|Tab|App|Thm|Def|Prop|Lem|Alg|e\.g|i\.e|et al|cf|vs|No|L)\.", lambda x: x.group(0)[:-1] + "<dot>", body[m.end():])
            rest = re.split(r"(?<=[.!?])\s", tail, maxsplit=1)[0]
            if not re.search(r"[:\"\"]|as follows|namely", rest):
                warns.append(f"Promise lacks substance near: '...{body[max(0, m.start()-40):m.end()+40].strip()}...' (do not promise, deliver).")
        for m in re.finditer(COMBATIVE, body, re.I):
            warns.append(f"Combative wording: '{m.group(0)}'")
        if re.search(SCORE_ASK, body, re.I):
            warns.append("Asking reviewers to change scores—let the evidence do that.")
        ap_n = len(re.findall(APOLOGY, body, re.I))
        if ap_n > 2:
            warns.append(f"{ap_n} apologies—keep at most one, and only where the paper was genuinely unclear.")
        if ledger is not None:
            for num in re.findall(r"(?<![\w.])\d+\.\d+%?", body):
                if num.rstrip("%") not in ledger:
                    warns.append(f"Number {num} not in claims ledger—please add or remove it from its source file.")
        first = body.strip().splitlines()[0] if body.strip() else ""
        print(f"== {f}: {n} characters ({n / a.limit:.0%} of limit)")
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
