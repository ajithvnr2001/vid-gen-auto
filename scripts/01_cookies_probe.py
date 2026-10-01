#!/usr/bin/env python3
"""01 — Cookie probe: load Netscape cookies.txt into Playwright, open the Flow
project, report auth state (logged in vs redirected to /about). Read-only."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIE_FILE = sys.argv[1] if len(sys.argv) > 1 else "cookies.txt"
PROJECT_URL = sys.argv[2] if len(sys.argv) > 2 else "https://flow.google.com/"


def load_netscape(path):
    cookies = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 7:
            continue
        domain, _, cpath, secure, exp, name, value = p[:7]
        try:
            exp = int(exp)
        except ValueError:
            exp = -1
        if exp == 0:
            exp = -1  # session cookie
        d = {"name": name, "value": value, "domain": domain,
             "path": cpath, "expires": exp}
        if secure.upper() == "TRUE":
            d["secure"] = True
        cookies.append(d)
    return cookies


def main():
    cookies = load_netscape(COOKIE_FILE)
    print("loaded %d cookies" % len(cookies))
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled", "--no-sandbox"])
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
            locale="en-US")
        ok = sum(1 for c in cookies if not _add(ctx, c))
        print("cookies added ok=%d" % ok)
        page = ctx.new_page()
        page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(12000)
        print("title:", page.title())
        print("url:", page.url)
        print("state:", "LOGGED_OUT" if "/about" in page.url else "CHECK")
        page.screenshot(path="probe.png")
        browser.close()


def _add(ctx, c):
    try:
        ctx.add_cookies([c])
        return False
    except Exception:
        return True


if __name__ == "__main__":
    main()
