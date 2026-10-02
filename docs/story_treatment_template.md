# Story treatment template (write this BEFORE generating anything)

Copy this file to `treatments/<your-story>.md` and fill it in. Every generation
prompt is derived from §3 — no prompt is ever written ad hoc.

## Logline
One sentence: whose story, what occasion/change, what moral. Example pattern:
"<Occasion> eve in <place>, told through <whose> working hands — ending in <image>."

## Character bible (repeat verbatim in every prompt)
- NAME (age): role, look, clothing (2–3 immutable visual tags each)
- NAME (age): ...
- Setting: one line — place, era, light mood

Rules: immutable tags never change between clips (checked shirt, red saree,
moustache…). New characters appear at most once per clip.

## Scene plan (one row per 10 s clip)
| # | Time | Beat | Visual (one action) | Dialogue (verbatim, target language) |
|---|------|------|---------------------|--------------------------------------|
| 1 | 0–10 | opening/work | … | line 1 |
| 2 | 10–20 | development | … | line 2 |
| … | … | … | … | … |
| N | … | moral/closing | … | closing line |

Rules: one simple action per clip; one or two short spoken lines per clip
(≈7 s of speech max — transcription-gated later); English direction +
verbatim dialogue (see DOCUMENTATION.md §5 prompt pattern).

## Continuity plan
- Clip N+1 references clip N (ingredient attach, script 05) and/or starts from
  clip N's saved last frame (script 11).
- Total runtime math: sum of clip lengths (e.g. 8 + 10×5 = 58 s). Note any
  non-10 s clip explicitly.

## Verification expectations
For each clip, the exact line(s) the transcription gate (script 07) must find.
If a line is missing → conversational edit turn, not blind regen.
