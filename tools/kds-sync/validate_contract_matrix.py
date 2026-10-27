#!/usr/bin/env python3
"""校验 GlobalCloud 项目群跨项目契约矩阵（PG-12 inventory 版）。

用途
----
只读校验 `runtime/contract-matrix.yaml`：检查顶层 schema、三套契约（xap / event / knowledge）
是否各有条目、contract_id 唯一、schema_paths 与 evidence 指向的文件真实存在、version / status
非空（`unknown` 必须同时标 `inferred: true`）、consumers 是项目名列表、每个契约引用的冲突点
存在且冲突表字段完整、必检冲突主题（contentDigest / 错误码 / 字段命名 / 版本语义 / 签名边界）
被覆盖，以及不包含凭据类键名或密钥形态的值。

本脚本不写任何文件，不修改矩阵，不声明契约已收敛或已集成。

用法
----
    python3 tools/kds-sync/validate_contract_matrix.py
    python3 tools/kds-sync/validate_contract_matrix.py --matrix /tmp/contract-matrix.yaml

退出码
------
    0  全部校验通过
    1  存在校验失败项
    2  矩阵文件缺失或不是合法 YAML

路径解析
--------
`schema_paths` / `evidence` / 冲突 `evidence` 中的相对路径按以下顺序解析：
绝对路径 → GPCF 仓库根 → 工作区根（GPCF 的上级目录）。允许 `path#段落` 形式的片段标注。
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
    print("FAIL validate_contract_matrix: 缺少 PyYAML（pip install pyyaml）", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
DEFAULT_MATRIX = ROOT / "runtime/contract-matrix.yaml"

REQUIRED_TOP = (
    "schema_version",
    "matrix_id",
    "generated_at",
    "owner",
    "scope",
    "source_of_truth",
    "contract_sets",
    "contracts",
    "conflicts",
)
REQUIRED_SETS = ("xap", "event", "knowledge")
REQUIRED_CONTRACT = (
    "contract_id",
    "contract_set",
    "name",
    "owner",
    "version",
    "status",
    "schema_paths",
    "evidence",
    "consumers",
    "compat_rule",
    "conflicts",
    "open_questions",
    "inferred",
)
REQUIRED_CONFLICT = (
    "conflict_id",
    "topic",
    "severity",
    "contracts",
    "description",
    "evidence",
    "impact",
    "recommendation",
    "status",
    "inferred",
)
SEVERITY_VALUES = ("high", "medium", "low")
CONFLICT_STATUS_VALUES = ("open", "mitigated", "closed")

# 必检冲突主题：主题名 -> 判定用正则（对 topic + description 文本匹配）
REQUIRED_CONFLICT_THEMES: Sequence[Tuple[str, str]] = (
    ("contentDigest 口径", r"contentDigest|content_digest|摘要"),
    ("WAME 错误码", r"错误码|错误代码|XAP-[0-9]{4}"),
    ("字段命名", r"字段命名|命名|camelCase|snake_case|casing"),
    ("版本语义", r"版本"),
    ("XAP 签名/无签名边界", r"签名|signature"),
)

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,80}$")
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]{0,40}$")

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
    """解析相对/绝对路径；允许 path#fragment 片段标注。"""
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


def check_top_level(data: Dict[str, Any]) -> List[str]:
    """校验顶层字段，返回声明的契约集合 id 列表。"""
    for field in REQUIRED_TOP:
        if field not in data:
            fail(f"顶层缺字段：{field}")
    if not isinstance(data.get("schema_version"), int):
        fail("schema_version 必须是整数")
    for field in ("matrix_id", "generated_at", "owner", "scope"):
        if field in data and not non_empty_str(data.get(field)):
            fail(f"顶层字段 {field} 必须是非空字符串")
    if not isinstance(data.get("source_of_truth"), bool):
        fail("source_of_truth 必须是布尔值（矩阵是索引，不得自称为契约本体）")
    elif data.get("source_of_truth"):
        fail("source_of_truth 必须为 false：本矩阵只是索引，不是契约本体")

    sets = data.get("contract_sets")
    set_ids: List[str] = []
    if not isinstance(sets, list) or not sets:
        fail("contract_sets 必须是非空列表")
        return set_ids
    for index, item in enumerate(sets):
        if not isinstance(item, dict):
            fail(f"contract_sets[{index}] 不是 mapping")
            continue
        set_id = item.get("set_id")
        if not non_empty_str(set_id):
            fail(f"contract_sets[{index}] 缺 set_id")
            continue
        if set_id in set_ids:
            fail(f"contract_sets 中 set_id 重复：{set_id}")
        set_ids.append(set_id)
        if not non_empty_str(item.get("name")):
            fail(f"contract_sets[{index}]({set_id}) 缺 name")
    for required in REQUIRED_SETS:
        if required not in set_ids:
            fail(f"契约集合缺失：{required}（必须覆盖 {'/'.join(REQUIRED_SETS)}）")
    return set_ids


