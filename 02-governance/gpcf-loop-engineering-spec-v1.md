# GPCF Loop Engineering v1.0 — 项目群工程闭环运行协议

日期：2026-06-12
状态：规范冻结 v1.0（基线）
适用范围：GlobalCloud 项目群全部 12 个项目
治理口径：遵循 Harness Engineering 治理机制，由总控（小即）统一推进、收口和状态升级

> 本规范是 GPCF 项目群 Loop Engineering 的**唯一主规范**。理论锚点为 [Agent 架构六要素总纲](gpcf-agent-architecture-six-elements.md)。
> 配套文件：状态机定义、证据分类、角色边界、模板集、状态矩阵。
> 所有项目仓、所有智能体、所有循环均以此协议为统一口径。

## 1. 定位

GPCF Loop Engineering v1.0 不是单个项目的开发规范，而是**12 个项目统一进入可控交付状态的底层工程机制**。

它把 GlobalCloud 项目群原本分散的几套治理机制串成一个闭环：

```
设计 → 实现 → 验证 → 反馈 → 再进入
```

## 2. 四层循环骨架

本项目群已有四层循环骨架，Loop Engineering 将其统一为运行协议：

| 循环层 | 已有定义 | 作用 |
|---|---|---|
| 交付生命周期环 | 11 阶段全过程模型 | 管阶段推进 |
| 事件-证据-治理闭环 | WAES 全链路事件与证据流 | 管证据确证 |
| 多智能体协同环 | 5 轮星型协同 | 管智能体协作 |
| Harness 治理环 | 状态→证据→验收→人工确认 | 管状态升级 |

## 3. 最小循环定义（所有项目仓、所有智能体的统一操作协议）

### 3.1 五段式微循环

```
输入 → 动作 → 输出 → 检查 → 反馈
```

| 段 | 含义 | 必留记录 |
|---|---|---|
| 输入 | 本轮要解决的问题/补齐的缺口 | 目标描述 + 入口条件 + 关联需求 |
| 动作 | 代码/文档/配置的变更 | 文件变更清单（新增/修改/删除） |
| 输出 | 本轮实际产出物 | 文件路径、功能描述、产物列表 |
| 检查 | 自查或审计复评 | 检查项 + 命令/方式 + 结果 + 证据 |
| 反馈 | 阻塞项、下一轮输入、状态更新 | 阻塞清单更新、下一轮目标、状态建议 |

### 3.2 循环实例模板

每轮循环使用统一模板 `loop-round-{ID}.md`（详见 `templates/loop-round-template.md`），记录：
- 输入来源、本轮目标、入口条件、不处理范围
- 动作（类型、文件、说明）
- 输出（产物、路径、说明）
- 检查（检查项、命令/方式、结果、证据）
- 反馈（阻塞项、风险项、下一轮输入、建议状态、Harness 判定）

### 3.3 循环状态文件

每个项目仓在 `docs/harness/loop-state.md` 维护当前循环状态（详见 `templates/loop-state-template.md`）：

| 字段 | 含义 |
|---|---|
| loop.round | 本轮序号 |
| loop.current_step | loop_ready / loop_running / evidence_ready / audit_ready / harness_review / accepted / integrated |
| loop.last_entry | 上一轮输入 |
| loop.last_exit | 上一轮输出 |
| loop.gate_result | pass / partial / fail |
| loop.blockers | 阻塞项列表 |
| loop.next_target | 下一轮目标 |

### 3.4 循环质量门

每段出口前必须满足：
1. 输出与输入可对应（不漂移）
2. 证据可被第三方复现（截图、日志、执行命令可追溯）
3. 状态变更必须由 Harness 判定，不得自行升级
4. 阻塞项必须在循环记录中显式列出

## 4. 项目群统一状态机

为避免不同项目用不同标准理解状态，全项目群统一使用以下状态机：

```text
not_started
    ↓
loop_ready          ←── 补齐 Manifest + loop-state.md + evidence 目录
    ↓
loop_running        ←── 至少完成 1 轮微循环
    ↓
evidence_ready      ←── 本轮 evidence 完整率 ≥80%（按 gpcf-evidence-taxonomy.md 权重模型计算；缺失 loop-round-{ID}.md 时不得进入此状态）
    ↓
audit_ready         ←── 完成中循环审计（评衡+证验）
    ↓
harness_review      ←── Harness Governance 判定
    ↓
accepted            ←── 人工确认通过
    ↓
integrated          ←── 小即跨项目收口完成
```

保留异常状态：

