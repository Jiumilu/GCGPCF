---
doc_id: GPCF-DOC-D295269E5B
title: WAS Project Group Ontology Registry Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-project-group-ontology-registry-20260621.md
source_path: docs/harness/evidence/was-project-group-ontology-registry-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS Project Group Ontology Registry Evidence

## 结论

本轮建立项目群级 WAS-Ontology Registry，把 GlobalCloud 项目群数字孪生骨架拆成 6 类受控注册项：对象、关系、事件、证据、状态、接口。

本轮结论为 `pass_with_hold`。Registry 已覆盖完整项目群和绿色供应链关键对象，但当前仍无真实源记录、无 WAES 审查、无 KDS 官方事实、无运行时主键、无 GFIS/KWE 写入，因此不得升级为业务完成。

## 覆盖范围

| 项 | 值 |
|---|---|
| project_group_scope | `14/14` |
| registry_categories | `6/6` |
| object_entries | `10` |
| relationship_entries | `6` |
| event_entries | `7` |
| evidence_entries | `7` |
| state_entries | `7` |
| interface_entries | `6` |
| positive_fixtures | `1` |
| negative_fixtures | `3` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| runtime_write | `false` |
| kds_api_write | `false` |

## 注册类目

| 类目 | 作用 | 边界 |
|---|---|---|
| object | 项目群业务对象与绿色供应链对象骨架 | 不等于真实业务主键 |
| relationship | source-record、KDS、WAES、RAG、Pool、runtime 之间的语义关系 | 不等于自动提升 |
| event | 候选提交、预检拒收、门禁输入、绑定请求、引用准入、写回预检、Pool 检查 | 不等于事件已发生 |
| evidence | 原件、确认、backlink、gate input、loop round、validator、反例拒收 | 不等于 KDS 官方事实 |
| state | candidate、hold、pending、blocked 等状态 | 不等于 accepted/integrated |
| interface | GFIS intake、KDS backlink、WAES gate、RAG reference、GFIS/KWE precheck、11 Pools link | 不等于运行时写入 |

## Future Project Policy

后续新增项目进入 GlobalCloud 项目群时，必须：

- 绑定完整项目群 scope。
- 映射到 object、relationship、event、evidence、state、interface 六类注册项。
- 保持 KDS / WAES / Loop / WAS / RAG / GFIS-KWE 的边界。
- 不绕过 KDS source-of-record、WAES promotion decision 和 Loop evidence closure。

## 执行命令

```bash
python3 tools/kds-sync/validate_was_project_group_ontology_registry.py
```

## 非声明

- Registry 是语义契约索引，不是新增知识库。
- Registry 不替代 KDS source-of-record。
- Registry 不创建 WAES review。
- Registry 不写 GFIS/KWE runtime。
- Registry 不把 RAG 输出提升为正式事实。
- Registry 不标记 accepted、integrated 或 production_ready。
