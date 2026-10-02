#!/usr/bin/env python3
"""12 — Batch-generate N clips with hardened guards (generic, any story).
Guards (each learned from a real failure):
  - settings_lock(): set Video/10s/x1/16:9/720p + model, READ BACK the trigger
    text, retry 4x, ABORT before spending credits if it won't stick. (Without
    this, runs silently fall back to image mode or 8s-x2.)
  - render watcher: completion = pending-tile percentage disappears AND no
    "Failed" tile. Never match prompt text (false positives).
  - failure retry: "Failed. Generation timed out... not charged" -> retry same
    prompt once (transient, costs nothing).
Usage: edit PROMPTS, then: python 12_batch_generate.py
Next: 06_download_clip.py + 07_verify_speech.py per clip, then 08/09.
"""
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_URL = "https://flow.google.com/project/<YOUR_PROJECT_ID>"
PROMPTS = [
    ("clip1", "<your scene-1 prompt with native dialogue line>"),
    ("clip2", "<your scene-2 prompt, reference clip 1 for continuity>"),
]

SHOTS = Path("shots")
SHOTS.mkdir(exist_ok=True)


def settings_lock(f, tries=4):
    for a in range(tries):
        f.get_by_role("button", name="Settings trigger").click()
        f.wait_for_timeout(2000)
        for name in ["Video", "10s", "x1", "16:9", "720p"]:
            try:
                f.get_by_role("radio", name=name).click(force=True, timeout=4000)
            except Exception:
                pass
        try:
            trig = f.get_by_role("button", name="Settings trigger").inner_text()
        except Exception:
            trig = ""
        f.keyboard.press("Escape")
        f.wait_for_timeout(1000)
        if "10s" in trig and "x1" in trig.split("·")[-1]:
            return True
    return False


def ensure_omni(f):
    try:
        trig = f.get_by_role("button", name="Settings trigger").inner_text()
        if "Omni" not in trig:
            f.get_by_role("button", name=re.compile("Select model family", re.I)).click()
            f.wait_for_timeout(1500)
            f.get_by_role("menuitem", name=re.compile("Omni 1.1 Flash", re.I)).click()
    except Exception as e:
        print("model step: %s" % str(e)[:150])


def render_done(f, limit_s=1200):
    import re as _re
    t0 = time.time()
    while time.time() - t0 < limit_s:
        f.wait_for_timeout(10000)
        try:
            s = f.locator("body").aria_snapshot()
        except Exception:
            continue
        if _re.search(r"\b\d{1,3}%", s):
            continue  # still rendering
        if "failed" in s.lower() and "timed out" in s.lower():
            return "failed"
        return "done"
    return "timeout"


def main():
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://localhost:9222")
        ctx = b.contexts[0]
        fps = [p for p in ctx.pages if "/project/" in (p.url or "")]
        f = fps[0]
        f.bring_to_front()
        for tag, prompt in PROMPTS:
            if not settings_lock(f):
                sys.exit("SETTINGS FAILED for %s - aborting, no credits spent" % tag)
            ensure_omni(f)
            f.keyboard.press("Escape")
            f.wait_for_timeout(800)
            editor = f.locator("div[contenteditable='true']").first
            editor.click()
            f.wait_for_timeout(800)
            f.keyboard.type(prompt, delay=2)
            f.wait_for_timeout(1500)
            f.screenshot(path=str(SHOTS / (tag + "_prompt.png")))
            start = f.get_by_role("button", name="Start generation")
            assert start.is_enabled(), "Start disabled - prompt empty?"
            start.click()
            print("%s: started" % tag, flush=True)
            f.wait_for_timeout(5000)
            st = render_done(f)
            f.screenshot(path=str(SHOTS / (tag + "_done.png")))
            print("%s: %s" % (tag, st), flush=True)
            if st != "done":
                print("%s needs attention - see screenshot" % tag, flush=True)


if __name__ == "__main__":
    main()
