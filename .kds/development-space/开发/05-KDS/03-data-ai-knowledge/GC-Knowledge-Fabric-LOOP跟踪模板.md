---
doc_id: GPCF-DOC-2BE90FCE73
title: GC-Knowledge Fabric LOOP跟踪模板
project: KDS
related_projects: [WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-LOOP跟踪模板.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-LOOP跟踪模板.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric LOOP跟踪模板

## 1. 模板用途

本模板用于 GC-Knowledge Fabric 每一轮受控推进。LOOP 记录证据、缺口、候选、确认事项和下一轮动作，不自动把状态升为完成。

## 2. 必填结构

```markdown
# LOOP Round <编号> - <主题>

## 1. 本轮目标

## 2. 本轮输入资料

## 3. 本轮新增知识对象

## 4. 本轮新增缺口

## 5. 本轮新增候选事实

## 6. 本轮新增候选 SOP

## 7. 本轮 WAES 门禁结果

## 8. 本轮人工确认事项

## 9. 本轮委员会事项

## 10. 本轮 RAG 准入变化

## 11. 本轮积分候选变化

## 12. 本轮收益或潜在收益变化

## 13. 本轮风险与阻塞

## 14. 本轮验证命令与结果

## 15. 下一轮动作
```

## 3. 状态边界

- 没有 evidence，不得提升为 accepted。
- 没有人工或委员会确认，不得形成正式事实。
- 没有 WAES 门禁，不得进入写回。
- 没有到账依据，不得进入正式收益。
- 没有脱敏或 metadata-only 处理，不得开放敏感资料。

## 4. 建议验证命令

- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py`
- `git diff --check -- <本轮文件>`
