# Third-Party Notices & Attributions

This repository (`anti-slop-editor`) is an **independent, clean-room implementation**
that bundles **zero third-party Python packages** and vendors **no third-party source code**.
All runtime scripts rely solely on the Python 3 Standard Library. The runtime environment,
platform specifications, editorial standards, open-source repositories, academic papers,
and public community sources studied during research and design are transparently
acknowledged below.

---

## 1. Runtime Environment & Standard Library

### Python 3 Standard Library (`argparse`, `collections`, `dataclasses`, `difflib`, `json`, `math`, `pathlib`, `re`, `subprocess`, `sys`, `tempfile`, `unicodedata`, `unittest`)
- **Provider:** Python Software Foundation (PSF)
- **License:** Python Software Foundation License Version 2 (PSF-2.0)
- **URL:** https://docs.python.org/3/license.html
- **Usage:** Deterministic 4-language scanner, Unicode artifact scrubber, 7-gate verifier, Markdown diff reporter (`skill/anti-slop-editor/scripts/slop_engine.py`), and 19-test suite (`test_slop_engine.py`). Not redistributed in this repository.

---

## 2. Platform Specifications & Public Editorial Standards Referenced

1. **Google Antigravity Agent Skill Format (`SKILL.md`)**
   - **Provider:** Google / Antigravity Platform
   - **URL:** https://antigravity.google/docs/skills
   - **Usage:** Skill directory structure (`SKILL.md`, `references/`, `scripts/`) and YAML frontmatter progressive-disclosure conventions.
2. **Wikipedia: `Wikipedia:Signs of AI writing` (`WP:AISIGNS`, WikiProject AI Cleanup)**
   - **Provider:** Wikipedia Contributors
   - **License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
   - **URL:** https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
   - **Usage:** Taxonomy reference for English AI-writing indicators and 2026 historical-indicator shifts (summarized analytically in `docs/ai_slop_removal_encyclopedia.md` and `references/lang-en.md`; no Wikipedia text is redistributed verbatim).
3. **ASD-STE100 Simplified Technical English Specification**
   - **Maintainer:** AeroSpace and Defence Industries Association of Europe (ASD)
   - **URL:** https://www.asd-ste100.org/
   - **Usage:** Referenced conceptually (via Andrej Karpathy's 80% pragmatic technical-writing adaptation) for technical clarity guidelines in `references/architecture-and-genres.md`. ASD-STE100 specifications and dictionaries are not bundled.

---

## 3. Open-Source Projects Studied (Clean-Room Design Synthesis — No Code Vendored)

No code, JSON dictionaries, or prompt files were copied or redistributed from the projects below.
Empirical findings, design lessons, and architectural patterns observed in their public
documentation informed our independent 4-language taxonomy and verification gates:

| Repository | Language | Concept / Finding Acknowledged |
| :--- | :--- | :--- |
| [`blader/humanizer`](https://github.com/blader/humanizer) | EN | Tiered staging-vs-stating taxonomy, 2-pass surviving-tell audit, prompt-injection security boundary, informal-register whitelist |
| [`hardikpandya/stop-slop`](https://github.com/hardikpandya/stop-slop) | EN | 5-dimension 50-point quality rubric (`< 35` revision trigger), inanimate false agency, pull-quote removal |
| [`Dodaios/ste80-humanizer`](https://github.com/Dodaios/ste80-humanizer) | EN | Two-pass de-slop + 80% ASD-STE100 structural clarity pipeline |
| [`harshaneel/humanize`](https://github.com/harshaneel/humanize) | EN | 9 research-backed humanization levers including RLHF-voice removal |
| [`Nanako0129/sepia`](https://github.com/Nanako0129/sepia) | EN/ZH | Identity-First 4-step pre-drafting order, StoryScope 3-pass calibration (moderate human band, never full inversion), Taiwan journalism reference |
| [`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai) | KO | Multi-family false-positive prevention (2+ independent signal families), context-checked Korean lexical traps (`keep_when` literal exclusions), P1 lexical regression guard, `route_hint` routing |
| [`DaleSeo/korean-skills`](https://github.com/DaleSeo/korean-skills) | KO | KatFishNet-informed Korean editing order (`humanizer -> grammar -> style-guide`) |
| [`textlint-ja/textlint-rule-preset-ai-writing`](https://github.com/textlint-ja/textlint-rule-preset-ai-writing) | JA | Structural-constraint principle ("constrain structure, not creativity") and predicate+colon detection |
| [`bamboo-nova/meiseki`](https://github.com/bamboo-nova/meiseki) | JA | Reading-load reduction for neutral technical prose and negation-parity meaning verification (`check:meaning`) |
| [`gonta223/humanizer-ja`](https://github.com/gonta223/humanizer-ja) / [`iKora128/stop-ai-slop-jp`](https://github.com/iKora128/stop-ai-slop-jp) | JA | Japanese boilerplate/hype expression cataloging |
| [`larashero3-dotcom/lieflat-less-ai-tone`](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) | ZH-CN | 5.2M-character empirical Chinese corpus findings, model-divergent fingerprints (Claude vs GPT em-dash direction), and X-tier debunked-myth exclusions |
| [`MrGeDiao/shuorenhua`](https://github.com/MrGeDiao/shuorenhua) | ZH-CN | Protected-term declaration and numbered rollback revision-list contract |
| [`xiaofenggan01/aigc-reduce`](https://github.com/xiaofenggan01/aigc-reduce) / [`AIScientists-Dev/academic-humanizer`](https://github.com/AIScientists-Dev/academic-humanizer) | ZH/EN | Scholarly register floor (blocking colloquialization in academic papers) and evidence-tied claim calibration |
| [`op7418/Humanizer-zh`](https://github.com/op7418/Humanizer-zh) / [`Raymondhou0917/speak-human-tw`](https://github.com/Raymondhou0917/speak-human-tw) | ZH-CN/TW | Chinese anti-slop baseline and Taiwan terminology / full-width punctuation normalization |
| [`sam-paech/antislop-sampler`](https://github.com/sam-paech/antislop-sampler) / [`seyedehsanhadi/sloptrim`](https://github.com/seyedehsanhadi/sloptrim) / [`devswha/patina`](https://github.com/devswha/patina) | EN/Multi | Decoding-level backtracking context, zero-dep local linting, and meaning-preservation gating concepts |

---

## 4. Academic Literature & Community References Cited

`docs/ai_slop_removal_encyclopedia.md` cites 31 API-verified academic papers (including `KatFishNet` ACL 2025 `doi:10.18653/v1/2025.acl-long.1030`, `StoryScope` `arXiv:2604.03136`, `SlopShape` `arXiv:2609.15369`, `Base Models Look Human` `arXiv:2605.19516`, `Antislop / FTPO` ICLR 2026 `arXiv:2510.15061`, `Verbalized Sampling` `arXiv:2510.01171`, `LAMP` CHI 2025 `doi:10.1145/3706598.3713559`, `Adversarial Paraphrasing` NeurIPS 2025 `doi:10.52202/085713-1588`, `HyPerAlign` `arXiv:2505.00038`, and `SciSlopBench` `arXiv:2610.00531`) along with publicly accessible community fieldwork from Reddit, X, Note.com, GPTERS, ArcaLive, SOV2EX, Threads, and open Naver Cafe posts.

- **Ownership & Scope:** All third-party trademarks, repository names, publication titles, and original writings remain the sole property of their respective authors, publishers, and platforms. Short analytical summaries and citations are included strictly for non-commercial research attribution.
