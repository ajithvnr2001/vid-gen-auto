#!/usr/bin/env python3
"""03 — CDP attach check: verify the live session (Flow app loaded? composer
present? PRO badge?). Run after the owner logs in via script 02."""
from playwright.sync_api import sync_playwright

PROJECT_URL = "https://flow.google.com/project/<YOUR_PROJECT_ID>"

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = b.contexts[0]
    for p in ctx.pages:
        print("PAGE:", p.title()[:60], "|", p.url[:110])
    flow = [p for p in ctx.pages if "flow.google.com" in (p.url or "")
            and "about" not in (p.url or "")]
    print("flow app pages:", len(flow))
    if flow:
        f = flow[0]
        f.bring_to_front()
        f.wait_for_timeout(3000)
        n = f.locator("[contenteditable='true'], textarea, [role='textbox']").count()
        print("composer count:", n, "(>0 means logged in)")
        f.screenshot(path="session_check.png")
