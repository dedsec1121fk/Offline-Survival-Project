#!/usr/bin/env sh
# MAINTENANCE: Hand diagnostics to the installed/default phone browser; do not hard-code a browser engine.
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "Offline Survival.py" --phone-browser-test "$@"
fi
exec python "Offline Survival.py" --phone-browser-test "$@"
