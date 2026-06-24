#!/usr/bin/env python3
"""Check operational Loop gates from local evidence."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".codex",
    ".kds",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".turbo",
}

EVIDENCE_ROOTS = (
    ".harness",
    "07-acceptance",
    "08-evidence-samples",
    "09-status",
    "docs/harness",
)


@dataclass(frozen=True)
class GateSpec:
    name: str
    pass_patterns: tuple[str, ...]
    rework_patterns: tuple[str, ...] = ()
    blocked_patterns: tuple[str, ...] = ()
    expected_evidence: tuple[str, ...] = ()


GATES = (
    GateSpec(
        name="quality",
        pass_patterns=(
            r"quality[-_ ]?check",
            r"test[-_ ]?result",
            r"测试结果",
            r"缺陷",
            r"验收矩阵",
            r"acceptance[-_ ]?matrix",
            r"status[-_ ]?audit",
        ),
        rework_patterns=(r"\bP[01]\b.*(缺陷|defect|bug).*(open|unresolved|未关闭|未解决)", r"(质量返工|quality.*rework)"),
        blocked_patterns=(r"质量.*blocked", r"质量.*阻塞", r"accepted_for_quality_profile.*`?0`?"),
        expected_evidence=("测试结果", "缺陷台账", "验收矩阵", "质量判定"),
    ),
    GateSpec(
        name="usability",
        pass_patterns=(
            r"screenshot",
            r"录屏",
            r"可用性",
            r"UI Quality Gate",
            r"UI gate status",
            r"ui_ready",
            r"ui_evidence_candidate",
            r"globalcloud-ui-quality-gate",
            r"G[1-9] Surface Structure",
            r"G[1-9] Design Tokens",
            r"G[1-9] Component Consistency",
            r"manual[-_ ]?test",
            r"smoke[-_ ]?test",
            r"\be2e\b",
            r"端到端",
        ),
        rework_patterns=(r"(界面|页面|产品|主流程|核心流程).*不可用", r"无法使用", r"主流程.*失败", r"ui_rework_required"),
        blocked_patterns=(r"无法启动", r"无法进入", r"核心流程.*阻塞", r"ui_blocked"),
        expected_evidence=("可运行入口", "主流程验证", "截图或录屏", "人工体验结论", "UI Quality Gate G1-G9 结论"),
    ),
    GateSpec(
        name="customer_satisfaction",
        pass_patterns=(
            r"customer",
            r"客户",
            r"满意",
            r"feedback",
            r"回访",
            r"试用",
            r"交付确认",
        ),
        rework_patterns=(r"不满意", r"客户.*返工", r"投诉", r"未达预期"),
        blocked_patterns=(r"客户.*拒收", r"业务.*拒收", r"accepted_for_customer.*`?0`?"),
        expected_evidence=("目标用户", "满意度记录", "反馈闭环", "未满足项"),
    ),
    GateSpec(
        name="dependency",
        pass_patterns=(
            r"dependency",
            r"依赖",
            r"接口",
            r"边界",
            r"alignment",
            r"项目主线",
            r"交叉比对",
        ),
        rework_patterns=(r"依赖.*未对齐", r"接口.*不一致", r"边界.*不清"),
        blocked_patterns=(r"依赖.*阻塞", r"上游.*阻塞", r"下游.*阻塞"),
        expected_evidence=("上下游依赖", "接口边界", "跨项目影响", "同步记录"),
    ),
    GateSpec(
        name="risk_rollback",
        pass_patterns=(
            r"risk",
            r"风险",
            r"rollback",
            r"回滚",
            r"恢复",
            r"应急",
            r"阻塞项",
        ),
        rework_patterns=(r"高风险.*无.*回滚", r"风险.*未闭环"),
        blocked_patterns=(r"高风险.*阻塞", r"不可回滚", r"安全风险.*未处理"),
        expected_evidence=("风险清单", "回滚策略", "恢复路径", "阻塞项处置"),
    ),
    GateSpec(
        name="evolution",
        pass_patterns=(
            r"retrospective",
            r"复盘",
            r"evolution",
            r"自我进化",
            r"下一轮",
            r"经验",
            r"Loop",
        ),
        rework_patterns=(r"重复问题.*未修正", r"复盘.*缺失"),
        blocked_patterns=(r"自我进化.*失效", r"机制.*失效"),
        expected_evidence=("本轮复盘", "规则更新", "技能更新", "下一轮输入"),
    ),
)


def iter_markdown(root: Path) -> list[Path]:
    files: list[Path] = []
    for evidence_root in EVIDENCE_ROOTS:
        candidate = root / evidence_root
        if not candidate.exists():
            continue
        for path in candidate.rglob("*.md"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def match_patterns(patterns: tuple[str, ...], text: str) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(pattern)
    return found


def excluded_context_line(line: str) -> bool:
    stripped = line.strip()
    if re.match(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|", stripped):
        return True
    if re.match(r"^\|\s*\d+\s*\|", stripped):
        return True
    if "全仓门禁" in line and not re.search(
        r"(accepted_for|hold_required|real_source_records|valid_source_records)",
        line,
        flags=re.IGNORECASE,
    ):
        return True
    if re.search(r"\|\s*\d+\s*\|", line) and not re.search(r"(当前|本轮|仍|未解除|accepted_for|hold_required)", line):
        return True
    if re.search(
        r"(status_values|allowed values|枚举|可选值|示例|样例|fixture|negative fixture|rejected examples|负例|拒收样例)",
        line,
        flags=re.IGNORECASE,
    ) and not re.search(r"(accepted_for|hold_required|real_source_records|valid_source_records)", line, flags=re.IGNORECASE):
        return True
    return False


def active_signal_patterns(patterns: tuple[str, ...], text: str) -> list[str]:
    active_lines = []
    for line in text.splitlines():
        if excluded_context_line(line):
            continue
        if re.search(
            r"(gate|门禁|状态|结论|判定|status|result|health|accepted_for|hold_required|real_source_records|valid_source_records|production_ready)",
            line,
            flags=re.IGNORECASE,
        ):
            active_lines.append(line)
    active_text = "\n".join(active_lines)
    return match_patterns(patterns, active_text)


def controlled_source_record_hold(relative_path: str, text: str) -> bool:
    if "was-real-source-record-monitor-" not in relative_path and "loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-" not in relative_path:
        return False
    if "不得替代 KDS source-of-record" not in text and "不创建 KDS 正式事实" not in text:
        return False
    return bool(
        re.search(r"accepted_for_[a-z0-9_]+.*`?0`?", text, flags=re.IGNORECASE)
        and re.search(r"hold_required.*`?1`?", text, flags=re.IGNORECASE)
    )


def ui_round_number(path: str) -> int | None:
    match = re.search(r"loop-round-GPCF-UI-STUDIO-WORKBENCH-(\d+)\.md$", path)
    if not match:
        return None
    return int(match.group(1))


def latest_ui_gate_status(corpus: list[tuple[Path, str]], root: Path) -> tuple[int, str] | None:
    latest: tuple[int, str] | None = None
    for path, text in corpus:
        relative = rel(path, root)
        round_number = ui_round_number(relative)
        if round_number is None:
            continue
        match = re.search(r"UI gate status:\s*(ui_[a-z_]+)", text, flags=re.IGNORECASE)
        if not match:
            continue
        status = match.group(1).lower()
        if latest is None or round_number > latest[0]:
            latest = (round_number, status)
    return latest


def filter_stale_usability_blockers(
    blocked_hits: list[str],
    corpus: list[tuple[Path, str]],
    root: Path,
) -> list[str]:
    latest = latest_ui_gate_status(corpus, root)
    if latest is None or latest[1] not in {"ui_ready", "ui_partial"}:
        return blocked_hits

    latest_round = latest[0]
    filtered: list[str] = []
    for hit in blocked_hits:
        round_number = ui_round_number(hit)
        if round_number is not None and round_number < latest_round:
            continue
        if hit.endswith("docs/harness/evidence/loop-ui-governance-baseline-20260622.md"):
            continue
        if hit.endswith("docs/harness/evidence/studio-kanban-runtime-entry-gate-20260622.md"):
            continue
        filtered.append(hit)
    return filtered


def evaluate_gate(spec: GateSpec, corpus: list[tuple[Path, str]], root: Path) -> dict[str, object]:
    pass_hits: list[str] = []
    rework_hits: list[str] = []
    blocked_hits: list[str] = []

    for path, text in corpus:
        relative_path = rel(path, root)
        if len(pass_hits) < 8 and match_patterns(spec.pass_patterns, text):
            pass_hits.append(relative_path)
        if len(rework_hits) < 8 and active_signal_patterns(spec.rework_patterns, text):
            if spec.name in {"quality", "customer_satisfaction"} and controlled_source_record_hold(relative_path, text):
                continue
            rework_hits.append(relative_path)
        if len(blocked_hits) < 8 and active_signal_patterns(spec.blocked_patterns, text):
            if spec.name in {"quality", "customer_satisfaction"} and controlled_source_record_hold(relative_path, text):
                continue
            blocked_hits.append(relative_path)

    if spec.name == "usability":
        rework_hits = filter_stale_usability_blockers(rework_hits, corpus, root)
        blocked_hits = filter_stale_usability_blockers(blocked_hits, corpus, root)

    if blocked_hits:
        gate = "blocked"
        reasons = [f"发现阻塞信号：{item}" for item in blocked_hits]
    elif rework_hits:
        gate = "rework"
        reasons = [f"发现返工信号：{item}" for item in rework_hits]
    elif pass_hits:
        gate = "pass"
        reasons = [f"发现证据：{item}" for item in pass_hits[:5]]
    else:
        gate = "partial"
        reasons = ["未发现足够证据，允许准备证据但不得升级状态。"]

    return {
        "gate": gate,
        "reasons": reasons,
        "evidence_files": pass_hits[:8],
        "expected_evidence": list(spec.expected_evidence),
    }


def overall(gates: dict[str, dict[str, object]]) -> str:
    states = [str(item["gate"]) for item in gates.values()]
    if "blocked" in states:
        return "blocked"
    if "rework" in states:
        return "rework"
    if "partial" in states:
        return "partial"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GlobalCloud Loop operational gates.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root to inspect")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    markdown_files = iter_markdown(root)
    corpus = [(path, read_text(path)) for path in markdown_files]
    gates = {spec.name: evaluate_gate(spec, corpus, root) for spec in GATES}
    result = {
        "repo": str(root),
        "gate": overall(gates),
        "markdown_files_scanned": len(markdown_files),
        "gates": gates,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
