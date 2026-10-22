---
doc_id: GPCF-DOC-0C89CA9D
title: proposal
project: KDS
related_projects: [KDS, GPCF, SpaceAI]
domain: openspec
status: implemented
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/spaceai-l4-precision-model/proposal.md
source_path: openspec/changes/spaceai-l4-precision-model/proposal.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-l4-precision-model · Proposal

> **追溯补建（2026-10-22）**：本变更的实现已于 2026-10-22 完成并本地提交（6 个提交），
> 但当时未建 OpenSpec 变更，形成「工作已做、变更无账」的治理缺口。本文按实际交付补齐，
> 不重做工作、不提升验收状态。

## Why

三维地图（`plugins/map-3d`）当前只有 OSM 白盒体块（L1，8614 栋）+ 程序化立面贴图，
三园区（居住区 50 栋 / 工厂 20 栋 / 商业中心 92 栋）达不到园区级精模要求。
老卢 2026-10-22 指令：**把三维模型升级为 L4 级精模，白盒模型保留、可切换**。

难点不是「买模型」，而是：

1. 真实资产未到位时不能空等——需要先用**明确标注的占位资产**打通全链；
2. 资产必须可停用/回滚，且清单不可用时前端要**自动回落白盒**，不能让地图白屏；
3. 「真实」与「占位」必须在 UI、文档、证据三处标注，避免把占位当真实 L4 汇报；
4. 资产接入要可复现（校验 → 导入 → 启停 → 验收），不能靠手工拷贝。

## What Changes

- 新增资产清单 `data/rebuild/l4/manifest.json`（schema v1）与 BFF 读取端点 `GET /RestFul/Rebuild/Tileset`（清单持久读 + 内存登记表合并）。
- 引擎新增能力：`tilesetAdd` / `tilesetSetAllVisible` / `tilesetSetVisible` / `tilesetGroundClamp`（贴地校准）。
- 新增精度模型与切换：`panorama/modelPrecision.ts`（纯逻辑）+ `useModelPrecision.ts`（加载 / 切换 / 回落 / 降级），图层菜单「模型精度 L4 精模 / 白盒」，localStorage 记忆。
- 新增接入工具链 `tools/l4`：`validate-tileset` / `import-asset` / `switch-asset`（dry-run 与 `--apply`、导入前备份 manifest、失败回滚）。
- 新增一键验收 `tools/l4/acceptance.mjs`（20 项检查：清单 / 加载 / 切换 / 回落 / 贴地 / 画面差异 / FPS / 错误）与 CI 工作流 `.github/workflows/l4-acceptance.yml`。
- 新增文档：`docs/3d/l4-{model,asset-ingest,acceptance,ci,sim-drill,procurement-spec,rfq-package,self-collect-plan,pilot-factory-package,external-data-compliance}.md`。

### New Capabilities

- `spaceai-l4-precision-model`：L4 资产口径（平面/高程 ≤0.3m、3D Tiles 1.1 + glTF、source/license 必填）、清单契约、
  加载/切换/回落行为、贴地规则、接入工具链与验收方法。

### Modified Capabilities

- 无。不改既有 `/RestFul` 端点契约；`/RestFul/Rebuild/Tileset` 为新增端点，已在 `packages/protocol` 登记。
- 不改数据库 schema。

## 三层对齐（契约 → 工具链 → 应用链）

| 层 | 契约 / 资产 | 本仓实现 | 证据 |
|---|---|---|---|
| 契约层 | `data/rebuild/l4/manifest.json`（schema v1：source/real\|placeholder、license、cover、heightOffset）+ `GET /RestFul/Rebuild/Tileset` | `apps/server/src/app.ts`（清单持久读 + 内存登记表合并） | 实取 200，返回 2 条资产（占位 1 条 published） |
| 工具链 | 校验/导入/启停/回滚脚本；一键验收；CI | `tools/l4/{validate-tileset,import-asset,switch-asset,acceptance,acceptance-lib}.mjs`、`tools/db/gen-l4-demo-tiles.mjs`、`.github/workflows/l4-acceptance.yml` | `harness/l4-evidence/toolchain-smoke.md`；`harness/l4-acceptance/{smoke-sim,smoke-demo}/report.json` |
| 应用链 | 精度模式与切换 | `panorama/modelPrecision.ts`、`useModelPrecision.ts`、`PanoramaDeep.vue` 图层菜单、`engine/unisecEngine.ts` | 3 个测试文件 53 例；e2e `panorama-l4.spec.ts` 3 条；PASS ×2（60 / 56 FPS） |

## Impact

- Project：SpaceAI；仓：`GlobalCloud SpaceAI Platform`（独立 Git 仓）。
- 触及：`apps/server`（1 个端点）、`plugins/map-3d`（引擎/视图/纯逻辑）、`tools/l4`、`tools/db`、`docs/3d`、`harness/l4-*`、CI 工作流。
- 不改：数据库 schema、既有端点契约、权限模型；资产二进制不入 git（`data/rebuild/` 已忽略）。
- 非目标：真实 L4 资产采购/自采执行（暂停，待授权）；室内细节（CityGML LOD4 另立范围）；真实三维重建（算力仍为 stub）。
- 回滚：按提交 revert；资产侧 `published=false` 即回退白盒，不阻塞平台。
- authorization：老卢 2026-10-22 指令「升级 L4、白盒保留可切换」，并同意暂停自采。
  confirmation：真实资产验收、业务验收、生产发布**未确认**；项目状态保持 partial。
