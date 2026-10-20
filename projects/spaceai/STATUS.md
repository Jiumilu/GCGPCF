---
doc_id: GPCF-SPACEAI-STATUS-20261010
title: SpaceAI 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.3
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/spaceai/STATUS.md
source_path: projects/spaceai/STATUS.md
sync_direction: bidirectional
last_reviewed: '2026-10-20'
supersedes: []
superseded_by: []
---

# SpaceAI 状态

## 项目定位（2026-10-16 更新）

- **当前主项目：GlobalCloud SpaceAI Platform**（`../GlobalCloud SpaceAI Platform`，安防监控平台统一重构，独立 Git 仓）。
- `../GlobalCloud SpaceAI` 为 **CWME 归档与本地应用区**（保留 `apps/city-model/`、`prototypes/was-city-flood/`、CWME 评审文档与 `.harness/` 证据）。
- 历史 Windows/.NET 桌面工程（`MB3000.sln` 及各 C# 项目）于 **2026-10-16 按用户指示丢弃**，本地不再保留；可恢复副本在 `/tmp/gcspaceai-backup/legacy-windows-source-20261016.tar.gz`（含疑似明文凭据，外发前须脱敏）。
- 角色：external；目录名与中央注册别名沿用 SpaceAI。

## 仓库与合并（2026-10-16）

- 私有仓库：`https://github.com/Jiumilu/GCSpaceAI`（private），main。
- **单仓合并**：主项目历史与 SpaceAI 纳管基线已合并进同一远端；合并提交 `f3cc4de`（双父 `31809b9` + `e12a247`），纳管基线 2 提交保留在历史中。
- 为满足 GitHub 100MB 单文件限制，已用 `git filter-repo` 剔除历史中的 195MB 废弃备份库（`data/spaceai.db.prename.bak`）：433 提交保留、`.git` 74M→15M、**重写前后 HEAD 树哈希一致**（只改历史未动内容）。
- 推送均为快进，未 force push，未覆盖远端既有历史。

## 运行状态（2026-10-20 复测）

- 平台服务：BFF `127.0.0.1:39010`（`/healthz` status ok、263 端点、库 SIMULATED 39 表 510 行）；前端 `127.0.0.1:5273`（Vite 6.4.4）。
- CWME 本地应用：`apps/city-model/index.html` 可浏览器直开；预览服务 `127.0.0.1:4173`。
- 全量测试：**87 文件 / 807 项全过**（2026-10-20 T4 修复后实测，连续三轮：**31.2s / 22.1s / 19.2s**）。
- 测试成本：修复前 771s（曾 12–20 分钟不结束）、临时占用约 28GB；修复后 **~20–31s、临时占用≈0**（APFS 写时复制）。
- BFF 启动：修复后 **约 6 秒**就绪（此前 90 秒–6 分钟），且重启不再向运行库追加数据。
- 数据性质：`data/spaceai.db` 为合成样例库（`_seed_info.data_kind = SIMULATED`），非真实业务数据。

## 当前 Feature

- **F-017 cwme-city-world-model-engine**（active，partial）：CWME 城市模型与内涝切片回放；本地应用入口为 ../GlobalCloud SpaceAI/apps/city-model/index.html，证据索引在 ../GlobalCloud SpaceAI/.harness/runs/20261016-080823-spaceai-was-city-flood-replay/evidence-index.yaml。
- 关联 OpenSpec：openspec/changes/spaceai-was-city-flood-replay；仅有合成样例和本地浏览器验证，不声明 Platform 集成或真实城市运行。
- **F-024 panorama-engineering-convergence**（P1，active，**iteration 1**）：全景态势工程收敛；证据已补齐（tests/build/api pass、screenshots waived 附理由），OpenSpec 变更状态 **implemented**（22/22）。
- 交付：组件 3351 → 3310 行、新增 8 个纯模块与 8 个测试文件（188 项）；模板零改动；修复 D-4、D-3、D-5。
- 证据：`../GlobalCloud SpaceAI Platform/harness/runs/20261016-panorama-convergence/`；Feature 证据在 `features/active/F-024-.../evidence/`。
- 其余两个 spaceai OpenSpec 变更：`spaceai-was-city-flood-replay` **implemented**（12/12）；`spaceai-studio-multiplatform-refactor` **in_progress**（91/93，剩字段级适配与移动端适配）。

