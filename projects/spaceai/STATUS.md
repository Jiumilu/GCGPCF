---
doc_id: GPCF-SPACEAI-STATUS-20261010
title: SpaceAI 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.13
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/spaceai/STATUS.md
source_path: projects/spaceai/STATUS.md
sync_direction: bidirectional
last_reviewed: '2026-10-24'
supersedes: []
superseded_by: []
---

# SpaceAI 状态

## 项目定位（2026-10-16 更新）

- **当前唯一正本：GlobalCloud SpaceAI Platform**（`../GlobalCloud SpaceAI Platform`，安防监控平台统一重构，独立 Git 仓）。
- 原 `../GlobalCloud SpaceAI`（SpaceAI-Legacy，CWME 归档与本地应用区）**已于 2026-10-22 归档**：与 Platform 同源双克隆分叉，Platform 为唯一正本；Legacy 46 个独有提交已打 tag `archive-spaceai-legacy-20261022`，目录移至 `_archive/2026-10-22-retired-assets/GlobalCloud SpaceAI`（可原路 `mv` 恢复，见其 `MANIFEST.md`）。CWME 资产（`apps/city-model/`、`apps/was-city-flood/`、CWME 评审文档与 `.harness/` 证据）随之归档，F-017 的证据路径以归档路径为准。
- 历史 Windows/.NET 桌面工程（`MB3000.sln` 及各 C# 项目）于 **2026-10-16 按用户指示丢弃**，本地不再保留；可恢复副本在 `/tmp/gcspaceai-backup/legacy-windows-source-20261016.tar.gz`（含疑似明文凭据，外发前须脱敏）。
- 角色：external；目录名与中央注册别名沿用 SpaceAI。

## 仓库与合并（2026-10-16）

- 私有仓库：`https://github.com/Jiumilu/GCSpaceAI`（private），main。
- **单仓合并**：主项目历史与 SpaceAI 纳管基线已合并进同一远端；合并提交 `f3cc4de`（双父 `31809b9` + `e12a247`），纳管基线 2 提交保留在历史中。
- 为满足 GitHub 100MB 单文件限制，已用 `git filter-repo` 剔除历史中的 195MB 废弃备份库（`data/spaceai.db.prename.bak`）：433 提交保留、`.git` 74M→15M、**重写前后 HEAD 树哈希一致**（只改历史未动内容）。
- 推送均为快进，未 force push，未覆盖远端既有历史。

## 运行状态（2026-10-22 复测）

- 平台服务：BFF `127.0.0.1:39010`（`/healthz` status ok、mode demo、**263 端点**、库摘要 SIMULATED 39 表 510 行）；前端 `127.0.0.1:5273`（Vite 6.4.4）。
- 全量测试：**143 文件 / 1293 例全过**（2026-10-22 20:09 实测，exit 0；含新增时间索引守卫 4 例与并行会话用例）；`pnpm typecheck` **0 错误**。
- 数据规模：`data/spaceai.db` **181.3MB**（190,074,880 B = 压缩后 160.5MB + 时间索引 20.8MB；压缩前 2069.5MB）——历史归档表 2196 万行已外置到 `data/archives/citylink-archive-20261020.db`（1984.3MB，manifest 登记），备份 `data/backups/spaceai.db.bak-20261022T114118`；`EXT_CityLink` 61,289、`EXT_SceneAsset` 50,179、`EXT_ObolObservation` 约 52.9 万、`IngestEvent` 约 14.2 万（随 BFF 正常增长）。
- 测试成本：修复前 771s、临时占用约 28GB；T4 + D-8 后 ~20–26s；2026-10-22 再上**小种子库**：基库 160.3MB → **18.9MB**，构建 10.4–13.1s → **0.49–0.61s**，全量峰值临时占用 4.15GB → **0.38–0.51GB**。
- BFF 启动：约 6 秒就绪（2026-10-20 口径；2026-10-22 只复测 `/healthz`，未复测冷启动耗时）。
- CWME 本地应用：`apps/city-model/index.html` 已随 Legacy 归档移出根目录（2026-10-22），F-017 证据路径以归档路径为准。
- e2e：`e2e/` 9 个 spec（含 `panorama-l4` 3 条、`panorama-operate` 5 条、`panorama-smoke`）；**已常态化**：`playwright.config.ts` 内置 `webServer`（BFF + dev，`reuseExistingServer`），`pnpm e2e:smoke` 一条命令跑通，不再手工起服务（D-12 已修复）。
- L4 一键验收：`harness/l4-acceptance/` **PASS ×2**（smoke-sim 60 FPS / smoke-demo 56 FPS，0 fail；资产为 placeholder/SIMULATED）。
- 数据性质：`data/spaceai.db` 为合成样例库（`_seed_info.data_kind = SIMULATED`），非真实业务数据。

## 当前 Feature

