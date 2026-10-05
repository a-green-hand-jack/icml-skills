#!/usr/bin/env python3
"""Check that every reported number in the LaTeX source appears in the claims ledger.

Extracts decimals, percentages and multipliers (e.g. 92.1, 12%, 3.5x, 2.4k) from prose
and tables, ignoring citations, references, labels, lengths and option lists, and checks
each against the `## Numbers` table of `.icml/claims.md`. Integers are skipped unless
--integers is given (they are usually counts, section numbers or years).

A number matches a ledger value if the strings are equal after normalisation (commas,
trailing %, x/×). Unmatched numbers are reported with file:line. Ledger rows with
`verified` other than `yes` are reported as unverified.

Usage:
    python check_numbers.py main.tex --ledger .icml/claims.md [--integers] [--ignore 0.5,1.0]
"""
import argparse
import re
import sys
from pathlib import Path

NUM = re.compile(r"(?<![\w.\\])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+)\s*(\\?%|\\times|×|x\b|k\b|M\b|B\b)?")
STRIP = [
    r"\\(cite[a-z]*|ref|cref|Cref|eqref|autoref|label|url|href|includegraphics|input|include|bibliography|bibliographystyle|usepackage|documentclass|setlength|addtolength|vspace|hspace|resizebox|scalebox|definecolor|newcommand|renewcommand|icml[a-z]*|begin|end|multicolumn|multirow|cline|cmidrule|rule|arraystretch|fontsize|linewidth|columnwidth|textwidth)\*?(\[[^\]]*\])*(\{[^{}]*(\{[^{}]*\}[^{}]*)*\})*",
    r"\[[^\]]*(width|height|scale|trim|angle)[^\]]*\]",
    r"\d*\.?\d+\s*\\?(linewidth|columnwidth|textwidth|pt|em|ex|cm|mm|in)\b",
]


def norm(s):
    s = s.replace(",", "").replace("\\%", "%").replace("×", "x").replace("\\times", "x").strip()
    return s.rstrip("%x").strip()


def load_ledger(path):
    vals, unverified = {}, []
    txt = Path(path).read_text(encoding="utf-8")
    sec = txt.split("## Numbers", 1)
    if len(sec) < 2:
        sys.exit("ERROR: ledger has no '## Numbers' section")
    for line in sec[1].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] in ("id", "") or set(cells[0]) <= set("-"):
            continue
        nid, value, verified = cells[0], cells[1], cells[5].lower()
        if not value:
            continue
        vals.setdefault(norm(value), []).append(nid)
        if verified != "yes":
            unverified.append((nid, value, cells[3]))
    return vals, unverified


def load_tex(path, seen=None, root=True):
    seen = seen or set()
    p = Path(path)
    if not p.suffix:
        p = p.with_suffix(".tex")
    if not p.exists() or p.resolve() in seen:
        return []
    seen.add(p.resolve())
    rows, in_doc = [], False
    for n, raw in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = re.sub(r"(?<!\\)%.*", "", raw)
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", line)
        if m:
            if in_doc or not root:
                rows.extend(load_tex(p.parent / m.group(1), seen, root=False))
            continue
        if "\\begin{document}" in line:
            in_doc = True; continue
        if "\\end{document}" in line:
            break
        if root and not in_doc:
            continue
        rows.append((p.name, n, line))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex")
    ap.add_argument("--ledger", default=".icml/claims.md")
    ap.add_argument("--integers", action="store_true", help="also check integers >= 10 (excluding years)")
    ap.add_argument("--ignore", default="", help="comma-separated values to ignore (e.g. hyperparameters already in the appendix)")
    args = ap.parse_args()

    vals, unverified = load_ledger(args.ledger)
    ignore = {norm(v) for v in args.ignore.split(",") if v.strip()}
    rows = load_tex(args.tex)
    unmatched, matched = [], 0
    in_appendix = False
    for fname, n, line in rows:
        if "\\appendix" in line:
            in_appendix = True
        s = line
        for pat in STRIP:
            s = re.sub(pat, " ", s)
        for m in NUM.finditer(s):
            raw, suffix = m.group(1), m.group(2) or ""
            is_dec = "." in raw
            if not is_dec and not suffix:
                if not args.integers:
                    continue
                iv = int(raw.replace(",", ""))
                if iv < 10 or 1900 <= iv <= 2100:
                    continue
            key = norm(raw + suffix)
            if key in ignore:
                continue
            if key in vals:
                matched += 1
            else:
                ctx = line.strip()
                unmatched.append((f"{fname}:{n}", raw + suffix, ctx[:110], in_appendix))

    print(f"Numbers matched to ledger: {matched}")
    print(f"Numbers NOT in ledger: {len(unmatched)}")
    for where, num, ctx, app in unmatched:
        tag = " (appendix)" if app else ""
        print(f"  {where}{tag}: {num}    | {ctx}")
    if unverified:
        print(f"\nLedger rows not verified against a project file: {len(unverified)}")
        for nid, v, src in unverified:
            print(f"  {nid} = {v} (source: {src})")
    print("\nEvery unmatched main-body result must be added to the ledger from its source file, "
          "or removed. Hyperparameters and settings may be passed via --ignore.")
    sys.exit(1 if [u for u in unmatched if not u[3]] or unverified else 0)


if __name__ == "__main__":
    main()
