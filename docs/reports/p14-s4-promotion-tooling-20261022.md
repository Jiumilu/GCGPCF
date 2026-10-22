---
doc_id: GPCF-DOC-04CECBF090
title: P14 · VU 进入 S4 的机检工具（防合成数据抬 C_real）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p14-s4-promotion-tooling-20261022.md
source_path: docs/reports/p14-s4-promotion-tooling-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P14 · VU 进入 S4 的机检工具（防合成数据抬 C_real）

- 日期：2026-10-22｜工具：`scripts/gpcf_promote_vu_stage.py`｜测试：`tests/test_gpcf_governance_remediation.py`
- 目的：把目标硬纪律②（不得用 fixture/PoC/dry-run/合成数据提升 `C_real`）**变成可执行校验**，而不是靠自觉

## 1. 工具做什么

把指定 VU 从 S0–S3 推进到 **S4（真实业务验证）**，并在写台账前强制校验六项：

| # | 校验 | 不通过即拒绝 |
|---|---|---|
| 1 | evidence 文件存在 | 无证据不许推进 |
| 2 | evidence 含 `data_class: real` | 声明 fixture/dry_run/poc/synthetic 一律拒绝 |
| 3 | evidence 含 `authorization_granted: true` | 无授权回执不许推进 |
| 4 | evidence 含回滚记录（`rollback` / `回滚`） | 无回滚不许推进 |
| 5 | 回执台账存在匹配 `auth_id`，`granted_by` 非空且未撤销 | 回执缺失/撤销即拒绝 |
| 6 | 当前 stage ∈ S0–S3 | 只许升级，不许降级或重复推进 |

## 2. 用法

```bash
# 预检（推荐先跑）
python3 scripts/gpcf_promote_vu_stage.py --vu-id PQC-VU-01 \
  --evidence features/active/F-032-*/evidence/pilot-receipt-20261022.json \
  --auth-id AUTH-PG-PQC-REAL-PILOT-20261022 --dry-run

# 通过后正式写入（写 runtime/vu-ledger.yaml：stage=S4, promoted_at, promotion_basis, inferred=false）
python3 scripts/gpcf_promote_vu_stage.py --vu-id PQC-VU-01 \
  --evidence ... --auth-id AUTH-PG-PQC-REAL-PILOT-20261022
```

## 3. 实测行为（阴性用例）

用 PQC 执行手册（非真实证据）预检 → 正确拒绝：

```json
{"status": "fail", "problems": ["evidence 缺少 authorization_granted: true"]}
```

## 4. 边界

- 工具不放宽任何纪律：它只是把纪律变成机器校验；
- 推进 S4 后仍**不得**声明 accepted/integrated/production_ready/customer_accepted；
- `C_real` 会因 S4 变化而上升，这是唯一被允许的上升路径（需真实单据 + 回执 + 回滚）。
