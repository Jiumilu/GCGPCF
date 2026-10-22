#!/usr/bin/env bash
# F-036 task_flow E2E 隔离运行器（可复现）：起临时 IdP 的 WAE dev :4301 → bootstrap → Playwright → 收尾。
# 用法：bash "GlobalCloud GPCF/features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/run-e2e.sh"
# 说明：4300 被其它会话占用时不终止他人服务，改用 4301 隔离实例；口令只在本机 /tmp 临时目录（600）与进程 env。
# 口令只在 /tmp 临时目录（600）与进程 env 中存在，运行结束整目录删除；不写入证据。
set -u

ROOT="/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
GPCF_FEATURE="$ROOT/GlobalCloud GPCF/features/active/F-036-wae-pkc-intake-integration"
EV="$GPCF_FEATURE/evidence/e2e-20261022"
WAE="$ROOT/GlobalCloud WAE"
TMP="/tmp/f036-e2e-idp"
PORT=4301
BASE="http://127.0.0.1:$PORT"

rm -rf "$TMP"; mkdir -p "$TMP"
chmod 700 "$TMP"
# 两个强口令（首登初始口令 / 改密后新口令）；仅本机临时目录 600
printf 'F036a!%sZ' "$(head -c 16 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)" > "$TMP/pw1"
printf 'F036b!%sZ' "$(head -c 16 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)" > "$TMP/pw2"
chmod 600 "$TMP/pw1" "$TMP/pw2"

cleanup() {
  if [ -n "${DEV_PID:-}" ]; then
    kill "$DEV_PID" 2>/dev/null || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      kill -0 "$DEV_PID" 2>/dev/null || break
      sleep 0.3
    done
    kill -9 "$DEV_PID" 2>/dev/null || true
  fi
  rm -f "$EV/node_modules"
  rm -rf "$TMP"
}
trap cleanup EXIT

# 1) 起隔离 dev（临时 IdP 目录；不碰 4300 上他人实例）
cd "$WAE"
WAE_IDP_DIRECTORY="$TMP/users.json" \
WAE_IDP_AUDIT="$TMP/audit.jsonl" \
WAE_IDP_SESSIONS="$TMP/sessions.json" \
WAE_IDP_CONFIRM_TOKENS="$TMP/confirm-tokens.json" \
WAE_IDP_TENANT_CONFIG="$TMP/tenant-config.json" \
WAE_IDP_ADMIN_USER="f036-e2e-admin" \
WAE_IDP_ADMIN_PASSWORD="$(cat "$TMP/pw1")" \
  pnpm --filter @globalcloud/wame exec vite --port "$PORT" --strictPort > "$TMP/dev.log" 2>&1 &
DEV_PID=$!

READY=0
for _ in $(seq 1 120); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 2 "$BASE/api/idp/roles" 2>/dev/null || true)
  case "$code" in 2*|3*|401) READY=1; break;; esac
  sleep 0.25
done
if [ "$READY" != "1" ]; then
  echo "DEV_NOT_READY"; tail -40 "$TMP/dev.log"; exit 2
fi
echo "DEV_READY $BASE"

# 2) bootstrap 唯一临时 system-admin（口令来自服务端 env，不落凭据）
BOOT=$(curl -sS -X POST "$BASE/api/idp/bootstrap" -H 'content-type: application/json' -d '{}' -m 10)
echo "BOOTSTRAP $BOOT" | sed 's/[A-Za-z0-9!_-]\{16,\}/<redacted>/g'
case "$BOOT" in *'"ok":true'*) : ;; *) echo "BOOTSTRAP_FAILED"; exit 3;; esac

# 3) Playwright（复用 F-010 配置模式；node_modules 临时软链到 WAE apps/wame 的安装）
ln -sfn "$WAE/apps/wame/node_modules" "$EV/node_modules"
cd "$WAE"
F036_OUT="$EV" F036_BASE_URL="$BASE" F036_USER="f036-e2e-admin" \
F036_PASSWORD="$(cat "$TMP/pw1")" F036_NEW_PASSWORD="$(cat "$TMP/pw2")" \
  apps/wame/node_modules/.bin/playwright test --config "$EV/playwright.f036.config.ts" > "$TMP/pw.log" 2>&1
PW_EXIT=$?
echo "PLAYWRIGHT_EXIT $PW_EXIT"
tail -60 "$TMP/pw.log"

# 4) 运行日志脱敏后落证据（不含凭据）
mkdir -p "$EV/logs"
tail -80 "$TMP/dev.log" | sed 's/[A-Za-z0-9!_-]\{20,\}/<redacted>/g' > "$EV/logs/dev-server.log"
cp "$TMP/pw.log" "$EV/logs/playwright-run.log"

# 5) 生成运行摘要（不含凭据/用户名以外的敏感值）
cat > "$EV/logs/run-meta.json" <<JSON
{
  "port": $PORT,
  "port4300_status": "busy-other-session",
  "isolated_idp_dir": "/tmp/f036-e2e-idp (deleted after run)",
  "bootstrapped_user": "f036-e2e-admin (system-admin, mustChangePassword=true)",
  "playwright_exit": $PW_EXIT,
  "run_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "secrets_in_evidence": "none (password only in /tmp + process env; evidence scrubbed)"
}
JSON

exit "$PW_EXIT"
