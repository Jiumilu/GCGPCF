---
doc_id: GPCF-DOC-B8ADFA9E30
title: GlobalCloud 项目群文档综合治理规范
project: WAES
related_projects: [WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群文档综合治理规范.md
source_path: 02-governance/GlobalCloud项目群文档综合治理规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群文档综合治理规范

日期：2026-06-12
状态：v1.0
适用范围：GlobalCloud 项目群全部 12 个项目

## 1. 目标

本规范用于确保项目群的整个工作都在文档中有体现、受控与更新，并防止文档体系结构漂移、事实失真和旧口径污染。

文档治理不是事后整理，而是 Loop Engineering 的组成部分。

## 2. 治理原则

1. 所有关键工作必须有文档入口。
2. 所有 Markdown 文档必须有受控元数据。
3. 所有文档目录必须有 README。
4. 所有文档必须纳入 KDS `开发` 空间。
5. 过期文档不得静默删除，只能归档、废弃或标记替代关系。
6. 文档不得把设计、配置、控制台可见、镜像同步写成业务完成。
7. 状态升级必须有文档、证据和 KDS 同步记录共同支撑。

## 3. 文档状态

| 状态 | 含义 | 状态上限 |
|---|---|---|
| controlled | 当前有效受控文档 | 可支撑 accepted |
| draft | 草案或待确认内容 | 不支撑 accepted |
| archive | 历史证据或运行记录 | 只支撑追溯 |
| deprecated | 过期文档 | 不支撑当前口径 |
| superseded | 已被替代文档 | 不支撑当前口径 |
| operational_controlled | 工具、技能、运行类文档 | 只支撑工具治理 |

## 4. 文档债务

若某轮工作影响了设计、实现、验证、状态或治理口径，但文档暂未完整更新，必须登记文档债务。

文档债务至少包含：

| 字段 | 含义 |
|---|---|
| reason | 为什么暂未更新 |
| affected_docs | 受影响文档 |
| owner | 责任项目或责任人 |
| due_loop | 必须关闭的 Loop 编号 |
| max_status | 状态上限，默认 partial |

存在未关闭文档债务时，项目状态不得进入 `accepted` 或 `integrated`。

## 5. 控制台账

文档治理入口固定为：

| 台账 | 路径 |
|---|---|
| 文档控制总台账 | `09-status/globalcloud-document-control-register.md` |
| KDS 同步台账 | `09-status/kds-development-space-sync-register.md` |
| 过期与归档台账 | `09-status/document-deprecation-register.md` |
| 文档健康报告 | `09-status/globalcloud-document-health-report.md` |

## 6. 执行方式

每次文档治理应运行：

```bash
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/kds_conflict_guard.py
python3 tools/kds-sync/loop_document_gate.py
```

上述命令的结果必须进入 Loop evidence 或本轮总结。
