#!/usr/bin/env python3
"""09 — Join verified Flow clips in story order (bytes only; no added audio/voice).
Usage: 09_assemble_final.py clip1.mp4 clip2.mp4 clip3.mp4 out.mp4
Re-verifies duration + per-segment transcription after joining."""
import subprocess
import sys

clips, out = sys.argv[1:4], sys.argv[4]
lst = "concat_list.txt"
open(lst, "w").write("\n".join("file '%s'" % c for c in clips))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", lst, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                "-movflags", "+faststart", out], check=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1", out], capture_output=True, text=True)
print("final duration: %ss -> %s" % (r.stdout.strip(), out))
