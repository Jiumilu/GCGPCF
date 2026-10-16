---
doc_id: GPCF-DOC-09F1A04495
title: Proposal — was-flow-naming-migration
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-flow-naming-migration/proposal.md
source_path: openspec/changes/was-flow-naming-migration/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# Proposal — was-flow-naming-migration

## 背景

- 《WAS 总体方案 v1.3.0》§19 明示：八流项要求「建立迁移表和兼容 validator」，且「在迁移完成前，不得把现有 OKF validator 通过解释为 V1.2 已完成」；§21 建议 #1 点名 `docs/WAS-V1.2术语迁移表.md`。
- 现状缺口：`was-flows.yaml` 仍为 OKF P0 旧命名 8 条，而 XWAIL 校验器已用 V1.2 新名——契约层与校验层名不一致；迁移表缺失。
- 执行授权：老卢 2026-10-16「继续／全部继续」。

## 变更

1. 建立《WAS-V1.2 术语迁移表》（WAS 仓 `docs/`）：旧 8 名→新名完整映射（6 更名＋1 并入＋1 重构）、兼容性说明与废弃策略、spacetime 处置、存量引用清单。
2. WAS 仓 okf 基线切换：`was-flows.yaml`（V1.2 8 名＋Value/Credit 新增；spacetime 移除）；`was_validation_lib`（`FLOWS`＝V1.2 名＋`DEPRECATED_FLOWS` 兼容窗口）；schemas×6（enum＝V1.2 名＋旧名兼容）；examples×4（数据值切换；S11 时空→物流归位；requiredFlows 补齐 V1.2 全 8）。
3. 引用件更新：`WAS引用键与数据出口字段规范` 兼容行；主方案迁移执行记录＋§19 表更新。
4. 校验器精准化：gfis profile「stages 覆盖核心 6 流」（Value/Credit 无既有业务实例，不编造）。

## 非目标

- 不改动八维、三层资产、生命周期与状态分离等其它契约（属 P0 其它交付物）。
- 不做 XWAIL 代码改动（其 `ALLOWED_FLOWS` 已是 V1.2 名；联动说明见场景流评估件）。
- 不编造 ValueFlow/CreditFlow 业务实例；不触发任何完成级声明。

## 跨仓影响

- XWAIL：无代码改动需要（存档说明即可）。
- KDS：存量旧名（WAME 文档中文旧名）列后续批次；历史规范件豁免。
- GPCF：`fixtures/was/*.json`（6 件）旧名值留后续批次（兼容枚举已保证可校验）。

## 验证

- `validate_all` 13/13 PASS；`kds_bundle_pipeline --check-only` 契约校验 PASS；WAS 仓旧名残留复扫＝100% 兼容/定义/说明类。
