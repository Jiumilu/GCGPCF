# Proposal: gbrain-portal-v1

## Summary
在 Mac mini 部署 GCBrain 知识门户 V1（Python FastAPI + 纯 HTML/JS），端口 19828，替代 LLM Wiki。

## Motivation
- LLM Wiki 已判定为僵尸服务（无人查询，内容被 GBrain 全面覆盖）
- GBrain 有完整的 pgvector 检索引擎，但无对外 Web 界面
- 需要一套轻量门户，复用现有 ECS 隧道（19828）

## Scope
- FastAPI 后端：5 个 API 端点（search/query/render/tree/stats）
- 单文件 HTML/JS 前端：搜索 + 文件树 + 页面渲染
- 部署到 Mac mini，Python 运行，不依赖 Docker

## Non-Scope
- 多租户权限（Phase 3）
- 后台管理控制台（Phase 2）
- 用户认证
- 域名/HTTPS 配置

## Risk Assessment
| Risk | Level | Mitigation |
|------|-------|------------|
| pgvector 连接失败 | Low | 已验证容器运行中 |
| GBrain 嵌入未完成 | Medium | 语义搜索暂时不可用，关键词搜索不受影响 |
| 端口冲突 | Low | 19828 当前为 LLM Wiki 占用，部署时先停 LLM Wiki |
| 磁盘空间 | Low | 43GB 可用 |

## Change Boundary
- 写入：Mac mini /Users/lujunxiang/gbrain-portal/（新建）
- 只读：pgvector DB、SPACE_REGISTRY.yaml、GBrain CLI
- 不影响：GBrain 仓库、现有 Docker 容器、Hermes 服务
