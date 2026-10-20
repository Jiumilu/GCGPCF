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
| T1 | 契约可信 | **✅ 完成（验收口径：差异归零或逐条登记例外）**：①静态审计 + `/__contract__` 运行期漂移报告 + mock 兜底可关闭（404/405 边界测试）；②口径纠偏：原「64 条未实现」高估约 2 倍（mock 循环先调 realData）→ 现三分：显式实现 **203/257 (79.0%)**、仅样例 **23**（全部登记原因）、bridged 31、未登记 26；③两批共补 10 个真端点（ServerDateTime / User.Info / KeepAlive / LogOut / Alarm 统计×2 / Asset.Type.Info / PatrolLine.Info / DeviceAccess / AssetInfo.AssetID），全部断言非 mock；④23 条例外分五类（no-data-model 14 / legacy-external 7 / unmapped-model 1 / static-page 1 / unsafe-debug 1），并加**双向一致性断言**防例外表腐化（新增缺口必须登记、已实现必须移除） |
| T2 | 写可靠（117 处 run 调用仅 1 处判返回值；26 个多写函数 0 个事务） | **已完成**：改造 **10 个函数**（advanceOps / transitionLifecycle / ingestPush / saveRule / toggleRule / saveRelation / executePlan / fuseEvents / runObolRound / addLowAltitudeAssets）→ `tx` + `runStrict` + 失败如实返回；新增 **10 项触发器注入写失败测试**（含原子回滚断言），每批均做变异验证。全量 91 文件 / 829 项全过 |
| T3 | 数据治理与保留策略 | **已完成**：CityLink 归档去重（原表改名保留 2196 万行，新表 61,289 + 唯一索引，零删除）→ `/City/Stats` 17,000ms→155ms、聚合 17,020ms→27ms；只读保留报告 + 可复现去重脚本 + 4 项完整性守卫 |
| T4 | 测试基座 | **已完成**：定位城市数据幂等守卫 off-by-one（`> 50000` 而实际恰为 50,000）致每次 createApp 重建 2133 万行；修复后全量 771s→**~20–31s**、createApp 106s→0.3s、r09 143s→1s；`DB_PATH` 惰性可注入；18 个测试已隔离；**连续三轮全绿（87 文件/807 项）** |
| 前端 | SSE 收口 / PanoramaDeep 拆分 / 设计系统 | **SSE 收口 ✅**、**设计系统 ✅**（令牌落地、23 个 `--gc-*` 全部有定义、浏览器实测生效）；**PanoramaDeep 拆分：部分达成**——组件 3351 → **3184 行**，外提 **20 个模块**（新增测试 100+ 项），并补了 **组件级测试**（3 项，经变异验证可捕获「类型与单测都过、运行时崩」的事故）。未达原计划「脚本 <800 行」（当前 2191 行，差 2.7×）；停止依据与建议见主项目 `harness/runs/20261020-final-gate/ASSESSMENT.md` 第六节 |
| 性能 | 无 GPU 环境可用性（SwiftShader） | **✅ 完成**：实测有 GPU 75.2 FPS / SwiftShader **4.8 FPS**；诊断确认瓶颈是**逐帧重绘**而非填充率（隐藏画布 5.5→60 FPS；0.6 分辨率仍只 5.4 FPS）；新增渲染档位判定（软件渲染 → 关阴影/雾/光照/FXAA + 0.6 分辨率 + **按需渲染** + 心跳 requestRender），实测软件渲染 **4.8 → 56.4 FPS（11.75×）**，有 GPU 侧 70.5 FPS 无回归；画面经像素采样验证（16 采样点 16 色）非冻结，21 卡、0 错误 |

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

## 状态与边界

- project_status: registered；overall_status: partial。
- authorization: `user_authorized_onboarding_and_git_2026-10-10`；`user_authorized_single_repo_merge_and_push_2026-10-16`。
- confirmation：业务验收、生产发布**未确认**；不得提升 accepted / integrated / production_ready / customer_accepted。
- 未部署、未接入真实设备或生产数据、未改 schema。

## 已知未修缺陷（台账）

| ID | 问题 | 状态 |
|---|---|---|
| D-1 | 测试临时库不清理致磁盘两次写满；`db.test.ts` 偶发失败（DB_PATH 于 import 期冻结 + worker 模块缓存跨文件存活） | 磁盘部分已治理（运行级根目录 + 主进程 teardown，跨轮零累积）；但**每轮仍实拷贝 17×1.9GB≈32GB**、`db.test.ts` 仍偶发 → 列入 **T4** |
| D-7 | 全量套件偶发单文件失败（2026-10-20 出现 2 次，重跑即绿） | **已定位并修复**：5 轮循环捕获现场，为 `world-axis.test.ts > W1-1 时空检索` **默认 5s 超时**（实测 5004ms），非此前的克隆内容猜测；已给该文件 20 个用例显式 30s 超时（与 ingest-bus 同法）。克隆完整性校验保留（解决另一类问题）。修复后连续三轮全量 99 文件 / 905 项全过 |

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
