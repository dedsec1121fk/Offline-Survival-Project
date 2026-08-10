#!/usr/bin/env sh
# MAINTENANCE: Keep this launcher dependency-light and route reader opening through the main Python CLI.
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "Offline Survival.py" --reader "$@"
fi
exec python "Offline Survival.py" --reader "$@"
