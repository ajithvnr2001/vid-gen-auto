# vid-gen-auto — End-to-End Documentation

Tamil moral-story video pipeline (Thirukkural 92, *Iniya Sol*): Google Flow + Gemini
Omni 1.1 Flash generation with native Tamil dialogue, driven by Playwright automation,
merged in Scenebuilder, delivered as a 30 s story video.

> What this repo is: the complete, runnable record of a real build
> (`/data/opencode/videogen/iniya_sol_30s_google_story.mp4`).
> What it is not: a SaaS wrapper. You run the scripts against your own Flow project.

---

## 1. How it was created (pipeline overview)

```
ins.txt (story + Flow project URL + cookie URL)
   │
   ├─► 01_authenticate ....... cookies.txt ─► Playwright ─► Flow project (PRO account)
   │                              (fallback: shared headed-Chrome login via VNC)
   ├─► 02_generate ........... 3 × text-to-video, Omni 1.1 Flash, 720p, 10 s, 16:9, x1
   │       clip1: merchant + native Tamil line 1 (no ingredient)
   │       clip2: temple blessing + native Tamil line 2 (clip1 attached as Ingredient)
   │       clip3: giving/moral + native Tamil lines 3–4 (clip2 attached as Ingredient)
   ├─► 03_verify ............. download each clip → faster-whisper transcription (Tamil)
   ├─► 04_merge .............. Scenebuilder scene [clip1, clip2, clip3] → Download scene
   └─► 05_deliver ............ order verified (frames + transcription) → final 30 s file
```

Flow options used, end to end: **Text-to-Video → Ingredients (video reference) →
Scenebuilder (Add to scene / Add clip / timeline verify) → Download scene**.
Deliberately *not* used: Extend (Veo-only per docs — disabled for Omni clips),
conversational edit (not needed), custom Voices (dialogue-in-prompt was enough).

Docs backing every step live in `docs/flow/` (crawled with Scrapling from
support.google.com/flow, DeepMind Omni, Gemini API docs — see §7).

---

## 2. What was used (tools & why)

| Tool | Role | Why this one |
|---|---|---|
| Python Playwright (+ bundled Chromium) | Browser automation driver | `add_cookies` session injection, CDP attach to a live browser, auto-waiting SPA locators |
| Real Google Chrome (stable .deb) under Xvfb | Logged-in session host | Google login + Flow need a real browser; headless cookie transfer fails (bound sessions) |
| x11vnc + websockify/noVNC + cloudflared tunnel | Remote login station | Owner opens a public URL, logs in manually once; automation then drives the live profile via CDP `:9222` |
| `cookies.txt` (Netscape, Get-cookies.txt-Locally) | Session bootstrap attempt | Worked for loading, but Google's `g.a000…` bound sessions reject datacenter IPs — documented dead-end, kept as fallback path |
| edge-tts (`ta-IN-PallaviNeural`) | Scratch narration only | Used for interim local cuts; **not** in the final Google-only video |
| faster-whisper (`tiny`, CPU int8) | Speech verification | Transcribes each downloaded clip, asserts Tamil dialogue present before merging |
| ffmpeg | Verification + joining | Frame extraction, duration/audio probes; final step joins the 3 verified Flow MP4s in story order |
| Scrapling (`Fetcher`) | Docs crawler | TLS-impersonating HTTP fetcher; used to crawl all 15 Flow help articles + Omni/API docs into `docs/flow/` |
| Scrapegraph-ai | Evaluated, not used | LLM-driven extraction is nondeterministic + costly per run; deterministic Playwright selectors won for repeated polling |
| Gemini API / `GEMINI_API_KEY` | Optional fast path | `omni_flow_build.py` generates the same scenes via Interactions API when a key exists (no browser needed) |

Environment this ran on: Ubuntu 22.04 container, Python 3.10, no GPU, no desktop
(noVNC provided the only display). Chromium for automation came from Playwright;
Chrome stable was installed from `dl.google.com` for the login station.

---

## 3. How it connects (architecture)

```
┌──────────────────────────── host/container ────────────────────────────┐
│  Xvfb :99 ─► openbox ─► google-chrome ──user-data-dir=./chrome-profile │
│      │                         │  --remote-debugging-port=9222         │
│      │ x11vnc :5900            │                                       │
│      └─► websockify :6080 ─► cloudflared tunnel ─► public noVNC URL    │
│                                (owner logs in here once)               │
│  Playwright ──connect_over_cdp(http://localhost:9222)──► same Chrome  │
│      │  scripts/sk/*.py                                               │
│      └─► flow.google.com/project/<id> (composer, settings, tiles,     │
│          ingredients, scenes, downloads)                               │
└────────────────────────────────────────────────────────────────────────┘
```

