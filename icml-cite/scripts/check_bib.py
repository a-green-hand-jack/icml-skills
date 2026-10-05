#!/usr/bin/env python3
"""Audit a BibTeX file against the LaTeX source of an ICML paper.

Report: keys cited but missing from .bib; unused entries; duplicate works; missing
required fields; arXiv/CoRR entries that should be upgraded; title capitalizations that
BibTeX will lowercase; placeholder keys; plain \\cite usage; when --log is given, entries
not yet present in the verification log (.icml/citations_log.md).

Exit code 1 if cited keys are missing or placeholders still exist.

Usage:
    python check_bib.py main.tex refs.bib [more.bib ...] [--log .icml/citations_log.md]
"""
import argparse
import re
import sys
from pathlib import Path

REQUIRED = {
    "inproceedings": ["author", "title", "booktitle", "year"],
    "conference": ["author", "title", "booktitle", "year"],
    "article": ["author", "title", "journal", "year"],
    "book": ["title", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["title", "year"],
}
KNOWN_LOWER_OK = {"I", "A"}


def parse_bib(text):
    entries = {}
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I).search(text, i)
        if not m:
            break
        etype, key = m.group(1).lower(), m.group(2)
        depth, j = 1, m.end()
        while j < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        body = text[m.end():j - 1]
        i = j
        if etype in ("comment", "string", "preamble"):
            continue
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            name, k = fm.group(1).lower(), fm.end()
            if k < len(body) and body[k] == "{":
                d, s = 1, k + 1
                while s < len(body) and d:
                    d += {"{": 1, "}": -1}.get(body[s], 0); s += 1
                fields[name] = body[k + 1:s - 1]
            elif k < len(body) and body[k] == '"':
                e = body.find('"', k + 1); fields[name] = body[k + 1:e]
            else:
                v = re.match(r"[^,\n]+", body[k:]); fields[name] = v.group(0).strip() if v else ""
        entries.setdefault(key, []).append((etype, fields))
    return entries


def tex_keys(path, seen=None):
    seen = seen or set()
    p = Path(path)
    if not p.suffix:
        p = p.with_suffix(".tex")
    if not p.exists() or p.resolve() in seen:
        return {}, 0
    seen.add(p.resolve())
    keys, plain = {}, 0
    for n, raw in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = re.sub(r"(?<!\\)%.*", "", raw)
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", line)
        if m:
            k2, p2 = tex_keys(p.parent / m.group(1), seen)
            for k, v in k2.items():
                keys.setdefault(k, []).extend(v)
            plain += p2
        for cm in re.finditer(r"\\(cite[a-zA-Z]*|nocite)\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}", line):
            if cm.group(1) == "cite":
                plain += 1
            for k in cm.group(2).split(","):
                k = k.strip()
                if k and k != "*":
                    keys.setdefault(k, []).append(f"{p.name}:{n}")
    return keys, plain


PROPER = {
    "bayesian", "bayes", "markov", "gaussian", "lipschitz", "transformer", "transformers", "monte", "carlo",
    "langevin", "euclidean", "hessian", "riemannian", "wasserstein", "boltzmann", "dirichlet", "hilbert",
    "fourier", "kalman", "newton", "nash", "shapley", "bellman", "lagrangian", "laplace", "laplacian",
    "poisson", "bernoulli", "gibbs", "metropolis", "hastings", "kullback", "leibler", "jensen", "shannon",
    "turing", "hamiltonian", "nesterov", "adam", "lstm", "english", "chinese", "german", "french",
    "japanese", "korean", "wikipedia", "atari", "python", "pytorch", "jax", "go", "imagenet", "cifar",
    "mujoco", "github", "stein", "rademacher", "vapnik", "chervonenkis", "banach", "sobolev", "hoeffding",
    "bregman", "frobenius", "kolmogorov", "itô", "ito", "brownian", "wiener",
}


