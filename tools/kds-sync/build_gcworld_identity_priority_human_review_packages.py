#!/usr/bin/env python3
"""生成GCWORLD第一批优先人工复核包，禁止自动身份裁决。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-kds-authoritative-integration/artifacts"
SUGGESTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-suggestions-20260828.jsonl"
EXCEPTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-exceptions-20260828.jsonl"
PACKAGES = ARTIFACTS / "gcworld-identity-review-batch-1-priority-human-review-packages-20260828.jsonl"

EXPECTED_SHA256 = {
    SUGGESTIONS: "6c5697bcd0b1b50770b064c4b417b4772c3f9410a63cc0fa7b8f612f7c72b2eb",
    EXCEPTIONS: "b2bf4c7063581115139767735c39e8e8ec7f4d93519f31c430ac301d845ee51f",
}

KDS_SNAPSHOT = {
    "提交": "341264982d47c2b7cabe92c5a107ad0d8cad653c",
    "仓库树": "946fdf51cd7f25b7c566e79843d0351236ff2231",
    "领先": 0,
    "落后": 0,
    "普通工作树记录数": 144,
    "普通工作树摘要": "7371cbbb166b416d48559f478902f8fbd8f69e98597d15d13087814b5c5940bf",
    "展开工作树记录数": 316,
    "展开工作树摘要": "b79d2d07af32782306dda5d42a8216833808f1514494744c7868bf97e7d705a9",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def package_id(package_type: str, seed: str) -> str:
    digest = hashlib.sha256(f"gcworld-priority-human-review-v1\0{package_type}\0{seed}".encode("utf-8")).hexdigest()
    return "gcw:human-review-package:" + digest[:24]


def validate_unresolved_boundary(row: dict) -> None:
    review_id = row.get("复核项标识")
    if row.get("身份决定") is not None or row.get("正式世界资产标识") is not None:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("自动合并") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("KDS写入授权") is not False or row.get("事实提升授权") is not False or row.get("权限授予授权") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("SLA状态") != "未启动":
        raise ValueError(f"SLA边界被改变: {review_id}")


def review_item(row: dict) -> dict:
    return {
        "复核项标识": row["复核项标识"],
        "输入排序序号": row["输入排序序号"],
        "数据等级": row["数据等级"],
        "显示名称": row["显示名称"],
        "同名候选组标识": row["同名候选组标识"],
        "主体类型建议": row["主体类型建议"],
        "机器建议动作": row["机器建议动作"],
        "证据包建议": row["证据包建议"],
        "例外代码": row["例外代码"],
        "身份决定": None,
        "正式世界资产标识": None,
        "自动合并": False,
    }


def make_package(package_type: str, priority: str, seed: str, rows: list[dict]) -> dict:
    sorted_rows = sorted(rows, key=lambda row: (row["输入排序序号"], row["复核项标识"]))
    role = "GKE-001整理冲突证据后动态路由至相应业务责任人"
    review_focus = ["主体类型冲突", "权威锚点", "真实业务责任归属"]
    if package_type == "同名候选组":
        role = "GKE-001整理同名证据后动态路由至相应业务责任人"
        review_focus = ["是否同一现实主体", "各自权威锚点", "跨来源关系是否冲突"]
    return {
        "复核包标识": package_id(package_type, seed),
        "复核包类型": package_type,
        "优先级": priority,
        "数据等级": "S2",
        "复核项数量": len(sorted_rows),
        "复核项": [review_item(row) for row in sorted_rows],
        "复核重点": review_focus,
        "主复核责任角色建议": role,
        "主复核责任主体标识": None,
        "主复核接受状态": "待识别与接受",
        "第二复核角色": "F-013独立复核线程",
        "第二复核接受状态": "待运行前确认",
        "重大争议最终裁决人": "老卢",
        "所需责任声明字段": [
            "责任主体名称或组织资产标识",
            "权威角色",
            "授权依据",
            "可验证身份或签名线程",
            "复核范围",
            "有效开始时间",
            "有效结束时间",
            "目标受众",
            "业务敏感边界",
            "利益冲突声明",
        ],
        "可提交的人工建议结论": ["保持未决", "建议确认同一主体", "建议确认不同主体", "建议拆分", "建议驳回"],
        "当前包状态": "待真实业务责任主体识别与接受",
        "调度状态": "未发送",
        "SLA状态": "未启动",
        "允许当前包直接产生正式结果": False,
        "允许自动身份合并": False,
        "允许正式世界资产生成": False,
        "允许KDS写入": False,
        "允许事实提升": False,
        "允许权限授予": False,
        "KDS只读快照": KDS_SNAPSHOT,
        "输入机器建议摘要": EXPECTED_SHA256[SUGGESTIONS],
        "输入例外清单摘要": EXPECTED_SHA256[EXCEPTIONS],
    }


def build_packages(suggestions: list[dict]) -> list[dict]:
    seen_ids: set[str] = set()
    for row in suggestions:
        review_id = row.get("复核项标识")
        if not isinstance(review_id, str) or not review_id or review_id in seen_ids:
            raise ValueError(f"复核项标识缺失或重复: {review_id}")
        seen_ids.add(review_id)
        validate_unresolved_boundary(row)

    conflict_rows = [row for row in suggestions if "多类型冲突" in row.get("例外代码", [])]
    same_name: dict[str, list[dict]] = defaultdict(list)
    for row in suggestions:
        if "同名候选需独立复核" in row.get("例外代码", []):
            same_name[row["同名候选组标识"]].append(row)

    for group_id, rows in same_name.items():
        declared_sizes = {row.get("同名候选组数量") for row in rows}
        if declared_sizes != {len(rows)} or len(rows) < 2:
            raise ValueError(f"同名候选组数量不一致: {group_id}")

    packages = [
        make_package("多类型冲突", "一级", row["复核项标识"], [row])
        for row in sorted(conflict_rows, key=lambda item: (item["输入排序序号"], item["复核项标识"]))
    ]
    for group_id, rows in sorted(
        same_name.items(), key=lambda item: (min(row["输入排序序号"] for row in item[1]), item[0])
    ):
        packages.append(make_package("同名候选组", "二级", group_id, rows))

    membership: dict[str, int] = defaultdict(int)
    for package in packages:
        for row in package["复核项"]:
            membership[row["复核项标识"]] += 1
    repeated = [review_id for review_id, count in membership.items() if count > 1]
    if repeated:
        raise ValueError("优先复核包存在重复归属: " + ",".join(sorted(repeated)))
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


def verify_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"密封输入摘要不匹配: {path.name} expected={expected} actual={actual}")


def main() -> int:
    parser = argparse.ArgumentParser(description="生成GCWORLD第一批优先人工复核包")
    parser.add_argument("--执行", action="store_true", help="写入S2复核包；未提供时仅校验和预览")
    args = parser.parse_args()
    verify_inputs()
    suggestions = read_jsonl(SUGGESTIONS)
    exceptions = {row["复核项标识"]: row for row in read_jsonl(EXCEPTIONS)}
    for row in suggestions:
        if row["复核项标识"] not in exceptions or row["例外代码"] != exceptions[row["复核项标识"]]["例外代码"]:
            raise ValueError(f"机器建议与例外清单不一致: {row['复核项标识']}")
    packages = build_packages(suggestions)
    conflict_packages = sum(package["复核包类型"] == "多类型冲突" for package in packages)
    same_name_packages = sum(package["复核包类型"] == "同名候选组" for package in packages)
    review_items = sum(package["复核项数量"] for package in packages)
    if (conflict_packages, same_name_packages, review_items) != (5, 15, 35):
        raise ValueError(
            f"优先范围不符合预期: conflicts={conflict_packages} same_name={same_name_packages} items={review_items}"
        )
    payload = jsonl_bytes(packages)
    if args.执行:
        atomic_write(PACKAGES, payload)
    print(
        "gcworld_identity_priority_human_review_packages=pass "
        f"execute={str(args.执行).lower()} packages={len(packages)} conflict_packages={conflict_packages} "
        f"same_name_packages={same_name_packages} review_items={review_items} "
        f"packages_sha256={hashlib.sha256(payload).hexdigest()} dispatched=false sla_started=false "
        "identity_decisions=0 formal_world_assets=0 kds_write=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
