#!/usr/bin/env python3
"""Advisory sentence-level lint for ML papers (LaTeX source).

Flags patterns that the writing sources bundled with icml-write (Perez, Lipton,
Foerster, Gopen & Swan, Farquhar) advise against. Every hit is a prompt to look, not an
order to change: e.g., passive voice is often right (Gopen & Swan). Skips comments,
math, and common non-prose environments.

Usage:
    python lint_prose.py main.tex [--only RULE1,RULE2] [--summary]
"""
import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

RULES = [
    # id, regex (case-insensitive unless noted), message
    ("filler", r"\b(actually|a bit|fortunately|basically|essentially|note that|observe that|it is worth noting( that)?|it should be noted( that)?|needless to say|in order to|try to|attempts? to)\b",
     "Filler (Perez, Foerster): delete or rephrase."),
    ("intensifier", r"\b(very|really|extremely|incredibly|highly|truly|quite|rather|completely|significantly(?! (better|worse|outperform)\w* than)|remarkably|vastly)\b",
     "Intensifier (Lipton): drop it or replace with a number. 'significantly' should mean statistical significance."),
    ("hedge", r"\b(may|might|could|can|possibly|perhaps|potentially|somewhat|arguably)\b",
     "Hedge (Perez, Lipton): keep only if it encodes real uncertainty; otherwise state scope or evidence."),
    ("vague-pronoun", r"(^|[.!?]\s+)(This|These|That|Those|It)\s+(is|are|was|were|shows?|demonstrates?|suggests?|means?|allows?|enables?|leads?|results? in|makes?|implies|indicates?)\b",
     "Pronoun without noun (Perez): 'This result shows', not 'This shows'."),
    ("future", r"\b(we|will) will\b|\bwe will\b|\bwill be (shown|discussed|presented|described|introduced)\b",
     "Future tense (Foerster): 'we show', 'Section 4 shows'."),
    ("contraction", r"\b\w+(n't|'re|'ve|'ll|'d)\b|\b(it's|that's|there's|let's)\b",
     "Contraction: write it out in a paper."),
    ("anthropomorphism", r"\b(the |our |this )?(model|network|algorithm|agent|method|llm|system)s? (knows?|understands?|thinks?|believes?|tries|try|wants?|realizes?|learns? to understand)\b",
     "Anthropomorphism (Lipton, Foerster): algorithms do not try or know; define terms or rephrase."),
    ("llm-tell", r"\b(delve|delves|delving|pivotal|crucial(ly)?|landscape|realm|seamless(ly)?|paves? the way|plays? a (vital|crucial|key|pivotal) role|in recent years|has (gained|attracted) (significant|considerable|increasing) attention|game[- ]changer|cutting[- ]edge|groundbreaking|unprecedented|intricate|tapestry|underscores?|showcases?|harness(es|ing)?|leverag(e|es|ing) (the )?power)\b",
     "Phrase typical of LLM-generated or hype prose: replace with specific content."),
    ("generic-claim", r"\b(novel|state[- ]of[- ]the[- ]art|sota|superior|outstanding|impressive|significant(ly)? (improve|boost|enhance|outperform)\w*|comprehensive|extensive experiments|robust(ly)?)\b",
     "Adjective claim (Foerster: adjectives are red flags): back it with a number/comparison or cut it."),
    ("comparative", r"\b(better|worse|faster|slower|improves?|improved|outperforms?|higher|lower|more efficient)\b(?![^.]{0,80}\b(than|over|compared|relative|vs\.?|baseline)\b)",
     "Comparative without explicit comparison (Perez): than what?"),
    ("passive", r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?\w+ed\s+by\b",
     "Passive with agent: fine if it keeps the paragraph's topic first (Gopen & Swan); otherwise prefer active."),
    ("on-the-other-hand", r"\bon the other hand\b", "'On the other hand' needs 'on the one hand' (Foerster); consider 'in contrast'."),
    ("however-start", r"(^|[.!?]\s+)However,", "Sentence-initial 'However' (Perez: drop most connectives) - is the contrast real and needed?"),
    ("cite-plain", r"\\cite\{", "Plain \\cite: use \\citet (author in sentence) or \\citep (parenthetical) with natbib."),
    ("citep-as-subject", r"(^|[.!?]\s+)~?\\citep(\[[^\]]*\])*\{[^}]+\}\s+(show|propose|introduce|find|demonstrate|use)", "Citation as sentence subject should be \\citet."),
    ("straight-quotes", r"(?<![`'\\])\"[A-Za-z]", "Straight double quote in LaTeX: use ``...'' or \\enquote{}."),
    ("eg-ie", r"\b(e\.g|i\.e)\.(?!,)", "Add a comma after e.g. / i.e. (US style), or rephrase."),
    ("dup-word", r"\b(\w{3,})\s+\1\b", "Repeated word."),
    ("we-start", None, "Many consecutive sentences start with 'We' (Perez): vary."),
    ("colon-before-eq", r":\s*(\\begin\{(equation|align)|\\\[|\$\$)", "Colon before an equation that completes the sentence (Foerster): usually drop it."),
    ("generic-opener", None, "First sentence of the introduction looks generic (Lipton): could it start any ML paper?"),
]

