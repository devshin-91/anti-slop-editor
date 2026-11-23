# Korean Anti-Slop Reference (`lang: ko`)

Synthesizes empirical Korean studies (`KatFishNet` ACL 2025, `im-not-ai` 85-pattern taxonomy +
115 blind-evaluated lexical items, `DaleSeo/korean-skills`, `GPTERS` STE100 adaptation, and
Korean Threads/Naver Cafe/Brunch/ArcaLive fieldwork).

---

## 1. Highest-Discriminative Model-Invariant Korean Tells (Fix First)

1. **부정 대구·반전 클리셰 (`C-8`, 실측 AI가 인간의 12배):**
   - `"A는 단순히 B가 아니라 C입니다"`, `"~에 그치지 않고"`, `"A보다 B에 가깝습니다"`.
   - **교정:** 독자가 실제로 품은 오해를 교정하는 경우가 아니면 앞의 부정·비교를 걷어내고 C를 정면 서술한다.
     - ❌ 마케팅은 단순히 서비스를 알리는 일이 아니라 고객의 마음을 이해하는 일입니다.
     - ✅ 마케팅은 고객의 마음을 이해하는 일입니다.
2. **번역투 조사·피동·숨은 동사 (`A` 계열):**
   - `~를 통해(서)`, `~에 대해(서)`, `~에 있어서`, `~에 의해(서)`, 이중 피동(`되어진다/보여진다/불려진다`), 잉여 동사(`가지고 있다`, `제공합니다`), 강박적 `그/그녀`(문맥상 생략 또는 역할명 사용), 긴 좌향 관계절 수식(`~할 수 있는 ~하는 ~의`), 이중 조사(`~에서의`, `~에로의`).
   - **숨은 동사 제거:** `검토를 진행하다` → `검토하다`, `개선을 수행하다` → `개선하다`, `결정을 내리다` → `결정하다`, `분석을 실시하다` → `분석하다`.
3. **감각적인 척하는 추상명사 조합 & 빈 행동 동사 (`@conbowl` 9패턴):**
   - ❌ `"정서의 결을 살립니다"`, `"여운의 농도를 높입니다"`, `"맥락의 밀도를 더합니다"`, `"방향성과 고객 반응을 함께 봅니다"`.
   - ✅ 실제 행동·지표·산출물로 풀어 쓴다 (예: `"최근 게시물의 저장·공유 수를 비교해 반응이 높았던 주제를 추립니다"`).
4. **지시 대상이 빈 지시대명사 (`그 기준`, `이를 통해`, `이러한 흐름`):**
   - 바로 앞 문장에서 가리키는 대상을 즉시 특정할 수 없으면 실제 명사를 직접 쓰거나 빠진 인과 단계를 보충한다.
5. **사전적 합성어 & 자소서·보고서 AI 클리셰 (`@conbowl`, `@jayber_jobpartner`):**
   - `구조적 접근`, `실질적 성과`, `업무 맥락`, `업무 흐름`, `판단 기준`, `작동 구조`, `운영 관점`이 한 문단에 2회 이상 겹치면 일상 업무 동사로 풀어 쓴다.
6. **선언형·요약형 마무리 & 챗봇 잔여물 (`D` 계열):**
   - `"결론적으로"`, `"시사하는 바가 크다"`, `"주목할 만하다"`, `"중요한 것은 ~입니다"`, `"기준은 분명합니다"`, `"~를 알아보았습니다"`, `"도움이 되셨길 바랍니다"`.
   - **교정:** 새 정보가 없으면 삭제하고 직전 구체 사실에서 문단을 끝낸다.
7. **연결어미 뒤 기계적 쉼표(`C-11`), 가운데점(`·`)·따옴표·엠대시(`—`) 남발 (`KatFishNet` 94.88% AUC 구두점 신호):**
   - 단, **단일 구두점 지표만으로 AI 작성으로 단정 금지** (개인 쉼표 습관 오탐 사례). 다른 계열 신호와 함께 나타날 때만 정리한다.
8. **형식명사·당위·다중 완곡 (`G/I` 계열):**
   - `~것이다` 연속, `~할 필요가 있다`, `~할 수 있을 것으로 보인다/기대된다`, `~라고 할 수 있습니다`, `~하는 편이 좋습니다/낫습니다`(권고 반복 시).
9. **문체 리듬 & 주어 규칙 (장르별 분기!):**
   - **에세이·블로그·SNS:** 문맥상 명백한 주어는 생략하고, `"A는 B이다"` 반복 대신 간결한 어미 변주·자연스러운 도치 활용. 단, `"완벽히 배제"`, `"말줄임표(……) 강제"` 같은 과잉 연출 금지.
   - **기획안·보고서·기술문서:** 주체가 불분명해지는 주어 생략 금지. 행위자(팀/시스템)를 명시하되 미정이면 `"담당자 지정 예정"`으로 적는다(없는 인물 창작 금지).
   - **3단계 병렬 (`A, B, 그리고 C`):** 실제로 독립된 3요소가 아니면 핵심 1~2개만 남기거나 각 항목의 역할을 구분한다.

