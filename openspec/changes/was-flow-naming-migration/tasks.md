---
doc_id: GPCF-DOC-1DFD8B740C
title: Tasks — was-flow-naming-migration
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-flow-naming-migration/tasks.md
source_path: openspec/changes/was-flow-naming-migration/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# Tasks — was-flow-naming-migration

## 1. 迁移表与映射

- [x] 1.1 建立《WAS-V1.2 术语迁移表》（WAS:docs/WAS-V1.2术语迁移表.md，v1.0）
- [x] 1.2 映射完备性核对（旧 8 名全部有去向；新 8 名一对一/新增标注）

## 2. 基线切换

- [x] 2.1 `was-flows.yaml`：8 旧键 → V1.2 名（含 Value/Credit 新增、spacetime 移除）
- [x] 2.2 `was_validation_lib.py`：`FLOWS`＝V1.2＋`DEPRECATED_FLOWS`／`ACCEPTED_FLOWS`
- [x] 2.3 schemas×6：flow enum 双列（V1.2＋旧名兼容）；pilot-scope const 放宽
- [x] 2.4 examples×4：数据值切换（S11 归位 LogisticsFlow；requiredFlows 补齐 V1.2 全 8）
- [x] 2.5 引用件更新（引用键规范；主方案迁移执行记录＋§19 表）
- [x] 2.6 校验器精准化（gfis profile：核心 6 流断言）

## 3. 验证

- [x] 3.1 `validate_all` 复跑 13/13 PASS
- [x] 3.2 `kds_bundle_pipeline --check-only` 契约校验 PASS
- [x] 3.3 WAS 仓旧名残留复扫（100% 兼容/定义/说明类）

## 4. 治理

- [x] 4.1 GPCF 侧 change＋F-023＋evidence 建立
- [x] 4.2 document_control 登记与镜像
- [x] 4.3 两仓（WAS/GPCF）提交推送
- [ ] 4.4 存量引用后续批次（GPCF fixtures／KDS WAME 文档）——留后续
- [ ] 4.5 兼容窗口关闭（另行版本发布时）——留后续