- **F-017 cwme-city-world-model-engine**（active，partial）：CWME 城市模型与内涝切片回放；本地应用入口为 `_archive/2026-10-22-retired-assets/GlobalCloud SpaceAI/apps/city-model/index.html`（原 `../GlobalCloud SpaceAI`，2026-10-22 归档），证据索引在同目录 `.harness/runs/20261016-080823-spaceai-was-city-flood-replay/evidence-index.yaml`。
- 关联 OpenSpec：openspec/changes/spaceai-was-city-flood-replay；仅有合成样例和本地浏览器验证，不声明 Platform 集成或真实城市运行。
- **F-024 panorama-engineering-convergence**（P1，active，**iteration 2**）：全景态势工程收敛；iteration 1 证据保持有效（tests/build/api pass、screenshots waived 附理由），iteration 2 于 2026-10-22 补记 B5a–B5e 的拆分收益；B5f/B5g 外提（`441f55c` / `9f4fbcb`）归 F-038 记账。
- 交付：iteration 1 组件 3351 → 3310 行、8 个纯模块 + 188 项测试、模板零改动、修复 D-4/D-3/D-5；iteration 2 再外提 5 个组合式（`useFeedback`/`useCardConfig`/`useCameraModes`/`useCardOrder`/`useDemoModes`，新增 9 例）；B5f/B5g 后组件 **3638 行**（气泡层与卡片列另拆组件：PanoramaBubbles / PanoramaCardColumn）。
- 证据：`../GlobalCloud SpaceAI Platform/harness/runs/20261016-panorama-convergence/`；Feature 证据在 `features/active/F-024-.../evidence/`。
- **F-037 map-3d-l4-precision-model**（P1，active，iteration 1，2026-10-22 追溯建账）：三维地图 L4 精模链路（口径/清单/BFF/引擎/切换回落/接入工具链/一键验收/演练/CI）全部落地并本地提交 6 个提交；**真实 L4 资产未接入**（采购与自采暂停，待授权）。
- F-037 证据：`../GlobalCloud SpaceAI Platform/harness/l4-acceptance/`（PASS ×2）、`harness/l4-evidence/`、`docs/3d/l4-*.md`；Feature 证据在 `features/active/F-037-.../evidence/`。
- **F-038 panorama-operation-normalization**（P1，active，**iteration 4**，2026-10-22 追溯建账）：全景态势操作流程规范化执行到 B5j（B0–B5j 共 16 个本地提交（含合并）；143 项操作 / 106 条问题审计 + N1–N12 方案）；**B5 五大块已全部外提完成**（气泡 B5f / 卡片列 B5g / 飞翔+CWME B5h、B5i / 控制器 B5j）；**剩余**：i18n 约 600 行、人工验收、script 行数目标未达（PanoramaDeep 总 3590 行 / script 2956 行）。
- F-038 证据：`../GlobalCloud SpaceAI Platform/.harness/runs/20261022-panorama-ops/`（01–21）、`docs/全景态势_操作流程规范化与合理化方案_20261022.md`；Feature 证据在 `features/active/F-038-.../evidence/`。
- 其余两个 spaceai OpenSpec 变更：`spaceai-was-city-flood-replay` **implemented**（12/12）；`spaceai-studio-multiplatform-refactor` **in_progress**（91/93，剩字段级适配与移动端适配）。
- **治理欠账（2026-10-22 登记，同日关闭）**：F-037 / F-038 当时未建 `openspec/changes/spaceai-*` 变更；2026-10-22 晚已补建 `spaceai-l4-precision-model`（**implemented**，真实资产仍待授权）与 `spaceai-panorama-operation-normalization`（**in_progress**，B5 剩余四大块未完成），三层对齐表门禁通过。

## 本轮迭代（2026-10-20 起，三条主线）

用户决策：三条主线全做、plaza 合入并默认关闭、T0–T4 全做。
计划全文：`../GlobalCloud SpaceAI Platform/评估与下轮迭代计划_20261020.md`

| 序 | 主题 | 状态 |
|---|---|---|
| T0 | 治理账实纠正 + plaza 收口 | **已完成**：F-024 证据/iteration 补齐；panorama 补 `.openspec.yaml`；三变更状态推进；plaza 按 WAE 规范 v1 补齐 Esc/resize/theme/版本降级/去 `'*'` 兜底，入口默认关闭，新增 16 项测试 |
| T1 | 契约可信 | **✅ 完成（验收口径：差异归零或逐条登记例外）**：①静态审计 + `/__contract__` 运行期漂移报告 + mock 兜底可关闭（404/405 边界测试）；②口径纠偏：原「64 条未实现」高估约 2 倍（mock 循环先调 realData）→ 现三分：显式实现 **203/257 (79.0%)**、仅样例 **23**（全部登记原因）、bridged 31、未登记 26；③两批共补 10 个真端点（ServerDateTime / User.Info / KeepAlive / LogOut / Alarm 统计×2 / Asset.Type.Info / PatrolLine.Info / DeviceAccess / AssetInfo.AssetID），全部断言非 mock；④23 条例外分五类（no-data-model 14 / legacy-external 7 / unmapped-model 1 / static-page 1 / unsafe-debug 1），并加**双向一致性断言**防例外表腐化（新增缺口必须登记、已实现必须移除） |
| T2 | 写可靠（117 处 run 调用仅 1 处判返回值；26 个多写函数 0 个事务） | **已完成**：改造 **10 个函数**（advanceOps / transitionLifecycle / ingestPush / saveRule / toggleRule / saveRelation / executePlan / fuseEvents / runObolRound / addLowAltitudeAssets）→ `tx` + `runStrict` + 失败如实返回；新增 **10 项触发器注入写失败测试**（含原子回滚断言），每批均做变异验证。全量 91 文件 / 829 项全过 |
| T3 | 数据治理与保留策略 | **已完成**：CityLink 归档去重（原表改名保留 2196 万行，新表 61,289 + 唯一索引，零删除）→ `/City/Stats` 17,000ms→155ms、聚合 17,020ms→27ms；只读保留报告 + 可复现去重脚本 + 4 项完整性守卫 |
| T4 | 测试基座 | **已完成**：定位城市数据幂等守卫 off-by-one（`> 50000` 而实际恰为 50,000）致每次 createApp 重建 2133 万行；修复后全量 771s→**~20–31s**、createApp 106s→0.3s、r09 143s→1s；`DB_PATH` 惰性可注入；18 个测试已隔离；**连续三轮全绿（87 文件/807 项）** |
| 前端 | SSE 收口 / PanoramaDeep 拆分 / 设计系统 | **SSE 收口 ✅**、**设计系统 ✅**（令牌落地、23 个 `--gc-*` 全部有定义、浏览器实测生效）；**PanoramaDeep 拆分：部分达成**——组件 3351 → **3184 行**，外提 **20 个模块**（新增测试 100+ 项），并补了 **组件级测试**（3 项，经变异验证可捕获「类型与单测都过、运行时崩」的事故）。未达原计划「脚本 <800 行」（当前 2191 行，差 2.7×）；停止依据与建议见主项目 `harness/runs/20261020-final-gate/ASSESSMENT.md` 第六节 |
| 性能 | 无 GPU 环境可用性（SwiftShader） | **✅ 完成**：实测有 GPU 75.2 FPS / SwiftShader **4.8 FPS**；诊断确认瓶颈是**逐帧重绘**而非填充率（隐藏画布 5.5→60 FPS；0.6 分辨率仍只 5.4 FPS）；新增渲染档位判定（软件渲染 → 关阴影/雾/光照/FXAA + 0.6 分辨率 + **按需渲染** + 心跳 requestRender），实测软件渲染 **4.8 → 56.4 FPS（11.75×）**，有 GPU 侧 70.5 FPS 无回归；画面经像素采样验证（16 采样点 16 色）非冻结，21 卡、0 错误 |

