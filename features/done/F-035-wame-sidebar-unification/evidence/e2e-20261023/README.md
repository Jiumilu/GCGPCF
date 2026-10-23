---
doc_id: GPCF-DOC-F035-E2E-20261023
title: F-035 WAME 侧栏 E2E 冒烟（2026-10-23）
project: GPCF
related_projects: [WAME]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-23
---

# F-035 WAME 侧栏 E2E 冒烟

- 环境：WAME architecture-contracts worktree（含 b233438/ea8f321），dev :4320。
- Playwright system Chrome：加载首页 → 等待 8s → 点击「世界资产」→ 截图。
- 结果：`clicked=true`、`pageErrors=[]`、侧栏与主内容正常渲染。
- 证据：sidebar-before.png / sidebar-after.png / assertions.json。
- 限制：本地冒烟，无前后差分基线、无多用户/无障碍实测。