SKIP_ENVS = r"(equation|align|gather|multline|figure|table|tabular|algorithm|algorithmic|tikzpicture|lstlisting|verbatim|minted|thebibliography)\*?"


def load(path, seen=None):
    seen = seen or set()
    p = Path(path)
    if not p.suffix:
        p = p.with_suffix(".tex")
    if not p.exists() or p.resolve() in seen:
        return []
    seen.add(p.resolve())
    rows, depth, in_doc = [], 0, True
    for n, raw in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = re.sub(r"(?<!\\)%.*", "", raw)
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", line)
        if m:
            rows.extend(load(p.parent / m.group(1), seen)); continue
        if re.search(r"\\begin\{%s\}" % SKIP_ENVS, line):
            depth += 1
        if depth:
            if re.search(r"\\end\{%s\}" % SKIP_ENVS, line):
                depth -= 1
            continue
        line = re.sub(r"\$[^$]*\$", " MATH ", line)
        line = re.sub(r"\\\(.*?\\\)", " MATH ", line)
        rows.append((p.name, n, line))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex")
    ap.add_argument("--only", help="comma-separated rule ids")
    ap.add_argument("--summary", action="store_true", help="print only counts per rule")
    args = ap.parse_args()
    only = set(args.only.split(",")) if args.only else None

    rows = load(args.tex)
    hits = defaultdict(list)
    for fname, n, line in rows:
        if line.lstrip().startswith("\\") and not re.search(r"[a-z]{3,} [a-z]{3,} [a-z]{3,}", line):
            continue  # command-only line
        for rid, pat, msg in RULES:
            if pat is None or (only and rid not in only):
                continue
            flags = 0 if rid in ("vague-pronoun", "however-start", "straight-quotes", "cite-plain", "citep-as-subject", "colon-before-eq") else re.I
            for m in re.finditer(pat, line, flags):
                frag = line[max(0, m.start() - 30): m.end() + 30].strip()
                hits[rid].append(f"{fname}:{n}: ...{frag}...")

    # Sentence-level checks over the joined text
    text = " ".join(l for _, _, l in rows)
    sents = re.split(r"(?<=[.!?])\s+", text)
    run = 0
    if not only or "we-start" in only:
        for s in sents:
            run = run + 1 if s.strip().startswith("We ") else 0
            if run == 4:
                hits["we-start"].append(f"...{s.strip()[:80]}...")
    if not only or "generic-opener" in only:
        intro = re.search(r"\\section\{Introduction\}(.*?)(?<=[.!?])\s", text, re.S | re.I)
        if intro:
            first = intro.group(1).strip()
            if re.search(r"(recent years|have (achieved|shown|demonstrated) (remarkable|impressive|great|significant)|has (become|emerged)|(is|are) (a |an )?(fundamental|important|key|central)|attracted|gained|success(es)? (in|across))", first, re.I):
                hits["generic-opener"].append(first[:160])

    # Spelling variety
    us = len(re.findall(r"\b\w+iz(e|es|ed|ing|ation)\b", text))
    uk = len(re.findall(r"\b\w+is(e|es|ed|ing|ation)\b", text)) - len(re.findall(r"\b(otherwise|likewise|precise|concise|exercise|advise|devise|promise|raise|noise|rise|wise|comprise|surprise|enterprise|expertise|premise|revise|supervise|compromise|disguise|praise|paradise|cruise|bruise|treatise|demise|chemise|franchise|televise|improvise)\w*\b", text, re.I))
    if us > 2 and uk > 2:
        hits["spelling-mix"].append(f"~{us} -ize forms and ~{uk} -ise forms: pick American or British and be consistent (Foerster).")

    msgs = {rid: msg for rid, _, msg in RULES}
    msgs["spelling-mix"] = "Spelling variety mix."
    total = sum(len(v) for v in hits.values())
    print(f"Prose lint: {total} hits across {len(hits)} rules (advisory).\n")
    for rid in sorted(hits, key=lambda r: -len(hits[r])):
        print(f"[{rid}] x{len(hits[rid])} - {msgs.get(rid, '')}")
        if not args.summary:
            for h in hits[rid][:40]:
                print(f"    {h}")
            if len(hits[rid]) > 40:
                print(f"    ... {len(hits[rid]) - 40} more")
        print()
    if not total:
        print("No hits. (A clean lint is not a clean paper: run the paragraph pass too.)")


if __name__ == "__main__":
    main()
