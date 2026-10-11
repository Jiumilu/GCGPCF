#!/usr/bin/env python3
"""Validate the CWME B4 ontology chain (files + manifest reconciliation + anti-drift + optional deep gate).

Deep mode (`--deep`) additionally runs the KDS-side ci-gate.sh (needs .venv + optionally docker/Neo4j).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KDS = ROOT.parent / "GlobalCloud KDS"
ONT = KDS / "世界资产/世界模型引擎/ontology"

REQUIRED = [
    "cwme-ext.ttl", "cwme-shapes-min.ttl", "cwme-sample-ok.ttl", "cwme-sample-bad.ttl",
    "cwme_gen.py", "verify_ontology.py", "verify_generated.py", "requirements.txt", "ci-gate.sh",
    "generated/GEN_MANIFEST.json", "generated/ts/cwme-types.ts", "generated/sql/cwme_schema.sql",
    "generated/cypher/cwme_graph.cypher", "generated/llm/cwme-vocab.json",
    "neo4j/sync_sample.py", "neo4j/sample-load.cypher", "neo4j/verify_queries.cypher",
    "README.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deep", action="store_true",
                    help="同时运行 ci-gate.sh 深检（需 .venv；约 30s）")
    a = ap.parse_args()

    for rel in REQUIRED:
        require((ONT / rel).exists(), f"missing file: {rel}")

    manifest = json.loads((ONT / "generated/GEN_MANIFEST.json").read_text(encoding="utf-8"))

    # 1 manifest 哈希对账
    mismatches = []
    for item in manifest["outputs"]:
        p = ONT / "generated" / item["path"]
        if not p.exists() or sha256(p) != item["sha256"]:
            mismatches.append(item["path"])
    require(not mismatches, f"manifest hash mismatch: {mismatches}")

    # 2 源头防漂移（静态）：本体哈希 == manifest 记录
    require(sha256(ONT / manifest["source"]) == manifest["source_sha256"],
            "source drift: cwme-ext.ttl 与 generated/ 不同步（重跑 cwme_gen.py 并提交）")

    # 3 加载脚本内容标记
    load = (ONT / "neo4j/sample-load.cypher").read_text(encoding="utf-8")
    require("MERGE" in load and "CREATE CONSTRAINT" in load,
            "sample-load.cypher missing MERGE/CONSTRAINT")
    require(len(load.splitlines()) >= 1000, "sample-load.cypher 行数异常")

    # 4 ci-gate 可执行
    gate = ONT / "ci-gate.sh"
    require(os.access(gate, os.X_OK), "ci-gate.sh 不可执行（chmod +x ci-gate.sh）")

    # 5 深度门禁（可选）
    if a.deep:
        require((ONT / ".venv/bin/python").exists(), "deep 模式需要 ontology/.venv（uv venv .venv）")
        r = subprocess.run([str(gate)], cwd=str(ONT), text=True, capture_output=True, timeout=900)
        require(r.returncode == 0, "deep gate failed:\n" + (r.stdout or r.stderr)[-1200:])
        deep_status = "deep=pass"
    else:
        deep_status = "deep=skipped"

    print(f"cwme_ontology_chain=pass required={len(REQUIRED)} "
          f"manifest_outputs={len(manifest['outputs'])} source_sync=ok "
          f"sample_load_lines={len(load.splitlines())} {deep_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
