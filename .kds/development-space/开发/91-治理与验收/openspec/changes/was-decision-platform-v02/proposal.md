---
doc_id: GPCF-WAS-DECISION-PLATFORM-V02-PROPOSAL-20261024
title: WAS 决策能力平台 v0.2 变更提案（was-decision-platform-v02）
project: WAS
related_projects: [WAS, WAES, WAME, GPCF, XWAIL]
domain: openspec
status: draft
version: v0.2
owner: WAS
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/was-decision-platform-v02/proposal.md
source_path: openspec/changes/was-decision-platform-v02/proposal.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/WAS世界资产体系总体方案.md
---

# WAS 决策能力平台 v0.2 变更提案（was-decision-platform-v02）

**结论：本提案申请在 GC 项目治理入口建立「WAS 决策能力平台 v0.2」变更包，把已判定的 No-Go / partial 现状、能力边界、跨仓影响矩阵、四项已拍板决策与跨仓任务包登记为可评审草案。本包只做规划与治理登记（D0），不写业务代码、不改任何项目仓、不启用模型、不提升状态；No-Go / partial 结论不因本提案改变。**

## 0. 变更元信息（内嵌项目群 Change Proposal 模板字段）

| 字段 | 内容 |
|---|---|
| change_id | `was-decision-platform-v02`（OpenSpec 1.4.1 kebab；版本 v0.2 由标题/`version` 承载） |
| change_source | `change_proposal`（项目群治理入口） |
| proposer | DSH Agent Teams · Lead（受老卢委托做规划与登记） |
| change_summary | 建立 WAS 决策能力平台 v0.2 治理入口，固化四项人工拍板、契约冻结/金标/许可/工具链/任务包六类 P0 输入 |
| requested_status | `draft`（评审通过前不得升 `controlled`/`accepted`） |
| user_confirmation_status | 四项方向决策：**已确认（2026-10-24）**；契约冻结、金标、许可审查、Go 判定：**未确认** |
| 影响项目 | WAS、WAES（退役归档）、WAME、GPCF、XWAIL；下游 AaaS/SCaaS 不在本包范围 |
| 阶段属性 | D0 治理登记；**不进入实现** |

## 1. Why

**结论：能力工程已有 P2-ready 的技术积累，但治理侧没有登记、没有边界、没有独立评测、没有安全许可结论，工具链还存在单一事实源漂移与门禁代理失效；此时进入正式开发不具备 Go 条件。**

### 1.1 老卢的 No-Go / partial 判定（2026-10-24）

| 维度 | 判定 |
|---|---|
| 当前状态 | `No-Go / partial` |
| 允许动作 | 检查、分类、规划、报告 |
| 禁止动作 | 实现、派发实现 agent、提交、清理现有改动 |
| 正式 Go 条件 | 方向/pilot/数据边界/商业目标人工确认；WAS v0.2 契约评审通过；独立金标与量化阈值可执行；工具链漂移与门禁代理修复；数据与许可审查通过；跨仓任务包/分支/worktree/锁建立；项目群文档门禁 Green；shadow/人工裁定/审计/停止/回滚可验证 |

### 1.2 八项 P0 的实际状态（2026-10-24 取证）

| # | P0 项 | 当前状态 | 关键证据 |
|---|---|---|---|
| 1 | 四项人工拍板 | **已完成**（D1–D4，见 §4） | 本会话选择；记录于 `decisions/four-decisions.md` |
| 2 | 跨项目治理任务 | **本变更包即入口**；14 个任务包已拆，全部 `pending` | `tasks.md`；`drafts/task-packages.md` |
| 3 | WAS v0.2 最小契约冻结 | **未通过**：0/8 可冻结；XWAIL 无决策 schema；4 个对象无字段卡 | `drafts/contract-freeze.md` |
| 4 | 「能力提升」验收合同 | **未建立**：无独立金标、无锁定集、无 Outcome 数据；PMC 任务无 due date | `drafts/acceptance-eval.md` |
| 5 | 独立金标与锁定评测集 | **未建立**：现有 347 条复核仅 195 条人工且非盲、单人；无 gold | 同上 |
| 6 | 工具链与规则口径 | **未修复**：StartLux 模板漂移；21/22 个门禁代理路径拼写错误；本地影子 down | `evidence/toolchain-forensics.md` |
| 7 | 安全/许可/数据边界 | **未签**：StartLux CC BY-NC；Qwen/DashScope 条款待法务；输出数据许可灰区；fail-open 反例 | `drafts/security-license.md` |
| 8 | 可实施任务包 | **已形成规划**：14 包（14+6+3 字段）；但全部被 No-Go 总闸与前置阻塞 | `tasks.md` |

