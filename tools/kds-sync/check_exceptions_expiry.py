#!/usr/bin/env python3
"""受控例外到期检查（P17 纪律：到期自动失效转 warn，不得自动续期）。

用法：
    python3 tools/kds-sync/check_exceptions_expiry.py [--file PATH] [--today YYYY-MM-DD] [--warn-only]

退出码：0 = 无过期；1 = 存在过期（warn-only 时仍为 0 但输出 expired 列表）
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILE = ROOT / "runtime" / "exceptions.yaml"
SOON_DAYS = 30


def parse_date(value) -> date | None:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(text)
        except ValueError:
            return None


def evaluate(doc: dict, today: date) -> dict:
    items = doc.get("exceptions") or []
    expired, soon, invalid = [], [], []
    for item in items:
        ex_id = item.get("exemption_id")
        until = parse_date(item.get("until"))
        if until is None:
            invalid.append(ex_id)
            continue
        if until < today:
            expired.append({"exemption_id": ex_id, "until": until.isoformat()})
        elif (until - today).days <= SOON_DAYS:
            soon.append({"exemption_id": ex_id, "until": until.isoformat(),
                         "days_left": (until - today).days})
        if not item.get("approved_by"):
            invalid.append(ex_id)
    return {"total": len(items), "expired": expired, "expiring_soon": soon, "invalid": invalid}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=str(DEFAULT_FILE))
    parser.add_argument("--today", default=None)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    today = parse_date(args.today) or date.today()
    if not path.exists():
        print(json.dumps({"status": "skip", "reason": f"no exceptions file: {path}"}, ensure_ascii=False))
        return 0

    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    result = evaluate(doc, today)
    result.update({"gate": "exceptions_expiry", "today": today.isoformat(),
                   "warn_only": args.warn_only,
                   "status": "fail" if (result["expired"] or result["invalid"]) else "pass"})
    print(json.dumps(result, ensure_ascii=False))
    if args.warn_only:
        return 0
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
