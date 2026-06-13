#!/usr/bin/env python3
"""Assess GlobalCloud project L3 admission readiness from local repo facts."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1")


@dataclass(frozen=True)
class Project:
    name: str
    code: str
    path: Path
    governance_hub: bool = False


PROJECTS = [
    Project("GFIS", "GF", ROOT / "GlobalCloud GFIS"),
    Project("GPC", "GP", ROOT / "GlobalCloud GPC"),
    Project("PVAOS", "PV", ROOT / "GlobalCloud PVAOS"),
    Project("WAES", "WA", ROOT / "GlobalCloud WAES"),
    Project("KDS", "KD", ROOT / "GlobalCloud KDS"),
    Project("Brain", "BR", ROOT / "GlobalCloud Brain"),
    Project("PKC", "PK", ROOT / "GlobalCloud PKC"),
    Project("XiaoC", "XC", ROOT / "GlobalCloud XiaoC"),
    Project("XGD", "XD", ROOT / "GlobalCloud XGD"),
    Project("XiaoG", "XG", ROOT / "GlobalCloud XiaoG"),
    Project("MMC", "MM", ROOT / "GlobalCloud MMC"),
    Project("GPCF", "CF", ROOT / "GlobalCoud GPCF", governance_hub=True),
]

WEIGHTS = {
    "repo": 10,
    "queue": 10,
    "code_config": 15,
    "test_validation": 15,
    "evidence": 10,
    "loop_state": 8,
    "git_gate": 8,
    "risk_rollback": 8,
    "dependencies": 6,
    "usability_customer": 5,
    "evolution": 5,
}


def run(cwd: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")
    except FileNotFoundError:
        return ""


def any_file(path: Path, patterns: list[str]) -> bool:
    for pattern in patterns:
        if any(path.glob(pattern)):
            return True
    return False


def status_band(score: int, governance_hub: bool, dirty_count: int = 0, sensitive_dirty_count: int = 0) -> str:
    if governance_hub:
        return "governance_hub"
    if sensitive_dirty_count:
        return "blocked"
    if dirty_count and score >= 90:
        return "L3 Conditional"
    if score >= 90:
        return "L3 Ready"
    if score >= 80:
        return "L3 Conditional"
    if score >= 65:
        return "L2.5"
    if score >= 50:
        return "L2"
    return "L1/L0"


def score_project(project: Project) -> dict:
    path = project.path
    facts: dict[str, object] = {"path": str(path)}
    scores = {key: 0 for key in WEIGHTS}
    gaps: list[str] = []
    tasks: list[str] = []

    git_exists = (path / ".git").exists()
    facts["repo_exists"] = path.exists()
    facts["git_exists"] = git_exists
    if path.exists() and git_exists:
        scores["repo"] = WEIGHTS["repo"]
    else:
        gaps.append("缺真实项目仓")

    status = ""
    if git_exists:
        _, status = run(path, "git", "status", "--short", "--branch")
    facts["git_status"] = status
    dirty_lines = [line for line in status.splitlines()[1:] if line.strip()]
    sensitive_lines = [
        line
        for line in dirty_lines
        if any(token in line.lower() for token in [".env", "token", "secret", "credential", ".pem", ".key"])
    ]
    if git_exists and not dirty_lines:
        scores["git_gate"] = WEIGHTS["git_gate"]
    elif git_exists and dirty_lines and not sensitive_lines:
        scores["git_gate"] = 5
        gaps.append("Git 工作区存在未提交变更")
    else:
        gaps.append("Git 门禁不可判断或存在敏感文件风险")
    facts["dirty_count"] = len(dirty_lines)
    facts["sensitive_dirty_count"] = len(sensitive_lines)

    package_json = read(path / "package.json")
    nested_package_json = "\n".join(read(p) for p in list(path.glob("main/**/package.json"))[:20])
    pyproject = read(path / "pyproject.toml")
    root_requirements = read(path / "requirements.txt")
    runtime_requirements = read(path / "runtime" / "requirements.txt")
    nested_requirements = "\n".join(read(p) for p in list(path.glob("main/**/requirements.txt"))[:20])
    requirements = root_requirements + "\n" + runtime_requirements + "\n" + nested_requirements
    has_code = any_file(
        path,
        [
            "src/**",
            "app/**",
            "packages/**",
            "runtime/app/**",
            "runtime/tests/**",
            "main/**/src/**",
            "main/**/*.py",
            "main/**/*.java",
            "main/**/*.js",
            "main/**/*.ts",
            "main/**/*.vue",
            "*.py",
            "gcfis_demo/**",
        ],
    )
    has_config = any_file(
        path,
        [
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "runtime/requirements.txt",
            "main/**/requirements.txt",
            "main/**/package.json",
            "main/**/pom.xml",
            "runtime/Dockerfile",
            "runtime/docker-compose*.yml",
            "Dockerfile*",
            "main/**/Dockerfile*",
            "main/**/docker-compose*.yml",
            "runtime/alembic.ini",
            "vite.config.*",
            "wrangler.*",
            "docker-compose*.yml",
        ],
    )
    if has_code and has_config:
        scores["code_config"] = WEIGHTS["code_config"]
    elif has_code or has_config:
        scores["code_config"] = 8
        gaps.append("代码/配置闭环不完整")
    else:
        gaps.append("缺代码/配置闭环")
    facts["has_code"] = has_code
    facts["has_config"] = has_config

    test_words = ["test", "lint", "build", "typecheck", "quality", "validate"]
    scripts_text = package_json + "\n" + nested_package_json + "\n" + pyproject + "\n" + requirements
    has_test_command = any(f'"{word}"' in scripts_text or f"{word} =" in pyproject for word in test_words)
    has_test_command = has_test_command or any_file(
        path,
        [
            "runtime/tests/test_*.*",
            "tests/test_*.*",
            "runtime/scripts/ci_local.sh",
            "runtime/scripts/contract_test.sh",
            "scripts/test_*.*",
        ],
    )
    has_validator = any_file(path, ["scripts/validate*.*", "tools/**/validate*.*", "docs/harness/**/validate*.*"])
    if has_test_command and has_validator:
        scores["test_validation"] = WEIGHTS["test_validation"]
    elif has_test_command or has_validator:
        scores["test_validation"] = 9
        gaps.append("测试/验证命令覆盖不足")
    else:
        gaps.append("缺测试/验证命令")
    facts["has_test_command"] = has_test_command
    facts["has_validator"] = has_validator

    harness = path / "docs" / "harness"
    loop_state = harness / "loop-state.md"
    evidence_index = harness / "evidence" / "evidence-index.md"
    loops_dir = harness / "loops"
    facts["has_harness"] = harness.exists()
    facts["has_loop_state"] = loop_state.exists()
    facts["has_evidence_index"] = evidence_index.exists()
    facts["has_loops_dir"] = loops_dir.exists()
    if loop_state.exists():
        scores["loop_state"] = WEIGHTS["loop_state"]
    else:
        gaps.append("缺 loop-state")
    if evidence_index.exists() and loops_dir.exists():
        scores["evidence"] = WEIGHTS["evidence"]
    elif evidence_index.exists() or harness.exists():
        scores["evidence"] = 5
        gaps.append("evidence 体系不完整")
    else:
        gaps.append("缺 evidence")

    joined_docs = "\n".join(
        read(p)
        for p in list(harness.glob("**/*.md"))[:80]
        + list(harness.glob("**/*.json"))[:40]
        + [path / "PROJECT_HARNESS_MANIFEST.md", path / "README.md", path / "AGENTS.md"]
    )
    queue_hits = sum(token in joined_docs for token in ["下一轮", "任务", "backlog", "P1", "Round", "next_task_queue", "required_action"])
    if queue_hits >= 3:
        scores["queue"] = WEIGHTS["queue"]
    elif queue_hits:
        scores["queue"] = 5
        gaps.append("L3 任务队列不足")
    else:
        gaps.append("缺 L3 任务队列")

    risk_hits = sum(token in joined_docs for token in ["风险", "回滚", "rollback", "禁止", "边界"])
    if risk_hits >= 4:
        scores["risk_rollback"] = WEIGHTS["risk_rollback"]
    elif risk_hits:
        scores["risk_rollback"] = 4
        gaps.append("风险与回滚方案不足")
    else:
        gaps.append("缺回滚方案")

    dep_hits = sum(token in joined_docs for token in ["KDS", "Brain", "PKC", "MMC", "WAES", "GFIS", "XiaoC", "XGD", "GPC"])
    if dep_hits >= 3:
        scores["dependencies"] = WEIGHTS["dependencies"]
    elif dep_hits:
        scores["dependencies"] = 3
        gaps.append("跨项目依赖验证不足")
    else:
        gaps.append("缺跨项目依赖验证")

    usability_hits = sum(token in joined_docs for token in ["可用", "用户", "客户", "UAT", "preview", "浏览器", "满意"])
    if usability_hits >= 3:
        scores["usability_customer"] = WEIGHTS["usability_customer"]
    elif usability_hits:
        scores["usability_customer"] = 2
        gaps.append("可用性/客户满意指标不足")
    else:
        gaps.append("缺可用性/客户满意指标")

    evolution_hits = sum(token in joined_docs for token in ["自我进化", "下一轮", "反馈", "复盘", "经验", "self-evolution", "feedback_to_rules", "rule_update"])
    if evolution_hits >= 3:
        scores["evolution"] = WEIGHTS["evolution"]
    elif evolution_hits:
        scores["evolution"] = 2
        gaps.append("自我进化机制不足")
    else:
        gaps.append("缺自我进化机制")

    raw_score = sum(scores.values())
    caps: list[str] = []
    score = raw_score
    if not git_exists:
        score = min(score, 40)
        caps.append("没有真实项目仓，最高 40 分")
    if not has_test_command and not has_validator:
        score = min(score, 60)
        caps.append("没有测试/验证命令，最高 60 分")
    if not scores["evidence"]:
        score = min(score, 65)
        caps.append("没有 evidence，最高 65 分")

    if "缺代码/配置闭环" in gaps or "代码/配置闭环不完整" in gaps:
        tasks.append("补齐最小代码/配置闭环入口，并添加对应 validator")
    if "缺测试/验证命令" in gaps or "测试/验证命令覆盖不足" in gaps:
        tasks.append("补齐项目级 test/lint/build/validate 命令并纳入 evidence")
    if "缺 evidence" in gaps or "evidence 体系不完整" in gaps:
        tasks.append("补齐 docs/harness/evidence/evidence-index.md 和轮次证据")
    if "缺 loop-state" in gaps:
        tasks.append("补齐 docs/harness/loop-state.md")
    if "Git 工作区存在未提交变更" in gaps or "Git 门禁不可判断或存在敏感文件风险" in gaps:
        tasks.append("清理 Git 工作区或登记敏感文件 ignore 门禁")
    if "风险与回滚方案不足" in gaps or "缺回滚方案" in gaps:
        tasks.append("补齐风险/回滚 runbook 并用脚本校验")
    if "跨项目依赖验证不足" in gaps or "缺跨项目依赖验证" in gaps:
        tasks.append("补齐跨项目依赖 dry-run 或 contract check")
    if "可用性/客户满意指标不足" in gaps or "缺可用性/客户满意指标" in gaps:
        tasks.append("补齐可用性/客户满意 smoke evidence")
    if "自我进化机制不足" in gaps or "缺自我进化机制" in gaps:
        tasks.append("补齐下一轮反馈到规则/模板的自我进化记录")
    tasks = tasks[:5]

    return {
        "project": project.name,
        "code": project.code,
        "governance_hub": project.governance_hub,
        "score": score,
        "raw_score": raw_score,
        "status": status_band(score, project.governance_hub, len(dirty_lines), len(sensitive_lines)),
        "scores": scores,
        "caps": caps,
        "gaps": gaps,
        "l3_tasks": tasks,
        "facts": facts,
    }


def main() -> int:
    results = [score_project(project) for project in PROJECTS]
    out = {
        "model": WEIGHTS,
        "hard_rules": [
            "没有真实项目仓，最高 40 分",
            "没有测试/验证命令，最高 60 分",
            "没有 evidence，最高 65 分",
            "GPCF 作为治理中枢单独标记 governance_hub",
        ],
        "results": results,
    }
    output = Path("docs/harness/evidence/l3_admission_assessment.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"l3_admission_assessment=pass projects={len(results)} output={output}")
    for item in results:
        print(f"{item['project']}: score={item['score']} status={item['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
