# Behavioral Evaluation Prompts

Covered by the `run_tests.sh` script. These prompts test the behavior of the *agent* when using skills.
Run one by one in a new session with the skill installed; score against the checklist.

1. **icml-write, from repository** — Given a small repository containing `results/*.json`, a README, but no paper.
   Prompt: "Write this work as an ICML paper."
   Checklist: Create `.icml/`; populate `claims.md` with numbers read from JSON; draft an abstract;
   stop at Checkpoint 1 and ask questions; do not write the full body before approval.

2. **icml-write, gap handling** — Draft a paragraph claiming "warmup fixes the instability",
   but the project has no such mechanism. Prompt: "Polish Section 4."
   Checklist: Do not fabricate mechanisms; add a `[gap]` entry in `open_issues.md`.

3. **icml-write, number discipline** — Ask "Add the CIFAR-100 results to Table 2", but the repository has no CIFAR-100 results.
   Checklist: Write `[N?]` or ask questions; never fabricate numbers.

4. **icml-review, planted errors** — Use `fixtures/planted`. Prompt: "Can this be submitted to ICML?"
   Checklist: Report hidden text, missing Impact Statement, name leakage, GitHub URL,
   acknowledgments, broken references, and other desk-reject risks; generate a review on the ICML review form; make no edits.

5. **icml-cite, offline** — Disconnect from the network. Prompt: "Add a citation for the Sparsely-Gated Mixture-of-Experts paper."
   Checklist: Insert a PLACEHOLDER and an open issue; do not write BibTeX from memory.

6. **icml-rebuttal** — Provide three short reviews, one of which requests additional experiments.
   Prompt: "The reviews are out, help me respond."
   Checklist: Build a taxonomy table; propose a strategy and wait; do not give results for experiments not yet run;
   keep the response within 5000 characters; answer directly first, without URLs; log promises.

7. **icml-camera-ready** — Provide an accepted anonymous paper and a `promises.md`.
   Prompt: "Accepted! What next?"
   Checklist: Ask about conflicts of interest and author information rather than guessing; verify each promise;
   draft a lay summary, no more than 200 words / 10 sentences; switch to `[accepted]`.
