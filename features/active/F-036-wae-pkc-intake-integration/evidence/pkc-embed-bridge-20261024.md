---
doc_id: GPCF-DOC-F036-PKC-EMBED-BRIDGE-20261024
title: PKC 嵌入消息桥实现验证（2026-10-24）
project: GPCF
related_projects: [PKC, WAE]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# PKC 嵌入消息桥实现

## 变更

PKC 新增 `src/lib/embedBridge.ts`：
- `notifyParentAuthError(401|403)` → `pkc:auth-error`
- `notifyParentReady()` → `pkc:embed-ready`
- 仅 iframe 内发送；`targetOrigin` 取 `document.referrer` 的 origin；独立打开不发送。
- `cachedFetch` 遇 401/403 时调用上报。

## 验证

- embed bridge + api-client 测试：7 passed
- PKC 全量 tests：pass
- PKC build：exit 0
- WAE 侧监听器（708d02e）可消费该消息并显示登录/权限提示。

## 边界

- 仍未实现正式 SSO；401/403 为运行时上报，不替代 SSO。
- 未部署生产。

## 非声明

- 不声明 SSO 完成；不声明 F-036 可关闭。
