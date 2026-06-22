#!/usr/bin/env python3
"""Validate KDS v2 search/filter dry-run semantics.

This script uses local fixtures only. It does not query KDS, vector indexes,
graph stores, GFIS, WAES, or external APIs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "kds" / "search-dry-run.json"


def includes_all_terms(title: str, query: str) -> bool:
    return all(term in title for term in query.split())


def has_acl(obj: dict[str, Any], user_id: str) -> bool:
    return user_id in set(obj.get("aclUserIds", []))


def pool_matches(obj: dict[str, Any], required_pools: list[str]) -> bool:
    object_pools = set(obj.get("poolRefs", []))
    return all(pool in object_pools for pool in required_pools)


def filter_objects(context: dict[str, Any], objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for obj in objects:
        if obj.get("tenantId") != context["tenantId"]:
            continue
        if not has_acl(obj, context["userId"]):
            continue
        if context.get("domain") and obj.get("domain") != context["domain"]:
            continue
        if context.get("poolRefs") and not pool_matches(obj, context["poolRefs"]):
            continue
        if context.get("projectId") and obj.get("projectId") != context["projectId"]:
            continue
        if context.get("ragAdmission") and obj.get("ragAdmission") != context["ragAdmission"]:
            continue
        if obj.get("ragAdmission") == "blocked":
            continue
        if not includes_all_terms(obj.get("title", ""), context["query"]):
            continue
        results.append(obj)

    trust_rank = {"T0": 0, "T1": 1, "T2": 2, "T3": 3, "T4": 4, "T5": 5}
    results.sort(key=lambda item: (trust_rank.get(item.get("trustLevel"), 99), item.get("updatedAt", "")))
    return results


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    context = data["context"]
    expected = data["expected"]
    results = filter_objects(context, data["objects"])
    result_ids = [item["id"] for item in results]
    failures: list[str] = []

    if result_ids != expected["resultIds"]:
        failures.append(f"resultIds expected={expected['resultIds']!r} actual={result_ids!r}")

    for result in results:
        for field in expected["requiredFields"]:
            if field not in result:
                failures.append(f"{result['id']} missing required field {field}")
        if result.get("ragAdmission") == "blocked":
            failures.append(f"{result['id']} blocked item leaked into results")

    leaked = set(result_ids).intersection(expected["blockedResultIds"])
    if leaked:
        failures.append("blocked ids leaked: " + ",".join(sorted(leaked)))

    if failures:
        print("kds_search_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kds_search_dry_run=pass "
        f"objects={len(data['objects'])} "
        f"results={len(results)} "
        "tenant_filter=covered acl_filter=covered domain_filter=covered "
        "pool_filter=covered project_filter=covered rag_filter=covered "
        "keyword_filter=covered result_fields=covered real_kds_reads=0 vector_reads=0 graph_reads=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