## 本轮迭代（2026-10-20 起，三条主线）

用户决策：三条主线全做、plaza 合入并默认关闭、T0–T4 全做。
计划全文：`../GlobalCloud SpaceAI Platform/评估与下轮迭代计划_20261020.md`

| 序 | 主题 | 状态 |
|---|---|---|
| T0 | 治理账实纠正 + plaza 收口 | **已完成**：F-024 证据/iteration 补齐；panorama 补 `.openspec.yaml`；三变更状态推进；plaza 按 WAE 规范 v1 补齐 Esc/resize/theme/版本降级/去 `'*'` 兜底，入口默认关闭，新增 16 项测试 |
| T1 | 契约可信（263 登记 / 233 显式注册 / mock 恒 200） | **进行中（基础设施已就位）**：①静态审计测试（运行时拦截 router）实测 **64 条登记但无显式实现 / 26 条已注册未登记**，设棘轮基线；②`/__contract__` 增加**运行期漂移报告**（登记数/路由数/mock 开关/双向差异），线上实测 263 登记·290 路由·26 条实现未登记；③mock 兜底可关闭且**在建 app 时冻结**，关闭后未实现端点 404、方法不匹配 405（新增 5 项强制边界测试，含开/关两实例对照）。剩余：逐条补齐 64 条未实现端点的 handler（棘轮分批） |
| T2 | 写可靠（117 处 run 调用仅 1 处判返回值；26 个多写函数 0 个事务） | **已完成**：改造 **10 个函数**（advanceOps / transitionLifecycle / ingestPush / saveRule / toggleRule / saveRelation / executePlan / fuseEvents / runObolRound / addLowAltitudeAssets）→ `tx` + `runStrict` + 失败如实返回；新增 **10 项触发器注入写失败测试**（含原子回滚断言），每批均做变异验证。全量 91 文件 / 829 项全过 |
| T3 | 数据治理与保留策略 | **已完成**：CityLink 归档去重（原表改名保留 2196 万行，新表 61,289 + 唯一索引，零删除）→ `/City/Stats` 17,000ms→155ms、聚合 17,020ms→27ms；只读保留报告 + 可复现去重脚本 + 4 项完整性守卫 |
| T4 | 测试基座 | **已完成**：定位城市数据幂等守卫 off-by-one（`> 50000` 而实际恰为 50,000）致每次 createApp 重建 2133 万行；修复后全量 771s→**~20–31s**、createApp 106s→0.3s、r09 143s→1s；`DB_PATH` 惰性可注入；18 个测试已隔离；**连续三轮全绿（87 文件/807 项）** |
| 前端 | SSE 收口 / PanoramaDeep 拆分 / 设计系统 | **SSE 收口 ✅**（全景态势 `sseOff` 从不退订 + click 监听未移除，新增静态生命周期守卫并变异验证）；**设计系统 ✅**（`tokens.css`/`base.css` 此前全仓 0 处 import 已落地到 desktop 入口；23 个 `--gc-*` 变量全部有定义；浏览器实测令牌生效、全景态势 DOM 1506/21 卡与基线一致、0 错误）；**PanoramaDeep 拆分待做**（脚本仍 2318 行） |
| 性能 | 无 GPU 环境可用性（SwiftShader 3 FPS） | 待做 |

**已登记未执行的治理动作**：OpenSpec 物理归档（`changes/` → `changes/archive/`）未做——移动会同时改变 `.kds` 镜像路径与 frontmatter 的 `kds_path`/`source_path` 双向映射，需一次专门的镜像同步操作，不与其他改动混做。

## 状态与边界

