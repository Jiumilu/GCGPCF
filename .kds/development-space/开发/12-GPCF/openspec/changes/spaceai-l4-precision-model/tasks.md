---
doc_id: GPCF-DOC-E2F62413
title: tasks
project: GPCF
related_projects: [GPCF, SpaceAI]
domain: openspec
status: implemented
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-l4-precision-model/tasks.md
source_path: openspec/changes/spaceai-l4-precision-model/tasks.md
sync_direction: bidirectional
last_reviewed: '2026-10-22'
supersedes: []
superseded_by: []
---

# spaceai-l4-precision-model · Tasks

> 状态口径：`[x]` = 已交付并本地提交（未 push）；`[ ]` = 未做（blocked 或留待下一轮）。
> 追溯补建：本清单按 2026-10-22 实际提交回填，不新增工作。

## 1. 口径与资产规范

- [x] 1.1 `docs/3d/l4-model.md`：L4 定义（平面/高程 ≤0.3m、门窗洞口级、不含室内）、3D Tiles 1.1/glTF/SPLAT 规范、清单 schema、source/license 必填、三园区范围。
- [x] 1.2 明确 L1 白盒与 L4 的边界（8614 栋白盒；三园区 53 栋 / 733 层）。

## 2. 清单与 BFF

- [x] 2.1 `data/rebuild/l4/manifest.json`（schema v1）+ `GET /RestFul/Rebuild/Tileset`（清单持久读 + 内存登记合并）。
- [x] 2.2 资产二进制不入 git（`data/rebuild/` 忽略）。

## 3. 引擎与切换

- [x] 3.1 引擎 `tilesetAdd` / `tilesetSetAllVisible` / `tilesetSetVisible` / `tilesetGroundClamp`。
- [x] 3.2 `panorama/modelPrecision.ts`（154 行）+ `useModelPrecision.ts`（172 行）：加载 / 切换 / 回落 / 降级、localStorage 记忆。
- [x] 3.3 图层菜单「模型精度 L4 精模 / 白盒」；真实/占位三处标注。
- [x] 3.4 清单异常（500）/无已发布资产 → 自动回落白盒，不白屏。

## 4. 接入工具链

- [x] 4.1 `tools/l4/validate-tileset.mjs`（结构/坐标/文件/清单）。
- [x] 4.2 `tools/l4/import-asset.mjs`（dry-run / --apply，导入前备份 manifest）。
- [x] 4.3 `tools/l4/switch-asset.mjs`（启停/发布/回滚）。
- [x] 4.4 `tools/db/gen-l4-demo-tiles.mjs` 生成三园区占位资产；`tools/db/gen-l4-sim-asset.mjs` 生成 SIMULATED 演练资产（162 栋）。

## 5. 一键验收与 CI

- [x] 5.1 `tools/l4/acceptance.mjs` + `acceptance-lib.mjs`（20 项检查、退出码 0/1/2）。
- [x] 5.2 `.github/workflows/l4-acceptance.yml`（单元 / 工具链 / 验收三段，含临时目录校验）。
- [x] 5.3 `docs/3d/l4-acceptance.md`、`l4-ci.md`。

## 6. 演练与证据

- [x] 6.1 SIMULATED 全流程演练（生成 → 校验 → 导入 → 上线 → 回落 → 回滚），证据 `harness/l4-evidence/sim-drill/`。
- [x] 6.2 一键验收 PASS ×2：`harness/l4-acceptance/smoke-sim`（60 FPS）、`smoke-demo`（56 FPS），0 fail。
- [x] 6.3 测试：3 文件 62 例（modelPrecision 20 / acceptance-lib 14 / tools 28）；e2e `panorama-l4` 3 条。

## 7. 采购 / 自采准备（不执行）

- [x] 7.1 `docs/3d/l4-procurement-spec.md`（技术规格与验收规范）。
- [x] 7.2 `docs/3d/l4-rfq-package.md` + `harness/l4-pilot/{rfq-email.md,quote-sheet-template.csv,quote-comparison.csv,pilot-checklist.md}`（RFQ 包，未发送）。
- [x] 7.3 `docs/3d/l4-self-collect-plan.md`、`l4-pilot-factory-package.md`（自采方案与试点包，暂停执行）。
- [x] 7.4 `docs/3d/l4-external-data-compliance.md`（合规外部数据源核验准备，未申请 key）。

## 8. 未完成（blocked / 留待下一轮）

- [ ] 8.1 **真实 L4 资产接入**：采购、自采、合规外部源三路径均未授权（blocker，F-037 记录）。
- [ ] 8.2 几何精度验收（≥20 特征点 ≤0.3m）：需真实资产与供应商质检报告。
- [ ] 8.3 远端 CI 实跑：未 push，工作流只在本地等价跑通。
- [ ] 8.4 真实三维重建（WorldMirror/3DGS）：算力仍为 stub，不在本变更范围。

## 9. 真实资产验收入口（2026-10-23 补，不采购前提）

- [x] 9.1 `docs/3d/l4-vendor-dataset-spec.md`：交付包规格（tileset/metadata/license/crs/cover/qa≥3 控制点）+ 三条来源路径与各自授权点。
- [x] 9.2 `tools/l4/verify-vendor-package.mjs` + `l4-lib.mjs::validateVendorPackage`：验包判定 pass/needs_human/fail；
      SIMULATED 必须显式 `--allow-simulated`；**脚本不判定几何精度达标**（needsHuman 列控制点实测等人工项）。
- [x] 9.3 单测 +9（l4-tools 19→28）：合规真实包→needs_human、缺 license/crs/qa/控制点/覆盖不全→fail、SIMULATED 默认 fail。
- [x] 9.4 DRY-RUN 证据 `harness/l4-acceptance/vendor-dryrun/`（合成包，非真实几何；证明 real 路径判定与「不自动宣称精度」）。
- [ ] 9.5 验收复跑：2026-10-23 被并行会话 pano 重构在途回归阻塞（登录后找不到「全景态势」入口），待其收口后重跑。
