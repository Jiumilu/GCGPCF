---
doc_id: GPCF-DOC-173EF82828
title: GPCF-L4-GFIS-REPAIR-021 Loop Engineering Self Discovery Hardening
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-021.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-021.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-021 Loop Engineering Self Discovery Hardening

## 本轮目标

将用户指出的两个关键问题转化为 Loop Engineering 的可检查机制：

1. GFIS SOP 开发主体必须是 `GFIS 运行层`，不能是 `GFIS Demo`。
2. SOP E2E 大师链路失败必须成为硬门禁，不能被 Demo E2E、fixture、dry-run、候选证据或文档叙事覆盖。

## 自我发现结论

| 问题 | Loop 旧风险 | 本轮修复 |
|---|---|---|
| 主体错误 | Demo 被误读为业务主体 | `subject_drift_detected` 纳入自纠文档和完整性 validator |
| E2E failed | 展示层通过可能压过 runtime failed | `gfis_runtime_sop_e2e=repair_required` 继续作为主状态 |
| Demo 替代 | Demo E2E 26 passed 可能被当作 SOP evidence | Demo 只能标记为 `pass_demo_only` |
| KDS 引用误判 | controlled reference 可能被当作真实业务凭证 | 必须区分 controlled reference 与 verified live artifact |
| 完成态污染 | 100/100、closed、accepted、integrated 可能过早恢复 | repair_required 存在时禁止状态升级 |

## 实施内容

| 仓库 | 文件/动作 | 结果 |
|---|---|---|
| GPCF | `02-governance/loop/LOOP_ENGINEERING_SELF_CORRECTION.md` | 新增关键问题重述、Loop Engineering 定义、自我发现触发器和防复发工程门禁 |
| GPCF | `tools/kds-sync/validate_loop_engineering_integrity.py` | 新增 `subject_drift_detected`、`pass_demo_only`、`verified live artifact` 等强制检查 |
| GPCF | `02-governance/loop/LOOP_CONTROL_BOARD.md` | 当前轮次更新为 REPAIR-021；下一步聚焦 POD runtime gate |
| GPCF | `09-status/gpcf-project-status-matrix.md` | 版本更新为 v1.91；GFIS/GPCF 继续 repair_required |
| GPCF | `docs/harness/loop-state.md`、`docs/harness/evidence/evidence-index.md`、`docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` | 回写本轮真实结论和 evidence |

## 验证要求

| 命令 | 期望 |
|---|---|
| `python3 tools/kds-sync/validate_loop_engineering_integrity.py` | pass；同时调用 GFIS runtime validator 并确认 repair_required |
| `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | blocked/repair；不得恢复 100/100 |
| `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | repair；项目群评分保持 79 |
| `python3 tools/kds-sync/check_document_pollution.py` | pass |
| `python3 tools/kds-sync/loop_document_gate.py` | pass |

## 当前结论

```text
GFIS Demo = pass_demo_only
GFIS 运行层 = 唯一 SOP 主体
GFIS runtime SOP E2E = repair_required
Loop Engineering = self-discovery hardening active
project_group_score = 79/100 repair
```

本轮没有完成 GFIS SOP E2E，也没有补齐真实业务输入。它只让 Loop 更难再次沿错误主体继续开发。

## 下一步

下一轮优先建立 GFIS runtime 只读 `proof_of_delivery` gate，拆清：

- GFIS DeliveryNote 发货事实。
- GPC/POD 签收主账。
- WAES evidence confirmation。
- KDS backlink receipt。

## 禁止与边界

- 未使用 GFIS Demo 作为业务主体。
- 未修改 GFIS 业务 API。
- 未执行 `bench migrate`、schema sync、数据库迁移、生产写入、真实外部 API 写入、权限变更、部署、Git push 或 accepted/integrated 状态升级。
- 未把本轮文档治理写成 SOP E2E 完成。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | completed_single_substantive_round |
