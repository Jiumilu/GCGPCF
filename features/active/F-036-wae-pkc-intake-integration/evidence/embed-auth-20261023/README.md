---
doc_id: GPCF-DOC-F036-embed-auth-20261023
title: F-036 嵌入证据
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-23
---

# F-036 登录态受控嵌入证据（2026-10-23）

- 环境：WAE dev :4301（隔离临时 IdP，system-admin bootstrap）+ PKC dev :5174 + `VITE_PKC_EMBED_URL`。
- 前置修复：WAE d9d9ee9（sandbox 加 allow-same-origin）、3247e53（去重复 aria-label）。
- 结果：Playwright 1 passed（26s）
  - 登录 system-admin → 进入 app shell → pkc-intake
  - 点击启用后 iframe src=http://127.0.0.1:5174/，iframe 内文本含 `GlobalCloud PKC`
  - 截图 `screens/embed-pkc-auth.png`
- 限制：dev 隔离 IdP；生产构建/CSP/SSO/403 仍未验证。
- 复现：`./run-embed-review.sh`（需要 WAE 依赖与 Chrome；临时 IdP/口令运行后删除，不写入证据）。
