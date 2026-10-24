---
doc_id: GPCF-DOC-F036-EMBED-MESSAGE-CONTRACT-20261024
title: WAE↔PKC 嵌入消息契约（2026-10-24）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/embed-message-contract-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/embed-message-contract-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# WAE↔PKC 嵌入消息契约

## 方向

PKC iframe → WAE 父页（`window.parent.postMessage`）。

## 消息

| type | payload | 语义 |
|---|---|---|
| `pkc:embed-ready` | `{}` | PKC 页面完成初始化，可交互 |
| `pkc:auth-error` | `{ status: 401 \| 403 }` | PKC 侧未登录/无权限 |

## 安全要求

- PKC 发送时指定 `targetOrigin` 为 WAE 页面 origin，不得使用 `*`（契约要求）。
- WAE 校验 `event.source === iframe.contentWindow` 后再处理。
- 不接受凭据/令牌内容，仅状态码。

## WAE 侧实现（已落）

`apps/wame/src/app/apps/PkcIntakePage.tsx`：
- `pkc:embed-ready` → 取消超时提示；
- `pkc:auth-error 401/403` → 显示「需要登录 / 无权限」可读提示；
- 8s 超时提示保留为兜底。

## PKC 侧（待属主实现）

PKC 需在 401/403 时 `postMessage` 上述消息；未实现前 WAE 仍以超时启发式兜底。

## 非声明

- 不声明 PKC 已实现；不声明 SSO 正式接入；不声明 F-036 可关闭。
