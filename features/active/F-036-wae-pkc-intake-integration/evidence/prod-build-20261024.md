---
doc_id: GPCF-DOC-F036-PROD-BUILD-20261024
title: F-036 WAE 生产构建验证（含 embed URL）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/prod-build-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/prod-build-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-036 WAE 生产构建验证

## 命令

```bash
cd GlobalCloud WAE
VITE_PKC_EMBED_URL='http://127.0.0.1:5174/' pnpm build
```

## 结果

- build exit 0（vite 2.06s）。
- 产物 `apps/wame/dist/assets/PkcIntakePage-*.js`：
  - 含 `127.0.0.1:5174`（embed URL 已注入）
  - 含 `allow-scripts allow-forms allow-same-origin`（sandbox 修复进入生产包）
- 仅验证构建产物；未部署、未验证 CSP/SSO/403。

## 非声明

- 不声明生产可用；不声明 F-036 可关闭。