## 本轮迭代（2026-10-22，多线并行）

老卢 2026-10-22 指令：三维地图模型升级为 L4 级精模、白盒模型保留可切换；随后同意**暂停 L4 自采**、转平台欠账。
本轮四条线均本地提交、**0 推送**，验收状态一律保持 partial。

| 线 | 主题 | 状态 | 证据 |
|---|---|---|---|
| A | 三维地图 L4 精模（F-037） | **链路完成，真实资产缺**：6 提交（管线 / 工具链 / 演练 / 验收 / CI / 采购包）；L4 相关 53 例、全仓 1242 例；一键验收 PASS ×2；占位与真实三处标注 | `harness/l4-acceptance/`、`docs/3d/l4-*.md` |
| B | 全景态势操作规范化（F-038） | **主体完成（B0–B5j，16 提交含合并）**：143 项操作 / 106 条问题审计 → N1–N12；六组 P0、Esc 单一契约、⌘K 命令面板、偏好收口；**B5 五大块全部外提**（气泡 / 卡片列 / 飞翔 / CWME / 控制器），组件 3955 → 3590 行；e2e 5/5；余 i18n 约 600 行 / 人工验收 / script <800 目标 | `.harness/runs/20261022-panorama-ops/01–21` |
| C | 平台欠账清理 | **完成**：`log-viewer` / `scene-hub` 零测试补齐 26 例（`063cc49`）；项目群规范四件套与 `.gitignore`（`6e7e227`）；README / AGENTS / Manifest 缺失章节（`1b7f4b1`） | 提交记录；全仓 1242 例 |
| D | 治理账实（本轮） | **完成**：追溯建 F-037 / F-038 账、F-024 iteration 2、STATUS / RISK / ROADMAP 同步；**OpenSpec 变更补建与 KDS 镜像同步登记为欠账** | 本文件、`features/active/F-037-*`、`F-038-*` |

**边界**：未 push（main 领先 `origin/main` 34 提交，随并行会话变动，以 `git rev-list --count origin/main..main` 为准）、未部署、未接真实设备或生产数据；L4 采购 / 自采 / 合规外部数据均待授权。

## 本轮迭代（2026-10-22 晚，待办排序执行）

按老卢指令「用决策模型确认所有待办排序执行」：以 `priority_rank` 逐轮淘汰得序列
**A2 刷新账实 → D e2e → C 测试基座 → E L4 采购/合规 → F 治理收尾 → B 数据保留 → G 推送 / H 全景收尾**（末两位模型分歧且 G 属红线，后置）。

| 序 | 待办 | 结果 | 提交 / 证据 |
|---|---|---|---|
| 1 | A2 刷新账实 | ✅ 完成：B5f、136/1251 例、提交数改为实查口径；queue 补 F-032/F-033 → repository-only 门禁 pass | GPCF `95383b013` |
| 2 | D e2e 常态化 | ✅ 完成：webServer 自起 BFF+dev、`e2e:smoke`、修 `dev:web` PATH；pano-smoke 1 passed / 33.2s | 平台 `ca96bee` |
| 3 | C 测试基座 | ✅ 完成：小种子库 18.9MB、峰值 0.4–0.5GB、138 文件/1263 例连绿；DB_PATH 注入 4 例证明 | 平台 `6d7fffc` |
| 4 | E L4 采购/合规 | ✅ 完成（文档）：RFQ 执行包 7 件 + 合规外部数据源核验清单（未申请 key、未对外发送） | 平台 `6c8c9bc` |
| 5 | F 治理收尾 | ✅ 完成：补建两个 OpenSpec 变更（三层对齐 `[OK]`），关闭治理欠账 | GPCF `4354c5baf` |
| 6 | B 数据保留 | ✅ 完成：方案 + 工具 + 压缩（2069.5MB → 160.5MB）+ **时间索引**（近 1 天查询 5–9ms→0.05ms） | 平台 `e06c9da`、`23a1a4d`、`e239242` |
| 7 | G 推送 / H 全景收尾 | G ✅ **已推送**（20:09，main → 私有远端，含合并远端 CI commit）；H ✅ 由并行会话完成 B5f–B5j（五大块全部外提） | 远端 `070a778` / F-038 |

