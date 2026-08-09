#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "Offline Survival.py" --phone-browser-test "$@"
fi
exec python "Offline Survival.py" --phone-browser-test "$@"
