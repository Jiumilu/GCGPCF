---
doc_id: GPCF-DOC-F036-CLOSURE-CHECKLIST-20261024
title: F-036 关闭清单与证据缺口（2026-10-24）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/closure-checklist-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/closure-checklist-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-036 关闭清单

| # | 条件 | 状态 | 证据/缺口 |
|---|---|---|---|
| 1 | WAE PKC 入口可构建 | ✅ | prod-build-20261024（embed URL + allow-same-origin） |
| 2 | 开发态受控嵌入 | ✅ | embed-20261023 |
| 3 | 登录态受控嵌入（隔离 IdP） | ✅ | embed-auth-20261023（Playwright 1 passed） |
| 4 | CSP frame-ancestors allow/block | ✅ | csp-20261024（:4300 allow / :4301 block） |
| 5 | 生产部署 | ❌ | 未部署 |
| 6 | SSO 正式接入 | ❌ | 仅临时/隔离 IdP；sso-403-design 为方案 |
| 7 | 401/403 可读降级 | ⚠️ | WAE 已实现 8s 超时 + postMessage 401/403 契约（sso-403-fallback / embed-message-contract）；PKC 侧未实现 |
| 8 | WAE 属主签字 | ❌ | 待签 |
| 9 | PKC 属主签字 | ❌ | 待签 |
| 10 | 正式评审结论 | ⚠️ | conditional，不批准关闭 |

## 结论

- 开发/构建/嵌入/CSP 侧证据齐备；生产/SSO/403/签字四项未满足。
- 仍 **conditional**，不关闭。

## 非声明

- 不声明生产可用；不声明可关闭。
