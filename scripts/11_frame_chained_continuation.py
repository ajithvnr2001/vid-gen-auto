#!/usr/bin/env python3
"""11 — Frame-chained continuation: the Omni-only Extend workaround.
Loop: last frame of clip N (Save frame) -> Frames-to-Video start frame for
clip N+1 with a continuation prompt (+ previous clip as ingredient for
identity) -> verify speech -> repeat -> merge in Scenebuilder.
No Veo involved. Each iteration is one 10 s generation (~15 credits).
Usage: python 11_frame_chained_continuation.py "<continuation prompt>" <tag>
The + Add clip -> Select media picker flow is used; the start frame is attached
via Frames in the generation settings (web-only for Omni). Verify the timeline
by downloading (see 08_build_scene.py notes) — never trust the filmstrip alone.
"""
import sys
import time
from playwright.sync_api import sync_playwright

PROMPT, TAG = sys.argv[1], sys.argv[2]

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = b.contexts[0]
    f = [p for p in ctx.pages if "/project/" in (p.url or "")][0]
    f.bring_to_front()
    # NOTE: attach the saved last-frame image first via
    #   Settings -> Video -> Frames -> + Add start frame,
    # then fill PROMPT below and generate. Kept semi-manual on purpose:
    # frame-picker thumbnails must be eyeballed (see DOCUMENTATION.md pitfalls).
    editor = f.locator("div[contenteditable='true']").first
    editor.click()
    f.wait_for_timeout(800)
    f.keyboard.type(PROMPT, delay=2)
    f.wait_for_timeout(1500)
    f.screenshot(path="chained_%s_prompt.png" % TAG)
    start = f.get_by_role("button", name="Start generation")
    print("start enabled:", start.is_enabled())
    start.click()
    print(TAG + ": continuation generating")
    f.wait_for_timeout(5000)
    import re
    for i in range(90):
        f.wait_for_timeout(10000)
        try:
            s = f.locator("body").aria_snapshot()
        except Exception:
            continue
        if re.search(r"0:1\d|1:0\d", s):
            print("%s: done at %ds" % (TAG, (i + 1) * 10))
            break
    f.screenshot(path="chained_%s_done.png" % TAG)
    print("verify speech next: 07_verify_speech.py <downloaded clip>")
