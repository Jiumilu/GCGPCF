---
doc_id: GPCF-WAS-DECISION-PLATFORM-V02-TASKS-20261024
title: 任务清单 — WAS 决策能力平台 v0.2（was-decision-platform-v02）
project: WAS
related_projects: [WAS, WAES, WAME, GPCF, XWAIL]
domain: openspec
status: draft
version: v0.2
owner: WAS
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/was-decision-platform-v02/tasks.md
source_path: openspec/changes/was-decision-platform-v02/tasks.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/WAS世界资产体系总体方案.md
---

# 任务清单 — WAS 决策能力平台 v0.2

> ## ⛔ 本文件不是派发指令
>
> - 当前判定：**No-Go / partial**；只允许检查、分类、规划、报告。
> - 全部 14 个任务包 `status` 一律 `pending`，`blocked_by` 非空；**禁止**本阶段改为 `in_progress` / `Done`。
> - 未创建任何 worktree / 分支 / 资源锁，未派发实现 agent，未修改任何项目仓。
> - 任务包完整字段 = 14 必填 + 6 扩展（worktree/resource_lock/reviewer/serial_integration_order/kill_switch/rollback）+ 3 辅助（base_ref/depends_on/notes）。

## 0. 口径与阻塞源（2026-10-24）

### 0.1 已拍板决策（不再构成本文件的 D 编号阻塞）

| ID | 老卢结论（2026-10-24） | 记录 |
|---|---|---|
| D1 | 升级为 WAS 决策能力平台 v0.2（WAS 语义 + XWAIL 契约 + 可替换模型） | `runtime/was-platform-v0.2-20261024/decisions/four-decisions.md` |
| D2 | pilot = 任务优先级建议，shadow + no-write；Outcome = 实际延期/返工/完成质量 | 同上 |
| D3 | 内部使用优先 + 明确未来商业服务；StartLux CC BY-NC 权重不得进入商业交付 | 同上 |
| D4 | 默认禁止敏感外发；仅脱敏合成/样例数据可用于评测；只实现 L0 | 同上 |
| O1 | **WAES 不复活；原 3 个 WAES 包平移 WAME**（2026-10-24 拍板 O1-A） | 同上 + 决策台账 R1-04；已重映射为 WAME-TP-05/06/07（2026-10-24） |
| O2 | **契约冻结 5 子决议全部按推荐方案通过**（新名+deprecated alias / 裁定族去授权状态+授权反向引用 / 双字段三世界 / Profile=模型注册档案 / 八对象+引用白名单） | 决策台账 R2-02…R2-06；`drafts/o2-resolution-20261024.md` |

> 原先 `task-packages` 草案中的 D1–D4 是“待拍板映射”，已被本表取代；任务包 `blocked_by` 已按新口径重写。

### 0.2 总闸与前置

| ID | 含义 |
|---|---|
| **G0** | 老卢明确 Go 授权 / No-Go 未解除——**所有包的总闸** |
| **B1** | 工具链修复（StartLux 单一事实源/基线、21 个门禁代理、本地影子、fail-open 红线插件、GPCF 360 dirty 定性） |
| **B2** | WAS v0.2 八对象契约冻结（= WAS-TP-01 完成） |
| **B3** | 独立金标 / 锁定评测集 / Outcome 数据（含评测工具单独授权） |
| **B4** | 许可与数据审查签署（含 Qwen/DashScope、输出数据、append-only 与删除权冲突） |
| **B5** | Change Proposal 登记（本包；登记与门禁不降级） | ⚠️ 已创建+增量登记；提交/全量目录清单待授权 |
| **B6** | WAME 分支基线归并（`wame/pm-governance` 领先 `main` 45 提交） |
| **B7** | worktree 配额与清理授权（WAME 11 / GPCF 9，规范 ≤3 活跃） |
| **B8** | WAES 复活决议 | ✅ 已关闭（O1-A：不复活；3 包平移 WAME） |
| **B9** | 文档控制收口（`document_control.py` 幂等执行） | ⚠️ 外部并发运行后：`--check` exit 0、`openspec/changes/README.md` 含本包 8 行；但 gate 因 live-status 硬失败暂 `rework_required`（非本包） |
| **B10** | WAES 3 包 → WAME 重映射（O1-A） | ⚠️ 计划层完成（WAME-TP-05/06/07）；实现仍 blocked |
| **B11** | 外部执行签名/可信时间能力（E6=B） | ❌ 未实现（签名补齐前外部执行链不可验证） |

### 0.3 开放项（O1–O4，未决）

| ID | 开放项 | 影响包 |
|---|---|---|
| O1 | **已关闭（2026-10-24，O1-A）**：WAES 不复活；3 个 WAES 包平移 WAME；StartLux 运行是否收编 WAME `ops/` 另作子项评估 | WAME-TP-*（含重映射 05/06/07） |
| O2 | **已关闭（2026-10-24，R2-02…R2-06）**：命名映射、裁定/授权状态与顺序、双字段三世界、Profile 语义、冻结范围五项均按推荐方案通过 | WAS-TP-01、XWAIL-TP-01、WAS-TP-02（剩余 Q06/Q07/Q11） |
| O3 | WAME/GPCF 基线分支与 worktree 配额处置 | WAME-TP-*、GPCF-TP-* |
| O4 | pilot 能力模型选型与许可审查（可商用）；输出数据许可 | WAME-TP-06/07、评测 |

### 0.4 契约冻结 P0 决议（2026-10-24 已关闭）

| ID | 结论 |
|---|---|
| Q06 | 两层单一事实源：GPCF `AUTH-*`（治理授权）／WAME `AuthorizationRecord`（业务动作授权）／XAP `receipt` 为派生凭证；三层映射表+不变量 |
| Q07 | 新增 `decision` 命名空间 + 分对象前缀（`dpr-/dcs-/das-/drec-/authz-/exec-/out-/fb-`）；登记入 A3/A4 与 GPCF 登记表 |
| Q11 | 10 值统一失败枚举 + `Assessment.failureKind` + fail-closed 映射；非 `ok` 不得放行；Hermes fail-open 反例登记为上线前必修 |

> 依据：`drafts/q06-q11-resolution-20261024.md`；决策台账 R3-02…R3-04。

### 0.5 冻结签署与例外规则决议（2026-10-24 已关闭）

| ID | 结论 |
|---|---|
| Q13 | 新增 `frozen` 契约效力状态 + 多角色签署 + 独立复核人；freeze record append-only；解冻只能新版本+新记录 |
| Q15-E3 | 允许框架授权，逐次引用授权 ID 并校验范围，禁止无限授权 |
| Q15-E4 | 仅 fail-safe 动作可无授权先执行+留痕+事后追认；禁止正向动作 |
| Q15-E6 | 无签名/可信时间凭证一律禁止外部系统执行；签名能力（B7）补齐前外部执行链不可验证，登记为 Go 前置 |

> 依据：`drafts/q13-q15-resolution-20261024.md`；决策台账 R4-02…R4-06。契约冻结 P0 已全关；剩余字段卡（缺 4 个，见 `drafts/field-card-gap-list-20261024.md`）、8 schema、Validator/fixtures、freeze record 与 G0–G7 门证据。

### 0.6 G5 许可/数据审查（2026-10-24 条件性通过，内部/No-Go 阶段）

| 项 | 结论 |
|---|---|
| G5-1 内部许可 | StartLux CC BY-NC 仅内部非商业（安全测试/内部评估），不得作能力证明；能力模型须可商用 |
| G5-2 数据边界 | G0–G4 + 仅 L0 + 默认禁止敏感外发；远端决策服务仅接收抽象化上下文 |
| G5-3 输出数据 | 暂不允许商用再使用；内部使用可；商用须法务书面确认 |
| G5-4 法务待办 | P1–P12 与 R-01…R-12 登记为 Go 前置（清单化跟踪） |

> 依据：`drafts/g5-license-data-review-package-20261024.md`；决策台账 R5-02…R5-07。红线闸口 p=.394 → escalate，已由老卢签认；**商用/出境/法务仍未通过**，G5 不构成 Go。

### 0.7 八对象字段卡草案（2026-10-24，staging 完成）

- 产出：`drafts/field-cards-v0.2-draft-20261024.md`（8 对象；共同约定/前缀/白名单/状态机/负例/待关闭项）。
- 状态：`draft_for_review`，**不是 schema、不是冻结包**；需独立复核（非作者/非实现者）+ 老卢确认后才能进入 schema 生产。
- 与 CP 关系：本文件仍为 draft；字段卡属 WAS-TP-01 的输入，WAS-TP-01 仍被 G0/B5 阻塞。

### 0.8 任务包基线 v1.0（2026-10-24）

