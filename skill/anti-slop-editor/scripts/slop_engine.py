#!/usr/bin/env python3
"""Anti-Slop Editor deterministic pre-scan, Unicode scrubber, verifier, and diff reporter.

Zero external dependencies (Python 3 standard library only).
Supports Korean (ko), English (en), Japanese (ja), Chinese Simplified (zh-cn),
and Chinese Traditional / Taiwan (zh-tw).

Subcommands:
  scan           Detect invisible Unicode artifacts, multi-family AI slop signals,
                 sentence rhythm stats, and route hint (light / standard / heavy).
  clean-unicode  Scrub invisible Unicode watermarks/artifacts outside code blocks.
  verify         Run deterministic post-rewrite gates (protected tokens, change rate,
                 length floor, negation parity, epistemic hedges, P1 lexical regression,
                 and academic register protection).
  diff-report    Produce a Markdown metrics table, gate breakdown, and numbered diff.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import difflib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
from typing import Any


# Ensure UTF-8 I/O on Windows consoles/pipes
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Constants & Data Structures
# ---------------------------------------------------------------------------

VALID_GENRES = ("auto", "blog", "tech", "academic", "fiction", "sns", "business")
VALID_LANGS = ("auto", "ko", "en", "ja", "zh", "zh-cn", "zh-tw")

# Characters used to distinguish Traditional Chinese (zh-tw) vs Simplified Chinese (zh-cn)
TRAD_DISCRIMINATORS = set(
    "這為個們國來說時會學經進發過對實點問關業機體與無應該讓還從現並將裡寫讀網資優專軟影臺灣號語書車馬東長門開見氣電"
)
SIMP_DISCRIMINATORS = set(
    "这为个们国来说时会学经进发过对实点问关业机体与无应该让还从现并将里写读网资优专软影台湾号语书车马东长门开见气电"
)

# Invisible Unicode artifacts tracked outside code spans
INVISIBLE_CHARS = {
    "\u202f": ("U+202F", "NARROW NO-BREAK SPACE", " "),
    "\u00a0": ("U+00A0", "NO-BREAK SPACE", " "),
    "\u200b": ("U+200B", "ZERO WIDTH SPACE", ""),
    "\u200c": ("U+200C", "ZERO WIDTH NON-JOINER", ""),
    "\u200d": ("U+200D", "ZERO WIDTH JOINER", ""),
    "\ufeff": ("U+FEFF", "BYTE ORDER MARK / ZWNBSP", ""),
}


@dataclass(frozen=True)
class PatternRule:
    rule_id: str
    lang: str  # "ko", "en", "ja", "zh-cn", "zh-tw", "zh", "all"
    family: str  # independent signal family or "model_fingerprint" / "x_tier_info"
    tier: str  # "P1", "P2", "A", "B", "C", "D", "F", "X"
    label: str
    pattern: str
    weight: int
    exclude: str | None = None
    flags: int = 0
    directional_only: bool = False
    informational_only: bool = False
    skip_genres: tuple[str, ...] = ()
    only_genres: tuple[str, ...] = ()
    suggestion: str = ""


@dataclass
class Hit:
    rule_id: str
    family: str
    tier: str
    label: str
    match: str
    line: int
    snippet: str
    weight: int
    directional_only: bool = False
    informational_only: bool = False
    suggestion: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "family": self.family,
            "tier": self.tier,
            "label": self.label,
            "match": self.match,
            "line": self.line,
            "snippet": self.snippet,
            "weight": self.weight,
            "directional_only": self.directional_only,
            "informational_only": self.informational_only,
            "suggestion": self.suggestion,
        }


# ---------------------------------------------------------------------------
# Rule Catalog (4 Languages, Grounded in Verified Empirical Research)
# ---------------------------------------------------------------------------

def _build_rules() -> list[PatternRule]:
    rules: list[PatternRule] = []

    # ==================== KOREAN (ko) ====================
    # Family: contrast_staging
    rules.extend([
        PatternRule(
            "KO-C8-01", "ko", "contrast_staging", "A",
            "부정 대구·반전 클리셰 (단순히 A가 아니라 B)",
            r"(?:단순히|단지|그저)\s+[^.!?\n]{1,40}?(?:이|가)?\s*아니라\b|에\s*그치지\s*않고|에\s*머무르지\s*않고",
            weight=14,
            suggestion="독자의 실제 오해를 교정하는 경우가 아니면 앞의 부정을 걷어내고 핵심을 정면 서술하세요.",
        ),
        PatternRule(
            "KO-C8-02", "ko", "contrast_staging", "A",
            "비교·반전 클리셰 (~보다 ~에 가깝다 / 문제가 아니라)",
            r"보다(?:는)?\s+[^.!?\n]{1,30}?에\s*가깝(?:습니다|다|고)|문제가\s*아니라\s+[^.!?\n]{1,25}?(?:문제|이슈|과제)",
            weight=10,
            suggestion="간접 비교 틀을 걷어내고 무엇인지 직접 서술하세요.",
        ),
    ])

    # Family: translationese_syntax
    rules.extend([
        PatternRule(
            "KO-TR-01", "ko", "translationese_syntax", "B",
            "번역투 조사 (~를 통해 / ~에 대해 / ~에 있어서 / ~에 의해)",
            r"(?:을|를)\s*통해서?|에\s*대해서?|에\s*있어서|에\s*의해서?",
            weight=6,
            suggestion="조사('로', '에서')나 능동 동사로 자연스럽게 풀어 쓰세요.",
        ),
        PatternRule(
            "KO-TR-02", "ko", "translationese_syntax", "B",
            "이중 피동 (되어지다 / 보여지다 / 불려지다 / 믿어지다)",
            r"(?:되어|보여|불려|믿어|쓰여|느껴|읽혀|만들어)지(?:는|ㄴ|다|고|며|면|었|았|습니다|ㅂ니다)",
            weight=10,
            suggestion="단일 피동('된다/보인다/불린다') 또는 능동형으로 고치세요.",
        ),
        PatternRule(
            "KO-TR-03", "ko", "translationese_syntax", "B",
            "숨은 동사 / 명사화 과잉 (검토를 진행 / 분석을 실시 / 결정을 내리다)",
            r"(?:검토|분석|개선|조사|점검|논의|평가|적용|구현|테스트|작업|연구)(?:를|을)\s*(?:진행|수행|실시)(?:하|했|합|할|한|해)|결정(?:을)?\s*내리(?:다|고|며|는|ㄴ|었|습니다)",
            weight=8,
            suggestion="직접 동사('검토하다', '분석하다', '개선하다', '결정하다')로 줄이세요.",
        ),
        PatternRule(
            "KO-TR-04", "ko", "translationese_syntax", "B",
            "이중 조사 (~에서의 / ~에로의 / ~으로의)",
            r"(?:에서|으로|로|에로|에게로)의\s+[가-힣]",
            weight=6,
            suggestion="관형절로 풀거나 불필요한 '의'를 덜어내세요.",
        ),
        PatternRule(
            "KO-TR-05", "ko", "translationese_syntax", "B",
            "다중 완곡·형식명사 (~할 수 있을 것으로 보인다/기대된다 / ~라고 할 수 있)",
            r"할\s*수\s*있을\s*것으로\s*(?:보인다|보입니다|기대된다|기대됩니다|예상된다|판단된다)|라고\s*할\s*수\s*있(?:다|습니다)",
            weight=9,
            suggestion="불필요한 완곡 겹침을 걷어내고 근거에 맞는 단정 수준으로 쓰세요.",
        ),
    ])

    # Family: ai_boilerplate
    rules.extend([
        PatternRule(
            "KO-BP-01", "ko", "ai_boilerplate", "A",
            "감각적 추상명사 조합 & 빈 행동 동사 (@conbowl 패턴)",
            r"(?:정서|감정|마음|시선|기억|생각|문장|브랜드|이야기)의\s*결|(?:여운|감정|경험|몰입|관계)의\s*농도|(?:맥락|관계|경험|사고|이야기|감정)의\s*밀도|함께\s*봅니다",
            weight=14,
            suggestion="추상적 미사여구 대신 실제 행동·지표·산출물로 풀어 쓰세요.",
        ),
        PatternRule(
            "KO-BP-02", "ko", "ai_boilerplate", "A",
            "선언형·요약형 마무리 & 챗봇 잔여물",
            r"(?:^|[\n.?!]\s*)(?:결론적으로|요약하자면|정리하자면|종합해\s*보면)|시사하는\s*바가\s*(?:크(?:다|습니다|며|고)|큰)|주목할\s*만하(?:다|습니다|며|고)|기준은\s*분명합니다|알아보았습니다|도움이\s*되셨길\s*바랍니다|앞으로가\s*기대됩니다|중요한\s*것은\s+[^.!?\n]{1,35}?(?:입니다|이다)",
            weight=12,
            suggestion="새 정보가 없는 요약 틀을 삭제하고 직전 구체 사실에서 마무리하세요.",
        ),
        PatternRule(
            "KO-BP-03", "ko", "ai_boilerplate", "B",
            "자소서·보고서 AI 합성어 클리셰 (@jayber_jobpartner 패턴)",
            r"구조적\s*접근|실질적\s*성과|업무\s*맥락|업무\s*흐름|작동\s*구조|운영\s*관점",
            weight=7,
            suggestion="사전적 합성어를 일상 업무 동사와 구체적 수치·결과로 바꾸세요.",
        ),
    ])

    # Family: lexical_traps (KO P1 — context-checked with literal exclusions, also used in verify restore gate!)
    rules.extend([
        PatternRule(
            "KO-LEX-P1-01", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '렌즈' (관점 은유)",
            r"(?<![가-힣])렌즈(?:로|를|가|는|의|에|와|도|라는)?(?![가-힣])",
            weight=14,
            exclude=r"카메라|안경|광학|망원경|현미경|콘택트|초점|촬영|필터|미러리스|구면|유리|눈|시력|굴절|줌",
            suggestion="관점·시각 은유라면 '관점에서 보면'으로 바꾸거나 틀 구절을 삭제하세요.",
        ),
        PatternRule(
            "KO-LEX-P1-02", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '축' (분류·기준 은유)",
            r"(?:두|세|네|양|핵심|주요|큰|중심)\s*(?:개의\s*)?축(?:을|이|으로|에|은|이다)?(?![가-힣])|(?<![가-힣])축(?:으로|을)\s*(?:삼|놓|나누|구성|정리)",
            weight=12,
            exclude=r"회전축|좌표축|차축|기계|모터|엔진|바퀴|가로축|세로축|[xyzXYZ]축|지구|자전|지축|선반",
            suggestion="'두 가지 기준' 또는 구체 항목으로 직접 서술하세요.",
        ),
        PatternRule(
            "KO-LEX-P1-03", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '기둥' (전략·정책 핵심 요소 은유)",
            r"(?:세|두|네|핵심|주요)\s*(?:개의\s*)?기둥|(?<![가-힣])기둥(?:으로|이)\s*(?:삼|세우|받치|역할)",
            weight=13,
            exclude=r"건물|집안의\s*기둥|팀의\s*기둥|가정의\s*기둥|건축|돌기둥|나무기둥|교각|콘크리트|벽|천장|지붕",
            suggestion="'핵심 과제', '세 가지 원칙' 등으로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-04", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '층위' (단계/수준 대체)",
            r"(?<![가-힣])층위(?:가|를|는|에|로|에서|의|와|도)?(?![가-힣])",
            weight=13,
            exclude=r"지질|지층|암석|퇴적|고고학|화석|층위학",
            skip_genres=("academic",),
            suggestion="'단계', '수준', '측면'으로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-05", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '짚다' (설명 전환 상투어)",
            r"짚고\s*(?:가|간|넘어가|보)|짚어\s*(?:보|볼|봤|봅|드)",
            weight=12,
            exclude=r"맥을\s*짚|지팡이|손을\s*짚|바닥을\s*짚|땅을\s*짚|벽을\s*짚|난간",
            suggestion="전환 상투어를 삭제하고 바로 본론으로 들어가세요.",
        ),
        PatternRule(
            "KO-LEX-P1-06", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '쥐다' (보유·주도권 은유)",
            r"(?:대안|길목|주도권|열쇠|해법|카드|방향|핵심|승기|권력|판)(?:을|를)\s*쥐(?:고|었|는|ㄴ|어)|(?<![가-힣])쥔\s*(?:채|쪽|사람|기업)",
            weight=12,
            exclude=r"손에\s*쥐|손으로\s*쥐|주먹을\s*쥐|펜을\s*쥐|칼을\s*쥐|지갑|물건|막대|핸들|마이크|우산|공을",
            suggestion="'가진', '차지한', '맡은' 등 일상 동사로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-07", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '얹다' (기술·기능 추가 직역)",
            r"(?:위에|위로)\s*얹(?:은|어|는|고|힌|혀)|(?:계층|기능|레이어|모델|서비스|도구|전략|규칙)(?:을|를)\s*얹",
            weight=12,
            exclude=r"밥|반찬|그릇|접시|냄비|불\s*위에|머리\s*위에|손을\s*얹|어깨에|이불|토핑|치즈|고기|김치|소금|떡",
            suggestion="'덧붙이다', '더하다', '올리다'로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-08", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '잠금 해제' (unlock 직역)",
            r"잠금\s?해제|잠금을\s*(?:해제|풀|푸)|(?:잠재력|역량|창의성|가능성)(?:을|를)\s*(?:해방|해제|풀어\s?놓)",
            weight=15,
            exclude=r"스마트폰|화면|계정|기능|비밀번호|기기|아이폰|갤럭시|앱|휴대폰|단말|지문|패턴|암호|도어락|자물쇠|잠금화면",
            suggestion="'잠재력을 발휘하다', '역량을 끌어내다'로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-09", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '무늬' (추상 쟁점 은유)",
            r"(?:논의|담론|시대|삶|관계|갈등|사유|생각|감정|기억)의\s*무늬|(?<![가-힣])무늬(?:가|를|는)\s*(?:드러나|읽|그려지|달라지)",
            weight=14,
            exclude=r"옷|천|벽지|꽃|물방울|호랑이|얼룩|도자기|타일|체크|문양|원단|깃털|나무|표범|돌|날개|가죽|비늘|직물|토기|빗살|지느러미|피부",
            suggestion="'쟁점', '양상', '차이' 등 원래 명사로 복원하세요.",
        ),
        PatternRule(
            "KO-LEX-P1-10", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '벼리다' (추상 명사 목적어)",
            r"벼[리려렸린릴](?:다|고|며|는|ㄴ|어|었|보)?",
            weight=14,
            exclude=r"칼|낫|연장|쇠|대장간|날을|도끼|검을|창을",
            suggestion="'추리다', '다듬다', '정리하다'로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-11", "ko", "lexical_traps", "P1",
            "P1 번역투 어휘: '길어 올리다 / 건져 올리다'",
            r"길어\s*(?:올리|올려|올린|올렸|올릴)|건져\s*올[리려린렸릴]",
            weight=13,
            exclude=r"물을|우물|샘|두레박|물고기|그물|바다|강에서|낚|양동이",
            suggestion="'분석하다', '찾아내다', '뽑아내다'로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P1-12", "ko", "lexical_traps", "P1",
            "P1 영어 연어 직역 (성공을 달성 / 결과를 전달 / 정보에 입각한 결정)",
            r"성공을\s*달성|결과를\s*전달|정보에\s*입각한\s*(?:결정|판단|선택)|게임\s*체인저|패러다임\s*시프트",
            weight=14,
            suggestion="'성과를 내다', '결과를 내다', '근거를 보고 판단하다'로 바꾸세요.",
        ),
        # KO P2 (conditional)
        PatternRule(
            "KO-LEX-P2-01", "ko", "lexical_traps", "P2",
            "P2 조건부 어휘: '본질적으로 / 궁극적으로'",
            r"(?<![가-힣])(?:본질적으로|궁극적으로)(?![가-힣])",
            weight=6,
            skip_genres=("academic",),
            suggestion="습관적 강조라면 삭제하거나 '결국' 등으로 바꾸세요.",
        ),
        PatternRule(
            "KO-LEX-P2-02", "ko", "lexical_traps", "P2",
            "P2 조건부 어휘: '~로 기능한다 / 지형도 / 여정'",
            r"(?:으)?로\s*기능(?:한다|합니다|하고|하며)|(?<![가-힣])(?:지형도|여정(?:을|이|은|의|에)?)(?![가-힣])",
            weight=7,
            exclude=r"여행|비행기|기차|항공|출발|도착|숙소|등산|지도|지리|산맥|해발",
            suggestion="'역할을 한다', '시장 구도', '과정'으로 구체화하세요.",
        ),
        PatternRule(
            "KO-LEX-P2-03", "ko", "lexical_traps", "P2",
            "P2 조건부 어휘: '~하는 편이 좋습니다/낫습니다'",
            r"(?:는|은)\s*편이\s*(?:좋습니다|좋다|낫습니다|낫다)",
            weight=5,
            exclude=r"보다(?:는)?\s+[^.!?\n]{1,30}?편이",
            suggestion="비교 대상이 없는 반복 권고라면 '~하세요' 또는 '~하는 게 안전합니다'로 바꾸세요.",
        ),
    ])

    # ==================== ENGLISH (en) ====================
    # Family: contrast_staging
    rules.extend([
        PatternRule(
            "EN-A-01", "en", "contrast_staging", "A",
            "Negative parallelism (Not just X, but Y / It's not X—it's Y)",
            r"(?:\b(?:is|are|was|were)|'s)\s+not\s+(?:just|merely|simply|only)\s+[^.!?\n]{2,60}?(?:,\s*|\s*—\s*|\s+)(?:but\s+(?:also\s+)?|it's\s+|they're\s+)|(?:it's|that's|this\s+is)\s+not\s+[^.!?\n]{2,45}?(?:,\s*|\s*—\s*)(?:it's|that's)\s+|\bnot\s+because\s+[^.!?\n]{2,50}?,\s*but\s+because\b",
            weight=14,
            flags=re.IGNORECASE,
            suggestion="State what it IS directly unless correcting an actual reader misconception.",
        ),
        PatternRule(
            "EN-A-02", "en", "contrast_staging", "A",
            "Dramatic one-line closer / LinkedIn pull-quote",
            r"(?:^|[\n.!?]\s*)(?:That(?:'s|\s+is)\s+the\s+real\s+(?:win|story|lesson|point|shift)\.?|Let\s+that\s+sink\s+in\.?|Read\s+that\s+again\.?|Full\s+stop\.?|No\s+excuses\.\s+No\s+shortcuts\.?)",
            weight=14,
            flags=re.IGNORECASE,
            suggestion="Delete theatrical closers unless they add a genuinely new fact.",
        ),
        PatternRule(
            "EN-A-03", "en", "contrast_staging", "A",
            "Fake-deep aphorism / staged run-up",
            r"\b(?:at\s+its\s+core|what\s+really\s+matters\s+is|the\s+real\s+question\s+is|let's\s+dive\s+in|without\s+further\s+ado|here's\s+the\s+thing)\b",
            weight=12,
            flags=re.IGNORECASE,
            suggestion="Cut the throat-clearing wind-up and name the mechanism immediately.",
        ),
        PatternRule(
            "EN-A-04", "en", "contrast_staging", "A",
            "Phantom objection / arguing with no one",
            r"\b(?:to\s+be\s+clear,\s+I'm\s+not\s+saying|don't\s+get\s+me\s+wrong|a\s+tempting\s+approach\s+would\s+be|some\s+might\s+(?:say|argue))\b",
            weight=10,
            flags=re.IGNORECASE,
            suggestion="Cut unattributed strawmen; address only real reader objections.",
        ),
    ])

    # Family: ai_boilerplate (RLHF voice)
    rules.extend([
        PatternRule(
            "EN-B-01", "en", "ai_boilerplate", "A",
            "RLHF chatbot wrapper / sycophancy",
            r"(?:^|[\n]\s*)(?:Great\s+question!|Certainly!|Absolutely!|Of\s+course!|Sure\s+thing!)|I\s+hope\s+this\s+helps!?|Let\s+me\s+know\s+if\s+you(?:'d|\s+would)\s+like|Feel\s+free\s+to\s+(?:ask|reach\s+out)",
            weight=15,
            flags=re.IGNORECASE,
            suggestion="Strip assistant preamble and closing filler completely.",
        ),
        PatternRule(
            "EN-B-02", "en", "ai_boilerplate", "B",
            "Autopilot transitions & boilerplate wrap-ups",
            r"(?:^|[\n.!?]\s*)(?:Furthermore|Moreover|Additionally|In\s+conclusion|All\s+in\s+all|Ultimately|Notably|Importantly),\s+",
            weight=8,
            flags=re.IGNORECASE,
            suggestion="Drop mechanical transition words when sentence order carries the logic.",
        ),
        PatternRule(
            "EN-B-03", "en", "ai_boilerplate", "B",
            "Formulaic academic/blog opener",
            r"\b(?:In\s+(?:today's|the)\s+(?:fast-paced|ever-evolving|rapidly\s+evolving|modern)\s+(?:world|landscape|era)|In\s+recent\s+years,\s+[^.!?\n]{2,50}?\s+has\s+(?:attracted|gained)\s+increasing\s+attention)\b",
            weight=13,
            flags=re.IGNORECASE,
            suggestion="Start directly at the specific problem, dataset, or observation.",
        ),
    ])

    # Family: translationese_syntax (EN copula avoidance & shallow -ing riders)
    rules.extend([
        PatternRule(
            "EN-C-01", "en", "translationese_syntax", "C",
            "Copula avoidance (serves as / stands as / functions as / boasts)",
            r"\b(?:serves|stands|functions)\s+as\s+(?:a|an|the)\b|\b(?:boasts|features)\s+(?:a|an)\s+(?:robust|seamless|comprehensive|wide|rich)\b",
            weight=9,
            flags=re.IGNORECASE,
            suggestion="Replace pretentious verbs with plain 'is', 'are', or 'has'.",
        ),
        PatternRule(
            "EN-C-02", "en", "translationese_syntax", "C",
            "Shallow participle (-ing) consequence rider",
            r",\s+(?:highlighting|underscoring|showcasing|fostering|reflecting|demonstrating|emphasizing|ensuring|paving\s+the\s+way\s+for)\s+(?:its|the|a|an|how|that)\b",
            weight=10,
            flags=re.IGNORECASE,
            suggestion="Cut bolted-on -ing commentary unless it adds a concrete new fact.",
        ),
    ])

    # Family: lexical_traps (EN P1 & P2)
    rules.extend([
        PatternRule(
            "EN-LEX-P1-01", "en", "lexical_traps", "P1",
            "P1 English AI vocabulary (delve/tapestry/testament/pivotal/vibrant/seamless/meticulously/garner/supercharge/game-changer)",
            r"\b(?:delve(?:s|d|ing)?|tapestry|testament\s+to|pivotal|vibrant|seamless(?:ly)?|meticulously|garner(?:s|ed|ing)?|supercharge(?:s|d|ing)?|game[- ]changer)\b",
            weight=14,
            flags=re.IGNORECASE,
            suggestion="Replace AI-clustered hype words with plain, concrete verbs/nouns.",
        ),
        PatternRule(
            "EN-LEX-P1-02", "en", "lexical_traps", "P1",
            "P1 English AI vocabulary: figurative 'landscape' / 'unlock potential'",
            r"\b(?:ever-evolving|digital|competitive|business|AI|tech|regulatory|media|political)\s+landscape\b|\bunlock(?:s|ed|ing)?\s+(?:new\s+|full\s+|hidden\s+|your\s+|its\s+|their\s+)?(?:potential|power|creativity|value|growth|insights|possibilities)\b",
            weight=14,
            exclude=r"mountain|valley|painting|photo|garden|terrain|desert|scenery|smart\s*phone|screen|door|account|password|device",
            flags=re.IGNORECASE,
            suggestion="Name the actual market/field or state the concrete gain directly.",
        ),
        PatternRule(
            "EN-LEX-P2-01", "en", "lexical_traps", "P2",
            "P2 English AI vocabulary (crucial/robust/leverage/foster/intricate/quietly)",
            r"\b(?:crucial|robust|leverage(?:s|d|ing)?|foster(?:s|ed|ing)?|intricate|quietly\s+(?:transform|reshap|chang|redefin))\b",
            weight=6,
            exclude=r"statistically\s+robust|financial\s+leverage|debt\s+leverage|foster\s+(?:care|parent|home|child)",
            flags=re.IGNORECASE,
            suggestion="When clustered, replace with specific measurable wording.",
        ),
    ])

    # ==================== JAPANESE (ja) ====================
    # Family: translationese_syntax (meiseki A/B/C)
    rules.extend([
        PatternRule(
            "JA-A-01", "ja", "translationese_syntax", "A",
            "二重否定 (〜ないとは言えません / 〜ないわけではありません)",
            r"(?:ない|ません)とは(?:言えません|言い切れません|限らない|限りません)|ないわけでは(?:ありません|ない)|否定(?:は)?でき(?:ません|ない)",
            weight=13,
            suggestion="肯定表現へ簡潔に言い換えてください（極性反転に注意）。",
        ),
        PatternRule(
            "JA-B-01", "ja", "translationese_syntax", "B",
            "冗長な可能表現・受身 (〜することができます / 〜が行われる)",
            r"することができ(?:ます|る|た|ました)|が行われ(?:ます|る|た|ました)",
            weight=8,
            suggestion="「〜できます」「（主語）が〜します」と能動・簡潔にしてください。",
        ),
        PatternRule(
            "JA-C-01", "ja", "translationese_syntax", "B",
            "「の」の連続連鎖 (4連以上)",
            r"[一-龥ァ-ヶーA-Za-z0-9]{1,12}の[一-龥ァ-ヶーA-Za-z0-9]{1,12}の[一-龥ァ-ヶーA-Za-z0-9]{1,12}の[一-龥ァ-ヶーA-Za-z0-9]{1,12}の",
            weight=9,
            suggestion="名詞連鎖を動詞句に分解してください。",
        ),
    ])

    # Family: contrast_staging (JA)
    rules.extend([
        PatternRule(
            "JA-ST-01", "ja", "contrast_staging", "A",
            "否定対比の構文 (単なる〜ではなく / 〜にとどまらず)",
            r"(?:単なる|ただの)[^。！？\n]{1,30}?ではなく|にとどまらず",
            weight=12,
            suggestion="誤解を解く必要がなければ、結論を直接述べてください。",
        ),
    ])

    # Family: ai_boilerplate (JA Tier D)
    rules.extend([
        PatternRule(
            "JA-D-01", "ja", "ai_boilerplate", "A",
            "AI定型導入・結び (本記事では / いかがでしたでしょうか / と言えるでしょう)",
            r"本記事では[^。！？\n]{1,40}?(?:解説|紹介|説明)します|近年、[^。！？\n]{1,40}?重要な(?:課題|テーマ)となってい(?:ます|る)|いかがでしたでしょうか|と言えるでしょう|お役に立てれば幸いです",
            weight=13,
            suggestion="定型挨拶・まとめを削り、具体的な事実や結論から始めてください。",
        ),
    ])

    # Family: formatting_decoration (JA Tier E — textlint predicate+colon)
    rules.extend([
        PatternRule(
            "JA-E-01", "ja", "formatting_decoration", "B",
            "英語調 述語+コロン接続 (実行します: / 行います:)",
            r"(?:します|ます|です|する|ある|いる)[:：]\s*(?:\r?\n\s*(?:[-*+•]|\d+\.|```))",
            weight=10,
            suggestion="「〜は以下の通りです。」など自然な日本語の文末にしてください。",
        ),
    ])

    # Family: lexical_traps (JA P1 & P2)
    rules.extend([
        PatternRule(
            "JA-LEX-P1-01", "ja", "lexical_traps", "P1",
            "P1 日本語AI誇張語彙 (ゲームチェンジャー / パラダイムシフト / 可能性を解き放つ / スーパーチャージ / シームレス / 革命的)",
            r"ゲームチェンジャー|パラダイムシフト|スーパーチャージ|(?:可能性|潜在能力)を解き放つ|シームレス(?:な|に)?|革命的(?:な|に)?",
            weight=14,
            suggestion="具体的な機能・数値・変化で言い換えてください。",
        ),
        PatternRule(
            "JA-LEX-P2-01", "ja", "lexical_traps", "P2",
            "P2 日本語ビジネスAI常套句 (包括的 / ダイナミック / 解像度が高い / 泥臭さ)",
            r"包括的(?:な|に)?|ダイナミック(?:な|に)?|解像度(?:を上げ|が高)|泥臭(?:い|さ)",
            weight=7,
            exclude=r"画面|モニター|画像|ディスプレイ|4K|ピクセル|dpi",
            suggestion="何をどこまで具体的に扱うか明示してください。",
        ),
    ])

    # ==================== CHINESE SIMPLIFIED & TRADITIONAL (zh-cn / zh-tw) ====================
    # Family: contrast_staging (Empirically strongest pure writing signal in 5.2M-char study!)
    rules.extend([
        PatternRule(
            "ZH-U-01", "zh", "contrast_staging", "A",
            "翻案腔 / 欧化对举 (不是A而是B / 并非…而是… / 与其说…不如说… / 你以为…其实…)",
            r"(?:不仅仅|不仅|不只是|不是|並非|并非|不僅僅|不僅)[^。！？\n]{1,35}?(?:而是|，而是)|与其说[^。！？\n]{1,30}?不如说|與其說[^。！？\n]{1,30}?不如說|表面(?:上)?[^。！？\n]{1,25}?(?:实则|实际|實則|實際)|你以为[^。！？\n]{1,25}?其实|你以為[^。！？\n]{1,25}?其實",
            weight=15,
            suggestion="直接陈述判断，删去多余的否定铺垫。",
        ),
        PatternRule(
            "ZH-U-02", "zh", "ai_boilerplate", "A",
            "结论提示冒号 (核心是： / 残酷的现实是： / 一句话总结： / 关键在于：)",
            r"(?:核心|关键|關鍵|真相|本质|本質|结论|結論|答案|残酷的现实|殘酷的現實|一句话总结|一句話總結)(?:是|在于|在於)?[:：](?!\s*\r?\n\s*(?:[-*+\d]|一、|1\.))",
            weight=13,
            suggestion="删去提示壳，或改用句号/逗号直接说出结论。",
        ),
        PatternRule(
            "ZH-U-03", "zh", "ai_boilerplate", "A",
            "起手式 / 空洞结尾 (说白了 / 说穿了 / 先说结论 / 让我们一起携手)",
            r"(?:^|[\n。！？]\s*)(?:说白了|說白了|说穿了|說穿了|先说结论|先說結論|老实说|老實說)[，,：:\s]|让我们(?:一起)?携手|讓我們(?:一起)?攜手|拥抱(?:更美好的)?未来|擁抱(?:更美好的)?未來",
            weight=12,
            suggestion="删去口水起手式或空洞升华，直接进入论点或停在最后一个具体事实。",
        ),
    ])

    # Family: translationese_syntax (ZH 4 proven translationese structures)
    rules.extend([
        PatternRule(
            "ZH-TR-01", "zh", "translationese_syntax", "B",
            "欧化时间从句 (当……时 / 當……時)",
            r"[当當][^。！？\n]{3,35}?(?:的)?[时時](?:候)?[，,]?",
            weight=8,
            suggestion="若时间关系明确，去掉「当……时」外壳直接叙述。",
        ),
        PatternRule(
            "ZH-TR-02", "zh", "translationese_syntax", "B",
            "前置话题壳 (对于……来说 / 就……而言 / 在……方面)",
            r"(?:对于|對於)[^。！？\n]{2,20}?(?:来说|來說|而言)|(?:就)[^。！？\n]{2,18}?而言|在[^。！？\n]{2,18}?方面[，,]",
            weight=8,
            suggestion="若该名词已是主语，删去前置壳直接作主语。",
        ),
        PatternRule(
            "ZH-TR-03", "zh", "translationese_syntax", "B",
            "过长前置定语 (同一名语前连续3个以上「的」)",
            r"[^，。！？；\n]{2,14}的[^，。！？；\n]{2,14}的[^，。！？；\n]{2,14}的[\u4e00-\u9fff]{2,10}",
            weight=9,
            suggestion="将长前置定语拆成两个短分句。",
        ),
    ])

    # Family: lexical_traps (ZH P1 — excluding X-tier myths!)
    rules.extend([
        PatternRule(
            "ZH-LEX-P1-01", "zh", "lexical_traps", "P1",
            "P1 中文AI直译/套话 (解锁潜力 / 织锦 / 游戏规则改变者 / 范式转移 / 无缝衔接 / 深刻重塑)",
            r"解锁[^。！？\n]{0,8}(?:潜力|潜能|可能|价值)|解鎖[^。！？\n]{0,8}(?:潛力|潛能|可能|價值)|织锦|織錦|游戏规则改变者|遊戲規則改變者|范式转移|範式轉移|无缝衔接|無縫銜接|深刻重塑",
            weight=14,
            exclude=r"手机|手機|屏幕|螢幕|密码|密碼|账号|帳號|门锁|門鎖|丝绸|絲綢|刺绣|刺繡",
            suggestion="用具体动作和真实结果替代英文直译套话。",
        ),
    ])

    # Traditional Chinese / Taiwan specific rules (zh-tw)
    rules.extend([
        PatternRule(
            "ZHTW-01", "zh-tw", "translationese_syntax", "B",
            "台灣用語漂移 (大陸科技/職場詞混入繁體文本)",
            r"软件|视频|信息|优化|项目|数据|质量|激活|打印|硬盘|内存|鼠标|服务器|代码|算法|用户体验|智能家居|人工智能",
            weight=9,
            suggestion="若面向台灣讀者，建議改為台灣常用詞（如：軟體、影片、資訊、改善、專案、資料、品質、程式碼、演算法）。",
        ),
        PatternRule(
            "ZHTW-02", "zh-tw", "formatting_decoration", "B",
            "繁體中文混用半形標點 (! , ? : ;)",
            r"[\u4e00-\u9fff]\s*[,!?;]\s*[\u4e00-\u9fff]",
            weight=8,
            suggestion="中文語句間請統一使用全形標點（，、！、？、；）。",
        ),
    ])

    # X-Tier Debunked Chinese Myths (Informational ONLY — zero penalty, zero family activation!)
    rules.extend([
        PatternRule(
            "ZH-X-01", "zh", "x_tier_info", "X",
            "[X-Tier 误区提醒] 「首先/其次/总之」「这意味着/这表明」「赋能/闭环/抓手」",
            r"首先|其次|总之|總之|这意味着|這意味著|这表明|這表明|赋能|賦能|闭环|閉環|抓手",
            weight=0,
            informational_only=True,
            suggestion="520万字双语料实证表明上述词在2026年模型上已无显著区分度或人类用得更多，切勿机械删除。",
        ),
    ])

    # ==================== CROSS-LANGUAGE FORMATTING & DECORATION ====================
    rules.extend([
        PatternRule(
            "FMT-01", "all", "formatting_decoration", "C",
            "Decorative bold+colon bullet list (- **Label**: ...)",
            r"(?m)^\s*[-*+]\s+\*\*[^*\n]{2,35}[:：]?\*\*\s*[:：]",
            weight=8,
            suggestion="Convert mechanical bold-label bullets into connected prose unless scanning a reference table.",
        ),
        PatternRule(
            "FMT-02", "all", "formatting_decoration", "C",
            "Emoji confetti / decorative AI icons",
            r"[🚀💡✨🎯🔥📌✅❌⚡🌟👉👇🧵]",
            weight=6,
            skip_genres=("sns",),
            suggestion="Strip decorative emojis outside casual SNS posts.",
        ),
    ])

    return rules


RULES = _build_rules()


# ---------------------------------------------------------------------------
# Protected Span Masking & Token Extraction
# ---------------------------------------------------------------------------

def _mask_with_spaces(text: str, start: int, end: int) -> str:
    """Replace text[start:end] with spaces while preserving newlines to keep line numbers exact."""
    segment = text[start:end]
    return "".join("\n" if ch == "\n" else " " for ch in segment)


def mask_protected_spans(text: str, mask_quotes: bool = True) -> tuple[str, dict[str, int]]:
    """Return a masked copy of text where protected spans are replaced by spaces (keeping \\n)."""
    chars = list(text)
    counts: dict[str, int] = {
        "frontmatter": 0,
        "fenced_code": 0,
        "inline_code": 0,
        "math": 0,
        "urls": 0,
        "quotes": 0,
    }

    def apply_mask(pattern: str, key: str, flags: int = 0) -> None:
        current = "".join(chars)
        for m in re.finditer(pattern, current, flags):
            counts[key] += 1
            for i in range(m.start(), m.end()):
                if chars[i] != "\n":
                    chars[i] = " "

    # 1. YAML frontmatter at top of document
    apply_mask(r"\A---\r?\n.*?\r?\n---(?:\r?\n|\Z)", "frontmatter", re.DOTALL)
    # 2. Fenced code blocks (``` or ~~~)
    apply_mask(r"(?m)^[ \t]*(?:```|~~~)[^\n]*\r?\n.*?\r?\n[ \t]*(?:```|~~~)[ \t]*(?:\r?\n|\Z)", "fenced_code", re.DOTALL)
    # 3. Inline code (`...`)
    apply_mask(r"`[^`\n]+`", "inline_code")
    # 4. Display math ($$...$$) and LaTeX \(...\) / \[...\]
    apply_mask(r"\$\$.+?\$\$|\\\[.+?\\\]|\\\(.+?\\\)", "math", re.DOTALL)
    # 5. URLs
    apply_mask(r"(?:https?|file)://[^\s)>\]]+", "urls")
    # 6. Direct quotations (for slop scanning; NOT masked for clean-unicode)
    if mask_quotes:
        apply_mask(r'“[^”\n]{2,400}”|「[^」\n]{2,400}」|『[^』\n]{2,400}』|"[^"\n]{2,400}"', "quotes")

    return "".join(chars), counts


def _is_emoji_like(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x1F000 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or cp in (0xFE0F, 0x20E3)
    )


def detect_invisible_unicode(text: str) -> dict[str, Any]:
    """Detect invisible Unicode artifacts outside code/frontmatter/URLs."""
    masked, _ = mask_protected_spans(text, mask_quotes=False)
    counts: dict[str, int] = {}
    positions: list[dict[str, Any]] = []
    nfd_warnings: list[dict[str, Any]] = []
    replacement_count = 0

    line = 1
    for idx, ch in enumerate(masked):
        if ch == "\n":
            line += 1
            continue
        if ch in INVISIBLE_CHARS:
            # Do not flag ZWJ when legitimately joining emoji pictographs
            if ch == "\u200d":
                prev_ch = text[idx - 1] if idx > 0 else ""
                next_ch = text[idx + 1] if idx + 1 < len(text) else ""
                if _is_emoji_like(prev_ch) or _is_emoji_like(next_ch):
                    continue
            code, name, _ = INVISIBLE_CHARS[ch]
            counts[code] = counts.get(code, 0) + 1
            if len(positions) < 25:
                positions.append({"code": code, "name": name, "line": line, "offset": idx})
        elif ch == "\ufffd":
            replacement_count += 1
        elif 0x1100 <= ord(ch) <= 0x11FF or ord(ch) in (0x3099, 0x309A):
            if len(nfd_warnings) < 10:
                nfd_warnings.append({"code": f"U+{ord(ch):04X}", "name": unicodedata.name(ch, "COMBINING"), "line": line})

    total = sum(counts.values())
    return {
        "total": total,
        "counts": counts,
        "positions": positions,
        "replacement_chars": replacement_count,
        "nfd_warnings": nfd_warnings,
    }


def clean_invisible_unicode(text: str) -> tuple[str, dict[str, Any]]:
    """Scrub invisible Unicode artifacts outside fenced/inline code blocks and frontmatter."""
    masked, _ = mask_protected_spans(text, mask_quotes=False)
    out_chars: list[str] = []
    removed: dict[str, int] = {}
    nfd_warnings = 0
    replacement_chars = 0

    for idx, orig_ch in enumerate(text):
        masked_ch = masked[idx]
        # Inside protected code/frontmatter/URL: masked_ch is ' ' while orig_ch may differ
        is_protected = (masked_ch == " " and orig_ch != " ")
        if not is_protected and orig_ch in INVISIBLE_CHARS:
            if orig_ch == "\u200d":
                prev_ch = text[idx - 1] if idx > 0 else ""
                next_ch = text[idx + 1] if idx + 1 < len(text) else ""
                if _is_emoji_like(prev_ch) or _is_emoji_like(next_ch):
                    out_chars.append(orig_ch)
                    continue
            code, _, replacement = INVISIBLE_CHARS[orig_ch]
            removed[code] = removed.get(code, 0) + 1
            if replacement:
                out_chars.append(replacement)
            continue
        if not is_protected:
            if orig_ch == "\ufffd":
                replacement_chars += 1
            elif 0x1100 <= ord(orig_ch) <= 0x11FF or ord(orig_ch) in (0x3099, 0x309A):
                nfd_warnings += 1
        out_chars.append(orig_ch)

    summary = {
        "total_cleaned": sum(removed.values()),
        "cleaned_by_code": removed,
        "replacement_chars_warn": replacement_chars,
        "nfd_combining_warn": nfd_warnings,
    }
    return "".join(out_chars), summary


# ---------------------------------------------------------------------------
# Language & Genre Detection
# ---------------------------------------------------------------------------

def detect_language(text: str, override: str = "auto") -> str:
    if override in ("ko", "en", "ja", "zh-cn", "zh-tw"):
        return override
    masked, _ = mask_protected_spans(text, mask_quotes=False)
    hangul = len(re.findall(r"[\uac00-\ud7a3\u3131-\u318e]", masked))
    kana = len(re.findall(r"[\u3040-\u309f\u30a0-\u30ff]", masked))
    han = len(re.findall(r"[\u4e00-\u9fff]", masked))
    latin = len(re.findall(r"[A-Za-z]", masked))
    total = max(hangul + kana + han + latin, 1)

    if override == "zh":
        trad = sum(1 for c in masked if c in TRAD_DISCRIMINATORS)
        simp = sum(1 for c in masked if c in SIMP_DISCRIMINATORS)
        return "zh-tw" if trad > simp else "zh-cn"

    if hangul >= 5 and hangul >= kana and (hangul / total >= 0.12 or hangul > han):
        return "ko"
    if kana >= 4:
        return "ja"
    if han >= 6 and (han / total >= 0.15 or han > latin):
        trad = sum(1 for c in masked if c in TRAD_DISCRIMINATORS)
        simp = sum(1 for c in masked if c in SIMP_DISCRIMINATORS)
        return "zh-tw" if trad > simp else "zh-cn"
    return "en"


def detect_genre(text: str, override: str = "auto") -> str:
    if override != "auto":
        return override
    _, spans = mask_protected_spans(text, mask_quotes=False)
    # Academic signals
    acad_hits = len(re.findall(
        r"\b(?:Abstract|Related\s+Work|Methodology|Experimental\s+Setup|et\s+al\.|doi:|arXiv:)\b|"
        r"(?:초록|선행연구|연구\s*방법|참고문헌|摘要|引言|参考文献|參考文獻|先行研究)",
        text, re.IGNORECASE,
    ))
    citations = len(re.findall(r"\[\d+\]|\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s*(?:19|20)\d{2}\)", text))
    if acad_hits >= 2 or (acad_hits >= 1 and citations >= 2):
        return "academic"
    # Tech signals
    tech_hits = len(re.findall(
        r"\b(?:README|API|endpoint|kubectl|docker|HTTP|JSON|YAML|CLI|SDK|PR\s*#|commit|deploy(?:ment)?|postmortem)\b",
        text,
    ))
    if spans["fenced_code"] >= 1 or spans["inline_code"] >= 3 or tech_hits >= 3:
        return "tech"
    # SNS signals
    non_ws = len(text.strip())
    hashtags = len(re.findall(r"(?:^|\s)#[^\s#]{2,}", text))
    if non_ws < 550 and (hashtags >= 2 or "🧵" in text or re.search(r"(?m)^\s*1/\d+", text)):
        return "sns"
    # Business signals
    biz_hits = len(re.findall(
        r"검토\s*요청|회신\s*부탁|마감일|기획안|보고서|담당자|\b(?:KPI|ROI|OKR|BLUF|Action\s+Items?|Best\s+regards)\b|お世話になっております|汇报",
        text, re.IGNORECASE,
    ))
    if biz_hits >= 2:
        return "business"
    # Fiction signals
    dialogue_lines = len(re.findall(r'(?m)^\s*["“「『]', text))
    if dialogue_lines >= 3:
        return "fiction"
    return "blog"


# ---------------------------------------------------------------------------
# Sentence & Rhythm Metrics (Reporting Only — Never Force Choppy Inversion!)
# ---------------------------------------------------------------------------

def split_sentences(text: str, lang: str) -> list[str]:
    masked, _ = mask_protected_spans(text, mask_quotes=False)
    # Remove markdown headings/list markers for prose rhythm measurement
    lines = []
    for ln in masked.splitlines():
        s = ln.strip()
        if not s or s.startswith("#") or re.match(r"^[-*+]\s*$", s):
            continue
        s = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", s)
        lines.append(s)
    joined = "\n".join(lines)
    if lang in ("ja", "zh-cn", "zh-tw"):
        raw = re.split(r"(?<=[。！？!?])\s*|\n+", joined)
    else:
        raw = re.split(r"(?<=[.!?。！？])\s+|\n+", joined)
    return [s.strip() for s in raw if len(s.strip()) >= 3]


def compute_rhythm_stats(text: str, lang: str) -> dict[str, Any]:
    sents = split_sentences(text, lang)
    if not sents:
        return {
            "sentence_count": 0,
            "unit": "words" if lang == "en" else "chars",
            "avg_length": 0.0,
            "std_length": 0.0,
            "cv": 0.0,
            "max_length": 0,
            "uniform_runs": 0,
        }
    if lang == "en":
        lengths = [len(re.findall(r"\b\w+(?:'\w+)?\b", s)) for s in sents]
        lengths = [x for x in lengths if x > 0]
        unit = "words"
    else:
        lengths = [len(re.sub(r"\s+", "", s)) for s in sents]
        lengths = [x for x in lengths if x > 0]
        unit = "chars"

    if not lengths:
        return {
            "sentence_count": 0,
            "unit": unit,
            "avg_length": 0.0,
            "std_length": 0.0,
            "cv": 0.0,
            "max_length": 0,
            "uniform_runs": 0,
        }

    mean = sum(lengths) / len(lengths)
    var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std = math.sqrt(var)
    cv = std / mean if mean > 0 else 0.0

    # Count 3+ consecutive sentences within narrow band (5 words EN or 10 chars CJK)
    tol = 5 if lang == "en" else 10
    uniform_runs = 0
    for i in range(len(lengths) - 2):
        window = lengths[i : i + 3]
        if max(window) - min(window) <= tol and min(window) >= (10 if lang == "en" else 20):
            uniform_runs += 1

    return {
        "sentence_count": len(lengths),
        "unit": unit,
        "avg_length": round(mean, 2),
        "std_length": round(std, 2),
        "cv": round(cv, 3),
        "max_length": max(lengths),
        "uniform_runs": uniform_runs,
    }


# ---------------------------------------------------------------------------
# Scanning Engine
# ---------------------------------------------------------------------------

def _line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _sentence_window(text: str, start: int, end: int) -> str:
    left = max(
        text.rfind("\n", 0, start),
        text.rfind(".", 0, start),
        text.rfind("!", 0, start),
        text.rfind("?", 0, start),
        text.rfind("。", 0, start),
        text.rfind("！", 0, start),
        text.rfind("？", 0, start),
    )
    lo = max(0, left + 1) if left != -1 else max(0, start - 80)
    right_candidates = [
        p for p in (
            text.find("\n", end),
            text.find(".", end),
            text.find("!", end),
            text.find("?", end),
            text.find("。", end),
            text.find("！", end),
            text.find("？", end),
        ) if p != -1
    ]
    hi = min(right_candidates) + 1 if right_candidates else min(len(text), end + 80)
    return text[lo:hi].strip()


def _snippet(text: str, start: int, end: int, radius: int = 28) -> str:
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    s = text[lo:hi].replace("\n", " ").strip()
    return ("..." if lo > 0 else "") + s + ("..." if hi < len(text) else "")


def _rule_applies(rule: PatternRule, lang: str, genre: str) -> bool:
    if rule.lang == "all":
        lang_ok = True
    elif rule.lang == "zh":
        lang_ok = lang in ("zh-cn", "zh-tw")
    else:
        lang_ok = rule.lang == lang
    if not lang_ok:
        return False
    if rule.skip_genres and genre in rule.skip_genres:
        return False
    if rule.only_genres and genre not in rule.only_genres:
        return False
    return True


def scan_text(
    text: str,
    genre: str = "auto",
    lang: str = "auto",
    strict: bool = False,
) -> dict[str, Any]:
    detected_lang = detect_language(text, lang)
    detected_genre = detect_genre(text, genre)
    masked_prose, protected_counts = mask_protected_spans(text, mask_quotes=True)
    unicode_info = detect_invisible_unicode(text)
    rhythm = compute_rhythm_stats(text, detected_lang)

    hits: list[Hit] = []
    info_notes: list[Hit] = []
    rule_hit_counts: Counter[str] = Counter()

    # 1. Invisible Unicode family
    if unicode_info["total"] > 0:
        codes_str = ", ".join(f"{k}×{v}" for k, v in unicode_info["counts"].items())
        first_line = unicode_info["positions"][0]["line"] if unicode_info["positions"] else 1
        hits.append(Hit(
            rule_id="UNI-01",
            family="invisible_unicode",
            tier="A",
            label="Invisible Unicode artifacts (U+202F / zero-width chars)",
            match=codes_str,
            line=first_line,
            snippet=f"Detected {unicode_info['total']} invisible character(s): {codes_str}",
            weight=min(20, 8 + unicode_info["total"] * 3),
            suggestion="Run `slop_engine.py clean-unicode` before editing.",
        ))

    # 2. Pattern rules
    for rule in RULES:
        if not _rule_applies(rule, detected_lang, detected_genre):
            continue
        for m in re.finditer(rule.pattern, masked_prose, rule.flags):
            raw_match = m.group(0)
            trimmed = raw_match.lstrip(" \t\r\n.?!。！？")
            lead_offset = len(raw_match) - len(trimmed)
            eff_start = m.start() + lead_offset
            eff_end = m.end()
            win = _sentence_window(masked_prose, eff_start, eff_end)
            if rule.exclude and re.search(rule.exclude, win, rule.flags):
                continue
            hit = Hit(
                rule_id=rule.rule_id,
                family=rule.family,
                tier=rule.tier,
                label=rule.label,
                match=trimmed.strip(),
                line=_line_number_at(text, eff_start),
                snippet=_snippet(text, eff_start, eff_end),
                weight=rule.weight,
                directional_only=rule.directional_only,
                informational_only=rule.informational_only,
                suggestion=rule.suggestion,
            )
            if rule.informational_only:
                if rule_hit_counts[rule.rule_id] < 3:
                    info_notes.append(hit)
                rule_hit_counts[rule.rule_id] += 1
            else:
                hits.append(hit)
                rule_hit_counts[rule.rule_id] += 1

    # 3. Directional / Model-Divergent Fingerprints (NEVER cause high-risk alone!)
    non_ws_chars = len(re.sub(r"\s+", "", masked_prose))
    word_count = len(re.findall(r"\b\w+(?:'\w+)?\b", masked_prose))

    # 3a. Em-dash density (model-divergent: high in Claude, low in GPT; Wikipedia Historical 2026)
    em_dashes = list(re.finditer(r"——|—|\s--\s", masked_prose))
    em_threshold = max(2, math.ceil(word_count / 300)) if detected_lang == "en" else max(2, math.ceil(non_ws_chars / 500))
    if len(em_dashes) > em_threshold:
        hits.append(Hit(
            rule_id="FP-EMDASH",
            family="model_fingerprint",
            tier="F",
            label="Elevated em-dash density (directional model fingerprint only)",
            match=f"{len(em_dashes)} em-dashes (threshold >{em_threshold})",
            line=_line_number_at(text, em_dashes[0].start()),
            snippet=_snippet(text, em_dashes[0].start(), em_dashes[0].end()),
            weight=4,
            directional_only=True,
            suggestion="Model-divergent hint only (high in Claude, low in GPT); tighten theatrical pauses if paired with other tells.",
        ))

    # 3b. Korean connective-ending comma rate (C-11 — directional ONLY due to 53.6% Pebblous false-positive finding!)
    if detected_lang == "ko" and rhythm["sentence_count"] >= 4:
        conn_commas = list(re.finditer(r"(?:며|고|지만|는데|므로|면서|으나|지만|하며|되고|하고),\s", masked_prose))
        rate = len(conn_commas) / max(rhythm["sentence_count"], 1)
        if len(conn_commas) >= 3 and rate >= 0.55:
            hits.append(Hit(
                rule_id="FP-KO-C11",
                family="model_fingerprint",
                tier="F",
                label="연결어미 뒤 쉼표 밀도 높음 (C-11, 단일 지표 오탐 주의)",
                match=f"{len(conn_commas)}회 ({rate:.2f}/문장)",
                line=_line_number_at(text, conn_commas[0].start()),
                snippet=_snippet(text, conn_commas[0].start(), conn_commas[0].end()),
                weight=3,
                directional_only=True,
                suggestion="개인 쉼표 습관일 수 있어 단독으로 AI 판정 금지; 다른 계열 신호와 함께 나타날 때만 정리하세요.",
            ))

    # 3c. Japanese long-sentence reading-load check (meiseki >90 chars)
    if detected_lang == "ja":
        for sent in split_sentences(text, "ja"):
            clean_len = len(re.sub(r"\s+", "", sent))
            if clean_len > 90 and sent.count("、") >= 4:
                hits.append(Hit(
                    rule_id="JA-B-02",
                    family="translationese_syntax",
                    tier="B",
                    label="長文・読点過多 (>90字かつ読点4個以上)",
                    match=f"{clean_len}字 / 読点{sent.count('、')}個",
                    line=1,
                    snippet=sent[:55] + "...",
                    weight=8,
                    suggestion="2文に分割し、主語と述語の距離を近づけてください。",
                ))
                break

    # 4. Rhythm uniformity family (strictly gated on longer passages to prevent false positives on short natural prose)
    min_avg = 14 if detected_lang == "en" else 30
    if (
        rhythm["sentence_count"] >= 8
        and rhythm["avg_length"] >= min_avg
        and rhythm["cv"] < 0.18
        and rhythm["uniform_runs"] >= 3
    ):
        hits.append(Hit(
            rule_id="RHY-01",
            family="rhythm_uniformity",
            tier="C",
            label="Metronomic sentence-length uniformity",
            match=f"CV={rhythm['cv']} across {rhythm['sentence_count']} sentences ({rhythm['uniform_runs']} uniform runs)",
            line=1,
            snippet=f"Avg {rhythm['avg_length']} {rhythm['unit']}, CV={rhythm['cv']}",
            weight=8,
            suggestion="Vary sentence openings/length naturally where content warrants it (never force choppy fragments).",
        ))

    # 5. Aggregate independent families & calibrated score (cap per-rule contribution so 1 word doesn't skew!)
    active_families: list[str] = []
    per_rule_capped: Counter[str] = Counter()
    score_raw = 0
    non_directional_count = 0

    for h in hits:
        if h.informational_only:
            continue
        if not h.directional_only:
            non_directional_count += 1
            if h.family not in active_families:
                active_families.append(h.family)
        # Diminishing returns after 2 hits of the same rule
        seen = per_rule_capped[h.rule_id]
        if seen == 0:
            score_raw += h.weight
        elif seen == 1:
            score_raw += max(1, h.weight // 2)
        elif seen == 2:
            score_raw += max(1, h.weight // 4)
        per_rule_capped[h.rule_id] += 1

    score = min(100, score_raw)
    fam_count = len(active_families)

    # Risk level strictly enforces the 2+ independent signal family rule!
    if fam_count >= 2 and score >= 40:
        risk_level = "high"
    elif fam_count >= 2 or (fam_count == 1 and score >= 16 and non_directional_count >= 2):
        risk_level = "medium"
    else:
        risk_level = "low"

    # Route hint per SKILL.md
    if len(text) > 10000:
        route_hint = "heavy"
    elif strict and fam_count >= 1:
        route_hint = "heavy"
    elif fam_count >= 3 or (fam_count >= 2 and score >= 45):
        route_hint = "heavy"
    elif fam_count >= 2 or (fam_count == 1 and non_directional_count >= 2 and score >= 16):
        route_hint = "standard"
    else:
        route_hint = "light"

    return {
        "language": detected_lang,
        "genre": detected_genre,
        "char_count": len(text),
        "word_count": word_count,
        "protected_spans": protected_counts,
        "invisible_unicode": unicode_info,
        "rhythm": rhythm,
        "active_families": active_families,
        "active_family_count": fam_count,
        "hit_count": len(hits),
        "non_directional_hit_count": non_directional_count,
        "score": score,
        "risk_level": risk_level,
        "route_hint": route_hint,
        "hits": [h.to_dict() for h in hits],
        "informational_notes": [n.to_dict() for n in info_notes],
    }


# ---------------------------------------------------------------------------
# Deterministic Verification Gates (`verify`)
# ---------------------------------------------------------------------------

def _extract_protected_tokens(text: str) -> dict[str, Counter[str]]:
    """Extract numbers, URLs, fenced code blocks, inline code, and direct quotes."""
    # Fenced code blocks
    fenced = [m.group(0).strip() for m in re.finditer(
        r"(?m)^[ \t]*(?:```|~~~)[^\n]*\r?\n.*?\r?\n[ \t]*(?:```|~~~)", text, re.DOTALL
    )]
    no_fenced = re.sub(
        r"(?m)^[ \t]*(?:```|~~~)[^\n]*\r?\n.*?\r?\n[ \t]*(?:```|~~~)", " ", text, flags=re.DOTALL
    )
    # Inline code
    inline = [m.group(0) for m in re.finditer(r"`[^`\n]+`", no_fenced)]
    no_code = re.sub(r"`[^`\n]+`", " ", no_fenced)
    # URLs
    urls = [m.group(0).rstrip(".,);") for m in re.finditer(r"(?:https?|file)://[^\s)>\]]+", no_code)]
    no_urls = re.sub(r"(?:https?|file)://[^\s)>\]]+", " ", no_code)
    # Direct quotes (>=4 chars inside quotes)
    quotes = [
        m.group(0) for m in re.finditer(
            r'“[^”\n]{4,400}”|「[^」\n]{4,400}」|『[^』\n]{4,400}』|"[^"\n]{4,400}"', no_urls
        )
    ]
    # Numbers (exclude markdown ordered list prefixes like "1. " at line start)
    no_list_nums = re.sub(r"(?m)^\s*\d+\.\s+", " ", no_urls)
    raw_nums = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?%?", no_list_nums)
    norm_nums = [n.replace(",", "") for n in raw_nums]

    return {
        "numbers": Counter(norm_nums),
        "urls": Counter(urls),
        "fenced_code": Counter(fenced),
        "inline_code": Counter(inline),
        "quotes": Counter(quotes),
    }


def _count_negations(text: str, lang: str) -> int:
    masked, _ = mask_protected_spans(text, mask_quotes=True)
    if lang == "ko":
        pat = (
            r"않(?:다|아|았|으|는|을|지|고|며|면|습|니|았습|을지)?|"
            r"없(?:다|어|었|으|는|을|지|고|며|면|습|니|이)?|"
            r"못(?:하|했|할|한|해|함|합|되|됐|될|된|\s)|"
            r"아니(?:다|라|면|야|었|었습|ㅂ니다|었어|었는|고|며|므로)?|"
            r"(?<![가-힣])안(?:\s|[가-힣]{1,3}(?:다|고|아|어|았|었|는|을|면|지))|"
            r"(?<![가-힣])(?:불가|미지원|금지)(?![가-힣])"
        )
        return len(re.findall(pat, masked))
    if lang == "en":
        pat = (
            r"\b(?:not|never|no|none|neither|nor|without|cannot|can't|won't|don't|"
            r"doesn't|didn't|isn't|aren't|wasn't|weren't|shouldn't|wouldn't|couldn't|"
            r"haven't|hasn't|hadn't|mustn't|fail(?:s|ed)?\s+to|unable\s+to)\b"
        )
        return len(re.findall(pat, masked, re.IGNORECASE))
    if lang == "ja":
        pat = r"ではない|じゃない|ませんでした|ません|なかった|できない|しない|ない|ずに|せず|不可|禁止"
        return len(re.findall(pat, masked))
    # zh-cn / zh-tw
    pat = r"不是|不能|不会|不會|没有|沒有|无法|無法|不要|不必|不得|并非|並非|从未|從未|未曾|不|没|沒|无|無|非|未|别|別|禁止"
    return len(re.findall(pat, masked))


def _count_epistemic(text: str, lang: str) -> tuple[int, int]:
    """Return (hedge_count, strong_certainty_count)."""
    masked, _ = mask_protected_spans(text, mask_quotes=True)
    if lang == "ko":
        hedges = len(re.findall(r"가능(?:성|하|한|할)|추정|일\s*수\s*있|수\s*있(?:다|습니다|어)|아마|보인다|보입니다|경향|일부|약\s*\d", masked))
        certain = len(re.findall(r"반드시|확실히|확실하|무조건|틀림없이|항상|절대(?:로|적)?|분명히", masked))
    elif lang == "en":
        hedges = len(re.findall(r"\b(?:may|might|could|likely|possibly|probably|appears?\s+to|suggests?|approximately|roughly|often|some)\b", masked, re.IGNORECASE))
        certain = len(re.findall(r"\b(?:must|certainly|definitely|always|undoubtedly|unquestionably|proves?|guaranteed)\b", masked, re.IGNORECASE))
    elif lang == "ja":
        hedges = len(re.findall(r"かもしれ|可能性|思われ|傾向|場合|ことがある|おそらく|約", masked))
        certain = len(re.findall(r"必ず|確実|絶対|常に|間違いなく", masked))
    else:
        hedges = len(re.findall(r"可能|或许|或許|大约|大約|似乎|倾向|傾向|也许|也許|有时|有時|部分", masked))
        certain = len(re.findall(r"必然|一定|肯定|绝对|絕對|始终|始終|毫无悬念|毫無懸念", masked))
    return hedges, certain


def _check_academic_register(text: str, lang: str) -> list[str]:
    """Return list of scholarly register violations in academic mode."""
    masked, _ = mask_protected_spans(text, mask_quotes=True)
    issues: list[str] = []

    colloquial_patterns = {
        "ko": r"(?<![가-힣])(?:솔직히|솔까|진짜(?:로)?(?=\s)|대박|완전(?=\s)|엄청(?=\s)|꿀팁|레전드|갓생)|ㅋㅋ+|ㅎㅎ+|ㅠㅠ+|ㅜㅜ+",
        "en": r"\b(?:honestly|super\s+cool|awesome|crazy|totally|kinda|gonna|wanna|tbh|btw|lol|omg|huge\s+win)\b",
        "ja": r"マジで?|やばい|ヤバい|ぶっちゃけ|めっちゃ|てか|ってか|ｗｗ+|すげー",
        "zh-cn": r"说白了|老实说|其实吧|说穿了|超级|简直|太牛了|绝了|哈哈+|讲真",
        "zh-tw": r"說白了|老實說|其實吧|說穿了|超級|簡直|太牛了|絕了|哈哈+|講真",
    }
    pat = colloquial_patterns.get(lang, colloquial_patterns["en"])
    found = re.findall(pat, masked, re.IGNORECASE)
    if found:
        uniq = sorted(set(found))
        issues.append(f"Colloquial/slang expression(s) in academic prose: {', '.join(uniq[:8])}")

    # Em-dash cap: <= 1 per paragraph in academic genre
    paragraphs = [p.strip() for p in re.split(r"\r?\n\s*\r?\n", masked) if p.strip()]
    for idx, para in enumerate(paragraphs, start=1):
        dashes = re.findall(r"——|—", para)
        if len(dashes) > 1:
            issues.append(f"Paragraph {idx} has {len(dashes)} em-dashes (academic cap: <=1 per paragraph)")

    return issues


def verify_edit(
    before: str,
    after: str,
    genre: str = "auto",
    lang: str = "auto",
    mode: str = "refactor",
) -> dict[str, Any]:
    detected_lang = detect_language(before, lang)
    detected_genre = detect_genre(before, genre)

    gates: dict[str, dict[str, Any]] = {}

    # Gate 1: Protected tokens preservation (numbers, URLs, code, quotes)
    b_tok = _extract_protected_tokens(before)
    a_tok = _extract_protected_tokens(after)
    missing: dict[str, list[str]] = {}
    for key in ("numbers", "urls", "fenced_code", "inline_code", "quotes"):
        diff = b_tok[key] - a_tok[key]
        if diff:
            missing[key] = list(diff.elements())
    added_nums = list((a_tok["numbers"] - b_tok["numbers"]).elements())

    if missing:
        gates["protected_spans"] = {
            "status": "FAIL",
            "missing": missing,
            "added_numbers": added_nums,
            "message": "Protected factual/structural elements were dropped or altered.",
        }
    elif added_nums:
        gates["protected_spans"] = {
            "status": "WARN",
            "missing": {},
            "added_numbers": added_nums,
            "message": f"New numeric token(s) appeared in edited text ({', '.join(added_nums[:8])}) — verify no fabricated figures.",
        }
    else:
        gates["protected_spans"] = {
            "status": "PASS",
            "missing": {},
            "added_numbers": [],
            "message": "All numbers, URLs, code blocks, and direct quotes preserved.",
        }

    # Gate 2: Change rate (SequenceMatcher)
    b_norm = before.strip()
    a_norm = after.strip()
    similarity = difflib.SequenceMatcher(None, b_norm, a_norm).ratio() if (b_norm or a_norm) else 1.0
    change_rate = round(1.0 - similarity, 4)
    if mode == "refactor":
        if change_rate > 0.50:
            cr_status = "FAIL"
            cr_msg = f"Change rate {change_rate:.1%} exceeds 50% refactor cap — rollback or switch to recreate mode."
        elif change_rate > 0.30:
            cr_status = "WARN"
            cr_msg = f"Change rate {change_rate:.1%} exceeds 30% surgical threshold — review for over-editing."
        else:
            cr_status = "PASS"
            cr_msg = f"Change rate {change_rate:.1%} is within surgical refactor band (<=30%)."
    else:
        cr_status = "PASS"
        cr_msg = f"Change rate {change_rate:.1%} (recreate mode — restructuring permitted)."

    gates["change_rate"] = {
        "status": cr_status,
        "change_rate": change_rate,
        "similarity": round(similarity, 4),
        "mode": mode,
        "message": cr_msg,
    }

    # Gate 3: Length floor & bloat guard (Note.com 70% floor)
    length_ratio = round(len(a_norm) / max(len(b_norm), 1), 4)
    if length_ratio < 0.70:
        lr_status = "WARN"
        lr_msg = f"Length ratio {length_ratio:.1%} fell below 70% floor — check for content collapse."
    elif length_ratio > 1.35:
        lr_status = "WARN"
        lr_msg = f"Length ratio {length_ratio:.1%} expanded >135% — check for AI padding/bloat."
    else:
        lr_status = "PASS"
        lr_msg = f"Length ratio {length_ratio:.1%} is within healthy bounds (70%–135%)."
    gates["length_ratio"] = {
        "status": lr_status,
        "before_chars": len(b_norm),
        "after_chars": len(a_norm),
        "length_ratio": length_ratio,
        "message": lr_msg,
    }

    # Gate 4: Negation parity check (meiseki insight)
    b_neg = _count_negations(before, detected_lang)
    a_neg = _count_negations(after, detected_lang)
    neg_delta = a_neg - b_neg
    if neg_delta % 2 != 0:
        neg_status = "WARN"
        neg_msg = (
            f"Odd negation delta ({b_neg} -> {a_neg}, delta {neg_delta:+d}) — "
            "verify polarity was not accidentally inverted (acceptable if a 'Not X, but Y' contrast was cleanly flattened)."
        )
    else:
        neg_status = "PASS"
        if neg_delta < 0:
            neg_msg = f"Even negation reduction ({b_neg} -> {a_neg}, delta {neg_delta:+d}) — consistent with double-negative collapse."
        else:
            neg_msg = f"Negation parity preserved ({b_neg} -> {a_neg})."
    gates["negation_parity"] = {
        "status": neg_status,
        "before_negations": b_neg,
        "after_negations": a_neg,
        "delta": neg_delta,
        "message": neg_msg,
    }

    # Gate 5: Epistemic modality / hedge conservation
    b_hedge, b_cert = _count_epistemic(before, detected_lang)
    a_hedge, a_cert = _count_epistemic(after, detected_lang)
    if a_hedge < b_hedge and a_cert > b_cert:
        ep_status = "WARN"
        ep_msg = (
            f"Epistemic shift detected: hedges fell ({b_hedge} -> {a_hedge}) while certainty rose ({b_cert} -> {a_cert}) — "
            "verify claims were not over-strengthened."
        )
    else:
        ep_status = "PASS"
        ep_msg = f"Epistemic modality balanced (hedges {b_hedge}->{a_hedge}, certainty {b_cert}->{a_cert})."
    gates["epistemic_hedges"] = {
        "status": ep_status,
        "before_hedges": b_hedge,
        "after_hedges": a_hedge,
        "before_certainty": b_cert,
        "after_certainty": a_cert,
        "message": ep_msg,
    }

    # Gate 6: P1 Lexical injection regression guard (im-not-ai restore insight)
    b_scan = scan_text(before, genre=detected_genre, lang=detected_lang)
    a_scan = scan_text(after, genre=detected_genre, lang=detected_lang)
    b_p1 = Counter(h["rule_id"] for h in b_scan["hits"] if h["tier"] == "P1")
    a_p1 = Counter(h["rule_id"] for h in a_scan["hits"] if h["tier"] == "P1")
    injected: list[dict[str, Any]] = []
    for rid, a_cnt in a_p1.items():
        if a_cnt > b_p1.get(rid, 0):
            matching_hits = [h for h in a_scan["hits"] if h["rule_id"] == rid]
            injected.append({
                "rule_id": rid,
                "label": matching_hits[0]["label"],
                "before_count": b_p1.get(rid, 0),
                "after_count": a_cnt,
                "matches": [h["match"] for h in matching_hits],
            })
    if injected:
        gates["lexical_regression"] = {
            "status": "FAIL",
            "injected": injected,
            "message": f"Edited text newly introduced {len(injected)} P1 AI lexical trap(s) absent from original.",
        }
    else:
        gates["lexical_regression"] = {
            "status": "PASS",
            "injected": [],
            "message": "Zero new P1 AI lexical traps introduced.",
        }

    # Gate 7: Academic register guard (aigc-reduce insight)
    if detected_genre == "academic":
        acad_issues = _check_academic_register(after, detected_lang)
        if acad_issues:
            gates["academic_register"] = {
                "status": "FAIL",
                "issues": acad_issues,
                "message": "Academic register violation detected (降重 ≠ 口语化).",
            }
        else:
            gates["academic_register"] = {
                "status": "PASS",
                "issues": [],
                "message": "Formal scholarly register preserved.",
            }
    else:
        gates["academic_register"] = {
            "status": "PASS",
            "issues": [],
            "message": f"Not applicable for genre '{detected_genre}'.",
        }

    # Overall status
    statuses = [g["status"] for g in gates.values()]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "WARN" in statuses:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall": overall,
        "language": detected_lang,
        "genre": detected_genre,
        "mode": mode,
        "before_score": b_scan["score"],
        "after_score": a_scan["score"],
        "before_families": b_scan["active_families"],
        "after_families": a_scan["active_families"],
        "gates": gates,
    }


# ---------------------------------------------------------------------------
# Formatters (Readable Markdown + Diff Report)
# ---------------------------------------------------------------------------

def format_scan_markdown(res: dict[str, Any]) -> str:
    lines = [
        "# Anti-Slop Pre-Scan Report",
        "",
        f"- **Language:** `{res['language']}` | **Genre:** `{res['genre']}` | **Route Hint:** `{res['route_hint']}` | **Risk Level:** `{res['risk_level']}`",
        f"- **Score:** `{res['score']}/100` | **Independent Signal Families:** `{res['active_family_count']}` ({', '.join(res['active_families']) or 'none'})",
        f"- **Length:** `{res['char_count']}` chars, `{res['word_count']}` words | **Sentences:** `{res['rhythm']['sentence_count']}` (avg `{res['rhythm']['avg_length']}` {res['rhythm']['unit']}, CV `{res['rhythm']['cv']}`)",
        f"- **Invisible Unicode Artifacts:** `{res['invisible_unicode']['total']}`",
        "",
    ]
    if res["hits"]:
        lines.append("## Detected Signals")
        lines.append("")
        lines.append("| # | Rule | Family | Tier | Line | Match | Guidance |")
        lines.append("|---|---|---|---|---:|---|---|")
        for idx, h in enumerate(res["hits"], start=1):
            match_esc = h["match"].replace("|", "\\|").replace("\n", " ")
            sug_esc = h["suggestion"].replace("|", "\\|")
            dir_tag = " *(directional)*" if h["directional_only"] else ""
            lines.append(f"| {idx} | `{h['rule_id']}` | `{h['family']}`{dir_tag} | `{h['tier']}` | {h['line']} | `{match_esc}` | {sug_esc} |")
    else:
        lines.append("## Detected Signals")
        lines.append("")
        lines.append("No deterministic slop signals detected. Text appears clean on surface & structural heuristics.")

    if res["informational_notes"]:
        lines.append("")
        lines.append("## Informational Notes (X-Tier — Do Not Auto-Edit)")
        for n in res["informational_notes"]:
            lines.append(f"- `{n['rule_id']}` (L{n['line']} `{n['match']}`): {n['suggestion']}")

    return "\n".join(lines) + "\n"


def format_verify_markdown(res: dict[str, Any]) -> str:
    lines = [
        f"# Anti-Slop Verification Report — `{res['overall']}`",
        "",
        f"- **Language:** `{res['language']}` | **Genre:** `{res['genre']}` | **Mode:** `{res['mode']}`",
        f"- **Slop Score:** `{res['before_score']}` -> `{res['after_score']}` | **Active Families:** `{len(res['before_families'])}` -> `{len(res['after_families'])}`",
        "",
        "| Gate | Status | Details |",
        "|---|---|---|",
    ]
    for name, g in res["gates"].items():
        msg = g["message"].replace("|", "\\|")
        lines.append(f"| `{name}` | **`{g['status']}`** | {msg} |")
        if name == "protected_spans" and g.get("missing"):
            lines.append(f"| ↳ missing | — | `{json.dumps(g['missing'], ensure_ascii=False)}` |")
        if name == "lexical_regression" and g.get("injected"):
            injected_str = "; ".join(f"{x['rule_id']}: {x['matches']}" for x in g["injected"])
            lines.append(f"| ↳ injected | — | `{injected_str}` |")
        if name == "academic_register" and g.get("issues"):
            lines.append(f"| ↳ issues | — | {'; '.join(g['issues'])} |")
    return "\n".join(lines) + "\n"


def generate_diff_report(
    before: str,
    after: str,
    genre: str = "auto",
    lang: str = "auto",
    mode: str = "refactor",
) -> str:
    b_scan = scan_text(before, genre=genre, lang=lang)
    a_scan = scan_text(after, genre=b_scan["genre"], lang=b_scan["language"])
    ver = verify_edit(before, after, genre=b_scan["genre"], lang=b_scan["language"], mode=mode)

    lines = [
        f"# Anti-Slop Diff & Metrics Report (`{ver['overall']}`)",
        "",
        "## 1. Before vs. After Metrics",
        "",
        "| Metric | Before | After |",
        "|---|---:|---:|",
        f"| Language / Genre | `{b_scan['language']}` / `{b_scan['genre']}` | `{a_scan['language']}` / `{a_scan['genre']}` |",
        f"| Characters | {b_scan['char_count']} | {a_scan['char_count']} ({ver['gates']['length_ratio']['length_ratio']:.1%}) |",
        f"| Sentences (avg / CV) | {b_scan['rhythm']['sentence_count']} ({b_scan['rhythm']['avg_length']} / {b_scan['rhythm']['cv']}) | {a_scan['rhythm']['sentence_count']} ({a_scan['rhythm']['avg_length']} / {a_scan['rhythm']['cv']}) |",
        f"| Invisible Unicode | {b_scan['invisible_unicode']['total']} | {a_scan['invisible_unicode']['total']} |",
        f"| Active Signal Families | {b_scan['active_family_count']} ({', '.join(b_scan['active_families']) or 'none'}) | {a_scan['active_family_count']} ({', '.join(a_scan['active_families']) or 'none'}) |",
        f"| Slop Score / Risk | {b_scan['score']} (`{b_scan['risk_level']}`) | {a_scan['score']} (`{a_scan['risk_level']}`) |",
        f"| Route Hint | `{b_scan['route_hint']}` | `{a_scan['route_hint']}` |",
        f"| Character Change Rate | — | {ver['gates']['change_rate']['change_rate']:.1%} |",
        "",
        "## 2. Deterministic Verification Gates",
        "",
        "| Gate | Status | Details |",
        "|---|---|---|",
    ]
    for name, g in ver["gates"].items():
        lines.append(f"| `{name}` | **`{g['status']}`** | {g['message'].replace('|', chr(92) + '|')} |")

    lines.extend(["", "## 3. Numbered Revisions", ""])
    b_lines = before.splitlines()
    a_lines = after.splitlines()
    sm = difflib.SequenceMatcher(None, b_lines, a_lines)
    rev_idx = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        rev_idx += 1
        lines.append(f"### [{rev_idx}] `{tag}` (L{i1 + 1}–L{max(i1 + 1, i2)})")
        for ln in b_lines[i1:i2]:
            lines.append(f"- **Before:** {ln}")
        for ln in a_lines[j1:j2]:
            lines.append(f"+ **After:** {ln}")
        lines.append("")

    if rev_idx == 0:
        lines.append("No textual changes detected.")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _read_input(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    return Path(path_arg).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slop_engine.py",
        description="4-Language Anti-Slop Scanner, Unicode Scrubber, Verifier, and Diff Reporter.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scan
    p_scan = sub.add_parser("scan", help="Scan text for invisible Unicode & multi-family AI slop.")
    p_scan.add_argument("input", help="Path to input file, or '-' for stdin.")
    p_scan.add_argument("--genre", choices=VALID_GENRES, default="auto")
    p_scan.add_argument("--lang", choices=VALID_LANGS, default="auto")
    p_scan.add_argument("--strict", action="store_true", help="Escalate any active slop family to heavy route.")
    p_scan.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")

    # clean-unicode
    p_clean = sub.add_parser("clean-unicode", help="Scrub invisible Unicode artifacts outside code blocks.")
    p_clean.add_argument("input", help="Path to input file, or '-' for stdin.")
    p_clean.add_argument("--out", help="Optional output file path (defaults to stdout).")
    p_clean.add_argument("--json", action="store_true", help="Emit cleanup summary as JSON (when --out is set, writes cleaned text to --out and JSON to stdout).")

    # verify
    p_ver = sub.add_parser("verify", help="Verify edited text against original using deterministic gates.")
    p_ver.add_argument("--before", required=True, help="Path to original text file.")
    p_ver.add_argument("--after", required=True, help="Path to edited text file.")
    p_ver.add_argument("--genre", choices=VALID_GENRES, default="auto")
    p_ver.add_argument("--lang", choices=VALID_LANGS, default="auto")
    p_ver.add_argument("--mode", choices=("refactor", "recreate"), default="refactor")
    p_ver.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")

    # diff-report
    p_diff = sub.add_parser("diff-report", help="Generate Markdown before/after diff and metrics report.")
    p_diff.add_argument("--before", required=True, help="Path to original text file.")
    p_diff.add_argument("--after", required=True, help="Path to edited text file.")
    p_diff.add_argument("--genre", choices=VALID_GENRES, default="auto")
    p_diff.add_argument("--lang", choices=VALID_LANGS, default="auto")
    p_diff.add_argument("--mode", choices=("refactor", "recreate"), default="refactor")
    p_diff.add_argument("--out", help="Optional output file path (defaults to stdout).")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        text = _read_input(args.input)
        res = scan_text(text, genre=args.genre, lang=args.lang, strict=args.strict)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(format_scan_markdown(res))
        return 0

    if args.command == "clean-unicode":
        text = _read_input(args.input)
        cleaned, summary = clean_invisible_unicode(text)
        if args.out:
            Path(args.out).write_text(cleaned, encoding="utf-8")
            if args.json:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print(
                    f"Cleaned {summary['total_cleaned']} invisible Unicode character(s) -> {args.out} "
                    f"({summary['cleaned_by_code']})"
                )
        else:
            if args.json:
                payload = dict(summary)
                payload["cleaned_text"] = cleaned
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                sys.stdout.write(cleaned)
        return 0

    if args.command == "verify":
        before = _read_input(args.before)
        after = _read_input(args.after)
        res = verify_edit(before, after, genre=args.genre, lang=args.lang, mode=args.mode)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(format_verify_markdown(res))
        return 1 if res["overall"] == "FAIL" else 0

    if args.command == "diff-report":
        before = _read_input(args.before)
        after = _read_input(args.after)
        report = generate_diff_report(before, after, genre=args.genre, lang=args.lang, mode=args.mode)
        if args.out:
            Path(args.out).write_text(report, encoding="utf-8")
            print(f"Diff report written to {args.out}")
        else:
            sys.stdout.write(report)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
