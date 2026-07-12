#!/usr/bin/env python3
"""Evaluate the Loop document governance gate and optionally write a health report."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "09-status/globalcloud-document-health-report.md"
MIRROR_REPORT = ROOT / ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md"
GFIS_REAL_FACT_ENTRY_GATE_CACHE = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT", "")
DELEGATED_PROJECT_ROOT = os.environ.get("GPCF_DELEGATED_PROJECT_ROOT", "")


def run(command: list[str]) -> tuple[int, str]:
    env = os.environ.copy()
    env["GPCF_LOOP_DOCUMENT_GATE_ACTIVE"] = "1"
    if GFIS_REAL_FACT_ENTRY_GATE_CACHE:
        env["GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT"] = GFIS_REAL_FACT_ENTRY_GATE_CACHE
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env)
    return result.returncode, (result.stdout + result.stderr).strip()


def run_with_retry(command: list[str], retries: int = 1) -> tuple[int, str]:
    code, output = run(command)
    attempts = [f"attempt=1 code={code} output={output}"]
    for attempt in range(2, retries + 2):
        if code == 0:
            break
        code, output = run(command)
        attempts.append(f"attempt={attempt} code={code} output={output}")
    return code, "\n".join(attempts)


def run_delegated_project_localization() -> tuple[int, str]:
    if not DELEGATED_PROJECT_ROOT:
        return 0, "delegated_project_localization=not_requested"
    project_root = Path(DELEGATED_PROJECT_ROOT).resolve()
    if project_root.parent != ROOT.parent or not project_root.is_dir():
        return 1, f"invalid delegated project root: {project_root}"
    gate = project_root / "scripts/validate_chinese_document_gate.py"
    if not gate.is_file():
        return 1, f"missing delegated Chinese document gate: {gate}"
    result = subprocess.run(
        [sys.executable, str(gate)],
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def iter_repo_md() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or ".kds" in path.parts or ".zcode" in path.parts:
            continue
        paths.append(path)
    return sorted(paths)


def frontmatter_managed_for(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(".okf/bundles/"):
        return False
    if rel.startswith((".codex/", ".agents/")):
        return False
    if rel.startswith(".codex/skills/") and path.name == "SKILL.md":
        return False
    return True


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def is_okf_bundle_doc(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith(".okf/bundles/")


def readme_exempt_dir(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel == "loops" or rel.startswith(("projects/", "features/"))


def count_unique_mirror_docs(path: Path) -> int:
    if not path.exists():
        return 0
    unique_paths: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("status") != "mirrored":
            continue
        kds_path = entry.get("kds_path")
        if isinstance(kds_path, str) and kds_path:
            unique_paths.add(kds_path)
    return len(unique_paths)


def build_gate_reasons(
    *,
    missing_metadata: int,
    missing_readme_dirs: int,
    hard_failures: list[str],
    localization_debt: bool,
    token_blocked: bool,
    fixed_doc_id_drift: bool,
    kds_md: int,
    local_mirror_unique_docs: int,
) -> list[str]:
    reasons: list[str] = []
    if missing_metadata:
        reasons.append("missing_metadata")
    if missing_readme_dirs:
        reasons.append("missing_readme_dirs")
    reasons.extend(f"hard_failure:{name}" for name in hard_failures)
    if localization_debt:
        reasons.append("localization_debt")
    if token_blocked:
        reasons.append("kds_token_blocked")
    if fixed_doc_id_drift:
        reasons.append("fixed_doc_id_drift")
    if kds_md < local_mirror_unique_docs:
        reasons.append("kds_mirror_coverage_gap")
    return reasons


def write_report(summary: dict[str, object], command_results: dict[str, str]) -> None:
    status_counts = summary["status_counts"]
    project_counts = summary["project_counts"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-C436DDB0F6",
        "title: GlobalCloud 文档健康报告",
        "project: GPCF",
        "related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/globalcloud-document-health-report.md",
        "source_path: 09-status/globalcloud-document-health-report.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-12",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GlobalCloud 文档健康报告",
        "",
        "本报告用于记录项目群文档门禁、镜像覆盖、状态分布和命令证据的当前健康状态。"
        "文中的英文项目名、脚本名、字段名和命令输出均为机器可回放证据，"
        "不代表业务事实完成、状态升级、客户验收、生产发布或真实外部写入。"
        "当前报告只作为受控治理快照，所有 accepted、integrated、production_ready、"
        "customer_accepted 等状态仍必须等待人工确认、真实 source-of-record 或等效正式确认文件、"
        "人工业务核验、运行层主键、review queue、runtime intake、WAES review 和 verified artifact "
        "全部满足后才能重新评估。",
        "",
        f"生成时间：{datetime.now(timezone.utc).isoformat()}",
        "",
        f"Loop 文档门禁：`{summary['gate']}`",
        "",
        "## 总览",
        "",
        f"- 仓库 Markdown：{summary['repo_md']}",
        f"- KDS 镜像 Markdown：{summary['kds_md']}",
        f"- KDS 本地镜像流水：{summary['local_mirror_ledger_lines']}",
        f"- KDS 本地镜像唯一文档：{summary['local_mirror_unique_docs']}",
        f"- KDS API 同步流水：{summary['api_sync_ledger_lines']}",
        f"- 元数据缺失：{summary['missing_metadata']}",
        f"- README 缺失目录：{summary['missing_readme_dirs']}",
        f"- 中文本地化债务：{summary['localization_debt']}",
        f"- 固定 doc_id 漂移：{summary['fixed_doc_id_drift']}",
        f"- 门禁原因：{', '.join(summary['gate_reasons']) if summary['gate_reasons'] else '无'}",
        "",
        "## 状态分布",
        "",
    ]
    for key, value in sorted(status_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 项目分布", ""])
    for key, value in sorted(project_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 命令结果", ""])
    for name, output in command_results.items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append("```text")
        lines.append(output or "(no output)")
        lines.append("```")
        lines.append("")
    content = "\n".join(lines)
    REPORT.write_text(content, encoding="utf-8")
    MIRROR_REPORT.parent.mkdir(parents=True, exist_ok=True)
    MIRROR_REPORT.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-only",
        action="store_true",
        dest="check_only",
        help="evaluate the gate without writing the health report or KDS mirror",
    )
    parser.add_argument(
        "--no-write-report",
        action="store_true",
        dest="check_only",
        help="deprecated alias for --check-only",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="explicitly write the health report and KDS mirror after evaluation",
    )
    args = parser.parse_args()
    if args.check_only and args.write_report:
        parser.error("--check-only and --write-report cannot be used together")
    if args.check_only and os.environ.get("GPCF_LOOP_DOCUMENT_GATE_ACTIVE") == "1":
        print(
            json.dumps(
                {
                    "gate": "pass",
                    "gate_reasons": [],
                    "delegated_nested_loop_document_gate": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    docs = iter_repo_md()
    missing_metadata = 0
    status_counts: Counter[str] = Counter()
    project_counts: Counter[str] = Counter()
    for path in docs:
        rel = path.relative_to(ROOT).as_posix()
        if (rel.startswith(".codex/skills/") or rel.startswith(".agents/skills/")) and path.name == "SKILL.md":
            continue
        if is_okf_bundle_doc(path):
            status_counts["okf_derived"] += 1
            project_counts["KDS"] += 1
            continue
        if not frontmatter_managed_for(path):
            continue
        fm = read_frontmatter(path)
        if not fm.get("doc_id"):
            missing_metadata += 1
        status_counts[fm.get("status", "missing")] += 1
        project_counts[fm.get("project", "missing")] += 1
    missing_readme_dirs = 0
    for directory in {path.parent for path in docs}:
        if directory == ROOT:
            continue
        if directory.relative_to(ROOT).as_posix().startswith(".okf/bundles/"):
            continue
        if readme_exempt_dir(directory):
            continue
        if not (directory / "README.md").exists():
            missing_readme_dirs += 1
    kds_md = len(list((ROOT / ".kds/development-space/开发").rglob("*.md"))) if (ROOT / ".kds/development-space/开发").exists() else 0
    local_mirror_ledger = ROOT / ".kds/local-mirror-ledger.jsonl"
    local_mirror_ledger_lines = len(local_mirror_ledger.read_text(encoding="utf-8").splitlines()) if local_mirror_ledger.exists() else 0
    local_mirror_unique_docs = count_unique_mirror_docs(local_mirror_ledger)
    api_sync_ledger = ROOT / ".kds/sync-ledger.jsonl"
    api_sync_ledger_lines = len(api_sync_ledger.read_text(encoding="utf-8").splitlines()) if api_sync_ledger.exists() else 0
    delegated = os.environ.get("GPCF_PROJECT_GROUP_GATE_DELEGATED") == "1"
    global GFIS_REAL_FACT_ENTRY_GATE_CACHE
    gfis_real_fact_entry_gate = run([sys.executable, "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"])
    if gfis_real_fact_entry_gate[0] == 0:
        GFIS_REAL_FACT_ENTRY_GATE_CACHE = gfis_real_fact_entry_gate[1]

    project_group_live_status_current = run([sys.executable, "tools/kds-sync/build_project_group_live_status_current.py"])

    delegated_project_localization = run_delegated_project_localization()
    checks = {
        "project_group_live_status_current": project_group_live_status_current,
        "loop_engineering_five_direction": run([sys.executable, "tools/kds-sync/validate_loop_engineering_five_direction_implementation.py"]),
        "loop_v11_slimming_delivery_recovery": run([sys.executable, "tools/kds-sync/validate_loop_v11_slimming_delivery_recovery.py"]),
        "loop_engineering_master_plan": run([sys.executable, "tools/kds-sync/validate_loop_engineering_master_plan.py"]),
        "loop_optional_commentary_policy": run([sys.executable, "tools/kds-sync/validate_loop_optional_commentary_policy.py"]),
        "loop_capability_registry": run([sys.executable, "tools/kds-sync/validate_loop_capability_registry.py"]),
        "codegraph_loop_schema": run([sys.executable, "tools/kds-sync/validate_codegraph_loop_schema.py"]),
        "loop_ui_quality_baseline": run([sys.executable, "tools/kds-sync/validate_loop_ui_quality_baseline.py"]),
        "loop_delivery_efficiency_control": run([sys.executable, "tools/kds-sync/validate_loop_delivery_efficiency_control.py"]),
        "gpcf_2_feature_workspace": run([sys.executable, "tools/kds-sync/validate_gpcf_2_feature_workspace.py"]),
        "icp_project_registration": run([sys.executable, "tools/kds-sync/validate_icp_project_registration.py"]),
        "constitution_g00_inheritance": run([sys.executable, "tools/kds-sync/validate_constitution_inheritance_gate.py"]),
        "loop_ui_product_first_control": run([sys.executable, "tools/kds-sync/validate_loop_ui_product_first_control.py"]),
        "loop_session_mainline_control": run([sys.executable, "tools/kds-sync/validate_loop_session_mainline_control.py"]),
        "current_session_mainline_declaration": run([sys.executable, "tools/kds-sync/validate_current_session_mainline_declaration.py"]),
        "loop_session_registry": run([sys.executable, "tools/kds-sync/validate_loop_session_registry.py"]),
        "session_mainline_preflight_enforcement": run([sys.executable, "tools/kds-sync/validate_session_mainline_preflight_enforcement.py"]),
        "session_mainline_drift_watch": run([sys.executable, "tools/kds-sync/validate_session_mainline_drift_watch.py"]),
        "session_mainline_handoff_request_gate": run([sys.executable, "tools/kds-sync/validate_session_mainline_handoff_request_gate.py"]),
        "gfis_real_fact_entry_gate": gfis_real_fact_entry_gate,
        "gfis_real_fact_entry_coverage": run([sys.executable, "tools/kds-sync/validate_gfis_real_fact_entry_coverage.py"]),
        "gfis_real_fact_no_status_promotion": run([sys.executable, "tools/kds-sync/validate_gfis_real_fact_no_status_promotion.py"]),
        "loop_document_gate_gfis_coverage": run([sys.executable, "tools/kds-sync/validate_loop_document_gate_gfis_coverage.py"]),
        "project_group_external_loop_gate_delegates": run([sys.executable, "tools/kds-sync/validate_project_group_external_loop_gate_delegates.py"]),
        "gpcf_project_status_matrix_17_project_scope": run([sys.executable, "tools/kds-sync/validate_gpcf_project_status_matrix_17_project_scope.py"]),
        "project_group_status_control_surface_17_scope": run([sys.executable, "tools/kds-sync/validate_project_group_status_control_surface_17_scope.py"]),
        "project_group_full_project_baseline": run([sys.executable, "tools/kds-sync/validate_project_group_full_project_baseline.py"]),
        "project_group_current_state_baseline_refresh": run([sys.executable, "tools/kds-sync/validate_project_group_current_state_baseline_refresh_20260626.py"]),
        "project_group_dev_task_queue": run([sys.executable, "tools/kds-sync/validate_project_group_dev_task_queue_20260626.py"]),
        "project_group_real_execution_metadata_coverage": run([sys.executable, "tools/kds-sync/validate_project_group_real_execution_metadata_coverage_20260626.py"]),
        "project_group_live_status_snapshot": run([sys.executable, "tools/kds-sync/validate_project_group_live_status_snapshot_20260626.py"]),
        "project_group_real_execution_governance_board": run([sys.executable, "tools/kds-sync/validate_project_group_real_execution_governance_board.py"]),
        "project_group_status_advancement_matrix": run([sys.executable, "tools/kds-sync/validate_project_group_status_advancement_matrix.py"]),
        "project_group_ready_for_review_advancement_queue": run([sys.executable, "tools/kds-sync/validate_project_group_ready_for_review_advancement_queue_20260626.py"]),
        "project_group_authorization_pre_execution_command_pack": run([sys.executable, "tools/kds-sync/validate_project_group_authorization_pre_execution_command_pack_20260626.py"]),
        "project_group_authorization_pre_execution_environment_readiness": run([sys.executable, "tools/kds-sync/validate_project_group_authorization_pre_execution_environment_readiness_20260626.py"]),
        "project_group_delivery_readiness": run([sys.executable, "tools/kds-sync/validate_project_group_delivery_readiness.py"]),
        "project_runtime_readiness": run([sys.executable, "tools/kds-sync/validate_project_runtime_readiness.py"]),
        "project_integration_readiness": run([sys.executable, "tools/kds-sync/validate_project_integration_readiness.py"]),
        "customer_acceptance_readiness": run([sys.executable, "tools/kds-sync/validate_customer_acceptance_readiness.py"]),
        "document_pollution": run([sys.executable, "tools/kds-sync/check_document_pollution.py"]),
        "fixed_doc_id_preservation": run([sys.executable, "scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py"]),
        "chinese_localization": run([sys.executable, "tools/kds-sync/check_chinese_localization_gate.py"]),
        "delegated_project_chinese_localization": delegated_project_localization,
        "kds_token": run([sys.executable, "tools/kds-sync/validate_kds_token.py"]),
    }
    if not delegated:
        checks["project_group_gate_readiness"] = run_with_retry(
            [sys.executable, "tools/kds-sync/validate_loop_project_group_gate_readiness.py"],
            retries=1,
        )
    hard_failures = [
        name
        for name, (code, _) in checks.items()
        if code != 0 and name not in {"kds_token", "chinese_localization", "delegated_project_chinese_localization"}
    ]
    token_blocked = checks["kds_token"][0] != 0
    fixed_doc_id_drift = checks["fixed_doc_id_preservation"][0] != 0
    localization_debt = (
        checks["chinese_localization"][0] != 0
        or checks["delegated_project_chinese_localization"][0] != 0
    )
    if missing_metadata or missing_readme_dirs or hard_failures or localization_debt:
        gate = "rework_required"
    elif token_blocked:
        gate = "blocked"
    elif kds_md < local_mirror_unique_docs:
        gate = "partial"
    else:
        gate = "pass"
    gate_reasons = build_gate_reasons(
        missing_metadata=missing_metadata,
        missing_readme_dirs=missing_readme_dirs,
        hard_failures=hard_failures,
        localization_debt=localization_debt,
        token_blocked=token_blocked,
        fixed_doc_id_drift=fixed_doc_id_drift,
        kds_md=kds_md,
        local_mirror_unique_docs=local_mirror_unique_docs,
    )
    summary = {
        "gate": gate,
        "gate_reasons": gate_reasons,
        "repo_md": len(docs),
        "kds_md": kds_md,
        "local_mirror_ledger_lines": local_mirror_ledger_lines,
        "local_mirror_unique_docs": local_mirror_unique_docs,
        "api_sync_ledger_lines": api_sync_ledger_lines,
        "missing_metadata": missing_metadata,
        "missing_readme_dirs": missing_readme_dirs,
        "localization_debt": localization_debt,
        "fixed_doc_id_drift": fixed_doc_id_drift,
        "status_counts": dict(status_counts),
        "project_counts": dict(project_counts),
    }
    command_results = {name: output for name, (_, output) in checks.items()}
    if args.write_report:
        write_report(summary, command_results)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if gate == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
