#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${FRONTMATTER_PIPELINE_PYTHON:-python3}"
CHECK_TOOL="$ROOT/tools/kds-sync/check_frontmatter_gate.py"
BASE_REF="${FRONTMATTER_GATE_BASE_REF:-HEAD}"
LOCK_FILE="$ROOT/.kds/frontmatter-pipeline.lock"
PIPELINE_STARTED_AT=$(date +%s)
EMIT_CLOSURE=0
DOCUMENT_CONTROL_STATUS="skipped"
LOOP_GATE_STATUS="skipped"
FRONTMATTER_GATE_STATUS="skipped"
PROJECT_GROUP_GATE_STATUS="not_run"
LOOP_MAINLINE_CONTROL_STATUS="not_run"

BUILD_COMMANDS=()
VALIDATE_COMMANDS=(
  "python3 tools/kds-sync/check_document_pollution.py"
  "python3 tools/kds-sync/validate_loop_governance_docs.py"
  "python3 tools/kds-sync/validate_loop_project_group_gate_readiness.py"
  "python3 tools/kds-sync/validate_loop_session_mainline_control.py"
)
PROFILE=""
CHECK_ONLY=0
SKIP_DOC_CONTROL=0
SKIP_LOOP_GATE=0
SKIP_GATE_CHECK=0
DRY_GATE=0

usage() {
  cat <<'USAGE'
Usage:
  run_frontmatter_pipeline.sh [options]

Options:
  --build-cmd "cmd"            append evidence build/run command (can repeat)
  --validate-cmd "cmd"         append read-only validate command (can repeat)
  --profile <name>              use a predefined build/run profile
  --list-profiles               list supported profile names
  --check-only                  loop_document_gate run in read-only mode
  --skip-doc-control            skip document_control stage
  --skip-loop-gate              skip loop_document_gate stage
  --skip-gate-check             skip final frontmatter ownership gate
  --dry-gate                    only run frontmatter ownership gate check
  --emit-closure                print compact closure report block
  --help                        show help

Profiles:
  base_knowledge
  headroom_lcx
  headroom_full

Examples:
  ./run_frontmatter_pipeline.sh \
    --profile base_knowledge \
    --build-cmd "python3 tools/kds-sync/validate_loop_codegraph_goal_optimization.py"

  ./run_frontmatter_pipeline.sh --check-only --profile headroom_lcx

  # Diagnose current allowed frontmatter write paths before running
  python3 tools/kds-sync/check_frontmatter_gate.py --emit-protected-paths

  # Pipeline check mode: auto passthrough check-only for headroom run_* tasks
  ./run_frontmatter_pipeline.sh --check-only --profile headroom_full --emit-closure

  # Reproduce gate allowlist quickly
  ./run_frontmatter_pipeline.sh --check-only --skip-doc-control --skip-loop-gate

  # Run only gate check (no write/validation commands)
  ./run_frontmatter_pipeline.sh --dry-gate

  # Same gate-only check, with profile name for context alignment
  ./run_frontmatter_pipeline.sh --dry-gate --profile headroom_full
USAGE
}

list_profiles() {
  cat <<'PROFILES'
Available profiles:
  base_knowledge
    build_headroom_lcx_project_group_sanitized_fixture.py
    build_headroom_lcx_fixture_extension_negative_gate.py
    build_headroom_lcx_sanitized_token_fixture_extension.py
    build_headroom_lcx_readiness_pilot_authorization_package.py
    build_base_knowledge_blank_review_templates.py
    build_base_knowledge_closure_dry_run_evidence.py
    build_base_knowledge_queue_schema_dry_run.py
    build_base_knowledge_confirmation_queue_views.py
    validate_base_knowledge_closure_score_dry_run.py
    validate_localization_debt_base_knowledge_evidence_repair_d97.py

  headroom_lcx
    run_headroom_lcx_project_group_replay_stability.py
    run_headroom_lcx_l35_controlled_sanitized_pilot_window.py
    run_headroom_lcx_l35_multi_window_stability.py
    run_headroom_lcx_l35_answer_equivalence_synthetic_gate.py
    run_headroom_lcx_fixture_extension_replay_comparison.py
    run_headroom_lcx_marker_retrieval_miss_comparison_gate.py
    run_headroom_lcx_fixture_stability_gate.py
    validate_headroom_lcx_project_group_replay_stability.py
    validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py
    validate_headroom_lcx_l35_multi_window_stability.py
    validate_headroom_lcx_l35_answer_equivalence_synthetic_gate.py
    validate_headroom_lcx_fixture_extension_replay_comparison.py
    validate_headroom_lcx_marker_retrieval_miss_comparison_gate.py
    validate_headroom_lcx_fixture_stability_gate.py

  headroom_full
    union of base_knowledge + headroom_lcx
PROFILES
}

