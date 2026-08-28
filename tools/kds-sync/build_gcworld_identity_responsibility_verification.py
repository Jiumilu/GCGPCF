#!/usr/bin/env python3
"""生成GCWORLD优先人工复核包的责任主体核验回执。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-kds-authoritative-integration/artifacts"
PACKAGES = ARTIFACTS / "gcworld-identity-review-batch-1-priority-human-review-packages-20260828.jsonl"
OUTPUT = ARTIFACTS / "gcworld-identity-review-batch-1-responsibility-identification-verification-20260828.jsonl"

METADATA_SOURCES = {
    "governance/openspec/gke001-program-binding.yaml": "0536e458d7510796426d3045cc0f4cceb2014f9f6c0fd219fdb5aa9a0c83f3c9",
    "docs/harness/minimum-closed-loop/project-role-verification-matrix.md": "22752fd5a715b6b77027f9f22e3c4003c9512c3760b8bb2c7298f6b75c94e31b",
    "registry/project-state-matrix.yaml": "bed92af15154f05e460be6ad5de0c3d5dcd7445b264409ebd0908dc2a2293a69",
    "config/project-group-projects.yaml": "2f53678063083a06c98188f2d423387fab4f54dd6ae72e56a142e9a2df31a326",
    "openspec/changes/gcworld-kds-authoritative-integration/artifacts/GCWORLD第一批优先人工复核包责任主体接受授权请求_20260828.md": "acd13e8b3ab0ec426d476975c5b3ac02ce61ac40c2caf6e9417136c0daf6786b",
}

PACKAGES_SHA256 = "cd06236075b7b9b9098a75ef6190dc6fd7d2258eb7e2865c27197949d2d50ced"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_package(package: dict) -> None:
    package_id = package.get("复核包标识")
    if package.get("允许当前包直接产生正式结果") is not False:
        raise ValueError(f"正式结果边界被改变: {package_id}")
    for key in ("允许自动身份合并", "允许正式世界资产生成", "允许KDS写入", "允许事实提升", "允许权限授予"):
        if package.get(key) is not False:
            raise ValueError(f"正式结果边界被改变: {package_id} {key}")
    if package.get("调度状态") != "未发送" or package.get("SLA状态") != "未启动":
        raise ValueError(f"调度或SLA边界被改变: {package_id}")


def build_receipts(packages: list[dict]) -> list[dict]:
    seen: set[str] = set()
    receipts: list[dict] = []
    for package in packages:
        validate_package(package)
        package_id = package.get("复核包标识")
        if not isinstance(package_id, str) or not package_id or package_id in seen:
            raise ValueError(f"复核包标识缺失或重复: {package_id}")
        seen.add(package_id)
        receipts.append(
            {
                "复核包标识": package_id,
                "复核包类型": package["复核包类型"],
                "优先级": package["优先级"],
                "数据等级": "S2",
                "复核项数量": package["复核项数量"],
                "主复核责任角色建议": package["主复核责任角色建议"],
                "真实业务主复核责任主体标识": None,
                "责任主体核验状态": "证据不足，保持未决",
                "核验缺口": [
                    "缺少真实业务责任主体标识",
                    "缺少可验证授权依据",
                    "缺少明确复核范围",
                    "缺少有效开始与结束时间",
                    "缺少目标受众与业务敏感边界",
                    "缺少利益冲突声明",
                    "缺少责任接受声明",
                ],
                "GKE-001角色核验": {
                    "线程标识": "019f0697-c8ce-7110-8ac8-9a7dbc6ba2a5",
                    "角色": "机器归一、证据整理与初步责任路由",
                    "状态": "线程与角色登记可验证，不得替代真实业务主复核",
                },
                "F-013角色核验": {
                    "线程标识": "019fc228-2403-7123-9cae-fb9028850b84",
                    "角色": "独立第二复核",
                    "状态": "线程与角色登记可验证，因主复核未接受而不得提前发起",
                },
                "交付状态": "未发送",
                "交付原因": "未找到满足完整声明字段的可验证真实业务责任主体",
                "主复核接受状态": "待识别与接受",
                "F-013发起状态": "未发起",
                "F-013接受状态": "待运行前确认",
                "SLA状态": "未启动",
                "身份决定": None,
                "正式世界资产标识": None,
                "允许自动身份合并": False,
                "允许KDS写入": False,
                "允许事实提升": False,
                "允许权限授予": False,
                "输入复核包摘要": PACKAGES_SHA256,
                "核验元数据来源": [
                    {"路径": path, "SHA-256": digest} for path, digest in METADATA_SOURCES.items()
                ],
            }
        )
    return receipts


def verify_inputs() -> None:
    actual = sha256(PACKAGES)
    if actual != PACKAGES_SHA256:
        raise ValueError(f"优先人工复核包摘要不匹配: expected={PACKAGES_SHA256} actual={actual}")
    for relative, expected in METADATA_SOURCES.items():
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise ValueError(f"责任核验元数据摘要不匹配: {relative} expected={expected} actual={actual}")


def jsonl_bytes(rows: list[dict]) -> bytes:
    return ("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for row in rows) + "\n").encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", delete=False) as handle:
        temp_path = Path(handle.name)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temp_path, 0o600)
    os.replace(temp_path, path)


def main() -> int:
    parser = argparse.ArgumentParser(description="生成GCWORLD优先复核包责任主体核验回执")
    parser.add_argument("--执行", action="store_true", help="写入S2核验回执；未提供时仅校验和预览")
    args = parser.parse_args()
    verify_inputs()
    receipts = build_receipts(read_jsonl(PACKAGES))
    if len(receipts) != 20 or sum(row["复核项数量"] for row in receipts) != 35:
        raise ValueError("责任主体核验范围不符合20包35项")
    payload = jsonl_bytes(receipts)
    if args.执行:
        atomic_write(OUTPUT, payload)
    print(
        "gcworld_identity_responsibility_verification=pass "
        f"execute={str(args.执行).lower()} packages={len(receipts)} items={sum(row['复核项数量'] for row in receipts)} "
        f"verified_primary_owners=0 delivered=0 f013_started=0 sla_started=0 "
        f"output_sha256={hashlib.sha256(payload).hexdigest()} kds_write=false identity_decisions=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
