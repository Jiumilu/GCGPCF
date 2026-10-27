#!/usr/bin/env python3
"""校验 GlobalCloud 项目群能力资产注册表（PG-09 能力复用中台）。

用途
----
只读校验 `runtime/asset-registry/registry.yaml`：检查顶层 schema、条目必填字段、
asset id 唯一性、type / status 白名单、source_path 真实存在、license 非空、
reused_by 为项目名列表且与 reuse_count 一致、四类覆盖、复用项目数下限，
以及条目不包含凭据类键名或密钥形态的值。

本脚本不写任何文件，不修改注册表，不声明任何项目状态。

用法
----
    python3 tools/kds-sync/validate_asset_registry.py
    python3 tools/kds-sync/validate_asset_registry.py --registry /tmp/registry.yaml
    python3 tools/kds-sync/validate_asset_registry.py --min-assets 20 --min-reuse-projects 3

退出码
------
    0  全部校验通过
    1  存在校验失败项
    2  注册表文件缺失或不是合法 YAML

schema 约定（兼容 bootstrap）
----------------------------
- 顶层：schema_version / registry_status / owner / domain / updated / source_tasks / entries
  其中 `entries` 即资产列表（等价于 PG-09 规格中的 assets）。
- 顶层可选 `bootstrap_entries`：列出由并行会话在 2026-10-22 建立、只按基础字段校验的
  条目 id；这些条目不要求扩展字段（source_path / reused_by / reuse_count / status / notes），
  且允许使用 `capability_service` 这一 bootstrap 类型。bootstrap 条目不得被本任务改写。
- 其余条目必须补齐扩展字段，并使用 prompt / skill / template / component 四类之一。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - 环境缺 PyYAML 时给出可读退出口
    print("FAIL validate_asset_registry: 缺少 PyYAML（pip install pyyaml）", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
DEFAULT_REGISTRY = ROOT / "runtime/asset-registry/registry.yaml"

REQUIRED_TOP = (
    "schema_version",
    "registry_status",
    "owner",
    "domain",
    "updated",
    "source_tasks",
    "entries",
)
REQUIRED_ENTRY = (
    "id",
    "title",
    "version",
    "type",
    "owner",
    "governor",
    "scope",
    "access",
    "license",
    "evidence",
    "constraints",
)
REQUIRED_EXTENSION = ("source_path", "reused_by", "reuse_count", "status", "notes")

ASSET_TYPES = ("prompt", "skill", "template", "component")
BOOTSTRAP_TYPES = ("capability_service",)
ALLOWED_TYPES = ASSET_TYPES + BOOTSTRAP_TYPES
STATUS_VALUES = ("active", "draft", "deprecated")

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{1,80}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]{0,40}$")

# 凭据类键名：命中即失败（不允许在注册表里登记凭据字段）
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

# 密钥形态的值：命中即失败
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
    """尽量以仓库根相对路径显示，便于比对。"""
    for base, label in ((ROOT, ""), (WORKSPACE, "../")):
        try:
            return label + str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_str_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) > 0
        and all(non_empty_str(item) for item in value)
    )


def license_ok(value: Any) -> bool:
    """license 允许字符串或 mapping；两种形态都必须非空。"""
    if non_empty_str(value):
        return True
    if isinstance(value, dict) and value:
        return all(non_empty_str(str(item)) for item in value.values())
    return False


def resolve_source_path(raw: str) -> Tuple[Optional[Path], List[str]]:
    """解析 source_path。

    解析顺序：绝对路径 → GPCF 仓库根相对 → 工作区根相对。
    返回 (命中路径, 尝试过的位置描述列表)。
    """
    tried: List[str] = []
    candidate = Path(raw)
    if candidate.is_absolute():
        tried.append(str(candidate))
        return (candidate if candidate.is_file() else None), tried
    for base in (ROOT, WORKSPACE):
        target = base / raw
        tried.append(rel(target))
        if target.is_file():
            return target, tried
    return None, tried


def walk_scalars(node: Any, path: str = "") -> List[Tuple[str, str]]:
    """展开 YAML 结构，返回 (字段路径, 字符串值) 列表。"""
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
    """检查凭据类键名与密钥形态的值。"""
    for where, text in walk_scalars(node):
        lowered = text.lower()
        if where.endswith("#key"):
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
    """校验顶层 schema，返回 bootstrap 条目 id 列表。"""
    for field in REQUIRED_TOP:
        if field not in data:
            fail(f"顶层缺字段：{field}")
    if "schema_version" in data and not isinstance(data["schema_version"], int):
        fail("schema_version 必须是整数")
    if "updated" in data and not DATE_PATTERN.match(str(data.get("updated", ""))):
        fail("updated 必须是 YYYY-MM-DD")
    for field in ("registry_status", "owner", "domain"):
        if field in data and not non_empty_str(data[field]):
            fail(f"顶层字段 {field} 必须是非空字符串")
    if "source_tasks" in data and not non_empty_str_list(data["source_tasks"]):
        fail("source_tasks 必须是非空列表")
    for optional in ("generated_at", "usage_rule", "extension_phase"):
        if optional in data and not non_empty_str(data[optional]):
            fail(f"顶层可选字段 {optional} 存在时必须是非空字符串")

    bootstrap = data.get("bootstrap_entries", [])
    if not isinstance(bootstrap, list) or not all(isinstance(item, str) for item in bootstrap):
        fail("bootstrap_entries 必须是字符串列表")
        bootstrap = []
    return list(bootstrap)


def check_entry(index: int, entry: Any, bootstrap_ids: Sequence[str]) -> Optional[str]:
    """校验单条资产，返回其 id（用于唯一性汇总）。"""
    if not isinstance(entry, dict):
        fail(f"entries[{index}] 不是 mapping")
        return None

    entry_id = entry.get("id")
    label = f"entries[{index}]({entry_id})"

    for field in REQUIRED_ENTRY:
        if field not in entry:
            fail(f"{label} 缺必填字段：{field}")

    if not non_empty_str(entry_id):
        fail(f"{label} 的 id 必须是非空字符串")
        return None
    if not ID_PATTERN.match(entry_id):
        fail(f"{label} 的 id 格式非法（小写字母数字加点/下划线/连字符）：{entry_id}")

    if not non_empty_str(entry.get("title")):
        fail(f"{label} title 必须是非空字符串")
    if not non_empty_str(entry.get("version")):
        fail(f"{label} version 必须是非空字符串")
    if not non_empty_str(entry.get("owner")):
        fail(f"{label} owner 必须是非空字符串")
    if not non_empty_str(entry.get("governor")):
        fail(f"{label} governor 必须是非空字符串")
    if not non_empty_str(entry.get("access")):
        fail(f"{label} access 必须是非空字符串")
    if not non_empty_str_list(entry.get("scope")):
        fail(f"{label} scope 必须是非空字符串列表")
    if not non_empty_str_list(entry.get("evidence")):
        fail(f"{label} evidence 必须是非空字符串列表")
    if not non_empty_str_list(entry.get("constraints")):
        fail(f"{label} constraints 必须是非空字符串列表")
    if "license" in entry and not license_ok(entry.get("license")):
        fail(f"{label} license 不能为空（字符串非空，或 mapping 的每个值非空）")

    entry_type = entry.get("type")
    if entry_type not in ALLOWED_TYPES:
        fail(f"{label} type 非法：{entry_type!r}，允许 {ALLOWED_TYPES}")
    elif entry_type in BOOTSTRAP_TYPES and entry_id not in bootstrap_ids:
        fail(f"{label} 只有 bootstrap_entries 中的条目可以使用类型 {entry_type}")

    is_bootstrap = entry_id in bootstrap_ids
    if not is_bootstrap:
        for field in REQUIRED_EXTENSION:
            if field not in entry:
                fail(f"{label} 缺扩展字段：{field}（非 bootstrap 条目必须补齐）")

        source_path = entry.get("source_path")
        if field_present(entry, "source_path"):
            if not non_empty_str(source_path):
                fail(f"{label} source_path 必须是非空字符串")
            else:
                resolved, tried = resolve_source_path(source_path)
                if resolved is None:
                    fail(f"{label} source_path 不存在：{source_path}（尝试：{tried}）")

        reused_by = entry.get("reused_by")
        if field_present(entry, "reused_by"):
            if not non_empty_str_list(reused_by):
                fail(f"{label} reused_by 必须是非空的项目名列表")
                reused_by = []
            else:
                for project in reused_by:
                    if not PROJECT_NAME_PATTERN.match(project):
                        fail(f"{label} reused_by 含非法项目名：{project!r}")
                if len(set(reused_by)) != len(reused_by):
                    fail(f"{label} reused_by 存在重复项目：{reused_by}")
                reuse_count = entry.get("reuse_count")
                if field_present(entry, "reuse_count"):
                    if not isinstance(reuse_count, int) or isinstance(reuse_count, bool):
                        fail(f"{label} reuse_count 必须是整数")
                    elif reuse_count != len(set(reused_by)):
                        fail(
                            f"{label} reuse_count={reuse_count} 与 reused_by 去重项目数 "
                            f"{len(set(reused_by))} 不一致"
                        )
                if entry.get("reuse_basis") not in (None, "verified_reference", "artifact_usage"):
                    fail(f"{label} reuse_basis 只能是 verified_reference / artifact_usage")

        if field_present(entry, "status") and entry.get("status") not in STATUS_VALUES:
            fail(f"{label} status 非法：{entry.get('status')!r}，允许 {STATUS_VALUES}")

        if field_present(entry, "notes") and not non_empty_str(entry.get("notes")):
            fail(f"{label} notes 必须是非空字符串")

        if non_empty_str(entry_type) and not str(entry_id).startswith(f"{entry_type}."):
            warn(f"{label} id 建议以 '{entry_type}.' 前缀开头")

    return entry_id


def field_present(entry: Dict[str, Any], field: str) -> bool:
    return field in entry


def check_entries(entries: Any, bootstrap_ids: Sequence[str]) -> List[Dict[str, Any]]:
    if not isinstance(entries, list) or not entries:
        fail("entries 必须是非空列表")
        return []

    seen: Dict[str, int] = {}
    valid_entries: List[Dict[str, Any]] = []
    for index, entry in enumerate(entries):
        entry_id = check_entry(index, entry, bootstrap_ids)
        if entry_id:
            key = entry_id.casefold()
            if key in seen:
                fail(f"asset id 重复：{entry_id}（entries[{seen[key]}] 与 entries[{index}]）")
            else:
                seen[key] = index
        if isinstance(entry, dict):
            valid_entries.append(entry)
    return valid_entries


def check_coverage(
    entries: Sequence[Dict[str, Any]], min_assets: int, min_reuse_projects: int
) -> Tuple[Dict[str, int], List[str]]:
    type_counts: Dict[str, int] = {}
    for entry in entries:
        entry_type = str(entry.get("type"))
        type_counts[entry_type] = type_counts.get(entry_type, 0) + 1

    four_type_total = sum(type_counts.get(name, 0) for name in ASSET_TYPES)
    if four_type_total < min_assets:
        fail(f"四类资产总数 {four_type_total} < 下限 {min_assets}")
    for name in ASSET_TYPES:
        if type_counts.get(name, 0) == 0:
            fail(f"type 覆盖缺失：没有任何 {name} 类资产")

    reuse_projects = set()
    for entry in entries:
        reused_by = entry.get("reused_by")
        if isinstance(reused_by, list):
            reuse_projects.update(item for item in reused_by if isinstance(item, str))
    if len(reuse_projects) < min_reuse_projects:
        fail(f"复用项目数 {len(reuse_projects)} < 下限 {min_reuse_projects}")
    return type_counts, sorted(reuse_projects)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="校验 GlobalCloud 能力资产注册表")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="注册表路径")
    parser.add_argument("--min-assets", type=int, default=20, help="四类资产数量下限")
    parser.add_argument("--min-reuse-projects", type=int, default=3, help="复用项目数下限")
    args = parser.parse_args(argv)

    registry_path = Path(args.registry)
    if not registry_path.is_file():
        print(f"FAIL validate_asset_registry: 注册表不存在：{registry_path}", file=sys.stderr)
        return 2

    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        print(f"FAIL validate_asset_registry: YAML 解析失败：{error}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("FAIL validate_asset_registry: 顶层必须是 mapping", file=sys.stderr)
        return 2

    bootstrap_ids = check_top_level(data)
    entries = check_entries(data.get("entries"), bootstrap_ids)
    type_counts, reuse_projects = check_coverage(
        entries, args.min_assets, args.min_reuse_projects
    )
    check_sensitive(data)

    if ERRORS:
        for message in ERRORS:
            print(f"FAIL {message}")
        for message in WARNINGS:
            print(f"WARN {message}")
        print(f"FAIL validate_asset_registry: {len(ERRORS)} 项校验失败（registry={registry_path}）")
        return 1

    for message in WARNINGS:
        print(f"WARN {message}")

    four_type_total = sum(type_counts.get(name, 0) for name in ASSET_TYPES)
    distribution = " ".join(f"{name}={type_counts.get(name, 0)}" for name in ASSET_TYPES)
    legacy = " ".join(
        f"{name}={type_counts[name]}" for name in BOOTSTRAP_TYPES if type_counts.get(name)
    )
    print("PASS validate_asset_registry")
    print(f"  registry        : {registry_path}")
    print(
        f"  schema_version  : {data.get('schema_version')}"
        f" (registry_status={data.get('registry_status')}, updated={data.get('updated')})"
    )
    print(f"  entries         : {len(entries)} 条（四类 {four_type_total} 条{', ' + legacy if legacy else ''}）")
    print(f"  type_distribution: {distribution}")
    print(f"  reuse_projects  : {len(reuse_projects)} 个 -> {', '.join(reuse_projects)}")
    print(
        "  checks          : schema=pass unique_id=pass type=pass source_path=pass "
        "license=pass reused_by=pass coverage=pass sensitive=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