append_profile_commands() {
  local profile="$1"
  local scripts

  case "$profile" in
    base_knowledge)
      scripts=(
        "build_headroom_lcx_project_group_sanitized_fixture.py"
        "build_headroom_lcx_fixture_extension_negative_gate.py"
        "build_headroom_lcx_sanitized_token_fixture_extension.py"
        "build_headroom_lcx_readiness_pilot_authorization_package.py"
        "build_base_knowledge_blank_review_templates.py"
        "build_base_knowledge_closure_dry_run_evidence.py"
        "build_base_knowledge_queue_schema_dry_run.py"
        "build_base_knowledge_confirmation_queue_views.py"
      )
      ;;
    headroom_lcx)
      scripts=(
        "run_headroom_lcx_project_group_replay_stability.py"
        "run_headroom_lcx_l35_controlled_sanitized_pilot_window.py"
        "run_headroom_lcx_l35_multi_window_stability.py"
        "run_headroom_lcx_l35_answer_equivalence_synthetic_gate.py"
        "run_headroom_lcx_fixture_extension_replay_comparison.py"
        "run_headroom_lcx_marker_retrieval_miss_comparison_gate.py"
        "run_headroom_lcx_fixture_stability_gate.py"
      )
      ;;
    headroom_full)
      append_profile_commands base_knowledge
      append_profile_commands headroom_lcx
      return
      ;;
    *)
      echo "Unknown profile: $profile" >&2
      echo "Use --list-profiles to view supported profiles." >&2
      exit 1
      ;;
  esac

  local s
  for s in "${scripts[@]}"; do
    BUILD_COMMANDS+=("python3 tools/kds-sync/$s")
  done
}

append_profile_validate_commands() {
  local profile="$1"
  local scripts

  case "$profile" in
    base_knowledge)
      scripts=(
        "validate_base_knowledge_closure_score_dry_run.py"
        "validate_localization_debt_base_knowledge_evidence_repair_d97.py"
      )
      ;;
    headroom_lcx)
      scripts=(
        "validate_headroom_lcx_project_group_replay_stability.py"
        "validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py"
        "validate_headroom_lcx_l35_multi_window_stability.py"
        "validate_headroom_lcx_l35_answer_equivalence_synthetic_gate.py"
        "validate_headroom_lcx_fixture_extension_replay_comparison.py"
        "validate_headroom_lcx_marker_retrieval_miss_comparison_gate.py"
        "validate_headroom_lcx_fixture_stability_gate.py"
      )
      ;;
    headroom_full)
      append_profile_validate_commands base_knowledge
      append_profile_validate_commands headroom_lcx
      return
      ;;
    *)
      echo "Unknown profile: $profile" >&2
      echo "Use --list-profiles to view supported profiles." >&2
      exit 1
      ;;
  esac

  local s
  for s in "${scripts[@]}"; do
    VALIDATE_COMMANDS+=("python3 tools/kds-sync/$s")
  done
}

acquire_lock() {
  mkdir -p "$ROOT/.kds"
  if command -v flock >/dev/null 2>&1; then
    exec 200>"$LOCK_FILE"
    if ! flock -n 200; then
      echo "frontmatter pipeline is already running." >&2
      exit 1
    fi
    return
  fi
  if [[ -e "$LOCK_FILE.running" ]]; then
    echo "frontmatter pipeline lock exists: $LOCK_FILE.running" >&2
    exit 1
  fi
  echo "$$" > "$LOCK_FILE.running"
  trap 'rm -f "$LOCK_FILE.running"' EXIT
}

run_step() {
  local label="$1"
  local cmd="$2"
  local started

  started=$(date +%s)
  echo "[START] $label"
  if (cd "$ROOT" && bash -lc "$cmd"); then
    local cost=$(( $(date +%s) - started ))
    echo "[OK] $label (${cost}s)"
  else
    local code=$?
    echo "[FAIL] $label" >&2
    case "$label" in
      document_control)
        DOCUMENT_CONTROL_STATUS="fail"
        ;;
      loop_document_gate*)
        LOOP_GATE_STATUS="fail"
        ;;
    esac
    case "$cmd" in
      *validate_loop_project_group_gate_readiness.py)
        PROJECT_GROUP_GATE_STATUS="fail"
        ;;
      *validate_loop_session_mainline_control.py)
        LOOP_MAINLINE_CONTROL_STATUS="fail"
        ;;
    esac
    if [[ "$EMIT_CLOSURE" -eq 1 ]]; then
      emit_closure_report fail
    fi
    exit "$code"
  fi
}

