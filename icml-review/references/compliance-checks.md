# Compliance Checks: Meaning, Fixes, and Manual Checks

`check_submission.py` codes and what to do. Severity in the script is a default; a
human may waive a WARN with a reason (log it in `decisions.md`).

| Code | Meaning | Fix |
|---|---|---|
| STYLE-MISSING / STYLE-ACCEPTED-IN-SUBMISSION / STYLE-NOT-ACCEPTED | Wrong use of the ICML style package | `\usepackage{icml20XX}` for review, `[accepted]` for camera-ready |
| PAPER-A4, PDF-PAGESIZE | Not US Letter | Remove a4paper; recompile |
| LAYOUT-HACK | Template spacing/layout altered | Remove; cut text instead. Altering the template is grounds for rejection |
| HIDDEN-TEXT, INJECTION-PHRASE | Invisible or reviewer/LLM-directed text | Remove entirely. Prompt injection = desk rejection |
| PLACEHOLDER | TODO/TBD/placeholder citation left | Resolve or remove |
| ABSTRACT-PARAGRAPHS / ABSTRACT-SENTENCES | Abstract not one paragraph / not ~4–6 sentences | Merge; tighten |
| TITLE-ALLCAPS / TITLE-CASE | Title capitalization | Capitalize content words only |
| IMPACT-MISSING / IMPACT-AFTER-REFS / IMPACT-IN-APPENDIX / IMPACT-NUMBERED | Impact Statement missing or misplaced | Unnumbered `\section*{Impact Statement}` before references |
| POSITION-ALT-VIEWS | Position track without "Alternative Views" | Add the section to the main body |
| ACK-IN-SUBMISSION | Acknowledgements in anonymous version | Remove until camera-ready |
| ANON-NAME / ANON-PDF-NAME | Author/affiliation string in text | Remove or rephrase; a hit inside a third-person reference entry is fine |
| ANON-SELFREF | "our previous work" style self-reference | Rewrite in the third person |
| ANON-URL | Non-anonymous URL (GitHub, personal page, shortener) | Replace with anonymous repo (e.g., anonymous.4open.science) or supplementary upload |
| ANON-FUNDING | Grant/funding text | Remove until camera-ready |
| ANON-PDFMETA | Author in PDF metadata | Remove `pdfauthor`, clear metadata; check figure PDFs too |
| ANON-HEADER | First page not showing anonymous author block | Check style option and `\icmlauthor` usage |
| BIB-MISSING / BIBSTYLE | Bibliography missing or wrong style | `\bibliographystyle{icml20XX}` + natbib |
| CAPTION-FIG-POSITION / CAPTION-TAB-POSITION | Caption placement | Figures: caption below. Tables: caption above |
| STY-MODIFIED | Style file differs from official | Restore official file |
| PDF-PAGE-LIMIT | Main body over the limit (heuristic) | Confirm visually; cut |
| PDF-BROKEN-REF / PDF-BROKEN-CITE | `??` or `(?)` | Fix labels/keys; rerun bibtex and latex twice |
| PDF-SIZE | Over file-size limit | Compress raster images; prefer vector plots |
| PDF-TYPE3 / PDF-UNEMBEDDED | Font issues | Use pdflatex; export plots as PDF with embedded fonts |
| CR-* | Camera-ready specific | See icml-camera-ready |

## Manual checks the script cannot do

Anonymity
- Open each figure file: axis labels, watermarks, file paths, usernames, institution
  logos, dataset names unique to the authors' lab, screenshots with names.
- Figure and image file metadata (PDF Author/Creator, EXIF in PNG/JPG).
- Supplementary code: author names in headers, LICENSE files, `.git` directories,
  absolute paths (`/home/<user>/`), cluster or bucket names, wandb/HF usernames,
  notebooks with outputs showing paths. Anonymous GitHub link must be in a text file
  inside the zip and on a branch frozen after the deadline.
- Self-citations read as third person and are not suspiciously over-represented.
- No mention that the paper is an ICML submission in any linked material.

Content
- Everything reviewers need to judge correctness is in the first 8 pages.
- The OpenReview abstract and title match the PDF.
- Impact Statement is more than boilerplate if the work has specific risks.
- LLM use that was notable in the research methodology is described (ICML encourages
  this).
- Dual submission: no substantially similar version under review elsewhere.

Formatting
- No text in margins; no wide content overflowing columns (check equations and tables).
- Figures legible at print size and in grayscale.
- At most three heading levels; headings capitalized.