### 1.3 能力侧现状（只读引用）

| # | 现状 | 缺口 |
|---|---|---|
| 1 | WAS v0.1 决策架构文档存在但**未受控**：untracked、`draft_for_review`、`confirmation: architecture_promotion_not_confirmed`、`evidence_status: partial` | 能力无受控来源；语义变更尚未回流 WAS 总体方案（受控主方案全文 0 处「决策」） |
| 2 | 双决策模型工程（WAES `runtime/dual-decision-model`）自述 R1–R8 PASS、P2-ready，7 项 P2 门槛待确认 | 「P2-ready」易被误读为可上线；且 WAES 已退役，资产交接 WAME |
| 3 | GPCF 全仓「WAS 决策能力平台 / 双决策模型 / 决策模型体系」Change/Feature 登记 = **0 命中**；PMC 301 项无对应工作项（最近似 `GC-339`） | 无入口、无台账、无影响矩阵；本包为首次登记 |
| 4 | GPCF `openspec/changes/` 已有 19 个先例（含 `gcmem-vision-r0`） | 入口与格式可复用；但本包不得声明已实现/已验收 |

### 1.4 工具链与仓库现状（阻塞证据）

| # | 事实 | 影响 |
|---|---|---|
| 1 | GPCF 正本门禁 2026-10-24 复跑：`gate=pass` / `status_ceiling=partial` / `review_overdue_90d=2811` / `review_date_unverified=52` | 不能把 `partial` 当 Green；2811 篇复核逾期不能靠批量改日期“修复” |
| 2 | 22 个 `tools/kds-sync/loop_document_gate.py` 中 21 个第 12 行写死 `GlobalCoud GPCF`（少 `l`） | 21 个仓的代理门禁全部失效；WAME 实测 `FAIL: missing GPCF canonical loop_document_gate.py` |
| 3 | GPCF 校验器把错误字符串列为 `REQUIRED_TOKENS` | 只修代理不改校验器会反向 FAIL；修复须同步、串行、可回滚 |
| 4 | StartLux `list_templates` 报 `redline_gate.instructions` 与生产 `GATE_RULES['redline']` 不一致（728 字 vs 617 字） | 红线命中记录没有单一基线；历史 selfcheck 基线已过期 |
| 5 | 本地 StartLux 影子 `127.0.0.1:18090` down；`manual-shadow` 实测 `unavailable` | **无本地模型闸口结论；`unavailable` 不得当作放行** |
| 6 | Hermes 红线插件当前为 fail-open（模型不可用即放行） | 与 fail-closed 要求方向相反，属上线前必须修复项 |
| 7 | GPCF 工作树 360 项脏（`document_control.py` 全量重写残留）；`main` 领先检出分支 179 提交；WAME 领先 `main` 45 提交；WAME/GPCF worktree 超配额 | 新任务包必须在独立 clean worktree、从正确基线作业；本阶段禁止清理/提交 |
| 8 | WAES 已于 2026-10-22 退役、资产交接 WAME | 原「WAS/WAES/WAME/GPCF」四仓拆分中的 WAES 包需 O1 决议（复活或平移 WAME） |

## 2. What Changes（全部为文档/登记，无功能变更）

| # | 变更项 | 交付物 | 类型 |
|---|---|---|---|
| 1 | 建立 WAS 域首个决策能力类 Change 包 | 本目录文件（`.openspec.yaml` + README/proposal/design/tasks/spec + artifacts 索引） | 登记 |
| 2 | 固化四项人工拍板与 No-Go 判定 | proposal §4 + `decisions/four-decisions.md` | 决策留痕 |
| 3 | 跨仓影响矩阵与任务包 | proposal §5–§6 + `tasks.md`（14 包） | 规划 |
| 4 | WAS v0.2 契约冻结评审输入 | design §3 + `drafts/contract-freeze.md`（8 对象、N01–N42 负例、评审门） | 评审输入 |
| 5 | pilot 能力验收合同与独立金标计划 | design §5–§6 + `drafts/acceptance-eval.md` | 评审输入 |
| 6 | 许可/数据/失败态矩阵 | design §7 + `drafts/security-license.md` | 审查输入 |
| 7 | 工具链修复与门禁 Green 口径 | design §8 + `evidence/toolchain-forensics.md` | 修复方案 |
| 8 | Go 条件与阻断清单 | proposal §9 | 治理 |