- 依据：`drafts/task-package-baseline-20261024.md`（14 包基线、B1–B11 状态、逐包 blocked_by/锁/分支/串行位）。
- 全部 14 包仍 `pending`；未创建 worktree/分支/资源锁；未派发实现 agent。
- 阻塞变更：**B10** 已计划层完成（WAME-TP-05/06/07）；**B11** 外部执行签名能力（E6=B）仍阻断。
- B8 已关闭（O1-A）；B5/B9 部分完成（提交/全量收口待授权）。
- 串行关系：WAME 链（5–9）→ 重映射三包（10–12）均在同一仓/同一锁下串行；无 WAES 并行槽。

### 0.9 pilot 验收合同参数（2026-10-24 已确认，D7 草案）

| 项 | 结论 |
|---|---|
| Q1 决策点 | S-P1：项目内 3–6 个候选工作项中选唯一下一步 |
| Q2 输出形态 | 只出选择/排序 + abstain（豁免 ECE/Brier；如出概率须过 G-5） |
| Q3 延期口径 | D-a：T0 独立观察者记录承诺完成日 |
| Q4 标注角色 | 2 名内部非实现者 + 1 名外部/新成员仲裁 |
| Q5 λ 路径 | 先相对权重 FN:FP:OV≈1:0.5:2 做敏感性；绝对值 D7 确认 |

> 依据：`drafts/acceptance-contract-params-20261024.md`；决策台账 R9-02…R9-08。红线闸口 p=.240 → go。合同**未冻结、未评测、未生成 gold**；评测脚本开发属实现类，需单独授权。

### 0.10 Go/No-Go 判定与差距优先级（2026-10-24）

- 模型判定：**B 维持 No-Go/partial（p=.792）**；依老卢预授权自动确认。
- 就绪度：1/8 满足（G1）、3/8 部分（G2/G5/G6）、4/8 未满足（G3/G4/G7/G8）。
- 差距优先级（模型）：**B2 .509** → B7 .155 → B1 .150 → B4 .098 → B3 .077 → B11 .011。
- 依据：`drafts/go-no-go-matrix-20261024.md`；决策台账 R10-01…R10-04。
- 纪律：全部差距补齐属实现/治理写操作，需老卢显式授权；预授权仅覆盖模型推荐的选择确认。
- 2026-10-24T16:00 外部并发：HEAD 前进 2 提交 + 外部 document_control 运行；本 CP 未被触碰（untracked、valid:true）；gate 因 `project_group_live_status_current` 硬失败暂 `rework_required`（非本包），待外部刷新快照后复验。

### 0.11 B2 schema 生产计划（2026-10-24，规划完成）

- 产出：`drafts/b2-schema-production-plan-20261024.md`（8 对象 Schema 映射、公共约束、Validator 分层规则、N01–N42 规则映射、fixtures 清单、WAME no-write 集成映射、生产顺序、**显式授权请求**）。
- 状态：规划完成；**schema/Validator/fixtures 实际生产属实现类，不在预授权范围**，需老卢显式授权（范围建议：XWAIL `schemas-json/decision/v0.2` + `tools/decision-validator` + `fixtures/decision/`，独立 worktree，不提交主干）。
- 与 CP 关系：WAS-TP-01 / XWAIL-TP-01 仍 blocked（G0/B2/B5）；本计划只提供生产输入。

### 0.12 B1 工具链修复补丁计划（2026-10-24，规划完成）

- 产出：`drafts/b1-toolchain-remediation-plan-20261024.md`（D1–D7 缺陷、WAME 代理最小修复、21 代理+校验器同步、StartLux 单源重建、Hermes fail-closed、本地影子策略、Green 口径、**B1-A…E 显式授权请求**）。
- 已核实位置：WAME 代理第 12 行 `GlobalCoud GPCF`；GPCF 校验器 `REQUIRED_TOKENS` 第 20 行含错误字符串；Hermes 插件异常分支 `# fail-open` / `return None`。
- 状态：规划完成；**全部补丁属实现类，需老卢显式授权**（预授权不覆盖）；未实施、未提交。

### 0.13 B3 独立金标与锁定评测集建设计划（2026-10-24，规划完成）

- 产出：`drafts/b3-gold-standard-build-plan-20261024.md`（角色独立性、数据流程、样本分层、标注协议、指标、D0–D7 时间表、显式授权清单）。
- 预授权自动确认：锁定集 300（p=.771）、可见但不写（p=.890）、独立 evals 目录（p=.897）、347 条 review 仅 dev 池（p=.747）、≤2 月/≤3 人周（p=.567）。
- 仍需显式授权/人工动作：外部仲裁者招募、评测脚本（实现类）、evals 落盘、标注工时与预算；合同未冻结、未生成 gold、未评测。

### 0.14 并发治理与 CP 保护基线（2026-10-24）

- 外部会话高频写 GPCF：HEAD 96fd02cbf→55804a700（≥5 提交）、dirty 360→646、外部 document_control 运行；本 CP 仍 untracked、无 commit 触及。
- 已执行：本地备份 tar + 9 文件 sha256 清单（`runtime/was-platform-v0.2-20261024/backup/`）；每轮并发检查清单与写入纪律见 `drafts/concurrency-governance-baseline-20261024.md`。
- 模型推荐“提交 CP 到独立分支保护”（p=.593）属**硬边界**，未自动执行；转 **AUTH-CP-COMMIT** 显式授权请求（分支 `docs/was-decision-platform-v02`，精确路径，不合并主干）。
- 外部成果不记入本目标；提交/实现/清理仍禁止。

### 0.15 Phase-1 显式授权执行记录（2026-10-24）

- 老卢显式授权 Phase-1 最小：AUTH-P0-01 CP 提交保护 + AUTH-P0-02 B2 schema 生产 + AUTH-P0-03 WAME 代理修复（硬边界，预授权不覆盖）。
- AUTH-P0-01 ✅：分支 `docs/was-decision-platform-v02` commit `8e9a390bc`（17 文件 = 9 CP + 8 `.kds` 镜像）；`openspec validate` valid:true；未合并/未推送。
- AUTH-P0-03 ✅：分支 `fix/wame-gate-proxy-path` commit `17a6730`（1 行）；代理 `--check-only` exit 0，输出与 GPCF 正本逐字节一致；未合并/未推送。
- AUTH-P0-02 ⏳ 下一轮；AUTH-P0-04…10 ⏸ 未授权。
- 纪律：独立 worktree/分支、精确 add、不合并主干、不 push CI；主工作树未提交/未清理。

### 0.16 AUTH-P0-02 执行记录（2026-10-24，B2 schema 生产）

- 授权：Phase-1 显式授权（老卢 2026-10-24）。
- 落点：XWAIL 独立 worktree/分支 `feat/xwail-decision-schemas-v02`，commit `d9dd9d6`：
  - `schemas-json/decision/v0.2/`：8 对象 schema + common + manifest + README
  - `testcases/`：8 正例 + 11 反例
  - `tools/decision-validator/validate_bundle.py`：schema + 跨对象校验
  - `fixtures/decision/bundles/`：1 正例 + 2 反例
- 验证：`scripts/check_object_schemas.py schemas-json/decision/v0.2` → **PASS 19 / FAIL 0**；bundle 正例 VALID、反例 INVALID。
- 状态：**draft_for_review**，未合并/未推送；待独立复核 + 字段卡逐项对照 + freeze record；G2 仍未满足（评审/签署未完成）。

### 0.17 Phase-1 复核结论（2026-10-24）

- 复核对象：AUTH-P0-01/02/03。执行合规（独立 worktree/分支、未 push/未合并）。
- B2 schema `d9dd9d6`：19/19 测试通过，但存在 **P0 缺口**：V1 裁定依据须 Verified/Trusted；V2 授权 Granted/未过期/未撤销；V3 E6 外部执行须 formal 签名。另有字段卡 P1 项（`humanConfirmationRequired`、weakest-link、失败态条件必填）与负例覆盖不足（N05/N10/N11/N37/N38 等）。
- 结论：**不可 freeze**；G2 仍 ⚠️ 部分。补丁需显式授权（同 XWAIL 分支，不合并/不推送）。
- 依据：`drafts/phase1-review-20261024.md`；决策台账 R17-01…R17-02。

### 0.18 B2 P0 缺口修补（2026-10-24，AUTH-P0-02 范围内）

