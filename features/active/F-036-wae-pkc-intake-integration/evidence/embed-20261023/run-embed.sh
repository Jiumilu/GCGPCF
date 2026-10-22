#!/usr/bin/env bash
# F-036 本地 iframe 嵌入复现
set -euo pipefail
ROOT="/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
cd "$ROOT/GlobalCloud PKC" && pnpm dev --host 127.0.0.1 >/tmp/pkc-dev-embed.log 2>&1 &
PKC_PID=$!
cd "$ROOT/GlobalCloud WAE"
printf 'VITE_WAE_AUTH_DEV_BYPASS=1\nVITE_PKC_EMBED_URL=http://127.0.0.1:5174/\n' > apps/wame/.env.local
pnpm dev >/tmp/wae-dev-embed.log 2>&1 &
WAE_PID=$!
cleanup() {
  kill "$PKC_PID" "$WAE_PID" 2>/dev/null || true
  rm -f apps/wame/.env.local
}
trap cleanup EXIT
sleep 10
cd "$(dirname "$0")"
[ -d node_modules ] || { npm init -y >/dev/null 2>&1; npm i playwright-core --no-audit --no-fund >/dev/null 2>&1; }
node embed-check.js
