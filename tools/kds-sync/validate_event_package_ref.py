#!/usr/bin/env python3
"""校验事件信封 packageRef 片段（CONFLICT-06 残留的机器可校验部分）。

不依赖 jsonschema：按 okf/event-envelope-package-ref.schema.json 的
required / type / pattern / additionalProperties 做最小校验。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "okf" / "event-envelope-package-ref.schema.json"
POSITIVE = ROOT / "fixtures" / "events" / "package-ref.positive.json"
NEGATIVE = ROOT / "fixtures" / "events" / "package-ref.negative.json"
CONTRACT = ROOT / "03-data-ai-knowledge" / "GlobalCloud绿色供应链体系事件合同.md"


def validate(obj: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    props = schema.get("properties", {})
    for key in schema.get("required", []):
        if key not in obj:
            errors.append(f"missing required: {key}")
    if schema.get("additionalProperties") is False:
        for key in obj:
            if key not in props:
                errors.append(f"unexpected property: {key}")
    for key, spec in props.items():
        if key not in obj:
            continue
        value = obj[key]
        if spec.get("type") == "string" and not isinstance(value, str):
            errors.append(f"{key}: expected string")
            continue
        if isinstance(value, str):
            if spec.get("minLength") and len(value) < spec["minLength"]:
                errors.append(f"{key}: too short")
            if spec.get("pattern") and not re.match(spec["pattern"], value):
                errors.append(f"{key}: pattern mismatch ({spec['pattern']})")
    return errors


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    pos = json.loads(POSITIVE.read_text(encoding="utf-8"))
    neg = json.loads(NEGATIVE.read_text(encoding="utf-8"))

    pos_errors = validate(pos, schema)
    neg_errors = validate(neg, schema)
    doc = CONTRACT.read_text(encoding="utf-8") if CONTRACT.exists() else ""
    doc_linked = "packageRef" in doc

    print(f"event_package_ref: positive_errors={len(pos_errors)} negative_errors={len(neg_errors)} contract_linked={doc_linked}")
    for e in pos_errors:
        print(f"  FAIL positive: {e}")
    if not neg_errors:
        print("  FAIL negative fixture unexpectedly passed")
    if not doc_linked:
        print("  FAIL event contract missing packageRef linkage")
    if pos_errors or not neg_errors or not doc_linked:
        return 1
    print("event_package_ref = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