- Automation never stores passwords. It either injects `cookies.txt` into a fresh
  context (`scripts/01_cookies_probe.py`) or attaches to the live profile where the
  owner already logged in (`scripts/02_live_session.py` pattern — CDP attach).
- Downloads are routed via CDP `Browser.setDownloadBehavior` to a local folder so
  generated MP4s land on disk without a save dialog.
- Every destructive/expensive step (generation ≈ 15 credits per 10 s Omni clip,
  scene download) is preceded by a screenshot + aria-snapshot so selectors can be
  re-anchored if Flow's Angular UI shifts.

---

## 4. Manual input required (checklist)

1. **Google account with a PRO (or better) AI plan.** Free tier blocks video at
   peak hours and has no 10 s Omni quota worth relying on.
2. **Login, once.** Open the remote noVNC URL (or run Chrome locally with
   `--remote-debugging-port=9222`), sign in, complete any phone verification,
   open your Flow project. Automation takes over from there.
3. **Fresh `cookies.txt` (optional fallback).** Export via Get-cookies.txt-Locally
   and use within minutes; cross-machine reuse usually fails — prefer step 2.
4. **Credits.** Budget ≈ 15 credits × number of 10 s Omni clips (3 clips ≈ 45).
5. **Verification eyes (optional but recommended).** Scripts dump `*_prompt.png`,
   `*_done.png`, timeline screenshots; glance at them before the merge step.

Nothing else is manual: prompts, settings (Video · 720p · 10 s · x1 · Omni 1.1
Flash), ingredient attach, polling, scene assembly, download, verification are
all scripted in `scripts/`.

---

## 5. Complete code (scripts/)

All scripts are in `scripts/` and run in this order. Each prints progress to
stdout (redirect to a log) and exits non-zero on failure without spending more
credits than the step it is on.

| # | Script | Purpose | Key technique |
|---|---|---|---|
| 1 | `01_cookies_probe.py` | Load Netscape `cookies.txt` → open Flow project → report auth state + screenshot | Netscape→Playwright cookie mapping; `sameSite` omitted; session cookies `expires=-1` |
| 2 | `02_remote_login_station.sh` | Launch Xvfb+openbox+Chrome(CDP:9222)+x11vnc+websockify+cloudflared | Headed Chrome as a shared login station; CDP attach afterwards |
| 3 | `03_cdp_attach_check.py` | Verify live session: list pages, find Flow project, count composers | `connect_over_cdp`, aria roles, never `time.sleep` for state |
| 4 | `04_generate_clip.py` | Set model settings → fill prompt → Start → poll ≤15 min → screenshot | Force-clicks through CDK backdrops; `Video · 720p · 10s · x1 · Omni 1.1 Flash` |
| 5 | `05_attach_ingredient.py` | Attach previous clip as video Ingredient reference | Ingredients panel → Videos tab → Recent-first asset → Add to prompt; composer chip asserted |
| 6 | `06_download_clip.py` | Hover tile → More options → Download → 720p via CDP download path | `Browser.setDownloadBehavior`; 720p Original size menuitem |
| 7 | `07_verify_speech.py` | Transcribe clip audio, assert Tamil dialogue | faster-whisper `tiny` CPU; language=`ta`; prints timed segments |
| 8 | `08_build_scene.py` | Tile ⋮ → Add to scene → New scene; + → Add clip → option-by-index → Add media; verify 30 s timeline; Download scene | Recent-sorted picker indices; per-append screenshot; timeline counter assertion |
| 9 | `09_assemble_final.py` | Join verified clip MP4s in story order → 30 s file + `.srt` | ffmpeg concat (video+audio re-encode for clean joins); frame+transcription re-verification |
| 10 | `omni_flow_build.py` | API alternative: same scenes via `gemini-omni-1.1-flash` Interactions API | Needs `GEMINI_API_KEY`; Tamil titles/voiceover muxed in post |

Prompts used (English direction + verbatim Tamil dialogue — the Omni pattern for
non-English speech; Tamil-only direction text underperforms per prompt guide):

- **Clip 1:** merchant counts coins, says `பணம் இருந்தால் போதும்!`
- **Clip 2** (clip 1 as ingredient): temple blessing, `ஐயா, உங்களுக்கு நல்ல உடல்நலமும் மனமகிழ்ச்சியும் கிடைக்கட்டும்!`
- **Clip 3** (clip 2 as ingredient): wisdom + moral, `உண்மையான செல்வம் அன்பான வார்த்தைகள் தான்.` + `இனிய சொல்லே பெரும் செல்வம்!`

