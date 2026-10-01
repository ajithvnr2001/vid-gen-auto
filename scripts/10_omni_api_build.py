#!/usr/bin/env python3
"""10 — API alternative: same story scenes via gemini-omni-1.1-flash Interactions API.
No browser needed. Requires GEMINI_API_KEY (Google AI Studio, billing enabled).
Dialogues stay in the characters' native language; titles/voiceover are muxed in
post because Omni on-screen text in non-Latin scripts is unreliable.
See DOCUMENTATION.md section 5/#10. Edit CHARS/SCENES for your own story."""
import base64
import os
import subprocess
import sys
from pathlib import Path

MODEL = "gemini-omni-1.1-flash"
CHARS = ("Characters (keep consistent across all clips): HERO, <age, look, clothing>; "
         "ELDER, <age, look, clothing>. "
         "Setting: <your location>.")
STYLE = ("Warm cinematic realism, soft morning light, shallow depth of field, "
         "gentle camera push-in, no text, no watermark, no subtitles in frame.")

SCENES = [
    ("story1", "HERO <action in location>, supporting cast nervous. HERO says "
               "arrogantly in <language>, '<line 1>'. " + CHARS + " " + STYLE),
    ("story2", "<Location> at morning. ELDER <action>, addressing HERO. ELDER says "
               "warmly in <language>, '<line 2>'. " + CHARS + " " + STYLE),
    ("story3", "ELDER says calmly in <language>, '<line 3>'. HERO, humbled, "
               "<kind action> and says in <language>, '<line 4>'. "
               + CHARS + " " + STYLE),
]


def main():
    from google import genai  # pip install "google-genai>=2.10.0"
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("Set GEMINI_API_KEY first.")
        return 2
    client = genai.Client(api_key=key)
    out = Path("clips")
    out.mkdir(exist_ok=True)
    for sid, prompt in SCENES:
        mp4 = out / (sid + ".mp4")
        if mp4.exists() and mp4.stat().st_size > 100_000:
            print("reuse", mp4)
            continue
        print("generating", sid)
        it = client.interactions.create(
            model=MODEL, input=prompt,
            response_format={"type": "video", "aspect_ratio": "16:9",
                             "resolution": "720p"})
        mp4.write_bytes(base64.b64decode(it.output_video.data))
    print("clips in ./clips/ - merge with 09_assemble_final.py after verifying")
    return 0


if __name__ == "__main__":
    sys.exit(main())
