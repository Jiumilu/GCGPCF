#!/usr/bin/env python3
"""基于密封S2输入生成GCWORLD第一批身份机器建议与例外清单。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "openspec/changes/gcworld-kds-authoritative-integration/artifacts"
HIGH_FREQUENCY = ARTIFACTS / "gcworld-identity-review-batch-1-high-frequency-20260826.jsonl"
TYPE_SUGGESTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-type-anchor-suggestions-20260826.jsonl"
ROUTING = ARTIFACTS / "gcworld-identity-review-batch-1-temporary-responsibility-routing-20260828.jsonl"
PREPARATION = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-preparation-20260828.yaml"
SUGGESTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-suggestions-20260828.jsonl"
EXCEPTIONS = ARTIFACTS / "gcworld-identity-review-batch-1-machine-normalization-exceptions-20260828.jsonl"

EXPECTED_SHA256 = {
    HIGH_FREQUENCY: "a8e8a27143a28e81b61cfe2e531ec4435444f3659c4a6705b3e6d3634078bdff",
    TYPE_SUGGESTIONS: "ea1e0aef79bcee9cb82339704c1dc0d07fcb05f09c762a6445449adc0a8ff2ff",
    ROUTING: "a8f7397c1392d1d61fcd096ca3b0ee97d4f82bded28004b7bad7fcd3a65eb163",
    PREPARATION: "d6de13b375f2c04bd3b2d8ec52047b684aa30832ea04814eb930f2939fd71195",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def indexed(rows: list[dict], label: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in rows:
        review_id = row.get("复核项标识")
        if not isinstance(review_id, str) or not review_id:
            raise ValueError(f"{label}缺少复核项标识")
        if review_id in result:
            raise ValueError(f"{label}存在重复复核项标识: {review_id}")
        result[review_id] = row
    return result


def normalized_name(value: str) -> str:
    return "".join(unicodedata.normalize("NFKC", value).split()).casefold()


def name_group_id(value: str) -> str:
    seed = "gcworld-name-review-group-v1\0" + normalized_name(value)
    return "gcw:name-review-group:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]


def validate_evidence_counts(row: dict) -> None:
    pairs = (
        ("候选标识", "候选数量"),
        ("来源证据标识", "来源证据数量"),
        ("关系证据标识", "关系证据数量"),
    )
    for refs_key, count_key in pairs:
        refs = row.get(refs_key)
        count = row.get(count_key)
        if not isinstance(refs, list) or len(refs) != count or not refs:
            raise ValueError(f"证据计数不一致: {row.get('复核项标识')} {refs_key}/{count_key}")


def validate_joined_rows(high: dict, subject: dict, route: dict) -> None:
    review_id = high["复核项标识"]
    if high.get("显示名称") != subject.get("显示名称") or high.get("显示名称") != route.get("显示名称"):
        raise ValueError(f"显示名称不一致: {review_id}")
    if high.get("排序序号") != subject.get("输入排序序号") or high.get("排序序号") != route.get("输入排序序号"):
        raise ValueError(f"排序序号不一致: {review_id}")
    if high.get("数据等级") != "S2" or subject.get("数据等级") != "S2" or route.get("数据等级") != "S2":
        raise ValueError(f"数据等级不是S2: {review_id}")
    if high.get("自动合并") is not False or subject.get("自动合并") is not False or route.get("自动合并") is not False:
        raise ValueError(f"自动合并边界被改变: {review_id}")
    if route.get("KDS写入授权") is not False or route.get("事实提升授权") is not False or route.get("权限授予授权") is not False:
        raise ValueError(f"禁止授权边界被改变: {review_id}")
    if route.get("身份决定") is not None or route.get("正式世界资产标识") is not None:
        raise ValueError(f"未决身份被提前决定: {review_id}")
    validate_evidence_counts(high)


def build_suggestions(
    high_frequency: list[dict], type_suggestions: list[dict], routing: list[dict]
) -> tuple[list[dict], list[dict]]:
    high_by_id = indexed(high_frequency, "高频身份复核视图")
    type_by_id = indexed(type_suggestions, "主体类型建议")
    route_by_id = indexed(routing, "临时责任路由")
    if set(high_by_id) != set(type_by_id) or set(high_by_id) != set(route_by_id):
        raise ValueError("三个输入的复核项标识集合不一致")

    selected_ids = [
        review_id
        for review_id, route in route_by_id.items()
        if route.get("机器归一与证据整理责任主体") == "GKE-001"
    ]
    selected_ids.sort(key=lambda review_id: (route_by_id[review_id]["输入排序序号"], review_id))
    name_counts = Counter(normalized_name(high_by_id[review_id]["显示名称"]) for review_id in selected_ids)

    suggestions: list[dict] = []
    exceptions: list[dict] = []
    for review_id in selected_ids:
        high = high_by_id[review_id]
        subject = type_by_id[review_id]
        route = route_by_id[review_id]
        validate_joined_rows(high, subject, route)

        comparison_name = normalized_name(high["显示名称"])
        exception_codes = ["权威锚点未登记", "真实业务责任主体未验证"]
        if name_counts[comparison_name] > 1:
            exception_codes.append("同名候选需独立复核")
        if subject["主体类型建议"] == "多类型冲突，需人工确认":
            exception_codes.append("多类型冲突")

        suggestion_action = "保持未决，补齐权威锚点后路由真实业务责任人与F-013复核"
        if "多类型冲突" in exception_codes:
            suggestion_action = "保持未决，进入跨域冲突人工复核并补齐权威锚点"

        suggestions.append(
            {
                "复核项标识": review_id,
                "输入排序序号": high["排序序号"],
                "数据等级": "S2",
                "显示名称": high["显示名称"],
                "名称比较值": comparison_name,
                "同名候选组标识": name_group_id(high["显示名称"]),
                "同名候选组数量": name_counts[comparison_name],
                "主体类型建议": subject["主体类型建议"],
                "机器建议状态": "候选建议已生成，禁止自动决定",
                "机器建议动作": suggestion_action,
                "证据包状态": "引用完整，权威锚点与业务责任确认缺失",
                "证据包建议": {
                    "候选标识": high["候选标识"],
                    "来源证据标识": high["来源证据标识"],
                    "关系证据标识": high["关系证据标识"],
                    "建议核验锚点": subject["建议核验锚点"],
                },
                "主复核责任路由建议": route["主复核责任路由"],
                "第二复核": "F-013独立复核线程",
                "例外代码": exception_codes,
                "SLA状态": "未启动",
                "身份决定": None,
                "自动合并": False,
                "正式世界资产标识": None,
                "KDS写入授权": False,
                "事实提升授权": False,
                "权限授予授权": False,
            }
        )
        exceptions.append(
            {
                "复核项标识": review_id,
                "输入排序序号": high["排序序号"],
                "数据等级": "S2",
                "显示名称": high["显示名称"],
                "例外代码": exception_codes,
                "例外处置": suggestion_action,
                "当前状态": "未决候选",
                "真实业务责任主体标识": None,
                "F-013复核状态": "待运行前确认",
                "SLA状态": "未启动",
                "允许自动身份合并": False,
                "允许正式世界资产生成": False,
                "允许KDS写入": False,
                "允许事实提升": False,
                "允许权限授予": False,
            }
        )
    return suggestions, exceptions


def jsonl_bytes(rows: list[dict]) -> bytes:
    return ("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for row in rows) + "\n").encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    parser = argparse.ArgumentParser(description="生成GCWORLD第一批身份机器建议与例外清单")
    parser.add_argument("--执行", action="store_true", help="写入密封S2输出；未提供时仅校验和预览统计")
    args = parser.parse_args()

    verify_inputs()
    suggestions, exceptions = build_suggestions(
        read_jsonl(HIGH_FREQUENCY), read_jsonl(TYPE_SUGGESTIONS), read_jsonl(ROUTING)
    )
    if len(suggestions) != 973 or len(exceptions) != 973:
        raise ValueError(f"输出数量不符合准备控制: suggestions={len(suggestions)} exceptions={len(exceptions)}")

    suggestion_payload = jsonl_bytes(suggestions)
    exception_payload = jsonl_bytes(exceptions)
    if args.执行:
        atomic_write(SUGGESTIONS, suggestion_payload)
        atomic_write(EXCEPTIONS, exception_payload)

    duplicate_rows = sum(item["同名候选组数量"] > 1 for item in suggestions)
    conflicts = sum("多类型冲突" in item["例外代码"] for item in suggestions)
    print(
        "gcworld_identity_machine_suggestions=pass "
        f"execute={str(args.执行).lower()} suggestions={len(suggestions)} exceptions={len(exceptions)} "
        f"duplicate_name_rows={duplicate_rows} multi_type_conflicts={conflicts} "
        f"suggestions_sha256={hashlib.sha256(suggestion_payload).hexdigest()} "
        f"exceptions_sha256={hashlib.sha256(exception_payload).hexdigest()} "
        "automatic_merge=false formal_world_asset=false kds_write=false fact_promotion=false permission_grant=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