**边界**：已推送（远端 `070a778`，本地与远端 0/0）、未部署、未提升验收状态；数据压缩已于 19:41 执行（有备份，可回滚）。

## 终态证据（2026-10-20）

- `pnpm gate`（typecheck + 全仓 build + 全量测试）**连续三轮 exit 0**。
  最终时点 HEAD `b54bd53`：各 **106 文件 / 964 项**（紧凑测试基库 135MB，D-8 根治后）；
  历史对照：`03b82d3` 96/879 → `cfa0c4c` 98/898 → `60d288b` 99/905，均存档。
- **完成度评估**：`../GlobalCloud SpaceAI Platform/harness/runs/20261020-final-gate/ASSESSMENT.md`
  —— 11 项达成、1 项部分达成（PanoramaDeep 拆分 3351→3199 行，未达计划形态，
  原因与建议见评估第二节）；缺陷台账 D-1/D-3/D-4/D-5/D-7 全部闭环。
  证据：`../GlobalCloud SpaceAI Platform/harness/runs/20261020-final-gate/`
  （原始日志 ×3 + `gate-summary.json` + 迭代要点 README）。
- 其余证据：全景态势收敛 `harness/runs/20261016-panorama-convergence/`、
  设计令牌 `.../20261020-frontend-convergence/evidence/`、
  无 GPU 性能 `.../20261020-perf-nogpu/evidence/`；
  e2e 旗舰队冒烟 `e2e/panorama-smoke.spec.ts`（断言 0 页面错误）。

**已登记未执行的治理动作**：OpenSpec 物理归档（`changes/` → `changes/archive/`）未做——移动会同时改变 `.kds` 镜像路径与 frontmatter 的 `kds_path`/`source_path` 双向映射，需一次专门的镜像同步操作，不与其他改动混做。

## 终态证据（2026-10-22）

- 全量测试：`npx vitest run` **143 文件 / 1293 例通过**（20:09，exit 0）；`pnpm typecheck` **0 错误**。
- **追加表时间索引已补**（20:01）：`idx_ingest_createdat` / `idx_obol_at`；近 1 天查询 5–9ms→**0.05ms**、18–22ms→**0.5–1ms**；`retention-report` 索引体检由两表告警变为「所有 >10 万行表都有索引」；证据 `harness/data-retention/index-evidence-20261022.md`（平台 `e239242`）。
- **数据压缩已执行**（19:41 维护窗口，老卢授权）：2069.5MB → **160.5MB**；外置 1984.3MB / 21,962,610 行；备份 2069.5MB；BFF 重启后 `/healthz` 200；压缩后全量测试通过。
- 提交数说明：本地领先数随并行会话持续提交变化（19:04 = 30、19:11 = 33、19:22 = 34），本页数字为复测时点快照。
- L4 一键验收：`harness/l4-acceptance/smoke-sim` 与 `smoke-demo` 的 `report.json` 均 **0 fail**（60 / 56 FPS；贴地 0m；画面差异 4.57% / 3.40%；错误 0）。
- L4 工具链冒烟：`harness/l4-evidence/toolchain-smoke.md`（校验 / manifest / 导入 dry-run 全 exit 0）；SIMULATED 演练 `harness/l4-evidence/sim-drill/report.md` 含回滚后快照。
- e2e：`panorama-l4.spec.ts` 3 条、`panorama-operate.spec.ts` 5/5（真实 Chrome）；`pnpm e2e:smoke` 5 passed（webServer 自起，12.6s）。
- 接口：`/healthz` 200（263 端点）；`/RestFul/Rebuild/Tileset` 200（2 条资产：占位 1 条 published、SIMULATED 1 条未发布）。
- 证据索引：`features/active/F-037-map-3d-l4-precision-model/evidence/`、`features/active/F-038-panorama-operation-normalization/evidence/`。
- 测试与 e2e：小种子库（18.9MB / 构建 0.5s）+ `webServer` 常态化（`pnpm e2e:smoke`）；数据保留方案与压缩工具（dry-run）就绪。
- **未执行**：时间窗归档（D-10 剩余，需数据变旧，当前 0 行到期）；真实 KDS API 写入（本轮只做本地镜像）。
- **已执行**：远端 CI 已恢复（GPCF 注册 self-hosted runner `mac-mini-gpcf`，repository-checks + 统一规范检查均跑通）；KDS 镜像全量收敛并提交（D-11 关闭，PR #57）。
- OpenSpec 变更账：`openspec/changes/spaceai-l4-precision-model`、`openspec/changes/spaceai-panorama-operation-normalization`（2026-10-22 补建，三层对齐 `[OK]`）。

## 状态与边界

