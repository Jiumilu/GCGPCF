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
    "docs/harness/evidence/",
    "docs/harness/loops/",
    "10-archive/",
}

DOC_SKIP_FILES = {
    "09-status/globalcloud-chinese-localization-governance-report.md",
}

REQUIRED_MAIN_DOCUMENT_GROUPS = {
    "project_group_master_plan": [
        "GlobalCloud 项目群总体方案.md",
        "01-architecture/GlobalCloud 项目群总体方案.md",
    ],
    "project_group_implementation_plan": [
        "GlobalCloud 项目群实施方案.md",
    ],
}

MAIN_DOCUMENT_PREFIXES = (
    "00-index/",
    "01-architecture/",
    "02-governance/",
    "03-data-ai-knowledge/",
    "04-ui-delivery/",
    "09-status/",
)

MAIN_DOCUMENT_NAME_KEYWORDS = (
    "README.md",
    "总体方案",
    "实施方案",
    "治理",
    "规范",
    "路线图",
    "矩阵",
    "台账",
    "报告",
)

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
    "artifact",
    "key",
    "primary",
    "queue",
    "review",
    "runtime",
    "verified",
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

    if len(english_words) >= 8 and len(chinese_chars) < max(30, len(english_words) // 2):
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


def is_main_document(path: Path) -> bool:
    source_path = rel(path)
    if source_path.startswith("."):
        return False
    if source_path in DOC_SKIP_FILES:
        return False
    if any(source_path.startswith(prefix) for prefix in DOC_SKIP_PREFIXES):
        return False
    if "/" not in source_path:
        return any(keyword in path.name for keyword in MAIN_DOCUMENT_NAME_KEYWORDS)
    if not any(source_path.startswith(prefix) for prefix in MAIN_DOCUMENT_PREFIXES):
        return False
    if source_path.count("/") > 1:
        return False
    name = path.name
    return any(keyword in name for keyword in MAIN_DOCUMENT_NAME_KEYWORDS)


def main_document_findings(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    findings: list[dict[str, object]] = []
    source_path = rel(path)

    title_line = ""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if line.startswith("title:"):
                    title_line = line.split(":", 1)[1].strip()
                    break
    if title_line and not has_chinese(title_line):
        findings.append(
            {
                "kind": "main_doc_non_chinese_title",
                "path": source_path,
                "line": 1,
                "detail": title_line[:180],
            }
        )

    h1_seen = False
    for line_no, line in strip_code_and_frontmatter(text):
        stripped = line.strip()
        if stripped.startswith("# "):
            h1_seen = True
            if not has_chinese(stripped):
                findings.append(
                    {
                        "kind": "main_doc_non_chinese_h1",
                        "path": source_path,
                        "line": line_no,
                        "detail": stripped[:180],
                    }
                )
            break
    if not h1_seen:
        findings.append(
            {
                "kind": "main_doc_missing_h1",
                "path": source_path,
                "line": 1,
                "detail": "主要文档缺少中文 H1 标题",
            }
        )

    for line_no, line in strip_code_and_frontmatter(text):
        stripped = line.strip()
        if stripped.startswith(("#", "- [", "<", ">", "::")):
            continue
        words = normalized_english_words(stripped)
        chinese_count = len(CHINESE_CHAR.findall(stripped))
        if len(words) >= 6 and chinese_count < len(words):
            findings.append(
                {
                    "kind": "main_doc_english_dominant_line",
                    "path": source_path,
                    "line": line_no,
                    "detail": stripped[:180],
                }
            )
            if len([item for item in findings if item["kind"] == "main_doc_english_dominant_line"]) >= 5:
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


def iter_main_documents() -> list[Path]:
    docs = []
    for path in iter_docs():
        if is_main_document(path):
            docs.append(path)
    return sorted(docs, key=rel)


def required_main_document_findings() -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for group, candidates in REQUIRED_MAIN_DOCUMENT_GROUPS.items():
        if any((ROOT / candidate).exists() for candidate in candidates):
            continue
        findings.append(
            {
                "kind": "main_doc_required_missing",
                "path": candidates[0],
                "line": 1,
                "detail": f"{group} 缺少主要文档；候选路径：{', '.join(candidates)}",
            }
        )
    return findings


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
    lines.extend(["", "## 治理判定", ""])
    if findings:
        lines.extend(
            [
                "- 本报告证明当前项目群存在存量中文化债务。",
                "- 中文化债务应以 `localization_debt=true` 进入 Loop 文档门禁摘要，作为可治理债务持续追踪。",
                "- 中文化债务不等同于文档污染、TOKEN 风险或 KDS 镜像冲突。",
                "- 新增或本轮修改内容触发中文化问题时，本轮状态应为 `rework_required`。",
                "- 历史归档允许保留原文，但不得作为当前有效规范复用。",
            ]
        )
    else:
        lines.extend(
            [
                "- 本报告证明当前项目群中文化门禁已通过。",
                "- `localization_debt=false`，Loop 文档门禁不得继续因中文化债务保持 `rework_required`。",
                "- 后续新增或修改文档仍必须保持中文优先；若重新触发命中项，应重新登记为本地化债务。",
                "- 历史记录中描述过往债务的证据可以保留，但不得覆盖当前门禁结论。",
            ]
        )
    lines.extend(["", "## 样本问题", ""])
    for item in findings[:120]:
        lines.append(
            f"- `{item['path']}:{item['line']}` `{item['kind']}`：{item['detail']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    global ROOT, REPORT
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-findings", type=int, default=80)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    ROOT = args.root.resolve()
    REPORT = ROOT / "09-status/globalcloud-chinese-localization-governance-report.md"

    findings: list[dict[str, object]] = []
    doc_count = 0
    software_count = 0

    for path in iter_docs():
        doc_count += 1
        findings.extend(doc_findings(path))
    main_docs = iter_main_documents()
    findings.extend(required_main_document_findings())
    for path in main_docs:
        findings.extend(main_document_findings(path))
    for path in iter_software_files():
        software_count += 1
        findings.extend(software_findings(path))

    summary = {
        "localization_gate": "pass" if not findings else "fail",
        "docs_checked": doc_count,
        "main_docs_checked": len(main_docs),
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
