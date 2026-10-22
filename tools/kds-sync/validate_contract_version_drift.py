#!/usr/bin/env python3
"""契约版本漂移告警（CONFLICT-04 残留）。

对登记在 runtime/contract-version-hashes.yaml 的契约文件做内容哈希比对：
- 内容变化但 version 未变 -> 报 drift（要求升版本或显式更新基线）；
- 版本变化 -> 提示需要重基线（不自动写入）；
- 基线缺失 -> 首次 bootstrap（写入当前哈希）。
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
BASELINE = ROOT / "runtime" / "contract-version-hashes.yaml"

CONTRACTS = [
    ROOT / "01-architecture" / "XAP回执与执行报告规格草案_v0.1.md",
    ROOT / "03-data-ai-knowledge" / "GlobalCloud绿色供应链体系事件合同.md",
    ROOT / "okf" / "knowledge-asset-contract-manifest.yaml",
    WORKSPACE / "GlobalCloud XWAIL" / "schemas-json" / "xap-manifest.schema.json",
]

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
VERSION_RE = re.compile(r"^version:\s*[\"']?([^\"'\n]+)", re.M)


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def version_of(frontmatter: str) -> str:
    m = VERSION_RE.search(frontmatter)
    return m.group(1).strip() if m else "unknown"


def body_hash(text: str) -> str:
    _, body = split_frontmatter(text)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    records: dict[str, dict] = {}
    current = {}
    for path in CONTRACTS:
        label = str(path.relative_to(WORKSPACE))
        if not path.exists():
            print(f"  FAIL missing contract file: {label}")
            return 1
        text = path.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        current[label] = {"version": version_of(fm), "hash": body_hash(text)}

    if not BASELINE.exists():
        BASELINE.write_text(
            yaml.safe_dump({"contracts": current}, allow_unicode=True, sort_keys=True),
            encoding="utf-8",
        )
        print(f"contract_version_drift: baseline created ({len(current)} contracts) = pass")
        return 0

    data = yaml.safe_load(BASELINE.read_text(encoding="utf-8")) or {}
    records = data.get("contracts", {}) or {}
    drift = []
    version_changed = []
    for label, cur in current.items():
        base = records.get(label)
        if not base:
            version_changed.append(f"{label}: new contract (no baseline)")
            continue
        if cur["version"] != base.get("version"):
            version_changed.append(f"{label}: version {base.get('version')} -> {cur['version']} (re-baseline needed)")
        elif cur["hash"] != base.get("hash"):
            drift.append(f"{label}: content changed but version {cur['version']} unchanged")
    missing = [k for k in records if k not in current]

    print(f"contract_version_drift: contracts={len(current)} drift={len(drift)} version_changed={len(version_changed)}")
    for item in drift:
        print(f"  FAIL drift: {item}")
    for item in version_changed:
        print(f"  advise: {item}")
    for item in missing:
        print(f"  FAIL baseline references missing contract: {item}")
    if drift or missing:
        return 1
    print("contract_version_drift = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