- project_status: registered；overall_status: partial。
- authorization: `user_authorized_onboarding_and_git_2026-10-10`；`user_authorized_single_repo_merge_and_push_2026-10-16`。
- confirmation：业务验收、生产发布**未确认**；不得提升 accepted / integrated / production_ready / customer_accepted。
- 未部署、未接入真实设备或生产数据、未改 schema。

## 已知未修缺陷（台账）

| ID | 问题 | 状态 |
|---|---|---|
| D-1 | 测试临时库不清理致磁盘两次写满；`db.test.ts` 偶发失败（DB_PATH 于 import 期冻结 + worker 模块缓存跨文件存活） | **已大幅收敛**：T4 + D-8 后实拷贝消除；2026-10-22 小种子库把基库 160.3MB → **18.9MB**、峰值临时占用 4.15GB → **0.4–0.5GB**、构建 ~11s → **0.5s**；`db.test.ts` 仍有意直读运行库（未改语义），偶发未复现 |
| D-7 | 全量套件偶发单文件失败（2026-10-20 出现 2 次，重跑即绿） | **已定位并修复**：5 轮循环捕获现场，为 `world-axis.test.ts > W1-1 时空检索` **默认 5s 超时**（实测 5004ms），非此前的克隆内容猜测；已给该文件 20 个用例显式 30s 超时（与 ingest-bus 同法）。克隆完整性校验保留（解决另一类问题）。修复后连续三轮全量 99 文件 / 905 项全过 |
| D-10 | 追加表无保留策略；库 2.17GB 中 1905.9MB 是历史归档表（2196 万行），追加表数据仅约 10 天 | **压缩 + 时间索引均已完成**（2026-10-22）：2069.5MB → 160.5MB（归档表外置 + 备份 + manifest）；新增 `idx_ingest_createdat` / `idx_obol_at`（库 181.3MB，近 1 天查询提升 100–180× / 20–40×，4 例查询计划守卫）；**剩余**：时间窗归档待数据变旧（当前 0 行到期）、`(Result, Id)` 查询型索引未做（不在本次范围） |
| D-11 | KDS 镜像与源码差异 | **已关闭（2026-10-22）**：`document_control.py --apply-full` 全量重建并提交（PR #57，484 文件 / +8845−4338：213 个目录 README 补 frontmatter、3 个台账重算、270 个镜像文件重写）；重建后 `--check` 幂等为 0；repository-only 门禁 pass（kds_md 3612）。真实 KDS API 写入未做（另需授权） |
| D-12 | e2e 基座缺 `webServer`：`playwright.config.ts` 无自启，9 个 spec 需手工先起 dev 5273 + BFF 39010 | **已修复（2026-10-22）**：`webServer` 自起 BFF+dev、`reuseExistingServer`、`e2e:smoke` 一条命令；Lead 复跑 panorama-smoke 1 passed 33.2s |
| D-13 | 提交与远端同步 | **已关闭（2026-10-22 20:09）**：老卢「继续」授权推送；main 推送到私有远端（46 本地提交 + 远端 1 个 CI 提交合并，含冲突解决：`.github/workflows/standards.yml` 采用远端 self-hosted runner 方案）；远端 `070a778`，本地/远端 0/0。历史备注：推送前修正了 `b9236aa` 的提交信息错位（索引工作被冠以 pano 信息），改写为 `e239242`（仅本地未推送历史）；未 force push |
| D-14 | 写路径「失败仍报成功」类缺陷（审计发现；T2 后残留） | **已修复并已推送（2026-10-22 深夜）**：只读审计（`tools/audit/contract-write-audit.mjs` + `.harness/runs/20261022-contract-write-audit/report.md`）定位 P0 原子性 1 个（`commitDraft` 两写无 tx）、P1 真值上报 31 个单写、P2 播种 5 个；分四轮修复：P0 `8a913a0`、P1 高价值 11 `a669722`、P1 其余 17 `9506f70`、P2 `d1fc01a`；配套统一错误出口 + 44 例注入测试。扫描口径 `run()` 吞异常写 63 函数 → **17（剩余均为启动播种或已核实例外/误报）** |
| D-15 | 契约登记滞后：25 条实现先行端点未进协议（Demo/Focus/Scene 等）；31 条 bridged 无元数据标注 | **已关闭（2026-10-22 深夜，`5bd911b`）**：登记 263 → **288**，25 条补登（Demo 标 `demo:true` 非对外契约），31 条标 `coverage:'bridged'`；`/__contract__` 与 mock 兜底参数形态泛化为 `\{param\}`；棘轮 `unregistered 26 → 0`，新增 bridged 双向一致断言。实测：显式实现 **226/280 = 80.7%**、仅样例 23（逐条例外）、bridged 31、**未登记 0** |

| D-16 | L4 真实资产缺口（公开源已排除；园区合作待对外授权） | **缺口仍在（2026-10-24）**：L4 精模链路已闭环（验收 PASS / 全链路演练 / 验包入口），但几何精度必须由真实资产+控制点实测证明。公开源调研（`docs/3d/l4-open-dataset-research.md`）结论：OSM/Google 实景三维/天地图/实景三维中国等均不满足 L4 精度或许可/境内合规；园区既有成果合作备料已就绪（`docs/3d/l4-park-cooperation-package.md` + `harness/l4-park-coop/` 三份模板），**未联系、未发送、未签约**。对外动作待老卢逐项授权；F-037 保持 active/partial |


