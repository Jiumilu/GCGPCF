---
doc_id: GPCF-SLC-RISK-20261018
title: GlobalCloud SLC 风险
project: GPCF
related_projects: [GPCF, SLC]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/slc/RISK.md
source_path: projects/slc/RISK.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# GlobalCloud SLC 风险

| 风险 | 当前控制 |
|---|---|
| 旧 Git 历史含数据库文件与密码哈希 | 新远端只接收当前无历史基线；旧分支仅本地保留 |
| 当前门禁被误读为业务验收 | 保持 `partial/rework`；运行、集成及交付分别取证 |
| 独立应用被误判为 WAE 模块 | WAE 适配和 G1 另行验证 |
| 项目级双方案继承未核验 | 列为后续任务，不提升治理状态 |
