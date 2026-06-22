#!/usr/bin/env python3
"""Smoke-test agent-style retrieval over the KDS OKF derived bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLE = ROOT / ".okf/bundles/kds-v0.1"
DEFAULT_JSON = ROOT / "docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.json"
DEFAULT_MD = ROOT / "docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md"

QUERIES = [
    {
        "query": "KDS 开发空间安全规范",
        "expected_source_path": "02-governance/GlobalCloud项目群KDS开发空间安全规范.md",
    },
    {
        "query": "ODF Phase 7 小批量样本",
        "expected_source_path": "09-status/odf-phase7-small-batch-execution-plan.md",
    },
    {
        "query": "KDS OKF v0.1 全量派生层实施方案",
        "expected_source_path": "09-status/kds-okf-v01-full-implementation-plan.md",
    },
    {
        "query": "KDS Markdown 化 OKF 兼容层闭环方案",
        "expected_source_path": "09-status/kds-md-okf-implementation-closure-plan.md",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def split_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
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
        data[key.strip()] = value.strip().strip('"')
    return data, body


def load_concepts(bundle: Path) -> list[dict[str, str]]:
    concepts: list[dict[str, str]] = []
    for path in sorted(bundle.rglob("*.md")):
        if path.name in {"index.md", "log.md"}:
            continue
        meta, body = split_frontmatter(path)
        if not meta.get("type"):
            continue
        searchable = " ".join(
            [
                meta.get("title", ""),
                meta.get("description", ""),
                meta.get("tags", ""),
                meta.get("source_path", ""),
                meta.get("kds_path", ""),
                body[:2000],
            ]
        ).lower()
        concepts.append(
            {
                "okf_path": path.relative_to(ROOT).as_posix(),
                "title": meta.get("title", ""),
                "source_path": meta.get("source_path", ""),
                "kds_path": meta.get("kds_path", ""),
                "searchable": searchable,
            }
        )
    return concepts


def score(query: str, concept: dict[str, str]) -> int:
    terms = [term.lower() for term in query.replace("v0.1", "v01").replace("-", " ").split() if term.strip()]
    searchable = concept["searchable"].replace("v0.1", "v01").replace("-", " ")
    return sum(1 for term in terms if term in searchable)


def run_smoke(bundle: Path) -> dict:
    concepts = load_concepts(bundle)
    results = []
    for item in QUERIES:
        ranked = sorted(
            concepts,
            key=lambda concept: (score(item["query"], concept), item["query"] in concept["searchable"]),
            reverse=True,
        )
        top = ranked[0] if ranked else {}
        passed = top.get("source_path") == item["expected_source_path"]
        results.append(
            {
                "query": item["query"],
                "expected_source_path": item["expected_source_path"],
                "top_source_path": top.get("source_path", ""),
                "top_okf_path": top.get("okf_path", ""),
                "top_title": top.get("title", ""),
                "score": score(item["query"], top) if top else 0,
                "status": "pass" if passed else "fail",
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bundle": bundle.relative_to(ROOT).as_posix(),
        "concepts": len(concepts),
        "queries": results,
        "status": "pass" if all(result["status"] == "pass" for result in results) else "fail",
    }


def write_markdown(report: dict, path: Path) -> None:
    rows = "\n".join(
        "| {query} | `{expected}` | `{actual}` | `{okf}` | {status} |".format(
            query=result["query"].replace("|", "\\|"),
            expected=result["expected_source_path"],
            actual=result["top_source_path"],
            okf=result["top_okf_path"],
            status=result["status"],
        )
        for result in report["queries"]
    )
    content = f"""---
doc_id: GPCF-DOC-931CDE09CE
title: KDS OKF v0.1 Agent Consumption Smoke Test
project: KDS
related_projects: [GPCF, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md
source_path: docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# KDS OKF v0.1 Agent Consumption Smoke Test

generated_at: {report["generated_at"]}

## Scope

This smoke test checks whether agent-style keyword queries can recover the expected KDS source document from the OKF v0.1 derived bundle. It is not a semantic search benchmark and does not prove business completion.

## Summary

| metric | value |
| --- | --- |
| status | {report["status"]} |
| bundle | `{report["bundle"]}` |
| concepts | {report["concepts"]} |
| queries | {len(report["queries"])} |

## Results

| query | expected_source_path | top_source_path | top_okf_path | status |
| --- | --- | --- | --- | --- |
{rows}

## Boundary

- OKF is a derived consumption layer.
- KDS/Git controlled documents remain the source of record.
- This test validates discoverability only, not acceptance or integration status.
"""
    write_text(path, content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", default=str(DEFAULT_BUNDLE))
    parser.add_argument("--json", default=str(DEFAULT_JSON))
    parser.add_argument("--markdown", default=str(DEFAULT_MD))
    args = parser.parse_args()

    report = run_smoke(Path(args.bundle))
    write_text(Path(args.json), json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report, Path(args.markdown))
    print(f"okf_agent_smoke={report['status']} concepts={report['concepts']} queries={len(report['queries'])}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
