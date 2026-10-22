---
doc_id: GPCF-DOC-E011AE8A70
title: P12 · PQC 首条真实业务链试点 · 授权申请包（待老卢签发）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p12-pqc-real-pilot-authorization-request-20261022.md
source_path: docs/reports/p12-pqc-real-pilot-authorization-request-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P12 · PQC 首条真实业务链试点 · 授权申请包（待老卢签发）

- 日期：2026-10-22｜依据：Q4 裁定「首条真实业务试点 = PQC」（模型 96.7%）
- 状态：**申请中**。本文件不构成授权已发生；`authorization_granted=false`、`action_executed=false`
- 纪律：不得用 E2E 联调客户/合成数据提升 `C_real`

## 1. 为什么是 PQC（实测依据）

| 维度 | 实测 | 结论 |
|---|---|---|
| 全栈可运行 | `:8100/api/health` 200、`:3000` 200、鉴权 401 生效 | 具备试点宿主 |
| 业务闭环 | 二期报价 + 三级审批已跑通；标准参数 2026-10-09 已获准用于对外报价 | 具备真实业务口径 |
| 测试证据 | 后端 661 passed、对外接口 `/ext/v1` 150 tests | 工程基线可支撑 |
| 公共面验证 | 公网 P2/P3 2026-10-21 8/8 PASS（但客户为「PVAAI 联调测试客户(E2E)」= 合成） | 需换真实客户 |
| 已知缺口 | F-032 仍 plan/0 pending 与仓内 2026-10-21 证据账实不符 | 试点前必须回填 |

## 2. 申请授权的具体动作（逐项可勾）

| # | 动作 | 数据/影响 | 回滚 |
|---|---|---|---|
| A1 | 接入**真实客户一单**报价数据（脱敏后入库） | 真实业务单据，非合成 | 单据级删除 + 报价记录回滚 |
| A2 | 以真实单据完成「资料解析→定额匹配→测算→偏差分解→三级审批」全链 | 运行时写库 | 逐表回滚脚本 + 快照 |
| A3 | 出具真实业务回执（含测算版本、价格快照 provenance、审批链） | 证据文件 | 无副作用 |
| A4 | **生产环境发布**（staging 先行，生产单独授权） | 生产服务 | release runbook + 回滚演练后生效 |
| A5 | 对外报价输出（含让价） | **资金相关红线** | 需单独确认每一单让价 |

## 3. 申请边界（明确不做什么）

- 不做客户合同承诺、不对外承诺交期与价格（对外承诺属红线，另行确认）；
- 不采集真实客户个人信息以外的最小必要字段；不把真实单据留档到公共仓；
- 不声明 `accepted / integrated / production_ready / customer_accepted`；
- A4 生产发布与 A5 对外报价**不包含在本申请**，需另行逐项授权。

## 4. 建议授权范围（最小可用）

```
AUTH-PG-PQC-REAL-PILOT-20261022
scope: pqc_first_real_customer_pilot
actions_allowed: read, intake_real_customer_order_deidentified, run_quote_chain, write_evidence, write_staging_deploy
actions_forbidden: production_deploy, external_quotation_commitment, price_concession, customer_data_export,
                   commit_real_customer_docs_to_repo, status_promotion
expires_at: 2027-01-20T23:59:59+08:00
```

## 5. 验收判据（试点完成 = 全部满足）

1. 真实客户一单走完全链，产出回执文件（含 auth_id）；
2. 对应 VU 记 S4（**唯一允许**由真实业务推 C_real 的路径）；
3. 复核人签认（报价复核 + 审批链留痕）；
4. 回滚演练记录（真实单据可撤回）；
5. `C_real` 由 0.00% → 非零，且证据链可回读。

## 6. 我先做的准备（本文件外）

- PQC 仓现状核对（`main@4ba5c89`，8 项脏，属规范化未提交）；
- F-032 账实回填清单（GPCF 侧）；
- 回执模板与回滚脚本清单。

## 7. 需要老卢决策的三点（问答提交）

1. 是否批准 `AUTH-PG-PQC-REAL-PILOT-20261022`（上述最小范围）？
2. 真实客户由谁提供/指定（哪家、哪一单、由谁对接）？
3. A4 生产发布与 A5 对外报价是否本轮一并授权，还是试点完成后另批？
