# `anti-slop-editor` (4-Language `ko` / `en` / `ja` / `zh` · Gate-Verified Antigravity Skill)

**Research-grounded Antigravity Agent Skill and zero-dependency Python verification engine that removes AI slop (AI투, 번역투, AI臭さ, AI味, structural/RLHF tells, and invisible Unicode artifacts) across Korean, English, Japanese, and Chinese (Simplified & Traditional) without breaking facts, numbers, citations, register, or personal voice.**

Built from primary-source verification across **31+ open-source repositories**, **31 API-verified academic papers**, **Wikipedia `WP:AISIGNS`**, and 4-language editorial fieldwork, then validated with **20/20 automated unit & CLI tests** (including universal UTF-8/UTF-16/UTF-32 stdin & file decoding under Windows CP949 locales) and live dogfooding on its own 44,000-character research encyclopedia (`Slop Score 56 -> 0`, `change_rate 0.8%`, `length_ratio 99.8%`).

---

## Core Design Principles (Five Iron Laws)

1. **Information Conservation:** Keep every number, date, percentage, unit, proper noun, URL, code identifier, direct quote, causal direction, polarity (negation), and epistemic modality (`가능/may` vs `반드시/must`) intact. Never fabricate anecdotes or metrics.
2. **Calibrate to the Human Band (False-Positive Defense):** Never escalate to high-risk from a single metric (such as Korean connective-ending comma density or em-dash count alone). Escalation requires **2+ independent signal families**. Respect literal usage exclusions (`카메라 렌즈`, `화면 잠금 해제`, `벽지 무늬`, `맥을 짚다`) and empirically debunked Chinese X-tier myths (`首先/其次/总之`, `这意味着/这表明`, `赋能/闭环/抓手`).
3. **`Rewrite -> Replace -> Delete` & Over-Edit Caps:** Avoid hollowing out text with blind deletion. In `refactor` mode, changes `> 30%` trigger a warning, changes `> 50%` fail the gate, and length `< 70%` triggers a content-collapse review.
4. **Venue & Voice Precedence:** Match user writing samples over general style rules. Enforce strict register separation across 6 genres (`blog`, `tech`/80% ASD-STE100, `academic`, `fiction`, `sns`, `business`), blocking colloquialization in academic prose (`降重 ≠ 口语化`).
5. **Deterministic Pre-Scan + 7-Gate Post-Rewrite Verification:** Every editing pass is bracketed by `slop_engine.py scan` and `slop_engine.py verify`.

---

## Capabilities

- **4 Operations:**
  - `write`: Identity-First pre-drafting (`Identity -> Facts -> Platform limits -> Scan/Verify`) without form-filling skeletons.
  - `review`: Read-only audit with quoted evidence and targeted fix suggestions (zero edits).
  - `refactor` *(default)*: Minimal surgical edits preserving structure and voice, with optional numbered rollback lists (`수정 목록` / `修订稿`).
  - `recreate`: Bare fact-sheet extraction followed by fresh drafting under genre rules and gate verification.
- **4 Languages (5 Locale Variants):** Korean (`ko`), English (`en`), Japanese (`ja`), Chinese Simplified (`zh-cn`), and Chinese Traditional / Taiwan (`zh-tw`).
- **Zero-Dependency Deterministic Engine (`slop_engine.py`, Python 3 stdlib only):**
  - `scan`: Language & genre auto-detection, protected-span masking (YAML frontmatter, fenced/inline code, LaTeX math, URLs, direct quotes), invisible Unicode detection (`U+202F`, `U+00A0`, `U+200B`–`U+200D`, `U+FEFF`), multi-family pattern scanning with literal exclusion windows, rhythm stats, and `route_hint` (`light` / `standard` / `heavy`).
  - `clean-unicode`: Scrubs invisible Unicode watermarks/artifacts outside code blocks while preserving emoji ZWJ sequences (`👨‍👩‍👧‍👦`).
  - `verify`: Runs 7 deterministic gates (`protected_spans`, `change_rate`, `length_ratio`, `negation_parity`, `epistemic_hedges`, `lexical_regression`, `academic_register`) and exits `1` on any `FAIL`.
  - `diff-report`: Outputs a Markdown before/after metrics table, gate breakdown, and numbered line diffs.

---

## Repository Structure

