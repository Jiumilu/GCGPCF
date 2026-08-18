---
doc_id: GPCF-DOC-F013-GKE001-BRAIN-A10P1T4-DISPATCH-20260812
title: GKE-001 Brain A10P1T4 基线修复派工
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1-tranche4-dispatch-20260812.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gke-001-brain-a10p1-tranche4-dispatch-20260812.md
sync_direction: bidirectional
last_reviewed: 2026-08-12
supersedes: []
superseded_by: []
---

# GKE-001 Brain A10P1T4 基线修复派工

## 当前事实

协调器在 Brain 的冻结 tranche 3 工作树上重新执行类型检查，得到恰好 `13 errors / 8 files`。`HEAD` 与 `origin/main` 均为 `925659b0144a5fb858a78cf32c1d8ddf6967c19b`，ahead/behind 为 `0/0`，暂存项为零，OpsX 锁不存在。既有九文件 dirty 仍全部属于已独立复核通过的 tranche 3，不与本批八文件重叠。

## 派工范围

控制 `GKE-001-COORDINATION-20260812-008-A10P1T4` 只授权 Brain 在八个明确产品/测试文件中清除这 13 个确定性类型错误，并生成新的 run-scoped OpsX 交接包。八文件当前 SHA-256 已写入控制，执行前必须逐一复核。

本批只处理：五个测试中的非法 `enterprise` 空间值、Dashboard 未使用的 lint 严重度状态、ReportsPanel 的可空反馈类型收窄，以及 SettingsPanel 四个未使用派生值。不得改变用户触发写入、授权、读回、本地草案或 KDS 只读边界。

## 验收和边界

- 全量类型检查必须达到零错误，而不是只清除 allowlist 内错误。
- 必须执行八文件对应 focused tests、构建、KDS read-model alignment、既有 OpenSpec strict、CodeGraph sync/status/query、diff-check 和锁释放检查。
- 必须生成 evidence index、acceptance matrix、补丁和 agent result，并交由 F-013 独立复核。
- 禁止网络、浏览器、真实 KDS/MMC/LLM、自动发送提示词、知识或业务事实写入、凭据、提交、推送、重启、部署和状态提升。

该派工与 MMC 十路径 canonical 复核互不重叠，可并行进行。真实 Search → WikiPreview → Chat 仍未授权，状态保持 `active / partial / not_complete`。