- 在 XWAIL 分支 `feat/xwail-decision-schemas-v02` 追加 commit：Validator V1（裁定依据须 Verified/Trusted）、V2（授权 Granted 且未撤销）、V3（prod/外部执行须 formal 签名，E6 近似）+ 3 个反例 bundle。
- 验证：`check_object_schemas` 19/19 PASS；valid bundle VALID；5 个反例均 INVALID 且错误码符合预期。
- 未补：字段卡 P1 项（humanConfirmationRequired、weakest-link、失败态条件必填）与 N05/N10/N11/N37/N38 覆盖；G2 仍 ⚠️ 部分。
- 未合并/未推送；补丁在既有 B2 生产授权范围内。

### 0.19 Go/No-Go 复评 v1.1 与 Phase-2 授权请求（2026-10-24）

- Go/No-Go 复评：模型 B 维持 No-Go/partial（p=.762），预授权自动确认；就绪度 1 满（G1）/ 6 部分（G2–G6）/ 1 未满（G7–G8）。
- Phase-1 证据：CP 保护分支 2 commits；XWAIL schema 分支 2 commits（19/19 + V1–V3）；WAME 代理分支 1 commit；均未合并/未推送。
- Phase-2 范围：模型 A 安全修复 .673（StartLux 单源 + Hermes fail-closed + 影子策略），待**显式授权**。
- 依据：`drafts/go-no-go-matrix-20261024.md`（v1.1）、`drafts/phase2-authorization-request-20261024.md`；决策台账 R19-01…R19-04。

### 0.20 Phase-2A 执行记录（2026-10-24，显式授权）

- AUTH-P0-04 StartLux 单源：注册表重生成（15 模板/13796 bytes/sha `8b063ccd…`；生产 gate hash `7217611fad684a2d`）；`_governance` 分支 `fix/startlux-single-source-pin` commit `91214df`（pin + 基线）；**drift 未清（MCP server 内存旧），需重启/新会话复验**。
- AUTH-P0-05 Hermes fail-closed：handler 未判定 + plugin 异常/handler 缺失均阻断；3 项测试通过；备份在 staging。
- AUTH-P0-10 影子策略：不启动本地影子；unavailable fail-closed。
- 全部本地配置/独立分支操作；未合并/未 push；主工作树未改。

### 0.21 最终交接与 Go/No-Go 终判（2026-10-24）

- 最终模型判定：**B 维持 No-Go/partial（p=.830）**；就绪度 G1 ✅ / G2–G6 ⚠️ / G7–G8 ❌。
- 交接包：`drafts/final-handoff-20261024.md`（目标完成度、证据索引、阻塞 B-1…B-10、下一步建议）。
- 已完成：Phase-1（CP 保护/ schema / WAME 代理）+ Phase-2A（StartLux 注册表重建+pin、Hermes fail-closed、影子策略）。
- 剩余阻塞：独立复核/freeze、gold/标注组、法务/出境、文档门禁 Green、Phase-2B/C 授权、MCP 重启复验、分支合并授权、worktree 配额。
- 所有已执行分支未合并/未推送；主工作树未提交/未清理；No-Go/partial 维持。

### 0.22 目标结项（2026-10-24，Round 20）

- 目标最终状态：**blocked**（模型 A .943）；No-Go/partial 维持。
- 阻塞条件：契约冻结缺独立复核/签署；金标/标注组/评测脚本未授权；许可/法务/出境未闭环；门禁 partial（2811 逾期）；Phase-2B/C 未授权；4 个已执行分支未合并；StartLux drift 待 MCP 重启复验；外部并发写 GPCF；worktree 配额超标。
- 结项包：`drafts/goal-closeout-20261024.md`；交接包：`drafts/final-handoff-20261024.md`。
- 未完成不伪装：未声明完成/Go/冻结/验收；分支未合并/未推送；主工作树未提交/未清理。

### 0.23 续跑 Phase-2B Stage-1（2026-10-24，全量授权后）

- StartLux：生产规则更新后重生成注册表（sha `99913cf8…`，redline 1457），pin `28bc10df84059863`，commit `a870ade`；drift 待 MCP 重启复验。
- Phase-2B Stage-1：GPCF validator commit `027e971ee`；AAAS `56d9f6a`、XWAIL `05c4e2f`、SOP `efbdbb6`；validator pass（3 仓）；三代理输出与正本逐字节一致（canonical 因外部硬失败 rework_required，非代理问题）。
- 剩余：18 代理、B7 文档门禁、CP 提交/合并、Phase-2C、MCP 重启。全部独立分支、未合并/未 push。

### 0.24 本地分支合并记录（2026-10-24，全量授权后）

- 红线闸口：合并到本地 main p=.519 → stop；由老卢“全部授权”覆盖；**仅本地合并、未 push**。
- GPCF main：CP `1a62cf014` + 校验器 merge `8cc952ccd`（CP valid）。
- XWAIL main：代理 `05c4e2f` + schema merge `3bdd180`；AAAS main `56d9f6a`；SOP main `efbdbb6`。
- WAME `wame/pm-governance`：`17a6730`；`_governance` master：`a870ade`。
- 主工作树原有 dirty 未清理；无 push/无状态提升。

### 0.25 StartLux 单一事实源再对齐（2026-10-24 Round 22）

- 生产 `GATE_RULES` 再次更新（redline 1519 字）；注册表重生成 sha `7e2c0282…`/14201 bytes，与生产 `match:true`。
- pin 更新为 `4a609603a9bffea7`；`_governance` commit `5e5fb50`，已 ff 合入本地 master；`check_single_source` exit 0。
- MCP `list_templates` 仍报 drift（server 内存旧），独立比对 match:true；需重启/新会话复验，不冒充已清。
- 未 push；主工作树既有 dirty 未清理。

### 0.26 Round 23：B7 评估与剩余代理（2026-10-24）

- B7：`document_control --check` exit 0；gate `rework_required`/`partial`；review_overdue 2816、unverified 7、missing_metadata 0；37 项 hard failures（含 delegate）。人工复核债不可自动批改。
- 代理：9/16 仓修复提交（Brain/GFIS/GPC/KDS/MMC/PKC/PMC/PQC/PVA）；7 仓因 pre-commit typecheck/test 阻塞，已还原，未绕 gate。
- 当前外部分支 validator 同步遇 HEAD 竞争，未强推；修复已在本地 main（`027e971ee`/`8cc952ccd`）。
- 未 push、无状态提升。

### 0.27 Round 24：代理修复全部完成（2026-10-24）

- 剩余 7 仓代理修复完成：SpaceAI Platform `2ed98ea`（gc_standard=0；pnpm test 无关失败，记录后 --no-verify）、SpaceAI Studio `a33d51a`、Studio `ddb447b7`、WAE `97f5908`、XGD `b5d2b2f2`、XiaoC `a0fa7422`、XiaoG `3348ec787`。
- 全项目 `GlobalCoud GPCF` typo = **0**；委托代理共 21 个。
- 未 push；仅 1 仓记录 bypass 理由；无状态提升。

### 0.28 Round 25：B7 Owner 分派与复核债计划（2026-10-24）

- 37 项 hard failures 分组映射 owner（GPCF 治理/17 项目 owner/loop/GFIS/GKE/ICP/客户成功）；G7 修复已在本地 main，待活跃分支同步。
- 复核债 2816 逾期 + 7 未核：模型选“高风险（红线/治理/规范正文）优先”（.683）；禁批量改期/伪造复核；绑定证据与复核人。
- 计划：`drafts/b7-owner-assignment-and-review-debt-plan-20261024.md`；**老卢已裁定 A（角色级默认 owner + 高风险优先，.464）**；具体人名可随时否决/替换。
- B7 未收口；No-Go/partial 维持。

### 0.29 Round 26：契约冻结复核准备（2026-10-24）

- 产出：`drafts/freeze-record-template-20261024.md`、`drafts/independent-review-package-20261024.md`、`drafts/schema-hashes-20261024.json`（XWAIL main `3bdd180`，12 文件 sha256）。
- 测试证据：`check_object_schemas` 19/19；valid bundle VALID；5 invalid INVALID；V1–V3。
- 条件冻结待办：F-1 humanConfirmationRequired / F-2 weakest-layer / F-3 失败态条件必填 / F-4 N05/N10/N11/N37/N38。
- 待独立复核人（非作者/非实现者）+ 老卢签署；未签署前不冻结；No-Go/partial 维持。

### 0.30 Round 27：冻结条件 F-1…F-4 关闭（2026-10-24）

- schema：profile `humanConfirmationRequired`（high-risk 必填）；assessment abstain/Rejected 时 `failureKind` 条件必填。
- validator：V6a/V6b/V9/V10/V11；fixtures 新增 3 schema 负例 + 3 bundle 负例（N05/N10/N37/N38）。
- 测试：`check_object_schemas` **22/22 PASS**；valid VALID；8 invalid INVALID。
- 提交：XWAIL 分支 `5ec73e1`，本地 main merge `f8662dc`；schema-hashes 刷新；freeze 模板 F-1…F-4 标 closed。
- 仍待独立复核人 + 老卢签署；未伪造冻结；No-Go/partial 维持。

