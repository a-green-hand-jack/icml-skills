---
name: icml-cite
description: Find, verify, and manage references for ICML papers, avoiding fabricated citations. Searches DBLP, Semantic Scholar, arXiv, and Crossref to fetch BibTeX programmatically, upgrades arXiv entries to their formally published versions, checks .bib against LaTeX source files (missing keys, duplicates, unprotected capitals, incomplete fields), and keeps a verification log. Use this skill when an ICML paper needs citations, related-work references, BibTeX entries, bibliography cleanup, confirmation that a cited paper exists or says what the text claims, ICML APA/natbib citation formatting, anonymous self-citations, or camera-ready Reference Correctness Check fixes—even if the user only says "add a citation here" or "clean up my bib." Never write BibTeX from memory.
compatibility: Python 3 standard library. Lookups require internet access to dblp.org, api.semanticscholar.org, export.arxiv.org, and doi.org; if offline, the skill marks citations as placeholders.
---

# ICML Citations

Language models misremember references: wrong authors, wrong years, wrong venues, and papers that do not exist at all. Fabricated or erroneous citations in a submission constitute academic misconduct, and ICML now runs an automated reference checker at the camera-ready stage. This skill makes every citation traceable to a database record.

Communicate with the user in their language. This skill shares the `.icml/` workspace with its sibling skills; first run `python scripts/init_workspace.py --root <latex-root> --skill icml-cite`, and see `references/workspace-contract.md` for format details.

## Principles

**Never write or edit BibTeX entries from memory.** Each entry must come from a database response (DBLP, Crossref via DOI, arXiv, Semantic Scholar) or a user-supplied file. If it cannot be obtained, insert a conspicuous placeholder and inform the user:

```latex
\citep{PLACEHOLDER_sparse_moe_routing}  % UNVERIFIED: need a source for "router collapse"
```

and add a `[cite]` item to `.icml/open_issues.md`. Placeholders are honest; a plausible but fabricated citation is not.

## Workflow: Adding a Citation

1. **Clarify exactly what claim it needs to support.** Write down the exact assertion the citation supports ("router collapse occurs without load balancing"). Citations support claims, not topics.
2. **Search.** `python scripts/cite_lookup.py search "query terms" [--year-from 2020]` searches DBLP (best for computer-science conferences, including ICML/PMLR, NeurIPS, ICLR via OpenReview) and Semantic Scholar. Add `--source arxiv` to search preprints. Try multiple phrasings and author names before concluding a paper does not exist.
3. **Identify the correct record.** Match title, first author, and year. When both a published version and an arXiv version exist, prefer the former (ICML requires this at camera-ready; Foerster: Google Scholar usually defaults to the arXiv version). Watch out for workshop versions and later papers with the same name.
4. **Retrieve BibTeX.** `python scripts/cite_lookup.py bibtex --dblp <key>` or `--doi <doi>` or `--arxiv <id>`. Paste the result into `.bib` verbatim, then edit only: set the citation key to the project convention, protect uppercase letters in the title with braces (`{B}ayesian`, `{MCMC}`, `{T}ransformer`), and remove fields the style does not need (abstract, keywords). Never manually change authors, year, venue, or pages.
5. **Verify the claim.** If the claim is important (it supports an argument, a baseline number, or a definition), read the abstract or relevant sections via the lookup output or paper page to confirm it actually says what the text claims. If you cannot access it, log the citation as `existence-verified, claim-unverified` and inform the user.
6. **Log** in `.icml/citations_log.md`: key, status (`verified` / `existence-only` / `placeholder`), sources checked, whether a published version exists, notes.

## Workflow: Auditing References

Run `python scripts/check_bib.py main.tex refs.bib`. It reports:
- keys cited but missing from `.bib`, and unused entries,
- duplicate entries (same title or same DOI/arXiv id under different keys),
- entries missing required fields for their type,
- arXiv-only or CoRR entries (candidates for upgrading to a published version),
- title capitalizations that BibTeX will lowercase (unprotected acronyms and proper nouns),
- placeholder keys still present,
- plain `\cite` usage (ICML uses natbib: `\citet` vs `\citep`).

Then verify every entry not yet in `citations_log.md`, prioritizing entries that support claims in the abstract, introduction, and experiments, and every baseline. For arXiv entries, run `python scripts/cite_lookup.py published "<title>"` to find the published version.

## ICML-Specific Rules

Detailed rules are in `references/citation-rules.md`. Key points:
- APA author-year format via `natbib` and `\bibliographystyle{icml20XX}`. Use `\citet{}` when the author is a grammatical part of the sentence, otherwise `\citep{}`; multiple citations in chronological order.
- Anonymous submission: cite your own published work in the third person, as if written by someone else; do not anonymize published entries in the reference list. Unpublished work of your own (e.g., under review elsewhere) is cited anonymously and uploaded as anonymous supplementary material.
- Work made public less than two months before the deadline counts as concurrent work for ICML; citing it is optional.
- Camera-ready: replace arXiv citations with published versions whenever possible; fix every item in the OpenReview "Reference Correctness Check"; keep author names up to date.

## Related-Work Support

When icml-write requests related work, return for each candidate: verified BibTeX, a one-sentence summary of what the paper does (from its abstract, in your own words), and its relationship to the project (same problem / same technique / baseline candidate). Group by methodological thread so the related-work section can compare and contrast rather than list papers. Flag any methods applicable to the problem setting: icml-write must either compare against them or explain why they are not applicable.

## When Offline

If lookups fail (no network), explicitly inform the user, preserve existing verified entries, add placeholders for new entries, and list them. Do not "complete from memory" even for famous papers—famous papers are exactly where confident misremembering happens (wrong year, arXiv vs. conference version confusion).

## Files

- `scripts/cite_lookup.py` — search / bibtex / published-version lookup (standard library only).
- `scripts/check_bib.py` — bibliography audit against LaTeX source.
- `scripts/init_workspace.py` — create the shared `.icml/` workspace.
- `references/citation-rules.md` — ICML citation format, anonymity, BibTeX specifications.
- `references/workspace-contract.md`, `references/icml-venue-facts.md` — shared files.
