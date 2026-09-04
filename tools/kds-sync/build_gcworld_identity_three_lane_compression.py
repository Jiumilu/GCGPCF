#!/usr/bin/env python3
"""构建GCWORLD第一批身份复核三车道总账与机器证据压缩清单。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-kds-authoritative-integration/artifacts"
ROUTING = ARTIFACTS / "gcworld-identity-review-batch-1-temporary-responsibility-routing-20260828.jsonl"
SUGGESTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-suggestions-20260828.jsonl"
PRIORITY_PACKAGES = ARTIFACTS / "gcworld-identity-review-batch-1-priority-human-review-packages-20260828.jsonl"
SEAT_REGISTRY = ARTIFACTS / "gcworld-identity-review-batch-1-responsibility-seat-registry-20260903.yaml"
PARTITION_OUTPUT = ARTIFACTS / "gcworld-identity-review-batch-1-three-lane-partition-20260904.jsonl"
COMPRESSION_OUTPUT = ARTIFACTS / "gcworld-identity-review-batch-1-machine-evidence-compression-20260904.jsonl"

EXPECTED_SHA256 = {
    ROUTING: "a8f7397c1392d1d61fcd096ca3b0ee97d4f82bded28004b7bad7fcd3a65eb163",
    SUGGESTIONS: "6c5697bcd0b1b50770b064c4b417b4772c3f9410a63cc0fa7b8f612f7c72b2eb",
    PRIORITY_PACKAGES: "cd06236075b7b9b9098a75ef6190dc6fd7d2258eb7e2865c27197949d2d50ced",
    SEAT_REGISTRY: "07ed0bba4493e2ae34458d2e1ace462442bf98e0f25c395f76a0ee88c9438c92",
}

KDS_SNAPSHOT = {
    "提交": "341264982d47c2b7cabe92c5a107ad0d8cad653c",
    "仓库树": "946fdf51cd7f25b7c566e79843d0351236ff2231",
    "领先": 0,
    "落后": 0,
    "普通工作树记录数": 146,
    "普通工作树摘要": "9997b1538a1542f180a8cbde3a1928e6ddb810d61b62af784b1d5d5bcda31203",
    "展开工作树记录数": 318,
    "展开工作树摘要": "27b56aebd9e95da9c8735a3c122f1e4df0a2e458bcd8e33afdecc59f04249784",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def index_rows(rows: list[dict], label: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in rows:
        review_id = row.get("复核项标识")
        if not isinstance(review_id, str) or not review_id or review_id in result:
            raise ValueError(f"{label}复核项标识缺失或重复: {review_id}")
        result[review_id] = row
    return result


def validate_unresolved(row: dict) -> None:
    review_id = row.get("复核项标识")
    if row.get("身份决定") is not None or row.get("正式世界资产标识") is not None or row.get("自动合并") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("KDS写入授权") is not False or row.get("事实提升授权") is not False or row.get("权限授予授权") is not False:
        raise ValueError(f"未决边界被改变: {review_id}")
    if row.get("SLA状态") != "未启动":
        raise ValueError(f"SLA边界被改变: {review_id}")


def refs_digest(values: list[str]) -> str:
    if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values):
        raise ValueError("证据标识列表为空或格式错误")
    canonical = json.dumps(sorted(values), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def priority_ids(packages: list[dict]) -> set[str]:
    result: set[str] = set()
    for package in packages:
        for item in package.get("复核项", []):
            review_id = item.get("复核项标识")
            if not isinstance(review_id, str) or not review_id or review_id in result:
                raise ValueError(f"优先复核项标识缺失或重复: {review_id}")
            result.add(review_id)
    return result


def compression_row(row: dict) -> dict:
    evidence = row.get("证据包建议", {})
    candidate_refs = evidence.get("候选标识")
    source_refs = evidence.get("来源证据标识")
    relation_refs = evidence.get("关系证据标识")
    return {
        "复核项标识": row["复核项标识"],
        "输入排序序号": row["输入排序序号"],
        "数据等级": "S2",
        "显示名称": row["显示名称"],
        "主体类型建议": row["主体类型建议"],
        "压缩状态": "机器证据摘要已生成，身份仍未决",
        "候选证据数量": len(candidate_refs),
        "候选证据摘要": refs_digest(candidate_refs),
        "来源证据数量": len(source_refs),
        "来源证据摘要": refs_digest(source_refs),
        "关系证据数量": len(relation_refs),
        "关系证据摘要": refs_digest(relation_refs),
        "建议核验锚点": evidence.get("建议核验锚点", []),
        "机器建议动作": row["机器建议动作"],
        "例外代码": row["例外代码"],
        "证据明细来源": "gcworld-identity-review-batch-1-machine-normalization-suggestions-20260828.jsonl",
        "摘要用途": "用于变更检测和复核包去重，不是权威身份锚点",
        "SLA状态": "未启动",
        "身份决定": None,
        "自动合并": False,
        "正式世界资产标识": None,
        "KDS写入授权": False,
        "事实提升授权": False,
        "权限授予授权": False,
    }


def build_outputs(
    routing: list[dict], suggestions: list[dict], priority_packages: list[dict]
) -> tuple[list[dict], list[dict]]:
    route_by_id = index_rows(routing, "临时责任路由")
    suggestion_by_id = index_rows(suggestions, "机器归一建议")
    for row in route_by_id.values():
        validate_unresolved(row)
    for row in suggestion_by_id.values():
        validate_unresolved(row)

    gke_ids = {review_id for review_id, row in route_by_id.items() if row.get("机器归一与证据整理责任主体") == "GKE-001"}
    direct_ids = {review_id for review_id, row in route_by_id.items() if row.get("机器归一与证据整理责任主体") is None}
    unexpected = set(route_by_id) - gke_ids - direct_ids
    if unexpected:
        raise ValueError("存在未定义的责任车道")
    if set(suggestion_by_id) != gke_ids:
        raise ValueError("机器归一建议与GKE-001路由集合不一致")

    human_priority_ids = priority_ids(priority_packages)
    if not human_priority_ids <= gke_ids:
        raise ValueError("优先人工例外不完全属于GKE-001候选集合")
    machine_ids = gke_ids - human_priority_ids
    if machine_ids & human_priority_ids or machine_ids & direct_ids or human_priority_ids & direct_ids:
        raise ValueError("三条处理车道存在交叉")
    if machine_ids | human_priority_ids | direct_ids != set(route_by_id):
        raise ValueError("三条处理车道未覆盖全部复核项")

    partition: list[dict] = []
    for review_id, route in sorted(route_by_id.items(), key=lambda item: (item[1]["输入排序序号"], item[0])):
        if review_id in machine_ids:
            lane = "机器证据压缩车道"
            state = "证据压缩已生成，仍待权威锚点与业务确认"
        elif review_id in human_priority_ids:
            lane = "优先人工例外车道"
            state = "责任席位空缺，保持冻结"
        else:
            lane = "直接业务责任车道"
            state = "待PMO、项目负责人或组织治理责任人验证并接受"
        partition.append(
            {
                "复核项标识": review_id,
                "输入排序序号": route["输入排序序号"],
                "数据等级": "S2",
                "显示名称": route["显示名称"],
                "主体类型建议": route["主体类型建议"],
                "处理车道": lane,
                "车道状态": state,
                "SLA状态": "未启动",
                "身份决定": None,
                "自动合并": False,
                "正式世界资产标识": None,
                "KDS写入授权": False,
                "事实提升授权": False,
                "权限授予授权": False,
                "KDS只读快照": KDS_SNAPSHOT,
            }
        )

    compressed = [
        compression_row(suggestion_by_id[review_id])
        for review_id in sorted(machine_ids, key=lambda value: (suggestion_by_id[value]["输入排序序号"], value))
    ]
    return partition, compressed


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
    parser = argparse.ArgumentParser(description="构建GCWORLD第一批身份复核三车道总账与机器证据压缩清单")
    parser.add_argument("--执行", action="store_true", help="写入S2输出；未提供时仅校验和预览")
    args = parser.parse_args()
    verify_inputs()
    partition, compressed = build_outputs(read_jsonl(ROUTING), read_jsonl(SUGGESTIONS), read_jsonl(PRIORITY_PACKAGES))
    lane_counts: dict[str, int] = {}
    for row in partition:
        lane_counts[row["处理车道"]] = lane_counts.get(row["处理车道"], 0) + 1
    expected_counts = {"机器证据压缩车道": 938, "优先人工例外车道": 35, "直接业务责任车道": 43}
    if lane_counts != expected_counts or len(compressed) != 938:
        raise ValueError(f"三车道数量不符合预期: lanes={lane_counts} compressed={len(compressed)}")
    partition_payload = jsonl_bytes(partition)
    compression_payload = jsonl_bytes(compressed)
    if args.执行:
        atomic_write(PARTITION_OUTPUT, partition_payload)
        atomic_write(COMPRESSION_OUTPUT, compression_payload)
    print(
        "gcworld_identity_three_lane_compression=pass "
        f"execute={str(args.执行).lower()} total={len(partition)} machine={lane_counts['机器证据压缩车道']} "
        f"priority_human={lane_counts['优先人工例外车道']} direct_business={lane_counts['直接业务责任车道']} "
        f"partition_sha256={hashlib.sha256(partition_payload).hexdigest()} "
        f"compression_sha256={hashlib.sha256(compression_payload).hexdigest()} "
        "identity_decisions=0 automatic_merge=false kds_write=false sla_started=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
