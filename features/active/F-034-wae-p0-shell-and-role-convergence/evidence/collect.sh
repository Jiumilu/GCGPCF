#!/bin/bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAE"
L=docs/evidence/F-034/logs
run() { # run <id> <timeout> <command...>
  local id="$1"; shift; local t="$1"; shift
  echo "== $id =="
  timeout "$t" "$@" > "$L/$id.log" 2>&1
  echo "$?" > "$L/$id.exit"
  echo "   exit=$(cat "$L/$id.exit")  → $L/$id.log"
}
run 01-test-framework 1200 pnpm test
run 02-typecheck 600 pnpm typecheck
run 03-wame-vitest 900 pnpm --dir apps/wame exec vitest run
run 04-wame-build 600 pnpm --dir apps/wame exec vite build
run 05-e2e-dual-role 600 pnpm e2e:dual-role
run 06-e2e-pkc-intake 600 pnpm e2e:pkc-intake
run 07-check-apps 300 pnpm check:apps
run 08-gen-apps-check 300 pnpm gen:apps --check
run 09-check-app-assembly 300 pnpm check:app-assembly
run 10-check-registry 300 pnpm check:registry
run 11-check-tokens-parity 300 pnpm check:tokens-parity
run 12-build-packages 600 pnpm build:packages
echo "DONE"
