#!/usr/bin/env python3
"""构建GCWORLD第一批高优先级身份候选的权威锚点需求包。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-kds-authoritative-integration/artifacts"
INPUT = ARTIFACTS / "gcworld-identity-review-batch-1-machine-priority-strata-20260904.jsonl"
OUTPUT = ARTIFACTS / "gcworld-identity-review-batch-1-high-priority-anchor-demand-packages-20260904.jsonl"
EXPECTED_INPUT_SHA256 = "04f58961549c29c3544bcae87a1862c357b8b79d0da8c54ab1c96a5b01c0f072"
BATCH_SIZE = 20

COMMON_DECLARATION_FIELDS = [
    "责任组织资产标识",
    "权威角色",
    "授权依据",
    "可验证线程或身份",
    "责任范围",
    "有效起始时间",
    "有效截止时间",
    "目标受众",
    "业务敏感边界",
    "分发约束",
    "撤销或到期条件",
    "利益冲突声明",
    "当前接受人",
]

TYPE_CONFIG = {
    "政府或公共机构候选": {
        "代码": "government-public",
        "队列": "政府关系与合规权威锚点队列",
        "主复核席位": "政府关系与合规责任席位",
        "专属锚点": ["正式机构全称", "行政层级与地域管辖", "机构编制或权威登记标识", "具体部门及职能边界", "关系有效期间"],
    },
    "自然人候选": {
        "代码": "natural-person",
        "队列": "人员与关系权威锚点队列",
        "主复核席位": "人员与关系责任席位",
        "专属锚点": ["经授权的唯一人员标识", "所属组织与岗位", "项目或业务关系", "任职及关系有效期间", "同名与别名排除证据"],
    },
    "法人或市场主体候选": {
        "代码": "legal-market",
        "队列": "法人法务商务权威锚点队列",
        "主复核席位": "法人、法务与商务责任席位",
        "专属锚点": ["法定登记全称", "统一社会信用代码或等价登记标识", "登记状态与有效期间", "集团、分支或关联主体边界", "法务或商务关系责任确认"],
    },
    "其他组织候选，需人工确认": {
        "代码": "other-organization",
        "队列": "组织治理权威锚点队列",
        "主复核席位": "组织治理责任席位",
        "专属锚点": ["组织正式名称", "发起或主管组织", "章程、决议或成立依据", "成员与治理边界", "存续及关系有效期间"],
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_unresolved(row: dict) -> None:
    review_id = row.get("复核项标识")
    if row.get("身份决定") is not None or row.get("正式世界资产标识") is not None or row.get("自动合并") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("KDS写入授权") is not False or row.get("事实提升授权") is not False or row.get("权限授予授权") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("SLA状态") != "未启动":
        raise ValueError(f"SLA边界被改变: {review_id}")


def package_item(row: dict, config: dict) -> dict:
    return {
        "复核项标识": row["复核项标识"],
        "原高优先级序号": row["等级内处理序号"],
        "显示名称": row["显示名称"],
        "主体类型建议": row["主体类型建议"],
        "处理评分": row["处理评分"],
        "候选证据数量": row["候选证据数量"],
        "候选证据摘要": row["候选证据摘要"],
        "来源证据数量": row["来源证据数量"],
        "来源证据摘要": row["来源证据摘要"],
        "关系证据数量": row["关系证据数量"],
        "关系证据摘要": row["关系证据摘要"],
        "所需专属权威锚点": config["专属锚点"],
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


def build_packages(rows: list[dict], batch_size: int = BATCH_SIZE) -> list[dict]:
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("每包数量必须为正整数")
    seen: set[str] = set()
    high_by_type: dict[str, list[dict]] = {subject_type: [] for subject_type in TYPE_CONFIG}
    for row in rows:
        validate_unresolved(row)
        review_id = row.get("复核项标识")
        if not isinstance(review_id, str) or not review_id or review_id in seen:
            raise ValueError(f"复核项标识缺失或重复: {review_id}")
        seen.add(review_id)
        subject_type = row.get("主体类型建议")
        if subject_type not in TYPE_CONFIG:
            raise ValueError(f"未定义的主体类型: {subject_type}")
        if row.get("处理优先级") == "高":
            high_by_type[subject_type].append(row)

    packages: list[dict] = []
    global_package_number = 0
    for subject_type, config in TYPE_CONFIG.items():
        type_rows = sorted(
            high_by_type[subject_type],
            key=lambda row: (row["等级内处理序号"], row["输入排序序号"], row["复核项标识"]),
        )
        for offset in range(0, len(type_rows), batch_size):
            global_package_number += 1
            group = type_rows[offset : offset + batch_size]
            type_package_number = offset // batch_size + 1
            packages.append(
                {
                    "需求包标识": f"gcw:identity-anchor-demand:{config['代码']}:{type_package_number:03d}",
                    "全局需求包序号": global_package_number,
                    "类型内需求包序号": type_package_number,
                    "数据等级": "S2",
                    "责任路由队列": config["队列"],
                    "主体类型建议": subject_type,
                    "复核项数量": len(group),
                    "每包数量上限": batch_size,
                    "机器整理责任主体": "GKE-001",
                    "主复核责任席位": config["主复核席位"],
                    "主复核责任席位状态": "空缺",
                    "独立第二复核责任主体": "F-013",
                    "第二复核启动条件": "仅在可验证主复核主体明确接受责任后启动",
                    "责任主体声明必填字段": COMMON_DECLARATION_FIELDS,
                    "统一裁决规则": "任一必填字段缺失、授权依据不可验证、存在责任冲突或主体拒绝接受时，保持未决且不启动SLA",
                    "交付状态": "未交付",
                    "SLA状态": "未启动",
                    "允许读取新KDS正文": False,
                    "允许自动身份合并": False,
                    "允许正式世界资产生成": False,
                    "允许KDS写入": False,
                    "允许事实提升": False,
                    "允许权限授予": False,
                    "复核项": [package_item(row, config) for row in group],
                }
            )
    return packages


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
    parser = argparse.ArgumentParser(description="构建GCWORLD第一批高优先级权威锚点需求包")
    parser.add_argument("--执行", action="store_true", help="写入S2需求包；未提供时仅校验和预览")
    args = parser.parse_args()
    actual_input_sha = sha256(INPUT)
    if actual_input_sha != EXPECTED_INPUT_SHA256:
        raise ValueError(f"密封输入摘要不匹配: expected={EXPECTED_INPUT_SHA256} actual={actual_input_sha}")
    packages = build_packages(read_jsonl(INPUT))
    item_counts = Counter(package["主体类型建议"] for package in packages for _ in package["复核项"])
    package_counts = Counter(package["主体类型建议"] for package in packages)
    expected_items = {
        "政府或公共机构候选": 32,
        "自然人候选": 80,
        "法人或市场主体候选": 79,
        "其他组织候选，需人工确认": 30,
    }
    expected_packages = {
        "政府或公共机构候选": 2,
        "自然人候选": 4,
        "法人或市场主体候选": 4,
        "其他组织候选，需人工确认": 2,
    }
    if dict(item_counts) != expected_items or dict(package_counts) != expected_packages:
        raise ValueError(f"需求包数量不符合预期: items={dict(item_counts)} packages={dict(package_counts)}")
    payload = jsonl_bytes(packages)
    if args.执行:
        atomic_write(OUTPUT, payload)
    print(
        "gcworld_identity_high_priority_anchor_packages=pass "
        f"execute={str(args.执行).lower()} packages={len(packages)} items={sum(item_counts.values())} "
        f"output_sha256={hashlib.sha256(payload).hexdigest()} identity_decisions=0 automatic_merge=false "
        "kds_write=false sla_started=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
