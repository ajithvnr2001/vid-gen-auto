#!/usr/bin/env python3
"""06 — Download a clip at 720p: open tile detail -> Download media -> 720p.
Saves into ./downloads/ via CDP download behavior. Usage: 06_download_clip.py
(clicks the newest video tile)."""
import os
import time
from playwright.sync_api import sync_playwright

DL = os.path.abspath("downloads")
os.makedirs(DL, exist_ok=True)

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = b.contexts[0]
    cdp = ctx.new_cdp_session(ctx.pages[0])
    cdp.send("Browser.setDownloadBehavior",
             {"behavior": "allow", "downloadPath": DL, "eventsEnabled": True})
    f = [p for p in ctx.pages if "/project/" in (p.url or "")][0]
    f.bring_to_front()
    f.wait_for_timeout(1500)
    before = set(os.listdir(DL))
    # open newest video tile (top-left area)
    f.mouse.click(500, 255)
    f.wait_for_timeout(5000)
    for b2 in f.locator("button").all():
        try:
            if "download" in ((b2.get_attribute("aria-label") or "").lower()):
                b2.click()
                break
        except Exception:
            pass
    f.wait_for_timeout(2000)
    f.get_by_role("menuitem", name="720p Original size").click()
    for _ in range(18):
        time.sleep(5)
        new = [x for x in os.listdir(DL) if x not in before
               and not x.endswith(".crdownload")]
        if new:
            print("downloaded:", new)
            break
    else:
        raise SystemExit("TIMEOUT waiting for download")
