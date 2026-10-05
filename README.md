# ICML Paper-Writing Skill Family

A family of ICML paper skills for coding agents (Claude Code, etc.), covering the full lifecycle from research repository to camera-ready.
Compiled from the ICML 2026 official rules (snapshot date 2026-10-05) and writing advice from Nanda, Farquhar, Foerster, Gopen & Swan, Lipton, Perez, Parikh/Batra/Lee, and others.

## Five Skills

| Skill | When to Trigger | Core Output | Mandatory Human Stop Points |
|---|---|---|---|
| `icml-write` | Drafting from repository, revising existing draft, migrating to ICML format | Claim ledger, paragraph outline, body text with `% TL;DR` annotations | ① Claims and abstract ② Outline, figure plan, page budget ③ True explanation of logical gaps |
| `icml-cite` | Finding literature, generating BibTeX, checking references | Verified `.bib` and verification log | Whether to keep unverifiable citations |
| `icml-review` | Pre-submission self-check, simulated review | Compliance report + ICML review-form-style simulated review | None (read-only, no editing) |
| `icml-rebuttal` | After receiving reviews | Review classification table, per-round responses, promise checklist | Response strategy; whether to point out reviewer misconduct; any new experimental results |
| `icml-camera-ready` | After acceptance | De-anonymized final draft, lay summary, submission checklist | Conflict-of-interest statement; author and affiliation information |

## Shared State: The `.icml/` Workspace

The five skills do not reference each other's installation directories; instead, they share state through the `.icml/` directory in the paper project
(see any skill's `references/workspace-contract.md` for details):

- `claims.md`: Claim ledger. Every number in the paper must be traceable to a results file in the project.
- `outline.md`, `open_issues.md` (questions only humans can answer), `decisions.md` (human decisions and justifications for style-rule exceptions)
- `citations_log.md`, `reviews/`, `rebuttal/` (including `promises.md`), `camera_ready.md`, `state.md`
- `venue_facts.md`: ICML rules for the target year. Must be refreshed for each new cycle.

Any skill runs `scripts/init_workspace.py` on startup, which only fills gaps and never overwrites.

## Installation

Use the [`skills` CLI](https://github.com/vercel-labs/skills) (requires Node.js), **in the root directory of your paper repository**, installing on demand:

```bash
cd <your-paper-repo>

# List available skills in this repo
npx skills add a-green-hand-jack/icml-skills --list

# Install only the skills needed for the current stage, e.g., writing stage:
npx skills add a-green-hand-jack/icml-skills --skill icml-write icml-cite icml-review -a claude-code
# Add after receiving reviews:
npx skills add a-green-hand-jack/icml-skills --skill icml-rebuttal -a claude-code

# Install all five at once
npx skills add a-green-hand-jack/icml-skills --skill '*' -a claude-code
```

- **Each skill can be installed individually.** Each skill directory carries its own `references/` and `scripts/` and does not depend on whether other skills are installed; they interact only through the `.icml/` directory in the paper repository.
- `-a` specifies the agent: `claude-code` installs to `.claude/skills/`; other common values are `codex`, `cursor`, `opencode`, `gemini-cli`; when omitted the CLI auto-detects or prompts.
- Installation generates `skills-lock.json` in the repository root, recording the source and version of each skill. Committing it together with the skill directories lets collaborators use the same versions after cloning.
- Update: `npx skills update -p`; uninstall: `npx skills remove icml-cite`.
- Without Node.js, you can manually copy a single skill: `cp -r icml-review <your-paper-repo>/.claude/skills/`.

**Global installation with `-g` is not recommended**, for the following reasons:

- These skills are intentionally given broad trigger descriptions (e.g., "look at my paper", "clean up my bib", "make my intro better"). When installed globally, they will fire on ICML-unrelated projects.
- `icml-venue-facts.md` is bound to a specific year's ICML rules. Project-level installation lets each paper lock to its submission cycle's version, so updating one repository does not affect another paper still under review or in rebuttal.

Dependencies: Python 3 (scripts use only the standard library). TeX Live (pdflatex, bibtex) and poppler-utils (pdftotext, pdfinfo, pdffonts) are recommended; without them, related checks are skipped with a notice. `icml-cite` requires access to dblp.org, api.semanticscholar.org, export.arxiv.org, and doi.org; when offline it explicitly downgrades to placeholders and never hallucinates citations from memory.

Do not install alongside very broad generic paper skills (e.g., davila7's `ml-paper-writing`), to avoid trigger contention.

## Maintenance

- **Year-specific rules are modified only in `_shared/references/icml-venue-facts.md`**, then run `bash sync_shared.sh` to distribute to all skills. `workspace-contract.md`, `init_workspace.py`, and `check_submission.py` are handled the same way.
- After modifying scripts, run `bash tests/run_tests.sh` (41 regression tests; the `icml2026.sty` in fixtures is a test stub, not the official style—never use it for real papers).
- `tests/eval-prompts.md` lists test prompts used to evaluate skill behavior (not just scripts).

## Known Limitations

- Compliance checks are heuristic: page count relies on the final section title in the PDF text; anonymity checks require supplying author names and institution names. Final verification still requires the official paper checker and human proofreading.
- `cite_lookup.py` online APIs cannot be tested with real network access in the build environment; only mock responses are used to test parsing logic. Please verify that a few queries return correctly on first use.
- Writing reference materials focus on empirical papers; theory papers should supplement with your group's own conventions.
- Position track has only basic support (Alternative Views check, no Impact Statement).

## Primary Sources

ICML 2026 Author Instructions / Call for Papers / Reviewer Instructions / example paper / Lay Summaries blog post;
Neel Nanda, *Highly Opinionated Advice on How to Write ML Papers* (2025);
Sebastian Farquhar, *How to Write ML Papers* (2024); Jakob Foerster, *How to ML Paper - A brief Guide*;
Gopen & Swan, *The Science of Scientific Writing* (1990); Zachary Lipton, *Heuristics for Scientific Writing* (2018);
Ethan Perez, *Easy Paper Writing Tips*; Parikh, Batra & Lee, *How we write rebuttals* (2020).
Content in each skill is paraphrased and adapted; examples are original.
