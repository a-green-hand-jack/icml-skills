# Compliance Checks: Meaning, Fixes, and Manual Checklist Items

`check_submission.py` codes and their meanings. Severity levels in the script are defaults;
a human may waive a WARN with justification (recorded in `decisions.md`).

| Code | Meaning | Fix |
|---|---|---|
| STYLE-MISSING / STYLE-ACCEPTED-IN-SUBMISSION / STYLE-NOT-ACCEPTED | Incorrect ICML style package usage | Use `\usepackage{icml20XX}` for submission, `[accepted]` for camera-ready |
| PAPER-A4, PDF-PAGESIZE | Not US Letter | Remove a4paper; recompile |
| LAYOUT-HACK | Template spacing/layout was modified | Remove it; cut text instead. Modifying the template is grounds for rejection |
| HIDDEN-TEXT, INJECTION-PHRASE | Invisible or reviewer/LLM-targeted text | Remove completely. Prompt injection = desk reject |
| PLACEHOLDER | Remaining TODO/TBD/placeholder citation | Resolve or remove |
| ABSTRACT-PARAGRAPHS / ABSTRACT-SENTENCES | Abstract is not one paragraph / not about 4–6 sentences | Merge; condense |
| TITLE-ALLCAPS / TITLE-CASE | Title capitalization | Capitalize content words only |
| IMPACT-MISSING / IMPACT-AFTER-REFS / IMPACT-IN-APPENDIX / IMPACT-NUMBERED | Impact statement missing or misplaced | Use unnumbered `\section*{Impact Statement}` before the references |
| POSITION-ALT-VIEWS | Position paper track missing "Alternative Views" | Add that section in the main text |
| ACK-IN-SUBMISSION | Acknowledgments appear in the anonymous version | Remove before camera-ready |
| ANON-NAME / ANON-PDF-NAME | Author/affiliation strings appear in the text | Remove or rephrase; hits in third-party citation entries are acceptable |
| ANON-SELFREF | "Our previous work" style self-citation | Rewrite in the third person |
| ANON-URL | Non-anonymous URL (GitHub, personal homepage, short link) | Replace with an anonymous repository (e.g., anonymous.4open.science) or supplementary material upload |
| ANON-FUNDING | Funding/grant text | Remove before camera-ready |
| ANON-PDFMETA | Author in PDF metadata | Remove `pdfauthor`, clear metadata; also check figure PDFs |
| ANON-HEADER | Anonymous author block not shown on the first page | Check style options and `\icmlauthor` usage |
| BIB-MISSING / BIBSTYLE | Missing references or wrong style | `\bibliographystyle{icml20XX}` + natbib |
| CAPTION-FIG-POSITION / CAPTION-TAB-POSITION | Caption placement | Figures: caption below. Tables: caption above |
| STY-MODIFIED | Style file differs from the official version | Restore the official file |
| PDF-PAGE-LIMIT | Main text exceeds the page limit (heuristic) | Visually confirm; trim |
| PDF-BROKEN-REF / PDF-BROKEN-CITE | `??` or `(?)` | Fix label/key; rerun bibtex and latex twice |
| PDF-SIZE | Exceeds file size limit | Compress raster images; prefer vector graphics |
| PDF-TYPE3 / PDF-UNEMBEDDED | Font issues | Use pdflatex; export figures as PDF with embedded fonts |
| CR-* | Camera-ready specific | See icml-camera-ready |

## Manual Checks the Script Cannot Perform

Anonymity
- Open every figure file: axis labels, watermarks, file paths, user names, institutional
  logos, dataset names unique to the author's lab, screenshots showing names.
- Figure and image file metadata (PDF Author/Creator, EXIF in PNG/JPG).
- Supplementary code: author names in headers, LICENSE files, `.git` directories,
  absolute paths (`/home/<user>/`), cluster or bucket names, wandb/HF usernames,
  notebook outputs showing paths. Anonymous GitHub links must be in a single text file inside the zip,
  on a branch frozen after the deadline.
- Self-references are written in the third person and do not suspiciously over-appear.
- No linked material mentions that the paper is an ICML submission.

Content
- Everything reviewers need to judge correctness is within the first 8 pages.
- OpenReview abstract and title match the PDF.
- If the work carries specific risks, the impact statement should not be mere boilerplate.
- Significant use of LLMs in the research methodology should be disclosed (ICML encourages this).
- Dual submission: no substantially similar version is under review elsewhere.

Formatting
- No text extends beyond the margins; no wide content overflows the column (check equations and tables).
- Figures and tables are legible at print size and in grayscale.
- At most three heading levels; headings use title case.
