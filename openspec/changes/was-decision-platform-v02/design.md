---
doc_id: GPCF-WAS-DECISION-PLATFORM-V02-DESIGN-20261024
title: WAS 决策能力平台 v0.2 设计（was-decision-platform-v02）
project: WAS
related_projects: [WAS, WAES, WAME, GPCF, XWAIL]
domain: openspec
status: draft
version: v0.2
owner: WAS
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/was-decision-platform-v02/design.md
source_path: openspec/changes/was-decision-platform-v02/design.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/WAS世界资产体系总体方案.md
---

# WAS 决策能力平台 v0.2 设计（draft）

**结论：本设计只冻结「方向与边界」的文档口径，不冻结任何 schema、阈值或模型。平台采用「WAS 语义 + Ontology 术语 + XWAIL 契约 + WAME 治理运行时 + 可替换模型适配层」的分层，模型只产出候选与评估，裁定与授权由人工/治理主体完成；所有运行时缺口在 No-Go 阶段不实现。**

## 1. Context（只读事实基线）

| 事实 | 时点/位置 | 设计含义 |
|---|---|---|
| 老卢判定 `No-Go / partial`，允许检查/分类/规划/报告 | 2026-10-24 本会话 | 本设计不产生实现任务，只产出评审输入 |
| WAS v0.1 决策架构文档 `draft_for_review`、`confirmation: architecture_promotion_not_confirmed`、untracked | `GlobalCloud WAS/docs/WAS决策模型体系架构与实施方案_v0.1.md` | 方案是**候选输入**，不是受控方案；架构提升须另行评审 |
| WAS 受控总体方案全文 0 处「决策」 | `GlobalCloud WAS/docs/GlobalCloud WAS 总体方案.md` | 语义回流记录缺失；本 CP 是回流入口，不是已完成传导 |
| WAES 已退役（2026-10-22），资产交接 WAME | WAES README 退役横幅 | 决策平台不得表述为「WAES 复活」；资产只读引用 |
| 双决策模型 R1–R8 PASS、P2-ready、7 项 P2 门槛待确认 | `GlobalCloud WAES/runtime/dual-decision-model/GOAL.md` | “P2-ready”≠ 启用授权 |
| 四项人工拍板 | `decisions/four-decisions.md` | D1–D4 已确认；O1–O4 未决 |

## 2. Goals / Non-Goals

### Goals

1. 把平台定位、分层、权威边界与四项拍板固化为可评审文档；
2. 给出 WAS v0.2 八对象契约的冻结评审方法与门槛；
3. 给出 pilot「任务优先级建议（shadow + no-write）」的可验收合同框架；
4. 给出独立金标/锁定评测集的建立方法与样本量；
5. 给出许可/数据/失败态/权限排除的可执行矩阵；
6. 给出工具链修复与跨仓执行隔离方案，使 Go 条件可判定。

### Non-Goals

不实现；不建 Feature；不启用模型；不接 JEV；不做产品化；不改任何项目仓；不写 PMC；不提交；不冻结 schema/阈值；不声明四禁词；不把 `gate=pass` 当 Green。

## 3. 平台分层与权威边界（方向级，未冻结）

```text
WAS          定义世界资产与决策域（横向能力平面），不替代各阶段责任主体
Ontology     定义资产语义与决策语义（术语、对象、关系、状态词表）
XWAIL        定义资产契约与决策契约（DecisionProfile 可选扩展包，首阶段不改 Core）
WAME         模型登记、裁定、授权、执行门禁、审计与反馈（治理运行时）
Model Adapter 可替换决定模型实现（规则/概率/优化/大模型），只产出候选判断
AaaS/SCaaS   将已授权决策能力服务化（下游，不在本包）
```

### 3.1 五条强制分离（来自 WAS v0.1 §6.2，本 CP 采纳为评审基线）

1. 模型评估 ≠ 裁定；
2. 裁定 ≠ 授权；
3. 授权 ≠ 执行；
4. 执行 ≠ 结果；
5. 结果 ≠ 目标实现。