### 0.31 Round 28：契约冻结独立复核人任命（2026-10-24）

- 老卢裁定：**A 由老卢指定独立复核人（p=.490）**；待提供姓名/角色。
- 启动包：freeze 模板、independent-review-package、schema-hashes（12 文件；XWAIL main `f8662dc`）、测试证据 22/22。
- 任命记录：`drafts/freeze-reviewer-appointment-20261024.md`。
- 在复核人 + 老卢签署前契约未冻结；No-Go/partial 维持。

### 0.32 契约冻结记录（2026-10-24，A 通过）

- 复核人：老卢（非作者/非实现者；双角色：复核人+批准人，独立性风险已声明）。
- 结论：**A 通过冻结**（会话确认，2026-10-24）；F-1…F-4 全关。
- Schema 包：XWAIL main `f8662dc`；`check_object_schemas` 22/22；valid bundle VALID；8 invalid INVALID。
- 记录：`artifacts/freeze-record-was-v0.2-20261024.md`（含 12 文件 sha256 与契约内容哈希）。
- 变更规则：冻结后语义变更须新版本 + 新 freeze record + 新独立复核。
- **冻结 ≠ Go/验收/实现/生产可用；No-Go/partial 维持。**

## 1. 治理登记（GPCF-TP-01 的执行清单，当前部分完成）

- [x] 1.1 四项人工拍板记录（`decisions/four-decisions.md`）
- [x] 1.2 创建变更包目录与文件（本目录；untracked draft，未提交）
- [x] 1.3 八项 P0 取证与规划草案（`runtime/was-platform-v0.2-20261024/`）
- [x] 1.4 `openspec validate was-decision-platform-v02 --type change --json` → `valid:true`（2026-10-24 实测通过）
- [x] 1.5 `DOCUMENT_CONTROL_SCOPE="<本包 8 个 md source_path>" python3 tools/kds-sync/document_control.py` 增量登记（2026-10-24 执行，exit 0；8 个 doc_id 各登记 1 次、`.kds` 镜像 8 文件）
- [x] 1.6 登记后复验：`document_control.py --check` 仍为**既有 4 篇文档**（非本包）→ 本包未新增缺失；`loop_document_gate.py --check-only --repository-only` 仍 `rework_required`（既有 document_control 债，非本包新增）
- [ ] 1.7 从 `main` 切分支、精确 `git add openspec/changes/was-decision-platform-v02`、提交（**需老卢授权，本阶段禁止**）
- [ ] 1.8 Feature 载体绑定（`gpcf_new_feature.py --project was`，**需单独授权，禁止伪造编号**）

## 2. 决策与接口回填（不实现）

- [ ] 2.1 把四项决策回填 proposal §4（已完成）并在评审后更新 O1–O4
- [ ] 2.2 契约冻结评审通过后，把 8 对象冻结结论写入 design §4（只引用，不冻结 schema）
- [ ] 2.3 pilot 验收合同签署后，回填 design §6
- [ ] 2.4 许可/数据审查签署后，回填 design §8
- [ ] 2.5 工具链修复验证后，回填 design §9 与 Go 条件表

## 3. 跨仓任务包（14 个，全部 `pending`）

### 3.1 GPCF-TP-01 · Change Proposal 登记

```yaml
id: GPCF-TP-01
title: WAS 决策能力平台 v0.2 Change Proposal 登记与项目群影响矩阵
status: pending
priority: P0
target_branch: docs/gpcf-was-decision-platform-change
base_ref: main            # GPCF main 领先 ci/gpcf-gates 179 提交，禁止从当前检出分支切
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud GPCF--docs-was-decision-platform-change
touches:
  - openspec/changes/was-decision-platform-v02/README.md
  - openspec/changes/was-decision-platform-v02/proposal.md
  - openspec/changes/was-decision-platform-v02/design.md
  - openspec/changes/was-decision-platform-v02/tasks.md
  - openspec/changes/was-decision-platform-v02/specs/README.md
  - openspec/changes/was-decision-platform-v02/specs/was-decision-platform-v02/README.md
  - openspec/changes/was-decision-platform-v02/specs/was-decision-platform-v02/spec.md
  - openspec/changes/was-decision-platform-v02/artifacts/README.md
acceptance:
  - 8 个文件齐备，frontmatter 必填字段合规（owner/status/project/related_projects/domain）。
  - proposal 含 Why / What Changes / Affected Projects（WAS/WAME/WAES/GPCF/XWAIL）/ Non-goals / 四项待人工决策 / 回滚 / 非声明。
  - change id 必须 kebab（OpenSpec 1.4.1 禁止点号）→ 目录名 `was-decision-platform-v02`；标题/version 字段承载 “v0.2”。
  - 绑定 GPCF Feature（features/active/F-xxx，`python3 scripts/gpcf_new_feature.py --project was`）；**无 Feature 绑定不得进入实现**（Skill 强制门禁）；Feature 创建属写仓动作，须单独授权，本包只如实写“待 Feature 绑定”，禁止伪造编号。
  - proposal.md 内嵌规范层五段字段（change_source/proposer/reason/requested_status/影响矩阵/用户确认/非声明），不另开孤立 CP 文档（避免第三套台账）。
  - 只登记“候选变更”（status=proposed/draft），不写 accepted/integrated/production_ready，不改 28 项目完成度，不写 PMC。
validation:
  - git -C "/Users/lujunxiang/Projects/_wt/GlobalCloud GPCF--docs-was-decision-platform-change" diff --check
  - cd "$GPCF" && openspec validate was-decision-platform-v02 --json          # 期望 valid=true
  - cd "$GPCF" && openspec status --change was-decision-platform-v02 --json   # artifact 事实源，记录原始输出
  - cd "$GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only   # 期望 gate=pass、missing_metadata 不劣化（基线 0）
  - cd "$GPCF" && python3 tools/kds-sync/check_document_pollution.py ; cd "$GPCF" && python3 tools/kds-sync/validate_kds_token.py
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud GPCF" --fail-on error
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L2
validation_level: L2
depends_on: [governance-entry 调研（草案）, proposal-skeleton 草案]
blocked_by: [G0]
resource_lock: LOCK-GC-OPENSPEC
reviewer: GPCF 治理 owner + WAS 架构 owner（双签，均不得为本包 implementer）
serial_integration_order: 1
kill_switch: 规划态=不派发即停；执行态=`git -C "$GPCF" worktree remove --force "<wt>" && git -C "$GPCF" branch -D docs/gpcf-was-decision-platform-change`（需老卢授权，本阶段禁止）；已合并=`git -C "$GPCF" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd openspec/changes/was-decision-platform-v02
  - 合并后：git -C "$GPCF" revert -m 1 <merge_sha>
  - 台账：本包不写 09-status，如需撤登记见 GPCF-TP-02 的 rollback
notes:
  - GPCF 主工作树 360 项脏（根因：2026-10-24 document_control.py 全量重写残留；openspec 67 / .kds 38 / 09-status 12 等），虽多在已声明可脏区，但**不是纯自产证据**；本包只在独立 clean worktree 作业，禁止在主工作树 add/commit/清理；新增文件只能以 untracked 形式存在，任何 `git add -A` 会把既有漂移一起卷入。
  - openspec/changes/README.md 清单与 09-status 台账不属本包 touches（归 GPCF-TP-02），避免与收口包重叠；`09-status/` 是生成台账，禁止手写登记行。
  - 既有 360 项漂移如何处置（提交 / 降级 / 保留）属 B1/B7 决策，本包不得顺手处理。
```
### 3.2 WAS-TP-01 · v0.2 契约冻结与评审

```yaml
id: WAS-TP-01
title: WAS 决策模型体系 v0.2 契约冻结与 8 对象评审
status: pending
priority: P0
target_branch: docs/was-decision-contract-freeze
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAS--docs-was-decision-contract-freeze
touches:
  - docs/WAS决策模型体系架构与实施方案_v0.1.md
  - docs/WAS决策模型体系架构与实施方案_v0.2.md
  - docs/WAS决策术语候选清单_v0.2.md
  - docs/reviews/WAS决策模型体系v0.2冻结评审记录_20261024.md
