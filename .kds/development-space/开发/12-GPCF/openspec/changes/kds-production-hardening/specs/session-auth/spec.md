---
doc_id: GPCF-DOC-18A2F48E80
title: 会话认证
project: GPCF
related_projects: [GPCF, WAES]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/kds-production-hardening/specs/session-auth/spec.md
source_path: openspec/changes/kds-production-hardening/specs/session-auth/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 会话认证

## 概述
将 BasicAuth 替换为服务端会话认证，并为管理路由增加 CSRF 保护。

## 要求
- 管理员通过 `POST /api/v1/admin/login` 提交用户名和密码表单完成登录
- 服务端使用 `itsdangerous` 签名 cookie 创建会话
- CSRF token 通过 `HMAC-SHA256` 与会话绑定生成
- Cookie 需设置 `HttpOnly`、`SameSite=Lax`、`Secure`（仅生产环境）
- 会话过期时间可配置，默认 `24` 小时
- 所有管理路由都必须要求有效会话，否则返回 `401`
- 登出时清理会话 cookie

## 验收
- [ ] 管理员登录后返回会话 cookie
- [ ] 管理路由在无有效会话时返回 `401`
- [ ] CSRF token 能针对正确会话完成校验
- [ ] 过期会话会被拒绝
- [ ] Cookie 属性正确设置（`HttpOnly`、`SameSite`、生产环境下的 `Secure`）