### 3.2 裁定与授权顺序（P0 冲突待 O2 解决）

强制顺序：`有权主体裁定（DecisionRecord） → WAME 授权（AuthorizationRecord） → 执行（ExecutionRecord）`。
**已知冲突**：WAS v0.1 §7.3 候选结构含 `authorizationRef`，若冻结为必填即等价「先授权后裁定」，与强制顺序相反。**O2 关闭前不得冻结 DecisionRecord schema。**

### 3.3 三世界归属（P0 冲突待 O2 解决）

已知冲突：裁定记录在 §4.3 归 `real` 世界，在 §7.3/§7.4 归 `trusted`/`real` 不一致。
**建议**：采用双字段 `worldLayer + assertionLayer`，并把判定规则写入 Ontology 术语表；**O2 关闭前不得冻结。**

## 4. WAS v0.2 八个最小契约对象（评审输入）

| # | 对象 | 现状（2026-10-24） | 归属层（待确认） |
|---|---|---|---|
| 1 | DecisionProfile | 无字段卡；与 `DecisionModel`/扩展包语义未定 | XWAIL（可选扩展包） |
| 2 | DecisionContextSnapshot | v0.1 中为 `DecisionContext`，需扩义改名 | XWAIL / WAS |
| 3 | DecisionAssessment | 有语义位置，字段未冻结 | XWAIL / WAME 评估层 |
| 4 | DecisionRecord | 有候选结构，但状态族混入 `Authorized/Revoked`，与「裁定≠授权」冲突 | WAS 裁定语义 / XWAIL 契约 |
| 5 | AuthorizationRecord | 无字段卡；WAME `receipts` 与 GPCF `AUTH-*` 双账未归一 | WAME |
| 6 | ExecutionRecord | 无字段卡；执行状态需与 WAME 现有状态机对齐 | WAME |
| 7 | OutcomeRecord | v0.1 中为 `DecisionOutcome`，需改名并走术语治理 | WAME / WAS |
| 8 | FeedbackRecord | v0.1 中为 `DecisionFeedback`；与 KDS 同名对象「同名异义」 | WAME / KDS 边界 |

### 4.1 O2 已拍板（2026-10-24）

| 子决议 | 结论 |
|---|---|
| 命名 | 新名为主；旧名 `DecisionContext/DecisionOutcome/DecisionFeedback` 登记为 deprecated alias；KDS 同名 `FeedbackRecord` 加 decision 限定语 |
| 裁定/授权 | `DecisionRecord.decisionStatus = Proposed/Decided/Rejected/Superseded/Revoked`；`AuthorizationRecord` 必须有 `decisionRef`；`authorizationRef` 不做裁定前置必填（最多 append-only 回填）；负例 N12 |
| 三世界 | 双字段 `worldLayer`（记录事件层）+ `assertionLayer`（内容断言层）；聚合 weakest-link；负例 N08 |
| DecisionProfile | Profile = 模型注册档案容器；DecisionModel = 其条目；场景模板留 v0.3；登记单一事实源归 Q06 |
| 冻结范围 | 八对象 schema + 外部引用白名单；Question/Objective/Alternative/Criterion/Constraint 等辅助对象留 v0.3；白名单逐字段评审 |

> 依据：`drafts/o2-resolution-20261024.md`；决策台账 R2-02…R2-06。

### 4.2 Q06/Q07/Q11 已拍板（2026-10-24）

| 决议 | 结论 |
|---|---|
| Q06 授权载体 | 两层单一事实源：GPCF `AUTH-*`（治理授权）／WAME `AuthorizationRecord`（业务动作授权）／XAP `receipt` 为派生凭证；三层映射表 + 不变量 |
| Q07 ID 命名空间 | 新增 `decision` ns；实例前缀 `dpr-/dcs-/das-/drec-/authz-/exec-/out-/fb-`；登记入引用键规范 A3/A4 与 GPCF 登记表 |
| Q11 失败枚举 | 10 值统一枚举 + `Assessment.failureKind` + fail-closed 映射；非 `ok` 不得放行；Hermes fail-open 反例登记为上线前必修 |

