---
doc_id: GPCF-DOC-ECA1059D68
title: GPCF-L4-012 最小闭环收口
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-012.md
source_path: docs/harness/loops/loop-round-GPCF-L4-012.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-012 最小闭环收口

## Correction Notice

2026-06-14 自我纠错：本轮原 `100/100`、`L4 closed` 与 `next=L5-preparation` 结论失效。GFIS 证据错误使用 `gcfis_demo` 作为工厂运行事实主体；正确主体应为 GFIS 运行层。GFIS SOP E2E last-run 当前为 `failed`。后续以 `GPCF-L4-CORR-001`、`docs/harness/evidence/loop_self_correction_assessment.json` 和修订后的 `validate_l4_minimum_closed_loop.py` 为准。

## Round Output

| 字段 | 值 |
| --- | --- |
| Round ID | GPCF-L4-012 |
| 涉及项目 | GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF |
| 本轮业务节点 | 项目群最小闭环收口、评分矩阵与 L5 建议 |
| 真实项目仓路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF` |
| KDS retrieval | 使用 L4-002 至 L4-011 项目级 KDS retrieval 和 `GlobalCloud Loop开发KDS关联数据检索机制.md` |
| Closure matrix | `docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` |
| Validator | `tools/kds-sync/validate_l4_minimum_closed_loop.py` |
| substantive_round | true for GPCF project-group closure, score matrix, validator and KDS mirror update |
| generated_items | 4 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | budget_exhausted |

## Boundary Check

| 项目 | 核对结果 |
| --- | --- |
| GFIS | 工厂事实主账，L4-008 提供只读工厂样本；不承接客户签样/POD |
| GPC | 平台协同主账，L4-007 提供平台订单/签样/转量产/POD 契约；不写 GFIS 工厂事实 |
| PVAOS | 生态入口，L4-006 提供组织/伙伴/权限输入；不承接订单或工厂事实 |
| WAES | 治理中枢，保持 evidence gate 和 audit 裁决权；不成为业务主账 |
| KDS | 知识主存，提供受控口径和回指；不替代当前业务事实 |
| Brain / PKC | 知识呈现和个人工作台；不拥有知识主存或业务事实 |
| MMC | 配置与策略模板中心；不拥有设备/产线/工序事实 |
| XiaoC / XGD / XiaoG | 蚁后/大象/蚂蚁职责清楚，不绕过 WAES、不写业务事实 |
| GPCF | 项目群总控与 evidence 收口，不替代业务项目主账 |

## KDS Retrieval Summary

| 字段 | 值 |
| --- | --- |
| retrieval_mode | local_mirror |
| source_documents | `GPCF-DOC-E3822328DF`, `GPCF-DOC-7B5E3B05D7`, `GPCF-DOC-3F160ABA27`, L4-002..L4-011 project retrieval evidence |
| retrieved_objects | PlatformOrder, SampleRequest, SampleWorkOrder, SampleApproval, ProductionRelease, FactoryOrder, WorkOrder, Shipment, ReadOnlyQueryResult, EvidenceRecord, KnowledgeBacklink |
| retrieved_statuses | ready_for_review, mock_ready, audit_candidate_prepared, blocked_without_required_evidence |
| unresolved_questions | L5 customer/UAT, production endpoint validation, live WAES/GFIS/GPC/PKC APIs and accepted/integrated status all require separate authorization |

## Verification

| Command | Result |
| --- | --- |
| `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | repair; project_group_score=78 next=real-source-record-or-business-input-remediation |
| `python3 tools/kds-sync/check_document_pollution.py` | pass |
| `python3 tools/kds-sync/loop_document_gate.py` | pass |
| `python3 tools/kds-sync/validate_continuous_round_substance.py` | pass; declared=12/30 substantive=12/30 |
| `python3 tools/kds-sync/validate_kds_token.py` | pass; fingerprint only |
| `python3 tools/kds-sync/kds_conflict_guard.py` | pass |
| `git diff --check -- .` | pass |

## L4 100 分评分

| 指标 | 分值 | 得分 | 扣分原因 |
| --- | ---: | ---: | --- |
| 职责边界准确性 | 15 | 15 | 12 项目职责、事实主账、协作输入和禁止越界项均已核对 |
| KDS 关联数据检索质量 | 10 | 10 | 汇总 L4-002 至 L4-011 检索证据，覆盖对象、状态、SOP、证据规则和依赖 |
| 真实仓实质变更 | 15 | 15 | GPCF 真实仓新增 closure matrix、round record、validator 扩展、KDS 镜像和台账更新 |
| 测试与验证 | 15 | 15 | 最小闭环 validator、文档污染、Loop 文档、连续轮次、KDS token/conflict、diff check 均通过 |
| Evidence 完整性 | 15 | 15 | 总控 evidence index、assessment JSON、closure matrix 和 KDS 镜像均完成 |
| 最小闭环贡献度 | 10 | 10 | 完成从项目初始化到 GPCF 收口的 L4 项目群闭环证明 |
| Git 与工作区可审计性 | 10 | 10 | 本地提交可审计，无敏感 Token 明文；不自动推送 |
| 下一轮可执行性 | 10 | 6 | 下一阶段不是 L5 preparation；必须先补真实 source-of-record、运行层 evidence 和 GFIS runtime SOP E2E |
| 总分 | 100 | 78/100 | L4 repair required |

结论：`counted_as_l4_substantive_round=true`。本轮只能作为 L4 项目群收口的受控证据记录；当前结论为 `repair_required`，不得恢复 100/100，不得自动升级 accepted/integrated。

## Project Group Cumulative Score

| 指标 | 当前估分 | 说明 |
| --- | ---: | --- |
| 12 项目覆盖率 | 15/15 | 全部 12 项目覆盖 |
| P0 主线业务链路贯通度 | 20/20 | 可按本地 fixture/dry-run/validator 重构完整主线 |
| 真实仓代码/配置/测试闭环率 | 20/20 | 12 项目均有真实仓证据或 GPCF 总控证据 |
| KDS 检索与知识回指完整度 | 10/10 | 项目级和总控级回指完整 |
| Evidence 与审计完整度 | 15/15 | L4 evidence 完整；WAES 运行态保留为 L5 授权项 |
| 跨项目契约一致性 | 10/10 | 无主账冲突，无越权写入 |
| 用户可复现与 L5 准备度 | 6/10 | 本地命令可复现，但 GFIS 真实业务线与运行层 SOP E2E 仍未闭合 |
| 项目群阶段累计评分 | 78/100 | L4 repair required；L5 not activated |

## Next Input

下一步安全输入：继续推进 GFIS 真实 source-of-record 或 business-input remediation。L5 准备仍被阻塞，直到 customer/UAT 样本、live read API、WAES runtime endpoint verification、monitoring、rollback 与 acceptance criteria 分别获得授权并形成证据。
