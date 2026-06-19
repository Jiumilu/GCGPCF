#!/usr/bin/env python3
"""Generate an OKF v0.1 derived bundle from controlled KDS documents."""

from __future__ import annotations

import argparse
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_INDEX = ROOT / ".okf/kds/index.md"
DEFAULT_OUT = ROOT / ".okf/bundles/kds-v0.1"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/kds-okf-v01-phase1-bundle-report-20260619.md"
TODAY = "2026-06-19"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def title_from_body(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def parse_source_index(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in read_text(path).splitlines():
        if line.startswith("| purpose | source_path | kds_path |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) != 3:
            continue
        purpose, source_path, kds_path = [part.strip("`") for part in parts]
        rows.append({"purpose": purpose, "source_path": source_path, "kds_path": kds_path})
    return rows


def concept_type(source_path: str, title: str) -> str:
    lower = f"{source_path} {title}".lower()
    if "ledger" in lower or "台账" in title:
        return "KDS Ledger"
    if "gate" in lower or "门禁" in title:
        return "Governance Gate"
    if "plan" in lower or "方案" in title or "计划" in title:
        return "Governance Plan"
    if "report" in lower or "报告" in title:
        return "Governance Report"
    if "index" in lower or "索引" in title:
        return "Knowledge Index"
    return "KDS Document"


def tags_for(source_path: str, title: str) -> list[str]:
    tags = ["kds", "okf-derived", "controlled"]
    if source_path.startswith("09-status/"):
        tags.append("status")
    if source_path.startswith("docs/harness/evidence/"):
        tags.append("evidence")
    if "ODF" in title or "odf" in source_path:
        tags.append("odf")
    if "OKF" in title or "okf" in source_path:
        tags.append("okf")
    if "KDS" in title or "kds" in source_path:
        tags.append("kds-governance")
    return sorted(set(tags))


def concept_path(source_path: str) -> Path:
    path = Path("concepts") / source_path
    if path.name in {"index.md", "log.md"}:
        return path.with_name(f"{path.stem}-concept.md")
    return path


def markdown_link_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def generate_concept(row: dict[str, str]) -> tuple[Path, str] | None:
    source_rel = row["source_path"]
    source = ROOT / source_rel
    if not source.exists():
        return None
    source_text = read_text(source)
    meta, body = split_frontmatter(source_text)
    title = meta.get("title") or title_from_body(source, body)
    description = row["purpose"] or title
    timestamp = meta.get("last_reviewed", TODAY)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    tags = ", ".join(tags_for(source_rel, title))
    ctype = concept_type(source_rel, title)
    out_rel = concept_path(source_rel)
    root_link = f"/{out_rel.as_posix()}"

    content = f"""---
type: {ctype}
title: {title}
description: {description}
resource: file://{source.resolve().as_posix()}
tags: [{tags}]
timestamp: {timestamp}T00:00:00Z
kds_path: {row["kds_path"]}
source_path: {source_rel}
source_hash: {source_hash}
source_of_record: kds
derivation_policy: metadata_only_no_body_copy
---

# Summary

{description}

# Source Of Record

| field | value |
| --- | --- |
| source_path | `{source_rel}` |
| kds_path | `{row["kds_path"]}` |
| source_hash | `{source_hash}` |
| source_of_record | `KDS / Git controlled document` |
| derivation_policy | `metadata_only_no_body_copy` |

# Governance Boundary

- This OKF concept is a derived navigation and exchange artifact.
- It does not replace KDS, Git source documents, KDS sync ledgers, ODF ledgers, or Loop evidence.
- Business completion, acceptance, and integration status must be decided from controlled source evidence, not this OKF concept.

# Citations

[1] [{markdown_link_escape(title)}](/../{source_rel})

<!-- okf_concept_id: {root_link.removesuffix(".md")} -->
"""
    return out_rel, content


def write_index(bundle: Path, concepts: list[tuple[Path, dict[str, str]]]) -> None:
    lines = [
        "---",
        'okf_version: "0.1"',
        "---",
        "",
        "# KDS OKF v0.1 Derived Bundle",
        "",
        "This bundle is derived from controlled KDS documents. KDS remains the source of record.",
        "",
        "# Concepts",
        "",
    ]
    for rel_path, row in concepts:
        lines.append(f"* [{row['purpose']}]({rel_path.as_posix()}) - `{row['source_path']}`")
    write_text(bundle / "index.md", "\n".join(lines) + "\n")


def write_log(bundle: Path, count: int) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    lines = [
        "# KDS OKF Bundle Update Log",
        "",
        f"## {TODAY}",
        "",
        f"* **Creation**: Generated metadata-only OKF v0.1 derived bundle with {count} concept documents.",
        f"* **Evidence**: generated_at `{generated_at}`.",
        "* **Boundary**: KDS remains source of record; no source body copy; no production or external API write.",
        "",
    ]
    write_text(bundle / "log.md", "\n".join(lines))


def write_dir_indexes(bundle: Path) -> None:
    for directory in sorted({p.parent for p in bundle.rglob("*.md") if p.parent != bundle}):
        children = sorted(p for p in directory.iterdir() if p.suffix == ".md" and p.name not in {"index.md", "log.md"})
        if not children:
            continue
        lines = [f"# {directory.relative_to(bundle).as_posix()}", ""]
        for child in children:
            text = read_text(child)
            meta, _ = split_frontmatter(text)
            title = meta.get("title", child.stem)
            description = meta.get("description", "")
            lines.append(f"* [{title}]({child.name}) - {description}")
        write_text(directory / "index.md", "\n".join(lines) + "\n")


def write_report(report_path: Path, bundle: Path, concepts: list[tuple[Path, dict[str, str]]]) -> None:
    rows = "\n".join(
        f"| {row['purpose']} | `{row['source_path']}` | `{(bundle / rel_path).relative_to(ROOT).as_posix()}` |"
        for rel_path, row in concepts
    )
    content = f"""---
doc_id: GPCF-DOC-2EC45F2D0B
title: KDS OKF v0.1 Phase 1-2 Derived Bundle Report
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/kds-okf-v01-phase1-bundle-report-20260619.md
source_path: docs/harness/evidence/kds-okf-v01-phase1-bundle-report-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-19
supersedes: []
superseded_by: []
---

# KDS OKF v0.1 Phase 1-2 Derived Bundle Report

日期：2026-06-19

## 结论

已开始执行 KDS 到 OKF v0.1 的受控派生层实施。当前输出为 metadata-only OKF bundle，已覆盖 `.okf/kds/index.md` 当前纳入的 KDS seed 文档；不复制 KDS 源文档正文，不替代 KDS 主存，不升级业务状态。

## Bundle

| item | value |
| --- | --- |
| bundle_path | `{bundle.relative_to(ROOT).as_posix()}` |
| concepts | {len(concepts)} |
| policy | `metadata_only_no_body_copy` |
| source_of_record | `KDS / Git controlled documents` |

## Concept 清单

| purpose | source_path | okf_concept |
| --- | --- | --- |
{rows}

## 边界

- KDS 仍是主存和事实源。
- OKF 是派生交换层和 Agent 消费层。
- 本阶段不执行全量 KDS 盲写。
- 本阶段不写生产系统、数据库或真实外部 API。
- 本阶段不把 OKF 生成解释为业务完成、验收完成或 `accepted/integrated`。
"""
    write_text(report_path, content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", default=str(DEFAULT_SOURCE_INDEX))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()

    source_index = Path(args.source_index)
    out = Path(args.out)
    report = Path(args.report)
    rows = parse_source_index(source_index)
    if args.limit:
        rows = rows[: args.limit]

    concepts: list[tuple[Path, dict[str, str]]] = []
    for row in rows:
        generated = generate_concept(row)
        if generated is None:
            continue
        rel_path, content = generated
        write_text(out / rel_path, content)
        concepts.append((rel_path, row))

    write_index(out, concepts)
    write_log(out, len(concepts))
    write_dir_indexes(out)
    write_report(report, out, concepts)
    print(f"okf_bundle_generate=pass bundle={out.relative_to(ROOT).as_posix()} concepts={len(concepts)} report={report.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