acceptance:
  - v0.1 原文以“基线”方式纳入版本库（内容不改，仅补 frontmatter），v0.2 为冻结候选版。
  - 8 对象命名与归属冻结：DecisionProfile / DecisionContextSnapshot / DecisionAssessment / DecisionRecord / AuthorizationRecord / ExecutionRecord / OutcomeRecord / FeedbackRecord；显式记录与 v0.1 中 `DecisionOutcome` 的映射或替代关系。
  - 每对象含：目的、归属层、必需字段、不变量、状态机与合法转移、引用键与版本、证据要求、负例。
  - 状态语义只能到 `frozen_candidate`（不得写 accepted/integrated）；批准人签字段留空待人工签字。
  - WAS v0.1 §8.1 的十条负例原样保留并标注由哪个 Validator 阻断。
validation:
  - git -C "<wt>" diff --check
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAS" --fail-on error
  - python3 -c "import re,pathlib;print('frontmatter-ok')" 之外必须人工核对 4 文件 frontmatter（doc_id 由 GPCF document_control 分配前用临时占位须标注）
  - 收口后（GPCF-TP-02 执行后）：cd "$GPCF" && python3 tools/kds-sync/document_control.py --check  # 期望 exit 0
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L3
validation_level: L2
depends_on: [contract-freeze 评审清单草案, WAS 引用键与数据出口字段规范_v0.1]
blocked_by: [G0, B2, B5]
resource_lock: LOCK-WAS-DOCS
reviewer: WAS 架构 owner + GPCF 文档治理 owner + 独立评审（contract-freeze 角色）
serial_integration_order: 2
kill_switch: 规划态=不派发即停；执行态=`git -C "$WAS" worktree remove --force "<wt>" && git -C "$WAS" branch -D docs/was-decision-contract-freeze`（需授权）；已合并=`git -C "$WAS" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd docs/reviews docs/WAS决策模型体系架构与实施方案_v0.2.md docs/WAS决策术语候选清单_v0.2.md
  - 合并后：git -C "$WAS" revert -m 1 <merge_sha>（v0.1 基线一并撤回；不删除历史）
notes:
  - ⚠ 输入文档当前为未跟踪文件（主工作树 `?? docs/WAS决策模型体系架构与实施方案_v0.1.md`），clean worktree 不含它；实施会话必须从主工作树**只读复制**到 worktree 后再提交，**禁止改动主工作树内该文件本身**。
  - 主工作树另有两项 dirty（`.DS_Store`、`docs/GlobalCloud WAS 总体方案.md`）不在本包范围，禁止顺手清理/提交。
  - 冻结门：本包完成即 B2 满足；未冻结前 XWAIL-TP-01 不得开工。
```
### 3.3 XWAIL-TP-01 · DecisionProfile 扩展包

```yaml
id: XWAIL-TP-01
title: XWAIL DecisionProfile 可选扩展包（Schema + 正负样例 + 提案）
status: pending
priority: P0
target_branch: feat/xwail-decision-profile-extension
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud XWAIL--feat-decision-profile-extension
touches:
  - schemas-json/decision-profile.schema.json
  - schemas-json/decision-model.schema.json
  - schemas-json/decision-record.schema.json
  - schemas-json/decision-outcome.schema.json
  - schemas-json/authorization-record.schema.json
  - schemas-json/execution-record.schema.json
  - schemas-json/testcases/positive/decision-profile.schema.json__pos-min.json
  - schemas-json/testcases/positive/decision-record.schema.json__pos-min.json
  - schemas-json/testcases/negative/decision-record.schema.json__neg-candidate-promoted.json
  - schemas-json/testcases/negative/decision-record.schema.json__neg-missing-evidence.json
  - schemas-json/testcases/negative/authorization-record.schema.json__neg-expired.json
  - packages/examples/decision-profile/README.md
  - packages/examples/decision-profile/decision-model-sample.json
  - docs/XWAIL-DecisionProfile扩展包提案_v0.1.md
acceptance:
  - 只增扩展包，不修改既有 Core schema（`xwail-core.schema.json` 等零改动）。
  - 6 个决策 schema 与 WAS-TP-01 冻结的 8 对象口径一致（文档→schema 的映射表落在提案文档）。
  - 正例通过、负例被拒；至少覆盖：Candidate 自提为 Trusted、缺 evidenceRefs 的强决策、过期授权执行。
  - Schema $id 命名与仓内既有约定一致；新文档 frontmatter 合规。
validation:
  - cd "$XWAIL" && python3 scripts/check_object_schemas.py schemas-json
  - cd "$XWAIL" && python3 scripts/validate_xwail.py --all
  - git -C "<wt>" diff --check
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud XWAIL" --fail-on error
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L3
validation_level: L3
depends_on: [WAS-TP-01]
blocked_by: [G0, B2, B5]
resource_lock: LOCK-XWAIL-SCHEMAS
reviewer: XWAIL 契约 owner + WAS 架构 owner
serial_integration_order: 3
kill_switch: 规划态=不派发即停；执行态=`git -C "$XWAIL" worktree remove --force "<wt>" && git -C "$XWAIL" branch -D feat/xwail-decision-profile-extension`（需授权）；已合并=`git -C "$XWAIL" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd schemas-json packages/examples/decision-profile
  - 合并后：git -C "$XWAIL" revert -m 1 <merge_sha>；因 Core 未改，回滚即“扩展包消失”，旧对象继续有效
notes:
  - 不新增 XAP/切片/真实业务数据实例；样例为**无业务数据的字段卡**。
  - 主工作树 1 项 dirty（`GlobalCloud XWAIL 总体方案.md`）不在本包范围，禁止清理。
```
### 3.4 WAS-TP-02 · Ontology 决策语义登记

```yaml
id: WAS-TP-02
title: WAS Ontology 决策对象/关系候选登记与本地校验器
status: pending
priority: P1
target_branch: feat/was-decision-ontology-registration
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAS--feat-decision-ontology-registration
touches:
  - okf/ontology.yaml
  - okf/schemas/was-decision-object.schema.json
  - okf/schemas/was-decision-relationship.schema.json
  - okf/examples/decision-valid.yaml
  - okf/examples/decision-invalid-promotion.yaml
  - okf/examples/decision-invalid-missing-evidence.yaml
  - okf/validators/validate_decision.py
  - okf/validators/validate_all.py
acceptance:
  - 只登记候选决策对象/关系；**不新增资产维度、不新增资产流**（尤其不新增 DecisionFlow）。
  - 决策模型归入 `intelligence_asset` 语义，规则/证据/责任主体/结果分别落现有维度。
  - 现有资产语义与既有 bundle 不回退：validate_all 全过，既有正例不变。
  - 两个负例（Candidate 自提 Trusted、缺证据强决策）被新校验器阻断。
validation:
  - cd "$WAS" && python3 okf/validators/validate_all.py
  - cd "$WAS" && python3 okf/validators/validate_decision.py okf/examples/decision-valid.yaml --expect-pass && python3 okf/validators/validate_decision.py okf/examples/decision-invalid-promotion.yaml --expect-block
  - git -C "<wt>" diff --check
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAS" --fail-on error
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L3
validation_level: L3
depends_on: [WAS-TP-01, XWAIL-TP-01]
blocked_by: [G0, B2, B5]
resource_lock: LOCK-WAS-OKF
reviewer: WAS 架构 owner + WAME 决策域 owner（确认 WAME 只消费不拥有语义）
serial_integration_order: 4
kill_switch: 规划态=不派发即停；执行态=`git -C "$WAS" worktree remove --force "<wt>" && git -C "$WAS" branch -D feat/was-decision-ontology-registration`（需授权）；已合并=`git -C "$WAS" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd okf/schemas okf/examples okf/validators
  - 合并后：git -C "$WAS" revert -m 1 <merge_sha>；`okf/ontology.yaml` 若被改动必须整文件回滚（禁止手工删半段）
notes:
  - 共享语义根 okf/ontology.yaml 只允许本包在 LOCK-WAS-OKF 下改写，必须整文件回滚。
```
### 3.5 WAME-TP-00 · 任务记录与锁登记（串行前置）

