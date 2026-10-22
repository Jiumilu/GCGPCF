#!/usr/bin/env python3
"""把价值单元（VU）推进到 S4「真实业务验证」——带强校验，防止合成数据抬 C_real。

纪律（老卢 2026-10-22 目标硬纪律②）：不得用 fixture / PoC / dry-run / 合成数据提升 C_real。
因此本工具在写台账前强制检查：
  1. evidence 文件存在，且含 `data_class: real` 或 `"data_class": "real"`
  2. evidence 含 `authorization_granted: true`
  3. evidence 含回滚记录（`rollback:` / `回滚`）
  4. 回执台账存在匹配 auth_id，且 granted_by 非空、revoked_at 为空
  5. 当前 stage ∈ S0–S3（只允许升级，不允许降级）
  6. data_class 不得为 fixture/dry_run/poc/synthetic

用法：
    python3 scripts/gpcf_promote_vu_stage.py --vu-id PQC-VU-01 --evidence <path> --auth-id AUTH-... [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "runtime" / "vu-ledger.yaml"
RECEIPTS = ROOT / "runtime" / "authorization-receipts.yaml"
ALLOWED_FROM = {"S0", "S1", "S2", "S3"}
FORBIDDEN_DATA_CLASS = {"fixture", "dry_run", "poc", "synthetic"}
# 反作弊：模板/占位符/TODO 一律拒绝（防止把模板当真实证据推进 S4）
PLACEHOLDER_MARKERS = ("<", ">", "TODO", "TBD", "占位", '"template": true', "template: true")


def validate_evidence(text: str) -> list[str]:
    problems = []
    if any(marker in text for marker in PLACEHOLDER_MARKERS if marker not in ("<", ">")):
        problems.append("evidence 含模板占位符/TODO，必须替换为真实内容")
    if "<" in text or ">" in text:
        problems.append("evidence 含尖括号占位符，必须替换为真实内容")
    if "data_class: real" not in text and '"data_class": "real"' not in text:
        problems.append("evidence 缺少 data_class: real（禁止用 fixture/dry_run/poc/synthetic 提升）")
    if "authorization_granted: true" not in text and '"authorization_granted": true' not in text:
        problems.append("evidence 缺少 authorization_granted: true")
    if "rollback" not in text.lower() and "回滚" not in text:
        problems.append("evidence 缺少回滚记录")
    for bad in FORBIDDEN_DATA_CLASS:
        if f"data_class: {bad}" in text or f'"data_class": "{bad}"' in text:
            problems.append(f"evidence 声明了禁用的 data_class: {bad}")
    return problems


def validate_receipt(receipts_doc: dict, auth_id: str) -> list[str]:
    problems = []
    match = [r for r in (receipts_doc.get("receipts") or []) if r.get("auth_id") == auth_id]
    if not match:
        return [f"回执台账缺少 auth_id: {auth_id}"]
    receipt = match[0]
    if not receipt.get("granted_by"):
        problems.append("回执缺少 granted_by")
    if receipt.get("revoked_at"):
        problems.append("回执已撤销")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vu-id", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--auth-id", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ledger", default=str(LEDGER), help="VU 台账路径（测试/彩排用）")
    parser.add_argument("--receipts", default=str(RECEIPTS), help="回执台账路径（测试/彩排用）")
    args = parser.parse_args()

    ledger_path = Path(args.evidence)
    if not ledger_path.exists():
        print(json.dumps({"status": "fail", "problems": [f"evidence 不存在: {args.evidence}"]}, ensure_ascii=False))
        return 1

    problems = validate_evidence(ledger_path.read_text(encoding="utf-8"))
    receipts_path = Path(args.receipts)
    receipts_doc = yaml.safe_load(receipts_path.read_text(encoding="utf-8")) if receipts_path.exists() else {}
    problems += validate_receipt(receipts_doc, args.auth_id)

    ledger_file = Path(args.ledger)
    ledger_doc = yaml.safe_load(ledger_file.read_text(encoding="utf-8"))
    units = ledger_doc.get("vu_units") or []
    target = next((u for u in units if u.get("vu_id") == args.vu_id), None)
    if target is None:
        problems.append(f"台账中不存在 VU: {args.vu_id}")
    elif str(target.get("stage")) not in ALLOWED_FROM:
        problems.append(f"当前 stage={target.get('stage')}，仅允许从 S0–S3 升级到 S4")

    result = {
        "gate": "vu_stage_promote",
        "vu_id": args.vu_id,
        "to_stage": "S4",
        "auth_id": args.auth_id,
        "evidence": args.evidence,
        "dry_run": args.dry_run,
        "problems": problems,
        "status": "fail" if problems else "pass",
    }
    if problems:
        print(json.dumps(result, ensure_ascii=False))
        return 1

    if not args.dry_run:
        target["stage"] = "S4"
        target["stage_evidence"] = f"真实业务验证（回执 {args.auth_id}）；证据 {args.evidence}"
        target["promoted_at"] = "2026-10-22"
        target["promotion_basis"] = "P14 判据：真实单据/数据 + 回执 + 回滚记录，data_class=real"
        target["inferred"] = False
        ledger_file.write_text(yaml.safe_dump(ledger_doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
        result["written"] = True
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
