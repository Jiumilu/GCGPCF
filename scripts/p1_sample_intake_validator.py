#!/usr/bin/env python3
"""P1-C C1：sample-intake.yaml 离线校验器。

校验 P1-B sample intake 协议要求的最小字段集：
- 必填字段齐全、非空且为字符串（``authorization`` 必须为 mapping）；
- 枚举：``redaction_level``/``evidence_grade``/``priority``，以及存在时的
  ``layer``/``stage``/``scope``/``warranty``；
- ``type=demand`` 时 ``level`` 为 R1-R4，``type=defect`` 时为 S1-S4；
- ``authorization.approved_by`` 必须为「老卢」（违规时不回显原值）；
- 键级/值级敏感信息粗筛：email、手机号（+86/86/分隔符/空格）、18 位身份证、
  token/JWT/Base64、api_key、password、secret、credential，以及姓名/地址/
  金额/合同号等键名（含中文键）；命中输出 ``sensitive field detected: <path>``。
  可用 ``--allow-sensitive FIELD[=REASON]`` 重复豁免，并输出审计告警
  ``[WARN] sensitive exemption: <field> (reason: ...)``。

本脚本只做本地静态校验：不访问网络、不调用模型、不读取真实样本。
退出码：0 = 全部通过；1 = 存在违规；2 = 参数、读取或解码错误。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

REQUIRED_FIELDS: Tuple[str, ...] = (
    "sample_id",
    "type",
    "source_system",
    "source_ref_alias",
    "customer_alias",
    "layer",
    "stage",
    "contract_alias",
    "level",
    "priority",
    "evidence_grade",
    "redaction_level",
    "authorization",
    "owner",
)

APPROVER = "老卢"
TYPE_LEVEL_RULES: Dict[str, str] = {
    "demand": r"R[1-4]",
    "defect": r"S[1-4]",
}
YAML_SUFFIXES = {".yaml", ".yml"}

# 必填枚举字段（缺失/空已由必填校验覆盖；这里只校验非空字符串值）。
ENUM_FIELDS: Dict[str, Tuple[str, ...]] = {
    "redaction_level": ("R1", "R2", "R3"),
    "evidence_grade": ("E0", "E1", "E2", "E3"),
    "priority": ("P0", "P1", "P2", "P3"),
}
# 可选枚举字段：仅在字段存在且非空时校验。
OPTIONAL_ENUM_FIELDS: Dict[str, Tuple[str, ...]] = {
    "layer": ("personal", "team", "enterprise", "city"),
    "stage": ("test", "trial", "formal"),
    "scope": ("in", "out", "unknown"),
    "warranty": ("true", "false", "unknown"),
}

# 键级粗筛：键名压缩成小写字母数字后包含以下片段即视为敏感字段。
SENSITIVE_KEY_HINTS: Tuple[str, ...] = (
    "email",
    "phone",
    "mobile",
    "msisdn",
    "token",
    "apikey",
    "accesskey",
    "password",
    "passwd",
    "secret",
    "credential",
    "customername",
    "contactname",
    "realname",
    "idcard",
    "idnumber",
    "address",
    "bankaccount",
    "contractno",
    "amount",
    "price",
)
# 中文键名粗筛：直接对原键名做子串匹配。
SENSITIVE_KEY_CHINESE_HINTS: Tuple[str, ...] = (
    "姓名",
    "手机号",
    "电话",
    "身份证",
    "地址",
    "金额",
    "价格",
    "合同号",
)

# 值级粗筛：明显凭据格式 / 赋值形态 / 联系方式 / 身份号码。
SENSITIVE_VALUE_PATTERNS: Tuple[re.Pattern, ...] = (
    re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    # 大陆手机号：允许 +86/86 前缀与空格/连字符分隔。
    re.compile(
        r"(?<![0-9])(?:\+?86[\s-]?)?1[3-9](?:[\s-]?[0-9]){9}(?![0-9])"
    ),
    # 18 位身份证（17 位数字 + 数字/X 校验位）。
    re.compile(r"(?<![0-9A-Za-z])[0-9]{17}[0-9Xx](?![0-9A-Za-z])"),
    re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b"),
    # JWT（三段 Base64URL，首段以 eyJ 开头）。
    re.compile(
        r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b"
    ),
    re.compile(r"\beyJ[A-Za-z0-9_\-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{16,}"),
    re.compile(
        r"(?i)\b(?:password|passwd|secret|token|api[_-]?key)\s*[:=]\s*\S{3,}"
    ),
)
BASE64_BLOB_PATTERN = re.compile(r"[A-Za-z0-9+/]+={0,2}")


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _display(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    return repr(value)


def _type_name(value: Any) -> str:
    return type(value).__name__


def _last_key(path: str) -> str:
    without_indexes = re.sub(r"\[\d+\]", "", path)
    return without_indexes.rsplit(".", 1)[-1].strip().lower()


def _key_is_sensitive(key: str) -> bool:
    if any(hint in key for hint in SENSITIVE_KEY_CHINESE_HINTS):
        return True
    compact = re.sub(r"[^a-z0-9]+", "", key.lower())
    if not compact:
        return False
    if compact == "tel":
        return True
    return any(hint in compact for hint in SENSITIVE_KEY_HINTS)


def _looks_like_base64_blob(token: str) -> bool:
    """识别较长的 Base64 形态；短文本/纯小写 hash 不命中。"""
    if len(token) < 40:
        return False
    if BASE64_BLOB_PATTERN.fullmatch(token) is None:
        return False
    return (
        any(character.isupper() for character in token)
        and any(character.islower() for character in token)
        and any(character.isdigit() for character in token)
    )


def _value_is_sensitive(value: str) -> bool:
    if any(
        pattern.search(value) is not None for pattern in SENSITIVE_VALUE_PATTERNS
    ):
        return True
    for token in re.split(r"\s+", value):
        candidate = token.strip(".,;:!?()[]{}\"'`")
        if _looks_like_base64_blob(candidate):
            return True
    return False


def _scalar_is_sensitive(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, str):
        return _value_is_sensitive(value)
    if isinstance(value, int):
        text = str(value)
        return (
            re.fullmatch(r"1[3-9][0-9]{9}", text) is not None
            or re.fullmatch(r"[0-9]{17}[0-9Xx]", text) is not None
        )
    return False


def scan_sensitive(document: Any, allow_sensitive: Iterable[str] = ()) -> List[str]:
    """键级/值级敏感粗筛；返回 ``sensitive field detected: <path>`` 列表。"""
    allowed = {
        str(entry).split("=", 1)[0].strip().lower()
        for entry in allow_sensitive
        if entry is not None and str(entry).strip()
    }
    hits: List[str] = []
    seen = set()

    def is_allowed(path: str) -> bool:
        return path.lower() in allowed or _last_key(path) in allowed

    def record(path: str) -> None:
        line = "sensitive field detected: %s" % path
        if line not in seen:
            seen.add(line)
            hits.append(line)

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child_value in value.items():
                key_text = str(key)
                child_path = "%s.%s" % (path, key_text) if path else key_text
                if _key_is_sensitive(key_text) and not is_allowed(child_path):
                    record(child_path)
                walk(child_value, child_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, "%s[%d]" % (path, index))
        elif path and _scalar_is_sensitive(value) and not is_allowed(path):
            record(path)

    walk(document, "")
    return hits


def _enum_violation(
    field: str, allowed: Tuple[str, ...], value: Any, allow_bool: bool = False
) -> str:
    text = None
    if isinstance(value, bool) and allow_bool:
        text = "true" if value else "false"
    elif isinstance(value, str):
        text = value.strip()
    allowed_text = ", ".join(allowed)
    if text is None:
        return "%s must be one of %s (got: %s)" % (
            field,
            allowed_text,
            _type_name(value),
        )
    if text not in allowed:
        return "%s must be one of %s (got: %s)" % (field, allowed_text, text)
    return None


def validate_document(
    document: Any, allow_sensitive: Iterable[str] = ()
) -> List[str]:
    """返回人类可读的违规列表；空列表表示通过。"""
    if not isinstance(document, dict):
        return ["top-level YAML must be a mapping with sample-intake fields"]

    violations: List[str] = []

    for field in REQUIRED_FIELDS:
        if field not in document or _is_blank(document[field]):
            violations.append("missing %s" % field)
            continue
        value = document[field]
        if field == "authorization":
            if not isinstance(value, dict):
                violations.append(
                    "authorization must be a mapping (got: %s)" % _type_name(value)
                )
        elif not isinstance(value, str):
            violations.append(
                "%s must be a string (got: %s)" % (field, _type_name(value))
            )

    for field, allowed in ENUM_FIELDS.items():
        value = document.get(field)
        if isinstance(value, str) and value.strip():
            problem = _enum_violation(field, allowed, value)
            if problem:
                violations.append(problem)

    for field, allowed in OPTIONAL_ENUM_FIELDS.items():
        if field not in document:
            continue
        value = document[field]
        if _is_blank(value):
            continue
        problem = _enum_violation(
            field, allowed, value, allow_bool=(field == "warranty")
        )
        if problem:
            violations.append(problem)

    declared_type = document.get("type")
    if isinstance(declared_type, str) and declared_type.strip():
        declared_type = declared_type.strip()
        level_pattern = TYPE_LEVEL_RULES.get(declared_type)
        if level_pattern is None:
            violations.append(
                "type must be one of demand, defect (got: %s)"
                % _display(declared_type)
            )
        else:
            level = document.get("level")
            if (
                isinstance(level, str)
                and level.strip()
                and re.fullmatch(level_pattern, level.strip()) is None
            ):
                violations.append(
                    "level must match %s for type=%s (got: %s)"
                    % (level_pattern, declared_type, level.strip())
                )

    authorization = document.get("authorization")
    if isinstance(authorization, dict):
        approved_by = authorization.get("approved_by")
        if _is_blank(approved_by):
            violations.append("missing authorization.approved_by")
        elif not isinstance(approved_by, str) or approved_by.strip() != APPROVER:
            # 不回显原值，避免真实姓名泄漏。
            violations.append("authorization.approved_by must be %s" % APPROVER)

    violations.extend(scan_sensitive(document, allow_sensitive))
    return violations


def load_document(path: Path) -> Tuple[bool, Any, str, str]:
    """读取 YAML；返回 (ok, document, error_kind, error_message)。

    error_kind 为 ``read``（读取/解码失败，调用方按退出码 2 处理）、
    ``parse``（YAML 内容非法，按违规处理）或空字符串。
    """
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return False, None, "read", "invalid UTF-8 content: %s" % error
    except OSError as error:
        return False, None, "read", "cannot read file: %s" % error
    try:
        return True, yaml.safe_load(text), "", ""
    except yaml.YAMLError as error:
        return False, None, "parse", "invalid YAML: %s" % error


def _iter_files(target: Path) -> List[Path]:
    if target.is_dir():
        return sorted(
            path
            for path in target.glob("*")
            if path.is_file() and path.suffix.lower() in YAML_SUFFIXES
        )
    return [target]


def parse_allow_sensitive(entries: Iterable[str]) -> List[Tuple[str, str]]:
    """解析 ``FIELD`` / ``FIELD=REASON``；返回 (field, reason) 列表。"""
    parsed: List[Tuple[str, str]] = []
    for entry in entries:
        if entry is None:
            continue
        field, separator, reason = str(entry).partition("=")
        field = field.strip()
        if not field:
            continue
        parsed.append((field, reason.strip() if separator else ""))
    return parsed


def _render_result(path: Path, violations: List[str]) -> None:
    status = "PASS" if not violations else "FAIL"
    print("[%s] %s: %d violation(s)" % (status, path, len(violations)))
    for violation in violations:
        print("  - %s" % violation)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "校验 sample-intake.yaml 的必填字段、字段类型、枚举、level 编码、"
            "授权人，并做敏感信息粗筛；仅本地静态检查，不访问网络或模型。"
        )
    )
    parser.add_argument(
        "--file",
        required=True,
        help="sample-intake YAML 文件路径（也可传目录，扫描一级 *.yaml/*.yml）",
    )
    parser.add_argument(
        "--allow-sensitive",
        action="append",
        default=[],
        metavar="FIELD",
        help=(
            "豁免敏感粗筛的字段名或路径，可重复使用；支持 FIELD=REASON 记录原因，"
            "无 reason 仅告警不阻断，如 --allow-sensitive notes=public "
            "或 --allow-sensitive authorization.email"
        ),
    )
    args = parser.parse_args(argv)

    target = Path(args.file).expanduser()
    if not target.exists():
        print("[ERROR] %s: path does not exist" % target, file=sys.stderr)
        return 2
    if not target.is_file() and not target.is_dir():
        print("[ERROR] %s: not a file or directory" % target, file=sys.stderr)
        return 2

    files = _iter_files(target)
    if not files:
        print("[ERROR] %s: no YAML files found" % target, file=sys.stderr)
        return 2

    allow_entries = parse_allow_sensitive(args.allow_sensitive)
    allow_fields = [field for field, _reason in allow_entries]
    for field, reason in allow_entries:
        print(
            "[WARN] sensitive exemption: %s (reason: %s)"
            % (field, reason if reason else "not provided")
        )

    failed = 0
    unreadable = 0
    for path in files:
        ok, document, error_kind, error_message = load_document(path)
        if not ok and error_kind == "read":
            print("[ERROR] %s: %s" % (path, error_message), file=sys.stderr)
            unreadable += 1
            continue
        violations = (
            validate_document(document, allow_fields)
            if ok
            else [error_message]
        )
        _render_result(path, violations)
        if violations:
            failed += 1

    if unreadable:
        print(
            "[ERROR] %d/%d file(s) unreadable" % (unreadable, len(files)),
            file=sys.stderr,
        )
        return 2
    if failed:
        print("[FAIL] %d/%d file(s) invalid" % (failed, len(files)))
        return 1
    print("[OK] %d/%d file(s) valid" % (len(files), len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
