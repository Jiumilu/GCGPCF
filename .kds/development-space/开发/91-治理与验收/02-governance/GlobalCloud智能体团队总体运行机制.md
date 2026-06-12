---
doc_id: GPCF-DOC-7F63F2D675
title: GlobalCloud 智能体团队总体运行机制
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud智能体团队总体运行机制.md
source_path: 02-governance/GlobalCloud智能体团队总体运行机制.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 智能体团队总体运行机制

日期：2026-06-12
状态：v1.1
定位：一份文档讲清楚"团队是谁、怎么跑、怎么接力、怎么和你配合"。工程细节指向各专项规范。
v1.1 变更：新增 §二"技能层深度展开"，详解协同开发 skill 如何被小即团队调用、project-registry 桥接机制、两阶段并行编排。

---

## 一、编制层：11 个智能体 × 12 个交付包

这是静态角色层——谁负责哪个项目，在治理文档中写死，不随任务变化。

### 1.1 全量智能体名录

| 智能体 | 中文名 | Loop 角色 | 绑定交付包 | 当前状态 |
|---|---|---|---|---|
| 小即 | 总控 | 集成层 | 团队总控 | in_progress |
| 宪衡 | 治理架构 | 执行层 | WAES 治理与控制塔包、MMC 管理配置中心包 | partial |
| 链同 | 协同业务 | 执行层 | PVAOS 生态入口包、GPC 运营协同包、PKC 个人知识工作台包 | partial |
| 厂行 | 工厂执行 | 执行层 | GFIS 工厂执行包、Edge 边缘接入包 | partial |
| 数枢 | 数据平台 | 执行层 | AI 与数据底座包 | in_progress |
| 仓图 | 资源仓库 | 执行层 | 资源仓库域、11 池映射 | not_started |
| 知源 | 知识体系 | 执行层 | 企业级知识主存与知识引擎包 | partial |
| 灵策 | AI 服务 | 执行层 | XiaoC+Hermes+XGD AI 服务包、Brain 智能知识平台包 | in_progress |
| 接稳 | 连接器可靠性 | 执行层 | XiaoG 本地语音助手包、连接器与可靠性（横向） | not_started |
| 评衡 | 评估审计 | 审计层 | 全局审计与评分 | not_started |
| 证验 | 证据验收 | 审计层 | 全局证据与验收 | not_started |

### 1.2 12 个交付包完整映射

| 交付包 | 牵头 | 协同 | 审计 |
|---|---|---|---|
| WAES 治理与控制塔包 | 宪衡 | 数枢、灵策 | 评衡、证验 |
| MMC 管理配置中心包 | 宪衡 | 链同 | 评衡、证验 |
| PVAOS 生态入口包 | 链同 | 宪衡 | 证验 |
| GPC 运营协同包 | 链同 | 数枢、接稳 | 评衡 |
| PKC 个人知识工作台包 | 链同 | 灵策 | 评衡、证验 |
| GFIS 工厂执行包 | 厂行 | 数枢、接稳 | 证验 |
| Edge 边缘接入包 | 厂行 | 接稳 | 证验 |
| AI 与数据底座包 | 数枢 | 仓图、知源 | 评衡 |
| 企业级知识主存与知识引擎包 | 知源 | 灵策、数枢 | 评衡 |
| XiaoC+Hermes+XGD AI 服务包 | 灵策 | 知源、宪衡 | 证验 |
| Brain 智能知识平台包 | 灵策 | 知源、数枢 | 评衡、证验 |
| XiaoG 本地语音助手包 | 接稳 | 厂行 | 证验 |

详细定义见 [12个交付包责任分解表](../05-agent-team/GlobalCloud智能体团队12个交付包责任分解表.md)。

### 1.3 角色硬边界

| 层 | 能做 | 不能做 |
|---|---|---|
| 执行层 | 修改业务文件、产出 evidence、自检、登记阻塞 | 自行宣布 complete/accepted、跨域修改 |
| 审计层（评衡） | 打分、发现问题、形成量化报告 | 修改业务文件、补证据 |
| 审计层（证验） | 验证 evidence 完整性、判断可复现性 | 替执行层补证据 |
| 集成层（小即） | 跨项目收口、命名统一、状态升级申请 | 绕过项目仓 evidence、替代项目微循环 |

核心原则：验收层可以判定，不可以代替执行层；集成层可以收口，不可以绕过 evidence。
详细定义见 [gpcf-role-boundary.md](gpcf-role-boundary.md)。

---

## 二、技能层深度展开：协同开发 skill 如何被小即团队调用

编制层定义"谁负责"，技能层定义"怎么跑"。二者通过 `project-registry.md` 桥接——它是唯一扩展点。

### 2.1 调用链：从编制层到技能层