---

## 2. Context-Checked Korean Lexical Trap Dictionary (No Blind Replace!)

Grounded in `im-not-ai` v2.4.6 blind evaluation (reduced awkward lexical survival from **94% → 34%**).
**Never run blind find-and-replace.** Check `Keep when` first; if the text uses the word figuratively
as English calque, rewrite naturally—and never introduce a *different* word from this list.

| Priority | Expression (English Calque) | Change When | Keep When (Do NOT Touch) | Natural Direction |
|---|---|---|---|---|
| **P1 (확실)** | **렌즈** (`~라는 렌즈로 보면`) | 관점·시각·기준의 은유 | 카메라·안경·광학 렌즈 | `관점에서 보면` / 틀 구절 삭제 |
| **P1 (확실)** | **축** (`두 축 / 세 개의 축`) | 분류·기준·요소 나열 | 회전축·좌표축·기계 축 | `두 가지 기준` / 번호·항목 직접 서술 |
| **P1 (확실)** | **기둥** (`세 개의 기둥`, Claude 17×) | 정책·전략의 핵심 요소 은유 | 건물 기둥, `집안의 기둥`, `팀의 기둥` | `핵심 과제`, `세 가지 원칙` |
| **P1 (확실)** | **층위** (인간 0 vs Claude 5.5) | 단순 단계·수준·측면 대체 | 분석 수준을 실제 층별로 나눠 논하는 학술 개념 | `단계`, `수준`, `측면` |
| **P1 (확실)** | **짚다** (`짚고 간다 / 짚어 보자`, GPT/Solar 15×) | 설명 전환용 상투어 | `맥을 짚다`, `지팡이를 짚다` | 삭제하고 바로 본론 진입 |
| **P1 (확실)** | **쥐다** (`대안을 쥔`, `길목을 쥐고`) | 보유·주도권의 어색한 은유 | 손으로 실제 물건을 쥐다 | `가진`, `차지한`, `맡은` |
| **P1 (확실)** | **얹다** (`~위에 얹은 계층`) | 기술·기능 추가의 번역투 (`layer on`) | 물건을 위에 올려놓다 | `덧붙이다`, `더하다`, `올리다` |
| **P1 (확실)** | **잠재력을 잠금 해제하다** (`unlock`) | 능력·성장·창의성 대상 | 화면·계정·기기 잠금 해제 | `잠재력을 발휘하다`, `역량을 끌어내다` |
| **P1 (확실)** | **논의의 무늬 / 생각을 벼리다** | 쟁점·양상/생각 정리의 과잉 시적 표현 | 실제 직물·동물 무늬, 칼·연장 벼리기 | `쟁점이 드러나다`, `생각을 추리다` |
| **P1 (확실)** | **성공을 달성하다 / 결과를 전달하다 / 정보에 입각한 결정** | 영어 연어 직역 (`achieve/deliver/informed`) | 직접 인용문 내부 | `성과를 내다`, `결과를 내다`, `근거를 보고 판단하다` |
| **P2 (조건부)** | **본질적으로** (AI 3.7×) | 문두 습관적 강조·반복 | 학술 논문 내 본질 규정 | 삭제하거나 핵심 내용 직접 서술 |
| **P2 (조건부)** | **~하는 편이 좋습니다/낫습니다** | 권고 문장 종결 반복 | 실제 비교 (`A보다 B하는 편이 낫다`) | `~하세요`, `~하는 게 안전합니다` |
| **P2 (조건부)** | **지형 / 여정 / 맞물리다 / ~로 기능한다 / 궁극적으로** | 문단 내 반복·추상적 부풀리기 | 지리적 지형, 실제 여행, 기어 맞물림 | `시장 구도`, `과정`, `역할을 한다`, `결국` |

---

## 3. Recommended Korean Post-Edit Pipeline (`DaleSeo/korean-skills` Order)

When polishing an important Korean draft, run in this exact order so passes do not fight each other:
1. **De-Slop (`anti-slop-editor`):** Remove translationese, structural AI tells, and awkward lexical calques (biggest changes first).
2. **Grammar & Spacing:** Fix `되/돼`, `-ㄴ지/-는지`, dependent nouns (`것/수/뿐`), and double-passive leftovers created by sentence splitting.
3. **Style Consistency & Read-Aloud Check:** Verify paragraph-level speech register (`합니다체`/`해요체`/`한다체`) consistency (note: preserve pure `하였다` academic style without false-flagging formality shift when splitting sentences!) and rewrite any sentence where reading aloud feels stiff ("입이 걸리는 문장").
