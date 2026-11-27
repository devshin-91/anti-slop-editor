# Architecture, Genre Routing, and Pre-Drafting Protocols

Empirical studies (`StoryScope`, arXiv:2604.03136; `SlopShape`, arXiv:2609.15369; `Base Models Look Human`,
arXiv:2605.19516) prove that surface vocabulary edits leave ~94% of structural AI fingerprints intact.
Fix architecture and venue alignment **before** touching word choice.

---

## 1. Pre-Drafting (`write` Operation): Preventing Slop at the Source

### A. Identity-First 4-Step Order (Avoid "Form-Filling" Mode)
Never hand an LLM a rigid bullet skeleton first—that triggers robotic form-filling. Follow this order:
1. **Identity first:** Who is speaking, to whom, and what actually happened.
2. **Separated fact source:** Supply raw notes, numbers, logs, or transcripts as the *only* allowed source of facts.
3. **Platform limits only:** State length/format boundaries; leave internal organization natural.
4. **Anti-slop check last:** Run `slop_engine.py scan` + targeted cleanup only after the draft exists.

### B. Interview-First & Raw-Context Rule
When user input is thin (<3 concrete facts/examples), **do not invent generic filler or fake anecdotes**.
Ask 3–5 concrete interview questions (real failure, exact metric, specific constraint, personal stance)
or mark missing specifics with explicit `[TODO: 구체 수치/사례 입력]` placeholders.

### C. Affirmative Framing (Avoid the Pink Elephant Problem)
Frame drafting instructions positively rather than stacking prohibitions:
- Instead of "Don't use bullet points" → "Write in connected prose paragraphs."
- Instead of "Don't add a generic conclusion" → "End on the last concrete fact or next step."
- Instead of "Don't sound like a robot" → "Name the actor as subject, use plain everyday verbs, and stop explaining once the fact is stated."

### D. Verbalized Sampling for Creative / Ideation Tasks (`arXiv:2510.01171`)
When brainstorming titles, hooks, metaphors, or story premises (where RLHF typicality bias causes
mode collapse), internally generate 5 diverse candidates across the probability tail (including unusual,
non-consensus angles) and pick the sharpest grounded option instead of the default modal answer.

---

## 2. Three-Pass Structural Repair (For `heavy`, `fiction`, and Long-Form)

| Pass | Layer | Core Actions |
|---|---|---|
| **Pass 1** | **Narrative / Structural Architecture** | Stop explaining the moral/theme; remove narrator-from-a-distance commentary; loosen overly tidy single-track causality; name real-world specifics (dates, tools, places, costs); strip unrequested RLHF "both-sides" hedging and fake-profound endings. |
| **Pass 2** | **Discourse Flow** | Break metronomic paragraph shapes and Q&A templates; remove consecutive explicit transition chains (`Furthermore / 또한 / 这也解释了`); allow natural topic transitions; unify synonym-cycled names for the same concept. |
| **Pass 3** | **Surface & Lexical** | Apply language-specific patterns (`lang-ko.md` / `lang-en.md` / `lang-ja-zh.md`), normalize decorative formatting, run `verify` gate. |

**Calibration Law:** Apply **3–5 natural moves per piece**; never crank every dial to the opposite extreme.
Maintain the human editing ratio (**~74% replace / ~18% delete / ~8% insert** — never bloat text).

---

## 3. Genre / Venue Routing Rules

### 3.1 Blog, Column, & Newsletter (`blog`)
- **Delete throat-clearing openers:** Start in media res—at the concrete problem, surprising number, or lived tension.
- **Concrete anchors:** Replace vague abstractions ("many teams", "효율이 크게 올랐다") with named tools, exact constraints, or real trade-offs.
- **Take a stance:** Cut unrequested balanced disclaimers when the author actually holds a clear view.
- **End cleanly:** Stop at the last real point; cut motivational wrap-ups ("앞으로가 기대됩니다", "The future looks bright").

### 3.2 Technical Docs, README, Release Notes, Postmortems, PR Replies (`tech`)
Combine **Karpathy's 80% ASD-STE100** + **Meiseki Clarity (明晰)** + **Sepia Professional Rules**:
- **Clarity over fake voice:** Do NOT inject artificial first-person chatter or forced warmth. Optimize for **one-pass comprehension**.
- **ASD-STE100 (80% pragmatic mode):**
  - 1 idea per sentence (target ≤20 words for instructions, ≤25 for descriptions in EN; ≤60–90 chars in KO/JA).
  - Condition first: `"If X fails, run Y"` / `"X가 실패하면 Y를 실행한다"`.
  - Active voice, simple tenses, **1 consistent term per concept** (kill synonym cycling!), no noun stacks >3 words, no semicolons.
  - Separate procedure steps from background explanation; put warnings *before* the risky step.
- **Venue specifics:**
  - *PR / Issue replies:* Lead with the decision; cite `file:line`; do not re-explain context the reviewer already knows; kill reflex praise ("Great catch!").
  - *Release notes:* User impact first; artifact/link per claim; zero marketing inflation.
  - *Postmortems:* Blameless toward people, ruthless toward mechanisms; exact timestamps, dead ends tried, owned action items.

