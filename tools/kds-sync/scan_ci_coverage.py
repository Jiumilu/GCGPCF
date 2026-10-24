#!/usr/bin/env python3
"""扫描各仓 CI workflow，按"步骤实际命令"判定 standards/test/build 覆盖（P16-2）。

与按 job 名猜测不同：本脚本解析每个 job 的 steps[].run，匹配测试/构建命令，
避免把 `repository-checks` 这类命名但实际跑 pytest 的 job 误判为缺失。

用法：python3 tools/kds-sync/scan_ci_coverage.py [--json] [--markdown]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
REGISTRY = ROOT / "config" / "project-group-projects.yaml"

TEST_PATTERNS = re.compile(
    r"(pytest|vitest|jest|mocha|npm\s+test|pnpm\s+test|yarn\s+test|go\s+test|cargo\s+test|"
    r"python[0-9.]*\s+-m\s+unittest|tox|nox|make\s+test|ctest)", re.I)
BUILD_PATTERNS = re.compile(
    r"(npm\s+run\s+build|pnpm\s+build|pnpm\s+-r\s+build|yarn\s+build|tsc(\s|$)|vite\s+build|"
    r"webpack|cargo\s+build|go\s+build|mvn\s+package|gradle\s+build|python\s+-m\s+build|"
    r"compileall|make\s+build|dotnet\s+build)", re.I)
STANDARDS_PATTERNS = re.compile(r"gc_standard\.py\"?\s+check", re.I)


def workflow_steps(repo: Path) -> list[dict]:
    items: list[dict] = []
    wf_dir = repo / ".github" / "workflows"
    if not wf_dir.is_dir():
        return items
    for wf in sorted(wf_dir.glob("*")):
        if wf.suffix not in (".yml", ".yaml"):
            continue
        try:
            doc = yaml.safe_load(wf.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        for job_name, job in (doc.get("jobs") or {}).items():
            if not isinstance(job, dict):
                continue
            runs = []
            for step in job.get("steps") or []:
                if isinstance(step, dict) and isinstance(step.get("run"), str):
                    runs.append(step["run"])
            items.append({"file": wf.name, "job": job_name, "runs": runs})
    return items


def classify(repo: Path) -> dict:
    steps = workflow_steps(repo)
    text = "\n".join(r for s in steps for r in s["runs"])
    return {
        "repo": repo.name,
        "workflow_files": sorted({s["file"] for s in steps}),
        "jobs": sorted({s["job"] for s in steps}),
        "standards": bool(STANDARDS_PATTERNS.search(text)),
        "test": bool(TEST_PATTERNS.search(text)),
        "build": bool(BUILD_PATTERNS.search(text)),
        "test_evidence": sorted({m.group(0) for m in TEST_PATTERNS.finditer(text)})[:3],
        "build_evidence": sorted({m.group(0) for m in BUILD_PATTERNS.finditer(text)})[:3],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args()

    repos = [str(p["repo"]) for p in yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["projects"]]
    rows = [classify(PROJECT_ROOT / r) for r in repos]
    summary = {
        "repos": len(rows),
        "standards": sum(r["standards"] for r in rows),
        "test": sum(r["test"] for r in rows),
        "build": sum(r["build"] for r in rows),
    }
    if args.markdown:
        print("| 仓 | standards | test | build | test 依据 | build 依据 |")
        print("|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['repo']} | {'✓' if r['standards'] else '—'} | {'✓' if r['test'] else '—'} | "
                  f"{'✓' if r['build'] else '—'} | {', '.join(r['test_evidence']) or '—'} | {', '.join(r['build_evidence']) or '—'} |")
        print()
    print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
