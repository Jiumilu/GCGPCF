#!/usr/bin/env python3
"""Build a relationship graph evidence artifact for OKF v0.1 bundles."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUNDLES = {
    "kds": ROOT / ".okf/bundles/kds-v0.1",
    "governance": ROOT / ".okf/bundles/governance-v0.1",
    "architecture": ROOT / ".okf/bundles/architecture-v0.1",
}
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-relationship-graph-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-relationship-graph-20260620.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def split_frontmatter(path: Path) -> dict[str, str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def doc_id_for(path: Path) -> str:
    digest = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:10].upper()
    return f"GPCF-DOC-{digest}"


def load_concepts() -> list[dict[str, str]]:
    concepts: list[dict[str, str]] = []
    for bundle_name, bundle_path in BUNDLES.items():
        if not bundle_path.exists():
            raise SystemExit(f"okf_relationship_graph=fail reason=missing_bundle:{rel(bundle_path)}")
        for path in sorted(bundle_path.rglob("*.md")):
            if path.name in {"index.md", "log.md"}:
                continue
            meta = split_frontmatter(path)
            if not meta.get("type"):
                continue
            concepts.append(
                {
                    "bundle": bundle_name,
                    "okf_path": rel(path),
                    "title": meta.get("title", ""),
                    "type": meta.get("type", ""),
                    "source_path": meta.get("source_path", ""),
                    "kds_path": meta.get("kds_path", ""),
                    "source_hash": meta.get("source_hash", ""),
                    "source_of_record": meta.get("source_of_record", ""),
                    "derivation_policy": meta.get("derivation_policy", ""),
                }
            )
    return concepts


def build_graph(concepts: list[dict[str, str]]) -> dict:
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)

    for bundle_name in BUNDLES:
        bundle_id = f"bundle:{bundle_name}"
        nodes[bundle_id] = {"id": bundle_id, "kind": "bundle", "label": bundle_name}

    for concept in concepts:
        concept_id = f"concept:{concept['okf_path']}"
        source_id = f"source:{concept['source_path']}"
        kds_id = f"kds:{concept['kds_path']}"
        bundle_id = f"bundle:{concept['bundle']}"

        nodes[concept_id] = {
            "id": concept_id,
            "kind": "concept",
            "label": concept["title"],
            "path": concept["okf_path"],
            "type": concept["type"],
        }
        nodes[source_id] = {"id": source_id, "kind": "source_document", "label": concept["source_path"]}
        nodes[kds_id] = {"id": kds_id, "kind": "kds_path", "label": concept["kds_path"]}
        edges.extend(
            [
                {"from": bundle_id, "to": concept_id, "type": "bundle_contains_concept"},
                {"from": concept_id, "to": source_id, "type": "concept_derives_from_source"},
                {"from": concept_id, "to": kds_id, "type": "concept_targets_kds_path"},
            ]
        )
        by_source[concept["source_path"]].append(concept)

    overlaps = {source: items for source, items in by_source.items() if len(items) > 1}
    for source, items in overlaps.items():
        source_id = f"source:{source}"
        for concept in items:
            edges.append(
                {
                    "from": source_id,
                    "to": f"concept:{concept['okf_path']}",
                    "type": "same_source_multi_bundle_view",
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "bundles": sorted(BUNDLES),
        "concepts": concepts,
        "nodes": list(nodes.values()),
        "edges": edges,
        "metrics": {
            "bundle_count": len(BUNDLES),
            "concept_count": len(concepts),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "duplicate_source_count": len(overlaps),
        },
        "boundary": {
            "source_of_record": "KDS / Git controlled documents",
            "derivation_policy": "metadata_only_no_body_copy",
            "does_not_replace_kds": True,
            "does_not_upgrade_business_status": True,
        },
    }


def write_markdown(graph: dict) -> None:
    metrics = graph["metrics"]
    bundle_rows = []
    for bundle_name in graph["bundles"]:
        count = sum(1 for concept in graph["concepts"] if concept["bundle"] == bundle_name)
        bundle_rows.append(f"| {bundle_name} | {count} |")

    edge_counts: dict[str, int] = defaultdict(int)
    for edge in graph["edges"]:
        edge_counts[edge["type"]] += 1
    edge_rows = "\n".join(f"| {edge_type} | {count} |" for edge_type, count in sorted(edge_counts.items()))

    overlap_sources = sorted(
        {
            edge["from"].removeprefix("source:")
            for edge in graph["edges"]
            if edge["type"] == "same_source_multi_bundle_view"
        }
    )
    overlap_rows = "\n".join(f"| `{source}` |" for source in overlap_sources[:20])
    if not overlap_rows:
        overlap_rows = "| none |"

    content = f"""---
doc_id: {doc_id_for(MD_OUT)}
title: OKF v0.1 Relationship Graph Evidence
project: GPCF
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-relationship-graph-20260620.md
source_path: docs/harness/evidence/okf-v01-relationship-graph-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Relationship Graph Evidence

generated_at: {graph["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {graph["status"]} |
| bundles | {metrics["bundle_count"]} |
| concepts | {metrics["concept_count"]} |
| nodes | {metrics["node_count"]} |
| edges | {metrics["edge_count"]} |
| duplicate_source_count | {metrics["duplicate_source_count"]} |
| json | `{rel(JSON_OUT)}` |

## Bundle Coverage

| bundle | concepts |
| --- | ---: |
{chr(10).join(bundle_rows)}

## Edge Types

| edge_type | count |
| --- | ---: |
{edge_rows}

## Multi-bundle Source Views

The following source documents intentionally appear in more than one bundle as scoped views. This is allowed only because KDS/Git remains the source of record.

| source_path |
| --- |
{overlap_rows}

## Boundary

- This graph is derived evidence, not a source of record.
- OKF nodes must be resolved back to `source_path` and `kds_path` before making factual decisions.
- This evidence does not upgrade business, acceptance or integration status.
"""
    write_text(MD_OUT, content)


def main() -> int:
    concepts = load_concepts()
    graph = build_graph(concepts)
    write_text(JSON_OUT, json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    write_markdown(graph)
    metrics = graph["metrics"]
    print(
        "okf_relationship_graph=pass "
        f"bundles={metrics['bundle_count']} "
        f"concepts={metrics['concept_count']} "
        f"nodes={metrics['node_count']} "
        f"edges={metrics['edge_count']} "
        f"duplicate_sources={metrics['duplicate_source_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
