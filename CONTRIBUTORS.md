# Contributors & Role Attribution (기여자 및 역할 분담)

**[한국어](#korean) | [English](#english)**

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Research Director & Governance Lead** | 4-language (`ko`/`en`/`ja`/`zh`) cross-media research mandate (SNS, academic papers, articles, open-source skills), Phase 1/2 scoping (prioritizing authenticated **Threads** & **Naver Cafe** inspection while respecting paywalls and anti-bot controls), human-consented desktop Chrome remote debugging access, global Antigravity skill direction, **live dogfooding directive** that cleaned the encyclopedia (`56 -> 0`) and uncovered a Korean word-boundary false positive in `slop_engine.py`, private release governance (Non-Commercial License, role attribution, Third-Party Notices, Zero-PII) |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Multilingual Researcher & Verification Engineer** | Primary-source verification across 31+ GitHub repos (live stars & raw `SKILL.md`/`README.md` inspection), 31 academic papers (OpenAlex/arXiv DOIs), and Wikipedia `WP:AISIGNS` API; public SNS browser audit + consented Chrome DevTools MCP harvest (Threads & Naver Cafe); [`docs/ai_slop_removal_encyclopedia.md`](./docs/ai_slop_removal_encyclopedia.md); [`skill/anti-slop-editor/`](./skill/anti-slop-editor/) (`SKILL.md`, 5 references, zero-dep stdlib `slop_engine.py` with 4 CLI commands & 7 verification gates, 19-test suite `test_slop_engine.py`); 2-pass dogfooding edit, boundary regex fix, and Zero-PII repo packaging |

---

<a id="korean"></a>
## 기여자 및 역할 분담 (Korean)

본 프로젝트(**`anti-slop-editor`**)는 인간 프로젝트 소유자의 4개국어 리서치 기획·수집 범위 결정·인증 브라우저 접근 승인·도그푸딩 검증 지시·배포 거버넌스 확정과, **Google Antigravity (AGY)** 플랫폼에서 협업한 AI 에이전트·브라우저 서브에이전트의 원문 검증·스킬 구현·결정론적 파이썬 엔진 개발·테스트 검증으로 완성했습니다.

### 1. Human Project Owner, Research Director & Governance Lead
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **핵심 기여 역할:**
  1. **전방위 4개국어 리서치 방향 수립:**
     - 한국어·영어·일본어·중국어(간체/번체) 구분 없이 논문, 기사, 웹 문서, 오픈소스 스킬, SNS 커뮤니티 전반의 AI Slop 제거 기법을 수집하도록 목표를 정의했습니다.
     - 로그인 벽·안티봇 검증·유료 페이월로 막히는 출처를 숨기지 않고 투명하게 보고하도록 원칙을 세웠습니다.
  2. **1·2단계 실행 범위 및 우선순위 확정:**
     - 1단계(추가 SNS 수집·백과사전 병합)와 2단계(Antigravity 전역 스킬 + 결정론적 파이썬 검증 스크립트 구축) 일괄 실행을 승인했습니다.
     - 차단 출처 가운데 한국어·중화권 실무 밀도가 높은 **Threads**와 **네이버 카페**로 1단계 로그인 수집 범위를 명확히 한정했습니다.
  3. **인간 동의 기반 인증 접근 제공 및 보안 경계 준수:**
     - 우회 방식 대신 본인 데스크톱 Google Chrome에 직접 로그인한 뒤 로컬 원격 디버깅(`chrome://inspect/#remote-debugging`)을 수동으로 허용하여, 정당한 권한 범위 내에서 Threads와 네이버 카페를 검증할 수 있도록 지원했습니다.
  4. **도그푸딩(Dogfooding) 실전 검증 지시:**
     - 완성된 `anti-slop-editor` 스킬을 리서치 산출물 백과사전 본문에 직접 적용하도록 지시하여, 2패스 윤문(`Slop Score 56 -> 0`)과 동시에 `slop_engine.py` 학술 문체 게이트의 한국어 어절 경계 오탐(`불완전주의` 내 `완전`)을 실전에서 발견·수정하게 이끌었습니다.
  5. **저장소 및 라이선스 거버넌스:**
     - 비공개 저장소 배포, 기여자 역할 분리 표기, 비상업적 소스 공개 라이선스([`LICENSE`](./LICENSE)), 서드파티 고지([`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)), 개인 로컬 경로·PII 배제 원칙을 확정했습니다.

### 2. AI Engineering, Multilingual Research & Verification Partner (`Google Antigravity`)
* **플랫폼 & 계정:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **세부 역할 및 참여 에이전트:**
  * **Main Orchestrator & Skill/Engine Co-Developer (`Google Antigravity`):**
    - GitHub REST API(31개 이상 저장소 실시간 스타·원문 `SKILL.md`/`README.md` 20여 편 열람), OpenAlex/arXiv API(31편 학술 논문 DOI·서지 검증), Wikipedia MediaWiki API(`WP:AISIGNS` 목차 검증)를 이용한 1차 출처 팩트체크를 수행했습니다.
    - 사용자 동의 하에 Chrome DevTools MCP로 Threads 6개 다국어 검색어·바이럴 스레드 및 네이버 카페 공개/가입전용 경계를 점검하고 임시 탭을 정리했습니다.
    - [`docs/ai_slop_removal_encyclopedia.md`](./docs/ai_slop_removal_encyclopedia.md)(7계층 제거 스택, 4개 언어권 비교, 저장소 카탈로그, 검증 논문 색인, 9대 역효과)를 집필하고 `anti-slop-editor` 2패스 도그푸딩 윤문 및 리포트([`docs/dogfood_diff_report.md`](./docs/dogfood_diff_report.md))를 생성했습니다.
    - [`skill/anti-slop-editor/`](./skill/anti-slop-editor/) 전체(`SKILL.md`, 5개 점진적 로딩 레퍼런스, 외부 의존성 없는 Python 표준 라이브러리 엔진 `slop_engine.py` 4개 CLI 커맨드·7개 검증 게이트, 19개 단위·통합 테스트 `test_slop_engine.py`)를 구현하고, 도그푸딩 중 발견된 `academic_register` 정규식 경계 버그를 수정했습니다.
  * **SNS & Community Research Browser Subagent (`Gemini Flash`, Antigravity `browser` subagent):**
    - Reddit(`r/LocalLLaMA`, `r/WritingWithAI`), X, Note.com, GPTERS, ArcaLive(`arca.live/b/characterai`), SOV2EX(`sov2ex.com`), 네이버 카페 공개글을 점검하고, 우회 없이 차단 호스트(`zhihu.com`, `nytimes.com`, 비로그인 `threads.com`)의 접근 제한 사유를 확인했습니다.

### 3. 인간 최종 책임 및 투명한 AI 기여 표기 원칙
본 저장소의 리서치 방향, 정책 확정, 라이선스 및 비공개 배포의 최종 책임은 프로젝트 소유자([`@devshin-91`](https://github.com/devshin-91))에게 있습니다. AI 파트너([`@antigravity-bot`](https://github.com/antigravity-bot))의 리서치·구현·테스트 기여는 Git 커밋 메타데이터(`Author` / `Co-authored-by`)와 본 문서에 투명하게 기록합니다.

---

<a id="english"></a>
## Contributors & Role Attribution (English)

### 1. Human Project Owner, Research Director & Governance Lead
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **Contributions:**
  - Defined the 4-language (`ko`/`en`/`ja`/`zh`) cross-media research mandate spanning SNS, academic papers, articles, open-source skills, and technical docs, with mandatory transparent reporting of blocked sources.
  - Scoped Phase 1/2 execution: narrowed login-gated Phase 1 community inspection to **Threads** and **Naver Cafe** while leaving paywalled and anti-bot-gated sites untouched.
  - Provided consented authenticated access via local Chrome remote debugging (`chrome://inspect/#remote-debugging`) so Threads and Naver Cafe could be inspected strictly within authorized session boundaries.
  - Directed live dogfooding of `anti-slop-editor` on the research encyclopedia (`Score 56 -> 0`), uncovering a real Korean word-boundary false positive in `slop_engine.py` (`academic_register`).
  - Established private repository governance, Non-Commercial Source-Available licensing ([`LICENSE`](./LICENSE)), third-party attributions ([`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)), and Zero-PII / portable-path release standards.

### 2. AI Engineering, Multilingual Research & Verification Partner (`Google Antigravity`)
* **Platform & Attribution:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **Sub-roles & Contributions:**
  - **Main Orchestrator & Skill/Engine Co-Developer (`Google Antigravity`):** Executed API-verified primary-source research (31+ GitHub repos, 31 OpenAlex/arXiv papers, Wikipedia `WP:AISIGNS`), performed consented Chrome DevTools MCP harvesting for Threads & Naver Cafe, authored [`skill/anti-slop-editor/`](./skill/anti-slop-editor/) (`SKILL.md`, 5 references, zero-dependency stdlib `slop_engine.py`, 19-test suite `test_slop_engine.py`), authored and dogfood-cleaned [`docs/ai_slop_removal_encyclopedia.md`](./docs/ai_slop_removal_encyclopedia.md), fixed the `academic_register` boundary regex bug, and prepared Zero-PII repository packaging.
  - **SNS & Community Research Browser Subagent (`Gemini Flash`, Antigravity `browser` subagent):** Inspected public community posts across Reddit, X, Note.com, GPTERS, ArcaLive, SOV2EX, and public Naver Cafe threads, and documented login/anti-bot walls without bypassing access controls.
