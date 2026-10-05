# Prose Principles: Paragraphs and Sentences

Backbone: George Gopen & Judith Swan, "The Science of Scientific Writing" (American
Scientist, 1990). Supplements: Lipton (2018), Ethan Perez ("Easy Paper Writing Tips"),
Jakob Foerster ("How to ML Paper"), Farquhar (2024). Principles are paraphrased; all
examples are written for this skill.

## Contents
1. The core idea: readers interpret structure
2. The seven reader-expectation principles (with ML examples)
3. How to apply them to a paragraph (procedure)
4. When a revision exposes a gap - stop
5. Sentence-level heuristics (Lipton, Perez, Foerster)
6. Terminology, notation and LaTeX hygiene
7. Patterns typical of LLM-drafted text to remove

## 1. The core idea

Readers do not just read; they interpret, and they take many interpretive cues from
*where* information sits. When structure puts information where readers do not expect
it, they spend effort decoding structure instead of content, and different readers come
away with different meanings. Gopen & Swan's claim is that clarity comes from placing
information where readers look for it - not from shortening sentences or removing jargon.
Their principles are explicitly *not* rules: good writers satisfy expectations most of
the time so that deliberate violations stand out.

## 2. The seven principles

**P1. Keep the subject close to its verb.** Readers treat anything between subject and
verb as an interruption of lesser importance, and they wait for the verb to know what
the sentence is about.
- Before: "Our method, which unlike prior approaches based on fixed-temperature
  sampling adapts the temperature per token using a learned predictor trained on held-out
  likelihoods, improves calibration."
- After: "Our method improves calibration by adapting the sampling temperature per token.
  A small predictor, trained on held-out likelihoods, sets each temperature."

**P2. Put the new, important information in the stress position (end of the sentence).**
Readers naturally emphasise what comes at the point of syntactic closure. A semicolon or
colon creates an extra stress position for a second important item.
- Before: "A 12% reduction in error is obtained when the auxiliary loss is added."
- After: "Adding the auxiliary loss reduces error by 12%."

**P3. Put the "whose story" item in the topic position (start of the sentence).** A
sentence is read as being about whatever comes first. "The gate routes tokens" is about
the gate; "Tokens are routed by the gate" is about tokens. The passive version is the
*better* sentence inside a paragraph about tokens.

**P4. Put backward-linking old information in the topic position.** Start sentences with
something the reader has already met, so each sentence hooks onto the previous one and
the paragraph has a visible thread. The usual failure: writers rush to put the new idea
first and tack the linking context on at the end.
- Before: "Gradient noise grows with batch size reduction. Smaller learning rates are
  therefore required. Divergence occurred in 4 of 5 runs at the default rate."
- After: "Reducing the batch size increases gradient noise. This added noise requires a
  smaller learning rate: at the default rate, 4 of 5 runs diverged."

