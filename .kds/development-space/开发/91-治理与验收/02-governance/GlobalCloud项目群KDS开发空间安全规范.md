---
doc_id: GPCF-DOC-AC66DE8415
title: GlobalCloud 项目群 KDS 开发空间安全规范
project: WAES
related_projects: [GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群KDS开发空间安全规范.md
source_path: 02-governance/GlobalCloud项目群KDS开发空间安全规范.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 KDS 开发空间安全规范

日期：2026-06-12
状态：v1.0
适用范围：KDS `开发` 空间、GPCF 文档镜像、文档同步脚本

## 1. 安全目标

KDS `开发` 空间用于承载项目群受控文档主存镜像。当前阶段只允许用户本人通过专用 TOKEN 访问、阅读与编辑。

## 2. 专用 TOKEN

推荐环境变量：

```text
KDS_DEVELOPMENT_SPACE_TOKEN
KDS_TOKEN_OWNER=lujunxiang
KDS_SPACE_NAME=开发
KDS_TOKEN_SCOPE=read,write,edit
```

## 3. 禁止事项

1. 禁止把 TOKEN 明文写入 Git。
2. 禁止把 TOKEN 明文写入 `.kds/`。
3. 禁止把 TOKEN 明文写入同步流水。
4. 禁止在日志、报告、健康检查中输出 TOKEN 明文。
5. 禁止非专用 TOKEN 读取、编辑或同步 KDS `开发` 空间。
6. 禁止自动删除 KDS 文档；过期内容必须走 archive/deprecated/superseded。

## 4. 校验要求

`validate_kds_token.py` 必须检查：

| 检查项 | 通过条件 |
|---|---|
| TOKEN 是否存在 | `KDS_DEVELOPMENT_SPACE_TOKEN` 非空 |
| owner | `KDS_TOKEN_OWNER=lujunxiang` |
| space | `KDS_SPACE_NAME=开发` |
| scope | 包含 read、write、edit |
| 明文泄漏 | 仓库与 `.kds` 不含 TOKEN 明文 |

未通过时，Loop 文档门禁必须返回 `blocked`。

## 5. 破窗机制

默认不启用破窗 TOKEN。未来若需要临时授权，只允许登记 TOKEN 指纹，不允许登记明文。