```
小即（集成层）分派任务给宪衡
    │
    │  宪衡说"启动协同开发"（触发词）
    │
    v
globalcloud-collaborative-dev skill 加载
    │
    │  Step 0：深度扫描（读长期记忆→Git 状态→构建验证→服务健康）
    │  Step 0d：读 project-registry.md，确定哪些项目 active=✅
    │
    │  对每个 active 项目，按角色映射到编排 Stage
    │
    v
多智能体两阶段并行编排
    │
    ├── Stage 1（control_plane + data_plane 并行）
    │       MMC(control_plane) → agent-be + agent-security + agent-qa
    │       KDS(data_plane)    → agent-be + agent-data + agent-qa
    │
    └── Stage 2（Stage 1 完成后，frontend 并行）
            Brain(frontend)    → agent-fe + agent-qa
            PKC(frontend)      → agent-fe + agent-qa
    │
    v
OpsX 11 步执行（产 evidence）
    │
    v
Harness Governance 独立审计（状态判定）
```

### 2.2 关键桥接：project-registry.md

`~/.codex/skills/globalcloud-collaborative-dev/references/project-registry.md` 是小即团队编制和协同开发引擎之间的唯一桥接点。它决定：

- 哪些项目参与多智能体编排（`active` 字段）
- 项目在哪个 Stage 执行（`角色` 字段）
- 每个项目的启动验证命令

**当前状态（仅 4 个试点 active）**：

| 项目 | 角色 | Stage | active |
|---|---|---|---|
| MMC | control_plane | Stage 1 | ✅ |
| KDS | data_plane | Stage 1 | ✅ |
| Brain | frontend | Stage 2 | ✅ |
| PKC | frontend | Stage 2 | ✅ |

**待纳入（8 个项目，对应小即团队已分配的交付包）**：

| 项目 | 对应牵头智能体 | 推荐角色 | 纳入阻塞 |
|---|---|---|---|
| GFIS | 厂行 | frontend | 独立项目，有自己的开发流程 |
| GPC | 链同 | frontend | 待确认技术方向 |
| PVAOS | 链同 | frontend | 待确认业务定位 |
| WAES | 宪衡 | frontend | 待确认业务定位 |
| XGD | 灵策 | frontend | 待确认技术栈 |
| XiaoC | 灵策 | external | UI test 超时 + 缺 Wrangler CLI |
| XiaoG | 接稳 | — | 目录不存在（ESP32 硬件项目，不在本地） |
| GPCF | 小即 | — | 纯文档项目，不参与代码编排 |

**纳入一个项目只需 3 步**：从"待纳入"表移至"活跃项目"表 → 填写角色/端口/启动验证命令 → 改 `active` 为 ✅。多智能体编排自动按角色分组派发，无需修改 SKILL.md。

### 2.3 两层调度：Layer 1（项目角色）→ Layer 2（技术标签）

这是协同开发 skill 的核心调度机制：

```
Layer 1 — 按项目角色分组（决定 Stage 和并行策略）
   control_plane → Stage 1 最先（API 路由、网关、权限）
   data_plane    → Stage 1 并行（数据存储、搜索、索引）
   frontend      → Stage 2 串行（依赖 Stage 1 的 API 定义）
   external      → 跳过（独立治理周期）

Layer 2 — 按任务标签派发技术子 Agent（同一个项目内）
   收到 3 个 tasks:
     task "新增 API 端点"  → agent-be
     task "添加权限检查"   → agent-security
     task "编写单元测试"   → agent-qa
```

**调度约束**：最多 3 Agent 并行、单 Agent ≤12 文件、≤30 分钟、重试 1 次。

### 2.4 Workspace 隔离与 Patch 合并

每个技术子 Agent 在独立 workspace 内修改，只产出 `.patch`：

```
.harness/runs/<run_id>/
  workspaces/
    agent-mmc/       ← agent-be 在 MMC 的隔离工作区
    agent-kds/       ← agent-data 在 KDS 的隔离工作区
  patches/
    agent-mmc.patch
    agent-kds.patch
```

合并前由 Merger 执行冲突检测（文件/API/行为三类），统一 apply。Agent 失败时：同 Stage 其他 Agent 结果保留，失败 workspace 用 `git checkout -- .` 重试，三次失败降级串行。

### 2.5 与 OpsX / Harness 的接力

协同开发 skill 在 Step 0-8 走 OpsX 的 11 步流程，Step 9-10 交给 Harness：

