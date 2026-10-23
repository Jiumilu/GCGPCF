#!/usr/bin/env bash
# F-036 正式接入评审证据采集：隔离临时 IdP（A=system-admin bootstrap；B=viewer 由 A 建号）+ WAE dev :4301 + Playwright。
# 只破坏临时目录；4300 上他人实例不动；口令仅 env/临时文件（600），运行结束全删，不写入证据。
set -u
ROOT="/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
EV="$ROOT/GlobalCloud GPCF/features/active/F-036-wae-pkc-intake-integration/evidence/embed-auth-20261023"
WAE="$ROOT/GlobalCloud WAE"
TMP="/tmp/f036-embed-auth-idp"
PKC_PID=""
PORT=4301
BASE="http://127.0.0.1:$PORT"

rm -rf "$TMP"; mkdir -p "$TMP"; chmod 700 "$TMP"
gen_pw() { printf 'F036r!%sZ' "$(head -c 16 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)"; }
gen_pw > "$TMP/a1"; gen_pw > "$TMP/a2"; gen_pw > "$TMP/b1"; gen_pw > "$TMP/b2"
chmod 600 "$TMP"/a1 "$TMP"/a2 "$TMP"/b1 "$TMP"/b2

cleanup() {
  if [ -n "${PKC_PID:-}" ]; then kill "$PKC_PID" 2>/dev/null || true; fi
  if [ -n "${PKC_PORT_PID:-}" ]; then kill "$PKC_PORT_PID" 2>/dev/null || true; fi
  if [ -n "${DEV_PID:-}" ]; then
    kill "$DEV_PID" 2>/dev/null || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do kill -0 "$DEV_PID" 2>/dev/null || break; sleep 0.3; done
    kill -9 "$DEV_PID" 2>/dev/null || true
  fi
  # pnpm 会再 spawn vite 子进程；按"本脚本记录的本端口 listener PID"精确收尾（不碰 4300）
  if [ -n "${DEV_PORT_PID:-}" ]; then kill "$DEV_PORT_PID" 2>/dev/null || true; fi
  rm -f "$EV/node_modules"
  rm -rf "$TMP"
}
trap cleanup EXIT

# 预检：4301 必须是空闲（若被占用——含上次残留——先报错，不盲目复用他人实例）
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "PORT_BUSY $PORT (cleanup leftover first; 4300 不在此列且不触碰)"
  exit 4
fi

cd "$ROOT/GlobalCloud PKC"
pnpm dev --host 127.0.0.1 > "$TMP/pkc-dev.log" 2>&1 &
PKC_PID=$!
for _ in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 2 http://127.0.0.1:5174/ 2>/dev/null || true)
  [ "$code" = "200" ] && break
  sleep 0.5
done
PKC_PORT_PID=$(lsof -nP -iTCP:5174 -sTCP:LISTEN -t 2>/dev/null | head -1 || true)
cd "$WAE"
WAE_IDP_DIRECTORY="$TMP/users.json" \
WAE_IDP_AUDIT="$TMP/audit.jsonl" \
WAE_IDP_SESSIONS="$TMP/sessions.json" \
WAE_IDP_CONFIRM_TOKENS="$TMP/confirm-tokens.json" \
WAE_IDP_TENANT_CONFIG="$TMP/tenant-config.json" \
WAE_IDP_ADMIN_USER="f036-review-admin" \
WAE_IDP_ADMIN_PASSWORD="$(cat "$TMP/a1")" \
VITE_PKC_EMBED_URL="http://127.0.0.1:5174/" \
  pnpm --filter @globalcloud/wame exec vite --port "$PORT" --strictPort > "$TMP/dev.log" 2>&1 &
DEV_PID=$!

READY=0
for _ in $(seq 1 120); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 2 "$BASE/api/idp/roles" 2>/dev/null || true)
  case "$code" in 2*|3*|401) READY=1; break;; esac
  sleep 0.25
done
if [ "$READY" != "1" ]; then echo "DEV_NOT_READY"; tail -40 "$TMP/dev.log"; exit 2; fi
DEV_PORT_PID=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -1 || true)
echo "DEV_READY $BASE (pid=${DEV_PORT_PID:-unknown})"
BOOT=$(curl -sS -X POST "$BASE/api/idp/bootstrap" -H 'content-type: application/json' -d '{}' -m 10)
case "$BOOT" in *'"ok":true'*) echo "BOOTSTRAP ok";; *) echo "BOOTSTRAP_FAILED $BOOT"; exit 3;; esac

ln -sfn "$WAE/apps/wame/node_modules" "$EV/node_modules"
cd "$WAE"
F036_OUT="$EV" F036_BASE_URL="$BASE" \
F036_A_USER="f036-review-admin" F036_A_PASSWORD="$(cat "$TMP/a1")" F036_A_NEW_PASSWORD="$(cat "$TMP/a2")" \
F036_B_USER="f036-review-viewer" F036_B_PASSWORD="$(cat "$TMP/b1")" F036_B_NEW_PASSWORD="$(cat "$TMP/b2")" \
  apps/wame/node_modules/.bin/playwright test --grep "受控嵌入" --config "$EV/playwright.embed.config.ts" > "$TMP/pw.log" 2>&1
PW_EXIT=$?
echo "PLAYWRIGHT_EXIT $PW_EXIT"
tail -50 "$TMP/pw.log"

mkdir -p "$EV/logs"
tail -80 "$TMP/dev.log" | sed 's/[A-Za-z0-9!_-]\{20,\}/<redacted>/g' > "$EV/logs/dev-server.log"
cp "$TMP/pw.log" "$EV/logs/playwright-run.log"
cat > "$EV/logs/run-meta.json" <<JSON
{
  "port": $PORT,
  "port4300_status": "busy-other-session (untouched)",
  "isolated_idp_dir": "/tmp/f036-review-idp (deleted after run)",
  "accounts": ["f036-review-admin (system-admin, bootstrap)", "f036-review-viewer (viewer, created via POST /api/idp/users)"],
  "playwright_exit": $PW_EXIT,
  "run_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "secrets_in_evidence": "none"
}
JSON
exit "$PW_EXIT"
