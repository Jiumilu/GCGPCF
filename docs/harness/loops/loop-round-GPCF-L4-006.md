---
doc_id: GPCF-DOC-18774733CF
title: GPCF-L4-006 PVAOS Organization Partner Permission Intake
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-006.md
source_path: docs/harness/loops/loop-round-GPCF-L4-006.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-006 PVAOS Organization Partner Permission Intake

## Round Output

| 字段 | 值 |
| --- | --- |
| Round ID | GPCF-L4-006 |
| 对应项目轮次 | PVAOS-L4-006 |
| 涉及项目 | PVAOS, GPC, WAES, KDS, GPCF |
| 本轮业务节点 | 组织/伙伴/权限输入基线 |
| 真实项目仓路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS` |
| KDS retrieval | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS/docs/harness/evidence/kds-retrieval-PVAOS-L4-006.json` |
| substantive_round | true for PVAOS real repository fixture/service/test/validator implementation |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## KDS Retrieval Summary

| 字段 | 值 |
| --- | --- |
| retrieval_mode | local_mirror |
| source_documents | `GPCF-DOC-E3822328DF`, `GPCF-DOC-7B5E3B05D7`, `GPCF-DOC-3F160ABA27`, `GPCF-DOC-9096ABA44D` |
| retrieved_objects | Tenant, Organization, Partner, ProjectSpace, PermissionBoundary |
| retrieved_statuses | pvaos_baseline_status, partner_status |
| unresolved_questions | 未调用 live PVAOS/GPC/WAES API；未取得真实客户组织和伙伴接入样本 |

## Verification

| Command | Result |
| --- | --- |
| `python3 scripts/validate_pvaos_l4_org_partner_baseline.py` | pass |
| `python3 scripts/validate_pvaos_l3_harness.py` | pass |
| `npm test -- src/app/tests/tenant/l4OrganizationPartnerBaseline.test.ts` | pass; 1 file / 4 tests |
| `npm run validate:modules` | pass; 50 menu ids, 50 configured modules |
| `npm run typecheck` | pass |
| `git diff --check -- .` | pass |

## L4 100 分评分

| 指标 | 分值 | 得分 | 扣分原因 |
| --- | ---: | ---: | --- |
| 职责边界准确性 | 15 | 15 | PVAOS/GPC/WAES/KDS/GPCF 边界清楚 |
| KDS 关联数据检索质量 | 10 | 10 | 检索清单覆盖组织/伙伴/权限对象、状态、SOP、证据规则和 mock 数据 |
| 真实仓实质变更 | 15 | 15 | PVAOS 真实仓新增 fixture、service、test、validator 和 evidence |
| 测试与验证 | 15 | 15 | validator、Vitest、module validation、typecheck 和 diff check 通过 |
| Evidence 完整性 | 15 | 13 | 扣 2；未调用 live PVAOS/GPC/WAES API，未取得真实客户组织样本 |
| 最小闭环贡献度 | 10 | 9 | 扣 1；完成组织/伙伴/权限入口，但平台订单契约要到 GPC-L4-007 |
| Git 与工作区可审计性 | 10 | 9 | 扣 1；PVAOS 本轮变更尚未提交 |
| 下一轮可执行性 | 10 | 10 | GPC-L4-007 输入明确 |
| 总分 | 100 | 96/100 | L4 Ready |

结论：`counted_as_l4_substantive_round=true`。不得升级 accepted/integrated/complete。

## Project Group Cumulative Score

| 指标 | 当前估分 | 说明 |
| --- | ---: | --- |
| 12 项目覆盖率 | 7/15 | L4-001 至 L4-006 已覆盖 GPCF/MMC/KDS/Brain/PKC/PVAOS |
| P0 主线业务链路贯通度 | 9/20 | 项目初始化与组织/伙伴入口已落 PVAOS dry-run，订单/样品/工厂主线待补 |
| 真实仓代码/配置/测试闭环率 | 11/20 | MMC、KDS、Brain、PKC、PVAOS 有真实仓变更和 validator |
| KDS 检索与知识回指完整度 | 8/10 | L4-002 至 L4-006 均有 kds_retrieval 或受控 evidence 回指 |
| Evidence 与审计完整度 | 8/15 | 项目级 evidence 与总控 evidence 可回指，WAES 审计运行态待补 |
| 跨项目契约一致性 | 7/10 | PVAOS -> GPC / WAES 输入边界已明确 |
| 用户可复现与 L5 准备度 | 5/10 | 本地测试可复现，客户场景仍未贯通 |
| 项目群阶段累计评分 | 55/100 | Return to L3/L3.5；继续 L4 补齐，不进入 L5 |

## Next Input

`GPC-L4-007`：消费 PVAOS 的 Tenant、Organization、Partner、ProjectSpace、PermissionBoundary 输入，建立平台订单、样品申请、客户签样、转量产和 POD 契约 mock/dry-run。
