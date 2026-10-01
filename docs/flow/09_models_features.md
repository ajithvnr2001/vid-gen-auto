# 09_models_features

Source: https://support.google.com/flow/answer/16352836?hl=en
Refreshed: 2026-10-01 (matrix verified live; supersedes earlier crawl)

Google Flow provides features powered by Veo models, Gemini Omni (standard 720p
and draft 360p) and Gemini. If you select an unsupported feature for a model,
Flow notifies you. Check prompt-box settings for active model/resolution/credits.

## Veo 3.1 - Lite
- Text to Video: both aspects, 4/6/8s
- Frames to Video (first; first+last): both aspects, 4/6/8s
- Ingredients/References to Video: both aspects, 8s only
- Extend videos: both aspects, 8s only; extends Veo 3.1 Lite/Fast/Quality 8s clips
  (Tip: ALL Veo 3.1 8s videos extend, but extension must run on Veo 3.1 Lite)
- NOT supported: Video to Video editing

## Veo 3.1 - Fast
- Same as Lite for Text/Frames/Ingredients (Ingredients 8s only)
- NOT supported: Video to Video editing, Extend videos

## Veo 3.1 - Quality
- Text to Video + Frames (first, first+last): both aspects, 4/6/8s
- NOT supported: Ingredients/References, Video to Video editing, Extend videos

## Gemini Omni Flash 1.1
- Text to Video / Frames first / Frames first+last / Ingredients: both aspects, 4/6/8/10s
- Video to Video editing: both aspects, up to 10s
- Coming soon: Extend videos
- Exclusives: Omni 360p draft (half credit cost); 10s clips; start+end frames
  (web-only); edit uploaded+generated videos; custom voices; free 360p->720p
  upscale (Pro/Ultra). Some voice features region-gated.

## Image models (frames & ingredients)
1. Nano Banana Pro: complex designs, accurate details, pro control (Ultra default)
2. Nano Banana 2 Lite: fast, high-quality (free default)
3. Nano Banana 2: standard fast

## Older matrix (Veo 2 era, answer/16893917) — extra modes not in current UI
- Camera Control (Veo 2 Fast, landscape, needs first frame)
- Jump To (Fast+Quality landscape; Quality recommended)
- Insert or remove an object (both aspects)
- Audio generation experimental on Veo 3.1: SFX/background/some speech via prompt
  text; known issues: speech muted on minors, speech may trigger subtitles;
  credits refunded on low-quality audio failures.