## 前端持续重构（第 37–43 轮续）

**按「说谎成本」而非行数挑选抽取目标**（说错了会误导用户/静默出错的地方优先）：

| 批次 | 模块 | 守住的风险 | 测试 |
|---|---|---|---|
| ⑯ | `dataInfo` | 把「演示模型」说成真实数据 | 7 |
| ⑰ | `sceneMap` | 消防数据被标成公共安全（表互逆性） | 8 |
| ⑱ | `markerIds` | 标记 id 前缀写错 → 标记点不动/关不掉 | 7 |
| ⑲ | `flightHeights` | 飞错高度导致穿模；原实现有 **5000/3000 两个不同兜底**，已保留差异 | 6 |
| ⑳ | `aliveIntervals` | 卸载后定时器继续跑并写失效状态 | 5 |

**一次自纠（重要）**：第 18 批的源码守卫**第一版是假测试**——正则只匹配已知前缀，
把某处改成 `ele-` 后测试依然全绿。经变异验证发现并两次修正（先误伤 `fp-`/`sn-` 等
非标记前缀，最终改为定向变体检测 + 按文件归属的出现性断言）。
**测试本身也经过验证，不是写完就算。**

**权威 gate 证据（第 43 轮）**：连续三轮 `pnpm gate` 全绿，HEAD `b563ffd`，
各 **116 文件 / 1038 项**。诚实边界已写入证据文件 `caveat` 字段：
工作树存在**他方 2 处未提交改动**（`apps/desktop/src/main.ts`、`vite.config.ts`，
「统一反馈入口 v0.3 跨仓植入」，非本迭代产出，本迭代未提交）。

## 前端持续重构（2026-10-20 晚，第 31–36 轮）

**从纯函数外提推进到 composable 级重构**（此前后 13 批均为无 ref 依赖的纯逻辑）：

| 批次 | 模块 | 内容 | 测试 |
|---|---|---|---|
| ③ | `useReplayPlayback` | 回放播放状态机（4 refs + 3 操作 + 定时器） | 8 |
| ④ | `useFlyPath` | 快捷航线状态簇（5 状态 + 5 操作，持久化/导入/分享/轨迹） | 11 |
| ⑤ | `useRealtimeIngest` | 实时警情摄入编排（计数/入流/上图/通知/审计注入） | 8 |
| — | `measure` / `bubbleState` | 测距计算与文案、气泡默认状态契约 | 10 + 4 |

**组件测试护栏两次生效**（这是本轮最有价值的产出）：
- `replayTimer is not defined`（残留引用）
- `Cannot access 'feed' before initialization`（TDZ，composable 实例化位置不当）
两者 `tsc` 均无法发现，正是第 8 轮事故（tsc 与 845 项单测全绿、界面整屏崩）的同类；
现由组件测试在提交前拦下。

**D-9（测试基建）**：高负载下 `beforeAll` 超默认 10s 钩子超时 → 整文件收集失败，
且清理阶段二次异常掩盖真因。已全局设 `hookTimeout: 30_000` 并为 3 个测试文件补 teardown 守卫。

**权威 gate 证据**：连续三轮 `pnpm gate` 在**同一提交**（平台仓 `ccd08e5`）上全绿，
各 **111 文件 / 1005 项**；工作树在三轮执行期间无改动。
证据：`../GlobalCloud SpaceAI Platform/harness/runs/20261020-final-gate/gate-summary-authoritative.json`。

## D-8（2026-10-20 晚）— 已根治

**曾**：`pnpm gate` 连续三轮偶发单文件级失败，失败点固定在 `useTestDb`
（`fixtures.ts`），报 `database disk image is malformed` 或复制失败，每次命中文件不同。

**真因（两次误判后确认）**：①17 个测试各克隆 2.14GB 运行库，磁盘 95% 时 APFS
写时复制退化为实拷贝 → 17×2.14GB ≈ 36GB > 可用 → 副本截断；
②**`copyFileSync` 拷了正在被 BFF 写入的运行库** → 撕裂副本（连紧凑基库构建都报 malformed）。

**修复**：`vitest.global-setup.ts` 改用 **`VACUUM INTO`** 一致性快照构建**紧凑测试基库**，
再清空归档表（实测占 1905.9MB / 89%）并 VACUUM：**2044MB → 135MB（15×）**；
`fixtures.ts` 优先克隆紧凑基库。夹具为派生、每轮重建、随 run 根回收，生产库不受影响。

**验证**：连续三轮 `pnpm gate` 全绿——各 **105 文件 / 953 项**、基库 135MB。
证据：`../GlobalCloud SpaceAI Platform/harness/runs/20261020-final-gate/g5-*.log` +
`gate-summary-d8.json`。**gate 结果自此恢复可信**。

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

## 变更说明（v1.3 → v1.4，2026-10-22）