| 异常状态 | 触发条件 |
|---|---|
| blocked | 存在阻塞项且无法自行消解 |
| partial | 部分通过、部分未通过 |
| rework_required | 模板、状态机或 evidence 规则需返工 |
| manual_confirmation_required | 等待人工确认 |

**关键约束**：不使用 `done` 表示项目完成。本轮完成使用 `round_done`，项目级状态使用上述状态机。

## 5. 三层循环节奏与触发条件

### 5.1 微循环（开发循环）

| 属性 | 值 |
|---|---|
| 频率 | 单次实现→自查→提交，建议 ≤30 分钟 |
| 触发条件 | 任意一次代码/文档/配置变更 |
| 执行者 | 各专项智能体 |
| 输出 | `loop-round-{ID}.md`、diff、evidence |
| 门禁 | 代码/文档合规、边界不越权 |

### 5.2 中循环（审计循环）

| 属性 | 值 |
|---|---|
| 频率 | 每日结束、或每 3 轮微循环后、或出现 blocked |
| 触发条件 | 日终 OR 累计 3 轮微循环 OR 状态变为 blocked |
| 执行者 | 评衡（量化评分）+ 证验（证据验收） |
| 输出 | `status-audit-YYYY-MM-DD.md`、评分表、阻塞表 |
| 门禁 | 评分达标 + 证据完整 + 无阻塞项未登记 |

**重要规则**：每个项目完成 3 轮微循环后，必须触发一次中循环审计。这与首轮成功标准（每试点项目 ≥3 轮微循环）对齐。

### 5.3 大循环（交付循环）

| 属性 | 值 |
|---|---|
| 频率 | 按交付包走完 11 阶段全过程 |
| 触发条件 | 试点项目完成首批闭环、阶段切换、或发布前 |
| 执行者 | 小即（总控）+ Harness Governance |
| 输出 | GPCF 总状态报告、证据汇总、人工确认记录 |
| 门禁 | 全部阶段证据完整 + 人工确认完成 |

### 5.4 循环节奏协调

```
微循环（分钟级）──→ 中循环（日级/3轮触发）──→ 大循环（交付包级）
       ↓                    ↓                      ↓
   自检记录         →   评分/阻塞清单        →   验收/发布结论
       ↓                    ↓                      ↓
   提交到项目仓      →   汇入 GPCF 证据池       →   GPCF 状态升级
```

## 6. 治理传动链

### 6.1 三层治理角色

| 层 | 角色 | 职责 |
|---|---|---|
| 执行层 | OpsX Full Cycle | 需求→规格→任务→实现→证据 |
| 验收层 | Harness Governance | 读取 evidence，做状态判定 |
| 集成层 | 小即（总控） | 跨项目收口、统一命名、版本冻结 |

### 6.2 角色边界（硬约束）

| 角色 | 能做 | 不能做 |
|---|---|---|
| 执行智能体 | 修改业务文件、产出 evidence、自检 | 自行宣布 complete/accepted |
| 评衡 | 打分、发现问题、形成量化报告 | 修改业务文件 |
| 证验 | 验证 evidence 完整性、判断可复现性 | 替执行层补证据 |
| Harness Governance | 状态判定、门禁裁决 | 绕过人工确认 |
| 小即 | 跨项目收口、命名统一、状态升级申请 | 直接替代项目微循环 |

核心原则：
- 验收层可以判定，不可以代替执行层修正业务内容
- 集成层可以收口，不可以绕过项目仓 evidence

详见 `gpcf-role-boundary.md`。

### 6.3 传动规则

1. 执行层产出 evidence → 写入项目仓 `docs/harness/evidence/`
2. 验收层读取 evidence → 判定状态
3. 验收层**不得**直接修改项目仓业务文件
4. 集成层在所有项目仓循环完成后 → 统一升级 GPCF 总体状态
5. 任何状态升级必须有对应 evidence 支撑

### 6.4 证据汇聚约定

项目群 evidence 统一汇聚到 GPCF 仓库的 `08-evidence-samples/`：

```
08-evidence-samples/
  README.md
  evidence-index.md
  {项目名}/
    loop-round-{ID}.md
    status-audit-YYYY-MM-DD.md
    evidence/
      command-log-{ID}.txt
      test-result-{ID}.md
      metrics-{ID}.json
      screenshots/
```

每个项目仓完成一轮循环后，由执行智能体或总控把本轮 evidence 汇聚到上述路径。evidence 类型和命名规范详见 `gpcf-evidence-taxonomy.md`。

## 7. Loop Round ID 统一编号

全项目群统一使用以下编号格式：

```
GPCF-{项目代号}-LR-{三位序号}
```

项目代号表：

