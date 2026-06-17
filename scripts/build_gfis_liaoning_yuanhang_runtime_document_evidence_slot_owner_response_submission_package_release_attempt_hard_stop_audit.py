#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "docs/harness/sop-e2e/evidence/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-quarantine-scanner.json"
OUTPUT_JSON_PATH = ROOT / "docs/harness/sop-e2e/evidence/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-release-attempt-hard-stop-audit.json"
OUTPUT_MD_PATH = ROOT / "docs/harness/sop-e2e/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-release-attempt-hard-stop-audit.md"

BLOCKERS = [
    "submission_package_missing",
    "submission_package_structure_not_valid",
    "source_of_record_live_proof_missing",
    "manual_authorization_envelope_missing",
    "anti_pollution_declaration_missing",
    "quarantine_review_not_available",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value


def build_audit() -> dict[str, Any]:
    source = load_json(SOURCE_PATH)
    require(source.get("subject") == "GFIS运行层", "source subject must be GFIS runtime layer")
    require(source.get("round_id") == "GFIS-RUNTIME-SOP-E2E-161", "source round id mismatch")
    require(source.get("runtime_sop_e2e") == "repair_required", "source must preserve repair_required")
    require(
        source.get("state") == "owner_response_submission_package_quarantine_blocked_no_submission_packages",
        "source state mismatch",
    )
    require(source.get("runtime_objects") == 12, "source must cover 12 runtime objects")
    require(source.get("proof_slots") == 62, "source must cover 62 proof slots")
    require(source.get("expected_submission_packages") == 62, "source must expect 62 submission packages")
    require(source.get("submission_packages_found") == 0, "source must find zero submission packages")
    require(source.get("quarantine_candidates") == 0, "source must find zero quarantine candidates")

    scan_items = source.get("scan_items")
    require(isinstance(scan_items, list) and len(scan_items) == 62, "source must contain 62 scan items")

    audit_items: list[dict[str, Any]] = []
    for item in scan_items:
        require(isinstance(item, dict), "scan item must be object")
        require(item.get("submission_package_id"), "submission package id missing")
        require(item.get("object"), "runtime object missing")
        require(item.get("slot_id"), "slot id missing")
        require(item.get("submission_package_exists") is False, "source must not claim package exists")
        require(item.get("eligible_for_quarantine") is False, "source must not claim quarantine eligibility")
        audit_items.append(
            {
                "submission_package_id": item.get("submission_package_id"),
                "handoff_id": item.get("handoff_id"),
                "response_id": item.get("response_id"),
                "transition_id": item.get("transition_id"),
                "object": item.get("object"),
                "slot_id": item.get("slot_id"),
                "owner_project": item.get("owner_project"),
                "owner_role": item.get("owner_role"),
                "submission_package_file": item.get("submission_package_file"),
                "attempted_release": True,
                "attempted_review_queue": True,
                "attempted_runtime_intake": True,
                "attempted_waes_review": True,
                "hard_stop": True,
                "blocker_count": len(BLOCKERS),
                "blockers": BLOCKERS,
                "release_allowed": False,
                "review_queue_allowed": False,
                "runtime_intake_allowed": False,
                "waes_review_allowed": False,
                "verified_artifact_allowed": False,
                "state": "release_attempt_hard_stopped_no_submission_package",
            }
        )

    return {
        "audit_id": "GFIS-LIAONING-YUANHANG-RUNTIME-DOCUMENT-EVIDENCE-SLOT-OWNER-RESPONSE-SUBMISSION-PACKAGE-RELEASE-ATTEMPT-HARD-STOP-AUDIT-001",
        "round_id": "GFIS-RUNTIME-SOP-E2E-162",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": "GFIS运行层",
        "current_runtime_site": "modern_jinggong_oem_current",
        "future_runtime_site": "gehu_owned_factory_after_commissioning",
        "source_quarantine_scanner": str(SOURCE_PATH.relative_to(ROOT)),
        "source_quarantine_scanner_round_id": source.get("round_id"),
        "runtime_objects": 12,
        "proof_slots": 62,
        "expected_submission_packages": 62,
        "attempted_release_count": len(audit_items),
        "hard_stop_count": len(audit_items),
        "total_blocker_count": len(audit_items) * len(BLOCKERS),
        "submission_packages_found": source.get("submission_packages_found"),
        "structure_valid_submission_packages": source.get("structure_valid_submission_packages"),
        "quarantine_candidates": source.get("quarantine_candidates"),
        "quarantined_packages": source.get("quarantined_packages"),
        "accepted_packages": 0,
        "rejected_packages": 0,
        "release_allowed": 0,
        "review_queue": 0,
        "runtime_intake": 0,
        "waes_review": 0,
        "verified": 0,
        "runtime_sop_e2e": "repair_required",
        "state": "owner_response_submission_package_release_attempt_hard_stopped_no_submission_packages",
        "audit_items": audit_items,
        "external_runtime_boundary": {
            "ecs_or_aliyun_config_change": False,
            "caddy_or_nginx_change": False,
            "ssh_tunnel_change": False,
            "docker_or_compose_change": False,
            "systemd_or_launchd_change": False,
            "hermes_runtime_config_write_allowed": False,
            "codex_runtime_config_write_executed": False,
        },
        "guardrails": {
            "production_write": False,
            "real_external_api_write": False,
            "real_kds_write": False,
            "real_waes_write": False,
            "bench_migrate": False,
            "schema_sync": False,
            "permission_change": False,
            "accepted_integrated_claim": False,
            "demo_substitution": False,
            "contract_review_draft_substitution": False,
            "user_statement_as_live_proof": False,
            "kds_candidate_only_as_live_proof": False,
        },
        "next": "collect_real_owner_response_submission_packages_before_any_release_or_review_attempt",
    }


def render_markdown(audit: dict[str, Any]) -> str:
    rows = "\n".join(
        "| `{submission_package_id}` | `{object}` | `{slot_id}` | `{attempted_release}` | `{hard_stop}` | `{blocker_count}` | `{state}` |".format(**item)
        for item in audit["audit_items"]
    )
    return "\n".join(
        [
            "# 辽宁远航 GFIS 运行层 owner response 提交包 release attempt hard-stop audit",
            "",
            f"- audit_id: `{audit['audit_id']}`",
            f"- round_id: `{audit['round_id']}`",
            "- subject: GFIS 运行层",
            f"- current_runtime_site: `{audit['current_runtime_site']}`",
            f"- future_runtime_site: `{audit['future_runtime_site']}`",
            f"- expected_submission_packages: `{audit['expected_submission_packages']}`",
            f"- attempted_release_count: `{audit['attempted_release_count']}`",
            f"- hard_stop_count: `{audit['hard_stop_count']}`",
            f"- total_blocker_count: `{audit['total_blocker_count']}`",
            f"- submission_packages_found: `{audit['submission_packages_found']}`",
            f"- structure_valid_submission_packages: `{audit['structure_valid_submission_packages']}`",
            f"- quarantine_candidates: `{audit['quarantine_candidates']}`",
            f"- release_allowed: `{audit['release_allowed']}`",
            f"- review_queue: `{audit['review_queue']}`",
            f"- runtime_intake: `{audit['runtime_intake']}`",
            f"- waes_review: `{audit['waes_review']}`",
            f"- verified: `{audit['verified']}`",
            f"- runtime_sop_e2e: `{audit['runtime_sop_e2e']}`",
            "",
            "## Hard-stop 明细",
            "",
            "| submission_package_id | object | slot_id | attempted_release | hard_stop | blocker_count | state |",
            "|---|---|---|---|---|---:|---|",
            rows,
            "",
            "## Gate Rule",
            "",
            "- 现代精工 OEM 为当前 GFIS 运行层承载，葛化自建工厂投产后继续使用同一 GFIS 运行时系统。",
            "- 未发现真实 owner response submission package 时，任何 release、review queue、runtime intake 或 WAES review 尝试都必须 hard-stop。",
            "- GFIS Demo、合同审阅稿、KDS 候选、用户口述和 Loop 生成文件都不能替代 source-of-record live proof。",
            "- 本轮未修改 ECS、阿里云、Caddy/Nginx、SSH 隧道、Docker/Compose、systemd/launchd 或任何运行时配置；Hermes 仍为只读边界。",
            "- 不生产写入、不真实外部 API 写入、不真实 KDS/WAES 写入、不 bench migrate、不 schema sync、不权限变更、不 accepted/integrated。",
            "",
        ]
    )


def main() -> None:
    audit = build_audit()
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD_PATH.write_text(render_markdown(audit), encoding="utf-8")
    print(
        "liaoning_yuanhang_runtime_document_evidence_slot_owner_response_submission_package_release_attempt_hard_stop_audit=written "
        f"objects={audit['runtime_objects']} proof_slots={audit['proof_slots']} "
        f"expected_submission_packages={audit['expected_submission_packages']} "
        f"attempted_release={audit['attempted_release_count']} hard_stops={audit['hard_stop_count']} "
        f"blockers={audit['total_blocker_count']} submission_packages_found={audit['submission_packages_found']} "
        f"structure_valid_submission_packages={audit['structure_valid_submission_packages']} "
        f"quarantine_candidates={audit['quarantine_candidates']} release_allowed=0 review_queue=0 "
        f"runtime_intake=0 waes_review=0 verified=0 state={audit['state']} runtime_sop_e2e=repair_required"
    )


if __name__ == "__main__":
    main()
