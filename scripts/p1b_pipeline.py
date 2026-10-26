#!/usr/bin/env python3
"""P1-B sample-intake -> grading pipeline.

输入：C1 风格 sample-intake（含 P1-B 判定附加字段）。
输出：intake 校验结果 + 引擎 initial/final。
仅本地静态处理；不接网络/模型/真实数据/价格。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

from p1_sample_intake_validator import validate_document as validate_c1_intake
from p1b_grading_engine import grade_document, load_document

EXTRA_FIELDS = {
    "demand": ("acceptance_criteria",),
    "defect": ("env", "impact", "description", "reproduce"),
}


def _blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _level(doc: Dict[str, Any]) -> str:
    value = doc.get("requirement_level") or doc.get("level") or ""
    return str(value).strip()


def _warranty_valid(doc: Dict[str, Any]) -> bool:
    value = doc.get("warranty")
    if isinstance(value, bool):
        return True
    return isinstance(value, str) and value.strip().lower() in ("true", "false")


def validate_intake(doc: Any) -> List[str]:
    if not isinstance(doc, dict):
        return ["top-level must be a mapping"]
    violations = list(validate_c1_intake(doc))
    case_type = doc.get("type")
    if case_type == "demand":
        for field in EXTRA_FIELDS["demand"]:
            if _blank(doc.get(field)):
                violations.append(f"missing {field} (grading field)")
        if doc.get("stage") == "formal" and _blank(doc.get("scope")):
            violations.append("missing scope (formal grading field)")
        if (doc.get("stage") == "formal" and doc.get("scope") == "in"
                and _level(doc) == "R2" and not isinstance(doc.get("quota_remaining"), bool)):
            violations.append("missing/invalid quota_remaining (R2 FP-02/03)")
    elif case_type == "defect":
        if not _warranty_valid(doc):
            violations.append("warranty must be bool or 'true'/'false'")
        for field in EXTRA_FIELDS["defect"]:
            if _blank(doc.get(field)):
                violations.append(f"missing {field} (grading field)")
    return list(dict.fromkeys(violations))


def run_pipeline(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(doc, dict):
        raise ValueError("top-level must be a mapping")
    case_type = doc.get("type")
    missing = validate_intake(doc)
    if case_type not in ("demand", "defect"):
        return {
            "case_id": doc.get("case_id") or doc.get("sample_id") or "UNKNOWN",
            "intake": {"status": "fail", "missing": missing or ["type must be demand or defect"]},
            "grading": None,
            "notes": "pipeline prototype; synthetic/local only; no real data/pricing",
        }
    grading = grade_document(doc)
    final_pending = grading["final"]["free_paid"] == "pending"
    status = "fail" if missing else ("pending" if final_pending else "pass")
    return {
        "case_id": grading["case_id"],
        "intake": {"status": status, "missing": missing},
        "grading": grading,
        "notes": "pipeline prototype; synthetic/local only; no real data/pricing",
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P1-B sample-intake -> grading pipeline")
    parser.add_argument("--file", required=True, help="sample-intake JSON/YAML")
    parser.add_argument("--output", help="optional output JSON path")
    args = parser.parse_args(argv)
    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"[ERROR] file not found: {path}", file=sys.stderr)
        return 2
    try:
        doc = load_document(path)
        result = run_pipeline(doc)
    except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output).expanduser()
        if not output.parent.exists():
            print(f"[ERROR] output directory not found: {output.parent}", file=sys.stderr)
            return 2
        try:
            output.write_text(text + "\n", encoding="utf-8")
        except OSError as error:
            print(f"[ERROR] cannot write output: {error}", file=sys.stderr)
            return 2
    else:
        print(text)
    return 0 if result["intake"]["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
