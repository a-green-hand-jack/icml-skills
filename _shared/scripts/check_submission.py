#!/usr/bin/env python3
"""对 ICML 论文进行机械合规性检查（LaTeX 源文件和/或编译后的 PDF）。

检查均为启发式：每条 ERROR 必须修正或由人类明确豁免；
每条 WARN 必须查看。未发现异常不等于合规证明 ——
官方 ICML 论文检查器和人工审读仍是必需的。

用法：
    python check_submission.py --tex main.tex [--pdf main.pdf] [--mode submission|camera-ready]
                               [--names "Jane Doe,John Roe"] [--affils "MIT,Acme Corp"]
                               [--position-track] [--pristine-sty path/to/official/icml2026.sty]
                               [--page-limit N] [--json]

退出码：0 = 无 ERROR 发现，1 = 至少一条 ERROR，2 = 用法错误。
仅使用 Python 标准库；当 poppler 工具（pdftotext、pdfinfo、
pdffonts）已安装时会使用它们，缺失时会提示。
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


# ----------------------------------------------------------------- LaTeX 加载

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
    """返回 (path, lineno, text_without_comment) 列表，追踪 \\input/\\include。"""
    seen = seen or set()
    main = Path(main)
    if not main.suffix:
        main = main.with_suffix(".tex")
    if not main.exists() or main.resolve() in seen:
        if not main.exists():
            add("WARN", "TEX-MISSING-INPUT", f"找不到输入文件 {main}")
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


# ----------------------------------------------------------------- TeX 检查

def check_tex(rows, args):
    text = "\n".join(r[2] for r in rows)
    mode = args.mode

    # 样式选项
    m = re.search(r"\\\\usepackage(\[[^\]]*\])?\{icml20\d\d\}", text)
    if not m:
        add("ERROR", "STYLE-MISSING", "未找到 \\usepackage{icml20XX}。官方 ICML 样式文件是强制的。")
    else:
        opts = m.group(1) or ""
        if mode == "submission" and "accepted" in opts:
            add("ERROR", "STYLE-ACCEPTED-IN-SUBMISSION", "设置了 'accepted' 选项：作者姓名将被打印。投稿前请移除。")
        if mode == "camera-ready" and "accepted" not in opts:
            add("ERROR", "STYLE-NOT-ACCEPTED", "最终稿必须使用 \\usepackage[accepted]{icml20XX}。")
    if re.search(r"\\\\documentclass\[[^\]]*a4paper", text) or "a4paper" in text:
        add("ERROR", "PAPER-A4", "发现 a4paper；ICML 要求 US Letter。")

    # 间距 / 版式 hack
    hacks = [
        (r"\\\\vspace\*?\{\s*-", "negative \\vspace"),
        (r"\\\\setlength\{\\\\(textheight|textwidth|columnsep|topmargin|oddsidemargin|evensidemargin|baselineskip|parskip|abovedisplayskip|belowdisplayskip|textfloatsep|floatsep|intextsep|abovecaptionskip|belowcaptionskip)\}", "\\setlength 修改版式长度"),
        (r"\\\\addtolength\{\\\\(textheight|textwidth|columnsep|topmargin)\}", "\\addtolength 修改版式长度"),
        (r"\\\\linespread\{", "\\linespread"),
        (r"\\\\renewcommand\{?\\\\baselinestretch", "\\baselinestretch"),
        (r"\\\\titlespacing", "\\titlespacing"),
        (r"\\\\usepackage(\[[^\]]*\])?\{(geometry|savetrees|titlesec|setspace)\}", "修改版式的宏包"),
    ]
    for r in rows:
        for pat, what in hacks:
            if re.search(pat, r[2]):
                lvl = "ERROR" if "版式" in what or "baselinestretch" in what or "linespread" in what else "WARN"
                add(lvl, "LAYOUT-HACK", f"{what}：ICML 禁止改动模板或压缩垂直间距。", loc(r))

    # 隐藏 / 面向审稿人的文本（提示注入风险）
    hidden = [
        (r"\\\\(text)?color\{\s*white\s*\}", "白色文本"),
        (r"\\\\color\[[^\]]*\]\{[^}]*\}\{?\s*1\s*,\s*1\s*,\s*1", "白色（RGB 1,1,1）文本"),
        (r"\\\\fontsize\{\s*0*(\.\d+|[0-3](\.\d+)?)\s*(pt)?\s*\}", "字号小于 4pt"),
        (r"\\\\scalebox\{\s*0*\.0\d", "接近零的 \\scalebox"),
        (r"\\\\phantom\{[^}]{20,}\}", "长 \\phantom 文本"),
    ]
    for r in rows:
        for pat, what in hidden:
            if re.search(pat, r[2]):
                add("ERROR", "HIDDEN-TEXT", f"{what}：不可见文本可被视作提示注入（直接拒稿）。请移除。", loc(r))
        if re.search(r"(?i)(ignore (all |any )?(previous|prior) instructions|as an? (ai|llm|language model) review|give (this paper )?a (high|positive) (score|rating)|reviewer.{0,20}(llm|ai|gpt))", r[2]):
            add("ERROR", "INJECTION-PHRASE", "文本指向 LLM 审稿人。提示注入被禁止。", loc(r))

    # 残留占位符
    for r in rows:
        if re.search(r"(\\\\todo\b|\bTODO\b|\bTBD\b|\bXXX\b|PLACEHOLDER|CITATION NEEDED|\?\?\?)", r[2]):
            add("ERROR" if mode == "camera-ready" else "WARN", "PLACEHOLDER", "未解决的占位符/TODO。", loc(r))

    # 摘要
    am = re.search(r"\\\\begin\{abstract\}(.*?)\\\\end\{abstract\}", text, re.S)
    if not am:
        add("ERROR", "ABSTRACT-MISSING", "未找到 abstract 环境。")
    else:
        body = am.group(1).strip()
        if re.search(r"\n\s*\n", body) or "\\par" in body:
            add("ERROR", "ABSTRACT-PARAGRAPHS", "摘要必须为单段。")
        plain = re.sub(r"\\\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", body)
        plain = re.sub(r"\b(e\.g|i\.e|et al|cf|vs|resp|approx|Fig|Sec|Eq|Tab)\.", "ABBR", plain)
        plain = re.sub(r"(\d)\.(\d)", r"\1DOT\2", plain)
        sents = [s for s in re.split(r"(?<=[.!?])\s+", plain.strip()) if len(s.split()) >= 3]
        n = len(sents)
        words = len(plain.split())
        if n < 4 or n > 6:
            add("WARN" if n <= 8 else "ERROR", "ABSTRACT-SENTENCES", f"摘要约 {n} 句（{words} 词）；ICML 建议 4–6 句。")
        else:
            add("INFO", "ABSTRACT-SENTENCES", f"摘要约 {n} 句（{words} 词）。")

    # 标题大小写
    tm = re.search(r"\\\\icmltitle\{(.+?)\}\s*$", text, re.M)
    if tm:
        title = re.sub(r"\\\\[a-zA-Z]+|[{}$]", "", tm.group(1))
        letters = re.sub(r"[^A-Za-z]", "", title)
        if letters and letters.isupper() and len(letters) > 12:
            add("ERROR", "TITLE-ALLCAPS", "标题为全大写；仅实义词首字母大写。")
        small = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "of", "in", "on", "at", "to", "by", "up", "as", "via", "with", "from", "into", "over", "is", "vs"}
        bad = [w for w in title.split()[1:] if w.isalpha() and w[0].islower() and w.lower() not in small]
        if bad:
            add("WARN", "TITLE-CASE", f"标题中可能需要大写的词：{', '.join(bad[:8])}")

    # 必需 / 禁止章节
    impact = re.search(r"\\\\section\*?\{\s*(Impact Statement|Broader Impact[s]?( Statement)?)\s*\}", text, re.I)
    ack = re.search(r"\\\\section\*?\{\s*Acknowledg(e)?ments?\s*\}", text, re.I)
    bib = re.search(r"\\\\bibliography\{|\\\\begin\{thebibliography\}|\\\\printbibliography", text)
    if args.position_track:
        if not re.search(r"\\\\section\*?\{[^}]*Alternative Views?[^}]*\}", text, re.I):
            add("ERROR", "POSITION-ALT-VIEWS", "立场论文赛道要求在正文中包含 'Alternative Views' 章节。")
    else:
        if not impact:
            add("ERROR", "IMPACT-MISSING", "主赛道论文要求在参考文献前有一个无编号的 'Impact Statement' 章节。")
        else:
            if not impact.group(0).startswith("\\\\section*"):
                add("WARN", "IMPACT-NUMBERED", "影响声明应为无编号章节（\\section*）。")
            if bib and impact.start() > bib.start():
                add("ERROR", "IMPACT-AFTER-REFS", "影响声明必须出现在参考文献之前。")
            app = re.search(r"\\\\appendix", text)
            if app and impact.start() > app.start():
                add("ERROR", "IMPACT-IN-APPENDIX", "影响声明必须出现在参考文献之前，不能在附录中。")
    if ack and mode == "submission":
        add("ERROR", "ACK-IN-SUBMISSION", "匿名投稿中不允许出现致谢。")
    if not bib:
        add("WARN", "BIB-MISSING", "未找到 bibliography 命令。")
    else:
        if not re.search(r"\\\\bibliographystyle\{icml20\d\d\}", text):
            add("WARN", "BIBSTYLE", "预期使用 \\bibliographystyle{icml20XX}（通过 natbib 的 APA 作者–年份格式）。")

    # 匿名性
    if mode == "submission":
        names = [n.strip() for n in (args.names or "").split(",") if n.strip()]
        affils = [a.strip() for a in (args.affils or "").split(",") if a.strip()]
        body_rows = [r for r in rows if not re.search(r"\\\\icml(author|affiliation|correspondingauthor)\b", r[2])]
        for r in body_rows:
            for nm in names + affils:
                if nm and re.search(r"(?<![A-Za-z])" + re.escape(nm) + r"(?![A-Za-z])", r[2], re.I if len(nm) > 4 else 0):
                    add("ERROR", "ANON-NAME", f"'{nm}' 出现在正文中（隐藏作者块之外）。", loc(r))
            if re.search(r"(?i)\b(our|we) (own )?(previous|prior|earlier|recent) (work|paper|study|studies|method)\b|\bin our (previous|prior|earlier) ", r[2]):
                add("WARN", "ANON-SELFREF", "可能以第一人称引用自己先前的工作；请以第三人称引用。", loc(r))
            for u in re.findall(r"https?://[^\s}\]+", r[2]):
                if re.search(r"anonymous\.4open\.science|openreview\.net|arxiv\.org|doi\.org", u):
                    continue
                lvl = "ERROR" if re.search(r"github\.com|gitlab|huggingface\.co/(?!datasets/|models?/)|bit\.ly|tinyurl|goo\.gl|t\.co/|\.edu/~|sites\.google", u) else "WARN"
                add(lvl, "ANON-URL", f"URL 可能暴露身份或非匿名：{u}", loc(r))
            if re.search(r"\\\\thanks\{|grant (no\.|number)|funded by|supported by (the )?(NSF|NIH|ERC|DARPA|NSFC)", r[2], re.I):
                add("WARN", "ANON-FUNDING", "投稿中出现资助/拨款文本会暴露身份；请在最终稿阶段再添加。", loc(r))
        hs = re.search(r"pdfauthor\s*=\s*\{?([^,}\n]+)", text)
        if hs and hs.group(1).strip():
            add("ERROR", "ANON-PDFMETA", f"hyperref pdfauthor 已设置（'{hs.group(1).strip()}'）：这会泄漏到 PDF 元数据中。")
    else:
        if not re.search(r"\\\\printAffiliationsAndNotice", text):
            add("ERROR", "CR-AFFIL-NOTICE", "最终稿必须调用 \\printAffiliationsAndNotice{}（或 {\\icmlEqualContribution}）。")
        if re.search(r"Anonymous (Author|Institution)", text):
            add("ERROR", "CR-ANON-LEFTOVER", "残留占位符 'Anonymous' 作者/单位文本。")
        coi = re.search(r"Conflict of Interest Disclosure", text)
        if coi:
            secs = [m.start() for m in re.finditer(r"\\\\section\{", text)]
            if len(secs) >= 2 and coi.start() > secs[1]:
                add("ERROR", "CR-COI-PLACEMENT", "利益冲突披露段落必须是引言（第一节）的最后一段。")
            else:
                add("INFO", "CR-COI", "存在利益冲突披露 — 请与作者确认其准确且必要。")
        else:
            add("INFO", "CR-COI", "无利益冲突披露段落。仅在无任何作者存在财务冲突（例如评估雇主模型）时才正确。")
        if re.search(r"arxiv", text, re.I) is None:
            pass

    # 图注：图注在下方，表题在上方（启发式）
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
                add("WARN", "CAPTION-FIG-POSITION", f"图注出现在图形上方（ICML 要求：下方）。约在合并行 {line_no}。")
            if env == "table" and cap > first:
                add("WARN", "CAPTION-TAB-POSITION", f"表题出现在表格下方（ICML 要求：上方）。约在合并行 {line_no}。")

    # 样式文件完整性
    if args.pristine_sty:
        mains = [Path(r[0]).parent for r in rows[:1]]
        local = mains[0] / Path(args.pristine_sty).name if mains else None
        if local and local.exists():
            h1 = hashlib.sha256(Path(args.pristine_sty).read_bytes()).hexdigest()
            h2 = hashlib.sha256(local.read_bytes()).hexdigest()
            if h1 != h2:
                add("ERROR", "STY-MODIFIED", f"{local.name} 与官方副本不一致。")
            else:
                add("INFO", "STY-OK", f"{local.name} 与官方副本一致。")
    else:
        add("INFO", "STY-UNCHECKED", "传入 --pristine-sty 并指定官方 icml20XX.sty 的路径，以验证样式文件未被修改。")


# ----------------------------------------------------------------- PDF 检查

def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return None


def check_pdf(pdf, args):
    pdf = Path(pdf)
    if not pdf.exists():
        add("ERROR", "PDF-MISSING", f"{pdf} 未找到")
        return
    size_mb = pdf.stat().st_size / 1e6
    limit = 20 if args.mode == "camera-ready" else 50
    add("ERROR" if size_mb > limit else "INFO", "PDF-SIZE", f"PDF 为 {size_mb:.1f} MB（{args.mode} 限制 {limit} MB）。")

    if shutil.which("pdfinfo"):
        info = run(["pdfinfo", str(pdf)]) or ""
        ps = re.search(r"Page size:\s*([\d.]+) x ([\d.]+)", info)
        if ps:
            w, h = float(ps.group(1)), float(ps.group(2))
            if abs(w - 612) > 2 or abs(h - 792) > 2:
                add("ERROR", "PDF-PAGESIZE", f"页面尺寸 {w}x{h} pt 不是 US Letter（612x792）。")
        au = re.search(r"^Author:[ \t]*(.*)$", info, re.M)
        if args.mode == "submission" and au and au.group(1).strip():
            add("ERROR", "ANON-PDFMETA", f"PDF 元数据 Author 字段为 '{au.group(1).strip()}'。")
    else:
        add("INFO", "TOOL-MISSING", "pdfinfo 未安装：未检查页面尺寸与元数据（请安装 poppler-utils）。")

    if shutil.which("pdffonts"):
        fonts = run(["pdffonts", str(pdf)]) or ""
        if re.search(r"\bType 3\b", fonts):
            add("WARN", "PDF-TYPE3", "存在 Type 3 字体（通常来自图片）。ICML 2026 无 Type 3 检查，但建议使用 pdflatex 的矢量 PDF 图片。")
        if re.search(r"\bno\s+no\s+no\b", fonts):
            add("WARN", "PDF-UNEMBEDDED", "部分字体似乎未嵌入。")

    if not shutil.which("pdftotext"):
        add("WARN", "TOOL-MISSING", "pdftotext 未安装：跳过页数限制与损坏引用检查（请安装 poppler-utils）。")
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
            # 双栏文本提取可能将右栏标题放在左栏文本之前，
            # 因此以标题前文本最多的位置判断页面。
            before = max(j for j, _ in found)
            body_pages = i if before > 3 else i - 1
            names = ", ".join(s for _, s in found)
            add("INFO", "PDF-BODY-END", f"第 {i} 页出现正文结束标题：{names}。正文计至第 {body_pages} 页。")
            break
    limit_pages = args.page_limit or (9 if args.mode == "camera-ready" else 8)
    if body_pages is None:
        add("WARN", "PDF-BODY-UNKNOWN", "无法定位正文结束位置（未找到 References/Impact Statement 标题）。")
    elif body_pages > limit_pages:
        add("ERROR", "PDF-PAGE-LIMIT", f"正文似乎占 {body_pages} 页；限制为 {limit_pages} 页。（启发式：请目视确认。）")
    else:
        add("INFO", "PDF-PAGE-LIMIT", f"正文约 {body_pages} 页（限制 {limit_pages} 页）。PDF 总页数：{len(pages)}。")

    for i, pg in enumerate(pages, 1):
        if "??" in pg:
            add("ERROR", "PDF-BROKEN-REF", f"第 {i} 页出现 '??'：未解析的 \\ref 或 \\cite。请重新运行 bibtex/latex。")
        if re.search(r"\(\?\s*,\s*\?\)|\(\?\)", pg):
            add("ERROR", "PDF-BROKEN-CITE", f"第 {i} 页出现未解析引用 '(?)'。")

    if args.mode == "submission":
        names = [n.strip() for n in (args.names or "").split(",") if n.strip()]
        affils = [a.strip() for a in (args.affils or "").split(",") if a.strip()]
        for nm in names + affils:
            hits = [i for i, pg in enumerate(pages, 1) if re.search(r"(?<![A-Za-z])" + re.escape(nm) + r"(?![A-Za-z])", pg, re.I if len(nm) > 4 else 0)]
            if hits:
                add("WARN", "ANON-PDF-NAME", f"'{nm}' 出现在 PDF 文本的第 {hits[:10]} 页（若仅作为第三人称参考文献条目则正常；否则为泄漏）。")
        if any(re.search(r"Anonymous Authors", pg) for pg in pages[:1]) is False:
            add("WARN", "ANON-HEADER", "首页未显示 'Anonymous Authors' — 请检查作者块是否已隐藏。")
    else:
        if pages and re.search(r"Under review|Preliminary work|Anonymous Authors", pages[0]):
            add("ERROR", "CR-STILL-ANON", "首页仍显示审稿版本通知或 'Anonymous Authors'。")


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", help="主 .tex 文件")
    ap.add_argument("--pdf", help="编译后的 PDF")
    ap.add_argument("--mode", choices=["submission", "camera-ready"], default="submission")
    ap.add_argument("--names", help="待搜索的作者姓名，逗号分隔（匿名性检查）")
    ap.add_argument("--affils", help="待搜索的单位/实验室名称，逗号分隔")
    ap.add_argument("--position-track", action="store_true")
    ap.add_argument("--pristine-sty", help="未改动的官方 icml20XX.sty 路径")
    ap.add_argument("--page-limit", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.tex and not args.pdf:
        ap.error("请提供 --tex 和/或 --pdf")

    if args.tex:
        rows = load_tex(args.tex)
        if rows:
            check_tex(rows, args)
    if args.pdf:
        check_pdf(args.pdf, args)
    if args.mode == "submission" and not args.names:
        add("INFO", "ANON-NAMES-UNCHECKED", "传入 --names（和 --affils）以搜索身份泄漏。")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    FINDINGS.sort(key=lambda f: order[f["level"]])
    if args.json:
        print(json.dumps(FINDINGS, indent=2))
    else:
        counts = {k: sum(f["level"] == k for f in FINDINGS) for k in order}
        print(f"ICML 合规检查（{args.mode}）：{counts['ERROR']} ERROR，{counts['WARN']} WARN，{counts['INFO']} INFO\n")
        for f in FINDINGS:
            where = f" [{f['loc']}]" if f["loc"] else ""
            print(f"{f['level']:5} {f['code']}{where}: {f['msg']}")
    sys.exit(1 if any(f["level"] == "ERROR" for f in FINDINGS) else 0)


if __name__ == "__main__":
    main()
