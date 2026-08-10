#!/usr/bin/env sh
# MAINTENANCE: Hand the loopback Command Center to Android's installed/default browser; do not select Chromium or another engine.
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "Offline Survival.py" --web "$@"
fi
exec python "Offline Survival.py" --web "$@"