**P5. Express the action in the verb.** When the real action hides in a noun ("performed
an analysis", "has an effect on", "is dependent on"), readers must guess what happens.
- Before: "There is a dependence of the gap on the depth of the network."
- After: "The gap grows with network depth."

**P6. Give context before asking the reader to take in something new.** Motivate an
equation before showing it; name the problem before the solution (Lipton's "Q before A").

**P7. Make structural emphasis match intended emphasis.** If the most important finding
sits in a subordinate clause or mid-sentence, readers will under-weight it.

Their definition of "too long": a sentence is too long when it holds more candidates for
emphasis than it has stress positions - not when it exceeds a word count. A 40-word
sentence that resolves cleanly is fine; a 15-word one with two buried points is not.

Paragraph-level corollaries:
- Each unit of discourse (sentence, paragraph, section) makes one point.
- A paragraph's topic positions, read in sequence, should tell one continuous story. If
  every sentence starts with a different, new subject, the paragraph has no thread.
- The first sentence states the paragraph's point; the last sentence lands on its most
  important consequence (Perez: lead and end with strong, clear sentences).

## 3. Applying them to a paragraph (procedure for the agent)

1. Read the paragraph's `% TL;DR`. If the paragraph makes more than that one point,
   split it; if it makes a different point, fix the TL;DR or the paragraph.
2. List the topic-position phrase of each sentence. Do they trace one story? Choose the
   recurring old information (e.g., "the learned router") as the main topic and move it
   to the front where it fits.
3. List the stress-position phrase of each sentence. Is it the new information worth
   emphasising? Move numbers, findings and key terms there.
4. Find long subject–verb gaps; move the interruption to its own sentence or the end.
5. Find buried actions (nominalisations, "is", "has", "occurs") and replace with the
   verb that names the action.
6. Check the connections between sentences. If you need to insert "however", "therefore"
   or "for example" to make the paragraph flow, verify the logical relation is actually
   true - this is where gaps appear (next section).

## 4. When a revision exposes a gap - stop

Gopen & Swan found that in most of their examples, restructuring stalled at a point
where the original author had never stated how two ideas connect; continuing required
either adding material or deleting some. They supplied the missing links from their own
domain knowledge and flagged that their reading might not match the author's intent.

For an agent this is the highest-risk moment in revision. Do not insert a mechanism,
causal story or justification that is not already in the paper, the project notes or a
verified source. Instead:
- leave the text as is or soften it to what is supported ("we observe X; we do not test
  why"),
- add an `[gap]` item to `.icml/open_issues.md` naming the two ideas that need a link and
  offering options: cite a source, run an experiment, state it as a hypothesis, or cut,
- continue with the rest of the pass.

## 5. Sentence-level heuristics

Use these as a checklist; `scripts/lint_prose.py` flags many of them automatically.

From Lipton:
- Delete generic openings that could start any ML paper.
- Do not tease: put the key number or equation up front.
- Avoid hostages to fortune: every sentence should be defensible in isolation ("on 7 of
  9 datasets", not "on most datasets").
- A sin of omission beats a sin of commission: drop claims you cannot fully support.
- Label opinions as opinions.
- Drop intensifiers and vacuous adverbs (very, extremely, essentially, quite, rather,
  completely, truly, real). "A tight bound" sounds more confident than "a very tight bound".
- Attribute actions to the right subject: algorithms do not "try", "want" or "know".
- Prefer short sentences for complex ideas; sophisticated ideas, plain syntax.
- Paragraphs usually have at least three sentences; sections either have zero or at
  least two subsections; section titles should be parallel in scope.

From Perez:
- Minimise pronouns; if you use "this/these/that", follow it with a noun ("this result").
- Put the verb early in the sentence.
- Unfold awkward possessives ("the variance of the estimator", not "the estimator's
  variance" when the latter stacks).
- Use simple, short words.
- No comparatives without an explicit comparison ("improves", "better" - than what?).
- One sentence, one idea; but long sentences with simple words are fine.
- Every sentence must add information. Ask of every word: is it necessary, can it be
  simpler, is it correct?
- Remove: actually, a bit, fortunately, note that, observe that, try to, to our
  knowledge (unless genuinely needed), very/really/extremely, most "however"s.
- Replace: want, hope, contractions, scare-quoted words.
- Do not start every sentence with "We".
- Define unusual terms at first use.
- Limit hedging ("may", "can") - it should almost always go.
- Avoid single-word last lines in paragraphs (they waste space).

From Foerster:
- Prefer active voice when it clarifies who did what - but see P3: keep the passive when
  it keeps the paragraph's topic in front.
- Be extremely clear about contributions; never blur prior work and yours.
- Keep tense consistent; avoid the future tense ("we will show" → "we show").
- Delete filler: "in order to" → "to"; "can be reformulated as a special subset of" →
  "is a special case of".
- After drafting, try deleting about a third of the words.
- Avoid anthropomorphising models ("knowledge", "understands") unless defined.
- Adjectives are red flags for subjective claims.
- "On the other hand" requires "on the one hand".
- Do not repeat the same word within a sentence.
- Simple language: many readers are not native English speakers.
- Never copy-paste from other papers; write from scratch.

## 6. Terminology, notation and LaTeX hygiene

- One term per concept. Never use synonyms for work-specific terminology; if a term
  could be confused with a standard one, say so once with an example.
- Introduce acronyms before use; do not Capitalise Random Words to make acronyms; only
  proper nouns are capitalised (Markov chain Monte Carlo, MCMC; Transformer is
  conventionally capitalised).
- Introduce only symbols and acronyms the paper actually uses.
- Equations are part of sentences: punctuate them, and do not put a colon before an
  equation that completes the sentence.
- `\citet{key}` when the authors are part of the sentence ("\citet{x} show"),
  `\citep{key}` otherwise; acronym with citation: `\citep[PPO;][]{schulman2017ppo}` or
  "proximal policy optimization \citep[PPO]{...}".
- Correct LaTeX quotes: ``like this'' (or `\enquote{}` with csquotes).
- `cleveref` (`\cref`) for cross-references; footnote marks after punctuation.
- Consistent bold/italic conventions; British or American spelling, not both.
- No `??` in the PDF; cite the published version rather than arXiv when one exists.

## 7. Patterns typical of LLM-drafted text to remove

Readers increasingly recognise and discount these. Remove them on sight:
- Field-level hype openers ("In recent years, X has attracted significant attention").
- Inflated vocabulary: delve, crucial, pivotal, landscape, realm, robust (when not a
  technical claim), seamless, comprehensive, novel (as decoration), leverage (as "use"),
  "plays a vital role", "paves the way".
- Triplets and symmetric lists used for rhythm rather than content.
- Summary sentences that restate the paragraph ("In summary, ...", "Overall, ...").
- Paired hedges and boosts in one sentence ("may significantly improve").
- Rhetorical questions and colons used for drama ("The answer: ...").
- Bulleted lists in running text other than the contribution list.
- Over-signposting ("It is worth noting that", "Importantly,").
