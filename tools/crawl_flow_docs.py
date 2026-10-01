#!/usr/bin/env python3
"""Crawl Flow/Omni help docs into docs/flow/*.md (with source-URL headers).

Method (why two drivers — documented deliberately):
- Scrapling Fetcher (static HTTP) is tried first: cheap and fast. It CANNOT read
  these pages: Google renders help-article bodies via JS hydration, so static DOM
  holds only headings (verified: <h1> present, no div >800 chars of text).
- Playwright Chromium (headless) is the working driver: wait 8 s post-load, read
  [role=main] inner_text. Playwright is one of the four ins.txt reference repos,
  same as the automation driver, so no new dependency.
Usage: python tools/crawl_flow_docs.py
"""
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "docs" / "flow"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = {
    "01_get_started": "https://support.google.com/flow/answer/16353333?hl=en",
    "02_flow_agent": "https://support.google.com/flow/answer/17093911?hl=en",
    "03_create_videos": "https://support.google.com/flow/answer/16353334?hl=en",
    "04_edit_scenes": "https://support.google.com/flow/answer/16935718?hl=en",
    "05_images": "https://support.google.com/flow/answer/16729550?hl=en",
    "06_avatar": "https://support.google.com/flow/answer/17102997?hl=en",
    "07_tools": "https://support.google.com/flow/answer/17104535?hl=en",
    "08_projects_assets": "https://support.google.com/flow/answer/16935308?hl=en",
    "09_models_features": "https://support.google.com/flow/answer/16352836?hl=en",
    "10_credits": "https://support.google.com/flow/answer/16526234?hl=en",
    "11_regions": "https://support.google.com/flow/answer/16353544?hl=en",
    "12_feedback": "https://support.google.com/flow/answer/16353335?hl=en",
    "13_data": "https://support.google.com/flow/answer/17025472?hl=en",
    "14_shortcuts": "https://support.google.com/flow/answer/17069754?hl=en",
    "15_download_data": "https://support.google.com/flow/answer/17571126?hl=en",
    "16_omni_prompt_guide": "https://deepmind.google/models/gemini-omni/prompt-guide/",
    "17_gemini_prompting": "https://ai.google.dev/gemini-api/docs/prompting-intro",
    "18_cloud_video": "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/overview",
}

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, args=["--no-sandbox"])
    pg = b.new_context(locale="en-US").new_page()
    for name, url in PAGES.items():
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(8000)
            main = pg.locator("[role='main']")
            text = main.inner_text() if main.count() else pg.locator("body").inner_text()
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
            text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
            (OUT / (name + ".md")).write_text(
                "# %s\n\nSource: %s\n\n%s\n" % (name, url, text[:35000]),
                encoding="utf-8")
            print("%s: %d chars" % (name, len(text)), flush=True)
        except Exception as e:
            print("%s: ERR %s" % (name, str(e)[:150]), flush=True)
        time.sleep(1)
    b.close()
print("CRAWL DONE")