| 项目 | 代号 | 仓库 |
|---|---|---|
| GlobalCloud Brain | BR | GCBrain |
| GlobalCloud GFIS | GF | GCGFIS |
| GlobalCloud GPC | GP | GCGPC |
| GlobalCloud PVAOS | PV | GCPVAOS |
| GlobalCloud WAES | WA | GCWAES |
| GlobalCloud KDS | KD | GCKDS |
| GlobalCloud PKC | PK | GCPKC |
| GlobalCloud XGD | XD | GCXGD |
| GlobalCloud XiaoC | XC | GCXiaoC |
| GlobalCloud XiaoG | XG | GCXiaoG |
| GlobalCloud MMC | MM | GCMMC |
| GlobalCloud GPCF | CF | GCGPCF |

示例：
- `GPCF-WA-LR-001`：WAES 项目第 1 轮微循环
- `GPCF-GP-LR-003`：链同（对应 GPC 项目）第 3 轮微循环

每轮的所有文件均带此编号。Loop ID 只使用项目代号（如 GP），不使用智能体角色名（如 链同/LT）。链同是智能体角色名，GPC 是项目名，GP 是项目代号。

## 8. 循环度量指标

### 8.1 必跟踪指标

| 指标 | 定义 | 采集方式 |
|---|---|---|
| 循环时间 | 从输入到检查完成的实际耗时 | `loop-round-{ID}.md` 时间戳差值 |
| 阻塞率 | 因阻塞项无法进入下一轮的比例 | 阻塞项轮次 / 总循环轮次 |
| 返工率 | 同一目标被重复打开的轮次占比 | 输入相同的轮次 / 总循环轮次 |
| 证据完整率 | 每轮循环有完整 evidence 的比例 | 证据齐全轮次 / 总轮次 |
| 门禁通过率 | 质量门 pass 的比例 | pass 轮次 / 已完成轮次 |

### 8.2 指标阈值与治理动作

| 指标 | 绿色 | 黄色 | 红色 |
|---|---|---|---|
| 证据完整率 | ≥80% | 60%-79% | <60% |
| 门禁通过率 | ≥80% | 60%-79% | <60% |
| 阻塞率 | ≤20% | 21%-40% | >40% |
| 返工率 | ≤15% | 16%-30% | >30% |
| 微循环平均耗时 | ≤30分钟 | 31-60分钟 | >60分钟 |

治理动作：

| 状态 | 动作 |
|---|---|
| 绿色 | 可进入下一轮 |
| 黄色 | 允许继续，但必须登记风险 |
| 红色 | 不得升级状态，进入 blocked 或 rework_required |

### 8.3 可选用指标

| 指标 | 定义 |
|---|---|
| AI 建议采纳率 | AISuggestion 被业务确认采纳的比例 |
| 跨项目依赖阻塞数 | 因其他项目未完成而导致阻塞的轮次 |
| 人工确认等待时间 | 从提交人工确认到收到反馈的耗时 |

## 9. 每个项目仓落地清单

### 9.1 必须补齐

| 文件 | 作用 | 模板来源 |
|---|---|---|
| `PROJECT_HARNESS_MANIFEST.md` | 项目治理基线 | 已有 |
| `docs/harness/loop-state.md` | 循环状态记录 | `templates/loop-state-template.md` |
| `docs/harness/loops/` | 各轮循环实例目录 | `templates/loop-round-template.md` |
| `docs/harness/evidence/README.md` | 证据目录索引 | 新建 |
| `docs/harness/evidence/evidence-index.md` | 证据索引表 | `templates/evidence-index-template.md` |
| `docs/harness/status-audit-YYYY-MM-DD.md` | 定期审计报告 | `templates/loop-audit-template.md` |

### 9.2 按需补齐

| 文件 | 作用 |
|---|---|
| `docs/harness/blockers.md` | 阻塞项专用台账 |
| `docs/harness/risks.md` | 风险登记册 |
| `docs/harness/dependency-map.md` | 跨项目依赖关系图 |

## 10. Evidence 统一分类

详见 `gpcf-evidence-taxonomy.md`。概要：

| 类型 | 文件命名 | 用途 |
|---|---|---|
| loop record | `loop-round-{ID}.md` | 本轮执行记录 |
| diff evidence | `diff-{ID}.patch` | 文件变更证据 |
| command log | `command-log-{ID}.txt` | 命令执行证据 |
| test result | `test-result-{ID}.md` | 测试结果 |
| audit report | `status-audit-YYYY-MM-DD.md` | 中循环审计 |
| screenshot | `screenshot-{scene}-{N}.png` | 页面/流程证据 |
| metric json | `metrics-{ID}.json` | 自动化指标 |

## 11. 首轮试点方案

