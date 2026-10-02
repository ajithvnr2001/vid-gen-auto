#!/usr/bin/env python3
"""00 — Google login automation for the shared-station Chrome (CDP :9222).
Reads credentials ONLY from env (never commit them, never log them):
  GOOGLE_EMAIL, GOOGLE_PASSWORD
Flow: identifier page -> fill email -> Next -> password page (skips hidden
decoy inputs, uses the visible box only) -> Next -> watches for the 2-step
challenge (approve / tap-the-number on your phone) or Flow landing.
Takes NO screenshot while the password is on screen.
Usage:
  GOOGLE_EMAIL=you@gmail.com GOOGLE_PASSWORD='...' python 00_login.py
"""
import os
import re
import sys
from playwright.sync_api import sync_playwright

email = os.environ.get("GOOGLE_EMAIL", "")
pwd = os.environ.get("GOOGLE_PASSWORD", "")
if not email or not pwd:
    sys.exit("Set GOOGLE_EMAIL and GOOGLE_PASSWORD env vars (never in files).")


def main():
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://localhost:9222")
        ctx = b.contexts[0]
        pages = [p for p in ctx.pages if "accounts.google.com" in (p.url or "")]
        if not pages:
            sys.exit("No Google sign-in tab found - open it first.")
        f = pages[0]
        f.bring_to_front()
        f.wait_for_timeout(2000)
        # STEP 1: email (identifier page; skip if already past it)
        try:
            ident = f.locator("input[name='identifier']").first
            if ident.count() and ident.is_visible():
                ident.click()
                f.wait_for_timeout(500)
                ident.fill(email)
                f.get_by_role("button", name="Next").click()
                print("email submitted")
                f.wait_for_timeout(8000)
        except Exception as e:
            print("email step: %s" % str(e)[:120])
        # STEP 2: password - visible box only (aria-hidden decoys ignored)
        box = None
        for _ in range(6):
            for b2 in f.locator("input[type='password']").all():
                try:
                    if b2.is_visible():
                        box = b2
                        break
                except Exception:
                    pass
            if box:
                break
            f.wait_for_timeout(3000)
        if not box:
            sys.exit("NO VISIBLE PW BOX - state: %s" % f.url[:100])
        box.click()
        f.wait_for_timeout(800)
        box.fill(pwd)
        f.wait_for_timeout(1000)
        f.get_by_role("button", name="Next").click()
        print("password submitted - approve on phone if challenged")
        # STEP 3: watch challenge / landing (3 min)
        import time
        for i in range(36):
            f.wait_for_timeout(5000)
            try:
                url = f.url
                snap = f.locator("body").aria_snapshot()[:3000]
            except Exception:
                continue
            low = snap.lower()
            if "flow.google.com" in url and "accounts" not in url:
                print("LOGGED IN - on Flow")
                return 0
            nums = re.findall(r"(?:select|tap|choose|number)\D{0,40}?([1-9][0-9])",
                              snap, re.I)
            if "select the number" in low or "tap the number" in low:
                print("TAP %s ON PHONE (t+%ds)" % (nums, (i + 1) * 5))
            elif any(k in low for k in ["verify it", "try another way",
                                        "2-step", "verification"]):
                print("VERIFY SCREEN (t+%ds)" % ((i + 1) * 5))
            elif "wrong password" in low or "incorrect" in low:
                sys.exit("PASSWORD REJECTED - check GOOGLE_PASSWORD")
        print("TIMEOUT waiting for approval")
        return 1


if __name__ == "__main__":
    sys.exit(main())
