#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PG-02 完成度双账本渲染器（开发口径 C_dev / 真实口径 C_real）。

输入：runtime/vu-ledger.yaml（29 项目 × 3–5 个价值单元 VU）
口径：runtime/plan-20261022/GlobalCloud项目群完成度与综合能力提升_任务优先级清单_v1.0.md §1.2
      GlobalCloud 项目群实施方案.md §4 状态机 / §4.1 开发完成与真实业务验证分离

公式（§1.2，PG-02 落地化，系数见 vu-ledger.yaml 的 stage_weights）：
    C_project = Σ(weight_i × coefficient(stage_i)) / Σ weight_i
    C_group   = Σ(PW_j × C_j) / Σ PW_j
    C_dev   系数 = stage_weights.*.dev  （S0–S3 归一化，S3 = 该口径 1.0；S4 及以上开发已饱和）
    C_real  系数 = stage_weights.*.real （只计 S4–S6，S0–S3 = 0；S6 = 1.0）

输出：
    默认         Markdown 表（stdout）
    --json       机器可读 JSON（stdout）
    --check      校验台账完整性；失败返回非 0
    --no-pyyaml  强制使用内置极简 YAML 解析器（验证无 PyYAML 环境）

用法：
    python3 tools/kds-sync/render_project_group_completion.py
    python3 tools/kds-sync/render_project_group_completion.py --json
    python3 tools/kds-sync/render_project_group_completion.py --check
    python3 tools/kds-sync/render_project_group_completion.py --check --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = REPO_ROOT / "runtime" / "vu-ledger.yaml"
SCOPE_CONFIG = REPO_ROOT / "config" / "project-group-projects.yaml"

EXPECTED_PROJECT_GROUP_SCOPE = 29
VU_COUNT_MIN = 3
VU_COUNT_MAX = 5
VU_TOTAL_MIN = 84
VU_TOTAL_MAX = 140
VALID_STAGES = ("S0", "S1", "S2", "S3", "S4", "S5", "S6")
VALID_DATA_CLASSES = ("real", "fixture", "dry_run", "synthetic", "poc", "none")
REQUIRED_VU_FIELDS = (
    "vu_id", "project", "weight", "scene", "authority", "object",
    "source_of_record", "acceptor", "stage", "stage_evidence",
    "data_class", "inferred", "notes",
)
TARGETS_90D = {
    "C_dev": 0.55,
    "C_real": 0.12,
    "source": "任务优先级清单 v1.0 §2.2 / §8（90 天目标，非当前事实）",
}

# 兜底范围：与 config/project-group-projects.yaml 的 29 个项目一致。
FALLBACK_SCOPE_IDS = [
    "AAAS", "Brain", "WAS", "XiaoC", "WAME", "GPC", "Studio", "GPCF",
    "XWAIL", "GFIS", "MMC", "KDS", "XiaoG", "PVAOS", "SOP", "PKC",
    "XGD", "ICP", "PQC", "SpaceAI", "SpaceAIStudio", "World", "GCMEM",
    "WAE", "Project", "PDC", "SLC", "DRC", "FireQuote",
]


# --------------------------------------------------------------------------- #
# YAML 读取：优先 PyYAML，缺失时退化为内置极简块解析器（覆盖本篇台账结构）
# --------------------------------------------------------------------------- #

class LedgerParseError(ValueError):
    """台账 YAML 解析失败。"""


def _split_key_value(text):
    """按第一个 key 分隔符切分；key 只含字母数字下划线，value 可含冒号。"""
    match = re.match(r"^([A-Za-z0-9_\-]+):(?:\s+(.*))?$", text)
    if not match:
        raise LedgerParseError("无法解析的 YAML 行: %r" % (text,))
    return match.group(1), (match.group(2) or "")


def _scalar(text):
    text = text.strip()
    if not text:
        return None
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        inner = text[1:-1]
        if text[0] == "'":
            return inner.replace("''", "'")
        return json.loads(text)
    if text in ("true", "True", "yes"):
        return True
    if text in ("false", "False", "no"):
        return False
    if text in ("null", "Null", "~"):
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d*", text) or re.fullmatch(r"-?\d*\.\d+", text):
        return float(text)
    return text