**明确不做**：不写业务代码；不建 GPCF Feature；不改 WAS/WAES/WAME/XWAIL 任何仓；不启动本地影子；不调用远端模型做评测；不写 PMC；不提交；不做任何状态提升。

## 3. Capabilities

### New Capabilities

- `was-decision-platform-v02`（能力域，见 `specs/was-decision-platform-v02/spec.md`）：
  1. **治理登记与变更门禁**：平台相关变更必须经中央入口登记并声明影响矩阵、决策项与回滚方式；
  2. **契约冻结门**：8 个最小契约对象未评审通过前不得进入实现；
  3. **能力验收合同**：pilot 必须用可量化 Outcome 与损失矩阵验收，禁止用「增加模型/一致率更高」替代；
  4. **独立金标与锁定评测**：双人盲标 + 第三人仲裁；禁 StartLux/JEV 输出作 gold；开发/校准/锁定/时间外隔离；
  5. **许可与数据边界**：按未来商业服务规划，CC BY-NC 权重不得进入商业交付；敏感数据默认禁止外发；
  6. **失败态 fail-closed**：unavailable / refusal / OOD / missing evidence / timeout 统一枚举，任一非 ok 不得放行；
  7. **权限排除**：模型不得取得裁定、授权、生产写入、状态提升权限；
  8. **状态诚实**：无四禁词声明，No-Go/partial 维持到 Go 条件全部满足。

### Modified Capabilities

无。本包不修改 WAS 既有八维/三层资产/生命周期契约，不触碰 WAS / GPCF 主方案条款。

## 4. 四项人工拍板（Decision Record，2026-10-24 已确认）

> 决策人：老卢。记录：`runtime/was-platform-v0.2-20261024/decisions/four-decisions.md`。以下为结论，不是模型推断。

| ID | 拍板项 | 结论 | 对平台/任务的直接约束 |
|---|---|---|---|
| **D1** | 平台方向 | 正式从「双模型方案」升级为 **WAS 决策能力平台 v0.2** | WAS 定义决策域/Ontology 语义；XWAIL 定契约；WAME 做登记/裁定/授权/执行/审计/反馈；双模型只是 `DecisionModel` 的一个可替换实现；**架构提升仍待评审** |
| **D2** | 首个 pilot | **任务优先级建议，shadow + no-write**；Outcome = 实际延期/返工/完成质量 | 只读、不写回；红线模型只做安全测试，不作为首个能力证明；验收合同须可量化 |
| **D3** | 使用范围 | 内部使用优先 + **明确未来商业服务** | StartLux 权重 CC BY-NC 4.0 **不得进入商业交付**；商用须授权或替换可商用模型；pilot 能力模型选型须先过许可审查（O4） |
| **D4** | 远端数据边界 | **默认禁止敏感外发** | 架构/代码/客户数据/凭据/未脱敏业务数据一律不发送远端；仅脱敏合成/样例数据可用于评测；当前只实现 L0，L1/L2 一律拒绝 |

### 4.2 后续已拍板决策（2026-10-24）

| ID | 结论 | 记录 |
|---|---|---|
| **O1** | **WAES 不复活**；原 3 个 WAES 任务包（模型适配器/评测 harness/no-write 运行时）**平移 WAME**，按 WAME 变更流程推进 | 决策台账 R1-04；`decisions/four-decisions.md` 开放项关闭记录 |
| **O2** | 契约冻结五个子决议全部按推荐方案通过：新名+旧名 deprecated alias；裁定族去授权状态、授权反向引用裁定；双字段 `worldLayer`+`assertionLayer`；Profile=模型注册档案容器；冻结范围=八对象+外部引用白名单 | 决策台账 R2-02…R2-06；`drafts/o2-resolution-20261024.md` |

### 4.3 契约冻结剩余 P0 决议（2026-10-24）