> 依据：`drafts/q06-q11-resolution-20261024.md`；决策台账 R3-02…R3-04。

### 4.3 Q13/Q15 已拍板（2026-10-24）

| 决议 | 结论 |
|---|---|
| Q13 冻结状态/签署 | 新增 `frozen` 契约效力状态；多角色最小签署集 + 独立复核人（非作者/非实现者）+ 老卢最终批准；freeze record append-only，解冻只能新版本+新记录 |
| Q15-E3 框架授权 | 允许框架授权（scope+有效期+最大次数/额度），逐次引用授权 ID 并校验范围，禁止无限授权 |
| Q15-E4 紧急动作 | 仅 fail-safe 动作（停止/回滚/隔离）可无授权先执行+留痕+事后追认；禁止正向动作 |
| Q15-E6 外部凭证 | **无签名/可信时间凭证一律禁止外部系统执行**；签名能力（B7）补齐前外部执行链不可验证，登记为 Go 前置 |

> 依据：`drafts/q13-q15-resolution-20261024.md`；决策台账 R4-02…R4-06。**契约冻结 P0 已全部关闭（Q06/Q07/Q11/Q13/Q15）**；八对象字段卡草案 v0.1 已完成（staging，待独立复核）：`drafts/field-cards-v0.2-draft-20261024.md`；B2 生产计划（schema 映射/Validator/fixtures/授权请求）见 `drafts/b2-schema-production-plan-20261024.md`；剩余 8 schema、Validator/fixtures、freeze record 与 G0–G7 门证据。

**冻结门（建议 G0–G7）**：范围与对象清单 → 字段/不变量 → 状态机与非法转移 → 引用键与版本 → 失败态与负例（N01–N42）→ 评审签署 → 冻结记录 → 发布。**当前 0/8 可冻结**（详见 `drafts/contract-freeze.md`）。

## 5. 运行承接与模型策略（受 D3 约束）

| 项 | 方向 | 待决 |
|---|---|---|
| 治理运行时 | WAME 承接登记/裁定/授权/执行/审计/反馈；边界「承接身份与资产 ≠ 生产运行接管」 | O1 |
| WAES 资产 | 只读引用；**不复活**为默认口径；复活需老卢批准并走 WAME 变更流程 | **O1 已定（2026-10-24，O1-A）：不复活；3 个 WAES 包平移 WAME** |
| StartLux 权重 | CC BY-NC 4.0：仅内部非商业可用；**不得进入商业交付**；不复制权重/推理正文 | D3 已拍板 |
| 可商用模型 | 平台适配层须支持许可可商用模型；pilot 能力模型选型前须过许可审查 | O4 |
| JEV 等第三方 SaaS | 客户数据默认禁止外发（D4）；接入前须合同/出境审查 | D4 / B4 |
| 本地影子 | `127.0.0.1:18090` down；`unavailable` 不得当放行；启动需授权 | B1 |

## 6. 首个 pilot 设计（D2 已拍板，合同待签）

| 维度 | 设计 |
|---|---|
| 决策问题 | 在给定项目内 3–6 个候选工作项中，建议先推进哪一项（或 abstain） |
| 形态 | shadow + no-write：可见建议但不自动执行、不写回任务状态 |
| 决策点 | S-P1（项目内候选工作项优先级），避免复用不同候选集的 `priority_rank` 历史流量 |
| no-action 基线 | 不做优先级建议时的现状推进顺序与结果 |
| 候选行动 | 建议某任务优先 / abstain；不产生写操作 |
| Outcome 时间窗 | T0 → +72h → +14d → +30d（实际延期、返工、完成质量） |
| 损失矩阵 | λ_FN/λ_FP/λ_OV/λ_review 四参数，需 D7 一次确认；未确认前不发布期望损失 |
| 当前基线 | 无独立金标、无 due date；需 shadow 期自建「承诺完成日」 |
| 晋级 | `ΔE[L] ≤ −10%` 且 bootstrap 95% CI 上界 < 0；λ 敏感性符号不变（草案，待签） |
| 停止 | 安全门/数据门/许可门任一失败；或人工复核量超预算 |
| 回滚 | 关闭建议开关，回到 no-action；不修改历史记录 |

