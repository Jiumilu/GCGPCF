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
run 13-e2e-a11y 600 pnpm e2e:a11y
run 14-e2e-visual 600 pnpm e2e:visual
run 15-e2e-machine-fields 600 pnpm e2e:machine-fields
run 16-e2e-pkc-states 600 pnpm e2e:pkc-states
run 17-check-tokens-registry 300 pnpm check:tokens-parity:registry
run 18-e2e-pixel 900 pnpm e2e:pixel --compare
run 19-e2e-panel-layout 900 pnpm e2e:panel-layout
run 20-m3-b5-visual 900 pnpm e2e:m3-b5-visual
echo "DONE"