| ID | 结论 | 记录 |
|---|---|---|
| **Q06** | 授权载体采用**两层单一事实源**：项目群治理授权=GPCF `AUTH-*` append-only 台账；业务动作授权=WAME `AuthorizationRecord`；XAP `receipt` 降为执行面向的派生凭证（`receiptRef`），不再同时承载裁定；三层映射表+不变量入 v0.2 | 决策台账 R3-02；`drafts/q06-q11-resolution-20261024.md` |
| **Q07** | 新增 `decision` 引用命名空间 + 分对象实例前缀（`dpr-/dcs-/das-/drec-/authz-/exec-/out-/fb-`），登记入引用键规范 A3/A4 与 GPCF 登记表；未登记前缀不得进入冻结包 | 决策台账 R3-03；同上 |
| **Q11** | 采用 **10 值统一失败枚举** + `Assessment.failureKind` + fail-closed 映射；任一非 `ok` 不得作为放行/授权/裁定依据；登记 Hermes 红线插件 fail-open 反例为上线前必修项 | 决策台账 R3-04；同上 |

### 4.4 冻结签署与例外规则决议（2026-10-24）

| ID | 结论 | 记录 |
|---|---|---|
| **Q13** | 新增 WAS 契约效力状态 `frozen`（区别于 implemented/verified/accepted）；多角色最小签署集 + 独立复核人（非作者/非实现者）+ 老卢最终批准；freeze record append-only，解冻只能新版本+新记录 | 决策台账 R4-02；`drafts/q13-q15-resolution-20261024.md` |
| **Q15-E3** | 允许框架/预授权（scope+有效期+最大次数/额度），每次执行必须逐条引用授权 ID 并校验范围，禁止无限授权 | 决策台账 R4-03；同上 |
| **Q15-E4** | 仅 fail-safe 动作（停止/回滚/隔离）可无授权先执行，必须留痕+事后补授权追认；禁止任何正向动作走此例外 | 决策台账 R4-04；同上 |
| **Q15-E6** | **无签名/可信时间凭证一律禁止外部系统执行**；签名能力（B7）补齐前外部执行链不可验证，登记为 Go 前置 | 决策台账 R4-05；同上 |

> 八对象字段卡草案 v0.1 已完成（staging，307 行，待独立复核）：`drafts/field-cards-v0.2-draft-20261024.md`；生产清单见 `drafts/field-card-gap-list-20261024.md`。

### 4.5 G5 许可/数据审查签认（2026-10-24）

| 项 | 结论 | 记录 |
|---|---|---|
| **G5-1 内部许可** | StartLux 权重 CC BY-NC 仅内部非商业（安全测试/内部评估），不得作能力证明；平台能力模型须可商用；不复制权重/正文；输出不得作授权/放行/状态提升依据 | 决策台账 R5-02；`drafts/g5-license-data-review-package-20261024.md` |
| **G5-2 数据边界** | G0–G4 分级 + 仅 L0 + 默认禁止敏感外发；远端决策服务仅接收抽象化上下文（≤500 字符，无代码/路径/凭据/客户数据）；评测仅脱敏合成/样例数据 | 决策台账 R5-03；同上 |
| **G5-3 输出数据** | 输出数据暂不允许商用再使用；内部使用可；商用须法务书面确认 | 决策台账 R5-04；同上 |
| **G5-4 法务待办** | P1–P12 与 R-01…R-12 全部登记为 Go 前置，清单化跟踪，不阻塞当前规划/取证 | 决策台账 R5-05；同上 |

> 红线闸口对本审查包 p(需确认)=.394 → `escalate`（升级人工），已由老卢于 2026-10-24 签认。**G5 仅“内部/No-Go 阶段”条件性通过**；商用授权、出境评估与法务项仍是 Go 前置。

### 4.6 pilot 验收合同参数（2026-10-24）

| 项 | 结论 | 记录 |
|---|---|---|
| **Q1 决策点** | S-P1：同一项目/同一周内 3–6 个候选工作项中选唯一下一步 | 决策台账 R9-02；`drafts/acceptance-contract-params-20261024.md` |
| **Q2 输出形态** | 只出选择/排序 + abstain（豁免 ECE/Brier；若未来出概率须另过 G-5） | 决策台账 R9-03；同上 |
| **Q3 延期口径** | D-a：T0 由独立观察者记录“承诺完成日”，按实际完成−承诺计算 | 决策台账 R9-04；同上 |
| **Q4 标注角色** | 2 名内部非实现者独立盲标 + 1 名外部/新成员仲裁 | 决策台账 R9-05；同上 |
| **Q5 λ 路径** | 先用相对权重 FN:FP:OV≈1:0.5:2 做敏感性；绝对值 D7 一次性确认 | 决策台账 R9-06；同上 |

