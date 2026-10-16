---
doc_id: GPCF-DOC-EE3E7D649C
title: tasks
project: KDS
related_projects: [WAME, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/was-scenario-flow-extension/tasks.md
source_path: openspec/changes/was-scenario-flow-extension/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

## 1. 治理与准入

- [x] 1.1 建立 Feature F-022 `was-scenario-flow-extension` 并绑定本变更（journal 与证据目录）。
- [x] 1.2 变更文档登记与镜像（`document_control.py` 增量 scope）。
- [x] 1.3 WAS 侧复核：承接方式与六项兼容性声明确认（治理侧）——2026-10-16 老卢『继续』授权推进。

## 2. 登记件

- [x] 2.1 产出《场景流扩展登记草案》（定义单源＋八流/八维关系＋六项声明＋未决项）。
- [x] 2.2 草案复核：WAS/WAME/XWAIL 侧意见；确定正式纳入路径与时点——裁定件 `vocab-extension-admission-was-scenario-flow-20261016.json`（candidate）；纳入时点＝版本发布（U16）。

## 3. 版本化纳入（后续）

- [x] 3.1 WAS 主方案扩展登记记录（候选口径，2026-10-16）。
- [x] 3.1b 主方案流清单并入——已正式纳入（2026-10-16，老卢『正式纳入』；主方案升 v1.3.1，§7 第九流）。
- [x] 3.2 Ontology registry 流类目登记（如适用）——评估：六类目不含 flow，不涉 registry 本体；落位＝was-flows.yaml/XWAIL（见裁定件 rulings）。
- [x] 3.3 XWAIL `flowType` 联动——评估件在案；**档位更新已执行**（2026-10-16：`ALLOWED_FLOWS` 九流、文案泛化、warehouse-basic 正例、议题 v0.11）。
- [x] 3.4 KDS GCWORLD 注记回填——已执行（2026-10-16，V1.0.2 修订记录；承接注记更新为已纳入）。

## 4. 验证与回滚

- [x] 4.1 术语一致性验证：草案定义 == 裁定文本 == GCWORLD V1.0.1（归一化逐字比对）。
- [x] 4.2 文档门禁运行与证据留存。
- [ ] 4.3 回滚预案：登记件 superseded 标记流程（不删除；镜像与登记可逆向同步）。