Verified transcriptions of the delivered file (faster-whisper, `ta @ 1.0`):
`0–10 s: பணம்…`, `10–20 s: உங்களுக்கு மகிழ்ச்சி…`, `20–30 s: உண்மையான செல்வம்… + இனிய சொல்லே…`.

---

## 6. Flow options analyzed (everything encountered, end to end)

Based on `docs/flow/*.md` (crawled help center) **plus** live-UI exploration. This is
the complete surface this project touched or evaluated:

**Create path (prompt box):** free-text composer (`contenteditable`), `+` Add
ingredients, Agent toggle, model Settings trigger, Start generation (disabled
until prompt non-empty). Settings: mode radio Image/Video; model family menu
(Nano Banana 2 default → switch to Video → Omni 1.1 Flash / Veo 3.1-Lite/Fast/
Quality); resolution 360p(draft)/720p; length 4/6/8/10 s (10 s = Omni-only);
aspect 16:9/9:16; outputs x1–x4 (credit multiplier shown live, e.g. 24 credits).

**Ingredients:** panel tabs All/Images/Videos/Voices/Characters/Avatars/Uploads;
Recent-first asset list with preview player + trim sliders; **Add to prompt**
attaches a composer chip the model conditions on. Voice refs are Omni-only and
error without ingredients. Custom voices: base voice + name + performance
description + 8 s sample dialogue → Sync → Save. (Evaluated; dialogue-in-prompt
was sufficient, so no custom voice was created.)

**Frames:** start/end frame picker (web-only for Omni); clip detail → pause →
hover → **Save frame** produces reusable ingredients. (Evaluated; video-ingredient
attach gave equivalent continuity with fewer steps.)

**Extend:** `Extend (Veo 3.1 - Lite)` — **disabled for Omni clips** (docs: "You can
currently only extend Veo generated videos"). Dead end for this pipeline; noted
so nobody retries it.

**Edit (Omni):** upload ≤60 s/1 GB (trim ≤30 s) → select ≤10 s segment → prompt +
optional ingredients → Generate; up to 3 conversational turns keep context.
History panel keeps every version + prompt; Save to Project reuses versions.
(Not needed — first-pass generations were accepted.)

**Characters/Avatar/Tools/Collections:** `@Name` mentions, `@me` avatar, custom
Tools builder, Collection folders — catalogued from docs, not required for a
3-clip fable.

**Scenebuilder:** tile ⋮ → Add to scene → New scene/append; + → Add clip →
Recent-sorted picker → Add media appends at END; timeline counter (00:30:00
asserted); trim handles; **drag reorder works but is coordinate-fragile — verify
by downloading, never trust the filmstrip alone**; Download scene → 720p file.
Scene tile shows clip-count badge; Bin holds deleted scenes (restorable).

**Credits/regions/safety:** per-generation costs (Omni 720p ≈ 15 cr per 10 s);
free 50/day with peak blackout ~14:00–17:00 UTC; some voice/frame features are
region-gated; uploads pass safety checks; all outputs carry SynthID + C2PA.

---

## 7. Docs included (crawled)

`docs/flow/*.md` — all 15 Flow help articles + Omni prompt guide + Gemini
prompting intro + cloud video overview, fetched with
`tools/crawl_flow_docs.py` (Scrapling `Fetcher`). Each file keeps its source
URL header. Start with `docs/flow/00_INDEX.md`.

`docs/repos.md` — what each ins.txt reference repo contributed:
Get-cookies.txt-Locally (Netscape format + load mapping), Scrapling (crawler +
`DynamicSession`/`capture_xhr` patterns), Scrapegraph-ai (evaluated, rejected
for driver duties), Playwright (cookie injection, `storage_state` > cookies.txt,
SPA wait/hydration rules, CDP download routing).

---

## 8. Verification & troubleshooting

- **Auth dead?** Project URL redirects to `/about`, or `myaccount.google.com`
  lands on marketing → session rejected cross-machine. Fix: fresh login via the
  remote station (§4.2), not older cookies.
- **VNC dead but generation alive?** x11vnc dies while Chrome/CDP continue.
  Restart `x11vnc` on `:99`; Flow work is unaffected.
- **Settings clicks intercepted?** CDK backdrop covers menu → use `force=True`
  clicks, or Escape + reopen menu.
- **Duplicate asset names?** Picker lists by Recent; disambiguate by index after
  screenshotting thumbnails, or rename assets first.
- **Wrong scene order?** Never trust the filmstrip. Download → extract frames at
  5/15/25 s → transcribe 0–10/10–20/20–30 s → compare against expected lines.
- **Silent clip?** Download → `volumedetect` (mean > −50 dB expected) →
  transcribe; if silent, use Omni conversational-edit turn to add dialogue
  rather than regenerating blind.