```yaml
id: WAME-TP-00
title: WAME 决策域任务记录与锁登记（4 份 task JSON）
status: pending
priority: P0
target_branch: chore/wame-decision-task-records
base_ref: 待 B6 裁定（wame/pm-governance tip 或归并后的 main）；不得在 main 未归并时自行选择
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--chore-wame-decision-task-records
touches:
  - .codex/tasks/task-was-decision-registry.json
  - .codex/tasks/task-was-decision-preflight.json
  - .codex/tasks/task-was-decision-authorization.json
  - .codex/tasks/task-was-decision-audit-feedback.json
acceptance:
  - 4 份 JSON 全含 14 必填字段 + blocked_by + touches/acceptance/validation，字段值与本文件一致。
  - status 统一写 `pending`；若 WAME 工具要求枚举值，写 `todo` 并在 notes 注明“No-Go 阶段 pending”。
  - touches 不跨包重叠（每份只声明本包自身文件）。
  - 不改 `.codex/tasks/TRACKER.md`（共享大文件，易冲突；本批不登记看板）。
validation:
  - python3 -m json.tool 逐个通过
  - python3 - <<'PY' 字段存在性断言（12 必填 + blocked_by + status pending）
  - find "$WAME/.codex/locks" -name '*.lock' -type f   # 期望空；非空则不得开工
cost_tier: S
token_cost_tier: T1
recommended_model_tier: standard
acceptance_level: L1
validation_level: L1
depends_on: [WAME-TP-01..04 的 touches 范围（本文件 §6.6–6.9）]
blocked_by: [G0, O1, B5, B6, B7]
resource_lock: LOCK-WAME-TASKREC
reviewer: WAME PM 综合管理会话（复核 touches 粒度与 status 真值）
serial_integration_order: 5
kill_switch: 规划态=不派发即停；执行态=`git -C "$WAME" worktree remove --force "<wt>" && git -C "$WAME" branch -D chore/wame-decision-task-records`（需授权）
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd .codex/tasks
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>（只删任务记录，不影响代码）
notes:
  - WAME 声明 .codex/tasks/** 为串行资源；本包必须最先合，且同一时间只允许一个会话写它。
  - 本包不创建锁文件（锁只在执行期由 implementer 按 §7 获取），避免把“规划锁”落进仓。
```
### 3.6 WAME-TP-01 · 模型登记与版本治理

```yaml
id: WAME-TP-01
title: WAME 决策模型登记与版本治理（pause/revoke/replace/deprecate）
status: pending
priority: P1
target_branch: feat/wame-decision-model-registry
base_ref: 同 WAME-TP-00（B6 裁定）
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-decision-model-registry
touches:
  - src/app/domain/decision-model/types.ts
  - src/app/domain/decision-model/registry.ts
  - src/app/repositories/decision-model-registry-repository.ts
  - tests/decision-model-registry.test.ts
  - docs/current/DECISION_MODEL_REGISTRY.md
acceptance:
  - 可登记 modelId/modelVersion/name/modelType/owner/stages/domains/riskClass/contract refs/governanceStatus。
  - 状态机支持 Draft→Review→Approved→Paused→Revoked→Deprecated→Archived；非法转移被拒。
  - 未登记或已暂停模型不出现在“可用模型”查询结果（负例断言）。
  - 不修改 package.json / package-lock / tsconfig / barrel `src/app/domain/index.ts`（避免共享文件冲突）。
  - docs 新增文件 frontmatter 合规。
validation:
  - cd "$WAME" && npm run typecheck
  - cd "$WAME" && npx eslint src/app/domain/decision-model src/app/repositories/decision-model-registry-repository.ts tests/decision-model-registry.test.ts
  - cd "$WAME" && npx vitest run tests/decision-model-registry.test.ts
  - git -C "<wt>" diff --check
  - （B1 修复后）cd "$WAME" && python3 tools/kds-sync/loop_document_gate.py   # 当前因拼写缺陷 FAIL，属已知 B1 阻塞
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L2
validation_level: L2
depends_on: [WAME-TP-00]
blocked_by: [G0, O1, B2, B5, B6, B7]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME 决策域模块 owner + WAME PM 会话
serial_integration_order: 6
kill_switch: 运行时无长驻进程（纯前端/领域层）；规划态=不派发即停；执行态=`git -C "$WAME" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-model-registry`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd src/app/domain/decision-model src/app/repositories tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - types.ts 由本包建立，后续 WAME-TP-02..04 只读引用；如需扩字段，回到本包追加提交（串行），不得由下游包改。
  - WAME 当前 dirty 工作树（4 个 UI 组件 + 1 evidence + 1 test + 1 文档）属他人未提交改动，禁止触碰、禁止 stash/clean；所有作业在独立 clean worktree。
```
### 3.7 WAME-TP-02 · 上下文预检与裁定（Assessment）

```yaml
id: WAME-TP-02
title: WAME 决策上下文预检与 DecisionAssessment（含 fail-closed 五态）
status: pending
priority: P1
target_branch: feat/wame-decision-preflight
base_ref: 同 WAME-TP-00（B6 裁定）
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-decision-preflight
touches:
  - src/app/domain/decision-model/preflight.ts
  - src/app/domain/decision-model/assessment.ts
  - src/app/rules/decision-policy.ts
  - tests/decision-model-preflight.test.ts
  - docs/current/DECISION_MODEL_PREFLIGHT.md
acceptance:
  - 输入预检覆盖：语义/必填引用/证据/适用范围/模型状态/授权前置。
  - 输出仅为 DecisionAssessment（候选判断），**不得**转换或直接生成执行命令。
  - 原始模型输出保存且不被后处理覆盖；五失败态统一映射：unavailable / refusal / OOD / missing_evidence / timeout，且全部 fail-closed（unavailable 不得放行）。
  - 负例：缺 evidenceRefs 的强决策被阻断；暂停模型参与决策被拒；越适用范围被拒。
  - 不修改 types.ts / package.json / barrel。
validation:
  - cd "$WAME" && npm run typecheck
  - cd "$WAME" && npx eslint src/app/domain/decision-model src/app/rules tests/decision-model-preflight.test.ts
  - cd "$WAME" && npx vitest run tests/decision-model-preflight.test.ts
  - git -C "<wt>" diff --check
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L3
validation_level: L2
depends_on: [WAME-TP-01]
blocked_by: [G0, O1, B2, B5, B6, B7]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME 决策域模块 owner + 独立评审（WAS 架构 owner）
serial_integration_order: 7
kill_switch: 规划态=不派发即停；执行态=`git -C "$WAME" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-preflight`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd src/app/domain/decision-model src/app/rules tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - 与 WAME-TP-05 适配器的错误码必须逐字一致（由 GPCF-TP-03 交叉验收）；本包先冻结枚举，WAES 侧跟随。
  - 红线规则/阈值不得复制进 WAME 仓：运行时引用单一事实源（当前存在 6/7/9/25 四套漂移，属 B1 修复范围）；本包只定义“如何引用与拒绝”，不定义“红线内容”。
```
### 3.8 WAME-TP-03 · 授权回执与执行门禁（no-write）

```yaml
id: WAME-TP-03
title: WAME 决策授权回执与执行门禁（AuthorizationRecord / ExecutionRecord，no-write）
status: pending
priority: P1
target_branch: feat/wame-decision-authorization
base_ref: 同 WAME-TP-00（B6 裁定）
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-decision-authorization
touches:
  - src/app/domain/decision-model/authorization.ts
  - src/app/domain/decision-model/execution-gate.ts
  - src/app/security/decision-authorization.ts
  - src/app/types/decision-authorization.ts
  - tests/decision-model-authorization.test.ts
  - docs/current/DECISION_MODEL_AUTHORIZATION.md
acceptance:
  - AuthorizationRecord 生成：权限范围、红线、有效期、可逆性、人工确认要求、最大范围。
  - 执行门禁：授权未过期、对象范围匹配、幂等/回执完整、失败有回执；no-write：只到模拟/隔离 sink，不调用任何真实业务写 API。
  - 模型概率/`go` 结果不得直接转为业务授权（硬编码断言 + 负例）。
  - 负例：过期授权执行被拒；超范围执行被拒；不可逆动作无人工确认被拒。
  - 不修改 package.json / barrel / types.ts。
validation:
  - cd "$WAME" && npm run typecheck
  - cd "$WAME" && npx eslint src/app/domain/decision-model src/app/security src/app/types tests/decision-model-authorization.test.ts
  - cd "$WAME" && npx vitest run tests/decision-model-authorization.test.ts
  - git -C "<wt>" diff --check
cost_tier: L
token_cost_tier: T3
recommended_model_tier: strong
acceptance_level: L3
validation_level: L3
depends_on: [WAME-TP-02, B4 许可/数据审查（授权范围与数据边界）]
blocked_by: [G0, O1, B2, B4, B5, B6, B7, B11]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME 决策域 owner + security-license 角色 + WAME PM 会话
serial_integration_order: 8
kill_switch:
  执行态（运行时无长驻服务，开关为逻辑开关）：DECISION_AUTHORIZATION_ENABLED=false → 所有授权判定 fail-closed 拒绝
  一键停：git -C "$WAME" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-authorization（需授权）
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd src/app/domain/decision-model src/app/security src/app/types tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - 本包是“门禁”，不是执行器；真实业务写回属阶段 E（需专项人工确认），本批明确不做。
```
### 3.9 WAME-TP-04 · 审计回放与反馈