### 11.1 试点项目选择

| 项目 | 对应仓 | 代号 | 首轮重点 | 战略意义 |
|---|---|---|---|---|
| MMC | GCMMC | MM | 治理模板基线、配置标准化 | 模板/规范源头验证 |
| KDS | GCKDS | KD | 数据资产、指标、证据结构化 | 度量与数据治理 |
| Brain | GCBrain | BR | 知识 UI 层联邦闭环 | 前后端知识闭环验证 |
| PKC | GCPKC | PK | 端到端用户闭环 | 个人工作台全链路验证 |

四者合起来覆盖：模板基线 → 数据证据 → 知识闭环 → 用户闭环。

### 11.2 首轮成功标准

- 每个试点项目完成 ≥3 轮微循环
- 证据完整率 ≥80%
- 阻塞项全部登记
- GPCF `08-evidence-samples/` 下产生首批汇聚 evidence
- Harness Governance 完成首次跨项目状态判定

## 12. 总体实施路线图（P0-P7）

```
P0 规范冻结
  ↓
P1 四项目试点初始化
  ↓
P2 四项目微循环执行（每项目 ≥3 轮）
  ↓
P3 首次中循环审计（评衡+证验）
  ↓
P4 小即跨项目收口
  ↓
P5 推广到其余 8 个项目（分两批）
  ↓
P6 GPCF 自动化治理面板
  ↓
P7 进入阶段 6：正式实施与交付推进
```

### 12.1 P0-A：主规范冻结（已完成）

- 主规范定版（本文档）
- 六要素架构总纲定版

### 12.2 P0-B：配套文件实例化（已完成）

- 状态机定义（gpcf-status-machine.md）
- evidence 分类定义（gpcf-evidence-taxonomy.md）
- 角色边界定义（gpcf-role-boundary.md）
- 4 个模板输出
- GPCF 状态矩阵初始化

### 12.3 P1：试点初始化（待启动）

让「MMC」「KDS」「Brain」「PKC」进入 `loop_ready` 状态。

### 12.4 P2：试点微循环

每项目执行 LR-001 → LR-002 → LR-003。

推荐首轮任务：


**MMC（管理配置中心）**
| 轮次 | 目标 |
|---|---|
| LR-001 | 导出并标准化治理模板基线（Manifest/loop-state/evidence） |
| LR-002 | 验证模板可复制到其他项目仓 |
| LR-003 | 产出模板版本号和变更管理规则 |

**KDS（知识中心）**
| 轮次 | 目标 |
|---|---|
| LR-001 | 定义证据指标数据结构 |
| LR-002 | 建立 metrics JSON 样例 |
| LR-003 | 生成首个证据完整率统计样本 |

**Brain（智能知识平台）**
| 轮次 | 目标 |
|---|---|
| LR-001 | 梳理 KDS→Brain 数据流依赖 |
| LR-002 | 建立知识 UI 层 evidence 产出路径 |
| LR-003 | 验证一个端到端知识展示闭环 |

**PKC（个人知识工作台）**
| 轮次 | 目标 |
|---|---|
| LR-001 | 定义个人工作台与项目群的状态同步接口 |
| LR-002 | 建立用户操作 evidence 采集点 |
| LR-003 | 验证一个完整的用户闭环操作链 |

### 12.5 P3：首次中循环审计

评衡 + 证验完成首次审计。产出：`status-audit-YYYY-MM-DD.md`、评分报告、阻塞清单、证据索引。

### 12.6 P4：小即跨项目收口

小即形成 GPCF 首次 Loop Engineering 状态结论。产出：试点总结、状态矩阵更新、推广决策。

### 12.7 P5：推广到其余 8 个项目

分两批推广。注意：GPCF 总控仓自身也必须纳入同等循环，不得作为免审计例外。

| 项目类型 | 处理方式 |
|---|---|
| 业务/专项项目 | 按普通项目仓执行 loop |
| GPCF 总控仓 | 同时维护总状态矩阵、evidence pool、治理模板 |
| GPCF 自身微循环 | 也必须产生 `GPCF-CF-LR-{N}` |

### 12.8 P6：自动化治理面板

从人工维护转向半自动治理。脚本契约：

| 脚本 | 输入 | 输出 |
|---|---|---|
| `check-loop-state.sh` | 项目仓路径 | loop-state 合规结果 |
| `check-evidence-completeness.sh` | 项目仓/轮次 ID | evidence 完整率 |
| `check-status-upgrade.sh` | 状态矩阵 + evidence | 是否允许升级 |
| `generate-status-matrix.sh` | 12 项目路径 | `gpcf-project-status-matrix.md` |
| `generate-loop-dashboard.sh` | 状态矩阵 + evidence-index | `gpcf-loop-dashboard.md` |

