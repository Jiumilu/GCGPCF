#!/usr/bin/env python3
"""Sync Cognee P4 live authorization signoff markdown from the JSON payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SIGNOFF_JSON = ROOT / "fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json"
DEFAULT_SIGNOFF_MD = ROOT / "docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", default=str(DEFAULT_SIGNOFF_JSON), help="machine-readable signoff payload")
    parser.add_argument("--output-md", default=str(DEFAULT_SIGNOFF_MD), help="signoff evidence markdown path")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def preserve_frontmatter(md_text: str) -> tuple[str, str]:
    require(md_text.startswith("---\n"), "markdown missing frontmatter")
    end = md_text.find("\n---\n", 4)
    require(end > 0, "markdown frontmatter invalid")
    frontmatter = md_text[: end + 5]
    body = md_text[end + 5 :].lstrip("\n")
    return frontmatter, body


def build_body(payload: dict) -> str:
    owner = payload["owner_signoff"]
    waes = payload["waes_signoff"]
    window = payload["signoff_window"]
    required_false = payload["required_false_until_completed"]

    owner_rows = [
        ["`owner_signer_name`", owner["owner_signer_name"], "Owner 签署人"],
        ["`owner_signer_role`", owner["owner_signer_role"], "签署人角色"],
        ["`owner_signer_token_source`", f"`{owner['owner_signer_token_source']}`", "来源见 P4 precheck/live 证据；live 样本中 `owner_jwt=4`，`project_group_jwt=1`"],
        ["`owner_signed_at`", owner["owner_signed_at"], "ISO-8601 时间"],
        ["`owner_decision`", owner["owner_decision"], "`approve_live_write` 或 `reject`"],
        ["`owner_decision_evidence`", owner["owner_decision_evidence"], "与决策一致的审批说明或截图编号"],
    ]
    waes_rows = [
        ["`waes_signer_name`", waes["waes_signer_name"], "WAES 签署人"],
        ["`waes_signer_role`", waes["waes_signer_role"], "WAES 审批角色"],
        ["`waes_signed_at`", waes["waes_signed_at"], "ISO-8601 时间"],
        ["`waes_decision`", f"`{waes['waes_decision']}`", "见 P4 precheck/live 证据，`waes_pass_rate=1.0`"],
        ["`waes_runtime_dependency_ok`", f"`{str(waes['waes_runtime_dependency_ok']).lower()}`", "见 P4 precheck/live 证据，`runtime_dependency_ok_rate=1.0`"],
        ["`waes_rollback_plan_verified`", f"`{str(waes['waes_rollback_plan_verified']).lower()}`", "见 P4 precheck/live 证据，`rollback_readiness_rate=1.0`"],
    ]
    window_rows = [
        ["`signoff_window_start_at`", window["signoff_window_start_at"], "签核窗口起始时间，ISO-8601"],
        ["`signoff_window_expires_at`", window["signoff_window_expires_at"], "签核窗口截止时间，ISO-8601，必须晚于起始时间"],
        ["`authorization_complete`", str(required_false["authorization_complete"]).lower(), "待双签补齐后改为 `true`"],
    ]
    gate_rows = [
        ["`production_write`", str(required_false["production_write"]).lower(), "未完成双签前必须保持 `false`"],
        ["`accepted`", str(required_false["accepted"]).lower(), "未完成双签前必须保持 `false`"],
        ["`integrated`", str(required_false["integrated"]).lower(), "未完成双签前必须保持 `false`"],
        ["`production_ready`", str(required_false["production_ready"]).lower(), "未完成双签前必须保持 `false`"],
    ]

    pending_fields: list[str] = []
    for section in (owner, waes, window):
        for key, value in section.items():
            if value == "REQUIRED_USER_INPUT":
                pending_fields.append(f"- `{key}`")

    pending_list = "\n".join(pending_fields) if pending_fields else "- 无"

    return f"""# Cognee P4 真实写入 live 授权签核包（待签）

## 1. 说明

本包为 `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002` 人审签字模板，不代表生产执行已完成；不表示生产写入权限已开启。

以下字段若已由现有 P4 precheck/live 证据明确证明，则直接采用证据值；仅保留必须由人工补录的签字事实为 `REQUIRED_USER_INPUT`。

## 2. 证据引用

- 预检证据：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- 演练证据：`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`
- 机读签核实例：`fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json`
- 签核校验：`python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py`
- 同步命令：`python3 tools/kds-sync/sync_cognee_p4_live_authorization_signoff.py`

## 3. 需签字段（Owner）

{table(["字段", "当前值", "说明"], owner_rows)}

## 4. 需签字段（WAES）

{table(["字段", "当前值", "说明"], waes_rows)}

## 5. 签核窗口

{table(["字段", "当前值", "说明"], window_rows)}

## 6. 状态门禁（未签核前不得提升）

{table(["字段", "当前值", "规则"], gate_rows)}

## 7. 固定执行命令清单（仅在签核完成后执行）

```bash
python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py \\
  --require-complete-signoff

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \\
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \\
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \\
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \\
  --allow-live-write

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \\
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

- 监控输出：以 `validate-cognee-p4-real-writeback-live.py` 的 `record_count=5`、`requested_write_count=5`、`live_execution_ready_rate=1.0`、`execution_count=5` 为最小复验基线。
- 回滚入口：如签核过期、字段冲突或 live 输出回归，恢复到 `GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004`，将 `authorization_complete` 改回 `false`，重新进入 dry-run 与授权复核。

## 8. 非声明（本轮签核不变更）

- 不声明 `production_write=true`
- 不声明 `external_api_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`

## 9. 签核后切换条件

需同时满足：

- `cognee_p4_real_writeback_live_output=pass`
- `record_count=5`
- `requested_write_count=5`
- `execution_count=5`
- `pilot_gate_pass=True`
- `live_execution_ready_rate=1.0`
- Owner/WAES 两签字段均非 `REQUIRED_USER_INPUT`，且 `owner_decision=approve_live_write`、`waes_decision=pass`。
- `waes_runtime_dependency_ok=true`、`waes_rollback_plan_verified=true`。
- `signoff_window_start_at` 与 `signoff_window_expires_at` 均为有效 ISO-8601，且 `signoff_window_expires_at > signoff_window_start_at`。
- `owner_signed_at` 与 `waes_signed_at` 必须位于签核窗口内。

## 10. 当前仍待人工补录字段

{pending_list}

## 11. 机读实例更新约定

- 人工签核信息优先写入 `fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json`。
- Markdown 与 JSON 必须保持一致；`validate_cognee_p4_live_authorization_signoff.py` 会同时校验两者。
- 完成签核后需同步更新：
  - `authorization_complete=true`
  - `instance_status=signoff_complete_ready_for_fixed_command_pack`
"""


def main() -> int:
    args = parse_args()
    input_json = Path(args.input_json).resolve()
    output_md = Path(args.output_md).resolve()

    payload = load_json(input_json)
    original_md = read_text(output_md)
    frontmatter, _ = preserve_frontmatter(original_md)
    body = build_body(payload)
    output_md.write_text(frontmatter + "\n" + body.strip() + "\n", encoding="utf-8")
    print(
        "cognee_p4_live_authorization_signoff_sync=pass "
        f"output_md={output_md.relative_to(ROOT).as_posix()} "
        f"input_json={input_json.relative_to(ROOT).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