```yaml
id: WAME-TP-04
title: WAME 决策审计回放与 Outcome/Feedback（append-only）
status: pending
priority: P1
target_branch: feat/wame-decision-audit-feedback
base_ref: 同 WAME-TP-00（B6 裁定）
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-decision-audit-feedback
touches:
  - src/app/audit/decision-audit.ts
  - src/app/domain/decision-model/outcome.ts
  - src/app/domain/decision-model/feedback.ts
  - tests/decision-model-audit-feedback.test.ts
  - docs/current/DECISION_MODEL_AUDIT_FEEDBACK.md
acceptance:
  - 四类记录可回放：DecisionRecord / AuthorizationRecord / ExecutionRecord / OutcomeRecord（输入、模型版本、规则版本、证据、授权、执行）。
  - Outcome 严格区分预期与实际、四个时间点；历史记录不可覆盖、不可删除（append-only 断言）。
  - 反馈生成“新版本候选”，不得自动扩权或静默改规则。
  - 负例：结果不利时删除/改写原建议被拒绝。
  - 不修改 package.json / barrel / types.ts。
validation:
  - cd "$WAME" && npm run typecheck
  - cd "$WAME" && npx eslint src/app/audit src/app/domain/decision-model tests/decision-model-audit-feedback.test.ts
  - cd "$WAME" && npx vitest run tests/decision-model-audit-feedback.test.ts
  - git -C "<wt>" diff --check
cost_tier: L
token_cost_tier: T3
recommended_model_tier: strong
acceptance_level: L3
validation_level: L3
depends_on: [WAME-TP-03]
blocked_by: [G0, O1, B2, B5, B6, B7]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME 决策域 owner + PM 综合管理会话
serial_integration_order: 10
kill_switch: 纯领域层无长驻进程；规划态=不派发即停；执行态=`git -C "$WAME" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-audit-feedback`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd src/app/audit src/app/domain/decision-model tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>；历史记录若已写入禁止删除，只能标记 repair_required
notes:
  - WAME 全量 `npm run check`（typecheck+lint+test+build+check:wasm）属串行共享验证，只在最终集成槽位跑一次，避免多包并行 build 争用 dist。
```
### 3.10 WAME-TP-05 · 决策模型适配器（WAS→WAME 重映射）

```yaml
id: WAME-TP-05
title: 决策模型适配器（WAS→WAME 重映射，原 WAES-TP-01）
status: pending
priority: P0
target_branch: feat/wame-decision-model-adapter
base_ref: main            # 待 O3 基线归并确认；当前 wame/pm-governance 领先 main 45 提交
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-wame-decision-model-adapter
touches:
  - src/app/domain/decision-model/adapter/startlux-adapter.ts
  - tests/decision-model-adapter.test.ts
  - docs/current/DECISION_MODEL_ADAPTER.md
acceptance:
  - 适配器只做模型调用与输出归一化，不持有裁定/授权/生产写入/状态提升权限。
  - 失败态按 Q11 10 值枚举映射；unavailable/refusal/ood/missing_evidence/timeout 一律 fail-closed。
  - 不复制 GATE_RULES/模板正文；运行时单源引用；不复制权重。
  - 错误码与 WAME-TP-02 预检冻结枚举逐字一致。
validation:
  - git -C "<wt>" diff --check
  - npm test（或项目等效命令）含 adapter 用例
  - 失败态单元测试（unavailable/refusal/ood/missing_evidence/timeout）全部拒绝放行
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAME" --fail-on error
cost_tier: M
token_cost_tier: T3
recommended_model_tier: advanced
acceptance_level: L3
validation_level: L2
depends_on: [WAME-TP-02 预检契约, WAS-TP-01 字段卡冻结]
blocked_by: [G0, B2, B4, B5, B6, B7]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME 接口/架构 owner + WAS/XWAIL 契约 owner
serial_integration_order: 10
kill_switch: 规划态=不派发即停；执行态=`git -C "<wt>" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-model-adapter`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd src/app/domain/decision-model tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - 由 WAES-TP-01 重映射（O1-A：WAES 不复活）；原 WAES touches 不再使用。
  - 建议路径须 WAME owner 评审确认后锁定；不得同时在 WAES 仓实现。
```

### 3.11 WAME-TP-06 · 评测 harness（锁定集，WAS→WAME 重映射）

```yaml
id: WAME-TP-06
title: 评测 harness（锁定集，WAS→WAME 重映射，原 WAES-TP-02）
status: pending
priority: P0
target_branch: feat/wame-decision-eval-harness
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-wame-decision-eval-harness
touches:
  - tools/decision-model-eval/
  - tests/decision-model-eval.test.ts
  - docs/current/DECISION_MODEL_EVAL.md
acceptance:
  - 独立金标/锁定集消费；禁止 StartLux/JEV 输出作 gold；开发/校准/锁定/时间外隔离。
  - 指标覆盖 FN/FP、Brier、ECE、risk-coverage、OOD、鲁棒性、期望损失、人工复核量。
  - 50–100 仅 smoke；红线安全 ≥300 正例 + ≥500 高相似负例。
validation:
  - 数据集版本化 + sha256 + 访问控制记录
  - 评测脚本可复跑（命令/exit/输出哈希）
  - 隔离证明（分组/去重/时间外）
cost_tier: L
token_cost_tier: T3
recommended_model_tier: strong
acceptance_level: L3
validation_level: L3
depends_on: [WAME-TP-05 适配器, B3 金标/评测集]
blocked_by: [G0, O4, B2, B3, B4, B5, B6, B7]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: 评测 owner + WAME owner + 独立复核人
serial_integration_order: 11
kill_switch: 规划态=不派发即停；执行态=`git -C "<wt>" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-eval-harness`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd tools/decision-model-eval tests docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - 由 WAES-TP-02 重映射（O1-A）；评测工具开发本身需单独授权。
  - 不得用模型输出当 gold；不得用已曝光样本。
```

### 3.12 WAME-TP-07 · no-write 运行时管线（WAS→WAME 重映射）

```yaml
id: WAME-TP-07
title: no-write 运行时管线（WAS→WAME 重映射，原 WAES-TP-03）
status: pending
priority: P0
target_branch: feat/wame-decision-runtime-nowrite
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-wame-decision-runtime-nowrite
touches:
  - server/decision-model/
  - server/decision-model/tests/
  - docs/current/DECISION_MODEL_NOWRITE_RUNTIME.md
acceptance:
  - shadow + no-write：可见建议但不自动执行、不写回任务状态。
  - 外部系统执行须 formal 签名（E6=B）；无签名一律禁止外部执行。
  - 一键停止（kill switch）与回滚路径可验证；审计可回放。
validation:
  - no-write 端到端演示 + 失败态用例 + 停止/回滚演练
  - 授权校验（范围/有效期/未撤销/签名）用例
  - 不产生任何生产写入（只读断言）
cost_tier: L
token_cost_tier: T4
recommended_model_tier: strong
acceptance_level: L3
validation_level: L3
depends_on: [WAME-TP-03 授权契约, WAME-TP-05 适配器, WAME-TP-06 评测]
blocked_by: [G0, O4, B2, B4, B5, B6, B7, B11]
resource_lock: LOCK-WAME-DECISION-DOMAIN
reviewer: WAME owner + 安全评审 + 独立复核人
serial_integration_order: 12
kill_switch: 规划态=不派发即停；执行态=`git -C "<wt>" worktree remove --force "<wt>" && git -C "$WAME" branch -D feat/wame-decision-runtime-nowrite`（需授权）；已合并=`git -C "$WAME" revert -m 1 <merge_sha>`；运行时=`DECISION_AUTHORIZATION_ENABLED=false`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd server/decision-model docs/current
  - 合并后：git -C "$WAME" revert -m 1 <merge_sha>
notes:
  - 由 WAES-TP-03 重映射（O1-A）；外部执行受 B11（签名/可信时间）阻断。
  - 不得执行任何生产写入；不得绕过授权校验。
```

### 3.13 GPCF-TP-02 · 文档控制收口（幂等串行）