def _parse_mini_yaml(text):
    """极简块状 YAML 解析器：嵌套 map / map 列表 / 标量，支持引号与注释行。"""
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, stripped))
    if not lines:
        raise LedgerParseError("空 YAML")
    value, pos = _parse_node(lines, 0, lines[0][0])
    if pos != len(lines):
        raise LedgerParseError("YAML 尾部存在无法归属的内容: %r" % (lines[pos],))
    return value


def _parse_node(lines, index, indent):
    if lines[index][1].startswith("- "):
        return _parse_sequence(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(lines, index, indent):
    result = {}
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent != indent or content.startswith("- "):
            break
        key, rest = _split_key_value(content)
        index += 1
        if rest:
            result[key] = _scalar(rest)
        elif index < len(lines) and lines[index][0] > indent:
            result[key], index = _parse_node(lines, index, lines[index][0])
        elif index < len(lines) and lines[index][0] == indent and lines[index][1].startswith("- "):
            # YAML 允许 key 下挂同级缩进的 sequence（indentless sequence）
            result[key], index = _parse_sequence(lines, index, indent)
        else:
            result[key] = None
    return result, index


def _parse_sequence(lines, index, indent):
    result = []
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent != indent or not content.startswith("- "):
            break
        body = content[2:].strip()
        index += 1
        if not body:
            value, index = _parse_node(lines, index, lines[index][0])
            result.append(value)
            continue
        # 只有形如 "key:" / "key: value" 的列表项才按 mapping 解析；
        # 带冒号的引号标量（如 'a: b'）必须按标量处理。
        if not re.match(r"^[A-Za-z0-9_\-]+:(?:\s|$)", body):
            result.append(_scalar(body))
            continue
        key, rest = _split_key_value(body)
        item = {}
        if rest:
            item[key] = _scalar(rest)
        elif index < len(lines) and lines[index][0] > indent:
            item[key], index = _parse_node(lines, index, lines[index][0])
        else:
            item[key] = None
        if index < len(lines) and lines[index][0] > indent and not lines[index][1].startswith("- "):
            extra, index = _parse_mapping(lines, index, lines[index][0])
            item.update(extra)
        result.append(item)
    return result, index


def load_yaml_file(path, allow_pyyaml=True):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if allow_pyyaml:
        try:
            import yaml  # type: ignore
        except ImportError:
            return _parse_mini_yaml(text)
        return yaml.safe_load(text)
    return _parse_mini_yaml(text)


def load_ledger(path, allow_pyyaml=True):
    ledger = load_yaml_file(path, allow_pyyaml=allow_pyyaml)
    if not isinstance(ledger, dict):
        raise LedgerParseError("台账顶层必须是 mapping")
    return ledger


def load_scope_ids(config_path=SCOPE_CONFIG):
    """从项目群范围配置读取 28 个项目 id；文件缺失或解析失败时用内置清单兜底。"""
    try:
        text = Path(config_path).read_text(encoding="utf-8")
    except OSError:
        return list(FALLBACK_SCOPE_IDS)
    ids = re.findall(r"^\s*-\s*\{?\s*id:\s*\"?([A-Za-z0-9_\-]+)\"?", text, re.MULTILINE)
    return ids or list(FALLBACK_SCOPE_IDS)


# --------------------------------------------------------------------------- #
# 计算
# --------------------------------------------------------------------------- #

def _coefficients(ledger):
    stage_weights = ledger.get("stage_weights") or {}
    dev, real = {}, {}
    for stage in VALID_STAGES:
        entry = stage_weights.get(stage)
        if not isinstance(entry, dict):
            raise LedgerParseError("stage_weights 缺少阶段 %s" % stage)
        try:
            dev[stage] = float(entry["dev"])
            real[stage] = float(entry["real"])
        except (KeyError, TypeError, ValueError) as exc:
            raise LedgerParseError("stage_weights.%s 系数非法: %s" % (stage, exc))
    return dev, real


def _ratio(numerator, denominator):
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def compute(ledger):
    dev_coef, real_coef = _coefficients(ledger)
    units = ledger.get("vu_units") or []
    if not isinstance(units, list):
        raise LedgerParseError("vu_units 必须是列表")

    by_project = {}
    for vu in units:
        by_project.setdefault(vu.get("project"), []).append(vu)

    projects = []
    total_weighted_dev = 0.0
    total_weighted_real = 0.0
    project_weight_sum = 0
    for entry in ledger.get("project_scope") or []:
        project_id = entry.get("id")
        project_weight = int(entry.get("weight") or 0)
        vus = by_project.get(project_id, [])
        vu_weight_sum = sum(int(vu["weight"]) for vu in vus)
        c_dev = _ratio(sum(int(vu["weight"]) * dev_coef[vu["stage"]] for vu in vus), vu_weight_sum)
        c_real = _ratio(sum(int(vu["weight"]) * real_coef[vu["stage"]] for vu in vus), vu_weight_sum)
        stage_counts = {stage: 0 for stage in VALID_STAGES}
        for vu in vus:
            stage_counts[vu["stage"]] += 1
        inferred_count = sum(1 for vu in vus if vu.get("inferred") is True)
        projects.append({
            "project": project_id,
            "project_weight": project_weight,
            "lane": entry.get("lane"),
            "current_form": entry.get("current_form"),
            "main_gap": entry.get("main_gap"),
            "vu_count": len(vus),
            "vu_weight_sum": vu_weight_sum,
            "C_dev": round(c_dev, 6),
            "C_real": round(c_real, 6),
            "stage_distribution": {k: v for k, v in stage_counts.items() if v},
            "inferred_vu_count": inferred_count,
        })
        total_weighted_dev += project_weight * c_dev
        total_weighted_real += project_weight * c_real
        project_weight_sum += project_weight

    missing_projects = [pid for pid in load_scope_ids() if pid not in by_project]
    unknown_projects = sorted({vu.get("project") for vu in units} - set(load_scope_ids()))

    result = {
        "schema_version": ledger.get("schema_version"),
        "generated_at": ledger.get("generated_at"),
        "model_ref": ledger.get("model_ref"),
        "project_group_scope": ledger.get("project_group_scope"),
        "vu_total": len(units),
        "vu_inferred_count": sum(1 for vu in units if vu.get("inferred") is True),
        "calibers": ledger.get("calibers"),
        "targets_90d": TARGETS_90D,
        "group": {
            "project_count": len(projects),
            "project_weight_sum": project_weight_sum,
            "C_dev": round(_ratio(total_weighted_dev, project_weight_sum), 6),
            "C_real": round(_ratio(total_weighted_real, project_weight_sum), 6),
        },
        "projects": projects,
        "coverage": {
            "expected_projects": len(load_scope_ids()),
            "ledger_projects": len(by_project),
            "missing_projects": missing_projects,
            "unknown_projects": unknown_projects,
        },
    }
    return result


# --------------------------------------------------------------------------- #
# 校验（--check）
# --------------------------------------------------------------------------- #

def check(ledger, result):
    """返回 (checks, errors)。checks 为 [(name, ok, detail)]。"""
    checks = []

    def record(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    errors = []

    scope = int(ledger.get("project_group_scope") or 0)
    record("project_group_scope == 29", scope == EXPECTED_PROJECT_GROUP_SCOPE,
           "顶部 project_group_scope=%s，要求 %d" % (scope, EXPECTED_PROJECT_GROUP_SCOPE))
    if scope != EXPECTED_PROJECT_GROUP_SCOPE:
        errors.append("project_group_scope 不等于 29")

    record("schema_version 存在", bool(ledger.get("schema_version")),
           "schema_version=%r" % (ledger.get("schema_version"),))
    if not ledger.get("schema_version"):
        errors.append("缺少 schema_version")

    expected_ids = load_scope_ids()
    units = ledger.get("vu_units") or []
    by_project = {}
    for vu in units:
        by_project.setdefault(vu.get("project"), []).append(vu)

    missing = [pid for pid in expected_ids if pid not in by_project]
    unknown = sorted(set(by_project) - set(expected_ids))
    record("29 项目覆盖 100%", not missing, "缺失项目=%s" % (missing or "无"))
    if missing:
        errors.append("未覆盖项目: %s" % ",".join(missing))
    record("无越界项目", not unknown, "越界项目=%s" % (unknown or "无"))
    if unknown:
        errors.append("台账含范围外项目: %s" % ",".join(unknown))

    bad_counts = {pid: len(by_project.get(pid, [])) for pid in expected_ids
                  if not VU_COUNT_MIN <= len(by_project.get(pid, [])) <= VU_COUNT_MAX}
    record("每项目 VU 数 3–5", not bad_counts,
           "不合规=%s" % (bad_counts or "无"))
    if bad_counts:
        errors.append("VU 数越界: %s" % bad_counts)

    record("VU 总数 84–140", VU_TOTAL_MIN <= len(units) <= VU_TOTAL_MAX,
           "vu_total=%d，允许区间 %d–%d" % (len(units), VU_TOTAL_MIN, VU_TOTAL_MAX))
    if not VU_TOTAL_MIN <= len(units) <= VU_TOTAL_MAX:
        errors.append("VU 总数越界: %d" % len(units))

    seen_ids = set()
    duplicated = []
    field_errors = []
    weight_errors = []
    stage_errors = []
    data_class_errors = []
    inferred_errors = []
    governor_violations = []
    for vu in units:
        vu_id = vu.get("vu_id")
        if vu_id in seen_ids:
            duplicated.append(vu_id)
        seen_ids.add(vu_id)
        for field in REQUIRED_VU_FIELDS:
            if field not in vu or vu[field] in (None, ""):
                field_errors.append("%s 缺字段 %s" % (vu_id, field))
        weight = vu.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or not 1 <= weight <= 5:
            weight_errors.append("%s weight=%r" % (vu_id, weight))
        stage = vu.get("stage")
        if stage not in VALID_STAGES:
            stage_errors.append("%s stage=%r" % (vu_id, stage))
        if vu.get("data_class") not in VALID_DATA_CLASSES:
            data_class_errors.append("%s data_class=%r" % (vu_id, vu.get("data_class")))
        if not isinstance(vu.get("inferred"), bool):
            inferred_errors.append("%s inferred=%r" % (vu_id, vu.get("inferred")))
        # fixture/dry-run/mock/SIMULATED/PoC 不得进入 S4+
        if stage in ("S4", "S5", "S6") and vu.get("data_class") != "real":
            governor_violations.append("%s stage=%s data_class=%s" % (vu_id, stage, vu.get("data_class")))

    record("vu_id 唯一", not duplicated, "重复=%s" % (duplicated or "无"))
    record("VU 必填字段完整", not field_errors, "; ".join(field_errors[:5]) or "全部完整")
    record("weight ∈ 1–5 整数", not weight_errors, "; ".join(weight_errors[:5]) or "全部合法")
    record("stage ∈ S0–S6", not stage_errors, "; ".join(stage_errors[:5]) or "全部合法")
    record("data_class 合法", not data_class_errors, "; ".join(data_class_errors[:5]) or "全部合法")
    record("inferred 为布尔", not inferred_errors, "; ".join(inferred_errors[:5]) or "全部合法")
    record("fixture/dry-run/PoC 不得进 S4+", not governor_violations,
           "; ".join(governor_violations[:5]) or "无违规")
    for label, bucket in (("vu_id 唯一", duplicated), ("必填字段", field_errors),
                          ("weight", weight_errors), ("stage", stage_errors),
                          ("data_class", data_class_errors), ("inferred", inferred_errors),
                          ("governor 纪律", governor_violations)):
        if bucket:
            errors.append("%s 校验失败: %s" % (label, bucket[:5]))

    scope_entries = ledger.get("project_scope") or []
    project_weight_errors = []
    for entry in scope_entries:
        weight = entry.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or not 2 <= weight <= 5:
            project_weight_errors.append("%s PW=%r" % (entry.get("id"), weight))
    record("项目权重 PW ∈ 2–5 整数", not project_weight_errors,
           "; ".join(project_weight_errors[:5]) or "全部合法")
    if project_weight_errors:
        errors.append("项目权重非法: %s" % project_weight_errors[:5])

    record("每项目至少 1 条 VU", all(len(by_project.get(pid, [])) >= 1 for pid in expected_ids),
           "已覆盖 %d/%d" % (len([p for p in expected_ids if by_project.get(p)]), len(expected_ids)))

    result_summary = {
        "project_count": result["group"]["project_count"],
        "vu_total": result["vu_total"],
        "vu_inferred_count": result["vu_inferred_count"],
        "C_group_dev": result["group"]["C_dev"],
        "C_group_real": result["group"]["C_real"],
    }
    return checks, errors, result_summary


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #

def _pct(value):
    return "%.2f%%" % (value * 100.0)


def _stage_distribution_text(distribution):
    if not distribution:
        return "—"
    return " ".join("%s×%d" % (stage, count) for stage, count in distribution.items())


def render_markdown(result):
    group = result["group"]
    lines = []
    lines.append("# GlobalCloud 项目群完成度双账本（PG-02）")
    lines.append("")
    lines.append("- 台账：`runtime/vu-ledger.yaml`（generated_at=%s）" % (result.get("generated_at"),))
    lines.append("- 公式：`C_project = Σ(weight_i × coefficient(stage_i)) / Σ weight_i`；"
                 "`C_group = Σ(PW_j × C_j) / Σ PW_j`")
    lines.append("- VU 总数：%d（inferred=%d）；项目数：%d；项目权重和：%d"
                 % (result["vu_total"], result["vu_inferred_count"],
                    group["project_count"], group["project_weight_sum"]))
    lines.append("- **项目群 C_dev = %s｜C_real = %s**"
                 % (_pct(group["C_dev"]), _pct(group["C_real"])))
    lines.append("- 90 天目标口径：C_dev ≥ %s、C_real ≥ %s（目标，非当前事实）"
                 % (_pct(TARGETS_90D["C_dev"]), _pct(TARGETS_90D["C_real"])))
    lines.append("- 全部条目为首版基线估算（inferred），不是受控事实。")
    lines.append("")
    lines.append("| 项目 | PW | VU 数 | C_dev | C_real | 阶段分布 | 主要缺口 |")
    lines.append("|---|---:|---:|---:|---:|---|---|")
    for project in result["projects"]:
        lines.append("| %s | %d | %d | %s | %s | %s | %s |" % (
            project["project"], project["project_weight"], project["vu_count"],
            _pct(project["C_dev"]), _pct(project["C_real"]),
            _stage_distribution_text(project["stage_distribution"]),
            project["main_gap"] or "—",
        ))
    lines.append("")
    lines.append("> 由 `tools/kds-sync/render_project_group_completion.py` 生成；"
                 "数值全部来自 `runtime/vu-ledger.yaml` 复算，无手工填写。")
    return "\n".join(lines)


def render_check_report(checks, errors, summary):
    lines = []
    for item in checks:
        lines.append("[%s] %s — %s" % ("PASS" if item["ok"] else "FAIL",
                                       item["check"], item["detail"]))
    lines.append("")
    lines.append("summary: projects=%d vu_total=%d inferred=%d C_group_dev=%.4f C_group_real=%.4f"
                 % (summary["project_count"], summary["vu_total"],
                    summary["vu_inferred_count"], summary["C_group_dev"],
                    summary["C_group_real"]))
    lines.append("result: %s" % ("PASS" if not errors else "FAIL (%d 项)" % len(errors)))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="PG-02 项目群完成度双账本渲染器（C_dev / C_real）")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                        help="vu-ledger.yaml 路径（默认仓内 runtime/vu-ledger.yaml）")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--check", action="store_true",
                        help="校验 29 项目覆盖 / VU 数 / weight / stage；失败返回非 0")
    parser.add_argument("--no-pyyaml", action="store_true",
                        help="强制使用内置极简 YAML 解析器")
    args = parser.parse_args(argv)

    try:
        ledger = load_ledger(args.ledger, allow_pyyaml=not args.no_pyyaml)
    except (OSError, LedgerParseError) as exc:
        print("ERROR: 台账读取失败: %s" % exc, file=sys.stderr)
        return 2

    try:
        result = compute(ledger)
    except (LedgerParseError, KeyError, TypeError, ValueError) as exc:
        print("ERROR: 台账复算失败: %s" % exc, file=sys.stderr)
        return 2

    checks, errors, summary = check(ledger, result)
    result["check"] = {"ok": not errors, "checks": checks, "errors": errors}

    if args.check:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(render_check_report(checks, errors, summary))
        return 0 if not errors else 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
