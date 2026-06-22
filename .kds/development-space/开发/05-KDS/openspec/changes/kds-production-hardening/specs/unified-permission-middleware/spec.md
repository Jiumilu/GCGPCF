---
doc_id: GPCF-DOC-D067D700F1
title: 统一权限中间件
project: KDS
related_projects: [PVAOS, WAES, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md
source_path: openspec/changes/kds-production-hardening/specs/unified-permission-middleware/spec.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# 统一权限中间件

## 概述
所有 API 路由（前台与管理端）都统一经过请求身份识别与权限上下文构建。

## 要求
- 每个请求都必须获得一个 UUID `request_id`
- 用户身份通过 session cookie 或 `X-KDS-API-Key` 请求头识别
- 权限上下文必须构建 `tenant_id`、`role`、`scopes`
- 租户与敏感级别 SQL 过滤必须在查询层生效
- 权限判定必须返回结构化解释（`allowed`、`reason`、`matched_rule`、`tenant`、`role`、`sensitivity`）
- 管理路由必须要求认证；前台路由需要具备权限感知能力（过滤，而非直接阻断）

## 验收
- [ ] 所有请求都带有 `X-Request-ID` 响应头
- [ ] 跨租户数据泄露在 SQL 层被阻断
- [ ] 权限拒绝返回带结构化原因的 `403`
- [ ] 前台搜索只返回当前租户适配的结果