> 红线闸口 p=.240 → `go`（未触发红线）。验收合同仍为 **D7 草案**：未冻结、未评测、未生成 gold；绝对 λ、外部仲裁者招募、PMC 数据补齐、评测脚本授权、存储路径、期限/预算仍待关闭。

### 4.1 D3 与 D2 的联合推论（必须写死）

1. pilot 的「能力证明」**不能依赖 StartLux 权重**；StartLux 仅可在内部用于安全测试（且须许可复核允许），不得成为产品依赖。
2. 平台 `DecisionModel` 适配层必须支持**可商用模型**与**许可替换**；「双模型（StartLux × JEV）」不是平台的商业架构前提。
3. JEV 等第三方 SaaS 接入须先完成数据出境与合同审查；D4 下客户数据不得外发。

## 5. Affected Projects（影响矩阵）

| project | 影响类型 | 影响面 | 必做动作 | 当前状态约束 | 阻塞/风险 |
|---|---|---|---|---|---|
| **WAS** | 归属/语义 | 决策能力域归属与平台定位；语义变更回流 | 评审 v0.2 契约与术语；补「语义变更回流记录」 | v0.1 文档 `draft_for_review` 且 untracked；受控总体方案 0 处「决策」；`ready_for_review` / `semantic_mapping_boundary` | 无受控来源；架构提升未确认 |
| **WAES** | 退役资产 | `runtime/dual-decision-model/` 与 R1–R8 evidence；已退役 | 只读引用；复活或平移由 O1 决定 | 2026-10-22 退役；资产交接 WAME；无 origin | 复活需老卢批准（O1）；3 个 WAES 包被 B8 阻塞 |
| **WAME** | 治理/授权 | 登记、裁定、授权、执行、审计、反馈承接方 | O1 定运行承接边界；O3 定分支基线 | `repair_required`；分支领先 `main` 45 提交；worktree 11 个 | 自身 repair 未解除；基线未归并 |
| **GPCF** | 入口/门禁 | 中央入口、台账、文档门禁、集成验收 | 登记本变更包；修门禁代理（B1）；文档控制收口 | 360 项脏；`main` 领先 179 提交；`gate=pass` / `partial` | 全量脚本重写风险；不能把 `partial` 当 Green |
| **XWAIL** | 契约 | `DecisionProfile` 可选扩展包（只增不改 Core） | O2 定命名与归属后起草 | 现 `schemas-json/` 无决策 schema；`wrapper_review_required` | 契约冻结 0/8；链断在 WAME 侧 |
| AaaS/SCaaS（下游） | 服务化 | 未来将已授权决策能力服务化 | 不在本包范围 | — | 商用依赖 D3 许可结论 |

## 6. 任务包（14 个，全部 `pending`）

> 完整 14+6+3 字段见 `tasks.md` §3。所有包在本阶段 `pending`，被 `G0`（No-Go 未解除/老卢 Go 授权）与 B1–B9、O1–O4 阻塞；不创建 worktree/分支/锁，不派发实现。

