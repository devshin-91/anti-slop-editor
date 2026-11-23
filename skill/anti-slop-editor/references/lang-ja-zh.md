# Japanese & Chinese (Simplified + Traditional) Anti-Slop Reference (`lang: ja / zh-cn / zh-tw`)

---

## Part I — Japanese (`lang: ja`)

Synthesizes `@textlint-ja/preset-ai-writing` (1.16k★), `bamboo-nova/meiseki`, `gonta223/humanizer-ja`,
`iKora128/stop-ai-slop-jp`, and Note.com editorial practice (`モノぐさ@AI活用`, `猿打 鍵`).

### 1. Structural & Reading-Load Priority Tiers (`meiseki` A→F + `textlint` Structural Principle)
Principle: **「表現を縛るのではなく、構造を縛る」** (Constrain structure, not creativity).

- **Tier A — Double Negatives & Nested Conditionals:** Collapse `〜ないとは言えません` → `〜ことがあります` / `〜と言えます`. **Guard:** Count negation parity per paragraph so collapsing a double negative never accidentally inverts polarity!
- **Tier B — Long Pre-Noun Modifiers & Passive Bloat:** Shorten sentences >90 chars or with >3 commas (`、`); bring distant subject–predicate pairs closer; change weak passive (`再送が行われる`) to active (`クライアントが再送する`).
- **Tier C — Nominalization & `の` Chains:** Break heavy kanji/noun chains (`リトライ回数の上限の設定の検討`) into clear verbs (`リトライ上限をどう決めるか検討する`).
- **Tier D — Boilerplate Openers, Closers & Redundancy:**
  - Cut `本記事では〜について解説します`, `近年、〜の中で重要な課題となっています`, `いかがでしたでしょうか`, `〜と言えるでしょう`, `お役に立てれば幸いです`.
  - Trim `〜することができます` → `〜できます` / `〜します`; trim mechanical connectors (`これにより`, `したがって`, `さらに`, `また、`) when context carries the logic.
- **Tier E — English-Style Formatting & Colon Continuation (`textlint`):**
  - Replace predicate+colon before lists/code (`実行します:\n- ...`) with natural Japanese (`実行方法は以下の通りです。`), while keeping noun+colon (`使用方法:`).
  - Strip decorative `- **重要**: ...`, emoji bullets (`✅❌💡🚀🎯`), bold inside headings, and full-width dashes (`──`).
- **Tier F — Hype Words & Business Clichés:**
  - Replace `革命的`, `ゲームチェンジャー`, `パラダイムシフト`, `スーパーチャージ`, `可能性を解き放つ`, `包括的`, `シームレス`, `ダイナミック`, `泥臭さ`, `解像度`, `本質`, and false agency (abstract nouns performing human actions).

### 2. Two Distinct Japanese Modes (Choose by Genre!)
- **Neutral Clarity Mode (`meiseki`, for tech docs/README/specs):** Strip reading load *without* adding `"自分は"` or fake opinions. Protect numbers, identifiers, conditions (`場合/ただし/のみ`), and certainty markers (`ことがある/べき/常に`).
- **Editorial Voice Mode (`blog`/`note`/`SNS`):** Inject explicit expressive intent (`表現意図`), real failures/measurements, and concrete stance instead of safe both-sides hedging (`〜という意見もありますが`). Enforce **`Rewrite → Replace → Delete`** and a **70% length floor** so aggressive pruning never hollows out the article.

---

## Part II — Chinese Simplified (`lang: zh-cn`) & Traditional/Taiwan (`lang: zh-tw`)

Synthesizes the **5.2M-character empirical corpus study** (`lieflat-less-ai-tone` 8.6k★),
`MrGeDiao/shuorenhua` (2.7k★), `xiaofenggan01/aigc-reduce` (758★), `op7418/Humanizer-zh` (23.5k★),
`Raymondhou0917/speak-human-tw` (1.2k★), `sepia/zh.md`, and Threads/V2EX fieldwork.

