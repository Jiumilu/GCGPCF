#!/usr/bin/env python3
"""Validate bounded registration of GlobalCloud ICP in the project group."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ICP_ROOT = ROOT.parent / "GlobalCloud ICP"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_icp_project_registration: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    master = read(ROOT / "01-architecture/GlobalCloud 项目群总体方案.md")
    implementation = read(ROOT / "GlobalCloud 项目群实施方案.md")
    master_register = read(ROOT / "09-status/globalcloud-project-master-plan-control-register.md")
    implementation_register = read(ROOT / "09-status/globalcloud-project-implementation-control-register.md")
    status = read(ROOT / "projects/icp/STATUS.md")
    risk = read(ROOT / "projects/icp/RISK.md")
    roadmap = read(ROOT / "projects/icp/ROADMAP.md")

    for path in [
        ICP_ROOT / "AGENTS.md",
        ICP_ROOT / "README.md",
        ICP_ROOT / "GlobalCloud ICP 总体方案.md",
        ICP_ROOT / "GlobalCloud ICP 实施方案.md",
        ICP_ROOT / "PROJECT_HARNESS_MANIFEST.md",
        ICP_ROOT / "docs/evidence/gc-icp-bootstrap-evidence-20260712.md",
        ROOT / "tools/kds-sync/validate_gfis_real_fact_entry_gate.py",
    ]:
        read(path)

    require("项目群当前纳入 18 个项目" in master, "master plan must declare 18 projects")
    require("| ICP | 24字产业模型" in master, "master plan missing ICP responsibility")
    require("18. GlobalCloud ICP" in implementation, "implementation plan missing project 18")
    require("17项目" in implementation, "historical 17-project baseline must be preserved")
    require("| GlobalCloud ICP | `GlobalCloud ICP`" in master_register, "master register missing ICP")
    require("| GlobalCloud ICP | `GlobalCloud ICP 总体方案.md`" in implementation_register, "implementation register missing ICP")

    combined = "\n".join([master, implementation, master_register, implementation_register, status, risk, roadmap])
    for phrase in ["candidate", "partial", "human_required", "不建立第二套资源事实主账", "不自动批准或晋升状态"]:
        require(phrase in combined, f"missing boundary phrase: {phrase}")
    for forbidden in ["accepted: true", "integrated: true", "production_ready: true", "customer_accepted: true"]:
        require(forbidden not in combined, f"forbidden promotion found: {forbidden}")

    print("icp_project_registration=pass")
    print("project_count=18 icp_status=candidate overall_status=partial confirmation_status=human_required")
    print("historical_project_count=17 historical_evidence_rewrite=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
