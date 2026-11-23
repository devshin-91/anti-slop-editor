# Anti-Slop Diff & Metrics Report (`WARN`)

## 1. Before vs. After Metrics

| Metric | Before | After |
|---|---:|---:|
| Language / Genre | `ko` / `academic` | `ko` / `academic` |
| Characters | 44124 | 44044 (99.8%) |
| Sentences (avg / CV) | 338 (72.09 / 0.68) | 338 (72.03 / 0.683) |
| Invisible Unicode | 0 | 0 |
| Active Signal Families | 3 (translationese_syntax, lexical_traps, formatting_decoration) | 0 (none) |
| Slop Score / Risk | 56 (`high`) | 0 (`low`) |
| Route Hint | `heavy` | `heavy` |
| Character Change Rate | — | 0.8% |

## 2. Deterministic Verification Gates

| Gate | Status | Details |
|---|---|---|
| `protected_spans` | **`PASS`** | All numbers, URLs, code blocks, and direct quotes preserved. |
| `change_rate` | **`PASS`** | Change rate 0.8% is within surgical refactor band (<=30%). |
| `length_ratio` | **`PASS`** | Length ratio 99.8% is within healthy bounds (70%–135%). |
| `negation_parity` | **`WARN`** | Odd negation delta (46 -> 43, delta -3) — verify polarity was not accidentally inverted (acceptable if a 'Not X, but Y' contrast was cleanly flattened). |
| `epistemic_hedges` | **`PASS`** | Epistemic modality balanced (hedges 16->15, certainty 9->8). |
| `lexical_regression` | **`PASS`** | Zero new P1 AI lexical traps introduced. |
| `academic_register` | **`PASS`** | Formal scholarly register preserved. |

## 3. Numbered Revisions

### [1] `replace` (L1–L1)
- **Before:** # 글로벌 AI Slop(AI 투·AI 냄새·AI 味) 제거 스킬 및 기법 총망라 백과사전 (EN · KO · JA · ZH)
+ **After:** # 글로벌 AI Slop(AI 투·AI 냄새·AI 味) 제거 스킬·기법 백과사전 (EN · KO · JA · ZH)

### [2] `replace` (L7–L9)
- **Before:** ## 1. 핵심 요약: 2024 → 2026 AI Slop 제거의 3대 패러다임 전환
- **Before:** 
- **Before:** 초기(2023~2024)의 *"delve, tapestry 같은 금지어 목록을 프롬프트에 넣는다"* 방식은 **2025~2026년 대규모 실증 연구에 의해 사실상 한계가 증명**되었습니다. 현재 최전선(GitHub 오픈소스 스킬 · ICLR/NeurIPS/CHI/PNAS 논문 · 로컬 LLM 커뮤니티)을 관통하는 3대 전환점은 다음과 같습니다.
+ **After:** ## 1. 핵심 요약: 2024 → 2026 AI Slop 제거의 3가지 변화
+ **After:** 
+ **After:** 2023~2024년에 널리 쓰인 *"delve, tapestry 같은 금지어 목록을 프롬프트에 넣는다"* 방식은 **2025~2026년 대규모 실증 연구에서 한계가 드러났습니다.** GitHub 오픈소스 스킬, ICLR·NeurIPS·CHI·PNAS 논문, 로컬 LLM 커뮤니티에서 공통으로 확인된 3가지 변화는 다음과 같습니다.

### [3] `replace` (L12–L14)
- **Before:** > **2026년 3대 실증적 반전**
- **Before:** > 1. **어휘보다 서사·구조 지문이 압도적이다 (`StoryScope`, `arXiv:2604.03136` / `SlopShape`, `arXiv:2609.15369`):** 61,608편의 소설 대조 연구에서 인간 편집자가 표층 문체·상투어를 완전히 고친 뒤에도, 서사 구조만 보는 분류기의 AI 탐지율은 **95.5% → 93.9%**로 겨우 1.6%p만 떨어졌습니다. 기업 블로그 2,250편 vs AI 미러 11,250편 대조에서도 구조 특징만으로 **98.0 macro-F1**로 분리되었습니다.
- **Before:** > 2. **탐지기가 잡는 것은 'AI 자체'가 아니라 'RLHF/지시 튜닝 문체'다 (`Base Models Look Human`, `arXiv:2605.19516`):** 비튜닝 베이스 모델의 출력은 현행 SOTA 탐지기에서 인간 글로 판정됩니다. 실제로 탐지기와 독자가 거부감을 느끼는 것은 RLHF가 심어 넣은 *과잉 정중함, 양비론 균형 맞추기, 과잉 목록화, 도우미 어조*입니다.
+ **After:** > **2026년 실증 연구의 3가지 발견**
+ **After:** > 1. **어휘보다 서사·구조 지문이 훨씬 강하다 (`StoryScope`, `arXiv:2604.03136` / `SlopShape`, `arXiv:2609.15369`):** 61,608편의 소설 대조 연구에서 인간 편집자가 표층 문체·상투어를 모두 고친 뒤에도, 서사 구조만 보는 분류기의 AI 탐지율은 **95.5% → 93.9%**로 겨우 1.6%p만 떨어졌습니다. 기업 블로그 2,250편 vs AI 미러 11,250편 대조에서도 구조 특징만으로 **98.0 macro-F1**로 분리되었습니다.
+ **After:** > 2. **탐지기가 잡는 것은 'AI 자체'가 아니라 'RLHF/지시 튜닝 문체'다 (`Base Models Look Human`, `arXiv:2605.19516`):** 비튜닝 베이스 모델의 출력은 현행 SOTA 탐지기에서 인간 글로 판정됩니다. 실제로 탐지기와 독자가 거부감을 느끼는 요소는 RLHF가 만든 *과잉 정중함, 양비론 균형 맞추기, 과잉 목록화, 도우미 어조*입니다.