### 6.1 「能力提升」的唯一合法表述（草案）

以期望损失改善 + 置信区间 + 人工复核成本共同表述；**禁止**用「增加模型」「一致率更高」「延迟更低」「合成集提升」「自评提升」替代能力目标。

### 6.2 验收参数已定（2026-10-24）

| 项 | 结论 |
|---|---|
| 决策点 | S-P1：项目内 3–6 个候选工作项，选唯一下一步；候选集由确定性规则生成 |
| 输出形态 | 只出选择/排序 + abstain（不要求概率；如出概率须过 G-5 校准门） |
| 延期口径 | D-a：T0 独立观察者记录承诺完成日，按实际完成−承诺计算 |
| 标注角色 | 2 名内部非实现者独立盲标 + 1 名外部/新成员仲裁（κ≥0.6、仲裁率≤20%） |
| λ 路径 | 相对权重 FN:FP:OV≈1:0.5:2 先做敏感性；绝对值 D7 一次确认 |

> 依据：`drafts/acceptance-contract-params-20261024.md`；决策台账 R9-02…R9-08。合同为 D7 草案，**未冻结、未评测、未生成 gold**。

## 7. 独立金标与锁定评测（评审输入）

> 2026-10-24 建设计划见 `drafts/b3-gold-standard-build-plan-20261024.md`（角色/独立性、数据流程、300 锁定集分层、标注协议、指标、D0–D7 时间表、≤2 月/≤3 人周、显式授权清单）。预授权已自动确认 Q6/Q8/Q10/Q11/Q12 参数。

| 要求 | 设计 |
|---|---|
| 标注 | 两人独立**盲标** + 第三人仲裁；κ≥0.6、仲裁率≤20%（草案） |
| 禁止 gold | StartLux / JEV / 预审标签 / 规则标签 / 已曝光样本一律不得作 gold |
| 隔离 | dev / calib / locked / temporal 物理隔离；按项目/事件/时间分组；近重复去重 |
| 指标 | FN/FP、Brier、ECE、risk-coverage、OOD、鲁棒性、期望损失、人工复核量 |
| 样本量 | 50–100 仅 smoke；锁定集 ≥300、时间外 ≥100；红线安全评估 ≥300 独立正例 + ≥500 高相似负例 |
| 版本与存储 | 数据集版本化 + sha256 + 访问控制；冻结封存；复现命令随集发布 |
| 当前缺口 | 无 gold、无锁定集、无 Outcome 数据；347 条复核仅 195 条人工且非盲单人 |

## 8. 许可、数据与失败态（评审输入）

### 8.1 许可边界（D3）

| 资产 | 许可 | 商用结论 |
|---|---|---|
| StartLux 权重 | CC BY-NC 4.0 | **禁止商业交付**；内部非商业可用；商用须 StartLux Labs 书面授权 |
| `startlux-decide` 推理包 | Apache-2.0 | 代码可商用，**不传递到权重** |
| 模型输出数据 | 许可未明文覆盖（灰区） | 商用前须法务书面确认 |
| Qwen / DashScope | API 服务条款（待法务） | 内部评估可用性待确认；客户数据不得外发 |
| 宿主模型（DSH `deepseek-flash`） | 平台条款待查 | 本会话上下文外发通道未纳入 L0 矩阵，须登记 |

### 8.2 数据边界（D4）

- 数据分级：公开 / 内部 / 敏感 / 客户数据 / 凭据；
- 默认禁止外发：内部架构、代码、客户数据、凭据、未脱敏业务数据；
- 出境只实现 L0；L1/L2 零外发拒绝；外发与出境应拆成两个字段；
- 评测只允许脱敏合成/样例数据；append-only 台账与删除/更正权冲突待法务定解。

