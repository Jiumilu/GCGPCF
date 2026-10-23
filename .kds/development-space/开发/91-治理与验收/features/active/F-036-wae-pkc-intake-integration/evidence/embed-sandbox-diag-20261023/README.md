---
doc_id: GPCF-DOC-F036-embed-sandbox-diag-20261023
title: F-036 嵌入证据
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/embed-sandbox-diag-20261023/README.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/embed-sandbox-diag-20261023/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# F-036 嵌入白块诊断（2026-10-23）

- 现象：PKC 页面在 `sandbox="allow-scripts allow-forms"` iframe 中空白；去掉 sandbox 正常。
- 证据：`sandbox-no-same-origin-blank.png`（4.6KB 空白）vs `no-sandbox-pkc-content.png`（37KB 含内容）。
- 原因：WAE commit `db403a7` 将 sandbox 收紧为不含 `allow-same-origin`；PKC 前端依赖同源存储，opaque origin 下启动失败。
- 影响：F-036 登录态嵌入空白；此前 dev bypass 证据（Round 71）在收紧前采集，已不代表 HEAD。
- 建议：跨源嵌入保留 `allow-same-origin`（PKC 仍为独立 origin），或在 PKC 侧去掉存储依赖；需 WAE/PKC 属主决策。

## 处置（2026-10-23）

- 决策模型：记录并交属主 72.5%；本轮不改 WAE/PKC 代码。
- 属主动作：
  1. WAE 属主评审 `sandbox` 是否需 `allow-same-origin`（跨源 iframe 仍为独立 origin，风险可控）；
  2. 或 PKC 属主移除前端对同源存储的启动依赖；
  3. 修复后重跑 F-036 登录态嵌入测试，替换 Round 71 的旧证据。
- 复现：启动 PKC :5174 后打开 `iframe-sandbox.html` / `iframe-nosandbox.html`。

## 修复验证（2026-10-23 19:40）

- 在相同 PKC :5174 下，`sandbox="allow-scripts allow-forms allow-same-origin"`：
  - 截图 `sandbox-with-same-origin-content.png` 37KB，PKC 内容正常渲染。
- 对比：无 `allow-same-origin` 4.6KB 空白。
- 结论：加回 `allow-same-origin` 可修复；跨源 iframe 仍为独立 origin，但需 WAE 安全评审确认。

## 生产构建产物验证（2026-10-23 22:40）

- `pnpm build`（PKC）→ dist 生成，build exit 0。
- `python3 -m http.server` 服务 dist，iframe 对照：
  - `sandbox="allow-scripts allow-forms"`：空白（4.6KB）
  - `sandbox` + `allow-same-origin`：正常渲染（37.7KB）
- 证据：`dist-sandbox-no-same-origin-blank.png`、`dist-sandbox-allow-same-origin-content.png`。
- 结论：生产构建产物同样需要 `allow-same-origin`；WAE 修复方向正确。
- 仍非生产部署验证（无 CSP/SSO/403）。
