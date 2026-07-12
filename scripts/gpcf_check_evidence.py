#!/usr/bin/env python3
"""Collect project-profile evidence for a GPCF 2.0 Feature."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from gpcf_feature_lib import append_journal, feature_file, find_feature, read_feature, run_command, update_queue_entry, write_feature


SCRIPT_CHECKS = [
    "scripts/gpcf_feature_lib.py",
    "scripts/gpcf_new_feature.py",
    "scripts/gpcf_dispatch.py",
    "scripts/gpcf_run_loop.py",
    "scripts/gpcf_check_evidence.py",
    "scripts/gpcf_close_feature.py",
    "tools/kds-sync/validate_gpcf_2_feature_workspace.py",
]

UI_EVIDENCE_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
UI_EVIDENCE_TEXT_SUFFIXES = {".md", ".txt", ".json"}
UI_EVIDENCE_NAME_HINTS = ("ui", "visual", "screenshot", "browser", "playwright", "runtime")


def feature_requires(data: dict[str, object], keywords: set[str]) -> bool:
    values: list[str] = [
        str(data.get("name", "")),
        str(data.get("goal", "")),
        str(data.get("project", "")),
    ]
    scope = data.get("scope", {})
    if isinstance(scope, dict):
        in_scope = scope.get("in", [])
        if isinstance(in_scope, list):
            values.extend(str(item) for item in in_scope)
    text = " ".join(values).lower()
    for keyword in keywords:
        if keyword.isascii() and keyword.replace(" ", "").isalnum():
            if re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text):
                return True
            continue
        if keyword in text:
            return True
    return False


def write_result(path: Path, title: str, results: list[tuple[str, str, str]]) -> str:
    lines = [f"# {title}", ""]
    status = "pass"
    for name, item_status, output in results:
        lines.extend([f"## {name}", "", f"status: {item_status}", "", "```text", output, "```", ""])
        if item_status != "pass":
            status = "fail"
    path.write_text("\n".join(lines), encoding="utf-8")
    return status


def write_markdown_preserving_frontmatter(path: Path, body: str) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end != -1:
                path.write_text(text[: end + 5] + "\n" + body, encoding="utf-8")
                return
    path.write_text(body, encoding="utf-8")


def detect_ui_evidence(feature_dir: Path, evidence_dir: Path) -> tuple[str, str]:
    screenshots_file = evidence_dir / "screenshots.txt"
    existing_text = screenshots_file.read_text(encoding="utf-8", errors="ignore").strip() if screenshots_file.exists() else ""
    placeholder_prefixes = (
        "UI evidence required by Feature scope",
        "waived: Feature scope has no UI/browser evidence requirement.",
    )
    if existing_text and not existing_text.startswith(placeholder_prefixes):
        return "pass", existing_text

    candidate_dirs = [evidence_dir, feature_dir / "artifacts"]
    asset_refs: list[str] = []
    note_refs: list[str] = []
    for base_dir in candidate_dirs:
        if not base_dir.exists():
            continue
        for path in sorted(base_dir.rglob("*")):
            if not path.is_file() or path.name == ".gitkeep":
                continue
            rel = path.relative_to(feature_dir).as_posix()
            lower_name = path.name.lower()
            if path.suffix.lower() in UI_EVIDENCE_IMAGE_SUFFIXES:
                asset_refs.append(rel)
                continue
            if path.suffix.lower() in UI_EVIDENCE_TEXT_SUFFIXES and any(hint in lower_name for hint in UI_EVIDENCE_NAME_HINTS):
                note_refs.append(rel)

    if asset_refs or note_refs:
        lines = ["UI evidence detected from Feature artifacts."]
        if asset_refs:
            lines.append("assets:")
            lines.extend(f"- {item}" for item in asset_refs[:12])
        if note_refs:
            lines.append("notes:")
            lines.extend(f"- {item}" for item in note_refs[:12])
        return "pass", "\n".join(lines)

    return "fail", "UI evidence required by Feature scope; provide screenshot/browser evidence before close."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_id")
    args = parser.parse_args()

    feature_dir = find_feature(args.feature_id)
    data = read_feature(feature_file(feature_dir))
    evidence_dir = feature_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    test_results = [
        (
            "validate_gpcf_2_feature_workspace",
            *run_command(["python3", "tools/kds-sync/validate_gpcf_2_feature_workspace.py"]),
        )
    ]
    tests_status = write_result(evidence_dir / "tests.txt", "Tests Evidence", test_results)

    compile_status, compile_output = run_command(["python3", "-X", "pycache_prefix=/private/tmp/gpcf-pycache", "-m", "py_compile", *SCRIPT_CHECKS])
    diff_status, diff_output = run_command(["git", "diff", "--check"])
    build_status = write_result(
        evidence_dir / "build.txt",
        "Build And Lint Evidence",
        [
            ("py_compile_gpcf_scripts", compile_status, compile_output),
            ("git_diff_check", diff_status, diff_output),
        ],
    )

    ui_required = feature_requires(data, {"ui", "界面", "前端", "浏览器", "screenshot", "studio"})
    api_required = feature_requires(data, {"api", "接口", "kds api", "external api", "真实 api"})
    if ui_required:
        screenshots_status, screenshots_text = detect_ui_evidence(feature_dir, evidence_dir)
    else:
        screenshots_status = "waived"
        screenshots_text = "waived: Feature scope has no UI/browser evidence requirement."
    if api_required:
        api_status = "fail"
        api_text = "API evidence required by Feature scope; provide API/dry-run output before close. Real external or KDS API calls still require explicit authorization."
    else:
        api_status = "waived"
        api_text = "waived: Feature scope has no API evidence requirement and no real external or KDS API call is authorized."
    (evidence_dir / "screenshots.txt").write_text(screenshots_text + "\n", encoding="utf-8")
    (evidence_dir / "api.txt").write_text(api_text + "\n", encoding="utf-8")
    summary_status = "pass" if all(status in {"pass", "waived"} for status in [tests_status, build_status, screenshots_status, api_status]) else "fail"
    write_markdown_preserving_frontmatter(
        evidence_dir / "summary.md",
        "\n".join(
            [
                "# 证据摘要",
                "",
                "本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。",
                "",
                f"- tests: {tests_status}",
                f"- build: {build_status}",
                f"- screenshots: {screenshots_status}",
                f"- api: {api_status}",
                "- lint: 已通过 build 证据中的 git diff --check 覆盖。",
                "- risk: 未授权 commit、push、deploy、真实 API、状态提升。",
                "",
            ]
        ),
    )

    data["evidence"] = {
        "tests": tests_status,
        "build": build_status,
        "screenshots": screenshots_status,
        "api": api_status,
        "summary": summary_status,
    }
    blockers = []
    if tests_status != "pass":
        blockers.append("tests evidence failed")
    if build_status != "pass":
        blockers.append("build or lint evidence failed")
    if screenshots_status == "fail":
        blockers.append("UI evidence required")
    if api_status == "fail":
        blockers.append("API evidence required")
    if summary_status != "pass":
        blockers.append("summary evidence failed")
    data["blockers"] = blockers
    data["loop"]["current_step"] = "evaluate"
    data["loop"]["iteration"] = int(data["loop"].get("iteration", 0)) + 1
    write_feature(feature_file(feature_dir), data)
    update_queue_entry(data["id"], status="evaluated" if not blockers else "blocked", role="Evaluator")
    append_journal(
        feature_dir,
        iteration=data["loop"]["iteration"],
        answers=[
            "采集本地可回放证据。",
            "更新 evidence 文件和 feature.yaml 证据状态。",
            "运行工作区 validator、py_compile、git diff --check 和范围证据门禁。",
            "未发现阻塞项。" if not blockers else "；".join(blockers),
            "是，前提是 close gate 通过。" if not blockers else "否。",
        ],
    )

    print(
        "gpcf_feature_evidence "
        f"feature={data['id']} tests={tests_status} build={build_status} "
        f"screenshots={screenshots_status} api={api_status} summary={summary_status}"
    )
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
