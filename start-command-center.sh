#!/usr/bin/env sh
# MAINTENANCE: Start the loopback Command Center through the main CLI and preserve forwarded arguments.
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "Offline Survival.py" --web "$@"
fi
exec python "Offline Survival.py" --web "$@"
