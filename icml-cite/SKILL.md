---
name: icml-cite
description: Find, verify and manage references for ICML papers without hallucinated citations. Searches DBLP, Semantic Scholar, arXiv and Crossref, fetches BibTeX programmatically, upgrades arXiv entries to their published versions, checks the .bib against the LaTeX source (missing keys, duplicates, unprotected capitals, incomplete fields), and keeps a verification log. Use this skill whenever an ICML paper needs citations, related-work references, a BibTeX entry, a bibliography cleanup, a check that a cited paper exists or says what the text claims, ICML's APA/natbib citation format, anonymous self-citation, or fixes from the camera-ready Reference Correctness Check - even if the user just says "add a cite for this" or "clean up my bib". Never write BibTeX from memory.
compatibility: Python 3 standard library. Network access to dblp.org, api.semanticscholar.org, export.arxiv.org and doi.org is needed for lookups; without it, the skill marks citations as placeholders.
---

# ICML Citations

Language models misremember references: wrong authors, wrong years, wrong venues, and
papers that do not exist. A fabricated or wrong citation in a submission is a form of
misconduct, and ICML now runs an automated reference checker at camera-ready. This skill
makes every reference traceable to a database record.

Talk to the user in their language. This skill shares the `.icml/` workspace with its
siblings; run `python scripts/init_workspace.py --root <latex-root> --skill icml-cite`
first, and see `references/workspace-contract.md` for the formats.

## The rule

**Never write or edit a BibTeX entry from memory.** Every entry comes from a database
response (DBLP, Crossref via DOI, arXiv, Semantic Scholar) or from a file the user
supplied. If you cannot get one, insert a visible placeholder and tell the user:

```latex
\citep{PLACEHOLDER_sparse_moe_routing}  % UNVERIFIED: need a source for "router collapse"
```

and add `[cite]` items to `.icml/open_issues.md`. A placeholder is honest; a plausible
but invented reference is not.

## Workflow: adding a citation

1. **Know what you need it for.** Write down the exact claim the citation supports
   ("router collapse happens without load balancing"). Citations support claims, not
   topics.
2. **Search.** `python scripts/cite_lookup.py search "query terms" [--year-from 2020]`
   searches DBLP (best for CS venues incl. ICML/PMLR, NeurIPS, ICLR via OpenReview) and
   Semantic Scholar. Add `--source arxiv` for preprints. Try several phrasings and author
   names before concluding a paper does not exist.
3. **Identify the right record.** Match title, first author and year. Prefer the
   peer-reviewed version over arXiv when both exist (ICML asks for this at camera-ready;
   Foerster: Google Scholar often defaults to the arXiv version). Beware workshop
   versions and same-title follow-ups.
4. **Fetch BibTeX.** `python scripts/cite_lookup.py bibtex --dblp <key>` or
   `--doi <doi>` or `--arxiv <id>`. Paste the result unchanged into the `.bib`, then
   apply only these edits: set the citation key to the project's convention, protect
   capitals in the title with braces (`{B}ayesian`, `{MCMC}`, `{T}ransformer`), and drop
   fields the style does not need (abstract, keywords). Never change authors, year,
   venue or pages by hand.
5. **Check the claim.** If the claim matters (it supports an argument, a baseline number
   or a definition), read the abstract or relevant section via the lookup output or the
   paper's page and confirm it says what the text says. If you cannot access it, log the
   citation as `existence-verified, claim-unverified` and tell the user.
6. **Log it** in `.icml/citations_log.md`: key, status (`verified` /
   `existence-only` / `placeholder`), sources checked, whether a published version
   exists, notes.

## Workflow: auditing a bibliography

Run `python scripts/check_bib.py main.tex refs.bib`. It reports:
- cited keys missing from the `.bib`, and unused entries,
- duplicate entries (same title or same DOI/arXiv id under different keys),
- entries missing required fields for their type,
- arXiv-only or CoRR entries (candidates for upgrading to the published version),
- titles with capitals that BibTeX will lowercase (unprotected acronyms and proper nouns),
- placeholder keys still present,
- plain `\cite` uses (ICML uses natbib: `\citet` vs `\citep`).

Then verify each entry not yet in `citations_log.md`, prioritising entries that support
claims in the abstract, introduction and experiments, and every baseline. For arXiv
entries run `python scripts/cite_lookup.py published "<title>"` to find a published
version.

## ICML-specific rules

Read `references/citation-rules.md` for details. The essentials:
- APA author–year via `natbib` and `\bibliographystyle{icml20XX}`. `\citet{}` when the
  authors are a grammatical part of the sentence, `\citep{}` otherwise; multiple
  citations in chronological order.
- Anonymous submission: cite your own published work in the third person, as if someone
  else wrote it; do not anonymize published entries in the reference list. Unpublished
  own work (e.g., under review elsewhere) is cited anonymously and uploaded as anonymized
  supplementary material.
- Works made public less than two months before the deadline are concurrent work at
  ICML; citing them is optional.
- Camera-ready: replace arXiv citations with peer-reviewed versions where possible; fix
  every item in OpenReview's "Reference Correctness Check"; keep author names current.

## Related work support

When icml-write asks for related work, return for each candidate: verified BibTeX, one
sentence on what the paper does (from its abstract, in your own words), and how it
relates to the project (same problem / same technique / baseline candidate). Group by
methodological line so the related-work section can compare and contrast rather than
list papers. Flag any method that is applicable to the problem setting: icml-write must
either compare against it or state why it is not applicable.

## When offline

If lookups fail (no network), say so explicitly, keep existing verified entries, add
placeholders for new ones, and list them for the user. Do not "fill in" from memory even
for famous papers - famous papers are exactly where confident misremembering happens
(wrong year, arXiv vs. conference version).

## Files

- `scripts/cite_lookup.py` — search / bibtex / published-version lookups (stdlib only).
- `scripts/check_bib.py` — bibliography audit against the LaTeX source.
- `scripts/init_workspace.py` — create the shared `.icml/` workspace.
- `references/citation-rules.md` — ICML citation format, anonymity, BibTeX hygiene.
- `references/workspace-contract.md`, `references/icml-venue-facts.md` — shared.
