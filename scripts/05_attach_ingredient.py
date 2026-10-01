#!/usr/bin/env python3
"""05 — Attach a project video as an Ingredient reference (Flow-native continuation).
Opens Ingredients -> Videos tab (Recent first) -> picks an asset by index after
printing names -> Add to prompt -> asserts composer chip. Print-only dry run with
--list (screenshots the picker so you can choose the index)."""
import sys
from playwright.sync_api import sync_playwright

DRY = "--list" in sys.argv

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = b.contexts[0]
    f = [p for p in ctx.pages if "/project/" in (p.url or "")][0]
    f.bring_to_front()
    f.wait_for_timeout(1500)
    import re
    f.get_by_role("button", name=re.compile("Add ingredients", re.I)).click()
    f.wait_for_timeout(2500)
    opts = f.locator("[role='option']").all()
    print("options: %d" % len(opts))
    for i, o in enumerate(opts):
        try:
            print("[%d] %r" % (i, o.inner_text()[:70]))
        except Exception:
            pass
    f.screenshot(path="ingredient_picker.png")
    if not DRY:
        idx = int(sys.argv[1])
        opts[idx].click()
        f.wait_for_timeout(1000)
        f.get_by_role("button", name="Add to prompt").click()
        f.wait_for_timeout(2500)
        s = f.locator("body").aria_snapshot()
        assert "Ingredient" in s, "chip missing - attach failed"
        print("attached option %d" % idx)
