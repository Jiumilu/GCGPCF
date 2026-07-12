#!/usr/bin/env python3
"""Validate the G00 Constitution inheritance and ownership boundary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_GROUP_ROOT = ROOT.parent


def require_text(path: Path, terms: tuple[str, ...]) -> None:
    if not path.exists():
        raise SystemExit(f"constitution_g00=fail reason=missing_file path={path}")
    text = path.read_text(encoding="utf-8")
    missing = [term for term in terms if term not in text]
    if missing:
        raise SystemExit(
            "constitution_g00=fail "
            f"reason=missing_terms path={path} terms={','.join(missing)}"
        )


def main() -> int:
    require_text(
        ROOT / "01-architecture/GlobalCloud 项目群总体方案.md",
        ("GlobalCloud宪法", "最高规范性", "ICP", "KDS"),
    )
    require_text(
        ROOT / "GlobalCloud 项目群实施方案.md",
        ("GlobalCloud宪法", "G00", "SOP", "WAES", "KDS"),
    )
    require_text(
        ROOT / "02-governance/constitution-governance-responsibility.md",
        ("产业领域解释与修订候选", "项目群传导与 G00", "正本与版本保管"),
    )
    require_text(
        PROJECT_GROUP_ROOT / "GlobalCloud ICP/config/constitution-governance.yaml",
        ("domainOwner: ICP", "canonicalCustodian: KDS", "noWriteAssertion: true"),
    )
    require_text(
        PROJECT_GROUP_ROOT / "GlobalCloud KDS/体系/GlobalCloud宪法.md",
        ("industry_domain_owner: ICP", "canonical_custodian: KDS"),
    )
    require_text(
        PROJECT_GROUP_ROOT / "GlobalCloud SOP/docs/governance/constitution-amendment-audit-policy.md",
        ("SOP 是宪法修订程序与审计责任方", "不批准宪法修订"),
    )
    print(
        "constitution_g00=pass status=candidate "
        "domain_owner=ICP canonical_custodian=KDS "
        "authorization=human_required status_promotion=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
