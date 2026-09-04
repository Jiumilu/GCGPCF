#!/usr/bin/env python3
"""对GCWORLD第一批机器车道复核项生成可解释的处理优先级分层。"""

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
INPUT = ARTIFACTS / "gcworld-identity-review-batch-1-machine-evidence-compression-20260904.jsonl"
OUTPUT = ARTIFACTS / "gcworld-identity-review-batch-1-machine-priority-strata-20260904.jsonl"
EXPECTED_INPUT_SHA256 = "168b77cad685f60c1b7d5068c58902cc368573e3a5dd531eeaeaf105d638148f"

SUBJECT_TYPE_SCORE = {
    "政府或公共机构候选": (3, "公共机构身份关系具有较高治理敏感度"),
    "自然人候选": (2, "自然人身份关系涉及个人责任与权限边界"),
    "法人或市场主体候选": (2, "法人身份关系涉及法律与商务责任边界"),
    "其他组织候选，需人工确认": (1, "其他组织候选先按一般组织治理敏感度排序"),
}
TIER_ORDER = {"高": 0, "中": 1, "低": 2}


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


def evidence_score(max_evidence_count: int) -> tuple[int, str]:
    if not isinstance(max_evidence_count, int) or max_evidence_count < 0:
        raise ValueError("证据数量必须为非负整数")
    if max_evidence_count >= 90:
        return 3, "前十分位证据规模（不少于90条）"
    if max_evidence_count >= 36:
        return 2, "上四分位证据规模（36至89条）"
    if max_evidence_count >= 18:
        return 1, "中位及以上证据规模（18至35条）"
    return 0, "中位以下证据规模（少于18条）"


def tier_for_score(score: int) -> str:
    if score >= 4:
        return "高"
    if score >= 2:
        return "中"
    return "低"


def build_priority_rows(rows: list[dict]) -> list[dict]:
    seen: set[str] = set()
    prepared: list[dict] = []
    for row in rows:
        validate_unresolved(row)
        review_id = row.get("复核项标识")
        if not isinstance(review_id, str) or not review_id or review_id in seen:
            raise ValueError(f"复核项标识缺失或重复: {review_id}")
        seen.add(review_id)
        subject_type = row.get("主体类型建议")
        if subject_type not in SUBJECT_TYPE_SCORE:
            raise ValueError(f"未定义的主体类型: {subject_type}")
        counts = [row.get("候选证据数量"), row.get("来源证据数量"), row.get("关系证据数量")]
        if any(not isinstance(value, int) or value < 0 for value in counts):
            raise ValueError(f"证据数量格式错误: {review_id}")
        max_evidence_count = max(counts)
        evidence_points, evidence_band = evidence_score(max_evidence_count)
        subject_points, subject_reason = SUBJECT_TYPE_SCORE[subject_type]
        score = evidence_points + subject_points
        tier = tier_for_score(score)
        prepared.append(
            {
                "复核项标识": review_id,
                "输入排序序号": row["输入排序序号"],
                "数据等级": "S2",
                "显示名称": row["显示名称"],
                "主体类型建议": subject_type,
                "处理优先级": tier,
                "处理评分": score,
                "证据规模分": evidence_points,
                "证据规模档": evidence_band,
                "主体治理敏感度分": subject_points,
                "主体治理敏感度说明": subject_reason,
                "最大证据数量": max_evidence_count,
                "候选证据数量": row["候选证据数量"],
                "候选证据摘要": row["候选证据摘要"],
                "来源证据数量": row["来源证据数量"],
                "来源证据摘要": row["来源证据摘要"],
                "关系证据数量": row["关系证据数量"],
                "关系证据摘要": row["关系证据摘要"],
                "排序依据": "处理评分降序、最大证据数量降序、原输入序号升序、复核项标识升序",
                "优先级语义": "仅决定机器整理与责任路由准备顺序，不表示身份可信度、事实有效性或合并许可",
                "当前处理动作": "保持未决；按优先级整理权威锚点需求和责任路由材料",
                "SLA状态": "未启动",
                "身份决定": None,
                "自动合并": False,
                "正式世界资产标识": None,
                "KDS写入授权": False,
                "事实提升授权": False,
                "权限授予授权": False,
            }
        )

    prepared.sort(
        key=lambda row: (
            TIER_ORDER[row["处理优先级"]],
            -row["处理评分"],
            -row["最大证据数量"],
            row["输入排序序号"],
            row["复核项标识"],
        )
    )
    tier_positions: Counter[str] = Counter()
    for position, row in enumerate(prepared, start=1):
        tier_positions[row["处理优先级"]] += 1
        row["全局处理序号"] = position
        row["等级内处理序号"] = tier_positions[row["处理优先级"]]
    return prepared


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
    parser = argparse.ArgumentParser(description="生成GCWORLD第一批机器车道处理优先级分层")
    parser.add_argument("--执行", action="store_true", help="写入S2分层清单；未提供时仅校验和预览")
    args = parser.parse_args()
    actual_input_sha = sha256(INPUT)
    if actual_input_sha != EXPECTED_INPUT_SHA256:
        raise ValueError(f"密封输入摘要不匹配: expected={EXPECTED_INPUT_SHA256} actual={actual_input_sha}")
    output_rows = build_priority_rows(read_jsonl(INPUT))
    counts = Counter(row["处理优先级"] for row in output_rows)
    expected_counts = {"高": 221, "中": 536, "低": 181}
    if len(output_rows) != 938 or dict(counts) != expected_counts:
        raise ValueError(f"分层数量不符合预期: total={len(output_rows)} counts={dict(counts)}")
    payload = jsonl_bytes(output_rows)
    if args.执行:
        atomic_write(OUTPUT, payload)
    print(
        "gcworld_identity_machine_priority_strata=pass "
        f"execute={str(args.执行).lower()} total={len(output_rows)} high={counts['高']} medium={counts['中']} low={counts['低']} "
        f"output_sha256={hashlib.sha256(payload).hexdigest()} identity_decisions=0 automatic_merge=false "
        "kds_write=false sla_started=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
