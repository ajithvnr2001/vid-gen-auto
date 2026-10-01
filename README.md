# vid-gen-auto

End-to-end Tamil moral-story video pipeline: **Google Flow + Gemini Omni 1.1 Flash**
generation with native Tamil dialogue, driven by Playwright automation, merged in
Scenebuilder, delivered as a 30 s story video (Thirukkural 92, *Iniya Sol*).

## Result

`iniya_sol_30s_google_story.mp4` — 30 s, 1280×720: merchant → temple blessing →
giving/moral, every line spoken natively in Tamil by the generated characters
(transcription-verified, `ta @ 1.0`).

## Quickstart

```bash
pip install -r requirements.txt
playwright install chromium   # automation browser (login station uses real Chrome)
# 1. log in (one manual step):  bash scripts/02_remote_login_station.sh
#    open the printed noVNC URL, sign in, open your Flow project
python scripts/03_cdp_attach_check.py     # verify live session
python scripts/04_generate_clip.py "<prompt>" story1
python scripts/05_attach_ingredient.py --list     # pick reference index
python scripts/05_attach_ingredient.py 0
python scripts/04_generate_clip.py "<prompt-2>" story2
python scripts/06_download_clip.py
python scripts/07_verify_speech.py downloads/<clip>.mp4
# ... repeat, then scripts/08_build_scene.py flow, then:
python scripts/09_assemble_final.py s1.mp4 s2.mp4 s3.mp4 final.mp4
```

No API key path: `GEMINI_API_KEY=… python scripts/10_omni_api_build.py`

## Contents

- `DOCUMENTATION.md` — full developer doc: pipeline, tools, connection, manual
  inputs, complete code guide, Flow option analysis, troubleshooting.
- `scripts/` — 01–10 runnable pipeline in order.
- `tools/crawl_flow_docs.py` — Scrapling crawler that produced `docs/flow/`.
- `docs/flow/` — all 15 Flow help articles + Omni/API docs (source URLs inside).
- `docs/repos.md` — what each reference repo contributed.
- `shots/`, `downloads/`, `clips/` — created at runtime (git-ignored).

## Costs & requirements

Google account with AI PRO plan; ≈15 credits per 10 s Omni clip; Chrome + Xvfb
for the login station; no GPU needed (verification uses CPU whisper).