### 1. Empirically Proven Universal Chinese AI Tells (Fix These — Paired-Corpus Verified)
1. **翻案腔 / 欧化对举 (`不是A而是B`, `并非…而是…`, `与其说…不如说…`, `表面…实际…`, `你以为…其实…`):** Strongest pure writing signal (`δ +0.88 GPT / +0.72 Opus`). State the judgment directly.
2. **同义重命名 (Synonym Cycling, MTLD/MATTR `δ +0.91/+0.55`):** Humans repeat the same clean word; AI rotates `优化/增强/提升/提高` or `版图/基地/项目/节点` for one entity within a paragraph. Unify back to one clear term.
3. **结论提示冒号 (`核心是：`, `残酷的现实是：`, `一句话总结：`, `关键在于：` — 2.1× AI):** Delete the announcer or swap the colon for a period/comma. *(Keep normal quotes, headings, and colon-before-list intros!)*
4. **起手式 (`说白了`, `说穿了`, `先说结论`):** Delete and deliver the point directly.
5. **四种实证翻译腔:**
   - 过长前置定语 (>15 chars or 2+ `的` before head noun) → split into two clauses.
   - `当……时` front-loaded clause → drop `当/时` unless exact timing becomes ambiguous.
   - 前置话题壳 (`对于……来说`, `就……而言`, `在……方面`) when the same noun is already the subject → strip shell.
   - 句首连接词路标 (`然而，`, `因此，`, `此外，`) repeated across consecutive paragraphs → move after subject or drop.
6. **密集顿号/分号罗列 (`1.45× AI`) & 相邻句高度同构三连 (`2.75× AI`):** Merge/rephrase one item to break mechanical skeleton cloning.
7. **衔接连环过长 (≥6 consecutive explicit paragraph bridges — 93% AI):** Allow 1–2 natural topic jumps instead of chaining `这也解释了为什么… / 从这个角度看…`.
8. **结构切得太碎 (AI median 7 micro-sections vs Human 1):** Only flag in `review`/`recreate`; do not break structure in `refactor` unless user approves.

### 2. X-Tier Debunked Myths (DO NOT Auto-Edit!)
Paired-corpus re-testing (270 matched pairs) proved these popular blacklist items are **invalid or reversed** on modern 2026 models:
- ❌ `"首先/其次/总之"` (`δ = +0.02`, obsolete) — only edit if genuinely clunky, never auto-flag.
- ❌ `"赋能/闭环/抓手"` (`δ = +0.10`, topic-dependent) — keep when real domain/discussed terms; only translate to plain speech in explicit `彻底清理黑话 / 修订稿` mode.
- ❌ `"这意味着/这表明"` (humans use MORE!) — do NOT strip.
- ❌ Ordinal subheadings (`一、二、三`) & `"以下几种场景："` list intros (humans use MORE!) — do NOT strip.
- ❌ Artificially alternating short/long sentences ("机械参差化") — worse than not editing.

### 3. Model-Divergent Fingerprints (Interpret Directionally, Never Force to Zero)
- **破折号 (`——`):** High in Claude (`δ +0.95`), *lower* than humans in GPT (`δ −0.54`). Prioritize fixing only when density >2 per 1,000 chars or used as theatrical pause (`答案很简单——专注` → `答案是专注`).
- **分号 (`；`) & 单动词句缺失:** GPT-skewed; split multi-tier semicolon chains into clean periods where safe.
- **比喻贴切度 (Human-Review Zone — `H` Tier):** LLMs show only 0–40% inter-model agreement on metaphor quality. Flag suspicious grand metaphors (`窄门/三根支柱`) for human review rather than silently deleting valid author imagery.

### 4. Academic Chinese (`aigc-reduce`) & Revision-List Mode (`shuorenhua`)
- **Academic hard rule:** Never rewrite an entire paper in one AI pass (compounds AI fingerprint). Edit paragraph-by-paragraph structurally (word order, voice, clause splitting) while keeping formal academic written Chinese (`书面学术语体`) and protecting all citations/terms/formulas.
- **Revision-list mode (`修订稿`):** Declare `不动:` (untouchable domain terms & author coinages) first, tag every edit `[等义]` / `[猜的]` / `[删除]` / `[校对]`, and allow exact rollback (`撤销 2、5` / `撤销所有猜的`).

### 5. Traditional Chinese / Taiwan Specifics (`lang: zh-tw`, `speak-human-tw` & `sepia/tw-journalism`)
- Convert Mainland corporate/tech terms to Taiwan usage when writing for Taiwan readers (`软件→軟體`, `视频→影片`, `信息→資訊`, `优化→優化/改善`, `项目→專案`, `数据→資料/數據`, `赋能/抓手/闭环` → plain Taiwanese phrasing).
- Normalize half-width punctuation mixed into Chinese prose (`!` `,` `:` `?` → full-width `！`，`：`，`？`, keeping proper spacing around English/numbers).
- Strip hollow inspirational endings (`讓我們一起攜手迎向未來`); cut at least half of redundant glue transitions (`然而/因此/此外/同時`).