1. **项目定位**：原 `../GlobalCloud SpaceAI`（SpaceAI-Legacy）于 2026-10-22 归档至 `_archive/2026-10-22-retired-assets/GlobalCloud SpaceAI`，Platform 为唯一正本；F-017 的应用入口与证据路径改为归档路径。
2. **当前 Feature**：F-024 推进到 iteration 2（B5a–B5e 拆分补记）；**新增 F-037（L4 精模）与 F-038（全景态势操作规范化）** 两个追溯建账的 Feature，并登记「未建 OpenSpec 变更」的治理欠账。
3. **新增「本轮迭代（2026-10-22，多线并行）」**：四条线（L4 / 全景操作规范化 / 平台欠账清理 / 治理账实）的状态、提交与证据，明确 0 推送与 partial 上限。
4. **运行状态**改为 2026-10-22 复测：135 文件 / 1242 例、typecheck 0、库 2.17GB 与四张追加表行数、L4 一键验收 PASS ×2、e2e 需手工起服务。
5. **新增「终态证据（2026-10-22）」**：测试/验收/接口/演练证据与未执行项（远端 CI、KDS 镜像同步）。
6. **缺陷台账**：更正 D-1（32GB 实拷贝已由 T4 + D-8 根治，`db.test.ts` 偶发未复现）；新增 D-10（数据保留）、D-11（KDS 镜像不同步）、D-12（e2e 无 webServer）、D-13（30 提交未推送 + 并行 WIP）。

## 变更说明（v1.10 → v1.11，2026-10-22 晚）

1. **D-11 关闭**：文档控制/本地 KDS 镜像全量收敛（PR #57，484 文件）；重建后 `document_control --check` 幂等为 0，repository-only 门禁 pass（kds_md 3612）。
2. **CI 恢复**：GPCF 注册 self-hosted runner `mac-mini-gpcf`（launchd 常驻），`repository-checks` 与 `统一规范检查（R01-R20）` 均已跑通；此前 PR #55 曾因无 runner 排队 8 分钟。
3. 终态证据与缺陷台账同步：D-11 改「已关闭」，未执行项仅剩时间窗归档与真实 KDS API 写入。
4. 边界不变：partial、未部署、未提升验收状态。
7. 边界不变：overall_status 保持 **partial**，未 push、未部署、未接真实设备或生产数据，不提升任何验收状态。

## 变更说明（v1.4 → v1.5，2026-10-22 晚）

1. F-038 推进到 **iteration 2**：B5f 气泡层外提（`441f55c`，PanoramaBubbles + bubbleState + 9 例），组件 3955 → **3711 行**；B5 剩余由五大块降为四大块。
2. 运行状态与终态证据刷新为 **136 文件 / 1251 例**（19:21 实测）。
3. 逐处把「领先 30 提交」改为**复测时点快照 + 以 git 实查为准**（19:22 已 34，并行会话仍在提交），避免账实随提交漂移。
4. 边界不变：partial、未 push、未部署。

## 变更说明（v1.6 → v1.7，2026-10-22 晚）

1. 新增「本轮迭代（2026-10-22 晚，待办排序执行）」：决策模型排序 + 7 项待办的执行结果与提交号。
2. 运行状态：全量测试 139 文件 / 1268 例（19:36）；小种子库（160.3MB → 18.9MB，峰值 4.15GB → 0.4–0.5GB）；e2e 已常态化（webServer 自起）。
3. 数据规模补实测：库 2.17GB 中历史归档表 1905.9MB（87.9%）。
4. F-038 → iteration 3（B5g 卡片列外提，组件 3638 行，剩余三大块）；F-024 交付行同步。
5. 缺陷台账：D-1 收敛、D-10 方案+工具就绪（待授权执行）、D-12 已修复、D-13 更新为 40 提交。
6. 边界不变：partial、未 push、未部署。

## 变更说明（v1.7 → v1.8，2026-10-22 晚）

1. **数据压缩执行完毕**（老卢授权）：`data/spaceai.db` 2069.5MB → **160.5MB**；历史归档表 2196 万行外置 `data/archives/`（1984.3MB，manifest 登记）；备份 2069.5MB 保留；BFF 重启 `/healthz` 200；压缩后全量测试通过。
2. 运行状态与终态证据刷新为 **141 文件 / 1279 例**（19:45）；数据规模改为压缩后实测并注明外置/备份路径。
3. F-038 → **iteration 4**：B5h/B5i/B5j（飞翔 / CWME / 控制器）由并行会话提交，**B5 五大块全部外提完成**；剩余 i18n、人工验收与 script 行数目标（2956 行）。
4. 待办排序执行第 6 项（B 数据保留）由「部分」改为「完成」；第 7 项（G 推送）老卢选择**暂缓**，等并行会话收口后一次性推送。
5. D-10 台账改为已执行 + 剩余项（时间索引、窗口归档）；D-13 更新为 43 提交并记录暂缓决定。

## 变更说明（v1.8 → v1.9，2026-10-22 晚）

1. **D-10 时间索引补齐**：`IngestEvent.CreatedAt`、`EXT_ObolObservation.At` 建索引（幂等 DDL 在 `ensureIngestTable` / `ensureObolTables`），4 例查询计划守卫测试；库 160.5MB → 181.3MB（+20.8MB 索引，仍比压缩前 −91%）。
2. 实测：近 1 天查询 Ingest 5–9ms→**0.05ms**、Obol 18–22ms→**0.5–1ms**；`retention-report` 索引体检转为全部通过。
3. 运行状态/终态证据刷新为 **142 文件 / 1283 例**（20:01）；数据规模改为索引后实测。
4. D-10 剩余仅「时间窗归档（待数据变旧）」；D-13 提交数不变（43→44，以 git 实查为准）。

## 变更说明（v1.9 → v1.10，2026-10-22 晚）

