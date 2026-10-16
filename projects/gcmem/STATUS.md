---
doc_id: GPCF-DOC-EAF988D469
title: GCMEM 状态
project: GCMEM
related_projects: [GCMEM]
domain: governance
status: controlled
version: v1.0
owner: GCMEM
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/STATUS.md
source_path: projects/gcmem/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# GCMEM 状态

本文件只记录 GCMEM 的当前项目节奏状态。功能级进度与证据由主设计文档与 KDS 页承载。

## 当前节奏（2026-10-16 立项）

- **状态**：active（世界资产空间，`WAS-GCMEM`）。
- **已完成**：
  - 记忆账本上线：`KDS/_meta/hermes-memory-log.md`（append-only；首条检索命中 0.91）；
  - mem0 退役：插件卸载＋备份留存（`~/.hermes/backups/mem0-plugin-*.tar.gz`）；
  - 服务接口：`~/.hermes/scripts/gcmem.py`（add / search / sync / stats / candidates / import-candidates）；
  - 自动迭代接入：夜间对话挖掘（每晚 23:00）提炼候选并自动入账；
  - 周报指标切换：体系进化周报由「Mem0 记忆数」改为「KDS 记忆条目数」。
- **已完成（2026-10-16 第二批）**：
  - 小G 记忆栈迁移·本机侧：后端 `primary=gcmem`（mem0_local / cognee 退役）＋控制台文案更新＋add / search 全链实测通过；
  - gbrain 升级 0.60.139 → 0.60.257：驻留进程全量重启、writer 门闸通过、回归完成；缺嵌块补嵌处理中。
- **进行中**：小G 记忆栈容器侧随下次部署切换；gbrain 补嵌收尾（3 个大页面待批）。
- **候选待办**：账本自动去重策略迭代。

## 关联

- 设计主文档：`projects/gcmem/MASTER-DESIGN.md`
- 记忆主存：`KDS/_meta/hermes-memory-log.md`｜项目页：`KDS/世界资产/GCMEM.md`
- 上游：GKE-001 知识工程（长期记忆条目为 working 级，随人工确认流转）
