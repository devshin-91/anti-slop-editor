# English Anti-Slop Reference (`lang: en`)

Synthesizes `blader/humanizer` v4.0 (26 tells), `hardikpandya/stop-slop` (50-point rubric),
`Dodaios/ste80-humanizer` (Karpathy ASD-STE100), `harshaneel/humanize` (9 research levers),
and Wikipedia `WP:AISIGNS` (2026 revision).

---

## 1. Priority Tiers (Strongest First)

### Tier A — Staging Instead of Stating (Act on 1 Sighting)
1. **Not X, but Y (Negative Parallelism):** `not just X, but Y`, `it's not X—it's Y`, `X rather than Y`, split across sentences (`This does not mean X. It means Y.`), or clipped negative tails (`..., no guessing`).
   - *Fix:* State Y directly unless X genuinely corrects a belief the reader holds.
2. **One-Line Closers & Dramatic Fragments:** `That is the real win.`, `Let that sink in.`, `Read that again.`, `No excuses. No shortcuts.`, or a final `Overall/Ultimately` restating what the paragraph just showed.
   - *Fix:* Cut unless it introduces a genuinely new fact or consequence.
3. **Fake-Deep Aphorisms:** `at its core`, `what really matters`, `the real question is`, `X is the language/currency/architecture of Y`, `not a tool, a mirror`.
   - *Fix:* State the plain mechanism.
4. **Staged Run-Ups & Throat-Clearing:** `Let's dive in`, `Here's the thing`, `Honestly?`, `Look,`, `Without further ado`, `The hard part is...`, `The part worth sharing...`.
   - *Fix:* Delete the wind-up and name the thing immediately.
5. **Arguing With No One (Phantom Objections):** `To be clear, I'm not saying...`, `Don't get me wrong`, `A tempting approach would be...`, `Some might say...`.
   - *Fix:* Delete unattributed strawmen; keep only objections the reader would actually weigh.

### Tier B — RLHF / Instruction-Tuning Voice (`Lever 9` — Highest-Impact 2026 Signal)
Grounded in `arXiv:2605.19516` ("Base Models Look Human"):
- Strip unrequested balanced tradeoffs ("On the one hand... on the other hand...").
- Strip chatbot wrappers (`Great question!`, `Certainly!`, `I hope this helps!`, `Let me know if...`).
- Strip knowledge-cutoff guesses (`While details are limited, it likely...` → `The sources do not say.`).
- Strip writing *about* the document (`This section compares...`, `This function was added to replace...`) except in changelogs/release notes.
- Strip re-explaining background the reader already has in replies/PRs; lead with the decision.

### Tier C — Rhythm, Inflation, & Copula Avoidance
- **Forced Triads (Rule of Three):** Break mechanical 3-adjective or 3-example clusters (`fast, intuitive, and powerful`) into 1–2 concrete specifics.
- **Avoidance of `is`/`are`/`has`:** Replace `serves as / stands as / functions as / boasts / features` with plain `is / are / has`.
- **Shallow `-ing` Riders:** Cut bolted-on participles (`..., highlighting its commitment to...`, `..., underscoring/fostering/showcasing...`) unless backed by a new fact.
- **Overused AI Lexicon (Act especially in clusters):** `delve`, `tapestry`, `testament`, `pivotal`, `crucial`, `vibrant`, `landscape` (figurative), `robust` (figurative), `seamless`, `leverage` (verb), `foster`, `garner`, `meticulously`, `intricate`, `quietly`, `game-changer`, `supercharge`, `unlock`.
- **Vague Authority & Association:** Replace `experts argue / linked to / associated with` with the named source and exact causal link—or cut.
- **Autopilot Transitions:** Cut `Furthermore`, `Moreover`, `Additionally`, `Notably`, `Importantly`, `In conclusion`.
- **Inanimate False Agency (`stop-slop`):** Replace `"The complaint becomes a fix"` / `"The decision emerges"` with a named human/system subject.
- **Cut Pull-Quotes (`stop-slop`):** If a sentence sounds written to be screenshotted on LinkedIn/X, rewrite it plainly.

### Tier D — Punctuation & Formatting (Contextual, Respect 2026 Shifts)
- **Em dashes (`—`) & double hyphens (` -- `):** Keep at most 1 per 300 words (or match author sample); eliminate double-wrapped ` — like this — ` asides. Note: Wikipedia moved em-dash overuse to *Historical indicators (2022–Sep 2026)* as newer models vary, so treat single dashes as *weak alone*.
- **Semicolons (`;`) & Mid-Sentence Colons (`:`):** Replace semicolons with periods (except complex lists); ensure colons follow grammatically complete sentences (`The problem: nobody tests` → `Nobody tests this.`).
- **Decorative Bold+Colon Lists & Emoji Headings:** Convert mechanical `- **Speed:** Speed is improved.` bullets into concise prose; use sentence case in headings.
- **Hyphenated Predicates:** `a well-documented API` (keep hyphen before noun) vs `the API is well documented` (drop hyphen after noun).

---

## 2. Five-Dimension Quality Rubric (`stop-slop`, Score 1–10 Each)

Before finishing a `refactor` or `write`, silently verify:
1. **Directness:** Statements or announcements?
2. **Rhythm:** Natural spread (mix ≤6-word sentences with longer explanatory ones; never 3 consecutive sentences within 5 words of each other—without mechanical choppiness)?
3. **Trust:** Respects reader intelligence without hand-holding or restating examples?
4. **Authenticity:** Sounds like a real person in this venue?
5. **Density:** Anything cuttable?

If total < **35/50**, run one targeted revision pass.

---

## 3. When NOT to Edit (English Whitelist)
- Informal chat/rant registers (`"Worst. Service. Ever."`, `"lmk"`, genuine anger) are already human—do not sanitize them.
- Clean grammar, formal register in legal/scientific texts, and intentional rhetorical parallelisms in speeches are NOT AI tells.
- Never alter direct quotations or deliberate dialect/nonstandard spelling.
