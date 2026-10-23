---
doc_id: GPCF-DOC-A1B1103B05
title: P14 · PQC 首条真实业务链执行手册（A1–A4 范围内）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p14-pqc-pilot-execution-runbook-20261022.md
source_path: docs/reports/p14-pqc-pilot-execution-runbook-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P14 · PQC 首条真实业务链执行手册（A1–A4 范围内）

- 依据：回执 `AUTH-PG-PQC-REAL-PILOT-20261022`（2026-10-22 22:10 批准 A1–A4）
- 边界：**不含生产发布与对外报价**（A5 未批）；不得用联调测试客户/合成数据推 `C_real`
- 执行方：PQC 属主（GPCF 只做证据回读与状态判定）

## 0. 前置（缺一不可）

| # | 前置 | 判据 |
|---|---|---|
| P1 | 老卢确认的**真实客户一单**（PQC 属主选单 → 老卢确认） | 确认记录（问答或回执附件） |
| P2 | F-032 账实回填完成（现 plan/0 pending 与仓内 2026-10-21 证据不符） | `gpcf_check_evidence.py F-032 --check-only` 无 evidence 类理由 |
| P3 | staging 环境可用 + 回滚脚本就位 | 回滚演练 1 次通过 |
| P4 | 复核人指定（报价复核 + 审批链签认） | 人选记录 |

## 1. 执行步骤（真实单据全链）

| 步 | 动作 | 产出 | 失败处理 |
|---|---|---|---|
| S1 | 真实单据脱敏导入（仅最小必要字段） | 导入回执 + 脱敏对照 | 立即停，不入库残留 |
| S2 | 资料解析 → 定额匹配（人工确认候选） | 候选清单 + 人工确认记录 | 候选不得自动生效 |
| S3 | 确定性测算（Decimal + 版本绑定 + 价格快照 provenance） | 测算结果 + 版本号 | 复算不一致即停 |
| S4 | 偏差分解（量差/消耗差/价差，恒等式校验） | 偏差报告 | 恒等式不成立即停 |
| S5 | 三级审批（含复核人签认） | 审批链记录 | 任一节点驳回即停 |
| S6 | 出具真实业务回执（含 auth_id、版本、快照、审批链） | `evidence/pilot-receipt-<date>.json` | — |
| S7 | staging 部署演练（如 A4 需要） | 部署记录 + 冒烟结果 | 回滚演练流程执行 |

## 2. 改为 S4 的唯一判据（C_real 提升条件）

1. S1–S6 全部完成，回执文件可回读且含 `authorization_granted=true`；
2. 复核人与审批链签认齐；
3. 回滚演练记录在案（真实单据可撤回）；
4. 证据含 `data_class: real`（**不得**为 fixture/dry_run/poc/synthetic）；
5. 由 GPCF 侧将该 VU 的 `stage` 由 S1/S2 改为 S4，并在 `runtime/vu-ledger.yaml` 记录变更依据。

> 上述 5 条同时满足才算 S4；缺一条则保持原 stage，`C_real` 不变。

## 3. 非声明

- 不声明 `accepted / integrated / production_ready / customer_accepted`；
- 不对外报价、不让价（A5 未批，涉资金红线）；
- 真实客户单据不提交进公共仓（脱敏后只留回执与指纹）。
