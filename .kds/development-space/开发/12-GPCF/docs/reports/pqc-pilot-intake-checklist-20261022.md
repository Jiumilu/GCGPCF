---
doc_id: GPCF-DOC-A3D4097C4E
title: PQC 真实试点数据接入清单（客户确认后按此一次性执行）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/pqc-pilot-intake-checklist-20261022.md
source_path: docs/reports/pqc-pilot-intake-checklist-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# PQC 真实试点数据接入清单（客户确认后按此一次性执行）

- 依据：回执 `AUTH-PG-PQC-REAL-PILOT-20261022`（A1–A4）；工具 `scripts/gpcf_promote_vu_stage.py`
- 模板：`features/active/F-032-pqc-external-service-via-pvaai/evidence/pilot-receipt-template.json`
- **纪律**：模板必须全部替换为真实内容；工具会拒绝任何 `<占位符>`、TODO、`template: true`

## 1. 客户确认后，属主需交付的 6 项

| # | 交付物 | 落到哪里 | 谁签 |
|---|---|---|---|
| 1 | 客户一单（脱敏）接入回执 | `evidence/pilot-receipt-<date>.json`（按模板） | PQC 属主 |
| 2 | 全链步骤记录（S1–S6 各自产物路径） | 同上 `chain_steps` + `evidence_paths` | PQC 属主 |
| 3 | 复核人签认 + 三级审批链 | `reviewer` + `approval_chain` | 复核人/审批人 |
| 4 | 回滚演练记录（时间/命令/耗时/前后断言） | `rollback` | PQC 属主 |
| 5 | `data_class: real` 与 `authorization_granted: true` 声明 | 同上 | 不得由合成数据替代 |
| 6 | F-032 证据回填（tests/build/summary） | `features/active/F-032-*/evidence/` | PQC 属主 |

## 2. GPCF 侧预检（我执行）

```bash
python3 scripts/gpcf_promote_vu_stage.py --vu-id <PQC 的 VU> \
  --evidence features/active/F-032-*/evidence/pilot-receipt-<date>.json \
  --auth-id AUTH-PG-PQC-REAL-PILOT-20261022 --dry-run
```
预期：`status=pass, problems=[]`；若仍报占位符/缺字段，退回属主补齐。

## 3. 通过后我执行的 4 步

1. `--dry-run` 复核 → 正式运行推进 VU 到 S4（写 `runtime/vu-ledger.yaml`：stage/promoted_at/promotion_basis/inferred=false）；
2. `render --check` + `derive --check` 复算，记录 `C_real` 变化（0 → 非零）；
3. 决策台账追加 `kind=promote` 行 + 回执关联；
4. 更新计划台账 P12/P14 状态。

## 4. 反作弊设计（已落地并测试）

- 模板/占位符 → 拒绝（新增校验）；
- `data_class` 为 fixture/dry_run/poc/synthetic → 拒绝；
- 缺 `authorization_granted: true` 或缺回滚记录 → 拒绝；
- 回执缺失/撤销 → 拒绝；
- stage 只允许 S0–S3 → S4，不允许降级或重复推进。
