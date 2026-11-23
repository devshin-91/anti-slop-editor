# Voice & Persona Distillation Template (HyPerAlign + 5-Line Voice Memo)

Pure few-shot copying ("write like these 3 posts") fails to transfer deep idiolect reliably.
Extract **explicit style hypotheses** from 2–3 real user samples first, then let the user correct
any guessed traits before applying.

---

## Step 1. Voice Extraction Prompt (Use When User Supplies 2–3 Real Writing Samples)

> **Rule:** Extract *only* traits directly evidenced in the samples. Never invent habits not present
> in the samples. Keep authentic quirks (emoji habits, `ㅋㅋ`, short parentheticals, contractions).

Produce a compact **Voice Profile** with these 7 slots:

```markdown
# Voice Profile: <author-or-channel-name>
- **Primary Language & Register:** <e.g., Korean 해요체 / English direct engineering prose>
- **Sentence Length & Cadence:** <observed range, short punchy ratio, comma/period habits>
- **Signature Openings & Closings:** <how the author enters a topic and ends a piece>
- **Explanation Order & Examples:** <conclusion-first vs story-first; how concrete examples appear>
- **Punctuation & Formatting Overrides:** <explicitly list tells to KEEP because the author genuinely uses them, e.g., "uses ~1 em-dash per 200 words", "uses parenthetical asides">
- **Frequent Expressions / Quirks:** <actual recurring words, endings, or mild discourse markers>
- **Hard Never-Use List (Author's Bans):** <words/tones the author dislikes, e.g., "no exclamation marks", "no '압도적인/혁신적인'", "no hashtags">
```

---

## Step 2. Precedence Contract (When Stacking Voice + Anti-Slop)

1. **Facts & Meaning Preservation** always win (outer guardrail).
2. **Architecture & Venue Register** come next (do not turn a postmortem into a chatty essay).
3. **Author Voice Overrides** beat generic surface bans (if the sample genuinely uses em-dashes or short fragments, match the sample rate instead of zeroing them out).
4. **Select 3–5 signature voice moves per piece**—never cram every quirk into every paragraph.
5. **Read-Aloud Calibration ("입이 걸리는 문장" test):** Draft 3 paragraphs first; any sentence the author would never say aloud gets rewritten before scaling to the full piece.
