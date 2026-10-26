#!/usr/bin/env python3
"""P1-B 分级判定引擎（原型，v0.3 initial/final）。

输入：sample-intake 风格 JSON/YAML；兼容 C1 字段：
- case_id 或 sample_id
- type
- stage / scope
- requirement_level 或 level
- customer_alias / layer / contract_alias
- acceptance_criteria
- feedback_ref 或 source_ref_alias / env / impact / description / reproduce
- warranty（bool 或 "true"/"false"）
- evidence_refs（mapping）
输出：initial + final；final 缺 E2 → pending FP-00F。
仅本地静态判定；不接网络/模型/真实数据/价格。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEMAND_LEVELS = ("R1", "R2", "R3", "R4")
DEFECT_LEVELS = ("S1", "S2", "S3", "S4")
STAGES = ("test", "trial", "formal")


def _blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _text(doc: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = doc.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _case_id(doc: Dict[str, Any]) -> str:
    return _text(doc, "case_id", "sample_id") or "UNKNOWN"


def _level(doc: Dict[str, Any]) -> str:
    return _text(doc, "requirement_level", "level")


def _severity(doc: Dict[str, Any]) -> str:
    value = _text(doc, "severity")
    if value:
        return value
    level = _text(doc, "level")
    return level if level in DEFECT_LEVELS else ""


def _warranty(doc: Dict[str, Any]) -> Any:
    raw = doc.get("warranty")
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, str):
        value = raw.strip().lower()
        if value == "true":
            return True
        if value == "false":
            return False
    return None


def _refs(doc: Dict[str, Any]) -> Dict[str, Any]:
    refs = doc.get("evidence_refs")
    return refs if isinstance(refs, dict) else {}


def _pending(stage: str, rule_id: str, unknown: List[str], grade: str) -> Dict[str, Any]:
    return {
        "stage": stage,
        "free_paid": "pending",
        "rule_id": rule_id,
        "evidence_grade": grade,
        "final_eligible": False,
        "confidence": 0.2,
        "unknown": unknown,
    }


def _ok(stage: str, free_paid: str, rule_id: str, grade: str = "E1",
        final_eligible: bool = False, confidence: float = 0.8) -> Dict[str, Any]:
    return {
        "stage": stage,
        "free_paid": free_paid,
        "rule_id": rule_id,
        "evidence_grade": grade,
        "final_eligible": final_eligible,
        "confidence": round(confidence, 2),
        "unknown": [],
    }


def initial_demand(doc: Dict[str, Any]) -> Dict[str, Any]:
    unknown: List[str] = []
    stage = _text(doc, "stage")
    scope = _text(doc, "scope")
    level = _level(doc)
    if stage not in STAGES:
        unknown.append("stage missing/invalid")
    if level not in DEMAND_LEVELS:
        unknown.append("requirement_level/level missing/invalid")
    if _blank(doc.get("customer_alias")):
        unknown.append("customer_alias missing")
    if _blank(doc.get("layer")):
        unknown.append("layer missing")
    if _blank(doc.get("acceptance_criteria")):
        unknown.append("acceptance_criteria missing")
    if stage == "formal":
        if _blank(doc.get("contract_alias")):
            unknown.append("contract_alias missing")
        if scope not in ("in", "out"):
            unknown.append("scope missing/invalid for formal")
        if scope == "in" and level in ("R1", "R2") and _text(doc, "contract_alias") in ("none", "unknown"):
            unknown.append("contract_alias none/unknown: no purchased quota for FP-02")
    if unknown:
        return _pending("initial", "FP-00I", unknown, "E0")
    if stage == "test":
        return _ok("initial", "free", "FP-04", confidence=0.85)
    if stage == "trial":
        return _ok("initial", "included", "FP-05", confidence=0.8)
    if level == "R1":
        return _pending("initial", "FP-00I",
                        ["R1 requires FP-07/老卢裁定; not implemented"], "E1")
    if scope == "out":
        return _ok("initial", "paid", "FP-03", confidence=0.8)
    if level == "R2":
        quota = doc.get("quota_remaining")
        if not isinstance(quota, bool):
            return _pending("initial", "FP-00I",
                            ["R2 quota_remaining missing; cannot determine FP-02 vs FP-03"], "E1")
        return _ok("initial", "included" if quota else "paid",
                   "FP-02" if quota else "FP-03", confidence=0.8)
    return _ok("initial", "paid", "FP-03", confidence=0.75)


def initial_defect(doc: Dict[str, Any]) -> Dict[str, Any]:
    unknown: List[str] = []
    severity = _severity(doc)
    warranty = _warranty(doc)
    if severity not in DEFECT_LEVELS:
        unknown.append("severity/level missing/invalid")
    if warranty is None:
        unknown.append("warranty missing/invalid (bool or 'true'/'false')")
    if _blank(doc.get("feedback_ref")) and _blank(doc.get("source_ref_alias")):
        unknown.append("feedback_ref/source_ref_alias missing")
    if _blank(doc.get("env")):
        unknown.append("env missing")
    if _blank(doc.get("description")):
        unknown.append("description missing")
    if _blank(doc.get("reproduce")):
        unknown.append("reproduce missing")
    if _blank(doc.get("impact")):
        unknown.append("impact missing")
    if unknown:
        return _pending("initial", "FP-00I", unknown, "E0")
    if warranty is True:
        return _ok("initial", "free", "FP-01", confidence=0.8)
    return _ok("initial", "paid", "FP-03", confidence=0.75)


def final_result(initial: Dict[str, Any], doc: Dict[str, Any]) -> Dict[str, Any]:
    if initial["free_paid"] == "pending":
        return _pending("final", "FP-00F", list(initial["unknown"]), "E1")

    case_type = doc.get("type")
    stage = _text(doc, "stage")
    # test/trial 无合同：final 不满足 E2，按严格口径 final_eligible=false
    if case_type == "demand" and stage in ("test", "trial"):
        result = _ok("final", initial["free_paid"], initial["rule_id"], grade="E1",
                     final_eligible=False, confidence=min(0.9, initial["confidence"] + 0.05))
        result["unknown"] = ["test/trial: final requires contract/E2; initial only"]
        return result

    refs = _refs(doc)
    missing: List[str] = []
    if case_type == "demand":
        if _blank(refs.get("contract_clause")):
            missing.append("contract_clause E2 missing")
        if _level(doc) in ("R3", "R4") and _blank(refs.get("change_request")):
            missing.append("change_request E2 missing")
    else:
        if _blank(refs.get("warranty_clause")):
            missing.append("warranty_clause E2 missing")
        if _blank(refs.get("ticket")):
            missing.append("ticket E2 missing")
    if missing:
        return _pending("final", "FP-00F", missing, "E1")
    return _ok("final", initial["free_paid"], initial["rule_id"], grade="E2",
               final_eligible=True, confidence=min(0.95, initial["confidence"] + 0.1))


def grade_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(doc, dict):
        raise ValueError("top-level must be a mapping")
    case_type = doc.get("type")
    if case_type not in ("demand", "defect"):
        raise ValueError("type must be demand or defect")
    initial = initial_demand(doc) if case_type == "demand" else initial_defect(doc)
    final = final_result(initial, doc)
    return {
        "case_id": _case_id(doc),
        "type": case_type,
        "level": _level(doc) if case_type == "demand" else _severity(doc),
        "priority": doc.get("priority"),
        "initial": initial,
        "final": final,
        "notes": "prototype; synthetic/local only; no real data/pricing",
    }


def load_document(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("top-level must be a mapping")
    return data


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P1-B grading engine prototype (v0.3 initial/final)")
    parser.add_argument("--file", required=True, help="sample JSON/YAML path")
    parser.add_argument("--output", help="optional output JSON path")
    args = parser.parse_args(argv)
    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"[ERROR] file not found: {path}", file=sys.stderr)
        return 2
    try:
        doc = load_document(path)
        result = grade_document(doc)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