load_gate_allowed_frontmatter_paths() {
  local -a paths=()
  local path
  while IFS= read -r path; do
    if [[ -n "$path" ]]; then
      paths+=("$path")
    fi
  done < <("$PYTHON" "$CHECK_TOOL" --emit-protected-paths)

  if (( ${#paths[@]} == 0 )); then
    paths=(
      "09-status/globalcloud-document-control-register.md"
      "09-status/kds-development-space-sync-register.md"
      "09-status/document-deprecation-register.md"
      "09-status/globalcloud-document-health-report.md"
      ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-control-register.md"
      ".kds/development-space/开发/91-治理与验收/09-status/kds-development-space-sync-register.md"
      ".kds/development-space/开发/91-治理与验收/09-status/document-deprecation-register.md"
      ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md"
    )
  fi

  printf '%s\n' "${paths[@]}"
}

run_gate_check() {
  if [[ "$SKIP_GATE_CHECK" -eq 1 ]]; then
    FRONTMATTER_GATE_STATUS="skipped"
    return
  fi
  local -a allowed=()
  local allowed_args=()
  local pattern
  while IFS= read -r pattern; do
    allowed+=("$pattern")
  done < <(load_gate_allowed_frontmatter_paths)
  for pattern in "${allowed[@]}"; do
    allowed_args+=("--allowed-frontmatter-write" "$pattern")
  done

  echo "[GATE] allowed frontmatter write patterns (${#allowed[@]}):"
  for pattern in "${allowed[@]}"; do
    echo "  - $pattern"
  done

  if (cd "$ROOT" && "$PYTHON" "$CHECK_TOOL" --base-ref "$BASE_REF" "${allowed_args[@]}"); then
    FRONTMATTER_GATE_STATUS="pass"
    return 0
  fi

  FRONTMATTER_GATE_STATUS="fail"
  return 1
}

maybe_add_check_only_arg() {
  local cmd="$1"
  if [[ "$CHECK_ONLY" -eq 0 ]]; then
    printf '%s\n' "$cmd"
    return
  fi
  if [[ "$cmd" == *"--check-only"* ]]; then
    printf '%s\n' "$cmd"
    return
  fi
  if [[ "$cmd" == *"tools/kds-sync/build_"* || "$cmd" == *"tools/kds-sync/run_"* ]]; then
    printf '%s --check-only\n' "$cmd"
    return
  fi
  printf '%s\n' "$cmd"
}

emit_closure_report() {
  local status="$1"
  local ended_at
  local elapsed
  local pipeline_started_at
  local mode
  local document_control_count=0
  local loop_document_gate_count=0
  local frontmatter_gate_count=0
  local project_group_count=0
  local loop_mainline_count=0

  ended_at=$(date +%s)
  elapsed=$(( ended_at - PIPELINE_STARTED_AT ))
  if ! pipeline_started_at=$(date -r "$PIPELINE_STARTED_AT" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null); then
    pipeline_started_at=$(date -d "@$PIPELINE_STARTED_AT" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo "$PIPELINE_STARTED_AT")
  fi

  if [[ "$DRY_GATE" -eq 1 ]]; then
    mode="gate_check"
  else
    mode="check"
  fi

  local profile_name="${PROFILE:-manual}"
  local build_count="${#BUILD_COMMANDS[@]}"
  local validate_count="${#VALIDATE_COMMANDS[@]}"

  if [[ "$DOCUMENT_CONTROL_STATUS" == pass || "$DOCUMENT_CONTROL_STATUS" == skipped ]]; then
    document_control_count=1
  fi
  if [[ "$LOOP_GATE_STATUS" == pass || "$LOOP_GATE_STATUS" == skipped ]]; then
    loop_document_gate_count=1
  fi
  if [[ "$FRONTMATTER_GATE_STATUS" == pass || "$FRONTMATTER_GATE_STATUS" == fail || "$FRONTMATTER_GATE_STATUS" == skipped ]]; then
    frontmatter_gate_count=1
  fi
  if [[ "$PROJECT_GROUP_GATE_STATUS" == pass || "$PROJECT_GROUP_GATE_STATUS" == fail ]]; then
    project_group_count=1
  fi
  if [[ "$LOOP_MAINLINE_CONTROL_STATUS" == pass || "$LOOP_MAINLINE_CONTROL_STATUS" == fail ]]; then
    loop_mainline_count=1
  fi

  echo "[CLOSURE] status=$status context=$profile_name mode=$mode pipeline_started_at=$pipeline_started_at started_path=$ROOT"
  echo "[CLOSURE] stage=document_control=$DOCUMENT_CONTROL_STATUS loop_document_gate=$LOOP_GATE_STATUS frontmatter_gate=$FRONTMATTER_GATE_STATUS project_group_gate=$PROJECT_GROUP_GATE_STATUS loop_mainline_control=$LOOP_MAINLINE_CONTROL_STATUS"
  echo "[CLOSURE] counts=document_control=$document_control_count loop_document_gate=$loop_document_gate_count frontmatter_gate=$frontmatter_gate_count project_group=$project_group_count loop_mainline=$loop_mainline_count"
  echo "[CLOSURE] metrics elapsed_s=${elapsed} build_count=$build_count validate_count=$validate_count"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build-cmd)
      BUILD_COMMANDS+=("$2")
      shift 2
      ;;
    --validate-cmd)
      VALIDATE_COMMANDS+=("$2")
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --list-profiles)
      list_profiles
      exit 0
      ;;
    --check-only)
      CHECK_ONLY=1
      shift
      ;;
    --skip-doc-control)
      SKIP_DOC_CONTROL=1
      shift
      ;;
    --skip-loop-gate)
      SKIP_LOOP_GATE=1
      shift
      ;;
    --skip-gate-check)
      SKIP_GATE_CHECK=1
      shift
      ;;
    --dry-gate)
      DRY_GATE=1
      SKIP_DOC_CONTROL=1
      SKIP_LOOP_GATE=1
      shift
      ;;
    --emit-closure)
      EMIT_CLOSURE=1
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$PROFILE" && -n "${FRONTMATTER_PIPELINE_PROFILE:-}" ]]; then
  PROFILE="$FRONTMATTER_PIPELINE_PROFILE"
