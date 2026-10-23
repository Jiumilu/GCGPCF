---
doc_id: GPCF-DOC-F23FD95D02
title: SpaceAI 路线图
project: GPCF
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/spaceai/ROADMAP.md
source_path: projects/spaceai/ROADMAP.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# SpaceAI 路线图

**项目定位**：`GlobalCloud SpaceAI Platform` 为唯一正本；CWME 本地应用已随 Legacy 归档（2026-10-22）。

## 当前基线（2026-10-22）

- **平台**：BFF `39010`（263 端点）/ 前端 `5273`；全仓 **135 文件 / 1242 例通过**、typecheck 0；库 2.17GB（合成 SIMULATED）。
- **三维地图 L4**：链路就绪（口径 / 清单 / BFF / 引擎 / 切换回落 / 接入工具链 / 一键验收 / CI / 演练），验收 PASS ×2；资产为 placeholder / SIMULATED，**真实 L4 资产未接入**。
- **全景态势**：操作流程规范化执行到 B5e（B0–B5e 共 12 提交，e2e 5/5）；组件 3955 行；B5 剩余五大块、i18n（约 600 行）、人工验收未完成。
- **治理**：F-017 / F-024（iteration 2）/ F-037 / F-038 四个 Feature 在账；本地 0 推送（领先 30 提交）。

## 下一阶段（按优先级）

1. **真实 L4 资产**（唯一硬缺口）：采购执行包 / 合规外部数据核验（Google Photorealistic 3D Tiles、Cesium ion）/ 恢复自采，三选一均需老卢授权；到位后跑 `pnpm l4:acceptance` 并做供应商质检（精度验收）。
2. **全景态势收尾**：B5 剩余五大块外提（卡片列 / 气泡 / 飞翔 / CWME / 控制器）、i18n 约 600 行、人工验收（派单确认与失败保留、CWME 回投 30s 幂等）。
3. **平台欠账**：数据保留策略（D-10）、测试基座小种子库、契约 / 写可靠只读复核、e2e `webServer` 常态化（D-12）。
4. **账实与发布**：推送 30 提交（需授权）、KDS 镜像同步（D-11）、F-037 / F-038 的 OpenSpec 变更补建（需老卢决定）。

## 两条交付线独立

- Platform 线：L4 精模 + 全景态势，证据以主项目 `harness/`、`.harness/runs/` 为准；
- CWME 线：已归档（`_archive/2026-10-22-retired-assets/GlobalCloud SpaceAI/apps/city-model/`），恢复需 `mv` 回根目录并把 `SpaceAI-Legacy` 加回注册表。

## 完成判定

关联 Feature 的验收命令、结果与人工确认边界均记录后，方可提升项目状态；当前仍为 **partial**。
