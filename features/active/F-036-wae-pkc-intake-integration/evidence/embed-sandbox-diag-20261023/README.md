---
doc_id: GPCF-DOC-F036-embed-sandbox-diag-20261023
title: F-036 嵌入证据
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-23
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