def unprotected_caps(title):
    """Words that BibTeX will lowercase but must remain uppercase: acronyms, camelCase,
    and common proper nouns. Normal title-case words are fine (the style will lowercase them)."""
    stripped = re.sub(r"\{[^{}]*\}", " ", title)
    flagged = []
    for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", stripped):
        if w in KNOWN_LOWER_OK:
            continue
        if sum(c.isupper() for c in w[1:]) >= 1 or re.search(r"\d", w) and w[0].isupper():
            flagged.append(w)          # BERT, GPT4, ImageNet, MuJoCo
        elif w.lower() in PROPER and w[0].isupper():
            flagged.append(w)          # Bayesian, Markov, Transformer
    return flagged


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex")
    ap.add_argument("bib", nargs="+")
    ap.add_argument("--log", help="Path to .icml/citations_log.md")
    a = ap.parse_args()

    entries = {}
    for b in a.bib:
        for k, v in parse_bib(Path(b).read_text(encoding="utf-8", errors="replace")).items():
            entries.setdefault(k, []).extend(v)
    cited, plain = tex_keys(a.tex)
    problems = 0

    def section(title, items):
        if items:
            print(f"\n## {title} ({len(items)})")
            for it in items:
                print(f"  - {it}")

    missing = [f"{k}  (cited in {', '.join(v[:3])})" for k, v in cited.items() if k not in entries]
    placeholders = [k for k in cited if re.search(r"placeholder|verify|todo|citation_?needed", k, re.I)]
    problems += len(missing) + len(placeholders)
    section("ERROR: cited keys missing from .bib", missing)
    section("ERROR: placeholder citations still in text", placeholders)
    section("Duplicate keys in .bib", [k for k, v in entries.items() if len(v) > 1])

    seen_titles, dups = {}, []
    for k, v in entries.items():
        t = re.sub(r"[^a-z0-9]", "", v[0][1].get("title", "").lower())
        ids = [v[0][1].get("doi", "").lower(), v[0][1].get("eprint", "").lower()]
        for ident in [t] + [i for i in ids if i]:
            if not ident:
                continue
            if ident in seen_titles and seen_titles[ident] != k:
                dups.append(f"{seen_titles[ident]} == {k}")
            seen_titles.setdefault(ident, k)
    section("Possible duplicate works under different keys", sorted(set(dups)))

    incomplete, arxiv, caps = [], [], []
    for k, v in entries.items():
        if k not in cited:
            continue
        etype, f = v[0]
        req = REQUIRED.get(etype, ["title", "year"])
        miss = [r for r in req if not f.get(r, "").strip()]
        if "author" not in f and "editor" not in f and etype not in ("misc", "book"):
            miss.append("author")
        if miss:
            incomplete.append(f"{k} (@{etype}): missing {', '.join(sorted(set(miss)))}")
        venue = " ".join([f.get("journal", ""), f.get("booktitle", ""), f.get("publisher", ""), f.get("howpublished", ""), f.get("archiveprefix", "")]).lower()
        if "arxiv" in venue or "corr" in venue.split() or f.get("eprint") and not f.get("booktitle"):
            arxiv.append(f"{k}: {f.get('title', '')[:80]}")
        fl = unprotected_caps(f.get("title", ""))
        if fl:
            caps.append(f"{k}: {', '.join(fl[:6])}")
    section("Entries missing required fields", incomplete)
    section("arXiv/CoRR entries - check for published version (cite_lookup.py published)", arxiv)
    section("Title capitalizations that BibTeX may lowercase - protect proper nouns/acronyms with braces", caps)
    section("Unused .bib entries (info)", sorted(k for k in entries if k not in cited))
    if plain:
        print(f"\n## Plain \\cite used {plain} times - ICML uses natbib: \\citet (in-text) or \\citep (parenthetical).")

    if a.log and Path(a.log).exists():
        logged = set(re.findall(r"^\|\s*([^|\s]+)\s*\|\s*(verified|existence-only|placeholder)", Path(a.log).read_text(encoding="utf-8"), re.M))
        logged_keys = {k for k, _ in logged}
        section("Cited but not in verification log", sorted(k for k in cited if k not in logged_keys))

    print(f"\nCited keys: {len(cited)}; .bib entries: {len(entries)}.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
