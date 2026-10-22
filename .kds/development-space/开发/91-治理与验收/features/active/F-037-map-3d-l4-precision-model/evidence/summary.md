---
doc_id: GPCF-DOC-DD1E0F56
title: F-037 map-3d-l4-precision-model 证据摘要
project: spaceai
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-037-map-3d-l4-precision-model/evidence/summary.md
source_path: features/active/F-037-map-3d-l4-precision-model/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: waived
- api: pass
- acceptance_declared: true
- risk: 验收资产为 placeholder / SIMULATED，只证明链路、切换、回落、贴地与性能基线；不代表真实 L4 几何精度，也不代表业务验收。
<!-- GPCF_EVIDENCE_GATE_END -->

## 交付摘要（2026-10-22）

三维地图 L4 精模链路打通（6 个本地提交），真实资产未接入。

| 项 | 结果 |
|---|---|
| 提交 | `3880c18` 管线与白盒切换 → `577c15b` 接入工具链 → `30cefd2` SIMULATED 演练 → `d6c83b1` 一键验收 → `f42aac0` CI 门禁 → `65738fc` 采购/自采文档（暂停） |
| 口径 | `docs/3d/l4-model.md`：L1 白盒（8614 栋）与 L4 精模（三园区 53 栋 / 733 层）定义、3D Tiles 1.1 规范、source=real/placeholder 必填、license 必填、贴地 heightOffset |
| 切换 | 图层菜单「模型精度」；localStorage 记忆；清单不可用/无已发布资产自动回落白盒；占位/真实三处标注 |
| 引擎 | `tilesetAdd` / `tilesetSetAllVisible` / `tilesetSetVisible` / `tilesetGroundClamp` |
| 工具链 | `validate-tileset` / `import-asset` / `switch-asset`（dry-run 与 `--apply`，导入前备份 manifest、失败回滚） |
| 验收 | 一键验收引擎 20 项检查；PASS ×2（smoke-sim 60 FPS / smoke-demo 56 FPS，贴地 0m，画面差异 4.57% / 3.40%，错误 0） |
| 演练 | 162 栋 SIMULATED 资产（1.0MB glb）走完 生成 → 校验 → 导入 → 上线 → 回落 → 回滚，回滚后快照留证 |
| 测试 | L4 相关 3 文件 53 例；全仓 135 文件 / 1242 例；typecheck 0 |
| 接口 | `/healthz` 200（263 端点 / SIMULATED 39 表）；`/RestFul/Rebuild/Tileset` 200（2 条资产，占位 1 条 published） |

## 未完成边界（如实记录）

- **真实 L4 资产未接入**：采购与自采均暂停（2026-10-22 决定），合规外部数据（Google Photorealistic 3D Tiles / Cesium ion）未核验许可与覆盖；几何精度验收（平面/高程 ≤0.3m）无样本可测。
- 采购需求包、自采方案、工厂试点包、RFQ 与比价表已归档（`docs/3d/l4-*.md`、`harness/l4-pilot/`），均为**未执行**文档。
- 重建算力仍为 stub；不做真实三维重建。
- OpenSpec 变更未建（治理欠账，见 journal Iteration 1 第 4 问）。
