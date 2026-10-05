#!/usr/bin/env python3
"""从真实数据库查找论文并获取 BibTeX（绝不要凭记忆）。

子命令：
  search QUERY [--source dblp|s2|arxiv|all] [--year-from Y] [--limit N]
      搜索候选论文。打印标题、作者、会议、年份以及 `bibtex` 所需的 ID。
  bibtex (--dblp KEY | --doi DOI | --arxiv ID)
      从 DBLP、Crossref（通过 doi.org）或 arXiv 打印 BibTeX 记录。
  published TITLE
      对于 arXiv/CoRR 论文，查找标题匹配的正式发表版本。
  abstract (--arxiv ID | --s2 PAPER_ID | --doi DOI)
      打印摘要（用于确认论文确实如你引用它时所述）。

仅使用标准库。退出码 3 表示网络/数据库不可达：此时插入一个 PLACEHOLDER
引用并告知用户——绝不要凭记忆补全。
"""
import argparse
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "icml-cite-skill/1.0 (citation verification; mailto:unknown@example.com)"
TIMEOUT = 20


def get(url, accept=None, retries=2):
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and attempt < retries:
                time.sleep(3 * (attempt + 1)); continue
            if e.code == 404:
                return None
            break
        except Exception as e:  # 网络断开、DNS、代理
            last = e
            if attempt < retries:
                time.sleep(1); continue
    raise ConnectionError(f"{url}: {last}")


def sim(a, b):
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


# ---------------------------------------------------------------- 数据源

def dblp_search(q, limit=10):
    url = "https://dblp.org/search/publ/api?" + urllib.parse.urlencode({"q": q, "format": "json", "h": limit})
    data = json.loads(get(url) or "{}")
    hits = data.get("result", {}).get("hits", {}).get("hit", []) or []
    out = []
    for h in hits:
        info = h.get("info", {})
        au = info.get("authors", {}).get("author", [])
        au = au if isinstance(au, list) else [au]
        names = [a.get("text", "") if isinstance(a, dict) else str(a) for a in au]
        out.append({
            "source": "dblp", "title": info.get("title", "").rstrip("."), "authors": names,
            "venue": info.get("venue", ""), "year": info.get("year", ""),
            "ids": {"dblp": info.get("key", ""), "doi": info.get("doi", "")},
            "type": info.get("type", ""),
        })
    return out


def s2_search(q, limit=10, year_from=None):
    params = {"query": q, "limit": limit, "fields": "title,authors,year,venue,externalIds,publicationTypes"}
    if year_from:
        params["year"] = f"{year_from}-"
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(params)
    data = json.loads(get(url) or "{}")
    out = []
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        out.append({
            "source": "s2", "title": p.get("title", ""), "authors": [a.get("name", "") for a in p.get("authors", [])],
            "venue": p.get("venue", ""), "year": p.get("year", ""),
            "ids": {"s2": p.get("paperId", ""), "doi": ext.get("DOI", ""), "arxiv": ext.get("ArXiv", ""), "dblp": ext.get("DBLP", "")},
        })
    return out


def arxiv_search(q, limit=10):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": f"all:{q}", "max_results": limit})
    xml = get(url)
    if not xml:
        return []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", ns):
        aid = (e.findtext("a:id", "", ns) or "").rsplit("/abs/", 1)[-1]
        out.append({
            "source": "arxiv", "title": " ".join((e.findtext("a:title", "", ns) or "").split()),
            "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)],
            "venue": "arXiv", "year": (e.findtext("a:published", "", ns) or "")[:4],
            "ids": {"arxiv": re.sub(r"v\d+$", "", aid)},
            "abstract": " ".join((e.findtext("a:summary", "", ns) or "").split()),
        })
    return out


# ---------------------------------------------------------------- 命令

def show(results, year_from=None):
    if year_from:
        results = [r for r in results if not r["year"] or int(str(r["year"])[:4] or 0) >= year_from]
    if not results:
        print("无结果。尝试其他措辞、作者名或另一 --source。")
    for i, r in enumerate(results, 1):
        au = ", ".join(r["authors"][:4]) + (" et al." if len(r["authors"]) > 4 else "")
        ids = ", ".join(f"{k}={v}" for k, v in r["ids"].items() if v)
        print(f"{i:2}. [{r['source']}] {r['title']}\n    {au} | {r['venue']} {r['year']}\n    {ids}")