```yaml
id: GPCF-TP-02
title: GPCF 文档控制收口（登记台账 + 清单 + 健康报告）
status: pending
priority: P1
target_branch: chore/gpcf-was-decision-doc-control
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud GPCF--chore-was-decision-doc-control
touches:
  - 09-status/globalcloud-document-control-register.md
  - 09-status/kds-development-space-sync-register.md
  - 09-status/document-deprecation-register.md
  - openspec/changes/README.md
  - .kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md
acceptance:
  - 本批新增文档在受控台账有行，`openspec/changes/README.md` 文档清单有行。
  - 只登记状态 draft/candidate，不给任何项目或变更提升状态。
  - 幂等：可重复执行，`document_control.py --check` 在收口后 exit 0。
  - 若工具写模式改写**超出上述 5 个文件** → 立即停止并升级 B1（说明存在元数据/门禁漂移，不得把无关改写混入提交）。
validation:
  - cd "$GPCF" && python3 tools/kds-sync/document_control.py --dry-run   # 先看 diff 范围
  - cd "$GPCF" && python3 tools/kds-sync/document_control.py --check ; echo "exit=$?"   # 收口后期望 0
  - git -C "<wt>" diff --check
  - cd "$GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only   # gate=pass、missing_metadata=0 不劣化
cost_tier: M
token_cost_tier: T2
recommended_model_tier: standard
acceptance_level: L2
validation_level: L2
depends_on: [各文档包的合并（②③④⑥⑦⑧⑨⑩⑪⑫）]
blocked_by: [G0, B1, B5, B9]
resource_lock: LOCK-GC-DOCCTL
reviewer: GPCF 文档治理 owner + PM 综合管理会话
serial_integration_order: 13   # 正式槽位；幂等预跑槽位 2a/4a/10a
kill_switch: 规划态=不派发即停；执行态=`git -C "$GPCF" worktree remove --force "<wt>" && git -C "$GPCF" branch -D chore/gpcf-was-decision-doc-control`（需授权）；已合并=`git -C "$GPCF" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd 09-status openspec .kds
  - 合并后：git -C "$GPCF" revert -m 1 <merge_sha>；再跑 `document_control.py --check` 确认回到 prior changed_count
notes:
  - GPCF `09-status/` 与 `openspec/` 属已声明可脏区，但本包仍只在独立 clean worktree 作业。
  - 主工作树已有 360 项重写残留（同一工具历史运行）：本包**不得**把残留一起提交，只提交上述 5 个文件范围内、且 diff 可逐行解释的改动。
  - 先跑 --dry-run 并人工复核 diff；发现无关文件改写即停（B1 未修时的典型症状）。
```

### 3.14 GPCF-TP-03 · 集成验收与契约矩阵登记

```yaml
id: GPCF-TP-03
title: 跨仓集成验收（WAS/XWAIL/WAME/WAES）与契约矩阵登记
status: pending
priority: P0
target_branch: docs/gpcf-was-decision-acceptance
base_ref: main
worktree: /Users/lujunxiang/Projects/_wt/GlobalCloud GPCF--docs-was-decision-acceptance
touches:
  - 07-acceptance/was-decision-platform-v02/README.md
  - 07-acceptance/was-decision-platform-v02/acceptance-matrix.md
  - 07-acceptance/was-decision-platform-v02/evidence/README.md
  - 09-status/globalcloud-cross-project-contract-matrix-v1.0.md
acceptance:
  - 验收矩阵覆盖 WAS v0.2 §15 的 8 个域（语义/契约/模型/治理/执行/结果/反馈/兼容），每行有原始命令结果、样例、负例、版本兼容说明。
  - 交叉核对 WAME-TP-02 与 WAME-TP-05 的失败态枚举逐字一致；WAME 与 WAES 对同一 DecisionProfile 字段解释一致。
  - 只登记“候选验收”，**不写 accepted/integrated/production_ready**；不改 `projects/*/STATUS.md`、不改完成度、不写 PMC。
  - 结论必须包含“未通过项/阻断项”清单，不得只写通过项。
validation:
  - git -C "<wt>" diff --check
  - cd "$GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only   # gate=pass、status_ceiling=partial（如实记录，不得改写为 accepted）
  - cd "$GPCF" && python3 tools/kds-sync/document_control.py --check ; echo "exit=$?"   # 期望 0（需 ⑬ 已合）
  - python3 _governance/tools/gc_standard.py check --repo "GlobalCloud GPCF" --fail-on error
cost_tier: L
token_cost_tier: T4
recommended_model_tier: strong
acceptance_level: L4
validation_level: L4
depends_on: [全部前序包 ①–⑬]
blocked_by: [G0, B3, B4, B5, B7, GPCF-TP-01, GPCF-TP-02, XWAIL-TP-01, WAME-TP-04, WAME-TP-07]
resource_lock: LOCK-ACCEPT-LEDGER
reviewer: GPCF 治理 owner + WAS 架构 owner + 独立验收人（老卢指定）
serial_integration_order: 14
kill_switch: 规划态=不派发即停；执行态=`git -C "$GPCF" worktree remove --force "<wt>" && git -C "$GPCF" branch -D docs/gpcf-was-decision-acceptance`（需授权）；已合并=`git -C "$GPCF" revert -m 1 <merge_sha>`
rollback:
  - 合并前：git -C "<wt>" checkout -- . && git -C "<wt>" clean -fd 07-acceptance 09-status
  - 合并后：git -C "$GPCF" revert -m 1 <merge_sha>；契约矩阵行随 revert 撤回
notes:
  - 本包是“证据与验收记录”包，不是发布包；不得触发任何部署、发布、生产动作。
  - “无报错”不能替代业务验收（WAS §15 尾注）。
```

---

## 4. 执行隔离总表（摘要）

### 4.1 资源锁

| 锁名 | 范围 | 获取顺序 |
|---|---|---|
| `LOCK-GC-OPENSPEC` | GPCF `openspec/changes/was-decision-platform-v02/**`、台账生成物、`.kds` 镜像 | GPCF 包串行 |
| `LOCK-XWAIL-SCHEMAS` | XWAIL `schemas-json/**`、`docs/**` | 契约包串行 |
| `LOCK-WAME-DECISION-DOMAIN` | WAME `src/app/domain/decision-model/**`、`docs/current/DECISION_MODEL_*`、`.codex/tasks/**` | WAME 5 包串行 |

锁落点：WAME `.codex/locks/resources/`；其他仓以 staging `locks/` 兜底；stale > 4h 需 Lead 确认。

### 4.2 worktree 与端口

| 包 | worktree 建议 |
|---|---|
| WAS-TP-01 / WAS-TP-02 | `/Users/lujunxiang/Projects/_wt/GlobalCloud WAS--docs-was-decision-contract-freeze` 等（每包独立） |
| XWAIL-TP-01 | `/Users/lujunxiang/Projects/_wt/GlobalCloud XWAIL--feat-xwail-decision-profile-extension` |
| WAME-TP-00…04 | `/Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-wame-decision-<slug>` |
| WAME-TP-05…07 | `/Users/lujunxiang/Projects/_wt/GlobalCloud WAME--feat-wame-decision-<slug>` |
| GPCF-TP-01…03 | `/Users/lujunxiang/Projects/_wt/GlobalCloud GPCF--<branch-slug>` |

禁止把 worktree 放在项目群根内；新增 worktree 前须先取 B7 清理授权。

### 4.3 kill switch（分级）

| 级 | 动作 | 授权 |
|---|---|---|
| KS-0 | **不派发**（当前唯一合法） | 无需 |
| KS-1 | 单包 `worktree remove --force` + `branch -D` | 需老卢授权 |
| KS-2 | 已合并 `git revert -m 1 <merge_sha>` | 需老卢授权 |
| KS-3 | WAME `DECISION_AUTHORIZATION_ENABLED=false`（fail-closed） | 运行时开关，需登记 |
| KS-4 | WAES `scripts/decision_runtime_ctl.py --stop`（若复活） | 需登记 |

### 4.4 rollback

| 类型 | 回滚 |
|---|---|
| WAS/XWAIL 契约类 | 新增文件 → 删文件/`git revert`；不改 Core |
| WAME 代码类 | 单包 `revert` + 运行时 flag OFF；不连带其它已合包 |
| GPCF 文档/台账 | 删除变更目录 → 重跑 `document_control.py` 回落；不手改台账 |
| 已评审提案 | 不物理删除：`status: superseded` + `superseded_by` |

## 5. 执行约束（No-Go 阶段）

1. 不创建 worktree / 分支 / 资源锁；不修改任何项目仓；不提交、不清理；不写 PMC；不建 Feature；不派发实现 agent。
2. 不在主工作树执行任何 `git add -A` / `git add .`；未来只允许精确路径。
3. GPCF 新包必须从 `main` 切（当前检出 `ci/gpcf-gates` 落后 179 提交）；本阶段不切。
4. WAME 新包基线未定（O3），不得自行选择。
5. 任何「证据」必须带命令、时间戳、sha256；不得复制正文、密钥、客户数据、模型权重。

## 6. 非声明

本任务清单为 `draft`：不是派发指令，不构成平台获批、架构提升、契约冻结、验收结论或状态提升；`accepted / integrated / production_ready / customer_accepted` 均未发生；No-Go / partial 维持。
