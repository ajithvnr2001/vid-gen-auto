#!/usr/bin/env python3
"""10 — API alternative: same story scenes via gemini-omni-1.1-flash Interactions API.
No browser needed. Requires GEMINI_API_KEY (Google AI Studio, billing enabled).
Dialogues stay native Tamil; Tamil titles/voiceover are muxed in post because
Omni on-screen Tamil text is unreliable. See DOCUMENTATION.md section 5/#10."""
import base64
import os
import subprocess
import sys
from pathlib import Path

MODEL = "gemini-omni-1.1-flash"
CHARS = ("Characters (keep consistent across all clips): SELVA, a middle-aged "
         "wealthy Tamil merchant, moustache, white dhoti, gold chain; PERIYAVAR, a "
         "frail elderly Tamil man, white beard, torn grey clothes. "
         "Setting: old Tamil village, South Indian temple.")
STYLE = ("Warm cinematic realism, soft morning light, shallow depth of field, "
         "gentle camera push-in, no text, no watermark, no subtitles in frame.")

SCENES = [
    ("story1", "SELVA counts gold coins, servants nervous. SELVA says arrogantly "
               "in Tamil, 'பணம் இருந்தால் போதும்!'. " + CHARS + " " + STYLE),
    ("story2", "Temple entrance, incense. PERIYAVAR blesses SELVA, saying warmly in "
               "Tamil, 'ஐயா, உங்களுக்கு நல்ல உடல்நலமும் மனமகிழ்ச்சியும் கிடைக்கட்டும்!'. "
               + CHARS + " " + STYLE),
    ("story3", "PERIYAVAR says calmly in Tamil, 'உண்மையான செல்வம் அன்பான "
               "வார்த்தைகள் தான்.'. SELVA places money into open hands, saying in "
               "Tamil, 'இனிய சொல்லே பெரும் செல்வம்!'. " + CHARS + " " + STYLE),
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
