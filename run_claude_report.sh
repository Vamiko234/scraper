#!/usr/bin/env bash
# Daily market report via Claude Code.
# Add to cron: 0 8 * * 1-5 /path/to/scraper/run_claude_report.sh >> /path/to/scraper/logs/report.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "=== Market report started at $(date -u '+%Y-%m-%d %H:%M UTC') ==="

cd "$SCRIPT_DIR"

# Load .env so notifiers have credentials
if [ -f "$SCRIPT_DIR/.env" ]; then
  export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Run Claude non-interactively with the market-report slash command
claude --print "/market-report"

echo "=== Done at $(date -u '+%Y-%m-%d %H:%M UTC') ==="
