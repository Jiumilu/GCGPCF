---
doc_id: GPCF-SPACEAI-FLOOD-DESIGN-20261016
title: design
project: GPCF
related_projects: [GPCF, PVAOS, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-was-city-flood-replay/design.md
source_path: openspec/changes/spaceai-was-city-flood-replay/design.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## Context

关联 F-017，当前目录按用户确认的 CWME 项目组织，保留 SpaceAI 注册别名并承载本地应用；现代 Platform 的切片查询会触发共享库建表，不能用作无副作用样例入口。复用 XWAIL 已批准 Schema 和校验器，不复制契约。当前文档门禁 rework_required，项目状态上限 partial。

## Goals / Non-Goals

目标：可复跑、可追溯、具有明确时间语义的合成内涝模型及中文动态图。非目标：真实数据、现场控制、Platform 集成、训练预测模型、生产或业务验收。

## Decisions

- 样例放在 prototypes/was-city-flood/network.json；使用既有切片字段。causality.outcomes 的指标载荷及 demo 展示元数据属于本地场景表达，不冒充 XWAIL 基础字段。
- Python 纯函数 project_at 生成投影；界面只消费生成的 snapshots。避免界面维护第二套状态规则；不依赖数据库和服务。
- 当时已知同时约束发生时间和获知时间；real 以 recordedTime 为获知时间，trusted 取 recordedTime/verifiedTime 较晚值，evolution 取 recordedTime/inferredTime 较晚值；后续审计不能隐藏原始观测，recordedTime 不得早于 occurredTime。演化输出的目标时刻另存，不回填发生时刻。
- 最新修正仅引入符合所选发生时间的后续勘误链，显式标迟到，保留原始节点及 supersededBy；勘误必须保持类型、主体、三世界身份、发生时间、指标和单位。不能把未来新观测或未来验证塞回过去。
- 同 ID 相同输入幂等，同 ID 不同内容拒绝。不同 ID 即使指纹相同也保留为候选重复，不自动删事实。
- 记录和边均需时间过滤；边端点不可见即隐藏。scope 过滤仅为本地纯函数验证，不声明真实用户鉴权。
- 指标过有效期显示未知，同时保留历史记录原值；推演/回执不改写观测或核验。
- 生成的界面展示 8 个时点、两种回放口径与证据详情。样例、算法、UI 分别验证。
- evidence-index、验收矩阵、日志和 patch 进入本次 Harness run；独立审查并以 partial 交接。中央 journal/evidence 仅记录本轮结果，不改变 Feature 状态。

## Risks / Trade-offs

- 合成数据不足以证明物理模型或现场效果 → 每片及视图显式标合成。
- Schema 校验器缺依赖可能跳过 → 测试显式导入 jsonschema/referencing 并确认 Schema 层执行。
- 只支持本样例单线勘误 → 冲突修订拒绝，不设计通用城市平台。
- 浏览器沙箱可能限制截图 → 保留实际证据，不能以静态或模拟 DOM 测试替代浏览器通过。

## Migration Plan

仅新增文件。未来接入 Platform 的 safety-brain 切片入口需独立变更。本轮不发布、不归档；回滚按 proposal 的新增文件边界执行。

## CWME 本地应用承载

- `apps/city-model/index.html` 为完整离线应用，页面标题为 CWME 城市模型；根项目首页链接至应用。
- `build.py` 复用 `prototypes/was-city-flood/replay.py` 校验并生成投影，再通过已安装的可视化导出器打包主题、状态存储与运行时。数据内嵌，不依赖 CDN 或业务服务；浏览成品无需 Python、Codex 或 XWAIL。
- 导出器仅是重建依赖，位置允许通过命令参数指定。保留原型及旧证据原路径，不复制业务状态规则，不修改当前已运行的其他应用。
- 验证直接 file:// 打开、断网、时间/口径/选择、刷新状态、中文和宽窄屏；原19项模型测试回归。当前目录按用户确认的 CWME 身份，不以历史 Windows 方案约束新应用。