```
协同开发 Orchestrator
    │
    ├── Step 0-8：走 OpsX 11 步流程
    │     Gate Check → Propose → Design → Task Breakdown
    │     → Agent Dispatch（此时触发两阶段并行）
    │     → TDD + Code → Evidence → gstack Review
    │
    ├── Step 9：OpsX 产出 Handoff 包 → 停手
    │
    └── Step 10：Harness Governance audit_only 模式
          独立审计 evidence → 状态判定
          → 人工确认 → accepted → archive
```

编排层不直接调用 `openspec archive`——那是 Harness 的权限。

---

## 三、技能层总览：三层引擎接力

```
globalcloud-collaborative-dev（指挥层）
    │  启动扫描 → 分派 5 个技术子 Agent → 两阶段并行
    │
    v
opsx-full-cycle（执行层）
    │  11 步流程：需求→设计→实现→证据→审查
    │  Step 9 产出 Handoff 包 → 自己停手
    │
    v
globalcloud-harness-governance（验收层）
    │  独立审计 evidence → 7 类冲突检测 → 状态判定
    │
    v
人工确认 → accepted → complete
```

### 3.1 指挥层：globalcloud-collaborative-dev

角色：Orchestrator。不直接写代码，而是分派任务给 5 个技术子 Agent。

| 技术子 Agent | 职责 |
|---|---|
| `agent-fe` | UI/前端/样式/组件 |
| `agent-be` | API/后端/函数 |
| `agent-qa` | 测试/验证/E2E |
| `agent-data` | 数据/DB/schema |
| `agent-security` | 安全/auth/权限 |

启动时执行 8 步深度扫描（依赖检查→长期记忆→Git 状态→OpenSpec 上下文→团队就绪→构建验证→依赖新鲜度→服务健康），带推荐方案提问，不把决策负担丢给用户。

### 3.2 执行层：opsx-full-cycle

角色：执行引擎。负责从需求到 evidence 的完整链路。

```
0. Gate Check          - 入口条件验证
1. Preflight + Lock    - 冻结状态、锁定工作区（锁 4h TTL 自动过期）
2. Propose             - 暂停确认变更方案
3. Design Review       - 设计评审 + 风险 + 边界
4. Task Breakdown      - 任务分解 → Agent 派发（触发两阶段并行）
5-6. TDD + Code        - 独立 workspace，产出 .patch
7. Evidence Collect    - 证据收集 + provenance
8. gstack Review       - 代码审查
9. Acceptance Verify   - 验收验证 → 产出 Handoff 包 → 停手
```

OpsX 的职责边界——只做执行，不做验收。Step 9 产完 Handoff 包后自己停手。

### 3.3 验收层：globalcloud-harness-governance

角色：验收权威。消费 OpsX 产出的 Handoff 包，独立审计。

8 步流程：Preflight → Freeze State → Consume Handoff（校验完整性，含缺失/不完整/矛盾三种失败模式）→ Audit Evidence（freshness + trust + 中文证据标准）→ Detect Conflicts（7 类：文件/API/行为/证据/策略/中文兼容/UI 语言）→ Validate（中文验收门禁）→ Set Status → Closeout。

中文验收门禁（`ready_for_human_acceptance` 前必过）：中文搜索/前端中文/标签响应/API 中文，全部实测验证。

Harness 的判定可能与 OpsX 声称的不同——这正是分两层的原因。

---

## 四、完整接力链路（一次变更的全流程）

以"宪衡为 MMC 补充治理模板"为例：

```
1. 你（用户）指定方向
   "MMC 需要补齐治理模板基线"
   │
2. 小即（集成层）分派任务
   宪衡 → MMC 管理配置中心包
   │
3. 宪衡（执行层）说"启动协同开发"
   → globalcloud-collaborative-dev skill 加载
   → 深度扫描：读长期记忆、Git 状态、project-registry
   → 发现 MMC active=✅ 角色=control_plane
   │
4. Orchestrator 任务分解 → Agent 派发
   Layer 1: MMC → Stage 1（control_plane）
   Layer 2: agent-be（模板逻辑）+ agent-security（权限）+ agent-qa（验证）
   │
5. OpsX 11 步执行
   Propose → Design → TDD → Code（.patch）→ Evidence → Review
   Step 9 产出 Handoff 包 → 停手
   │
6. Harness Governance 独立审计
   评衡（打分）+ 证验（验证 evidence 完整性 + 中文门禁）
   → 状态判定
   │
7. 你（用户）人工确认 → accepted
   │
8. 小即（集成层）跨项目收口 → integrated
```

---

## 五、循环节奏：三层时间尺度

| 循环 | 节奏 | 谁做 | 产出 |
|---|---|---|---|
| 微循环 | ~30 分钟/轮 | 各专项智能体 | loop-round-{ID}.md、diff、command log |
| 中循环 | 每 3 轮微循环 / 日终 | 评衡 + 证验 | status-audit、评分报告、阻塞清单 |
| 大循环 | 阶段切换 / 发布前 | 小即 + Harness | GPCF 总状态报告、人工确认记录 |

