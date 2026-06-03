#!/usr/bin/env bash
# Runs the daily market report via Claude Code.
#
# CRON SETUP (weekdays at 8am UTC):
#   crontab -e
#   0 8 * * 1-5 /full/path/to/scraper/run_claude_report.sh >> /full/path/to/scraper/logs/report.log 2>&1
#
# MANUAL RUN:
#   bash run_claude_report.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SCRIPT_DIR/logs"

echo "=== Market report started: $(date -u '+%Y-%m-%d %H:%M UTC') ==="

cd "$SCRIPT_DIR"

# Load .env credentials for the notifiers
set -o allexport
source "$SCRIPT_DIR/.env"
set +o allexport

# Run Claude non-interactively with the /market-report slash command
claude --print "/market-report"

echo "=== Done: $(date -u '+%Y-%m-%d %H:%M UTC') ==="
