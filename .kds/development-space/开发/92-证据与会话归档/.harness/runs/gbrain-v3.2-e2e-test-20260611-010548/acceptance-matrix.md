---
doc_id: GPCF-DOC-CAC95B5694
title: acceptance-matrix
project: WAES
related_projects: [WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-e2e-test-20260611-010548/acceptance-matrix.md
source_path: .harness/runs/gbrain-v3.2-e2e-test-20260611-010548/acceptance-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

| 标签 | API | 实测 | 前台按钮 |
|---|---|---|---|
| 搜索 | /api/v1/search | ✓ 200 | ✓ |
| 问答 | /api/v2/ask/stats | ✓ 200 | ✓ |
| 图谱 | /api/v2/graph/* | ✓ 200 | ✓ |
| 连接器 | /api/v2/connectors/types | ✓ 200 | ✓ |
| 协作 | /api/v2/comments | ✓ 200 | ✓ |
| 协作 | /api/v2/proposals | ✓ 401(需登录) | ✓(优雅提示) |
| 协作 | /api/v2/subscriptions | ✓ 200 | ✓ |
