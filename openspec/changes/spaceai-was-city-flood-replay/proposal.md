---
doc_id: GPCF-SPACEAI-FLOOD-PROPOSAL-20261016
title: proposal
project: KDS
related_projects: [PVAOS, WAME, KDS]
domain: openspec
status: implemented
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-was-city-flood-replay/proposal.md
source_path: openspec/changes/spaceai-was-city-flood-replay/proposal.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## Why

上一轮神经网示意把状态写在界面中，尚不能证明 WAS 切片数据可以重建过去态势。用户“下一步”授权继续本地建模和验证，本轮以合成内涝样例验证真实结构、回放逻辑及数据驱动视图。

## What Changes

- 复用 XWAIL 已获批切片 Schema，新增完整来源标注的内涝样例。
- 增加无业务库依赖的纯回放投影，区分当时已知、最新修正、验证时间、推演时间与过期未知。
- 由投影结果生成可交互切片网络，保留原始记录与证据，验证时间倒退、重复输入、迟到修订和三世界分离。

## Capabilities

### New Capabilities
- `spaceai-city-slice-replay`: 本地合成城市场景的切片投影、回放与中文网络演示。

### Modified Capabilities
无。

## Impact

- Program：GlobalCloud WAS；Project：SpaceAI；复用 Feature F-017，不新建 Feature、不改变中央调度。非 GKE-001 范围。
- 模型实现位于 GlobalCloud SpaceAI/prototypes/was-city-flood/，独立应用位于 apps/city-model/，根 README/AGENTS/Manifest 同步当前 CWME 定位；Harness 证据在本仓 .harness/；中央仅本变更目录及 F-017 的 journal/evidence。
- 只读依赖 GlobalCloud XWAIL/schemas-json、scripts/slice_check.py；不复制或更改基础契约。
- 非目标：真实城市数据、设备控制、共享数据库、KDS 写入、现有 Platform 集成、模型训练、生产发布或业务验收。
- authorization：本地建模、实现、测试、可视化与必要中央追溯；confirmation：业务验收/生产发布未确认。
- 回滚只移除本次新增文件与本次 journal 追加段，保留所有既有未提交内容；不 reset/clean/force push。
- 文档门禁当前 rework_required/missing_metadata=6，项目状态保持 partial；本地样例通过不提升项目验收状态。

## 2026-10-16 应用落地补充

用户要求形成应用放入当前项目，并明确当前目录按 CWME 项目组织。沿用 SpaceAI 注册别名和 F-017；应用落点 `apps/city-model/`。复用现有原型数据/投影，导出无需会话宿主或服务器即可打开的完整本地网页；增加可重复构建入口与根项目入口。根 README、AGENTS 与 Harness Manifest 纠正当前 CWME 定位，历史 Windows 源码保留。此授权不含发布、业务验收或修改 Platform。