### [4] `replace` (L16–L16)
- **Before:** >    - 2026년 중국어 520만 자 실측에서 엠대시(`——`)는 **Claude Opus 4.6에서 δ = +0.95(전편 등장)**인 반면 **GPT-5.6에서는 δ = −0.54(인간보다 적음)**으로 방향이 완전히 반대였습니다.
+ **After:** >    - 2026년 중국어 520만 자 실측에서 엠대시(`——`)는 **Claude Opus 4.6에서 δ = +0.95(전편 등장)**인 반면 **GPT-5.6에서는 δ = −0.54(인간보다 적음)**으로 방향이 정반대였습니다.

### [5] `replace` (L36–L36)
- **Before:** ## 2. 7계층별 전체 제거 기법 완전 분해
+ **After:** ## 2. 7계층별 제거 기법 상세

### [6] `replace` (L40–L42)
- **Before:** 프롬프트나 후처리가 아닌 **모델 자체의 Slop 생성 성향을 제거**하는 가장 근본적인 계층입니다.
- **Before:** 
- **Before:** 1. **FTPO (Final Token Preference Optimization)** — Paech et al., ICLR 2026 ([arXiv:2510.15061](https://doi.org/10.48550/arxiv.2510.15061))
+ **After:** **모델 자체의 Slop 생성 성향을 직접 줄이는** 계층입니다.
+ **After:** 
+ **After:** 1. **FTPO (Final Token Preference Optimization)** (Paech et al., ICLR 2026, [arXiv:2510.15061](https://doi.org/10.48550/arxiv.2510.15061))

### [7] `replace` (L44–L45)
- **Before:**    - FTPO는 추론 트레이스에서 금지 패턴이 촉발되는 **최종 분기 토큰의 로짓(logit)만 외과적으로 선호도 최적화**하여, 일반 벤치마크 성능을 유지·향상시키면서 반복적 Slop만 대폭 억제합니다.
- **Before:** 2. **학습 없는 활성화 방향 절제 (Activation Abliteration for Slop)** — `u/-p-e-w-` ([r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1qa0w6c/it_works_abliteration_can_reduce_slop_without/), `p-e-w/heretic`)
+ **After:**    - FTPO는 추론 트레이스에서 금지 패턴이 촉발되는 **최종 분기 토큰의 로짓(logit)만 선별해 선호도 최적화**함으로써 일반 벤치마크 성능을 유지·향상시키면서 반복적 Slop만 크게 억제합니다.
+ **After:** 2. **학습 없는 활성화 방향 절제 (Activation Abliteration for Slop)** (`u/-p-e-w-`, [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1qa0w6c/it_works_abliteration_can_reduce_slop_without/), `p-e-w/heretic`)

### [8] `replace` (L47–L48)
- **Before:**    - *화려한 Slop 프롬프트* vs *건조한 Non-Slop 프롬프트* 대조쌍을 주입해 잔차 스트림(residual stream)에서 Slop 벡터 방향(예: Mistral Nemo 7~10층)을 도려내어 **파인튜닝 없이** 과잉 수식·클리셰를 제거합니다(`p-e-w/Mistral-Nemo-Instruct-2407-heretic-noslop`).
- **Before:** 3. **역-슬롭화 파인튜닝 (Reverse-Enslop Training)** — `u/N8Karma` ([r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1qd88v2/i_trained_a_model_to_unslop_ai_prose/))
+ **After:**    - *화려한 Slop 프롬프트* vs *건조한 Non-Slop 프롬프트* 대조쌍을 주입해 잔차 스트림(residual stream)에서 Slop 벡터 방향(예: Mistral Nemo 7~10층)을 제거하여 **파인튜닝 없이** 과잉 수식·클리셰를 줄입니다(`p-e-w/Mistral-Nemo-Instruct-2407-heretic-noslop`).
+ **After:** 3. **역-슬롭화 파인튜닝 (Reverse-Enslop Training)** (`u/N8Karma`, [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1qd88v2/i_trained_a_model_to_unslop_ai_prose/))

### [9] `replace` (L50–L50)
- **Before:** 4. **편집 기반 글쓰기 보상 정렬 (Edit-Based Writing Rewards / LAMP)** — Chakrabarty, Laban, & Wu, CHI 2025 ([doi:10.1145/3706598.3713559](https://doi.org/10.1145/3706598.3713559))
+ **After:** 4. **편집 기반 글쓰기 보상 정렬 (Edit-Based Writing Rewards / LAMP)** (Chakrabarty, Laban, & Wu, CHI 2025, [doi:10.1145/3706598.3713559](https://doi.org/10.1145/3706598.3713559))

### [10] `replace` (L52–L52)
- **Before:** 5. **베이스 모델(Non-RLHF) 패러프레이징** — Xu et al., 2026 ([arXiv:2605.19516](https://doi.org/10.48550/arxiv.2605.19516))
+ **After:** 5. **베이스 모델(Non-RLHF) 패러프레이징** (Xu et al., 2026, [arXiv:2605.19516](https://doi.org/10.48550/arxiv.2605.19516))

### [11] `replace` (L59–L59)
- **Before:** 모델 가중치를 바꾸지 않고 **토큰 생성 순간의 확률 분포**를 제어하는 기법입니다.
+ **After:** 가중치를 유지한 채 **토큰 생성 시점의 확률 분포**를 제어하는 기법입니다.

### [12] `replace` (L69–L69)
- **Before:** 3. **Verbalized Sampling (언어화 샘플링, VS)** — Zhang, Manning, Shi et al., 2025 ([arXiv:2510.01171](https://doi.org/10.48550/arxiv.2510.01171))
+ **After:** 3. **Verbalized Sampling (언어화 샘플링, VS)** (Zhang, Manning, Shi et al., 2025, [arXiv:2510.01171](https://doi.org/10.48550/arxiv.2510.01171))

### [13] `replace` (L79–L79)
- **Before:** **"빈 도화지에서 AI에게 바로 초안을 시키는 순간(ポン出し) Slop은 이미 확정된다"**는 것이 4개 언어권 실무자들의 공통 결론입니다.
+ **After:** 4개 언어권 실무자들이 공통으로 강조하는 출발점은 **"빈 도화지에서 AI에게 바로 초안을 시키는 순간(ポン出し) Slop은 이미 확정된다"**는 사실입니다.

### [14] `replace` (L87–L87)
- **Before:**    - 목차·불릿 뼈대(skeleton)를 미리 쥐여주면 모델이 "양식 채우기(form-filling)" 모드로 전환되어 Slop이 폭발합니다. **누가 누구에게 말하느냐(Identity)**와 **팩트 원천(Facts)**을 분리하고, 물리적 플랫폼 제약(글자 수·마크업)만 준 뒤 구조는 열어두는 편이 훨씬 자연스럽습니다.
+ **After:**    - 목차·불릿 뼈대(skeleton)를 미리 쥐여주면 모델이 "양식 채우기(form-filling)" 모드로 전환되어 Slop이 급격히 늘어납니다. **누가 누구에게 말하느냐(Identity)**와 **팩트 원천(Facts)**을 분리하고, 물리적 플랫폼 제약(글자 수·마크업)만 준 뒤 구조는 열어두면 글이 훨씬 자연스럽습니다.

### [15] `replace` (L91–L91)
- **Before:**    - 항공기 정비 매뉴얼용 통제 언어 규격(ASD-STE100 Issue 9)을 80% 강도로 적용합니다: **지시문 20단어/설명문 25단어 상한, 1문장 1아이디어, 조건 선행(`If X, do Y`), 능동태·단순시제, 1개념 1용어 고정(동의어 돌려쓰기 박멸), 3단어 초과 명사 연쇄 금지, 문단당 최대 6문장, 세미콜론 금지.**
+ **After:**    - 항공기 정비 매뉴얼용 통제 언어 규격(ASD-STE100 Issue 9)을 80% 강도로 적용합니다: **지시문 20단어/설명문 25단어 상한, 1문장 1아이디어, 조건 선행(`If X, do Y`), 능동태·단순시제, 1개념 1용어 고정(동의어 돌려쓰기 차단), 3단어 초과 명사 연쇄 금지, 문단당 최대 6문장, 세미콜론 금지.**

### [16] `replace` (L94–L95)
- **Before:**    - 단순 "내 글 3편을 보고 비슷하게 써줘"가 아니라, 본인 샘플에서 **명시적 스타일 가설**(문장 길이 분포, 쉼표/구두점 습관, 첫 문장 진입 방식, 절대 안 쓰는 어휘, 온기가 붙는 위치)을 먼저 JSON/마크다운 페르소나 문서로 추출·검증(`check_persona.py`)한 뒤 적용합니다.
- **Before:** 5. **긍정 프레이밍 (Affirmative Framing — 핑크 엘리펀트 문제 회피)**
+ **After:**    - "내 글 3편을 보고 비슷하게 써줘" 식으로 맡기는 대신, 본인 샘플에서 **명시적 스타일 가설**(문장 길이 분포, 쉼표/구두점 습관, 첫 문장 진입 방식, 절대 안 쓰는 어휘, 온기가 붙는 위치)을 먼저 JSON/마크다운 페르소나 문서로 추출·검증(`check_persona.py`)한 뒤 적용합니다.
+ **After:** 5. **긍정 프레이밍 (Affirmative Framing: 핑크 엘리펀트 문제 회피)**

### [17] `replace` (L106–L108)
- **Before:**    - **Pass 1 — 서사 아키텍처 (Fiction):** 해설자가 주제를 직접 설교하는 버릇 제거(AI 77% vs 인간 52%), 단선적 인과사슬 느슨화, 폭로/반전 후치, 신체 감각 클리셰(*가슴이 조여왔다* AI 81% vs 인간 38%) 탈피, 실제 지명·브랜드·금액 등 현실 고유명사 삽입(인간이 AI의 2배), 도덕적 모호성 허용.
- **Before:**    - **Pass 2 — 담화 흐름 (Discourse Flow):** 예측 가능한 문단-질문 전개(QUD) 해체, 중반부 처짐(mid-story sag) 교정, 지나치게 매끄러운 문단 연결 고의 단절(중국어 실측: 인간은 14문단마다 화제 점프, AI는 50문단당 1회).
- **Before:**    - **Pass 3 — 표층 스타일 (Surface Style):** 상투어·대구·구두점·어조 정리.
+ **After:**    - **Pass 1 · 서사 아키텍처 (Fiction):** 해설자가 주제를 직접 설교하는 버릇 제거(AI 77% vs 인간 52%), 단선적 인과사슬 느슨화, 폭로/반전 후치, 신체 감각 클리셰(*가슴이 조여왔다* AI 81% vs 인간 38%) 탈피, 실제 지명·브랜드·금액 등 현실 고유명사 삽입(인간이 AI의 2배), 도덕적 모호성 허용.
+ **After:**    - **Pass 2 · 담화 흐름 (Discourse Flow):** 예측 가능한 문단-질문 전개(QUD) 해체, 중반부 처짐(mid-story sag) 교정, 지나치게 매끄러운 문단 연결 고의 단절(중국어 실측: 인간은 14문단마다 화제 점프, AI는 50문단당 1회).
+ **After:**    - **Pass 3 · 표층 스타일 (Surface Style):** 상투어·대구·구두점·어조 정리.

### [18] `replace` (L113–L113)
- **Before:**    3. **완곡어구 외과수술 (Hedge surgery):** 실질적 불확실성이 아니면 완곡어 삭제; 진짜 불확실하면 1인칭 인간식으로 표현.
+ **After:**    3. **완곡어구 정리 (Hedge surgery):** 실질적 불확실성이 아니면 완곡어를 빼고, 실제로 불확실한 내용만 1인칭으로 명시.

### [19] `replace` (L119–L119)
- **Before:**    9. **RLHF/지시 튜닝 보이스 박리 (Strip RLHF voice — 최상위 레버):** 요청하지 않은 양비론 트레이드오프, 질문 칭찬 오프너, 도우미 클로저, 과도한 완결성 제거.
+ **After:**    9. **RLHF/지시 튜닝 보이스 박리 (Strip RLHF voice, 최상위 레버):** 요청하지 않은 양비론 트레이드오프, 질문 칭찬 오프너, 도우미 클로저, 과도한 완결성 제거.

### [20] `replace` (L122–L122)
- **Before:**    - **기술문서·설계서 (`bamboo-nova/meiseki`, `sepia`):** *"자연스러움/목소리 추가"*가 아니라 **독해 부하 제거(이중부정·긴 관형절·연속 한자·명사화 해체)**와 **결론 우선·`file:line` 근거·블레임리스 포스트모템**에 집중합니다.
+ **After:**    - **기술문서·설계서 (`bamboo-nova/meiseki`, `sepia`):** *"자연스러움/목소리 추가"* 대신 **독해 부하 제거(이중부정·긴 관형절·연속 한자·명사화 해체)**와 **결론 우선·`file:line` 근거·블레임리스 포스트모템**에 집중합니다.

### [21] `replace` (L136–L137)
- **Before:** | **`seyedehsanhadi/sloptrim`** (429★) | EN | Zero-dep Python stdlib 71패턴·20개 파일 포맷(`.docx/.pptx/.tex/.ipynb` 등) | Claude Code 저장 훅 자동 채점(0~100, 기본 40 / strict 20), 코드 블록 완전 제외 |
- **Before:** | **`devswha/patina`** (390★) | **KO/EN/ZH/JA** | 189패턴(언어별 37~41 리라이트 + 9 훅), 3독립축(장르·페르소나·격식) | **MPS(의미 보존 점수) 하한선 게이트** + 오프라인 CI 게이트(`--score --offline --exit-on 30`) |
+ **After:** | **`seyedehsanhadi/sloptrim`** (429★) | EN | Zero-dep Python stdlib 71패턴·20개 파일 포맷(`.docx/.pptx/.tex/.ipynb` 등) | Claude Code 저장 훅 자동 채점(0~100, 기본 40 / strict 20), 코드 블록 제외 |
+ **After:** | **`devswha/patina`** (390★) | **KO/EN/ZH/JA** | 189패턴(언어별 37~41 리라이트 + 9 훅), 3개 독립 기준(장르·페르소나·격식) | **MPS(의미 보존 점수) 하한선 게이트** + 오프라인 CI 게이트(`--score --offline --exit-on 30`) |

### [22] `replace` (L147–L147)
- **Before:**    - `stop-slop`은 **5개 축(Directness, Rhythm, Trust, Authenticity, Density) 50점 루브릭**을 매겨 **35/50 미만이면 강제 재작성**합니다.
+ **After:**    - `stop-slop`은 **5개 항목(Directness, Rhythm, Trust, Authenticity, Density) 50점 루브릭**을 매겨 **35/50 미만이면 강제 재작성**합니다.

### [23] `replace` (L153–L153)
- **Before:**    - 정적 규칙만으로 상용 학습 분류기(GPTZero, Pangram 3.0)를 뚫지 못하는 한계를 넘기 위한 최강 하이브리드 기법: 후보 3~5개를 생성 → 탐지기/슬롭 점수로 채점 → 최저 점수안 선택(8개 탐지기 평균 TPR **87.88% 감소**).
+ **After:**    - 정적 규칙만으로 상용 학습 분류기(GPTZero, Pangram 3.0)를 뚫지 못하는 한계를 넘기 위한 대표적 하이브리드 기법: 후보 3~5개를 생성 → 탐지기/슬롭 점수로 채점 → 최저 점수안 선택(8개 탐지기 평균 TPR **87.88% 감소**).

### [24] `replace` (L162–L162)
- **Before:** ### Layer 7. 인간 편집 & 기계가 대체 불가능한 최후의 경계
+ **After:** ### Layer 7. 인간 편집과 자동화의 한계

### [25] `replace` (L169–L173)
- **Before:**   - **Dan Shipper / Every.to:** 수천 건의 사내 편집자 교정 이력으로 커스텀 에디팅 에이전트를 훈련시키되, 최종 **편집적 취향(taste)**과 **실제 경험·입장**은 인간이 쥐는 실용주의 제시.
- **Before:** 
- **Before:** ---
- **Before:** 
- **Before:** ## 3. 4개 언어권별 AI Slop 지문 & 특화 제거 기법 완전 비교
+ **After:**   - **Dan Shipper / Every.to:** 수천 건의 사내 편집자 교정 이력으로 커스텀 에디팅 에이전트를 훈련시키되, 최종 **편집적 취향(taste)**과 **실제 경험·입장**은 인간이 직접 맡는 실용 방식을 택함.
+ **After:** 
+ **After:** ---
+ **After:** 
+ **After:** ## 3. 4개 언어권별 AI Slop 특징과 제거 기법

### [26] `replace` (L176–L176)
- **Before:** - **사실상 표준 카탈로그 — `Wikipedia:Signs of AI writing` (`WP:AISIGNS`, WikiProject AI Cleanup):**
+ **After:** - **사실상 표준 카탈로그: `Wikipedia:Signs of AI writing` (`WP:AISIGNS`, WikiProject AI Cleanup)**

### [27] `replace` (L178–L178)
- **Before:**   - **주목할 최신 개정:** *과장된 홍보 문체(2023–2025)*와 *엠대시 남용(2022–September 2026)*이 **Historical indicators(§13)**로 이동 — 최신 모델이 대시 습관을 일부 교정하면서 더 은밀한 구조적 티(부정 병렬·스테이징·독자 맥락 무시)가 전면에 부상했습니다.
+ **After:**   - **주요 최신 개정:** *과장된 홍보 문체(2023–2025)*와 *엠대시 남용(2022–September 2026)*이 **Historical indicators(§13)**로 이동했습니다. 최신 모델이 대시 습관을 일부 교정하면서 더 은밀한 구조적 티(부정 병렬·스테이징·독자 맥락 무시)가 핵심 지표로 올라왔습니다.

### [28] `replace` (L180–L180)
- **Before:**   - **A. 말하지 않고 연출하기(Staging instead of stating, §1~5 — 단 1회 발견 시 즉시 수정):** `Not X but Y`, 한 줄 극적 클로저(`That is the real win.`), 깊어 보이는 격언(`X is the language of Y`), 헛기침 도입(`Let's dive in / Here's the thing / the hard part is`), 허수아비 반박(`To be clear, I'm not saying... / A tempting approach would be...`).
+ **After:**   - **A. 말하지 않고 연출하기(Staging instead of stating, §1~5, 단 1회 발견 시 즉시 수정):** `Not X but Y`, 한 줄 극적 클로저(`That is the real win.`), 깊어 보이는 격언(`X is the language of Y`), 헛기침 도입(`Let's dive in / Here's the thing / the hard part is`), 허수아비 반박(`To be clear, I'm not saying... / A tempting approach would be...`).

### [29] `replace` (L193–L193)
- **Before:**     - `C. 구조적 AI 패턴`: 기계적 `첫째/둘째/셋째`, **대구 구조(C-8 — 실측 AI가 인간의 12배!)**, 연결어미 뒤 쉼표(C-11).
+ **After:**     - `C. 구조적 AI 패턴`: 기계적 `첫째/둘째/셋째`, **대구 구조(C-8, 실측 AI가 인간의 12배)**, 연결어미 뒤 쉼표(C-11).

### [30] `replace` (L195–L196)
- **Before:**   - **v2.4 블라인드 평가 어휘 레이어 (115개 한국어 걸림돌 낱말 — 생존율 94% → 34%, 2점 확실 어색 어휘 96% → 22%):**
- **Before:**     - **바꿈 우선(2점) 대표:** `렌즈`(*두 렌즈로 보면*), `축`(*세 개의 축*), `쥐다`(*대안을 쥔*), `얹다`, `기둥`(**인간 0.47 vs Claude 7.95** / 10만 자당), `층위`(**인간 0 vs Claude 5.5, Solar 4.1**), `짚다`(*짚고 간다* — **인간 0.23 vs GPT/Solar 3.4**), 영어 연어 직역(`성공을 달성하다`, `결과를 전달하다`, `정보에 입각한 결정`, `잠재력을 잠금 해제하다`, 평가 술어 `서늘하다`).
+ **After:**   - **v2.4 블라인드 평가 어휘 레이어 (115개 한국어 걸림돌 낱말: 생존율 94% → 34%, 2점 확실 어색 어휘 96% → 22%):**
+ **After:**     - **바꿈 우선(2점) 대표:** `렌즈`("두 렌즈로 보면"), `축`("세 개의 축"), `쥐다`("대안을 쥔"), `얹다`, `기둥`(**인간 0.47 vs Claude 7.95** / 10만 자당), `층위`(**인간 0 vs Claude 5.5, Solar 4.1**), `짚다`("짚고 간다", **인간 0.23 vs GPT/Solar 3.4**), 영어 연어 직역(`성공을 달성하다`, `결과를 전달하다`, `정보에 입각한 결정`, `잠재력을 잠금 해제하다`, 평가 술어 `서늘하다`).

### [31] `replace` (L208–L208)
- **Before:**     - **`@conbowl` 한국어 AI 글 9대 필수 교정 패턴 (조회 11만회, 10연타 스레드):** ① `A는 단순히 B가 아니라 C다` ② 행동을 숨기는 추상 동사 **`~를 함께 봅니다`** ③ 감각적인 척하는 추상명사 조합(**`"정서의 결"`, `"여운의 농도"`, `"맥락의 밀도"`**) ④ 앞 문장에 지시 대상이 없는 빈 지시대명사(`그 기준`, `이를 통해`) ⑤ 사전적 합성어 남발(`판단 기준`, `작동 구조`, `운영 관점`) ⑥ 새 정보 없는 선언형 마무리(`기준은 분명합니다`) ⑦ 불필요한 비교 늘이기(`A보다 B에 가깝습니다`) ⑧ **기획안·서류에서의 맥락 없는 주어 생략**(일상 글과 달리 업무 문서에서는 주체 명시 필수) ⑨ 관계 설명 없는 기계적 3단계 나열.
+ **After:**     - **`@conbowl` 한국어 AI 글 9대 필수 교정 패턴 (조회 11만회, 10연타 스레드):** ① `A는 단순히 B가 아니라 C다` ② 행동을 숨기는 추상 동사 **`~를 함께 봅니다`** ③ 감각적인 척하는 추상명사 조합(**`"정서의 결"`, `"여운의 농도"`, `"맥락의 밀도"`**) ④ 앞 문장에 지시 대상이 없는 빈 지시대명사(`그 기준`, `이를 통해`) ⑤ 사전적 합성어 남발(`판단 기준`, `작동 구조`, `운영 관점`) ⑥ 새 정보 없는 선언형 마무리(`기준은 분명합니다`) ⑦ 불필요한 비교 늘이기(`A보다 B에 가깝습니다`) ⑧ **기획안·서류에서 맥락 없이 주어를 빼는 습관**(일상 글과 달리 업무 문서에서는 주체 명시 필수) ⑨ 관계 설명 없는 기계적 3단계 나열.

### [32] `replace` (L217–L217)
- **Before:**   - *(영문 연계)* Zonder Labs **Zhizhuo Zhou (`@zhizdev`)**의 가독성 저하 분석(핵심 논지 은폐, 모호한 서술, 관련 어휘 간 구문 거리 증가 — Stack Overflow 인간 답변과 대조)이 한국 아카라이브·네이버 카페에서도 널리 인용됨.
+ **After:**   - *(영문 연계)* Zonder Labs **Zhizhuo Zhou (`@zhizdev`)**의 가독성 저하 분석(핵심 논지 은폐, 모호한 서술, 관련 어휘 간 구문 거리 증가; Stack Overflow 인간 답변과 대조)이 한국 아카라이브·네이버 카페에서도 널리 인용됨.

### [33] `replace` (L220–L222)
- **Before:** 일본어권은 **정적 린터(`textlint`) 생태계 + 독해 부하 기반 '명석화(明晰化)' + 편집자 3인 워크플로우**가 독보적으로 발달했습니다.
- **Before:** 
- **Before:** - **결정적 린터 — `@textlint-ja/preset-ai-writing` (1,165★, azu) & `p1ass/textlint-rule-preset-ai-words-ja` (132★):**
+ **After:** 일본어권은 **정적 린터(`textlint`) 생태계 + 독해 부하 기반 '명석화(明晰化)' + 편집자 3인 워크플로우**가 체계적으로 발달했습니다.
+ **After:** 
+ **After:** - **결정적 린터: `@textlint-ja/preset-ai-writing` (1,165★, azu) & `p1ass/textlint-rule-preset-ai-words-ja` (132★)**

### [34] `replace` (L226–L227)
- **Before:** - **역발상 스킬 — `bamboo-nova/meiseki` (明晰, Zenn 화제작):**
- **Before:**   - 기존 휴머나이저(`iKora128/stop-ai-slop-jp`의 1인칭 `"自分は"` 주입 등)와 **정반대 방향**으로, 인위적 목소리를 덧칠하지 않고 오직 **독해 부하(RLS)가 높은 AI 구문만 6단계(A~F)로 절삭**합니다:
+ **After:** - **역발상 스킬: `bamboo-nova/meiseki` (明晰, Zenn 화제작)**
+ **After:**   - 기존 휴머나이저(`iKora128/stop-ai-slop-jp`의 1인칭 `"自分は"` 주입 등)와 달리 화자 목소리를 추가하지 않고, **독해 부하(RLS)가 높은 AI 구문만 6단계(A~F)로 줄입니다**:

### [35] `replace` (L232–L232)
- **Before:**   - `iKora128/stop-ai-slop-jp`: 일본어 비즈니스 AI 클리셰(`泥臭さ, 解像度, 本質`), 무생물 주어 가짜 행위성(false agency), 전각 대시(`──`) 박멸.
+ **After:**   - `iKora128/stop-ai-slop-jp`: 일본어 비즈니스 AI 클리셰(`泥臭さ, 解像度, 本質`), 무생물 주어 가짜 행위성(false agency), 전각 대시(`──`) 제거.

### [36] `replace` (L236–L241)
- **Before:** ### 3.4 중국어권 — 간체(ZH-CN) & 번체/대만(ZH-TW)
- **Before:** 전 세계에서 **코퍼스 계량 검증**과 **학술 AIGC 탐지 대응(知网/维普/万方/腾讯朱雀)**이 가장 치밀하게 진화한 언어권입니다.
- **Before:** 
- **Before:** - **간체(ZH-CN) 520만 자 실증 연구 — `larashero3-dotcom/lieflat-less-ai-tone` (8,621★):**
- **Before:**   - 1,169편(2라운드 페어링 실험 포함), 90개 Python 스크립트 지표 + 약 50만 회 LLM 의미 판정으로 **진짜 AI 味 9대 지표**와 **폐기된 미신 6종**을 가려냈습니다:
- **Before:**     - **진짜 9대 지표:** ① 구미화 대조 `"不是A而是B"`(δ +0.88/+0.72, 최강 신호) ② **동의어 돌려쓰기 강박**(MTLD/MATTR δ +0.91/+0.55 — 인간은 같은 단어를 반복, AI는 `优化/增强/提升/提高`를 억지로 돌려씀) ③ 소제목 과잉 분할(중앙값 AI 7절 vs 인간 1절) ④ 문장·쉼표절 길이 균일성(δ −0.88) ⑤ 긴 구미화 관형어(前置定语) ⑥ 결론 예고 콜론(`核心是：/残酷的现实是：` AI 2.1배) ⑦ 과잉 매끄러운 문단 연결(AI 98.9% vs 인간 95.2%) ⑧ 밀집 병렬·열거(1.45배) ⑨ 부적절한 거대 비유(인간 심사 확증).
+ **After:** ### 3.4 중국어권: 간체(ZH-CN) & 번체/대만(ZH-TW)
+ **After:** 중국어권은 **코퍼스 계량 검증**과 **학술 AIGC 탐지 대응(知网/维普/万方/腾讯朱雀)** 도구가 가장 활발하게 개발되는 권역입니다.
+ **After:** 
+ **After:** - **간체(ZH-CN) 520만 자 실증 연구: `larashero3-dotcom/lieflat-less-ai-tone` (8,621★)**
+ **After:**   - 1,169편(2라운드 페어링 실험 포함), 90개 Python 스크립트 지표 + 약 50만 회 LLM 의미 판정으로 **유효한 AI 味 9대 지표**와 **폐기된 미신 6종**을 가려냈습니다:
+ **After:**     - **유효한 9대 지표:** ① 구미화 대조 `"不是A而是B"`(δ +0.88/+0.72, 가장 강한 신호) ② **동의어 돌려쓰기 강박**(MTLD/MATTR δ +0.91/+0.55; 인간은 같은 단어를 반복, AI는 `优化/增强/提升/提高`를 억지로 돌려씀) ③ 소제목 과잉 분할(중앙값 AI 7절 vs 인간 1절) ④ 문장·쉼표절 길이 균일성(δ −0.88) ⑤ 긴 구미화 관형어(前置定语) ⑥ 결론 예고 콜론(`核心是：/残酷的现实是：` AI 2.1배) ⑦ 과잉 매끄러운 문단 연결(AI 98.9% vs 인간 95.2%) ⑧ 밀집 병렬·열거(1.45배) ⑨ 부적절한 거대 비유(인간 심사 확증).

### [37] `replace` (L286–L286)
- **Before:** | [`devswha/patina`](https://github.com/devswha/patina) | **KO/EN/ZH/JA** | **390** | 4개국어 CLI + Skill | 189패턴, 3독립축, MPS 의미 보존 게이트, 페르소나 학습, 오프라인 CI | `npx skills add devswha/patina` |
+ **After:** | [`devswha/patina`](https://github.com/devswha/patina) | **KO/EN/ZH/JA** | **390** | 4개국어 CLI + Skill | 189패턴, 3개 독립 기준, MPS 의미 보존 게이트, 페르소나 학습, 오프라인 CI | `npx skills add devswha/patina` |

### [38] `replace` (L297–L297)
- **Before:** | [`bamboo-nova/meiseki`](https://github.com/bamboo-nova/meiseki) | JA | **49** | 3층 플러그인 | 독해부하 절삭(RLS) + Jev 고속판정 + 기계적 의미 검산/자동 롤백 | `npx skills add bamboo-nova/meiseki` |
+ **After:** | [`bamboo-nova/meiseki`](https://github.com/bamboo-nova/meiseki) | JA | **49** | 3층 플러그인 | 독해부하 절감(RLS) + Jev 고속판정 + 기계적 의미 검산/자동 롤백 | `npx skills add bamboo-nova/meiseki` |

### [39] `replace` (L304–L304)
- **Before:** ## 5. 핵심 학술 논문 정밀 색인 (API 검증 완료 31편)
+ **After:** ## 5. 핵심 학술 논문 색인 (API 검증 완료 31편)

### [40] `replace` (L311–L311)
- **Before:** | **원인·RLHF** | *Base Models Look Human To AI Detectors* | Xu, Zhong, Raghunathan, Fang, Kolter (2026) | [arXiv:2605.19516](https://doi.org/10.48550/arxiv.2605.19516) | 탐지기가 잡는 본질은 **RLHF/지시 튜닝 문체**; 베이스 모델은 인간 판정 |
+ **After:** | **원인·RLHF** | *Base Models Look Human To AI Detectors* | Xu, Zhong, Raghunathan, Fang, Kolter (2026) | [arXiv:2605.19516](https://doi.org/10.48550/arxiv.2605.19516) | 탐지기가 잡는 핵심은 **RLHF/지시 튜닝 문체**; 베이스 모델은 인간 판정 |

### [41] `replace` (L340–L340)
- **Before:** ## 6. 실증적으로 판명된 '죽은 길(Dead Ends)' & 9대 역효과(Anti-Patterns)
+ **After:** ## 6. 실증 연구로 판명된 '죽은 길(Dead Ends)'과 9가지 역효과(Anti-Patterns)

### [42] `replace` (L360–L360)
- **Before:** > **우회 금지 원칙 준수:** 로그인 벽·안티봇 검증(CAPTCHA)·유료 페이월은 우회하지 않고 즉시 중단하여 아래에 정확히 기록했습니다. 원하시는 항목에 로그인하시거나 원문 PDF/텍스트를 넘겨주시면 바로 2차 심층 분석에 통합하겠습니다.
+ **After:** > **우회 금지 원칙 준수:** 로그인 벽·안티봇 검증(CAPTCHA)·유료 페이월은 우회하지 않고 즉시 중단하여 아래에 정확히 기록했습니다. 원하시는 항목에 로그인하시거나 원문 PDF/텍스트를 넘겨주시면 바로 2차 분석에 반영하겠습니다.

### [43] `replace` (L367–L367)
- **Before:** | **Threads (스레드)** | `https://www.threads.com/search?q=AI%ED%88%AC` 외 6개 쿼리 | **✅ Chrome 로그인 세션으로 수집 완료** | 한국어(`@conbowl`, `@jayber_jobpartner`, `@__bi_dam__`, `@yourgpt3650`) · 중화권(`@canigotoschoolbytaxi`, `@waterwool_ultramarineblue`, `@_3cpj_`) 핵심 기법 모두 3장에 병합 완료 |
+ **After:** | **Threads (스레드)** | `https://www.threads.com/search?q=AI%ED%88%AC` 외 6개 쿼리 | **수집 완료 (Chrome 로그인 세션)** | 한국어(`@conbowl`, `@jayber_jobpartner`, `@__bi_dam__`, `@yourgpt3650`) · 중화권(`@canigotoschoolbytaxi`, `@waterwool_ultramarineblue`, `@_3cpj_`) 핵심 기법 모두 3장에 병합 완료 |

