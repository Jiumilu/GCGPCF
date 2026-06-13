---
doc_id: GPCF-DOC-C81CDC4FDC
title: GPCF-L4-008 GFIS Factory Sample Order Evidence Intake
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-008.md
source_path: docs/harness/loops/loop-round-GPCF-L4-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-008 GFIS Factory Sample Order Evidence Intake

## Round Output

| 字段 | 值 |
| --- | --- |
| Round ID | GPCF-L4-008 |
| 对应项目轮次 | GFIS-L4-008 |
| 涉及项目 | GFIS, GPC, WAES, KDS, XiaoG, GPCF |
| 本轮业务节点 | 配方研发/样品打样/样品检测/工厂订单/工单/质量库存批次/设备/发货只读样本 |
| 真实项目仓路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` |
| KDS retrieval | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/evidence/kds-retrieval-GFIS-L4-008.json` |
| substantive_round | true for GFIS real repository read-only fixture and validator implementation |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## Boundary Check

| 项目 | 核对结果 |
| --- | --- |
| GPC | 生产转移输入来自 GPC-L4-007 ProductionRelease 和 GFIS.factory_order_input_after_release |
| GFIS | 承接 FormulaResearch、SampleWorkOrder、SampleInspection、FactoryOrder、WorkOrder、QualityInventoryBatch、EquipmentSnapshot、Shipment 工厂事实 |
| WAES | WAES gate 只作为 confirmed 输入；最终状态裁决仍归 WAES |
| KDS | 只提供开发口径与候选回指；GFIS 不写 KDS source record |
| XiaoG | 后续只读查询消费者；本轮不执行设备、API 或审计写入 |

## KDS Retrieval Summary

| 字段 | 值 |
| --- | --- |
| retrieval_mode | local_mirror |
| source_documents | `GPCF-DOC-E3822328DF`, `GPCF-DOC-7B5E3B05D7`, `GPCF-DOC-3F160ABA27`, `GPCF-DOC-9096ABA44D`, `GPC-L4-007` |
| retrieved_objects | FormulaResearch, SampleWorkOrder, FactoryOrder, WorkOrder, QualityInventoryBatch, Shipment |
| retrieved_statuses | factory_order_gate, work_order_status, shipment_boundary |
| unresolved_questions | 未调用 live GFIS/Frappe API、未执行 bench migrate、未取得真实配方/样品检测/库存/发货证据 |

## Verification

| Command | Result |
| --- | --- |
| `python3 scripts/validate_gfis_l4_factory_sample_order_readonly.py` | pass; `formula_research=1 sample_work_orders=1 factory_orders=1 work_orders=1 quality_inventory_batches=1 shipments=1` |
| `python3 scripts/validate_gfis_work_order_rules.py` | pass; `demand_cases=5 transition_cases=4` |
| `python3 scripts/validate_gfis_stock_entry_inventory_fields.py` | pass; `fields=5 real_inventory_posting_allowed=False runtime_write_allowed=False` |
| `python3 scripts/validate_gfis_outbound_pod_finance_boundary.py` | pass; `finance_action_gate=L4_blocked fund_fact_auto_confirmed=False` |
| `npm run check:js` | pass |
| `npm run quality:repo` | pass |
| `git diff --check -- .` | pass |

## L4 100 分评分

| 指标 | 分值 | 得分 | 扣分原因 |
| --- | ---: | ---: | --- |
| 职责边界准确性 | 15 | 15 | GFIS/GPC/WAES/KDS/XiaoG/GPCF 边界清楚 |
| KDS 关联数据检索质量 | 10 | 10 | 检索清单覆盖工厂对象、状态、SOP、证据规则、跨项目依赖和 mock 数据 |
| 真实仓实质变更 | 15 | 15 | GFIS 真实仓新增只读 fixture、validator、KDS evidence、round record 并更新 loop-state/evidence-index |
| 测试与验证 | 15 | 15 | 新 validator、既有相关 validator、JS check 和 quality:repo 通过 |
| Evidence 完整性 | 15 | 13 | 扣 2；未调用 live GFIS/Frappe API，未取得真实现场样品/库存/发货证据 |
| 最小闭环贡献度 | 10 | 9 | 扣 1；完成工厂侧本地样本链，但 WAES 审计与 XiaoG 只读查询仍待后续 |
| Git 与工作区可审计性 | 10 | 9 | 扣 1；本轮结果完成时仍需本地提交 |
| 下一轮可执行性 | 10 | 10 | XiaoC-L4-009 / WAES evidence gate follow-up 输入明确 |
| 总分 | 100 | 96/100 | L4 Ready |

结论：`counted_as_l4_substantive_round=true`。不得升级 accepted/integrated/complete。

## Project Group Cumulative Score

| 指标 | 当前估分 | 说明 |
| --- | ---: | --- |
| 12 项目覆盖率 | 9/15 | L4-001 至 L4-008 已覆盖 GPCF/MMC/KDS/Brain/PKC/PVAOS/GPC/GFIS |
| P0 主线业务链路贯通度 | 15/20 | 平台订单、样品申请、客户签样、转量产、工厂样品/工单/质量库存/发货只读样本已串起 |
| 真实仓代码/配置/测试闭环率 | 15/20 | MMC、KDS、Brain、PKC、PVAOS、GPC、GFIS 均有真实仓变更和 validator |
| KDS 检索与知识回指完整度 | 9/10 | L4-002 至 L4-008 均有 kds_retrieval 或受控 evidence 回指 |
| Evidence 与审计完整度 | 10/15 | 项目级 evidence 与总控 evidence 可回指，WAES 审计运行态待补 |
| 跨项目契约一致性 | 9/10 | GPC -> GFIS handoff boundary 已明确，POD/客户签样不归 GFIS |
| 用户可复现与 L5 准备度 | 6/10 | 本地验证可复现，客户真实样本/UAT/WAES 审计仍未贯通 |
| 项目群阶段累计评分 | 73/100 | L4 Repair；继续 L4 补齐，不进入 L5 |

## Next Input

`XiaoC-L4-009`：消费 GPC/GFIS/Brain/KDS/PKC 现有 L4 evidence，建立任务拆解、模型路由和 Agent 编排 dry-run；不得绕过 WAES 授权或直接写业务事实。
