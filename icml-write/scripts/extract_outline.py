#!/usr/bin/env python3
"""Build a reverse outline from `% TL;DR:` comments placed above paragraphs.

For each section it lists the TL;DR of every paragraph, flags paragraphs that have no
TL;DR, and flags TL;DR comments not followed by a paragraph. Follows \\input/\\include.

Usage:
    python extract_outline.py main.tex [--show-first-sentence]

Convention (Foerster): one outline line == one paragraph. Put the line as a comment
directly above the paragraph:

    % TL;DR: Adding the auxiliary loss halves divergence on long sequences.
    Adding the auxiliary loss ...
"""
import argparse
import re
from pathlib import Path

TLDR = re.compile(r"^\s*%+\s*TL;?DR\s*:?\s*(.*)$", re.I)
SECTION = re.compile(r"\\(section|subsection|subsubsection|paragraph)\*?\{(.+?)\}")
SKIP_ENVS = ("figure", "table", "equation", "align", "algorithm", "tabular", "itemize",
             "enumerate", "abstract", "thebibliography", "tikzpicture", "lstlisting", "verbatim")


def read_lines(path, seen=None):
    seen = seen or set()
    p = Path(path)
    if not p.suffix:
        p = p.with_suffix(".tex")
    if not p.exists() or p.resolve() in seen:
        return []
    seen.add(p.resolve())
    out = []
    for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        code = line.split("%", 1)[0] if not TLDR.match(line) else ""
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", code)
        if m:
            out.extend(read_lines(p.parent / m.group(1), seen))
            continue
        out.append((p.name, n, line))
    return out


def first_sentence(text):
    text = re.sub(r"\\(cite[pt]?|ref|cref|Cref|label|eqref)\*?(\[[^\]]*\])*\{[^}]*\}", "[x]", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", "", text)
    text = re.sub(r"[{}]", "", text).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text)[:200]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex")
    ap.add_argument("--show-first-sentence", action="store_true",
                    help="print each paragraph's first sentence under its TL;DR to compare them")
    args = ap.parse_args()

    lines = read_lines(args.tex)
    in_doc = not any("\\begin{document}" in l for _, _, l in lines)
    env_depth = 0
    pending = None            # (tldr text, file, line)
    para = []                 # current paragraph lines
    para_start = None
    para_tldr = None
    out = []                  # entries: ("sec", title) | ("para", tldr, loc, first) | ("orphan", tldr, loc)
    n_para = n_missing = 0
    backmatter = False

    def flush():
        nonlocal para, para_start, para_tldr, n_para, n_missing
        if para and backmatter:
            para, para_start, para_tldr = [], None, None
            return
        if para:
            text = " ".join(para).strip()
            if len(text.split()) >= 8:
                n_para += 1
                if para_tldr is None:
                    n_missing += 1
                out.append(("para", para_tldr, para_start, first_sentence(text)))
        para, para_start, para_tldr = [], None, None

    for fname, n, raw in lines:
        if "\\begin{document}" in raw:
            in_doc = True
            continue
        if not in_doc:
            continue
        if "\\end{document}" in raw:
            break
        m = TLDR.match(raw)
        if m:
            flush()
            if pending:
                out.append(("orphan", pending[0], pending[1]))
            pending = (m.group(1).strip(), f"{fname}:{n}")
            continue
        code = raw.split("%", 1)[0]
        if re.search(r"\\begin\{(%s)\*?\}" % "|".join(SKIP_ENVS), code):
            flush(); env_depth += 1
        if env_depth:
            if re.search(r"\\end\{(%s)\*?\}" % "|".join(SKIP_ENVS), code):
                env_depth -= 1
            continue
        s = SECTION.search(code)
        if s:
            flush()
            if pending:
                out.append(("orphan", pending[0], pending[1])); pending = None
            level = {"section": 0, "subsection": 1, "subsubsection": 2, "paragraph": 3}[s.group(1)]
            out.append(("sec", "  " * level + s.group(2)))
            backmatter = bool(re.match(r"\s*(Acknowledg|Impact Statement|Broader Impact)", s.group(2), re.I))
            rest = code[s.end():].strip()
            if s.group(1) == "paragraph" and rest:
                para_start = f"{fname}:{n}"
                para_tldr = pending[0] if pending else None
                pending = None
                para.append(rest)
            continue
        if not code.strip():
            flush()
            continue
        if re.match(r"\s*\\(appendix|bibliography|bibliographystyle|maketitle|printAffiliations|icml)", code):
            if "\\appendix" in code:
                flush(); out.append(("sec", "APPENDIX"))
            continue
        if not para:
            para_start = f"{fname}:{n}"
            para_tldr = pending[0] if pending else None
            pending = None
        para.append(code)
    flush()
    if pending:
        out.append(("orphan", pending[0], pending[1]))

    print("# Reverse outline\n")
    for e in out:
        if e[0] == "sec":
            print(f"\n## {e[1]}")
        elif e[0] == "para":
            _, tl, where, first = e
            if tl:
                print(f"- {tl}  ({where})")
            else:
                print(f"- **[NO TL;DR]** ({where}) starts: \"{first}\"")
            if args.show_first_sentence and tl:
                print(f"    first sentence: \"{first}\"")
        else:
            print(f"- **[ORPHAN TL;DR - no paragraph follows]** {e[1]} ({e[2]})")
    print(f"\n---\n{n_para} paragraphs, {n_missing} without TL;DR.")
    print("Read the TL;DR lines alone: they should tell the paper's story in order. "
          "Compare each TL;DR with its paragraph's first sentence; they should say the same thing.")


if __name__ == "__main__":
    main()
