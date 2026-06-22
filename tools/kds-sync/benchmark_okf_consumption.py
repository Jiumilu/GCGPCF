#!/usr/bin/env python3
"""Benchmark deterministic OKF v0.1 collection consumption across bundles."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUNDLES = {
    "kds": ROOT / ".okf/bundles/kds-v0.1",
    "governance": ROOT / ".okf/bundles/governance-v0.1",
    "architecture": ROOT / ".okf/bundles/architecture-v0.1",
}
DEFAULT_JSON = ROOT / "docs/harness/evidence/okf-v01-consumption-benchmark-20260620.json"
DEFAULT_MD = ROOT / "docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md"

QUERIES = [
    {
        "query": "KDS 开发空间安全规范",
        "bundle": "kds",
        "expected_source_path": "02-governance/GlobalCloud项目群KDS开发空间安全规范.md",
    },
    {
        "query": "KDS Markdown 化 OKF 兼容层闭环方案",
        "bundle": "kds",
        "expected_source_path": "09-status/kds-md-okf-implementation-closure-plan.md",
    },
    {
        "query": "Loop 控制板",
        "bundle": "governance",
        "expected_source_path": "02-governance/loop/LOOP_CONTROL_BOARD.md",
    },
    {
        "query": "ODF Phase 7 小批量样本执行方案",
        "bundle": "governance",
        "expected_source_path": "09-status/odf-phase7-small-batch-execution-plan.md",
    },
    {
        "query": "体系总架构",
        "bundle": "architecture",
        "expected_source_path": "01-architecture/GlobalCloud绿色供应链体系总架构.md",
    },
    {
        "query": "三阶段激活深度",
        "bundle": "architecture",
        "expected_source_path": "01-architecture/GlobalCloud体系最小闭环与三阶段激活深度总表.md",
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_concepts() -> list[dict[str, str]]:
    concepts: list[dict[str, str]] = []
    for bundle_name, bundle_path in BUNDLES.items():
        if not bundle_path.exists():
            raise SystemExit(f"okf_consumption_benchmark=fail reason=missing_bundle:{rel(bundle_path)}")
        for path in sorted(bundle_path.rglob("*.md")):
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
                    "bundle": bundle_name,
                    "okf_path": rel(path),
                    "title": meta.get("title", ""),
                    "source_path": meta.get("source_path", ""),
                    "kds_path": meta.get("kds_path", ""),
                    "searchable": searchable,
                }
            )
    return concepts


def terms_for(query: str) -> list[str]:
    normalized = query.replace("v0.1", "v01").replace("-", " ").lower()
    return [term for term in normalized.split() if term.strip()]


def score(query: str, concept: dict[str, str]) -> int:
    searchable = concept["searchable"].replace("v0.1", "v01").replace("-", " ")
    return sum(2 if term == concept["title"].lower() else 1 for term in terms_for(query) if term in searchable)


def run_benchmark(concepts: list[dict[str, str]]) -> dict:
    results = []
    for item in QUERIES:
        scoped = [concept for concept in concepts if concept["bundle"] == item["bundle"]]
        ranked = sorted(scoped, key=lambda concept: (score(item["query"], concept), concept["title"]), reverse=True)
        top = ranked[0] if ranked else {}
        passed = top.get("source_path") == item["expected_source_path"]
        results.append(
            {
                "query": item["query"],
                "bundle": item["bundle"],
                "expected_source_path": item["expected_source_path"],
                "top_source_path": top.get("source_path", ""),
                "top_okf_path": top.get("okf_path", ""),
                "top_title": top.get("title", ""),
                "score": score(item["query"], top) if top else 0,
                "status": "pass" if passed else "fail",
            }
        )
    passed_count = sum(1 for result in results if result["status"] == "pass")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if passed_count == len(results) else "fail",
        "concepts": len(concepts),
        "queries": results,
        "passed_queries": passed_count,
        "total_queries": len(results),
        "boundary": {
            "source_of_record": "KDS / Git controlled documents",
            "derivation_policy": "metadata_only_no_body_copy",
            "benchmark_scope": "deterministic keyword lookup over OKF metadata",
            "does_not_replace_semantic_search": True,
        },
    }


def write_markdown(report: dict, path: Path, json_path: Path) -> None:
    rows = "\n".join(
        "| {query} | {bundle} | `{expected}` | `{actual}` | `{okf}` | {score} | {status} |".format(
            query=result["query"].replace("|", "\\|"),
            bundle=result["bundle"],
            expected=result["expected_source_path"],
            actual=result["top_source_path"],
            okf=result["top_okf_path"],
            score=result["score"],
            status=result["status"],
        )
        for result in report["queries"]
    )
    content = f"""---
doc_id: GPCF-DOC-C7697CB4E6
title: OKF v0.1 Consumption Benchmark Evidence
project: GPCF
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md
source_path: docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Consumption Benchmark Evidence

generated_at: {report["generated_at"]}

## Scope

This benchmark verifies deterministic metadata lookup across KDS, Governance and Architecture OKF v0.1 bundles. It validates navigability and source recovery only.

## Summary

| metric | value |
| --- | --- |
| status | {report["status"]} |
| concepts | {report["concepts"]} |
| passed_queries | {report["passed_queries"]} |
| total_queries | {report["total_queries"]} |
| json | `{rel(json_path)}` |

## Results

| query | bundle | expected_source_path | top_source_path | top_okf_path | score | status |
| --- | --- | --- | --- | --- | ---: | --- |
{rows}

## Boundary

- This is a deterministic metadata benchmark, not a semantic search or performance benchmark.
- OKF remains a derived consumption layer.
- KDS/Git controlled documents remain the source of record.
- This evidence does not upgrade business, acceptance or integration status.
"""
    write_text(path, content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default=str(DEFAULT_JSON))
    parser.add_argument("--markdown", default=str(DEFAULT_MD))
    args = parser.parse_args()

    report = run_benchmark(load_concepts())
    json_path = Path(args.json)
    markdown_path = Path(args.markdown)
    write_text(json_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report, markdown_path, json_path)
    print(
        "okf_consumption_benchmark={status} concepts={concepts} passed={passed}/{total}".format(
            status=report["status"],
            concepts=report["concepts"],
            passed=report["passed_queries"],
            total=report["total_queries"],
        )
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
