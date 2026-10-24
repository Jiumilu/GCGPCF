---
doc_id: GPCF-DOC-F036-PKC-EMBED-BRIDGE-20261024
title: PKC 嵌入消息桥实现验证（2026-10-24）
project: GPCF
related_projects: [PKC, WAE]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/pkc-embed-bridge-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/pkc-embed-bridge-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
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

## 2026-10-24 补：referrer 为空时的兜底

- WAE iframe 使用 `referrerPolicy="no-referrer"`，PKC 内 `document.referrer` 可能为空；
- PKC `resolveParentOrigin` 增加 `location.ancestorOrigins[0]` 兜底，避免 401/403 消息因无 targetOrigin 而不发送；
- PKC 提交 6daf867e；bridge 4/4、全量 151、build pass。

## 2026-10-24 补：ready 消息

- PKC App 挂载时调用 `notifyParentReady()` → `pkc:embed-ready`；独立打开时 no-op。
- PKC 提交 e74c12ce；151 tests、build pass。