def check_conflicts(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """校验冲突表，返回 conflict_id -> 冲突条目。"""
    conflicts = data.get("conflicts")
    if not isinstance(conflicts, list) or not conflicts:
        fail("conflicts 必须是非空列表")
        return {}

    by_id: Dict[str, Dict[str, Any]] = {}
    for index, item in enumerate(conflicts):
        if not isinstance(item, dict):
            fail(f"conflicts[{index}] 不是 mapping")
            continue
        conflict_id = item.get("conflict_id")
        label = f"conflicts[{index}]({conflict_id})"
        for field in REQUIRED_CONFLICT:
            if field not in item:
                fail(f"{label} 缺必填字段：{field}")
        if not non_empty_str(conflict_id):
            fail(f"{label} 缺 conflict_id")
            continue
        if not ID_PATTERN.match(conflict_id):
            fail(f"{label} conflict_id 格式非法：{conflict_id}")
        if conflict_id in by_id:
            fail(f"conflict_id 重复：{conflict_id}")
            continue
        by_id[conflict_id] = item

        if not non_empty_str(item.get("topic")):
            fail(f"{label} topic 必须是非空字符串")
        if item.get("severity") not in SEVERITY_VALUES:
            fail(f"{label} severity 非法：{item.get('severity')!r}，允许 {SEVERITY_VALUES}")
        if item.get("status") not in CONFLICT_STATUS_VALUES:
            fail(f"{label} status 非法：{item.get('status')!r}，允许 {CONFLICT_STATUS_VALUES}")
        if not isinstance(item.get("inferred"), bool):
            fail(f"{label} inferred 必须是布尔值")
        if not non_empty_str_list(item.get("contracts")):
            fail(f"{label} contracts 必须是契约 id 列表")
        for field in ("description", "impact", "recommendation"):
            if not non_empty_str(item.get(field)):
                fail(f"{label} {field} 必须是非空字符串")
        check_paths(label, item.get("evidence"), "evidence")

    check_theme_coverage(by_id)
    return by_id


def check_theme_coverage(by_id: Dict[str, Dict[str, Any]]) -> None:
    """必检冲突主题覆盖：任一冲突的 topic+description 命中即算覆盖。"""
    corpus = "\n".join(
        f"{item.get('topic', '')} {item.get('description', '')}" for item in by_id.values()
    )
    for theme, pattern in REQUIRED_CONFLICT_THEMES:
        if not re.search(pattern, corpus):
            fail(f"必检冲突主题未覆盖：{theme}（无任何冲突条目命中 /{pattern}/）")


def check_contracts(
    contracts: Any, set_ids: Sequence[str], conflict_ids: Sequence[str]
) -> List[Dict[str, Any]]:
    if not isinstance(contracts, list) or not contracts:
        fail("contracts 必须是非空列表")
        return []

    seen: Dict[str, int] = {}
    per_set: Dict[str, int] = {}
    valid: List[Dict[str, Any]] = []

    for index, item in enumerate(contracts):
        if not isinstance(item, dict):
            fail(f"contracts[{index}] 不是 mapping")
            continue
        valid.append(item)
        contract_id = item.get("contract_id")
        label = f"contracts[{index}]({contract_id})"

        for field in REQUIRED_CONTRACT:
            if field not in item:
                fail(f"{label} 缺必填字段：{field}")

        if not non_empty_str(contract_id):
            fail(f"{label} contract_id 必须是非空字符串")
            continue
        if not ID_PATTERN.match(contract_id):
            fail(f"{label} contract_id 格式非法：{contract_id}")
        if contract_id in seen:
            fail(f"contract_id 重复：{contract_id}（contracts[{seen[contract_id]}] 与 [{index}]）")
        else:
            seen[contract_id] = index

        contract_set = item.get("contract_set")
        if contract_set not in set_ids:
            fail(f"{label} contract_set 非法或未声明：{contract_set!r}（已声明 {set_ids}）")
        else:
            per_set[contract_set] = per_set.get(contract_set, 0) + 1

        if not non_empty_str(item.get("name")):
            fail(f"{label} name 必须是非空字符串")
        if not non_empty_str(item.get("owner")):
            fail(f"{label} owner 必须是非空字符串")
        if not non_empty_str(item.get("compat_rule")):
            fail(f"{label} compat_rule 必须是非空字符串")
        if not non_empty_str_list(item.get("open_questions")):
            fail(f"{label} open_questions 必须是非空字符串列表")
        if not isinstance(item.get("inferred"), bool):
            fail(f"{label} inferred 必须是布尔值")

        check_version_status(label, item)
        check_paths(label, item.get("schema_paths"), "schema_paths")
        check_paths(label, item.get("evidence"), "evidence")

        consumers = item.get("consumers")
        if not non_empty_str_list(consumers):
            fail(f"{label} consumers 必须是非空的项目名列表")
        else:
            for project in consumers:
                if not PROJECT_NAME_PATTERN.match(project):
                    fail(f"{label} consumers 含非法项目名：{project!r}")
            if len(set(consumers)) != len(consumers):
                fail(f"{label} consumers 存在重复项目：{consumers}")

        declared_conflicts = item.get("conflicts")
        if not non_empty_str_list(declared_conflicts):
            fail(f"{label} conflicts 必须是冲突 id 列表")
        else:
            for conflict_id in declared_conflicts:
                if conflict_id not in conflict_ids:
                    fail(f"{label} 引用了未定义的冲突：{conflict_id}")

    for set_id in REQUIRED_SETS:
        if per_set.get(set_id, 0) < 1:
            fail(f"契约集合 {set_id} 没有任何契约条目（三套契约至少各一条）")
    return valid


def check_version_status(label: str, item: Dict[str, Any]) -> None:
    inferred = item.get("inferred") is True
    for field in ("version", "status"):
        value = item.get(field)
        if not non_empty_str(value):
            fail(f"{label} {field} 不能为空（找不到真实依据请写 unknown 并置 inferred: true）")
            continue
        if value.strip().lower() == "unknown" and not inferred:
            fail(f"{label} {field}=unknown 时必须同时声明 inferred: true")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="校验 GlobalCloud 跨项目契约矩阵")
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="矩阵文件路径")
    args = parser.parse_args(argv)

    matrix_path = Path(args.matrix)
    if not matrix_path.is_file():
        print(f"FAIL validate_contract_matrix: 矩阵不存在：{matrix_path}", file=sys.stderr)
        return 2
    try:
        data = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        print(f"FAIL validate_contract_matrix: YAML 解析失败：{error}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("FAIL validate_contract_matrix: 顶层必须是 mapping", file=sys.stderr)
        return 2

    set_ids = check_top_level(data)
    conflicts = check_conflicts(data)
    contracts = check_contracts(data.get("contracts"), set_ids, list(conflicts))
    check_sensitive(data)

    if ERRORS:
        for message in ERRORS:
            print(f"FAIL {message}")
        for message in WARNINGS:
            print(f"WARN {message}")
        print(f"FAIL validate_contract_matrix: {len(ERRORS)} 项校验失败（matrix={matrix_path}）")
        return 1

    for message in WARNINGS:
        print(f"WARN {message}")

    print("PASS validate_contract_matrix")
    print(f"  matrix        : {matrix_path}")
    print(f"  matrix_id     : {data.get('matrix_id')}（source_of_truth={data.get('source_of_truth')}）")
    print(f"  contract_sets : {', '.join(set_ids)}")
    print(f"  contracts     : {len(contracts)} 条")
    for item in contracts:
        print(
            f"    - {item['contract_id']}: set={item['contract_set']}"
            f" version={item['version']} status={item['status']}"
            f" schema_paths={len(item['schema_paths'])} consumers={len(item['consumers'])}"
        )
    severity_counts: Dict[str, int] = {}
    for item in conflicts.values():
        severity = str(item.get("severity"))
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    distribution = " ".join(f"{name}={severity_counts.get(name, 0)}" for name in SEVERITY_VALUES)
    print(f"  conflicts     : {len(conflicts)} 条（{distribution}）")
    print(
        "  checks        : schema=pass contract_sets=pass unique_id=pass schema_paths=pass "
        "evidence_paths=pass version=pass consumers=pass conflict_links=pass themes=pass sensitive=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
