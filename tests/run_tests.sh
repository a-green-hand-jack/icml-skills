#!/usr/bin/env bash
# skill 脚本的回归测试。需要 python3；pdflatex + bibtex + poppler-utils
# 用于 PDF 部分（缺失则跳过）。使用 STUB icml2026.sty —— 切勿用于正式论文。
set -u
cd "$(dirname "$0")"; ROOT=$(cd .. && pwd); W=$(mktemp -d); PASS=0; FAIL=0
ok(){ echo "PASS  $1"; PASS=$((PASS+1)); }; bad(){ echo "FAIL  $1"; FAIL=$((FAIL+1)); }
expect(){ # 名称, 预期退出码 (0/1/nonzero), 命令...
  local name=$1 want=$2; shift 2; out=$("$@" 2>&1); code=$?
  if [ "$want" = nonzero ] && [ $code -ne 0 ] || [ "$want" = "$code" ]; then ok "$name"; else bad "$name (exit $code)"; echo "$out" | head -20; fi; }
contains(){ if echo "$out" | grep -q -- "$2"; then ok "$1"; else bad "$1 (missing '$2')"; fi; }

for d in planted clean; do
  cp -r fixtures/$d "$W/$d"; cp "$(kpsewhich plainnat.bst 2>/dev/null || echo /dev/null)" "$W/$d/icml2026.bst" 2>/dev/null
  python3 "$ROOT/icml-write/scripts/init_workspace.py" --root "$W/$d" >/dev/null
  cat "$W/$d/ledger_rows.md" >> "$W/$d/.icml/claims.md"
  if command -v pdflatex >/dev/null; then (cd "$W/$d" && pdflatex -interaction=nonstopmode main.tex >/dev/null; bibtex main >/dev/null; pdflatex -interaction=nonstopmode main.tex >/dev/null; pdflatex -interaction=nonstopmode main.tex >/dev/null); fi
done
P=$W/planted; C=$W/clean; PDFP=""; PDFC=""
[ -f "$P/main.pdf" ] && PDFP="--pdf $P/main.pdf"; [ -f "$C/main.pdf" ] && PDFC="--pdf $C/main.pdf"

expect "提交检查：标记预埋论文" 1 python3 "$ROOT/icml-review/scripts/check_submission.py" --tex "$P/main.tex" $PDFP --names "Jane Doe" --affils "MIT"
for code in HIDDEN-TEXT INJECTION-PHRASE ABSTRACT-PARAGRAPHS IMPACT-MISSING ACK-IN-SUBMISSION ANON-NAME ANON-URL ANON-PDFMETA ANON-SELFREF LAYOUT-HACK CAPTION-FIG-POSITION; do contains "  检测到 $code" "$code"; done
[ -n "$PDFP" ] && contains "  检测到 PDF-BROKEN-REF" "PDF-BROKEN-REF"
expect "提交检查：通过干净论文" 0 python3 "$ROOT/icml-review/scripts/check_submission.py" --tex "$C/main.tex" $PDFC --names "Jane Doe" --affils "MIT"
expect "camera-ready 检查：标记匿名版本" 1 python3 "$ROOT/icml-camera-ready/scripts/check_submission.py" --tex "$C/main.tex" --mode camera-ready
contains "  检测到 STYLE-NOT-ACCEPTED" "STYLE-NOT-ACCEPTED"
expect "数字：预埋论文有未匹配/未验证项" 1 python3 "$ROOT/icml-write/scripts/check_numbers.py" "$P/main.tex" --ledger "$P/.icml/claims.md"
contains "  找到派生数字 1.8" "1.8"
expect "数字：干净论文全部匹配" 0 python3 "$ROOT/icml-write/scripts/check_numbers.py" "$C/main.tex" --ledger "$C/.icml/claims.md"
expect "大纲检查运行" 0 python3 "$ROOT/icml-write/scripts/extract_outline.py" "$P/main.tex"
contains "  标记缺少 TL;DR" "NO TL;DR"; contains "  标记孤立 TL;DR" "ORPHAN"
expect "lint：在预埋论文上运行" 0 python3 "$ROOT/icml-write/scripts/lint_prose.py" "$P/main.tex" --summary
for r in llm-tell anthropomorphism future generic-opener cite-plain; do contains "  lint 规则 $r" "\[$r\]"; done
expect "lint：干净论文无命中" 0 python3 "$ROOT/icml-write/scripts/lint_prose.py" "$C/main.tex" --summary
contains "  零命中" "0 hits"
expect "bib：预埋论文有缺失 key" 1 python3 "$ROOT/icml-cite/scripts/check_bib.py" "$P/main.tex" "$P/refs.bib"
contains "  发现重复" "Probable duplicate"; contains "  发现未保护的大写" "BERT"
expect "bib：干净论文通过" 0 python3 "$ROOT/icml-cite/scripts/check_bib.py" "$C/main.tex" "$C/refs.bib"
expect "rebuttal 检查：标记预埋回复" 1 python3 "$ROOT/icml-rebuttal/scripts/check_rebuttal.py" "$P/rebuttal_R-abcd.md" --names "Jane Doe" --ledger "$P/.icml/claims.md"
for k in "shortened URL" "Identity string" "Combative" "change the score" "Promise without content" "88.7"; do contains "  rebuttal: $k" "$k"; done

echo; echo "$PASS 通过, $FAIL 失败"; rm -rf "$W"; [ $FAIL -eq 0 ]