def cmd_search(a):
    res = []
    srcs = ["dblp", "s2"] if a.source == "all" else [a.source]
    errors = []
    for s in srcs:
        try:
            if s == "dblp":
                res += dblp_search(a.query, a.limit)
            elif s == "s2":
                res += s2_search(a.query, a.limit, a.year_from)
            elif s == "arxiv":
                res += arxiv_search(a.query, a.limit)
        except ConnectionError as e:
            errors.append(f"{s}: {e}")
    if errors and not res:
        print("数据库不可达——这**不是**论文不存在的证据。\n"
              "插入一个 PLACEHOLDER 引用，在 .icml/open_issues.md 中将其记录为 [cite]，并告知用户。\n"
              "绝不要凭记忆补全引用。")
        print("详情: " + "; ".join(errors), file=sys.stderr)
        sys.exit(3)
    show(res, a.year_from)
    if errors:
        print("\n部分不可达（结果可能不完整）: " + "; ".join(errors), file=sys.stderr)


def cmd_bibtex(a):
    try:
        if a.dblp:
            txt = get(f"https://dblp.org/rec/{a.dblp}.bib?param=1")
        elif a.doi:
            doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", a.doi)
            txt = get(f"https://doi.org/{urllib.parse.quote(doi)}", accept="application/x-bibtex; charset=utf-8")
        else:
            aid = re.sub(r"^arxiv:", "", a.arxiv, flags=re.I)
            txt = get(f"https://arxiv.org/bibtex/{aid}")
    except ConnectionError as e:
        print(f"不可达: {e}\n插入一个 PLACEHOLDER 引用并告知用户。", file=sys.stderr)
        sys.exit(3)
    if not txt or "@" not in txt:
        print("未找到该标识符的 BibTeX 记录。", file=sys.stderr)
        sys.exit(1)
    print(txt.strip())
    print("\n% 来源：数据库记录。允许的编辑：引用 key、用花括号保护标题大写字母、删除未使用的字段。", file=sys.stderr)


def cmd_published(a):
    try:
        cands = dblp_search(a.title, 15)
    except ConnectionError as e:
        print(f"不可达: {e}", file=sys.stderr); sys.exit(3)
    found = False
    for c in cands:
        s = sim(a.title, c["title"])
        venue = c["venue"] or ""
        is_preprint = venue.lower() in ("corr", "arxiv") or c["ids"]["dblp"].startswith("journals/corr")
        if s >= 0.9 and not is_preprint:
            found = True
            print(f"已发表: {c['title']} | {venue} {c['year']} | dblp={c['ids']['dblp']} doi={c['ids']['doi']} (标题相似度 {s:.2f})")
    if not found:
        print("在 DBLP 上未找到标题匹配的正式发表版本。请检查标题是否被重命名 "
              "（正式发表版本经常更改标题）、作者主页或 OpenReview。")


def cmd_abstract(a):
    try:
        if a.arxiv:
            url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": a.arxiv})
            xml = get(url)
            ns = {"a": "http://www.w3.org/2005/Atom"}
            e = ET.fromstring(xml).find("a:entry", ns)
            print(" ".join((e.findtext("a:summary", "", ns) or "").split()) if e is not None else "未找到")
        else:
            pid = a.s2 if a.s2 else f"DOI:{a.doi}"
            data = json.loads(get(f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(pid)}?fields=title,abstract,year,venue") or "{}")
            print(f"{data.get('title')} ({data.get('venue')} {data.get('year')})\n\n{data.get('abstract') or 'Semantic Scholar 未提供摘要。'}")
    except ConnectionError as e:
        print(f"不可达: {e}", file=sys.stderr); sys.exit(3)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--source", default="all", choices=["dblp", "s2", "arxiv", "all"])
    s.add_argument("--year-from", type=int); s.add_argument("--limit", type=int, default=8)
    b = sub.add_parser("bibtex"); g = b.add_mutually_exclusive_group(required=True)
    g.add_argument("--dblp"); g.add_argument("--doi"); g.add_argument("--arxiv")
    p = sub.add_parser("published"); p.add_argument("title")
    ab = sub.add_parser("abstract"); g2 = ab.add_mutually_exclusive_group(required=True)
    g2.add_argument("--arxiv"); g2.add_argument("--s2"); g2.add_argument("--doi")
    a = ap.parse_args()
    {"search": cmd_search, "bibtex": cmd_bibtex, "published": cmd_published, "abstract": cmd_abstract}[a.cmd](a)


if __name__ == "__main__":
    main()
