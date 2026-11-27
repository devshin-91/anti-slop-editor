#!/usr/bin/env python3
"""Comprehensive unit & CLI test suite for slop_engine.py (4 languages + 7 verify gates)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import slop_engine as se


class TestLanguageAndGenreDetection(unittest.TestCase):
    def test_detect_languages(self) -> None:
        self.assertEqual(se.detect_language("한국어 문장을 자연스럽게 다듬어 보겠습니다."), "ko")
        self.assertEqual(se.detect_language("This release fixes a race condition in the worker pool."), "en")
        self.assertEqual(se.detect_language("この記事では、非同期処理の再送制御について説明します。"), "ja")
        self.assertEqual(se.detect_language("这篇文章讨论了分布式系统里的数据一致性与容错机制。"), "zh-cn")
        self.assertEqual(se.detect_language("這篇文章討論了分散式系統裡的資料一致性與容錯機制，並整理台灣工程團隊的實務經驗。"), "zh-tw")

    def test_detect_genres(self) -> None:
        acad = "Abstract\nIn this study, we evaluate latency (Kim et al., 2025) [1].\nMethodology\nSee [2]."
        self.assertEqual(se.detect_genre(acad), "academic")

        tech = "Deploy the service with `kubectl apply -f app.yaml`.\n```bash\ndocker compose up\n```"
        self.assertEqual(se.detect_genre(tech), "tech")

        biz = "안녕하세요, 3분기 기획안 검토 요청드립니다. 마감일은 금요일이며 담당자 회신 부탁드립니다."
        self.assertEqual(se.detect_genre(biz), "business")


class TestMultilingualSlopScanning(unittest.TestCase):
    def test_korean_heavy_slop_and_families(self) -> None:
        text = (
            "마케팅은 단순히 서비스를 알리는 일이 아니라 고객의 마음을 이해하는 일입니다.\n"
            "이 렌즈를 통해 팀의 잠재력을 잠금 해제하고 정서의 결을 살립니다.\n"
            "또한 검토를 진행하고 방향성과 고객 반응을 함께 봅니다.\n"
            "결론적으로 시사하는 바가 크며, 도움이 되셨길 바랍니다.\u202f"
        )
        res = se.scan_text(text, genre="blog")
        self.assertEqual(res["language"], "ko")
        self.assertIn("invisible_unicode", res["active_families"])
        self.assertIn("contrast_staging", res["active_families"])
        self.assertIn("lexical_traps", res["active_families"])
        self.assertIn("ai_boilerplate", res["active_families"])
        self.assertEqual(res["risk_level"], "high")
        self.assertEqual(res["route_hint"], "heavy")

    def test_english_slop_detection(self) -> None:
        text = (
            "Great question! Let's dive in.\n"
            "In today's fast-paced digital landscape, this tool is not just a helper, "
            "but a game-changer that serves as a testament to vibrant innovation, "
            "highlighting its commitment to seamless growth.\n"
            "That is the real win. I hope this helps!"
        )
        res = se.scan_text(text, genre="blog")
        self.assertEqual(res["language"], "en")
        self.assertGreaterEqual(res["active_family_count"], 4)
        self.assertEqual(res["risk_level"], "high")
        self.assertEqual(res["route_hint"], "heavy")

    def test_japanese_slop_detection(self) -> None:
        text = (
            "本記事では、この革命的な機能について解説します。\n"
            "単なる自動化ツールではなく、可能性を解き放つゲームチェンジャーと言えます。\n"
            "設定を忘れないとは言えませんし、以下の手順を実行します:\n"
            "- 確認することができます。\n"
            "いかがでしたでしょうか。お役に立てれば幸いです。"
        )
        res = se.scan_text(text, genre="blog")
        self.assertEqual(res["language"], "ja")
        rule_ids = {h["rule_id"] for h in res["hits"]}
        self.assertIn("JA-A-01", rule_ids)
        self.assertIn("JA-D-01", rule_ids)
        self.assertIn("JA-E-01", rule_ids)
        self.assertIn("JA-LEX-P1-01", rule_ids)
        self.assertEqual(res["route_hint"], "heavy")

    def test_chinese_simplified_universal_tells_and_x_tier_immunity(self) -> None:
        # Clean Chinese text containing ONLY X-tier debunked myths MUST stay low/light!
        clean_x_tier = (
            "首先，我们复现了内存泄漏问题。其次，排查了连接池配置。"
            "这意味着问题出在超时回收策略上，这表明旧版本存在竞态条件。总之，上线补丁后延迟恢复正常。"
        )
        res_clean = se.scan_text(clean_x_tier, genre="tech")
        self.assertEqual(res_clean["language"], "zh-cn")
        self.assertEqual(res_clean["active_family_count"], 0)
        self.assertEqual(res_clean["score"], 0)
        self.assertEqual(res_clean["risk_level"], "low")
        self.assertEqual(res_clean["route_hint"], "light")
        self.assertGreaterEqual(len(res_clean["informational_notes"]), 1)

        # Real Chinese AI slop with universal tells MUST trigger heavy/standard
        slop_zh = (
            "说白了，这不仅仅是一次工具升级，而是一场范式转移。\n"
            "残酷的现实是：当团队面对复杂需求时，对于管理者来说，解锁潜在价值才能深刻重塑未来。"
        )
        res_slop = se.scan_text(slop_zh, genre="blog")
        self.assertEqual(res_slop["language"], "zh-cn")
        rule_ids = {h["rule_id"] for h in res_slop["hits"]}
        self.assertIn("ZH-U-01", rule_ids)
        self.assertIn("ZH-U-02", rule_ids)
        self.assertIn("ZH-TR-01", rule_ids)
        self.assertIn("ZH-LEX-P1-01", rule_ids)
        self.assertEqual(res_slop["risk_level"], "high")

    def test_chinese_traditional_taiwan_specifics(self) -> None:
        text = (
            "這套软件可以幫團隊快速整理视频与数据,提升用户体验!\n"
            "核心是：這不只是更新，而是徹底重塑工作流程。讓我們一起攜手擁抱未來。"
        )
        res = se.scan_text(text, genre="blog", lang="zh-tw")
        rule_ids = {h["rule_id"] for h in res["hits"]}
        self.assertIn("ZHTW-01", rule_ids)
        self.assertIn("ZHTW-02", rule_ids)
        self.assertIn("ZH-U-01", rule_ids)
        self.assertIn("ZH-U-02", rule_ids)


class TestFalsePositiveResistanceAndProtectedZones(unittest.TestCase):
    def test_korean_literal_contexts_zero_lexical_hits(self) -> None:
        text = (
            "새로 산 카메라 렌즈에 지문이 묻어 부드러운 천으로 닦았다.\n"
            "스마트폰 화면 잠금 해제 비밀번호를 세 번 틀렸다.\n"
            "거실 벽지 무늬를 고르느라 주말 오후를 다 썼다.\n"
            "할아버지는 평생 집안의 기둥으로 가족을 지켰다.\n"
            "의사가 환자의 맥을 짚고 안정이 필요하다고 말했다.\n"
            "대장간에서 달군 쇠로 칼날을 벼렸다.\n"
            "기계 설계 도면에서 회전축과 좌표축의 오차를 수정했다.\n"
            "우물에서 찬 물을 길어 올렸다."
        )
        res = se.scan_text(text, genre="blog")
        lex_hits = [h for h in res["hits"] if h["family"] == "lexical_traps"]
        self.assertEqual(lex_hits, [], f"Unexpected literal false positives: {lex_hits}")
        self.assertEqual(res["risk_level"], "low")
        self.assertEqual(res["route_hint"], "light")

    def test_single_metric_comma_rate_never_escalates_high_risk(self) -> None:
        # Pre-ChatGPT style clean Korean essay with frequent commas after connective endings (Pebblous lesson)
        essay = (
            "가을비가 내리며, 골목 돌담이 젖어 들었다.\n"
            "나는 우산을 접고, 처마 밑에서 잠시 숨을 돌렸다.\n"
            "오래된 서점 문이 열리지만, 안에서는 종이 냄새만 은은히 났다.\n"
            "주인장은 차를 따르며, 요즘 손님이 뜸하다고 웃었다.\n"
            "책장을 한참 넘겼으나, 끝내 빈손으로 밖을 나왔다."
        )
        res = se.scan_text(essay, genre="blog")
        # Directional C-11 hint may appear, but active_family_count MUST stay 0 and risk_level MUST be low!
        self.assertEqual(res["active_family_count"], 0)
        self.assertEqual(res["risk_level"], "low")
        self.assertEqual(res["route_hint"], "light")

    def test_protected_zones_ignored_by_scanner(self) -> None:
        text = (
            "---\n"
            "title: Let's dive in to the vibrant tapestry\n"
            "---\n"
            "We benchmarked the parser on 200 files.\n\n"
            "```python\n"
            "# Let's delve into the game-changer tapestry\n"
            "msg = 'Great question! I hope this helps!'\n"
            "```\n\n"
            "The inline token `delve_tapestry` stays untouched, and "
            "the interviewee said \"This is not just a tool, but a vibrant game-changer\" in March.\n"
            "Reference: https://example.com/delve-into-vibrant-tapestry\n"
        )
        res = se.scan_text(text, genre="tech")
        self.assertEqual(res["active_family_count"], 0, f"Protected zones leaked into hits: {res['hits']}")
        self.assertEqual(res["risk_level"], "low")


class TestUnicodeScrubbing(unittest.TestCase):
    def test_clean_unicode_preserves_code_and_emoji_zwj(self) -> None:
        raw = (
            "Hello\u202fworld\u200b! Family emoji 👨‍👩‍👧‍👦 stays intact.\n"
            "Inline `\u202fkeep\u200b` stays intact.\n"
            "```txt\n"
            "code\u202fblock\u200b\n"
            "```\n"
        )
        cleaned, summary = se.clean_invisible_unicode(raw)
        self.assertEqual(summary["total_cleaned"], 2)
        self.assertEqual(summary["cleaned_by_code"]["U+202F"], 1)
        self.assertEqual(summary["cleaned_by_code"]["U+200B"], 1)
        self.assertIn("Hello world! Family emoji 👨‍👩‍👧‍👦 stays intact.", cleaned)
        self.assertIn("`\u202fkeep\u200b`", cleaned)
        self.assertIn("code\u202fblock\u200b", cleaned)


class TestDeterministicVerifyGates(unittest.TestCase):
    def test_clean_surgical_refactor_passes(self) -> None:
        before = (
            "우리 팀은 2026년 3월에 14개 서비스의 응답 지연을 점검했다.\n"
            "캐시 정책을 통해 응답 시간을 240ms에서 85ms로 줄였다.\n"
            "담당자는 \"다음 분기에도 같은 기준을 적용한다\"고 밝혔다.\n"
            "자세한 로그와 설정은 https://example.com/bench-2026 에서 확인할 수 있다."
        )
        after = (
            "우리 팀은 2026년 3월에 14개 서비스의 응답 지연을 점검했다.\n"
            "캐시 정책을 바꿔 응답 시간을 240ms에서 85ms로 줄였다.\n"
            "담당자는 \"다음 분기에도 같은 기준을 적용한다\"고 밝혔다.\n"
            "자세한 로그와 설정은 https://example.com/bench-2026 에서 확인할 수 있다."
        )
        res = se.verify_edit(before, after, genre="tech", mode="refactor")
        self.assertEqual(res["overall"], "PASS", f"Expected PASS, got: {res}")

    def test_dropped_number_or_quote_fails(self) -> None:
        before = '매출이 24% 늘었고 담당자는 "내년 3월 출시한다"고 말했다.'
        after = '매출이 크게 늘었고 담당자는 "내년 봄 출시한다"고 말했다.'
        res = se.verify_edit(before, after, genre="blog", mode="refactor")
        self.assertEqual(res["overall"], "FAIL")
        self.assertEqual(res["gates"]["protected_spans"]["status"], "FAIL")
        self.assertIn("24%", res["gates"]["protected_spans"]["missing"]["numbers"])
        self.assertIn('"내년 3월 출시한다"', res["gates"]["protected_spans"]["missing"]["quotes"])

    def test_over_editing_fails_in_refactor_and_length_collapse_warns(self) -> None:
        before = (
            "첫 번째 문단에서는 데이터베이스 인덱스 재구성 과정과 잠금 시간을 설명합니다. "
            "두 번째 문단에서는 배치 크기를 조정했을 때의 메모리 변화를 기록합니다. "
            "세 번째 문단에서는 배포 후 모니터링 결과를 요약합니다."
        )
        after = "인덱스 재구성 후 메모리와 지연을 확인했다."
        res = se.verify_edit(before, after, genre="tech", mode="refactor")
        self.assertEqual(res["gates"]["change_rate"]["status"], "FAIL")
        self.assertEqual(res["gates"]["length_ratio"]["status"], "WARN")
        self.assertEqual(res["overall"], "FAIL")

        # Same edit in recreate mode passes change_rate (only length_ratio warns)
        res_recreate = se.verify_edit(before, after, genre="tech", mode="recreate")
        self.assertEqual(res_recreate["gates"]["change_rate"]["status"], "PASS")

    def test_negation_parity_odd_warns_even_passes(self) -> None:
        # Japanese double negative collapse: 2 -> 0 (delta -2, even) => PASS
        ja_before = "この設定を使えないとは言えません。"
        ja_after = "この設定を使うことができます。"
        res_even = se.verify_edit(ja_before, ja_after, genre="tech", mode="recreate")
        self.assertEqual(res_even["gates"]["negation_parity"]["status"], "PASS")
        self.assertEqual(res_even["gates"]["negation_parity"]["delta"], -2)

        # Polarity flip: 1 -> 0 (delta -1, odd) => WARN
        ko_before = "이 옵션은 구버전 브라우저를 지원하지 않는다."
        ko_after = "이 옵션은 구버전 브라우저를 지원한다."
        res_odd = se.verify_edit(ko_before, ko_after, genre="tech", mode="refactor")
        self.assertEqual(res_odd["gates"]["negation_parity"]["status"], "WARN")
        self.assertEqual(res_odd["gates"]["negation_parity"]["delta"], -1)

    def test_epistemic_hedge_shift_warns(self) -> None:
        before = "The patch may reduce peak memory usage and likely avoids deadlocks."
        after = "The patch must reduce peak memory usage and certainly avoids deadlocks."
        res = se.verify_edit(before, after, genre="tech", mode="refactor")
        self.assertEqual(res["gates"]["epistemic_hedges"]["status"], "WARN")

    def test_p1_lexical_regression_fails(self) -> None:
        before = "이 관점에서 보면 팀의 역량을 끌어낼 방법이 보인다."
        after = "이 렌즈로 보면 팀의 잠재력을 잠금 해제할 방법이 보인다."
        res = se.verify_edit(before, after, genre="blog", mode="recreate")
        self.assertEqual(res["overall"], "FAIL")
        self.assertEqual(res["gates"]["lexical_regression"]["status"], "FAIL")
        injected_ids = {x["rule_id"] for x in res["gates"]["lexical_regression"]["injected"]}
        self.assertIn("KO-LEX-P1-01", injected_ids)
        self.assertIn("KO-LEX-P1-08", injected_ids)

    def test_academic_register_guard_fails_on_slang_or_excess_em_dashes(self) -> None:
        before = "Abstract\nWe evaluate 3 models across 10 datasets (Lee et al., 2025)."
        after_slang = "Abstract\nHonestly, we evaluate 3 models across 10 datasets — super cool — right (Lee et al., 2025)."
        res = se.verify_edit(before, after_slang, genre="academic", mode="recreate")
        self.assertEqual(res["overall"], "FAIL")
        self.assertEqual(res["gates"]["academic_register"]["status"], "FAIL")
        self.assertGreaterEqual(len(res["gates"]["academic_register"]["issues"]), 2)

        zh_before = "摘要\n本研究基于3组公开数据集评估模型稳定性。"
        zh_slang = "摘要\n说白了，本研究基于3组公开数据集评估模型稳定性，太牛了。"
        res_zh = se.verify_edit(zh_before, zh_slang, genre="academic", mode="recreate")
        self.assertEqual(res_zh["gates"]["academic_register"]["status"], "FAIL")


class TestCLISubcommands(unittest.TestCase):
    def test_cli_end_to_end_all_subcommands(self) -> None:
        script = str(SCRIPT_DIR / "slop_engine.py")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            orig = p / "orig.md"
            cleaned_u = p / "orig_clean.md"
            edited = p / "edited.md"
            report = p / "diff.md"

            orig.write_text(
                "우리 팀은 2026년 4월에 12개 API를 점검했다.\u202f\n"
                "이 도구는 단순히 빠른 것이 아니라 혁신의 렌즈를 통해 잠재력을 잠금 해제합니다.\n"
                "결론적으로 시사하는 바가 크다.\n",
                encoding="utf-8",
            )
            edited.write_text(
                "우리 팀은 2026년 4월에 12개 API를 점검했다.\n"
                "이 도구는 응답 속도를 높이고 팀의 업무 병목을 줄인다.\n",
                encoding="utf-8",
            )

            # 1. scan --json
            r_scan = subprocess.run(
                [sys.executable, script, "scan", str(orig), "--genre", "blog", "--json"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            scan_data = json.loads(r_scan.stdout)
            self.assertEqual(scan_data["language"], "ko")
            self.assertEqual(scan_data["invisible_unicode"]["total"], 1)
            self.assertEqual(scan_data["route_hint"], "heavy")

            # 2. clean-unicode --out --json
            r_clean = subprocess.run(
                [sys.executable, script, "clean-unicode", str(orig), "--out", str(cleaned_u), "--json"],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            clean_data = json.loads(r_clean.stdout)
            self.assertEqual(clean_data["total_cleaned"], 1)
            self.assertNotIn("\u202f", cleaned_u.read_text(encoding="utf-8"))

            # 3. verify --mode recreate --json (should exit 0)
            r_ver = subprocess.run(
                [
                    sys.executable, script, "verify",
                    "--before", str(cleaned_u), "--after", str(edited),
                    "--genre", "blog", "--mode", "recreate", "--json",
                ],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            ver_data = json.loads(r_ver.stdout)
            self.assertIn(ver_data["overall"], ("PASS", "WARN"))
            self.assertEqual(ver_data["gates"]["protected_spans"]["status"], "PASS")
            self.assertEqual(ver_data["gates"]["lexical_regression"]["status"], "PASS")

            # 4. diff-report --out
            subprocess.run(
                [
                    sys.executable, script, "diff-report",
                    "--before", str(cleaned_u), "--after", str(edited),
                    "--genre", "blog", "--mode", "recreate", "--out", str(report),
                ],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            rep_txt = report.read_text(encoding="utf-8")
            self.assertIn("# Anti-Slop Diff & Metrics Report", rep_txt)
            self.assertIn("## 1. Before vs. After Metrics", rep_txt)
            self.assertIn("### [1]", rep_txt)

    def test_universal_unicode_cli_stdin_and_encodings(self) -> None:
        script = str(SCRIPT_DIR / "slop_engine.py")
        sample = (
            "이 기능은 단순히 빠른 것이 아니라 사용자 여정의 렌즈를 통해 혁신을 이룹니다.\u202f 🚀𠮷\n"
            "도움이 되셨길 바랍니다.\n"
        )
        cp949_env = os.environ.copy()
        cp949_env["PYTHONUTF8"] = "0"
        cp949_env["PYTHONIOENCODING"] = "cp949:replace"

        # 1. UTF-8 piped to stdin under CP949 locale must preserve full Unicode & detect all families
        r_stdin = subprocess.run(
            [sys.executable, script, "scan", "-", "--genre", "blog", "--json"],
            input=sample.encode("utf-8"),
            capture_output=True,
            env=cp949_env,
            check=True,
        )
        data_stdin = json.loads(r_stdin.stdout.decode("utf-8"))
        self.assertEqual(data_stdin["language"], "ko")
        self.assertEqual(data_stdin["invisible_unicode"]["total"], 1)
        self.assertEqual(data_stdin["route_hint"], "heavy")

        # 2. UTF-16 LE/BE and UTF-32 files produce identical scan results
        with tempfile.TemporaryDirectory() as tmp:
            for enc in ("utf-16", "utf-16-be", "utf-32"):
                fp = Path(tmp) / f"sample_{enc}.md"
                fp.write_bytes(sample.encode(enc))
                r_file = subprocess.run(
                    [sys.executable, script, "scan", str(fp), "--genre", "blog", "--json"],
                    capture_output=True,
                    env=cp949_env,
                    check=True,
                )
                data_file = json.loads(r_file.stdout.decode("utf-8"))
                self.assertEqual(data_file["invisible_unicode"]["total"], 1, enc)
                self.assertEqual(data_file["route_hint"], "heavy", enc)
                self.assertEqual(data_file["hit_count"], data_stdin["hit_count"], enc)


if __name__ == "__main__":
    unittest.main()
