#!/usr/bin/env python3
"""07 — Verify spoken dialogue in a clip (faster-whisper tiny, CPU).
Usage: 07_verify_speech.py clip.mp4 [lang]  -> prints timed segments.
Gate the merge step on this: no verified dialogue -> conversational edit, not blind regen."""
import subprocess
import sys

src = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) > 2 else "en"
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1", src], capture_output=True, text=True)
print("duration: %ss" % r.stdout.strip())

from faster_whisper import WhisperModel  # pip install faster-whisper
m = WhisperModel("tiny", device="cpu", compute_type="int8")
segs, info = m.transcribe(src, language=lang, beam_size=1)
print("language: %s (%.2f)" % (info.language, info.language_probability))
found = False
for s in segs:
    print("[%.1f-%.1f] %s" % (s.start, s.end, s.text))
    found = True
if not found:
    raise SystemExit("NO SPEECH DETECTED")
