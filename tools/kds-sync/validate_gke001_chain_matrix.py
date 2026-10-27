#!/usr/bin/env python3
"""校验 GlobalCloud GKE-001 知识工程链路矩阵（PG-13 inventory 版）。

用途
----
只读校验 `runtime/gke001-chain-matrix.yaml`：检查顶层 schema、六个环节是否齐全
（canonical 契约 / KDS 存储 / Studio 接入 / Brain candidate / MMC 授权 / 人工确认）、
stage_id 唯一、artifacts 与 evidence 指向的文件真实存在、status 取值合法（S0-S3 / pending，
或 unknown 且 inferred=true）、depends 引用完整且无环、每个未完成环节至少登记一条 gap、
断点表按 P0→P1→P2 排序且引用真实 stage、矩阵不自称链路闭环，以及不包含凭据类键名或密钥形态的值。

本脚本不写任何文件，不修改矩阵，不声明链路闭环或授权生效。

用法
----
    python3 tools/kds-sync/validate_gke001_chain_matrix.py
    python3 tools/kds-sync/validate_gke001_chain_matrix.py --matrix /tmp/gke001-chain-matrix.yaml

退出码
------
    0  全部校验通过
    1  存在校验失败项
    2  矩阵文件缺失或不是合法 YAML

路径解析
--------
artifacts / evidence / 断点 evidence 中的相对路径按顺序解析：绝对路径 → GPCF 仓库根 →
工作区根（GPCF 的上级目录）。允许 `path#段落` 片段标注。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    print("FAIL validate_gke001_chain_matrix: 缺少 PyYAML（pip install pyyaml）", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
DEFAULT_MATRIX = ROOT / "runtime/gke001-chain-matrix.yaml"

REQUIRED_TOP = (
    "schema_version",
    "matrix_id",
    "generated_at",
    "owner",
    "engineering_domain",
    "canonical_feature",
    "scope",
    "source_of_truth",
    "chain_closed",
    "stage_scale",
    "declared_status",
    "stages",
    "breakpoints",
)
REQUIRED_SCALE_KEYS = ("S0", "S1", "S2", "S3", "pending")
REQUIRED_STAGE_KEYS = (
    "canonical_contract",
    "kds_storage",
    "studio_ingest",
    "brain_candidate",
    "mmc_authorization",
    "human_confirmation",
)
REQUIRED_STAGE_FIELDS = (
    "stage_id",
    "stage_key",
    "name",
    "owner",
    "status",
    "status_basis",
    "artifacts",
    "evidence",
    "depends",
    "gaps",
    "inferred",
)
REQUIRED_BREAKPOINT_FIELDS = (
    "breakpoint_id",
    "stage_id",
    "title",
    "severity",
    "blocking",
    "detail",
    "evidence",
    "recommendation",
    "inferred",
)
REQUIRED_DECLARED = (
    "engineering_status",
    "cross_project_status",
    "completion_status",
    "real_kds_write_authorized",
    "long_term_memory_write_authorized",
    "business_state_change_authorized",
    "status_promotion_authorized",
)
STATUS_VALUES = ("S0", "S1", "S2", "S3", "pending", "unknown")
INCOMPLETE_STATUSES = ("S0", "S1", "S2", "pending", "unknown")
SEVERITY_ORDER = ("P0", "P1", "P2")
COMPLETION_FORBIDDEN = ("complete", "completed", "accepted", "done", "closed")

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,80}$")

FORBIDDEN_KEY_PARTS = (
    "token",
    "secret",
    "password",
    "passwd",
    "api_key",
    "apikey",
    "api-key",
    "credential",
    "private_key",
    "access_key",
    "client_secret",
    "cookie",
    "authorization",
    "bearer",
)
SECRET_VALUE_PATTERNS: Sequence[re.Pattern[str]] = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*\S{8,}"),
)

ERRORS: List[str] = []
WARNINGS: List[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def rel(path: Path) -> str:
    for base, label in ((ROOT, ""), (WORKSPACE, "../")):
        try:
            return label + str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_str_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(non_empty_str(v) for v in value)


def resolve_path(raw: str) -> Tuple[Optional[Path], List[str]]:
    cleaned = raw.split("#", 1)[0].strip()
    tried: List[str] = []
    candidate = Path(cleaned)
    if candidate.is_absolute():
        tried.append(str(candidate))
        return (candidate if candidate.is_file() else None), tried
    for base in (ROOT, WORKSPACE):
        target = base / cleaned
        tried.append(rel(target))
        if target.is_file():
            return target, tried
    return None, tried


def check_paths(label: str, paths: Any, field: str) -> None:
    if not non_empty_str_list(paths):
        fail(f"{label} 的 {field} 必须是非空字符串列表")
        return
    seen = set()
    for raw in paths:
        if raw in seen:
            fail(f"{label} 的 {field} 含重复路径：{raw}")
            continue
        seen.add(raw)
        resolved, tried = resolve_path(raw)
        if resolved is None:
            fail(f"{label} 的 {field} 路径不存在：{raw}（尝试：{tried}）")


def walk_scalars(node: Any, path: str = "") -> List[Tuple[str, str]]:
    found: List[Tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            key_text = str(key)
            found.append((path + "/" + key_text + "#key", key_text))
            found.extend(walk_scalars(value, path + "/" + key_text))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(walk_scalars(value, f"{path}[{index}]"))
    elif isinstance(node, (str, int, float, bool)):
        found.append((path, str(node)))
    return found


def check_sensitive(node: Any) -> None:
    for where, text in walk_scalars(node):
        if where.endswith("#key"):
            lowered = text.lower()
            for part in FORBIDDEN_KEY_PARTS:
                if part in lowered:
                    fail(f"敏感字段名：{where} -> {text}（不允许登记凭据类字段）")
                    break
            continue
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(text):
                fail(f"疑似密钥值：{where} 命中 {pattern.pattern}")
                break


def check_top_level(data: Dict[str, Any]) -> None:
    for field in REQUIRED_TOP:
        if field not in data:
            fail(f"顶层缺字段：{field}")
    if not isinstance(data.get("schema_version"), int):
        fail("schema_version 必须是整数")
    for field in ("matrix_id", "generated_at", "owner", "engineering_domain", "canonical_feature", "scope"):
        if field in data and not non_empty_str(data.get(field)):
            fail(f"顶层字段 {field} 必须是非空字符串")

    for flag in ("source_of_truth", "chain_closed"):
        if not isinstance(data.get(flag), bool):
            fail(f"{flag} 必须是布尔值")
    if data.get("source_of_truth") is True:
        fail("source_of_truth 必须为 false：本矩阵是链路索引，不是契约本体")
    if data.get("chain_closed") is True:
        fail("chain_closed 必须为 false：本任务不声明链路闭环")

    scale = data.get("stage_scale")
    if not isinstance(scale, dict):
        fail("stage_scale 必须是 mapping")
    else:
        for key in REQUIRED_SCALE_KEYS:
            if key not in scale:
                fail(f"stage_scale 缺状态定义：{key}")
            elif not non_empty_str(scale.get(key)):
                fail(f"stage_scale.{key} 必须是非空字符串")

    declared = data.get("declared_status")
    if not isinstance(declared, dict):
        fail("declared_status 必须是 mapping")
    else:
        for field in REQUIRED_DECLARED:
            if field not in declared:
                fail(f"declared_status 缺字段：{field}")
        completion = str(declared.get("completion_status", "")).strip().lower()
        if completion in COMPLETION_FORBIDDEN:
            fail(f"declared_status.completion_status 不得声明完成类结论：{declared.get('completion_status')}")
        for flag in ("real_kds_write_authorized", "long_term_memory_write_authorized",
                     "business_state_change_authorized", "status_promotion_authorized"):
            if declared.get(flag) is not False:
                fail(f"declared_status.{flag} 必须为 false（本任务不授权任何写入或状态提升）")


def check_stages(data: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    stages = data.get("stages")
    if not isinstance(stages, list) or not stages:
        fail("stages 必须是非空列表")
        return {}, []

    by_id: Dict[str, Dict[str, Any]] = {}
    key_counts: Dict[str, int] = {}
    order: List[str] = []

    for index, item in enumerate(stages):
        if not isinstance(item, dict):
            fail(f"stages[{index}] 不是 mapping")
            continue
        stage_id = item.get("stage_id")
        label = f"stages[{index}]({stage_id})"
        for field in REQUIRED_STAGE_FIELDS:
            if field not in item:
                fail(f"{label} 缺必填字段：{field}")

        if not non_empty_str(stage_id):
            fail(f"{label} stage_id 必须是非空字符串")
            continue
        if not ID_PATTERN.match(stage_id):
            fail(f"{label} stage_id 格式非法：{stage_id}")
        if stage_id in by_id:
            fail(f"stage_id 重复：{stage_id}")
            continue
        by_id[stage_id] = item
        order.append(stage_id)

        stage_key = item.get("stage_key")
        if stage_key not in REQUIRED_STAGE_KEYS:
            fail(f"{label} stage_key 非法：{stage_key!r}，允许 {REQUIRED_STAGE_KEYS}")
        else:
            key_counts[stage_key] = key_counts.get(stage_key, 0) + 1

        for field in ("name", "owner", "status_basis"):
            if not non_empty_str(item.get(field)):
                fail(f"{label} {field} 必须是非空字符串")
        if not isinstance(item.get("inferred"), bool):
            fail(f"{label} inferred 必须是布尔值")

        check_status(label, item)
        check_paths(label, item.get("artifacts"), "artifacts")
        check_paths(label, item.get("evidence"), "evidence")

        depends = item.get("depends")
        if not isinstance(depends, list) or not all(non_empty_str(v) for v in depends):
            fail(f"{label} depends 必须是字符串列表（可为空列表）")
        elif stage_id in depends:
            fail(f"{label} depends 不得包含自身")

        gaps = item.get("gaps")
        if not isinstance(gaps, list) or not all(non_empty_str(v) for v in gaps):
            fail(f"{label} gaps 必须是字符串列表")
        elif item.get("status") in INCOMPLETE_STATUSES and not gaps:
            fail(f"{label} 未完成环节（status={item.get('status')}）必须至少登记 1 条 gap")

    for required in REQUIRED_STAGE_KEYS:
        if key_counts.get(required, 0) != 1:
            fail(f"环节缺失或重复：stage_key={required}（出现 {key_counts.get(required, 0)} 次，必须恰好 1 次）")

    check_depends(by_id)
    return by_id, order


def check_status(label: str, item: Dict[str, Any]) -> None:
    status = item.get("status")
    if status not in STATUS_VALUES:
        fail(f"{label} status 非法：{status!r}，允许 {STATUS_VALUES}")
        return
    if status == "unknown" and item.get("inferred") is not True:
        fail(f"{label} status=unknown 时必须同时声明 inferred: true")


def check_depends(by_id: Dict[str, Dict[str, Any]]) -> None:
    for stage_id, item in by_id.items():
        for dep in item.get("depends") or []:
            if dep not in by_id:
                fail(f"{stage_id} 的 depends 引用了不存在的环节：{dep}")

    # 环检测（三色 DFS）
    state: Dict[str, int] = {}

    def visit(node: str, trail: List[str]) -> None:
        if state.get(node) == 2:
            return
        if state.get(node) == 1:
            fail(f"depends 存在环：{' -> '.join(trail + [node])}")
            return
        state[node] = 1
        for dep in by_id.get(node, {}).get("depends") or []:
            if dep in by_id:
                visit(dep, trail + [node])
        state[node] = 2

    for stage_id in by_id:
        visit(stage_id, [])


def check_breakpoints(
    data: Dict[str, Any], stage_ids: Sequence[str]
) -> Dict[str, Dict[str, Any]]:
    breakpoints = data.get("breakpoints")
    if not isinstance(breakpoints, list) or not breakpoints:
        fail("breakpoints 必须是非空列表")
        return {}

    by_id: Dict[str, Dict[str, Any]] = {}
    last_rank = -1
    for index, item in enumerate(breakpoints):
        if not isinstance(item, dict):
            fail(f"breakpoints[{index}] 不是 mapping")
            continue
        breakpoint_id = item.get("breakpoint_id")
        label = f"breakpoints[{index}]({breakpoint_id})"
        for field in REQUIRED_BREAKPOINT_FIELDS:
            if field not in item:
                fail(f"{label} 缺必填字段：{field}")
        if not non_empty_str(breakpoint_id):
            fail(f"{label} breakpoint_id 必须是非空字符串")
            continue
        if breakpoint_id in by_id:
            fail(f"breakpoint_id 重复：{breakpoint_id}")
            continue
        by_id[breakpoint_id] = item

        for field in ("title", "detail", "recommendation"):
            if not non_empty_str(item.get(field)):
                fail(f"{label} {field} 必须是非空字符串")
        if not isinstance(item.get("inferred"), bool):
            fail(f"{label} inferred 必须是布尔值")
        if not isinstance(item.get("blocking"), bool):
            fail(f"{label} blocking 必须是布尔值")
        if item.get("stage_id") not in stage_ids:
            fail(f"{label} stage_id 未指向已定义环节：{item.get('stage_id')!r}")
        severity = item.get("severity")
        if severity not in SEVERITY_ORDER:
            fail(f"{label} severity 非法：{severity!r}，允许 {SEVERITY_ORDER}")
        else:
            rank = SEVERITY_ORDER.index(str(severity))
            if rank < last_rank:
                fail(f"{label} 断点未按 P0→P1→P2 排序（{severity} 出现在其后）")
            last_rank = max(last_rank, rank)
        check_paths(label, item.get("evidence"), "evidence")

    return by_id


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="校验 GlobalCloud GKE-001 知识工程链路矩阵")
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="矩阵文件路径")
    args = parser.parse_args(argv)

    matrix_path = Path(args.matrix)
    if not matrix_path.is_file():
        print(f"FAIL validate_gke001_chain_matrix: 矩阵不存在：{matrix_path}", file=sys.stderr)
        return 2
    try:
        data = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        print(f"FAIL validate_gke001_chain_matrix: YAML 解析失败：{error}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("FAIL validate_gke001_chain_matrix: 顶层必须是 mapping", file=sys.stderr)
        return 2

    check_top_level(data)
    stages, order = check_stages(data)
    breakpoints = check_breakpoints(data, order)
    check_sensitive(data)

    if ERRORS:
        for message in ERRORS:
            print(f"FAIL {message}")
        for message in WARNINGS:
            print(f"WARN {message}")
        print(f"FAIL validate_gke001_chain_matrix: {len(ERRORS)} 项校验失败（matrix={matrix_path}）")
        return 1

    for message in WARNINGS:
        print(f"WARN {message}")

    status_counts: Dict[str, int] = {}
    for item in stages.values():
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
    severity_counts: Dict[str, int] = {}
    blocking = 0
    for item in breakpoints.values():
        severity = str(item.get("severity"))
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        if item.get("blocking") is True:
            blocking += 1

    declared = data.get("declared_status") or {}
    print("PASS validate_gke001_chain_matrix")
    print(f"  matrix         : {matrix_path}")
    print(f"  domain         : {data.get('engineering_domain')}（canonical_feature={data.get('canonical_feature')}）")
    print(f"  chain_closed   : {data.get('chain_closed')}（source_of_truth={data.get('source_of_truth')}）")
    print(
        f"  declared       : engineering={declared.get('engineering_status')}"
        f" cross_project={declared.get('cross_project_status')}"
        f" completion={declared.get('completion_status')}"
    )
    print(f"  stages         : {len(stages)} 个环节")
    for stage_id in order:
        item = stages[stage_id]
        print(
            f"    - {stage_id}: key={item['stage_key']} status={item['status']}"
            f" owner={item['owner']} artifacts={len(item['artifacts'])}"
            f" evidence={len(item['evidence'])} gaps={len(item['gaps'])}"
        )
    distribution = " ".join(f"{name}={status_counts.get(name, 0)}" for name in ("S0", "S1", "S2", "S3", "pending"))
    print(f"  status_dist    : {distribution}")
    sev = " ".join(f"{name}={severity_counts.get(name, 0)}" for name in SEVERITY_ORDER)
    print(f"  breakpoints    : {len(breakpoints)} 条（{sev}，blocking={blocking}）")
    print(
        "  checks         : schema=pass stages=pass unique_id=pass artifacts=pass evidence=pass "
        "status=pass depends=pass gaps=pass breakpoints_order=pass no_closure_claim=pass sensitive=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
