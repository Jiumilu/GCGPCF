---
doc_id: GPCF-PROJECT-PLANE-DESIGN-20261018
title: GlobalCloud Project Plane 与 GPCF 对接设计
project: GPCF
related_projects: [GPCF, Project]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/project-plane-gpcf-integration/design.md
source_path: openspec/changes/project-plane-gpcf-integration/design.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

## Context

GPCF 的 `runtime/queue.json`、Feature 工作区和 Evidence Gate 是交付状态事实源。Plane 社区版负责团队任务协作。用户选择先对接 GPCF；F-028 记录本次实现与验证。

## Goals / Non-Goals

**Goals:** 独立项目可追溯 Plane 上游版本和许可证；本地适配器从 GPCF 读取 Feature 及证据状态，生成可核验预览，并在显式配置的开发实例中按稳定外部 ID 幂等同步到 Plane 工作项。

**Non-Goals:** 不从 Plane 回写 GPCF；不自动提升 `accepted`、`integrated`、`production_ready`、`customer_accepted`；不复制证据正文到 Plane；不创建 KDS 或 MMC 生产配置。

## Decisions

1. 项目仓以官方 Plane 社区版源码为基线，保留原有许可证和 Git 上游；GlobalCloud 定制放在独立集成目录，降低上游合并冲突。相较直接改动 Plane 核心模型，首期适配器更容易回滚和验证。
2. GPCF `runtime/queue.json` 提供 Feature ID、项目、状态及工作区相对路径；适配器只读取对应工作区的受限证据状态，不读取或上传证据正文。`external_source=gpcf`、`external_id=F-xxx` 用于 Plane 工作项幂等关联。
3. 默认执行为预览；实际写入 Plane API 要明确指定目标实例与项目并启用写入开关，密钥只从进程环境读取。开发实例写入不改变 GPCF 状态。生产或共享实例写入另需人工授权。
4. GPCF 中央登记、项目级总体方案与实施方案继承项目群双主控。F-028 `journal.md`、`evidence/` 和 Harness 记录实施结果；文档控制工具维护本地 KDS 镜像，不宣称 API 同步。

## Risks / Trade-offs

- Plane 社区版功能边界与 API 版本可能变化 → 固定上游提交，针对所用 API 做本地验证。
- AGPL-3.0 及仓内个别文件许可声明需要复核 → 保留原版权与许可证，发布或分发前做许可证审查。
- Plane 工作项被人工编辑后与投影冲突 → 首期只更新受控的标题和来源摘要，不覆盖指派、Plane 工作流等人工字段。
- GPCF 证据不足或门禁为 partial/rework → 如实显示原状态，禁止推断为验收通过。

## Migration Plan

先建立本地项目和只读预览；再用本地测试实例验证幂等同步。回滚时停用适配器并删除本次投影工作项，GPCF 原始队列和证据不变。远端发布与生产接入不在本轮范围。

## Open Questions

正式 Plane 服务地址、工作区及项目 ID 尚未确定；本轮不写入共享实例。
