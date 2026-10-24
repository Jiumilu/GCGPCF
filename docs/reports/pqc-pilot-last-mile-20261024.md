---
doc_id: GPCF-DOC-F9B1DDF847
title: PQC 真实试点最后一段：一键收口脚本（2026-10-24）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/pqc-pilot-last-mile-20261024.md
source_path: docs/reports/pqc-pilot-last-mile-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# PQC 真实试点最后一段：一键收口脚本（2026-10-24）

- 目的：把"真实回执到 S4 与 C_real 破 0"压缩成**一条命令**，减少数据到达后的操作失误
- 脚本：`scripts/gpcf_pqc_pilot_close.py`
- 纪律：所有校验都在写台账前执行；dry-run 模式**绝不写任何文件**

## 1. 用法

```bash
# 1) 数据到达后先预检（不写）
python3 scripts/gpcf_pqc_pilot_close.py \
  --vu-id PQC-VU-01 \
  --evidence features/active/F-032-pqc-external-service-via-pvaai/evidence/pilot-receipt-<date>.json

# 2) 预检 status=ready 后执行
python3 scripts/gpcf_pqc_pilot_close.py --vu-id PQC-VU-01 --evidence ... --apply
```

`--apply` 会：推进 VU→S4（`stage/promoted_at/promotion_basis/inferred=false`）→ 追加 `runtime/audit/decision-ledger-20261024.jsonl`（kind=promote_s4）→ 输出 `c_real_before/after`。

## 2. 实测

| 场景 | 结果 |
|---|---|
| 模板证据（占位符） | **status=fail**，problems=4（含模板占位符、缺 data_class: real 等） |
| 合规临时证据 dry-run | **status=ready**，`vu-ledger.yaml` sha256 **未变**（证明不写） |
| 合规证据 + `--apply` | 仅在真实回执到手时使用；脚本会再次跑六项强校验 |

## 3. 与 P12/P14 的关系

- 前置：`AUTH-PG-PQC-REAL-PILOT-20261022`（A1–A4 已批）、M0 已过、契约已登记；
- 本脚本不产生任何业务数据，只做"校验 + 台账登记"；
- 真实回执必须由 PQC 属主按 `pqc-pilot-intake-checklist` 交付 6 项。

## 4. 测试

`tests/test_gpcf_governance_remediation.py::test_pqc_pilot_close_dry_run_never_writes_ledger`
—— 断言模板证据被拒（exit 1）、合规证据 dry-run 通过（exit 0）且 VU 台账 hash 不变。