### 3.3 Academic Papers & Grant Proposals (`academic`)
Grounded in `academic-humanizer`, `aigc-reduce`, and `SciSlopBench` (`arXiv:2610.00531`):
- **Hard Floor — Scholarly Register Only (`降重 ≠ 口语化`):** NEVER inject internet slang, casual filler ("솔직히", "说白了", "honestly"), emotional exclamations, or choppy telegraphic fragments.
- **Tie claims strictly to evidence:** Downgrade unsupported strength (`prove` → `show empirically`, `revolutionize` → `reduce latency by X%`); convert vague magnitudes into cited/measured ranges.
- **Preserve legitimate scholarship:** Keep evidence-tied hedging, appropriate passive voice (Methods), `we`, formal definitions, mathematical notation, exact numbers, and every citation verbatim.
- **Structural de-slopping for papers:**
  - Cut formulaic openers ("In recent years, X has attracted increasing attention...").
  - Replace author-by-author laundry lists in Related Work with thematic synthesis + explicit contrast to the present study.
  - Eliminate floating consequence chains (2+ consecutive `thereby/highlighting/이를 통해/从而` riders).
  - Keep em-dashes ≤1 per paragraph (prefer clean subordinate clauses or periods).
  - In grants (NSF/NIH), keep forward vision where required, tie every ambitious claim to feasibility/preliminary evidence, and front-load clarity on page 1.

### 3.4 Fiction, Web Novels, & Roleplay (`fiction`)
Grounded in `StoryScope` (`arXiv:2604.03136`), `arXiv:2611.01284`, and SillyTavern/RisuAI practice:
- **Repair StoryScope architectural gaps first:**
  - Never let the narrator spell out the lesson/moral at scene end (AI 77% vs Human 52%).
  - Mix emotion modes: replace overused bodily-sensation clichés (*tightening chest, shivers down spine, knuckles white, 입술을 깨물었다, 전율이 흘렀다*) with concrete actions, practical costs, subtext, or silence.
  - Allow moral ambiguity, messy loose ends, flashbacks/nonlinear pacing, and sparse character networks.
  - Avoid LLM character-name concentration (*Elara, Marcus, Vance, Thorne, Aria, Lyra, Elena*).
- **Do not apply STE80 or business rules to fiction.** Preserve literary rhythm, intentional repetition/refrains, and dialogue dialect.

### 3.5 SNS, Threads, X, & Community Posts (`sns`)
- **Platform pacing:** Open with a concrete hook (real number, counter-intuitive observation, lived confession)—never clickbait templates ("Most people don't know this...").
- **De-ornamentation:** Strip emoji confetti (`🚀💡✨🎯`), forced `"1/10 🧵"` theatrics, and unnecessary hashtags.
- **Short-form compression trick:** If output still feels over-polished or dressed up, apply the compression pass: *"Cut 20–30% length without losing the core point."*
- **Register protection:** Keep authentic informal texture (short fragments, natural colloquial endings, genuine frustration/humor) intact.

### 3.6 Business Proposals, Emails, & Cover Letters (`business`)
- **Subject / Actor Clarity:** Unlike casual chat, business docs and proposals MUST clearly state **who** performs the action (or explicitly state `"담당자 지정 예정"` if unassigned—never invent a name).
- **Kill empty corporate nouns & hidden verbs:** Replace `"검토를 진행합니다"` → `"검토합니다"`, `"방향성과 반응을 함께 봅니다"` → name the actual metric and action, `"구조적 접근 / 실질적 성과 / 업무 맥락"` → concrete deliverables and numbers.
- **Conclusion first (BLUF):** State the request, deadline, or decision in the first 2 lines.

### 3.7 Spoken Scripts, Narration, & Voiceover Dialogue (`fiction` / `blog` → `voice-directing-mastery`)
- **Deterministic gate routing:** Run `slop_engine.py scan` / `verify` with `--genre fiction` (dialogue, audio drama, character monologue) or `--genre blog` (documentary, YouTube, podcast narration) on clean plain text **before** injecting engine performance tags (`[...]`, `<...>`, `|...|`) so tag tokens do not distort text-diff metrics.
- **Kill written-essay stiffness ("입이 걸리는 문장"):** Break stacked noun modifiers and multi-clause written sentences into natural single-breath clauses; strip robotic connective chains (`더 나아가 / 뿐만 아니라 / Furthermore`) and replace eye-only formatting (parenthetical citations, slash stacks) with speakable phrasing.
- **Preserve vocal breath, ending cadence, and subtext:** Allow authentic spoken disfluencies (`"어, 음..."`), intentional pauses (`...`, `--`), and clean sentence-ending tone drops (`語尾処理`) instead of over-polishing dialogue into sterile textbook prose.
- **Optional handoff to `voice-directing-mastery` (`production` mode, if installed):** Once the plain script passes `verify`, if companion skill `voice-directing-mastery` (`~/.gemini/config/skills/voice-directing-mastery/SKILL.md`) is installed, delegate vocal casting (6-axis Voice Design), Laban/Rodenburg/Navarasa tone directing, and engine-specific tag insertion (ElevenLabs `Eleven v3` / `Multilingual v2` vs Google AI Studio `gemini-3.8-flash-tts`) to it in **`production` mode**. If not installed, skip the handoff and deliver the verified spoken script directly without attempting to load missing companion files.
