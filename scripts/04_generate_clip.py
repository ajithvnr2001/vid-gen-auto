#!/usr/bin/env python3
"""04 — Generate one clip: enforce settings, fill prompt, Start, poll for completion.
Usage: python 04_generate_clip.py "<prompt>" <tag>   (screenshots -> ./shots/)
Credit warning: each run spends ~15 credits (10 s Omni x1)."""
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SHOTS = Path("shots")
SHOTS.mkdir(exist_ok=True)

PROMPT, TAG = sys.argv[1], sys.argv[2]
PROJECT_URL = "https://flow.google.com/project/<YOUR_PROJECT_ID>"


def wait_clear(f, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            if "Creating scene" not in f.locator("body").aria_snapshot():
                pass
            s = f.locator("body").aria_snapshot()
            if re.search(r"0:1\d|1:0\d", s):
                return True
        except Exception:
            pass
        time.sleep(10)
    return False


with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = b.contexts[0]
    f = [p for p in ctx.pages if "/project/" in (p.url or "")][0]
    f.bring_to_front()
    # --- settings: Video - 720p - 10s - x1 - Omni 1.1 Flash ---
    f.get_by_role("button", name="Settings trigger").click()
    f.wait_for_timeout(2000)
    for name in ["Video", "10s", "x1", "16:9", "720p"]:
        try:
            f.get_by_role("radio", name=name).click(force=True, timeout=4000)
        except Exception as e:
            print("radio %s: %s" % (name, str(e)[:100]))
    try:
        trig = f.get_by_role("button", name="Settings trigger").inner_text()
        if "Omni" not in trig:
            f.get_by_role("button", name=re.compile("Select model family", re.I)).click()
            f.wait_for_timeout(1500)
            f.get_by_role("menuitem", name=re.compile("Omni 1.1 Flash", re.I)).click()
    except Exception as e:
        print("model:", str(e)[:150])
    f.keyboard.press("Escape")
    f.wait_for_timeout(1000)
    # --- prompt + generate ---
    editor = f.locator("div[contenteditable='true']").first
    editor.click()
    f.wait_for_timeout(800)
    f.keyboard.type(PROMPT, delay=2)
    f.wait_for_timeout(1500)
    f.screenshot(path=str(SHOTS / (TAG + "_prompt.png")))
    start = f.get_by_role("button", name="Start generation")
    print("start enabled:", start.is_enabled())
    start.click()
    print(TAG + ": generation started")
    f.wait_for_timeout(5000)
    ok = wait_clear(f)
    f.screenshot(path=str(SHOTS / (TAG + "_done.png")))
    print(TAG + (": DONE" if ok else ": TIMEOUT - check screenshot"))