### 8.3 失败态与 fail-closed

统一枚举（草案）：`ok / unavailable / refusal / ood / missing_evidence / timeout / invalid_input / low_confidence / disputed / policy_blocked`。

- 红线：任一非 `ok` → stop + 人工（fail-closed）；
- 分类：非 `ok` 保留原规则，不得静默降级为无门禁；
- 授权问答：不得退回散文式；
- 高风险输出：必须保留结构化证据（输入摘要、模型版本、规则命中、置信度、时间戳、调用链）；
- **反例**：Hermes 红线插件当前 fail-open，上线前必须先改；本地影子 `unavailable` 不得当放行。

### 8.4 权限排除

模型/适配器**不得**取得：裁定权、授权权、生产写入权、状态提升权、读凭据、改规则、自动扩权。上述权限只属于人工/治理主体，且需审计与双人复核（当前未建）。

### 8.5 G5 已签认（2026-10-24）

| 项 | 结论 |
|---|---|
| 内部许可 | StartLux CC BY-NC 仅内部非商业（安全测试/内部评估），不得作能力证明；平台能力模型须可商用；不复制权重/正文；保留 LICENSE/NOTICE |
| 数据边界 | G0–G4 分级 + 仅 L0 + 默认禁止敏感外发；远端决策服务仅接收抽象化上下文（≤500 字符，无代码/路径/凭据/客户数据）；评测仅脱敏合成/样例数据 |
| 输出数据 | 暂不允许商用再使用；内部使用可；商用须法务书面确认 |
| 法务待办 | P1–P12 与 R-01…R-12 登记为 Go 前置，清单化跟踪 |
| 权限排除 | 模型/适配器不得取得裁定、授权、生产写入、状态提升、读凭据、改规则、自动扩权 |

> 依据：`drafts/g5-license-data-review-package-20261024.md`；决策台账 R5-02…R5-06。红线闸口 p=.394 → escalate，已由老卢签认。**G5 仅内部/No-Go 阶段条件性通过**；商用/出境/法务未通过。

## 9. 工具链修复方案（B1，仅方案不执行）

> 2026-10-24 补丁计划见 `drafts/b1-toolchain-remediation-plan-20261024.md`（D1–D7、WAME 代理最小修复、21 代理+校验器同步、StartLux 单源重建、Hermes fail-closed、B1-A…E 显式授权请求）。全部属实现类，未实施。

| # | 问题 | 方案 | 风险 |
|---|---|---|---|
| 1 | GPCF 门禁 `status_ceiling=partial`（2811 逾期） | 只登记 backlog，人工逐篇复核；**禁止批量改 `last_reviewed`** | 伪造证据 |
| 2 | WAME 代理 `GlobalCoud GPCF` 拼写 | 改 `GlobalCloud GPCF`；同改 GPCF 校验器 `REQUIRED_TOKENS` | 21 仓脏树；反向 FAIL |
| 3 | StartLux 模板漂移 | 以生产 `GATE_RULES` 为唯一事实源重新生成注册表；重建基线并 pin 期望 hash | 写 `~/.config/startlux` 需授权 |
| 4 | 本地影子 down | 不启动；所有结论标 `unavailable`，不得当放行 | 启动需授权 |
| 5 | 红线基线四套（6/7/9/25） | 归一为单一版本化基线并登记 | 影响范围待评估 |
| 6 | GPCF 360 dirty | 定性为 `document_control.py` 全量重写残留；新任务包只在独立 worktree 作业 | 提交污染 |

**Green 口径（建议，需老卢确认）**：`gate=pass` 且 `status_ceiling=controlled`；不得把 `partial` 表述为 Green。

## 10. 跨仓执行隔离（未来若 Go）