fi
if [[ -n "$PROFILE" && "$DRY_GATE" -eq 0 ]]; then
  append_profile_commands "$PROFILE"
  append_profile_validate_commands "$PROFILE"
fi

if [[ "$DRY_GATE" -eq 1 ]]; then
  echo "[DRY] frontmatter gate-only mode"
  acquire_lock
  if run_gate_check; then
    [[ "$EMIT_CLOSURE" -eq 1 ]] && emit_closure_report pass
    exit 0
  fi
  [[ "$EMIT_CLOSURE" -eq 1 ]] && emit_closure_report fail
  exit 1
fi

acquire_lock

if [[ "$SKIP_DOC_CONTROL" -eq 0 ]]; then
  DOCUMENT_CONTROL_STATUS="running"
  run_step "document_control" "$PYTHON tools/kds-sync/document_control.py"
  DOCUMENT_CONTROL_STATUS="pass"
else
  echo "[SKIP] document_control"
fi

if [[ "$SKIP_LOOP_GATE" -eq 0 ]]; then
  LOOP_GATE_STATUS="running"
  if [[ "$CHECK_ONLY" -eq 1 ]]; then
    run_step "loop_document_gate(check-only)" "$PYTHON tools/kds-sync/loop_document_gate.py --check-only"
  else
    run_step "loop_document_gate" "$PYTHON tools/kds-sync/loop_document_gate.py"
  fi
  LOOP_GATE_STATUS="pass"
else
  echo "[SKIP] loop_document_gate"
fi

if (( ${#BUILD_COMMANDS[@]} > 0 )); then
  BUILD_INDEX=1
  for cmd in "${BUILD_COMMANDS[@]}"; do
    run_step "build/run[${BUILD_INDEX}/${#BUILD_COMMANDS[@]}]" "$(maybe_add_check_only_arg "$cmd")"
    BUILD_INDEX=$(( BUILD_INDEX + 1 ))
  done
else
  echo "[SKIP] build/run evidence stage (no --build-cmd or profile provided)"
fi

if (( ${#VALIDATE_COMMANDS[@]} > 0 )); then
  VALIDATE_INDEX=1
  for cmd in "${VALIDATE_COMMANDS[@]}"; do
    run_step "validate[${VALIDATE_INDEX}/${#VALIDATE_COMMANDS[@]}]" "$cmd"
    case "$cmd" in
      *validate_loop_project_group_gate_readiness.py)
        PROJECT_GROUP_GATE_STATUS="pass"
        ;;
      *validate_loop_session_mainline_control.py)
        LOOP_MAINLINE_CONTROL_STATUS="pass"
        ;;
    esac
    VALIDATE_INDEX=$(( VALIDATE_INDEX + 1 ))
  done
else
  echo "[SKIP] validate stage"
fi

if run_gate_check; then
  if [[ "$EMIT_CLOSURE" -eq 1 ]]; then
    emit_closure_report pass
  fi
  exit 0
fi
[[ "$EMIT_CLOSURE" -eq 1 ]] && emit_closure_report fail
exit 1
