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
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
REGISTRY = ROOT / "config" / "project-group-projects.yaml"

TEST_PATTERNS = re.compile(
    r"(pytest|vitest|jest|mocha|npm\s+(run\s+)?test|pnpm\s+(-s\s+)?(run\s+)?test|yarn\s+test|go\s+test|cargo\s+test|"
    r"python[0-9.]*\s+-m\s+unittest|tox|nox|make\s+test|ctest)", re.I)
BUILD_PATTERNS = re.compile(
    r"(npm\s+run\s+build|pnpm\s+(-r\s+)?(run\s+)?build|yarn\s+build|tsc(\s|$)|vite\s+build|"
    r"webpack|cargo\s+build|go\s+build|mvn\s+package|gradle\s+build|python\s+-m\s+build|"
    r"compileall|ast\.parse|make\s+build|dotnet\s+build|turbo\s+run\s+build)", re.I)
STANDARDS_PATTERNS = re.compile(r"gc_standard\.py\"?\s+check", re.I)


def tracked_workflow_names(repo: Path) -> set[str]:
    """已被 git 跟踪（= 会真正在 CI 生效）的 workflow 文件名。"""
    try:
        out = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), "ls-files", ".github/workflows"],
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return set()
    return {Path(line).name for line in out.stdout.splitlines() if line.strip()}


def push_pending(repo: Path) -> bool:
    """本地 HEAD 是否领先远端（= 已提交但未推送，CI 尚未生效）。"""
    try:
        out = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), "status", "-sb"],
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return False
    first = out.stdout.splitlines()[0] if out.stdout else ""
    return "ahead" in first


def remote_workflow_text(repo: Path) -> str:
    """远端默认分支上的 workflow 文本（= 真正会触发 CI 的定义）。"""
    for ref in ("origin/main", "origin/master", "origin/HEAD"):
        try:
            ls = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), "ls-tree", "-r", "--name-only",
                                 ref, "--", ".github/workflows"], capture_output=True, text=True, timeout=30)
        except Exception:
            continue
        if ls.returncode != 0 or not ls.stdout.strip():
            continue
        chunks = []
        for path in ls.stdout.splitlines():
            if not path.endswith((".yml", ".yaml")):
                continue
            show = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), "show", f"{ref}:{path}"],
                                  capture_output=True, text=True, timeout=30)
            if show.returncode == 0:
                chunks.append(show.stdout)
        return "\n".join(chunks)
    return ""


def workflow_steps(repo: Path) -> list[dict]:
    items: list[dict] = []
    wf_dir = repo / ".github" / "workflows"
    if not wf_dir.is_dir():
        return items
    tracked = tracked_workflow_names(repo)
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
            items.append({"file": wf.name, "job": job_name, "runs": runs,
                          "tracked": wf.name in tracked})
    return items


SCRIPT_REF = re.compile(r"(?:bash|sh|node|python3?)\s+([\w./-]+\.(?:sh|mjs|js|py))")


def resolve_scripts(repo: Path, runs_text: str) -> str:
    """把 run 中引用的本地脚本内容一并纳入判定（gate.sh 这类封装脚本很常见）。"""
    chunks: list[str] = []
    for ref in sorted(set(SCRIPT_REF.findall(runs_text))):
        path = repo / ref
        if path.is_file() and path.stat().st_size < 200_000:
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


NPM_RUN = re.compile(r"\b(?:npm|pnpm|yarn)\s+(?:-s\s+)?(?:run\s+)?([\w:.-]+)")


def resolve_npm_scripts(repo: Path, runs_text: str, depth: int = 3) -> str:
    """展开 npm/pnpm/yarn 脚本体（quality:ci 这类封装很常见），递归 depth 层。"""
    pkg = repo / "package.json"
    if not pkg.is_file():
        return ""
    try:
        scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts") or {}
    except Exception:
        return ""
    seen: set[str] = set()
    chunks: list[str] = []
    queue = [name for name in NPM_RUN.findall(runs_text) if name in scripts]
    for _ in range(depth):
        nxt: list[str] = []
        for name in queue:
            if name in seen:
                continue
            seen.add(name)
            body = str(scripts.get(name, ""))
            chunks.append(body)
            nxt.extend([n for n in NPM_RUN.findall(body) if n in scripts and n not in seen])
        queue = nxt
        if not queue:
            break
    return "\n".join(chunks)


def classify(repo: Path) -> dict:
    steps = workflow_steps(repo)
    tracked_steps = [s for s in steps if s.get("tracked")]
    runs_text = "\n".join(r for s in steps for r in s["runs"])
    text = runs_text + "\n" + resolve_scripts(repo, runs_text) + "\n" + resolve_npm_scripts(repo, runs_text)
    tracked_text = "\n".join(r for s in tracked_steps for r in s["runs"])
    tracked_text += "\n" + resolve_scripts(repo, tracked_text) + "\n" + resolve_npm_scripts(repo, tracked_text)
    remote_text = remote_workflow_text(repo)
    remote_text += "\n" + resolve_scripts(repo, remote_text) + "\n" + resolve_npm_scripts(repo, remote_text)
    return {
        "repo": repo.name,
        "active_test": bool(TEST_PATTERNS.search(tracked_text)),
        "active_build": bool(BUILD_PATTERNS.search(tracked_text)),
        "push_pending": push_pending(repo),
        "remote_test": bool(TEST_PATTERNS.search(remote_text)),
        "remote_build": bool(BUILD_PATTERNS.search(remote_text)),
        "prepared_only": bool((TEST_PATTERNS.search(text) or BUILD_PATTERNS.search(text)) and not tracked_steps),
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
        print("| 仓 | standards | test | build | active test | active build | test 依据 | build 依据 |")
        print("|---|---|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['repo']} | {'✓' if r['standards'] else '—'} | {'✓' if r['test'] else '—'} | "
                  f"{'✓' if r['build'] else '—'} | {'✓' if r.get('active_test') else '—'} | "
                  f"{'✓' if r.get('active_build') else '—'} | {', '.join(r['test_evidence']) or '—'} | "
                  f"{', '.join(r['build_evidence']) or '—'} |")
        print()
    print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
