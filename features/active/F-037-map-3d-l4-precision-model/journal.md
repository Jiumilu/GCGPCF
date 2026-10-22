---
doc_id: GPCF-DOC-2587592C
title: F-037 map-3d-l4-precision-model
project: GPCF
related_projects: [SpaceAI, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-037-map-3d-l4-precision-model/journal.md
source_path: features/active/F-037-map-3d-l4-precision-model/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-037 map-3d-l4-precision-model

## 账实说明（2026-10-22 补建）

- 本 Feature 为**治理账实补齐时追溯建立**：L4 精模工作 2026-10-22 已完成并本地提交 6 个提交，
  但当时没有走 GPCF Feature 入口（PMC 侧有 GC-335 登记），形成「工作已做、中央 Feature 无账」的缺口。
- 本次补建只做**记账与证据归位**，不重做工作、不改产品代码、不提升任何验收状态。
- 真实 L4 资产仍未接入，Feature 保持 active。

## LOOP 日志

### Iteration 0（追溯建账）

1. 这轮做什么？
   - 追溯建立 Feature Workspace，把已完成的 L4 精模工作纳入中央账。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - 发现账实缺口：工作已提交但无 Feature；OpenSpec 也未建变更（见 Iteration 1 第 4 问）。
5. 是否可以提交？
   - 否，Evidence Gate 待 Iteration 1 补齐。

### Iteration 1（2026-10-22 证据归位）

1. 这轮做什么？
   - 把 6 个已提交的 L4 精模提交对应到本 Feature，补齐证据并复测当前 HEAD。
2. 改了什么？
   - 提交链（主项目 `../GlobalCloud SpaceAI Platform`，均本地提交未 push）：
     - `3880c18` feat(map-3d): 三维地图 L4 精模管线与白盒切换（占位资产打通）
     - `577c15b` feat(l4): 资产接入工具链 + 采购需求包（校验/导入/回滚）
     - `30cefd2` test(l4): SIMULATED 供应商资产全流程演练 + 证据
     - `d6c83b1` feat(l4): 一键验收引擎 + CI 门禁（清单/加载/切换/回落/贴地/FPS）
     - `f42aac0` ci(l4): L4 门禁工作流（单元/工具链/验收）+ 临时目录校验
     - `65738fc` docs(l4): 自采执行方案 + 工厂试点包（暂停执行）
   - 本 Feature 补齐 feature.yaml 的 scope / acceptance / verification、evidence 五项与 summary。
3. 怎么验证？
   - L4 相关：`npx vitest run plugins/map-3d/tests` → 3 文件 53 例通过（modelPrecision 20 / acceptance-lib 14 / tools 19）。
   - 全仓：`npx vitest run` → 135 文件 / 1242 例通过（2026-10-22 19:04，26.44s）。
   - 类型：`pnpm typecheck` → 0 错误。
   - 验收链路：`harness/l4-acceptance/smoke-sim/report.md`、`smoke-demo/report.md` 均 PASS（0 fail；60 / 56 FPS）。
   - 接口：`/healthz`、`/RestFul/Rebuild/Tileset` 实取 200（Tileset 返回 2 条资产，其中占位 1 条 published）。
   - e2e：`e2e/panorama-l4.spec.ts` 3 条（默认加载 / 切换 / 回落）。
4. 发现什么问题？
   - **真实 L4 资产仍缺**：演练与验收资产为 placeholder / SIMULATED，不能作为几何精度验收依据；已写入 blockers 与 summary 诚实边界。
   - **OpenSpec 变更缺失**：L4 工作未建 `openspec/changes/spaceai-*` 变更，登记为治理欠账，需老卢决定补建或并入后续变更（本轮不擅自补建）。
   - 采购 / 自采文档已归档但暂停执行，不算交付达成。
5. 是否可以提交？
   - 证据齐备可提交（治理产物独立提交）；Feature 保持 active，项目状态保持 partial，不提升 accepted / integrated / production_ready / customer_accepted。


## 治理补记（2026-10-22）

- 本 Feature 的 OpenSpec 变更账已补建：`openspec/changes/spaceai-l4-precision-model/`（proposal / design / tasks / specs / README / `.openspec.yaml`），
  状态 **implemented**，含「三层对齐（契约 → 工具链 → 应用链）」段。
- 校验：`python3 tools/kds-sync/validate_change_alignment_sections.py` → 本变更为 `[OK]`。
- 此前 STATUS 登记的「F-037 / F-038 未建 OpenSpec 变更」欠账**同日关闭**；只补账，不重做工作、不提升验收状态。
