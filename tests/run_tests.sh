#!/usr/bin/env bash
# Regression tests for skill scripts. Requires python3; pdflatex + bibtex + poppler-utils
# for the PDF portion (skipped if missing). Uses a STUB icml2026.sty — NEVER use for a real paper.
set -u
cd "$(dirname "$0")"; ROOT=$(cd .. && pwd); W=$(mktemp -d); PASS=0; FAIL=0
ok(){ echo "PASS  $1"; PASS=$((PASS+1)); }; bad(){ echo "FAIL  $1"; FAIL=$((FAIL+1)); }
expect(){ # name, expected exit code (0/1/nonzero), command...
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

expect "submission check: flag planted paper" 1 python3 "$ROOT/icml-review/scripts/check_submission.py" --tex "$P/main.tex" $PDFP --names "Jane Doe" --affils "MIT"
for code in HIDDEN-TEXT INJECTION-PHRASE ABSTRACT-PARAGRAPHS IMPACT-MISSING ACK-IN-SUBMISSION ANON-NAME ANON-URL ANON-PDFMETA ANON-SELFREF LAYOUT-HACK CAPTION-FIG-POSITION; do contains "  detected $code" "$code"; done
[ -n "$PDFP" ] && contains "  detected PDF-BROKEN-REF" "PDF-BROKEN-REF"
expect "submission check: pass clean paper" 0 python3 "$ROOT/icml-review/scripts/check_submission.py" --tex "$C/main.tex" $PDFC --names "Jane Doe" --affils "MIT"
expect "camera-ready check: flag anonymous version" 1 python3 "$ROOT/icml-camera-ready/scripts/check_submission.py" --tex "$C/main.tex" --mode camera-ready
contains "  detected STYLE-NOT-ACCEPTED" "STYLE-NOT-ACCEPTED"
expect "numbers: planted paper has unmatched/unverified items" 1 python3 "$ROOT/icml-write/scripts/check_numbers.py" "$P/main.tex" --ledger "$P/.icml/claims.md"
contains "  found derived number 1.8" "1.8"
expect "numbers: clean paper fully matches" 0 python3 "$ROOT/icml-write/scripts/check_numbers.py" "$C/main.tex" --ledger "$C/.icml/claims.md"
expect "outline check runs" 0 python3 "$ROOT/icml-write/scripts/extract_outline.py" "$P/main.tex"
contains "  flagged missing TL;DR" "NO TL;DR"; contains "  flagged orphan TL;DR" "ORPHAN"
expect "lint: run on planted paper" 0 python3 "$ROOT/icml-write/scripts/lint_prose.py" "$P/main.tex" --summary
for r in llm-tell anthropomorphism future generic-opener cite-plain; do contains "  lint rule $r" "\[$r\]"; done
expect "lint: clean paper has no hits" 0 python3 "$ROOT/icml-write/scripts/lint_prose.py" "$C/main.tex" --summary
contains "  zero hits" "0 hits"
expect "bib: planted paper has missing key" 1 python3 "$ROOT/icml-cite/scripts/check_bib.py" "$P/main.tex" "$P/refs.bib"
contains "  found duplicate" "Probable duplicate"; contains "  found unprotected uppercase" "BERT"
expect "bib: clean paper passes" 0 python3 "$ROOT/icml-cite/scripts/check_bib.py" "$C/main.tex" "$C/refs.bib"
expect "rebuttal check: flag planted response" 1 python3 "$ROOT/icml-rebuttal/scripts/check_rebuttal.py" "$P/rebuttal_R-abcd.md" --names "Jane Doe" --ledger "$P/.icml/claims.md"
for k in "shortened URL" "Identity string" "Combative" "change the score" "Promise without content" "88.7"; do contains "  rebuttal: $k" "$k"; done

echo; echo "$PASS passed, $FAIL failed"; rm -rf "$W"; [ $FAIL -eq 0 ]