- project_status: registered；overall_status: partial。
- authorization: `user_authorized_onboarding_and_git_2026-10-10`；`user_authorized_single_repo_merge_and_push_2026-10-16`。
- confirmation：业务验收、生产发布**未确认**；不得提升 accepted / integrated / production_ready / customer_accepted。
- 未部署、未接入真实设备或生产数据、未改 schema。

## 已知未修缺陷（台账）

| ID | 问题 | 状态 |
|---|---|---|
| D-1 | 测试临时库不清理致磁盘两次写满；`db.test.ts` 偶发失败（DB_PATH 于 import 期冻结 + worker 模块缓存跨文件存活） | 磁盘部分已治理（运行级根目录 + 主进程 teardown，跨轮零累积）；但**每轮仍实拷贝 17×1.9GB≈32GB**、`db.test.ts` 仍偶发 → 列入 **T4** |

## 项目群总体架构 v1.1 承接（2026-10-18）

SpaceAI Platform 是安防统一重构主工作区，CWME 是城市/空间域实现，World 定义注册、引用和推演接口，XWAIL 定义模型/事件契约。现有合成样例不构成真实设备或城市业务运行。仓内唯一项目总体方案尚未确认，传导状态 `pending_unique_plan`；本状态页不替代项目总体方案。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/spaceai-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project spaceai`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## Git 回读

- 私有 origin 已创建并可用；纳管基线初始提交 `480c59bb172afc68236edc2299d1998bfc27807e` 仍在历史中。
- 本目录 CWME 应用、样板、六份评审/评估文档及部分 .harness 证据目前仍为本地未跟踪文件；已纳入治理范围与路径核验，但尚未形成新的 Git 提交或远端归档。
- 技能链与 OpenSpec 覆盖按并行新增后的 21 项目通过。
- 文档门禁于 2026-10-18 实跑：loop_document_gate.py --check-only 返回 rework_required（missing_metadata、hard_failure:loop_ui_product_first_control、hard_failure:document_pollution）；属于当前 GPCF 总控门禁结果，保持 partial/rework。本目录 README 与 Harness Manifest 已纠正为 CWME 定位，纳管不等于业务验收。

## 变更说明（v1.0 → v1.1，2026-10-16）

1. 项目定位由「Windows/.NET 桌面工程，入口 MB3000.sln」更正为「主项目 = SpaceAI Platform；本目录为 CWME 归档与本地应用区」——依据用户 2026-10-16 明确指示。
2. 新增仓库与合并、运行状态、当前 Feature、已知缺陷台账四节。
3. 删除已失效条目：「历史源码存在疑似凭据，保留本地且未提交/上传」「当前 macOS 缺 Windows/.NET 构建工具」「下一步：凭据清理后源码入库」——源码已丢弃，上述前提不成立。
4. 保留：状态保持 partial、不得自动提升验收状态、OpenSpec 入口与 Git 回读口径。

## 变更说明（v1.1 → v1.2，2026-10-18）

- 对齐本目录 README 与 Harness Manifest 的 CWME 定位，并记录当前 GPCF 文档门禁实测结果；业务验收与生产发布边界不变。

## 变更说明（v1.2 → v1.3，2026-10-20）

1. 当前 Feature 一节：F-024 由「待收口」更正为 iteration 1 + 证据齐备（tests/build/api pass、screenshots waived 附理由）；OpenSpec 三个 spaceai 变更状态由 draft 推进为 implemented（2 个）/ in_progress（1 个，剩余 2 项真实未完），并补 panorama 变更缺失的 `.openspec.yaml`。
2. 新增「本轮迭代（2026-10-20 起，三条主线）」一节，记录 T0–T4 与前端/性能的当前状态与用户决策（三条主线全做、plaza 合入并默认关闭、T0–T4 全做）。
3. 运行状态一节改为 2026-10-20 复测数据：86 文件 / 802 项、单轮 12.8 分钟、临时占用约 28GB。
4. 缺陷台账 D-1 更新：磁盘累积已治理，但每轮仍 32GB 实拷贝与 `db.test.ts` 偶发，明确列入 T4。
5. 登记未执行动作：OpenSpec 物理归档需同步 `.kds` 镜像与 frontmatter 双向路径，单独操作。