详细定义见 [gpcf-loop-engineering-spec-v1.md](gpcf-loop-engineering-spec-v1.md)。

---

## 六、统一的度量指标

| 指标 | 绿色（可进入下一轮） | 黄色（允许继续但登记风险） | 红色（不得升级） |
|---|---|---|---|
| 证据完整率 | >=80% | 60%-79% | <60% |
| 门禁通过率 | >=80% | 60%-79% | <60% |
| 阻塞率 | <=20% | 21%-40% | >40% |
| 返工率 | <=15% | 16%-30% | >30% |
| 微循环耗时 | <=30 分钟 | 31-60 分钟 | >60 分钟 |

---

## 七、合规铁律

1. 不产 evidence = 不算完成
2. 状态升级必须经 Harness 判定，执行智能体不得自行升级
3. 每 3 轮微循环触发中循环审计
4. 阻塞项必须在 loop-state.md 显式登记
5. AI 建议不得直接写入业务事实（SUGG → WAES → 业务确认链路）
6. 人工确认是 `accepted` 状态的唯一入口
7. GPCF 总控仓自身也必须纳入 Loop Engineering，不得作为免审计例外

---

## 八、当前缺口：4 个 active 项目 vs 12 个交付包

小即团队已为全部 12 个项目分配了交付包责任，但协同开发 skill 的 `project-registry.md` 目前只有 4 个试点项目标记 `active=✅`。其余 8 个项目需要在小即团队激活对应智能体后，逐步纳入注册表：

| 优先级 | 项目 | 牵头智能体 | 纳入时机 |
|---|---|---|---|
| P1（试点） | MMC/KDS/Brain/PKC | 宪衡/数枢/灵策/链同 | 已 active ✅ |
| P2 | GFIS/GPC/PVAOS/WAES | 厂行/链同/链同/宪衡 | 厂行激活后、链同完成试点后 |
| P3 | XGD/XiaoC | 灵策 | XiaoC UI test 阻塞消解后 |
| P3 | XiaoG | 接稳 | ESP32 硬件项目，不在本地，特殊处理 |
| — | GPCF | 小即 | 纯文档项目，不参与代码编排 |

纳入操作：将项目从注册表"待纳入"表移至"活跃项目"表，填写角色/端口/启动验证命令，改 `active` 为 ✅。多智能体编排自动按角色分组派发。

---

## 九、配套规范索引

| 想了解... | 看这个 |
|---|---|
| 完整 12 交付包责任分解 | [12个交付包责任分解表](../05-agent-team/GlobalCloud智能体团队12个交付包责任分解表.md) |
| Loop Engineering 五段式微循环 | [gpcf-loop-engineering-spec-v1.md](gpcf-loop-engineering-spec-v1.md) |
| 六要素架构总纲 | [gpcf-agent-architecture-six-elements.md](gpcf-agent-architecture-six-elements.md) |
| 角色 CAN/CANNOT 硬边界 | [gpcf-role-boundary.md](gpcf-role-boundary.md) |
| 状态机定义 | [gpcf-status-machine.md](gpcf-status-machine.md) |
| evidence 分类与命名 | [gpcf-evidence-taxonomy.md](gpcf-evidence-taxonomy.md) |
| 协同开发 skill 全文 | `~/.codex/skills/globalcloud-collaborative-dev/SKILL.md` |
| 协同开发 - 项目注册表 | `~/.codex/skills/globalcloud-collaborative-dev/references/project-registry.md` |
| 协同开发 - 多智能体编排 | `~/.codex/skills/globalcloud-collaborative-dev/references/multi-agent-guide.md` |
| OpsX skill 全文 | `~/.codex/skills/opsx-full-cycle/SKILL.md` |
| Harness Governance skill 全文 | `~/.codex/skills/globalcloud-harness-governance/SKILL.md` |
| 12 项目实时状态矩阵 | [gpcf-project-status-matrix.md](../09-status/gpcf-project-status-matrix.md) |
| 智能体 Loop Engineering 改进方案 | [Loop Engineering 全面改进方案](../05-agent-team/GlobalCloud智能体团队Loop Engineering全面改进方案.md) |
| 显性智能体名录 | [显性智能体名录](../05-agent-team/GlobalCloud智能体团队显性智能体名录与可见机制.md) |

---

## 十、版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 初始发布：编制层+技能层双视角、完整接力链路、度量指标、合规铁律、配套索引 |
| 2026-06-12 | v1.1 | 新增 §二"技能层深度展开"：协同开发 skill 调用链、project-registry 桥接机制、两层调度、Workspace 隔离、4 vs 12 缺口分析 |
