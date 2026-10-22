#!/usr/bin/env python3
"""校验 XAP 错误码是否全部登记在 runtime/xap-error-code-registry.yaml。

扫描三方来源：GPCF XAP 规格/清单、XWAIL 脚本/schema、WAME 受理实现。
未登记码视为违规；登记表重复码视为违规。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
REGISTRY = ROOT / "runtime" / "xap-error-code-registry.yaml"
CODE_RE = re.compile(r"XAP-\d{4}")

SOURCE_GLOBS = [
    (ROOT / "01-architecture", "*.md"),
    (WORKSPACE / "GlobalCloud XWAIL" / "scripts", "**/*.py"),
    (WORKSPACE / "GlobalCloud XWAIL" / "schemas-json", "**/*.json"),
    (WORKSPACE / "GlobalCloud XWAIL" / "tools", "**/*.py"),
    (WORKSPACE / "GlobalCloud WAME" / "server" / "xap-intake", "**/*.py"),
    (WORKSPACE / "GlobalCloud WAME" / "tests", "**/*.py"),
]


def main() -> int:
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    codes = [item["code"] for item in reg.get("codes", []) if isinstance(item, dict) and item.get("code")]
    dup = sorted({c for c in codes if codes.count(c) > 1})
    known = set(codes)

    found: dict[str, list[str]] = {}
    for base, pattern in SOURCE_GLOBS:
        if not base.exists():
            continue
        for path in base.glob(pattern):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for code in CODE_RE.findall(text):
                found.setdefault(code, []).append(str(path.relative_to(WORKSPACE)))

    unregistered = sorted(set(found) - known)
    unseen = sorted(known - set(found))

    print(f"xap_error_code_registry: codes={len(codes)} sources={len(found)} unregistered={len(unregistered)} duplicates={len(dup)}")
    if unseen:
        print(f"  note: registered but not referenced in scanned sources: {', '.join(unseen)}")
    for code in dup:
        print(f"  FAIL duplicate registry code: {code}")
    for code in unregistered:
        files = found[code][:3]
        print(f"  FAIL unregistered code: {code} in {', '.join(files)}")

    if dup or unregistered:
        return 1
    print("xap_error_code_registry = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
