# vid-gen-auto

End-to-end story-video automation for **Google Flow + Gemini Omni 1.1 Flash**:
text-to-video generation with native dialogue, driven by Playwright automation,
merged in Scenebuilder, delivered as a finished story video.

## Result

Produces a 30 s, 1280×720 story video (opening → development → moral), every
line spoken natively by the generated characters (transcription-verified).

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

## Progress

**Video creation is automated** ✅ — text-to-video (Omni 1.1 Flash) + video
Ingredients + speech verification + Scenebuilder merge + download, end to
end via `scripts/04–09`. Proven on a shipped 30 s story build.

| Flow Studio capability | Status |
|---|---|
| Text-to-video generation (Omni/Veo, settings, polling) | ✅ Automated (`04`) |
| Video Ingredients attach (continuity references) | ✅ Automated (`05`) |
| Clip download 720p via CDP | ✅ Automated (`06`) |
| Dialogue verification (transcription gate) | ✅ Automated (`07`) |
| Scenebuilder merge + Download scene | ✅ Automated (`08`, supervised — verify order by download) |
| Join + deliver final file | ✅ Automated (`09`) |
| Omni API path (no browser) | ✅ Scripted (`10`, needs `GEMINI_API_KEY`) |
| Cookie login bootstrap | ✅ Scripted (`01`, usually fails cross-machine — use login station) |
| Remote login station (VNC + tunnel + CDP) | ✅ Scripted (`02`, `03`) |
| Docs crawler (all Flow help articles) | ✅ Automated (`tools/crawl_flow_docs.py`) |
| Frames (start/end, Save frame) | ⏳ Pending automation |
| Custom Voices + voice references (`@Voice`) | ⏳ Pending automation |
| Characters / avatar (`@Name`, `@me`) | ⏳ Pending automation |
| Nano Banana image gen + image ingredients | ⏳ Pending automation |
| Omni conversational edit (3-turn refine) | ⏳ Pending automation |
| Veo Extend (Veo clips only) | ⏳ Pending automation |
| Upload-edit flow (≤60 s in, ≤10 s segment) | ⏳ Pending automation |
| Flow Agent batch variations | ⏳ Pending automation |
| Collections / Tools builder / Keyboard flows | ⏳ Pending automation |
| 1080p/4K upscale + YouTube publish | ⏳ Pending automation |

## Contents

- `DOCUMENTATION.md` — full developer doc: pipeline, tools, connection, manual
  inputs, complete code guide, Flow option analysis, troubleshooting.
- `scripts/` — 01–10 runnable pipeline in order.
- `tools/crawl_flow_docs.py` — crawler behind `docs/flow/` (Scrapling attempted,
  Playwright fallback wins; see file header for why).
- `docs/flow/` — all 15 Flow help articles + Omni/API docs (source URLs inside).
- `docs/repos.md` — what each reference repo contributed.
- `shots/`, `downloads/`, `clips/` — created at runtime (git-ignored).

## Costs & requirements

Google account with AI PRO plan; ≈15 credits per 10 s Omni clip; Chrome + Xvfb
for the login station; no GPU needed (verification uses CPU whisper).