1. **推送完成**（老卢「继续」授权）：SpaceAI Platform `main` → 私有远端 `GCSpaceAI`；合并远端 CI 提交 `1bb1715`（self-hosted runner），冲突文件 `.github/workflows/standards.yml` 采用远端方案；远端 HEAD = `070a778`，本地/远端 0/0，未 force push。
2. **提交信息错位修正**：`b9236aa`（内容为时间索引 6 文件，信息误为 pano 外提）在推送前改写为 `e239242`，信息如实描述索引工作；改用 `commit-tree` 改写，未触碰工作区（并行会话 WIP 未受影响）。
3. 运行状态/终态证据刷新为 **143 文件 / 1293 例**（20:09）；D-13 关闭并记录冲突解决与改写过程。
4. GPCF 本仓未推送：本地 `main` 与远端分叉（本地 22 / 远端 137），需专门治理同步，不在本轮范围。
5. 边界：已推送但不部署、不提升验收状态；数据压缩与索引均有备份/证据。
5. 边界不变：partial、未 push、未部署、无数据删除。

## 变更说明（v1.5 → v1.6，2026-10-22 晚）

1. 补建两个 OpenSpec 变更：`spaceai-l4-precision-model`（implemented；真实资产待授权）、`spaceai-panorama-operation-normalization`（in_progress）；均含「三层对齐」段并通过 `validate_change_alignment_sections.py`。
2. 「F-037 / F-038 未建 OpenSpec 变更」治理欠账同日关闭；只补账，不重做工作、不提升验收状态。
3. 终态证据新增 OpenSpec 变更账条目；其余数字与边界不变。

## 变更说明（v1.11 → v1.12，2026-10-22 深夜）

1. **契约/写可靠审计闭环（四轮，全部经决策模型排序 + 老卢逐轮授权）**：
   - 只读审计产出工具 + 证据（`tools/audit/contract-write-audit.mjs`、`.harness/runs/20261022-contract-write-audit/report.md`）；
   - P0 `8a913a0`（`commitDraft` 事务化 + 真值上报）、P1 高价值 11 `a669722`、P1 其余 17 `9506f70`、P2 播种事务化 `d1fc01a`、契约补登记 `5bd911b`；
   - 契约：登记 **288**，显式实现 **226/280 = 80.7%**，仅样例 23（逐条例外）、bridged 31、**未登记 0**；
   - 写可靠：`run()` 吞异常写 63 函数 → **17**（余为启动播种/有意例外/扫描误报）；新增 44 例触发器注入测试。
2. **发布**：Platform PR **#1**（审计 + P0-P2 + 契约 + 并行 pano R 系列，统一规范检查 pass）、PR **#2**（R7f/R7g/R7h + origin 对齐）均已合并；本地/远端 **0/0**（`5e28dad`）。
3. **运行状态**：全仓 **158 文件 / 1447 例**通过、typecheck 0（本轮收尾实测）；审计工具可复跑并已在报告中固化口径。
4. **缺陷台账**：新增 D-14（写可靠缺陷，已修复）、D-15（契约登记滞后，已关闭）。
5. 边界不变：**partial**、未部署、未接真实设备/生产数据、不提升任何验收状态；并行会话 pano 重构 WIP（脏树）不在本轮范围内。

## 变更说明（v1.12 → v1.13，2026-10-24 晚）

1. **L4 精模主线闭环（会话纠偏后 7 轮）**：
   - 真实资产验收入口：`docs/3d/l4-vendor-dataset-spec.md` + `tools/l4/verify-vendor-package.mjs`（pass/needs_human/fail，不宣称精度达标）+ 9 例新测试；
   - 全链路演练：`tools/l4/chain-dryrun.mjs`（生成→验包→导入→校验→切换→回滚，9 步/10 断言 PASS，临时 manifest 不触线上）；
   - **一键验收复跑 PASS**（2026-10-23 09:07）：贴地 0m、切白盒/回切、画面差异 3.28% ≥1%、清单 500→fallback/whitebox、页面错误 0、控制台错误 0、FPS 55.7；证据 `harness/l4-acceptance/2026-10-23T01-07-31-373Z/`；
   - 卡点根因更正：侧栏 DOM 契约变更致测试选择器过期（非 UI 回归）+ `PanoramaDeep.vue` `isFavoLite` 运行时缺陷（随 B5-R2 `d4a2bcc` 修复）+ 引擎就绪时序；证据 `harness/coordination/ui-regression-20261023/`。
2. **e2e 基座恢复**：全量从 14 passed / 11 failed → **18 passed / 7 skipped / 0 failed**（1.3 分钟）；7 条跳过均写明「能力移除/视图合并/外部产物缺失」，未放宽断言；新增菜单映射/命令面板探针。
3. **真实资产路径**：老卢选定「园区既有成果合作」（决策模型 80.3%）；备料包与三份模板已入库，均标注未发送/未签署；公开数据源调研结论为「不满足 L4 精度」。
4. **缺陷台账**：新增 D-16（L4 真实资产缺口，待对外授权）。
5. **发布**：Platform PR #4/#5/#6/#7、GPCF #62/#64/#65/#66 均已合并；两仓本地/远端 0/0；CI 全绿。
6. **运行状态（2026-10-24 实测）**：Platform 全仓 **175 文件 / 1535 例**通过；e2e **18 passed / 7 skipped / 0 failed**；typecheck 0。
7. 边界不变：**partial**、未部署、未接真实资产、不提升任何验收状态；对外联系/发送/签约均未执行。
