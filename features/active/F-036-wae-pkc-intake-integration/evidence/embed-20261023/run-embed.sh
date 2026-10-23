#!/usr/bin/env bash
# F-036 本地 iframe 嵌入复现（dev bypass）
set -euo pipefail
ROOT="/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKC_PID=""; WAE_PID=""
cleanup() {
  [ -n "$PKC_PID" ] && kill "$PKC_PID" 2>/dev/null || true
  [ -n "$WAE_PID" ] && kill "$WAE_PID" 2>/dev/null || true
  for p in 4300 5174; do
    pid=$(lsof -nP -iTCP:"$p" -sTCP:LISTEN -t 2>/dev/null | head -1 || true)
    [ -n "$pid" ] && kill "$pid" 2>/dev/null || true
  done
  rm -f "$ROOT/GlobalCloud WAE/apps/wame/.env.local"
}
trap cleanup EXIT
for p in 4300 5174; do
  if lsof -nP -iTCP:"$p" -sTCP:LISTEN -t >/dev/null 2>&1; then echo "PORT_BUSY $p"; exit 4; fi
done
cd "$ROOT/GlobalCloud PKC"
pnpm dev --host 127.0.0.1 >/tmp/pkc-dev-embed.log 2>&1 &
PKC_PID=$!
cd "$ROOT/GlobalCloud WAE"
printf 'VITE_WAE_AUTH_DEV_BYPASS=1\nVITE_PKC_EMBED_URL=http://127.0.0.1:5174/\n' > apps/wame/.env.local
pnpm dev >/tmp/wae-dev-embed.log 2>&1 &
WAE_PID=$!
for _ in $(seq 1 60); do
  c1=$(curl -s -o /dev/null -w '%{http_code}' -m 2 http://127.0.0.1:5174/ 2>/dev/null || true)
  c2=$(curl -s -o /dev/null -w '%{http_code}' -m 2 http://127.0.0.1:4300/ 2>/dev/null || true)
  [ "$c1" = "200" ] && [ "$c2" = "200" ] && break
  sleep 1
done
cd "$SCRIPT_DIR"
[ -d node_modules ] || { npm init -y >/dev/null 2>&1; npm i playwright-core --no-audit --no-fund >/dev/null 2>&1; }
node embed-check.js