| 序号 | 包 | 仓 | 目标分支 | 串行位 | 主要阻塞 |
|---|---|---|---|---|---|
| 1 | GPCF-TP-01 Change Proposal 登记 | GPCF | `docs/gpcf-was-decision-platform-change` | 1 | G0（本文件即其产物；登记/提交待授权） |
| 2 | WAS-TP-01 v0.2 契约冻结与评审 | WAS | `docs/was-decision-contract-freeze` | 2 | G0、O2、B5 |
| 3 | XWAIL-TP-01 DecisionProfile 扩展包 | XWAIL | `feat/xwail-decision-profile-extension` | 3 | G0、O2、B2、B5 |
| 4 | WAS-TP-02 Ontology 决策语义登记 | WAS | `feat/was-decision-ontology-registration` | 4 | G0、O2、B2 |
| 5 | WAME-TP-00 任务记录与锁登记 | WAME | `chore/wame-decision-task-records` | 5 | G0、O1、B5、B6、B7 |
| 6 | WAME-TP-01 模型登记与版本治理 | WAME | `feat/wame-decision-model-registry` | 6 | G0、O1、B2、B5、B6、B7 |
| 7 | WAME-TP-02 上下文预检与裁定 | WAME | `feat/wame-decision-preflight` | 7 | 同上 |
| 8 | WAME-TP-03 授权回执与执行门禁（no-write） | WAME | `feat/wame-decision-authorization` | 8 | 同上 + B4 |
| 9 | WAME-TP-04 审计回放与反馈 | WAME | `feat/wame-decision-audit-feedback` | 9 | 同上 |
| 10 | WAME-TP-05 决策模型适配器（WAS→WAME 重映射） | WAME | `feat/wame-decision-model-adapter` | 10（重映射后串行） | G0、B2、B4、B5、B6、B7 |
| 11 | WAME-TP-06 评测 harness（锁定集，重映射） | WAME | `feat/wame-decision-eval-harness` | 11 | G0、O4、B2、B3、B4、B5、B6、B7 |
| 12 | WAME-TP-07 no-write 运行时（重映射） | WAME | `feat/wame-decision-runtime-nowrite` | 12 | G0、O4、B2、B4、B5、B6、B7、B11 |
| 13 | GPCF-TP-02 文档控制收口 | GPCF | `chore/gpcf-was-decision-doc-control` | 13 | G0、B1、B5 |
| 14 | GPCF-TP-03 集成验收与契约矩阵登记 | GPCF | `docs/gpcf-was-decision-acceptance` | 14 | G0、B3、B4、B5、B7 |

## 7. 本变更包自身的验收（不是平台验收）

| # | 判据 | 命令/方式 | 当前 |
|---|---|---|---|
| A1 | 结构合法 | `openspec validate was-decision-platform-v02 --type change --json` → `valid: true` | 待执行验证 |
| A2 | 文档受控 | `document_control.py --check` → exit 0 | **未执行**（登记待授权） |
| A3 | 门禁不降级 | `loop_document_gate.py --check-only --repository-only` 不新增 `missing_metadata` / `missing_readme_dirs` / `localization_debt` | 待复验 |
| A4 | 台账可见 | 7+ 个 `doc_id` 在 `09-status/globalcloud-document-control-register.md` 与 `openspec/changes/README.md` 各出现 1 次 | 待登记后核对 |
| A5 | 引用可回读 | 每个外部事实带 `source_path`；不复制正文 | 本包遵守 |
| A6 | 状态诚实 | 四禁词仅出现在「非声明」段（否定语境） | 本包遵守 |
| A7 | 决策有形 | §4 四项逐条有形，记录可回读 | ✅ |
| A8 | 可回滚 | 全部改动 = 1 个新增目录树；删除后生成物可重跑回落 | 设计如此 |

## 8. Rollout（D0 文档推进）

| 阶段 | 动作 | 出口 | 当前 |
|---|---|---|---|
| S0 | staging 草案与取证（本包前身） | Lead 汇总 | ✅ |
| S1 | 创建 CP 目录（untracked draft） | 本文件即产物 | ✅ 已创建（未提交） |
| S2 | 登记：`DOCUMENT_CONTROL_SCOPE` 增量写 + `--check` 归零 + `openspec validate` | 台账可见、门禁不降级 | ⏳ 待授权 |
| S3 | 老卢评审四项决策与 Scope（D1–D4 已确认；O1–O4 待定） | 决策与开放项有形 | ⏳ |
| S4 | 契约冻结/金标/许可/工具链四类 P0 输入回填（仍不实现） | 提案完备、Go 条件可判定 | ⏳ |
| S5（不在本包） | 若老卢改为 Go/受限推进：另立 Feature + 实现授权 | 另行授权 | ❌ |

## 9. Go 条件与阻断清单（老卢口径逐条对齐）