```text
anti-slop-editor/
├── README.md
├── CONTRIBUTORS.md                                # Role attribution (@devshin-91 & @antigravity-bot)
├── LICENSE                                        # Non-Commercial Source-Available License
├── THIRD_PARTY_NOTICES.md                         # Python stdlib, specs, open-source & paper attributions
├── .gitignore
├── skill/
│   └── anti-slop-editor/                          # Ready-to-install Antigravity Skill
│       ├── SKILL.md
│       ├── references/
│       │   ├── architecture-and-genres.md         # 3-pass structural repair, 6 venue rules + spoken-script handoff, Identity-First
│       │   ├── lang-ko.md                         # Korean tells + context-checked P1/P2 lexical traps
│       │   ├── lang-en.md                         # English Tier A-D tells + 50-point quality rubric
│       │   ├── lang-ja-zh.md                      # Japanese meiseki/textlint + ZH-CN 5.2M-char & ZH-TW rules
│       │   └── voice-persona-template.md          # User writing-sample DNA distillation template
│       └── scripts/
│           ├── slop_engine.py                     # Zero-dep Python stdlib CLI (scan/clean-unicode/verify/diff-report)
│           └── test_slop_engine.py                # 20 unit, false-positive, Unicode I/O, gate, and CLI E2E tests
└── docs/
    ├── ai_slop_removal_encyclopedia.md            # 4-language research encyclopedia (7-layer stack, 31 papers, 31+ repos)
    └── dogfood_diff_report.md                     # Live dogfooding metrics & numbered revision report (56 -> 0)
```

---

## Installation (Antigravity Skill)

Copy `skill/anti-slop-editor/` into your Antigravity skills discovery path:

- **Global (all workspaces):** `~/.gemini/config/skills/anti-slop-editor/`
- **Project-local:** `<workspace>/.agents/skills/anti-slop-editor/`

Once installed, natural requests such as `"이 글에서 AI투랑 번역투 빼줘"`, `"AI 티 검사만 해줘"`, `"humanize this README under STE80"`, or `"去AI味并给出修订稿"` trigger the skill automatically.

---

## CLI & Verification Tests

```bash
# 1. Run all 20 automated unit & CLI tests (Python 3 stdlib only)
python -B skill/anti-slop-editor/scripts/test_slop_engine.py -v

# 2. Pre-scan a draft
python -B skill/anti-slop-editor/scripts/slop_engine.py scan draft.md --genre auto

# 3. Clean invisible Unicode artifacts outside code blocks
python -B skill/anti-slop-editor/scripts/slop_engine.py clean-unicode draft.md --out draft_clean.md

# 4. Run 7-gate deterministic verification after editing
python -B skill/anti-slop-editor/scripts/slop_engine.py verify --before draft_clean.md --after edited.md --genre auto --mode refactor

# 5. Generate Markdown diff and metrics report
python -B skill/anti-slop-editor/scripts/slop_engine.py diff-report --before draft_clean.md --after edited.md --genre auto --mode refactor
```

---

## Validation & Dogfooding Results

| Check | Result |
| :--- | :--- |
| Automated Test Suite (`test_slop_engine.py`) | **20 / 20 OK** (`covering 4-language detection, Korean literal-context false-positive immunity, single-metric comma-rate immunity, Chinese X-tier immunity, protected zones, emoji ZWJ preservation, universal UTF-8/UTF-16/UTF-32 stdin & file decoding under CP949 locales, all 7 verify gates, and 4 CLI subcommands`) |
| Live Dogfooding on [`docs/ai_slop_removal_encyclopedia.md`](./docs/ai_slop_removal_encyclopedia.md) | **Slop Score `56 -> 0`**, active families **`3 -> 0`**, change rate **`0.8%`**, length ratio **`99.8%`**, **`protected_spans` / `lexical_regression` / `epistemic_hedges` / `academic_register` all `PASS`** (see [`docs/dogfood_diff_report.md`](./docs/dogfood_diff_report.md)) |

---

## Contributors, Third-Party Notices & License

- **Contributors & Role Attribution:** See [`CONTRIBUTORS.md`](./CONTRIBUTORS.md).
- **Third-Party Notices:** See [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md).
- **License:** Distributed under the **Non-Commercial Source-Available License** — see [`LICENSE`](./LICENSE).
