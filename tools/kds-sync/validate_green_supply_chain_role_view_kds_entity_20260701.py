#!/usr/bin/env python3
"""Validate the local KDS entity artifact for the green supply-chain role view."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
KDS_ROOT = ROOT.parent / "GlobalCloud KDS"

GPCF_DOC = ROOT / "03-data-ai-knowledge" / "GlobalCloud绿色供应链角色视图KDS实体产物.md"
LOOP_DOC = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001.md"
ENTITY_DOC = KDS_ROOT / "entities" / "green-supply-chain-role-view-entity.md"
REGISTRY = KDS_ROOT / "_registries" / "global-object-registry.yaml"

ENTITY_ID = "KDS-GSC-ROLE-VIEW-20260701"


def fail(message: str) -> None:
    print(f"green_supply_chain_role_view_entity_gate=fail: {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing {path}")
    return path.read_text(encoding="utf-8")


def require_tokens(path: Path, text: str, tokens: list[str]) -> None:
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{path} missing tokens: {', '.join(missing)}")


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path} missing frontmatter")
    require(text.find("\n---\n", 4) > 0, f"{path} invalid frontmatter")


def main() -> None:
    gpcf_doc = read(GPCF_DOC)
    loop_doc = read(LOOP_DOC)
    entity_doc = read(ENTITY_DOC)
    registry = read(REGISTRY)

    for path, text in ((GPCF_DOC, gpcf_doc), (LOOP_DOC, loop_doc), (ENTITY_DOC, entity_doc)):
        require_frontmatter(path, text)

    require_tokens(
        GPCF_DOC,
        gpcf_doc,
        [
            ENTITY_ID,
            "controlled_local_entity",
            "no_write",
            "candidate_only",
            "KDS 11 池",
            "知识工程",
            "GPCF-KDS-DKS-054",
            "GPCF-KDS-DKS-060",
            "merged_precondition_controlled",
            "GPCF-GCKF-P0-D190-001",
            "nextExecutableRounds=0",
            "禁止声明 `accepted`",
            "不等于 KDS API 已真实同步",
        ],
    )
    require_tokens(
        ENTITY_DOC,
        entity_doc,
        [
            f"entity_id: {ENTITY_ID}",
            "entity_type: kds_role_view",
            "status: controlled_candidate",
            "write_boundary: no_write",
            "confirmation_status: human_review_pending",
            "GSC-ROLE-UNIT-OWNER",
            "GSC-ROLE-PROJECT-OWNER",
            "GSC-ROLE-MATERIAL-CURATOR",
            "GSC-ROLE-AI-QUOTA-ADMIN",
            "GSC-ROLE-POINTS-ADMIN",
            "GSC-ROLE-BOUNTY-ADMIN",
            "GSC-ROLE-FINANCE-CONTACT",
            "GSC-ROLE-QUALITY-POD-CONTACT",
            "GSC-ROLE-GFIS-OPERATOR",
            "GSC-ROLE-WAES-LIAISON",
            "GSC-ROLE-KDS-RECORDER",
            "talent_pool",
            "data_pool",
            "scenario_pool",
            "finance_private",
            "waes_boundary",
            "kds_operator",
            "Promotion Blockers",
            "Forbidden Claims",
            "GPCF-KDS-DKS-054",
            "GPCF-KDS-DKS-060",
            "GPCF-GCKF-P0-D185-001",
            "GPCF-GCKF-P0-D190-001",
            "nextExecutableRounds=0",
            "resumeAllowed=false",
        ],
    )
    require_tokens(
        LOOP_DOC,
        loop_doc,
        [
            "GPCF-KDS-GSC-ROLE-VIEW-ENTITY-001",
            "## 3. LOOP 运行控制闭环",
            "### run",
            "### stop",
            "### verify",
            "### recover",
            "### debug",
            "validate_green_supply_chain_role_view_kds_entity_20260701.py",
            "merged_precondition_controlled",
            "authorization_boundary",
            "nextExecutableRounds=0",
        ],
    )
    require_tokens(
        REGISTRY,
        registry,
        [
            ENTITY_ID,
            "green-supply-chain-role-view-entity.md",
            "kds_role_view",
            "governance_index_only",
            "no_write",
            "merged_precondition_status: merged_precondition_controlled",
            "mainline_stop_type: authorization_boundary",
            "next_executable_rounds: 0",
        ],
    )

    forbidden_confirmed_claims = [
        "status: accepted",
        "status: integrated",
        "status: production_ready",
        "status: customer_accepted",
        "production_write",
        "approved_business_fact",
    ]
    combined = "\n".join([gpcf_doc, loop_doc, entity_doc])
    offenders = [claim for claim in forbidden_confirmed_claims if claim in combined]
    require(not offenders, f"forbidden promotion claims found: {', '.join(offenders)}")

    print("green_supply_chain_role_view_entity_gate=pass")
    print(f"entity_id={ENTITY_ID}")
    print(f"entity_doc={ENTITY_DOC}")
    print(f"gpcf_doc={GPCF_DOC.relative_to(ROOT)}")
    print(f"loop_doc={LOOP_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
