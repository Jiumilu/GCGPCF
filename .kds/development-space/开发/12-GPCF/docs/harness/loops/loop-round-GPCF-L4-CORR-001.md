---
doc_id: GPCF-DOC-F03D128E75
title: GPCF-L4-CORR-001 Loop Self Correction
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-CORR-001.md
source_path: docs/harness/loops/loop-round-GPCF-L4-CORR-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-CORR-001 Loop Self Correction

## Trigger

用户指出两个关键事实缺口：

1. GFIS 被错误地以 GFIS Demo 为开发和证据主体；正确主体应为 GFIS 运行层。
2. 整个 SOP E2E 测试大师路径失败，不能继续把 L4 项目群最小闭环计为 100/100。

本轮不修改 GFIS 脏工作区，只在 GPCF 总控仓建立事实纠偏、降级和机器门禁。

## Self Finding

| 项 | 发现 |
|---|---|
| GFIS 正确主体 | GFIS 运行层是工厂生产、质量、仓储、设备、安全和经营台账的运行主体 |
| GFIS Demo 边界 | 只能用于展示、培训、追溯说明和前端回归 |
| 错误证据 | `GPCF-L4-008` 将 `gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json` 计入 GFIS 工厂运行事实 |
| E2E 事实 | GFIS `test-results/.last-run.json` 为 `status=failed`，包含 8 个 failed tests |
| 影响 | `GFIS-L4-008` 不能作为 GFIS 运行层 L4 完成证据；`GPCF-L4-012` 100/100 和 L4 closed 结论失效 |

## Correction

| 项 | 新判定 |
|---|---|
| GFIS-L4-008 | `repair_required`，Demo fixture 可保留为展示/前端回归证据，但不能计为运行层 SOP/E2E/验收证据 |
| GPCF-L4-012 | `invalidated_by_self_correction`，不能继续表述为 L4 closed |
| 项目群评分 | 从 `100/100` 降为 `78/100`，状态为 `L4 repair required` |
| 下一轮 | `GFIS-runtime-repair`：以 GFIS 运行层 DocType、工作流、权限、报表、附件和运行态 API 重建证据 |

## Machine Gate

新增：

```bash
python3 tools/kds-sync/validate_loop_self_correction_gate.py
```

该门禁检查：

- GPCF/GFIS evidence 是否仍将 `gcfis_demo` 作为运行层证据。
- GFIS 是否声明运行层为 SOP/E2E/UAT/业务验收主体。
- GFIS Playwright last-run 是否失败。
- GFIS 仓是否 dirty，从而限制自动修复范围。

## Loop Engineering Requirement

Loop 后续必须具备自我发现和自我纠偏能力：

- 发现 evidence 与真实系统主体冲突时，必须自动降级，不得继续维持完成态。
- 发现 E2E failed 时，必须进入 repair，不得用局部 validator 或 Demo E2E 替代 SOP E2E。
- 发现用户指出的事实比文档更新时，以事实为准修正文档和机器门禁。
- 批量文档、模板、fixture 或 mock 不能替代运行层闭环。

## Verification Plan

| Command | Expected |
|---|---|
| `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | blocked；project_group_score=78；next=GFIS-runtime-repair |
| `python3 tools/kds-sync/validate_l4_minimum_closed_loop.py` | repair；project_group_score=78 |
| `python3 tools/kds-sync/check_document_pollution.py` | pass |
| `python3 tools/kds-sync/loop_document_gate.py` | pass |
| `git diff --check -- .` | pass |

## Round Accounting

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 3 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | hard_stop |
| stop_evidence | GFIS Demo 主体错位和 SOP E2E failed 均属于真实系统闭环阻断 |

## Next Input

下一轮应优先进入 GFIS 真实项目仓修复，但必须保护 GFIS 当前 dirty 工作区：先读取并确认已有用户改动，再以 GFIS 运行层为主体补齐运行态 evidence、SOP E2E 修复计划和项目级 validator。
