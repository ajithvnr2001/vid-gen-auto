#!/bin/bash
# 02 — Remote login station: headed Chrome + VNC + public URL for one manual login.
# The owner opens the printed noVNC URL, signs in to Google, opens the Flow project.
# Automation then attaches via CDP on :9222 (see 03_cdp_attach_check.py).
set -u
export DISPLAY=:99
mkdir -p remote/chrome-profile
pkill -f "Xvfb :99" 2>/dev/null; pkill -f "remote-debugging-port=9222" 2>/dev/null; sleep 1
Xvfb :99 -screen 0 1366x900x24 > remote/xvfb.log 2>&1 &
sleep 2
openbox --display :99 > remote/openbox.log 2>&1 &
google-chrome --display=:99 --user-data-dir=$PWD/remote/chrome-profile \
  --remote-debugging-port=9222 --no-sandbox --disable-dev-shm-usage \
  --no-first-run --no-default-browser-check --window-size=1366,900 \
  "https://accounts.google.com/ServiceLogin?continue=https://flow.google.com/" \
  > remote/chrome.log 2>&1 &
sleep 3
x11vnc -display :99 -rfbport 5900 -shared -forever -bg \
  -o remote/x11vnc.log -ncache 0 -nosel -noprimary
websockify --web=/usr/share/novnc 6080 localhost:5900 > remote/websockify.log 2>&1 &
sleep 1
cloudflared tunnel --url http://localhost:6080 > remote/cloudflared.log 2>&1 &
sleep 12
echo "noVNC public URL:"
grep -oiE "https://[a-z0-9.-]+\.trycloudflare\.com" remote/cloudflared.log | sort -u | head -1
echo "(append /vnc.html, click Connect)"
curl -s -m 5 http://localhost:9222/json/version | head -c 120; echo