| # | Go 条件 | 当前 | 阻断项 |
|---|---|---|---|
| G1 | 平台方向、pilot、远端数据边界、商业目标人工确认 | ✅ 已确认（D1–D4） | — |
| G2 | WAS v0.2 最小契约评审通过 | ⚠️ 契约冻结 P0 全关；八对象字段卡草案完成；但 schema/Validator/freeze record/独立复核未完成，0/8 可冻结 | 8 schema、Validator/fixtures、独立复核+老卢确认 |
| G3 | 独立金标、基线与量化阈值可执行 | ⚠️ 验收参数已定（S-P1/选择+abstain/D-a/2+1/相对λ）；但无 gold/锁定集/Outcome、无绝对 λ、标注组未任命 | B3、O4、标注组、评测脚本 |
| G4 | 模板/规则漂移与 WAME 门禁代理错误修复 | ❌ 未修复（仅取证+方案） | B1（实现类，需授权） |
| G5 | 数据与许可证审查通过 | ⚠️ **内部/No-Go 阶段条件性通过**（2026-10-24 老卢签认）；商用授权、出境评估、P1–P12/R-01…R-12 未通过 | 法务/许可、B7 签名、商用授权 |
| G6 | 跨仓任务包、分支、worktree 和锁已建立 | ⚠️ 14 包基线 v1.0 + WAES→WAME 重映射完成；未创建 worktree/分支/锁（No-Go 禁止）；B6/B7 待决 | G0、O3、B6/B7 |
| G7 | 项目群文档门禁 Green（非 partial） | ❌ `gate=pass` / `status_ceiling=partial`；2811 逾期；4 篇既有文档待登记 | B9、人工复核债 |
| G8 | shadow、人工裁定、审计、停止和回滚路径可验证 | ❌ 未验证；E6=B 外部执行被签名阻断 | B11、运行时未建 |

> **Round 10 判定（预授权自动确认）**：模型 B 维持 No-Go/partial（p=.792）；就绪度 1/8 满足、3/8 部分、4/8 未满足。判定矩阵与差距优先级见 `drafts/go-no-go-matrix-20261024.md`；差距优先级 B2 .509 > B7 .155 > B1 .150 > B4 .098 > B3 .077 > B11 .011。

**结论：G2–G8 均未满足，维持 No-Go / partial；本提案只解决 G1 与「入口/任务包」的规划形态，不构成 Go。**

## 10. Rollback

| 对象 | 方式 | 验证 |
|---|---|---|
| 新增目录（本变更包） | 删除 `openspec/changes/was-decision-platform-v02/` | `git status` 中该目录消失；`document_control.py --check` 回落 |
| 生成台账/清单/镜像（登记后） | 重跑 `document_control.py` 生成物回落 | grep 本包 `doc_id` = 0 |
| 已进入评审的提案 | **不物理删除**：`status: superseded` + `superseded_by` 指向替代包 | 过期台账自动收录 |
| 账本 / Feature / PMC | 本包从不写入，无需回滚 | — |

## 11. 非声明边界

1. 本包为 `draft` / `proposed`，**不等于平台获批**；No-Go / partial 不因本提案改变。
2. **不等于架构提升**：不修改 WAS / GPCF 主方案任何条款；结构性变化须另开 `GPCF-MASTER-PLAN-CHANGE-YYYYMMDD-NNN` 并经老卢确认。
3. **不等于能力已实现/已集成/已上线**：不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
4. **不授权任何执行**：不写代码、不派发实现 agent、不改任何项目仓、不写 PMC、不建 Feature、不提交、不做状态提升。
5. 双决策模型工程的「P2-ready」「R1–R8 PASS」是工程侧自述（只读引用），不等于启用授权；7 项 P2 门槛仍待老卢确认。
6. 门禁 `gate=pass` 不等于 Green：`status_ceiling=partial`（`review_overdue_90d=2811` / `review_date_unverified=52`）是既有债，不能以批量改 `last_reviewed` 伪造。

## 12. 证据与引用要求

| 类别 | 要求 |
|---|---|
| 结构 | `openspec validate was-decision-platform-v02 --type change --json` → `valid:true` |
| 文档控制 | `document_control.py --check` → exit 0（登记后） |
| 门禁 | `loop_document_gate.py --check-only --repository-only` 不新增 `missing_metadata` / `missing_readme_dirs` / `localization_debt` |
| 引用 | 外部事实带 `source_path` + 时点；不复制正文；staging 路径只在 `artifacts/README.md` 登记 |
| 禁词 | 四禁词仅否定语境 |

## 13. 关联工作项（只读引用）

- PMC `GC-339`「[DSH][收尾] WAES 归档前迁移双决策模型策略路径」（Todo）——与本包主题重叠，本包**不写 PMC**，仅声明关系。
- GPCF `openspec/changes/gcmem-vision-r0/`——结构母本（非内容继承）。
- `openspec/changes/was-flow-naming-migration/`、`was-scenario-flow-extension/`——WAS 域 OpenSpec 写法参照。
