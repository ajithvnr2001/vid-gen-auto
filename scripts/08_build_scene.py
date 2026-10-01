#!/usr/bin/env python3
"""08 — Build ONE scene in exact order and download it.
Strategy that works: tile menu -> Add to scene -> New scene (clip 1 verified via
panel prompt), then + -> Add clip -> picker option BY INDEX (Recent order, verify
the preview thumbnail screenshot before Add media) -> wait for build.
Then Done -> open scene -> Download scene -> verify 30 s + transcribe segments.
See DOCUMENTATION.md section 6 for the full option analysis and pitfalls
(duplicate asset names, order scrambling - always verify, never trust filmstrip).
"""
# Full step-by-step implementation lives in DOCUMENTATION.md §5/#8 table plus the
# session scripts; the primitives below are the exact calls used in production.

PRIMITIVES = """
# new scene from a tile menu (grid view, tile hovered):
menuitem "Add to scene" -> menuitem "New scene" -> button "Switch to Scenebuilder"
# append at timeline end:
button[aria-label="Add clip" and y>400] -> [menuitem "Add clip"] ->
  option[index] (screenshot preview FIRST) -> button "Add media" ->
  wait until "Creating scene…" leaves the snapshot
# download:
button "Done" -> Scenes tab -> open scene tile -> button "Download scene"
# verify (shell):
ffprobe duration == 30.0 ; frames at 5/15/25 s ; transcribe 0-10/10-20/20-30 (ta)
"""

if __name__ == "__main__":
    print(PRIMITIVES)
    print("Run the steps against your live session; keep every screenshot.")