| 机制 | 设计 |
|---|---|
| 分支 | `docs/` `feat/` `chore/` 前缀；WAS/WAME 从 `main`，GPCF 从 `main`（不得从 `ci/gpcf-gates`），WAME 基线待 O3 |
| worktree | 每包独立 clean worktree，放 `~/Projects/_wt/<repo>--<branch-slug>/`；禁止项目群根内 |
| 锁 | `LOCK-GC-OPENSPEC`、`LOCK-XWAIL-SCHEMAS`、`LOCK-WAME-DECISION-DOMAIN`；同仓多包串行；stale>4h 需 Lead 确认 |
| 串行顺序 | GPCF Change → WAS 冻结 → XWAIL schema → WAS Ontology → WAME 链 ∥ WAES 适配器 → WAES 评测/运行时 → GPCF 收口 → 验收 |
| Kill switch | 当前仅「不派发」合法；执行态单包 `worktree remove + branch -D`（需授权）；WAME `DECISION_AUTHORIZATION_ENABLED=false`；WAES `decision_runtime_ctl.py --stop` |
| 回滚 | 契约类为新增文件 → revert 即消失；代码类单包 revert + flag OFF；文档类删除目录 + 重跑生成器 |

## 11. 风险

| # | 风险 | 缓解 |
|---|---|---|
| R1 | 把 CP 创建误读为平台获批 | 全文件非声明边界；评审先读 §11 |
| R2 | 商业目标下仍依赖 CC BY-NC | D3 写死；pilot 模型选型过 O4 许可审查 |
| R3 | 契约冲突被带入 schema | O2 关闭前不冻结；N01–N42 负例必须通过 |
| R4 | 无 gold 却宣称能力提升 | G3 未满足前禁止任何能力结论 |
| R5 | 批量改复核日期伪造 Green | 明确禁止；只登记 backlog |
| R6 | 21 仓代理统一修引发反向 FAIL | 同步改校验器；串行、可回滚、单独授权 |
| R7 | 在脏工作树/错误基线上建包 | 独立 worktree + 正确 `base_ref`；本阶段不动 |
| R8 | WAES 复活与退役口径冲突 | O1 未决前 WAES 3 包一律不可执行 |

## 12. 开放问题（需老卢/评审关闭）

| ID | 问题 | 影响 | 保守默认 |
|---|---|---|---|
| O1 | WAES 是否复活；StartLux 运行是否收编 WAME `ops/` | WAES 3 包去留、WAME 边界 | 不复活、只读引用 |
| O2 | 8 对象命名/归属冻结（`DecisionOutcome`↔`OutcomeRecord` 等）、裁定状态族、三世界字段、`authorizationRef` 顺序 | 契约冻结、XWAIL schema | **已关闭（2026-10-24，R2-02…R2-06）**；Q06/Q07/Q11 仍 P0 |
| O3 | WAME/GPCF 分支基线与 worktree 配额 | 任务包开工位置 | 本阶段不清理、不切分支 |
| O4 | pilot 能力模型选型与许可审查（可商用） | G3/G5 | 未定；不得用 StartLux 作能力证明 |

## 13. Go/No-Go 判定矩阵（2026-10-24）

| 项 | 结论 |
|---|---|
| 模型判定 | **B 维持 No-Go/partial（p=.792）**；C 条件 Go .167；A Go .041 |
| 就绪度 | G1 ✅；G2/G5/G6 ⚠️；G3/G4/G7/G8 ❌（1/8 满足、3/8 部分、4/8 未满足） |
| 差距优先级 | B2 契约 schema/冻结 .509 → B7 文档门禁 .155 → B1 工具链 .150 → B4 许可法务 .098 → B3 金标 .077 → B11 签名 .011 |
| 预授权 | 依老卢 2026-10-24 授权自动确认 B；实现/提交/状态提升仍为硬边界 |
| 依据 | `drafts/go-no-go-matrix-20261024.md`；决策台账 R10-01…R10-04 |

## 14. 非声明

本设计为 `draft`：不构成架构提升、契约冻结、实现授权、验收结论或状态提升；`accepted / integrated / production_ready / customer_accepted` 均未发生；No-Go / partial 维持。
