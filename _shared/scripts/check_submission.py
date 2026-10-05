#!/usr/bin/env python3
"""Mechanical compliance checker for ICML papers (LaTeX source and/or compiled PDF).

All checks are heuristic: every ERROR must be fixed or explicitly waived by a human;
every WARN must be inspected. No anomalies found does not constitute proof of compliance —
the official ICML paper checker and human review are still required.

Usage:
    python check_submission.py --tex main.tex [--pdf main.pdf] [--mode submission|camera-ready]
                               [--names "Jane Doe,John Roe"] [--affils "MIT,Acme Corp"]
                               [--position-track] [--pristine-sty path/to/official/icml2026.sty]
                               [--page-limit N] [--json]

Exit codes: 0 = no ERROR found, 1 = at least one ERROR, 2 = usage error.
Uses only the Python standard library; uses poppler tools (pdftotext, pdfinfo,
pdffonts) when installed, warns when missing.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

FINDINGS = []


def add(level, code, msg, loc=None):
    FINDINGS.append({"level": level, "code": code, "msg": msg, "loc": loc})


# ----------------------------------------------------------------- LaTeX loading

def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\\\" and i + 1 < len(line):
            out.append(line[i:i + 2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)


def load_tex(main, seen=None):
    """Return list of (path, lineno, text_without_comment), tracking \\input/\\include."""
    seen = seen or set()
    main = Path(main)
    if not main.suffix:
        main = main.with_suffix(".tex")
    if not main.exists() or main.resolve() in seen:
        if not main.exists():
            add("WARN", "TEX-MISSING-INPUT", f"Input file not found: {main}")
        return []
    seen.add(main.resolve())
    rows = []
    for n, raw in enumerate(main.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = strip_comment(raw)
        for m in re.finditer(r"\\\\(?:input|include|subfile)\{([^}]+)\}", line):
            child = (main.parent / m.group(1).strip())
            rows.extend(load_tex(child, seen))
        rows.append((str(main), n, line))
    return rows


def loc(row):
    return f"{Path(row[0]).name}:{row[1]}"


# ----------------------------------------------------------------- TeX checks

def check_tex(rows, args):
    text = "\n".join(r[2] for r in rows)
    mode = args.mode

    # Style options
    m = re.search(r"\\\\usepackage(\[[^\]]*\])?\{icml20\d\d\}", text)
    if not m:
        add("ERROR", "STYLE-MISSING", "\\usepackage{icml20XX} not found. Official ICML style file is mandatory.")
    else:
        opts = m.group(1) or ""
        if mode == "submission" and "accepted" in opts:
            add("ERROR", "STYLE-ACCEPTED-IN-SUBMISSION", "'accepted' option set: author names will be printed. Please remove before submission.")
        if mode == "camera-ready" and "accepted" not in opts:
            add("ERROR", "STYLE-NOT-ACCEPTED", "Camera-ready must use \\usepackage[accepted]{icml20XX}.")
    if re.search(r"\\\\documentclass\[[^\]]*a4paper", text) or "a4paper" in text:
        add("ERROR", "PAPER-A4", "a4paper found; ICML requires US Letter.")

    # Spacing / layout hacks
    hacks = [
        (r"\\\\vspace\*?\{\s*-*", "negative \\vspace"),
        (r"\\\\setlength\{\\\\(textheight|textwidth|columnsep|topmargin|oddsidemargin|evensidemargin|baselineskip|parskip|abovedisplayskip|belowdisplayskip|textfloatsep|floatsep|intextsep|abovecaptionskip|belowcaptionskip)\}", "\\setlength modifying layout length"),
        (r"\\\\addtolength\{\\\\(textheight|textwidth|columnsep|topmargin)\}", "\\addtolength modifying layout length"),
        (r"\\\\linespread\{", "\\linespread"),
        (r"\\\\renewcommand\{?\\\\baselinestretch", "\\baselinestretch"),
        (r"\\\\titlespacing", "\\titlespacing"),
        (r"\\\\usepackage(\[[^\]]*\])?\{(geometry|savetrees|titlesec|setspace)\}", "package modifying layout"),
    ]
    for r in rows:
        for pat, what in hacks:
            if re.search(pat, r[2]):
                lvl = "ERROR" if "layout" in what or "baselinestretch" in what or "linespread" in what else "WARN"
                add(lvl, "LAYOUT-HACK", f"{what}: ICML prohibits altering the template or compressing vertical spacing.", loc(r))

    # Hidden / reviewer-facing text (prompt injection risk)
    hidden = [
        (r"\\\\(text)?color\{\s*white\s*\}", "white text"),
        (r"\\\\color\[[^\]]*\]\{[^}]*\}\{?\s*1\s*,\s*1\s*,\s*1", "white (RGB 1,1,1) text"),
        (r"\\\\fontsize\{\s*0*(\.\d+|[0-3](\.\d+)?)\s*(pt)?\s*\}", "font size smaller than 4pt"),
        (r"\\\\scalebox\{\s*0*\.0\d", "near-zero \\scalebox"),
        (r"\\\\phantom\{[^}]{20,}\}", "long \\phantom text"),
    ]
    for r in rows:
        for pat, what in hidden:
            if re.search(pat, r[2]):
                add("ERROR", "HIDDEN-TEXT", f"{what}: invisible text may be regarded as prompt injection (direct rejection). Please remove.", loc(r))
        if re.search(r"(?i)(ignore (all |any )?(previous|prior) instructions|as an? (ai|llm|language model) review|give (this paper )?a (high|positive) (score|rating)|reviewer.{0,20}(llm|ai|gpt))", r[2]):
            add("ERROR", "INJECTION-PHRASE", "Text targets LLM reviewers. Prompt injection is prohibited.", loc(r))

    # Leftover placeholders
    for r in rows:
        if re.search(r"(\\\\todo\b|\bTODO\b|\bTBD\b|\bXXX\b|PLACEHOLDER|CITATION NEEDED|\?\?\?)", r[2]):
            add("ERROR" if mode == "camera-ready" else "WARN", "PLACEHOLDER", "Unresolved placeholder/TODO.", loc(r))

    # Abstract
    am = re.search(r"\\\\begin\{abstract\}(.*?)\\\\end\{abstract\}", text, re.S)
    if not am:
        add("ERROR", "ABSTRACT-MISSING", "abstract environment not found.")
    else:
        body = am.group(1).strip()
        if re.search(r"\n\s*\n", body) or "\\par" in body:
            add("ERROR", "ABSTRACT-PARAGRAPHS", "Abstract must be a single paragraph.")
        plain = re.sub(r"\\\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", body)
        plain = re.sub(r"\b(e\.g|i\.e|et al|cf|vs|resp|approx|Fig|Sec|Eq|Tab)\.", "ABBR", plain)
        plain = re.sub(r"(\d)\.(\d)", r"\1DOT\2", plain)
        sents = [s for s in re.split(r"(?<=[.!?])\s+", plain.strip()) if len(s.split()) >= 3]
        n = len(sents)
        words = len(plain.split())
        if n < 4 or n > 6:
            add("WARN" if n <= 8 else "ERROR", "ABSTRACT-SENTENCES", f"Abstract has about {n} sentences ({words} words); ICML recommends 4–6 sentences.")
        else:
            add("INFO", "ABSTRACT-SENTENCES", f"Abstract has about {n} sentences ({words} words).")

    # Title case
    tm = re.search(r"\\\\icmltitle\{(.+?)\}\s*$", text, re.M)
    if tm:
        title = re.sub(r"\\\\[a-zA-Z]+|[{}$]", "", tm.group(1))
        letters = re.sub(r"[^A-Za-z]", "", title)
        if letters and letters.isupper() and len(letters) > 12:
            add("ERROR", "TITLE-ALLCAPS", "Title is all-caps; use title case for content words only.")
        small = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "of", "in", "on", "at", "to", "by", "up", "as", "via", "with", "from", "into", "over", "is", "vs"}
        bad = [w for w in title.split()[1:] if w.isalpha() and w[0].islower() and w.lower() not in small]
        if bad:
            add("WARN", "TITLE-CASE", f"Words in title that may need capitalization: {', '.join(bad[:8])}")

    # Required / prohibited sections
    impact = re.search(r"\\\\section\*?\{\s*(Impact Statement|Broader Impact[s]?( Statement)?)\s*\}", text, re.I)
    ack = re.search(r"\\\\section\*?\{\s*Acknowledg(e)?ments?\s*\}", text, re.I)
    bib = re.search(r"\\\\bibliography\{|\\\\begin\{thebibliography\}|\\\\printbibliography", text)
    if args.position_track:
        if not re.search(r"\\\\section\*?\{[^}]*Alternative Views?[^}]*\}", text, re.I):
            add("ERROR", "POSITION-ALT-VIEWS", "Position paper track requires an 'Alternative Views' section in the body.")
    else:
        if not impact:
            add("ERROR", "IMPACT-MISSING", "Main-track papers require an unnumbered 'Impact Statement' section before references.")
        else:
            if not impact.group(0).startswith("\\\\section*"):
                add("WARN", "IMPACT-NUMBERED", "Impact statement should be an unnumbered section (\\section*).")
            if bib and impact.start() > bib.start():
                add("ERROR", "IMPACT-AFTER-REFS", "Impact statement must appear before references.")
            app = re.search(r"\\\\appendix", text)
            if app and impact.start() > app.start():
                add("ERROR", "IMPACT-IN-APPENDIX", "Impact statement must appear before references, not in the appendix.")
    if ack and mode == "submission":
        add("ERROR", "ACK-IN-SUBMISSION", "Acknowledgments are not allowed in anonymous submissions.")
    if not bib:
        add("WARN", "BIB-MISSING", "bibliography command not found.")
    else:
        if not re.search(r"\\\\bibliographystyle\{icml20\d\d\}", text):
            add("WARN", "BIBSTYLE", "Expected \\bibliographystyle{icml20XX} (APA author–year format via natbib).")

    # Anonymity
    if mode == "submission":
        names = [n.strip() for n in (args.names or "").split(",") if n.strip()]
        affils = [a.strip() for a in (args.affils or "").split(",") if a.strip()]
        body_rows = [r for r in rows if not re.search(r"\\\\icml(author|affiliation|correspondingauthor)\b", r[2])]
        for r in body_rows:
            for nm in names + affils:
                if nm and re.search(r"(?<![A-Za-z])" + re.escape(nm) + r"(?![A-Za-z])", r[2], re.I if len(nm) > 4 else 0):
                    add("ERROR", "ANON-NAME", f"'{nm}' appears in the main text (outside the hidden author block).", loc(r))
            if re.search(r"(?i)\b(our|we) (own )?(previous|prior|earlier|recent) (work|paper|study|studies|method)\b|\bin our (previous|prior|earlier) ", r[2]):
                add("WARN", "ANON-SELFREF", "Possible first-person self-citation of prior work; please cite in third person.", loc(r))
            for u in re.findall(r"https?://[^\s}\]+", r[2]):
                if re.search(r"anonymous\.4open\.science|openreview\.net|arxiv\.org|doi\.org", u):
                    continue
                lvl = "ERROR" if re.search(r"github\.com|gitlab|huggingface\.co/(?!datasets/|models?/)|bit\.ly|tinyurl|goo\.gl|t\.co/|\.edu/~|sites\.google", u) else "WARN"
                add(lvl, "ANON-URL", f"URL may reveal identity or is non-anonymous: {u}", loc(r))
            if re.search(r"\\\\thanks\{|grant (no\.|number)|funded by|supported by (the )?(NSF|NIH|ERC|DARPA|NSFC)", r[2], re.I):
                add("WARN", "ANON-FUNDING", "Funding/grant text in submission reveals identity; please add only at camera-ready stage.", loc(r))
        hs = re.search(r"pdfauthor\s*=\s*\{?([^,}\n]+)", text)
        if hs and hs.group(1).strip():
            add("ERROR", "ANON-PDFMETA", f"hyperref pdfauthor is set ('{hs.group(1).strip()}'): this leaks into PDF metadata.")
    else:
        if not re.search(r"\\\\printAffiliationsAndNotice", text):
            add("ERROR", "CR-AFFIL-NOTICE", "Camera-ready must call \\printAffiliationsAndNotice{} (or {\\icmlEqualContribution}).")
        if re.search(r"Anonymous (Author|Institution)", text):
            add("ERROR", "CR-ANON-LEFTOVER", "Leftover placeholder 'Anonymous' author/institution text.")
        coi = re.search(r"Conflict of Interest Disclosure", text)
        if coi:
            secs = [m.start() for m in re.finditer(r"\\\\section\{", text)]
            if len(secs) >= 2 and coi.start() > secs[1]:
                add("ERROR", "CR-COI-PLACEMENT", "Conflict of Interest Disclosure paragraph must be the last paragraph of the introduction (Section 1).")
            else:
                add("INFO", "CR-COI", "Conflict of Interest Disclosure present — please confirm with authors that it is accurate and necessary.")
        else:
            add("INFO", "CR-COI", "No Conflict of Interest Disclosure paragraph. This is only correct if no author has a financial conflict (e.g., evaluating an employer's model).")
        if re.search(r"arxiv", text, re.I) is None:
            pass

    # Captions: caption below for figures, title above for tables (heuristic)
    for env in ("figure", "table"):
        for m in re.finditer(r"\\\\begin\{%s\*?\}(.*?)\\\\end\{%s\*?\}" % (env, env), text, re.S):
            blk = m.group(1)
            cap = blk.find("\\caption")
            content_pos = [blk.find(k) for k in ("\\includegraphics", "\\begin{tikzpicture}", "\\begin{tabular", "\\resizebox", "\\begin{subfigure}") if blk.find(k) >= 0]
            if cap < 0 or not content_pos:
                continue
            first = min(content_pos)
            line_no = text[:m.start()].count("\n") + 1
            if env == "figure" and cap < first:
                add("WARN", "CAPTION-FIG-POSITION", f"Figure caption appears above the graphic (ICML requires: below). Around merged line {line_no}.")
            if env == "table" and cap > first:
                add("WARN", "CAPTION-TAB-POSITION", f"Table title appears below the table (ICML requires: above). Around merged line {line_no}.")

    # Style file integrity
    if args.pristine_sty:
        mains = [Path(r[0]).parent for r in rows[:1]]
        local = mains[0] / Path(args.pristine_sty).name if mains else None
        if local and local.exists():
            h1 = hashlib.sha256(Path(args.pristine_sty).read_bytes()).hexdigest()
            h2 = hashlib.sha256(local.read_bytes()).hexdigest()
            if h1 != h2:
                add("ERROR", "STY-MODIFIED", f"{local.name} does not match the official copy.")
            else:
                add("INFO", "STY-OK", f"{local.name} matches the official copy.")
    else:
        add("INFO", "STY-UNCHECKED", "Pass --pristine-sty with the path to the official icml20XX.sty to verify the style file has not been modified.")


# ----------------------------------------------------------------- PDF checks

def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return None


def check_pdf(pdf, args):
    pdf = Path(pdf)
    if not pdf.exists():
        add("ERROR", "PDF-MISSING", f"{pdf} not found")
        return
    size_mb = pdf.stat().st_size / 1e6
    limit = 20 if args.mode == "camera-ready" else 50
    add("ERROR" if size_mb > limit else "INFO", "PDF-SIZE", f"PDF is {size_mb:.1f} MB ({args.mode} limit {limit} MB).")

    if shutil.which("pdfinfo"):
        info = run(["pdfinfo", str(pdf)]) or ""
        ps = re.search(r"Page size:\s*([\d.]+) x ([\d.]+)", info)
        if ps:
            w, h = float(ps.group(1)), float(ps.group(2))
            if abs(w - 612) > 2 or abs(h - 792) > 2:
                add("ERROR", "PDF-PAGESIZE", f"Page size {w}x{h} pt is not US Letter (612x792).")
        au = re.search(r"^Author:[ \t]*(.*)$", info, re.M)
        if args.mode == "submission" and au and au.group(1).strip():
            add("ERROR", "ANON-PDFMETA", f"PDF metadata Author field is '{au.group(1).strip()}'.")
    else:
        add("INFO", "TOOL-MISSING", "pdfinfo not installed: page size and metadata not checked (please install poppler-utils).")

    if shutil.which("pdffonts"):
        fonts = run(["pdffonts", str(pdf)]) or ""
        if re.search(r"\bType 3\b", fonts):
            add("WARN", "PDF-TYPE3", "Type 3 fonts present (usually from images). ICML 2026 does not check Type 3, but vector PDF images with pdflatex are recommended.")
        if re.search(r"\bno\s+no\s+no\b", fonts):
            add("WARN", "PDF-UNEMBEDDED", "Some fonts appear unembedded.")

    if not shutil.which("pdftotext"):
        add("WARN", "TOOL-MISSING", "pdftotext not installed: skipping page-limit and broken-reference checks (please install poppler-utils).")
        return
    txt = run(["pdftotext", str(pdf), "-"]) or ""
    pages = txt.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]

    def real_lines(page):
        out = []
        for ln in page.splitlines():
            s = ln.strip()
            if not s or re.fullmatch(r"\d{1,3}", s):
                continue
            if re.search(r"Submission and Formatting Instructions|Under review by the International Conference", s):
                continue
            out.append(s)
        return out

    heading = re.compile(r"^(Acknowledg(e)?ments?|Impact Statement|Broader Impacts?( Statement)?|References)$")
    body_pages = None
    for i, pg in enumerate(pages, 1):
        lines = real_lines(pg)
        found = [(j, s) for j, s in enumerate(lines) if heading.match(s)]
        if found:
            # Two-column text extraction may place right-column headings before left-column text,
            # so use the position with the most text before the heading to determine the page.
            before = max(j for j, _ in found)
            body_pages = i if before > 3 else i - 1
            names = ", ".join(s for _, s in found)
            add("INFO", "PDF-BODY-END", f"Body-ending heading on page {i}: {names}. Body counted through page {body_pages}.")
            break
    limit_pages = args.page_limit or (9 if args.mode == "camera-ready" else 8)
    if body_pages is None:
        add("WARN", "PDF-BODY-UNKNOWN", "Cannot locate body end (References/Impact Statement heading not found).")
    elif body_pages > limit_pages:
        add("ERROR", "PDF-PAGE-LIMIT", f"Body appears to occupy {body_pages} pages; limit is {limit_pages} pages. (Heuristic: please visually confirm.)")
    else:
        add("INFO", "PDF-PAGE-LIMIT", f"Body is about {body_pages} pages (limit {limit_pages} pages). Total PDF pages: {len(pages)}.")

    for i, pg in enumerate(pages, 1):
        if "??" in pg:
            add("ERROR", "PDF-BROKEN-REF", f"Page {i} contains '??': unresolved \\ref or \\cite. Please rerun bibtex/latex.")
        if re.search(r"\(\?\s*,\s*\?\)|\(\?\)", pg):
            add("ERROR", "PDF-BROKEN-CITE", f"Page {i} contains unresolved citation '(?)'.")

    if args.mode == "submission":
        names = [n.strip() for n in (args.names or "").split(",") if n.strip()]
        affils = [a.strip() for a in (args.affils or "").split(",") if a.strip()]
        for nm in names + affils:
            hits = [i for i, pg in enumerate(pages, 1) if re.search(r"(?<![A-Za-z])" + re.escape(nm) + r"(?![A-Za-z])", pg, re.I if len(nm) > 4 else 0)]
            if hits:
                add("WARN", "ANON-PDF-NAME", f"'{nm}' appears on PDF pages {hits[:10]} (normal if only as third-person reference entries; otherwise a leak).")
        if any(re.search(r"Anonymous Authors", pg) for pg in pages[:1]) is False:
            add("WARN", "ANON-HEADER", "First page does not show 'Anonymous Authors' — please check that the author block is hidden.")
    else:
        if pages and re.search(r"Under review|Preliminary work|Anonymous Authors", pages[0]):
            add("ERROR", "CR-STILL-ANON", "First page still shows review-version notice or 'Anonymous Authors'.")


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", help="Main .tex file")
    ap.add_argument("--pdf", help="Compiled PDF")
    ap.add_argument("--mode", choices=["submission", "camera-ready"], default="submission")
    ap.add_argument("--names", help="Author names to search, comma-separated (anonymity check)")
    ap.add_argument("--affils", help="Affiliation/lab names to search, comma-separated")
    ap.add_argument("--position-track", action="store_true")
    ap.add_argument("--pristine-sty", help="Path to unmodified official icml20XX.sty")
    ap.add_argument("--page-limit", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.tex and not args.pdf:
        ap.error("Please provide --tex and/or --pdf")

    if args.tex:
        rows = load_tex(args.tex)
        if rows:
            check_tex(rows, args)
    if args.pdf:
        check_pdf(args.pdf, args)
    if args.mode == "submission" and not args.names:
        add("INFO", "ANON-NAMES-UNCHECKED", "Pass --names (and --affils) to search for identity leaks.")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    FINDINGS.sort(key=lambda f: order[f["level"]])
    if args.json:
        print(json.dumps(FINDINGS, indent=2))
    else:
        counts = {k: sum(f["level"] == k for f in FINDINGS) for k in order}
        print(f"ICML compliance check ({args.mode}): {counts['ERROR']} ERROR, {counts['WARN']} WARN, {counts['INFO']} INFO\n")
        for f in FINDINGS:
            where = f" [{f['loc']}]" if f["loc"] else ""
            print(f"{f['level']:5} {f['code']}{where}: {f['msg']}")
    sys.exit(1 if any(f["level"] == "ERROR" for f in FINDINGS) else 0)


if __name__ == "__main__":
    main()