### 12.9 P7：进入阶段 6——正式实施与交付推进

Loop Engineering 不再只是治理试点，而成为 GPCF 阶段 6 及之后的正式实施机制。

## 13. 项目群统一状态矩阵

GPCF 总仓维护 `09-status/gpcf-project-status-matrix.md`，记录全部 12 个项目的实时状态：

| 字段 | 含义 |
|---|---|
| 项目 | 项目名称 |
| Manifest | 是否具备 PROJECT_HARNESS_MANIFEST.md |
| loop-state | 是否具备 docs/harness/loop-state.md |
| 微循环轮次 | 已完成轮次数 |
| evidence完整率 | 已完成的 evidence 统计 |
| 当前状态 | 状态机节点 |
| 阻塞项 | 当前阻塞项列表 |
| Harness判定 | Harness Governance 判定结果 |
| 下一步 | 建议动作 |

该矩阵是 GPCF 总体状态升级的唯一入口。

## 14. 推荐目录结构

### GPCF 总仓

```
GPCF/
  02-governance/
    gpcf-loop-engineering-spec-v1.md    ← 本文档
    gpcf-status-machine.md
    gpcf-evidence-taxonomy.md
    gpcf-role-boundary.md
    ...（已有治理规范）

  templates/
    loop-state-template.md
    loop-round-template.md
    loop-audit-template.md
    evidence-index-template.md

  08-evidence-samples/
    README.md
    evidence-index.md
    WAES/
    GPC/
    KDS/
    ...（其他项目）

  09-status/
    gpcf-project-status-matrix.md
    gpcf-loop-dashboard.md

  scripts/
    harness/
      （自动化脚本，P6 阶段补齐）
```

### 每个项目仓

```
{project}/
  PROJECT_HARNESS_MANIFEST.md
  docs/harness/
    loop-state.md
    acceptance.md
    blockers.md
    risks.md
    dependency-map.md
    loops/
      loop-round-{ID}.md
    evidence/
      README.md
      evidence-index.md
      command-log-{ID}.txt
      test-result-{ID}.md
      metrics-{ID}.json
      screenshots/
```

## 15. 约束与禁止

| # | 禁止事项 | 检查方式 |
|---|---|---|
| 1 | 无 evidence 的状态升级 | 检查状态字段与 evidence 文件是否匹配 |
| 2 | 循环记录"完成"但无对应文件变更 | 检查 diff / commit 是否存在 |
| 3 | AI 建议直接写入业务事实 | 检查 SUGG → WAES 链路 |
| 4 | 绕过小即做跨项目收口 | 检查总状态文件修改者/来源 |
| 5 | 一个循环同时修改多个不相关模块 | 检查变更文件路径跨度 |
| 6 | 验收层代替执行层修正业务内容 | 检查文件修改者来源 |
| 7 | 自行将状态升级为 accepted/complete | 检查状态变更来源 |
| 8 | GPCF 总控仓作为例外不参与循环 | GPCF 总控仓作为项目群治理中枢，也必须纳入 Loop Engineering，产生 `GPCF-CF-LR-{N}`，不得作为免审计例外 |

P6 阶段将通过自动化脚本执行以上检查。

## 16. 配套文件索引

| 文件 | 路径 | 说明 |
|---|---|---|
| 架构总纲 | `02-governance/gpcf-agent-architecture-six-elements.md` | 六要素顶层设计，本规范的理论锚点 |
| 主规范 | `02-governance/gpcf-loop-engineering-spec-v1.md` | 本文档 |
| 状态机定义 | `02-governance/gpcf-status-machine.md` | 状态转移规则 |
| 证据分类 | `02-governance/gpcf-evidence-taxonomy.md` | evidence 类型与命名 |
| 角色边界 | `02-governance/gpcf-role-boundary.md` | 各角色 CAN/CANNOT |
| 循环状态模板 | `templates/loop-state-template.md` | 项目仓 loop-state.md |
| 循环实例模板 | `templates/loop-round-template.md` | 单轮 loop-round-{ID}.md |
| 审计模板 | `templates/loop-audit-template.md` | 中循环审计报告 |
| 证据索引模板 | `templates/evidence-index-template.md` | 项目仓 evidence-index.md |
| 状态矩阵 | `09-status/gpcf-project-status-matrix.md` | 12 项目实时状态 |

## 17. 版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 规范冻结：循环定义、状态机、evidence分类、角色边界、三层循环、度量阈值、P0-P7路线图、统一编号、证据汇聚约定、配套文件索引 |
