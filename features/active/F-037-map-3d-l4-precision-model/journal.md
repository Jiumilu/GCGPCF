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
   - **OpenSpec 变更缺失**：L4 工作未建 `openspec/changes/spaceai-*` 变更，登记为治理欠账，需老卢决定补建或并入后续变更（本轮不擅自补建；**同日 19:27 已由提交 `769b1547f` 补建 `openspec/changes/spaceai-l4-precision-model/`，该欠账已关闭——见 Iteration 2 更正**）。
   - 采购 / 自采文档已归档但暂停执行，不算交付达成。
5. 是否可以提交？
   - 证据齐备可提交（治理产物独立提交）；Feature 保持 active，项目状态保持 partial，不提升 accepted / integrated / production_ready / customer_accepted。


## 治理补记（2026-10-22）

- 本 Feature 的 OpenSpec 变更账已补建：`openspec/changes/spaceai-l4-precision-model/`（proposal / design / tasks / specs / README / `.openspec.yaml`），
  状态 **implemented**，含「三层对齐（契约 → 工具链 → 应用链）」段。
- 校验：`python3 tools/kds-sync/validate_change_alignment_sections.py` → 本变更为 `[OK]`。
- 此前 STATUS 登记的「F-037 / F-038 未建 OpenSpec 变更」欠账**同日关闭**；只补账，不重做工作、不提升验收状态。

### Iteration 2（2026-10-23 上午 · 主线纠偏与真实资产验收入口）

1. 这轮做什么？
   - 纠正主线偏离：会话中段转入契约/写可靠审计与治理旁线约 11 轮，本轮回到 L4 精模主线；
   - 在**不采购/不飞行/不授权外部数据**的前提下，把「真实 L4 资产到位后如何验收入口」固化成可执行规格与脚本；
   - 核实并更正 Iteration 1 的陈旧结论（OpenSpec 欠账已在 2026-10-22 19:27 关闭）。

2. 改了什么？
   - 主项目 `../GlobalCloud SpaceAI Platform`（本地提交，未 push）：
     - `docs/3d/l4-vendor-dataset-spec.md`：交付包规格（tileset/metadata/license/crs/cover/qa≥3 控制点）+ 三来源路径与授权点 + 人工核验清单 + PASS/PARTIAL/FAIL 判据；
     - `tools/l4/verify-vendor-package.mjs`：验包 CLI（pass / needs_human / fail；SIMULATED 须 `--allow-simulated`）；
     - `tools/l4/l4-lib.mjs`：新增纯逻辑 `validateVendorPackage`（可单测，不读文件系统）；
     - `plugins/map-3d/tests/l4-tools.test.ts`：+9 例（l4-tools 19 → 28）；
     - `harness/l4-acceptance/vendor-dryrun/`：DRY-RUN 证据（合成包，非真实几何）+ README 声明。
   - 本 Feature：journal 本迭代 + `feature.yaml`（scope/acceptance/verification/blockers/iteration=2）+ OpenSpec `spaceai-l4-precision-model/tasks.md`（§9 入口 + 测试口径 53→62）。

3. 怎么验证？
   - L4 相关：`npx vitest run plugins/map-3d/tests/l4-tools.test.ts plugins/map-3d/tests/l4-acceptance.test.ts plugins/map-3d/tests/panorama-model-precision.test.ts` → **3 文件 / 62 例通过**（08:01）。
   - 验包 CLI 实测：合成 real 包 → `needs_human`（0 error，2 项人工）；SIMULATED 包（显式允许）→ `pass` 且带「不得作为 L4 精度验收依据」警告；占位包 `data/rebuild/l4-demo` → `fail`（缺 vendor-metadata）。
   - 类型：`pnpm typecheck` 0。
   - **验收复跑失败（记录为环境阻塞）**：`node tools/l4/acceptance.mjs` 在登录后定位「全景态势」超时；
     同一根因使 e2e 全量 14/25（2026-10-22 深夜实测）——并行会话 pano R 系列重构在途回归（工作树 2000+ 脏条目），非 L4 代码回归。

4. 发现什么问题？
   - **Iteration 1 记录陈旧**：OpenSpec 变更并非缺失——`769b1547f`（10-22 19:27）已补建并通过 document_control，main 上 8 个文件（proposal/design/tasks/specs）；本迭代已更正。
   - **L4 无法在本会话独立收口**：一键验收与 e2e 都依赖登录后主界面，被并行重构阻塞；真实资产仍未授权。
   - **精度不可自动化**：验包脚本只能判「声明齐全 + 结构可用」，几何精度必须控制点实测——已在工具输出中固定为 `needs_human`，防止「脚本 pass 被误读为 L4 精度达标」。

5. 是否可以提交？
   - 可以（文档 + 工具 + 测试 + 证据 + 治理账实；本地提交，不 push、不部署、不提升验收状态）。
   - 未完成：9.5 验收复跑（待并行会话收口）、8.1 真实资产接入（待授权）、8.2 几何精度验收（需真实资产 + 实测）。

### Iteration 3（2026-10-23 上午 · 全链路演练，不依赖 UI）

1. 这轮做什么？
   - 一键验收/e2e 被并行重构阻塞期间，补上「不依赖登录/UI」的 L4 全链路演练，证明接入链路本身没坏。
2. 改了什么？
   - `tools/l4/chain-dryrun.mjs`：生成 SIMULATED → 验包 → 导入 dry-run → 导入 apply → 校验 manifest →
     `--list`/`--off`/`--on`/`--fallback` 切换回滚；manifest 一律用临时文件，资产副本写 gitignored 目录，结束清理；
   - 证据 `harness/l4-acceptance/vendor-chain-dryrun/`（report.json 机器可读 + README 复跑说明）。
3. 怎么验证？
   - `node tools/l4/chain-dryrun.mjs` → **PASS：9 步全 0，10 项断言全过**（2026-10-23 08:17）；
   - 断言含：dry-run 不写 manifest、导入后 published=true、停用后 false、启用后 true、回滚后 manifest 有效且占位启用。
4. 发现什么问题？
   - 链路本身健康；唯一未闭环项仍是 9.6 验收复跑（被并行 pano 重构阻塞）与真实资产接入（未授权）；
   - 临时 manifest 隔离有效：线上 `data/rebuild/l4/manifest.json` 未被触碰（可 `git status` 与文件 mtime 复核）。
5. 是否可以提交？
   - 可以（工具 + 证据 + 治理账实；本地提交不 push）；Feature 保持 active/partial，不提升验收状态。
