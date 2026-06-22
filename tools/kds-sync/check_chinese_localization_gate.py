#!/usr/bin/env python3
"""Check documentation and user-facing software text for Chinese-first governance."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "09-status/globalcloud-chinese-localization-governance-report.md"

EXCLUDE_PARTS = {
    ".git",
    ".kds",
    "__pycache__",
    "node_modules",
}

DOC_SKIP_PREFIXES = {
    ".agents/skills/",
    ".codex/skills/",
    ".harness/runs/",
    ".okf/",
    ".okf/bundles/",
    "08-evidence-samples/",
    "10-archive/",
}

DOC_SKIP_FILES = {
    "09-status/globalcloud-chinese-localization-governance-report.md",
}

SOFTWARE_DIRS = {
    "packages",
}

SOFTWARE_SUFFIXES = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".json",
    ".py",
}

TECHNICAL_ALLOWLIST = {
    "AI",
    "API",
    "Brain",
    "Codex",
    "GFIS",
    "GPC",
    "GPCF",
    "HTTP",
    "JSON",
    "KDS",
    "LOOP",
    "Loop",
    "MMC",
    "OKF",
    "PKC",
    "PVAOS",
    "README",
    "SQL",
    "TOKEN",
    "TS",
    "UI",
    "URL",
    "WAES",
    "XGD",
    "XiaoC",
    "XiaoG",
}

SOFTWARE_KEY_ALLOWLIST = {
    "action",
    "api",
    "code",
    "created_at",
    "debug",
    "description",
    "domain",
    "dry_run",
    "error",
    "event",
    "id",
    "message",
    "method",
    "name",
    "owner",
    "path",
    "project",
    "reason",
    "result",
    "source",
    "status",
    "target",
    "timestamp",
    "title",
    "type",
    "updated_at",
    "url",
    "version",
}

ENGLISH_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
CHINESE_CHAR = re.compile(r"[\u4e00-\u9fff]")
INLINE_CODE = re.compile(r"`[^`]+`")
URL = re.compile(r"https?://\S+")
PATH_LIKE = re.compile(r"(?:^|\s)(?:[\w.-]+/)+[\w./-]+")
STRING_LITERAL = re.compile(r"(['\"])(?P<value>(?:\\.|(?!\1).){3,})\1")
JSON_KEY_VALUE = re.compile(r"^\s*\"(?P<key>[A-Za-z0-9_.-]+)\"\s*:\s*\"(?P<value>.*)\"[,}]?\s*$")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_excluded(path: Path) -> bool:
    return bool(set(path.relative_to(ROOT).parts) & EXCLUDE_PARTS)


def strip_code_and_frontmatter(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fence = False
    in_frontmatter = text.startswith("---\n")
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if line_no > 1 and in_frontmatter and stripped == "---":
            in_frontmatter = False
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped or stripped.startswith("|"):
            continue
        lines.append((line_no, line))
    return lines


def normalized_english_words(text: str) -> list[str]:
    text = INLINE_CODE.sub(" ", text)
    text = URL.sub(" ", text)
    text = PATH_LIKE.sub(" ", text)
    words = []
    for match in ENGLISH_WORD.findall(text):
        if match in TECHNICAL_ALLOWLIST:
            continue
        if len(match) <= 2:
            continue
        words.append(match)
    return words


def has_chinese(text: str) -> bool:
    return bool(CHINESE_CHAR.search(text))


def doc_findings(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    content_lines = strip_code_and_frontmatter(text)
    joined = "\n".join(line for _, line in content_lines)
    english_words = normalized_english_words(joined)
    chinese_chars = CHINESE_CHAR.findall(joined)
    findings: list[dict[str, object]] = []

    if english_words and len(chinese_chars) < max(30, len(english_words) // 2):
        findings.append(
            {
                "kind": "doc_english_heavy",
                "path": rel(path),
                "line": 1,
                "detail": f"english_words={len(english_words)} chinese_chars={len(chinese_chars)}",
            }
        )

    for line_no, line in content_lines:
        words = normalized_english_words(line)
        if len(words) >= 8 and not has_chinese(line):
            findings.append(
                {
                    "kind": "doc_english_line",
                    "path": rel(path),
                    "line": line_no,
                    "detail": line.strip()[:180],
                }
            )
            if len(findings) >= 3:
                break
    return findings


def looks_like_user_text(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    if stripped.startswith(("http://", "https://", "/", "./", "../")):
        return False
    if re.fullmatch(r"[A-Z0-9_.:/ -]+", stripped):
        return False
    if re.fullmatch(r"[a-z0-9_.:/-]+", stripped):
        return False
    if has_chinese(stripped):
        return False
    words = normalized_english_words(stripped)
    return len(words) >= 3


def software_findings(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line_no, line in enumerate(text.splitlines(), 1):
        json_match = JSON_KEY_VALUE.match(line)
        if json_match:
            key = json_match.group("key")
            value = json_match.group("value")
            if key in SOFTWARE_KEY_ALLOWLIST and looks_like_user_text(value):
                findings.append(
                    {
                        "kind": "software_english_user_text",
                        "path": rel(path),
                        "line": line_no,
                        "detail": f"{key}: {value[:160]}",
                    }
                )
        else:
            for match in STRING_LITERAL.finditer(line):
                value = match.group("value")
                if looks_like_user_text(value):
                    findings.append(
                        {
                            "kind": "software_english_user_text",
                            "path": rel(path),
                            "line": line_no,
                            "detail": value[:180],
                        }
                    )
                    break
        if len(findings) >= 5:
            break
    return findings


def iter_docs() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        if is_excluded(path):
            continue
        source_path = rel(path)
        if source_path in DOC_SKIP_FILES:
            continue
        if any(source_path.startswith(prefix) for prefix in DOC_SKIP_PREFIXES):
            continue
        paths.append(path)
    return sorted(paths, key=rel)


def iter_software_files() -> list[Path]:
    paths = []
    for top in SOFTWARE_DIRS:
        base = ROOT / top
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in SOFTWARE_SUFFIXES and not is_excluded(path):
                paths.append(path)
    return sorted(paths, key=rel)


def top_bucket(path: str) -> str:
    parts = path.split("/")
    if path.startswith(".agents/skills/") and len(parts) >= 3:
        return "/".join(parts[:3])
    if path.startswith(".codex/skills/") and len(parts) >= 3:
        return "/".join(parts[:3])
    if path.startswith("docs/harness/loops/"):
        return "docs/harness/loops"
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def write_report(summary: dict[str, object], findings: list[dict[str, object]]) -> None:
    by_bucket = Counter(top_bucket(str(item["path"])) for item in findings)
    by_kind = Counter(str(item["kind"]) for item in findings)
    lines = [
        "---",
        "doc_id: GPCF-DOC-0B97A8283D",
        "title: GlobalCloud 项目群中文化治理报告",
        "project: GPCF",
        "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/globalcloud-chinese-localization-governance-report.md",
        "source_path: 09-status/globalcloud-chinese-localization-governance-report.md",
        "sync_direction: bidirectional",
        f"last_reviewed: {date.today().isoformat()}",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GlobalCloud 项目群中文化治理报告",
        "",
        f"生成时间：{datetime.now(timezone.utc).isoformat()}",
        "",
        f"中文化门禁：`{summary['localization_gate']}`",
        "",
        "## 总览",
        "",
        f"- 检查文档：{summary['docs_checked']}",
        f"- 检查软件/样例文件：{summary['software_files_checked']}",
        f"- 问题总数：{summary['findings']}",
        "",
        "## 问题类型",
        "",
    ]
    for kind, count in sorted(by_kind.items()):
        lines.append(f"- `{kind}`：{count}")
    lines.extend(["", "## 重点目录", ""])
    for bucket, count in by_bucket.most_common(30):
        lines.append(f"- `{bucket}`：{count}")
    lines.extend(
        [
            "",
            "## 治理判定",
            "",
            "- 本报告证明当前项目群存在存量中文化债务。",
            "- 中文化债务应以 `localization_debt=true` 进入 Loop 文档门禁摘要，作为可治理债务持续追踪。",
            "- 中文化债务不等同于文档污染、TOKEN 风险或 KDS 镜像冲突，不单独阻断当前文档门禁。",
            "- 新增或本轮修改内容触发中文化问题时，本轮状态应为 `rework_required`。",
            "- 历史归档允许保留原文，但不得作为当前有效规范复用。",
            "",
            "## 样本问题",
            "",
        ]
    )
    for item in findings[:120]:
        lines.append(
            f"- `{item['path']}:{item['line']}` `{item['kind']}`：{item['detail']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-findings", type=int, default=80)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    doc_count = 0
    software_count = 0

    for path in iter_docs():
        doc_count += 1
        findings.extend(doc_findings(path))
    for path in iter_software_files():
        software_count += 1
        findings.extend(software_findings(path))

    summary = {
        "localization_gate": "pass" if not findings else "fail",
        "docs_checked": doc_count,
        "software_files_checked": software_count,
        "findings": len(findings),
        "findings_by_kind": dict(Counter(str(item["kind"]) for item in findings)),
        "sample_findings": findings[: args.max_findings],
    }

    if args.write_report:
        write_report(summary, findings)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"localization_gate={summary['localization_gate']}")
        print(f"docs_checked={doc_count}")
        print(f"software_files_checked={software_count}")
        print(f"findings={len(findings)}")
        for kind, count in sorted(summary["findings_by_kind"].items()):
            print(f"{kind}={count}")
        for item in findings[: args.max_findings]:
            print(f"{item['path']}:{item['line']}: {item['kind']}: {item['detail']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
