---
doc_id: GPCF-DOC-F036-FORMAL-REVIEW-20261024
title: F-036 正式接入评审记录（conditional）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/formal-review-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/formal-review-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-036 正式接入评审记录（2026-10-24）

## 1. 评审范围

PKC 在 WAE 的注册与首批接入演练：placement/manifests/menus、PkcIntakePage 受控嵌入、令牌/状态语义、回滚与非声明边界。

## 2. 已核验证据

| 项 | 结果 |
|---|---|
| 登记门禁 | check:apps / gen:apps --check / check:app-assembly 均 pass |
| 六门 | functional / quality / multi_user / task_flow / a11y / evidence = pass |
| dev bypass 嵌入 | 点击后 iframe 加载 PKC Home（embed-20261023） |
| 登录态嵌入 | system-admin + 隔离 IdP，iframe 加载 PKC（Playwright 1 passed，embed-auth-20261023） |
| PKC 生产 dist | sandbox 加 allow-same-origin 正常；无则空白（dist 对照） |
| WAE 修复 | d9d9ee9 / 3247e53 已 push；WAE 1374 tests pass |

## 3. 未满足条件

1. 生产构建部署、CSP/X-Frame-Options、SSO/403 对齐未验证。
2. PKC P4/P5 残留（非真实包消费、部分页面未迁移、C1/C4/C10 既有项）。
3. WAE/PKC 属主对 `allow-same-origin` 安全边界未正式签字。

## 4. 评审结论

- **conditional：不批准关闭**；不得声明 PKC 已接入或生产可用。
- 关闭条件：上述 1–3 满足，并由属主签署。

## 5. 2026-10-24 补充核验

- CSP：`frame-ancestors` 白名单内 iframe 正常、白名单外被阻止（evidence/csp-20261024）。
- SSO/403：设计预案已记录四方案（evidence/sso-403-design-20261024.md）；未实现。
- 结论不变：conditional，不批准关闭；生产部署/SSO/403 与属主签字仍是关闭条件。
