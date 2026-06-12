# GlobalCloud 智能体团队真实项目仓库映射与只读预检计划

日期：2026-06-12
状态：实施前准备工作文件 v2
用途：在不进入真实代码修改的前提下，为小即团队 11 个智能体对应 12 个交付包建立真实项目仓库映射、只读预检顺序和证据采集口径。
变更：v1→v2 新增 MMC/PKC/XiaoG 三个缺口项目仓库映射，补齐仓图/接稳专项章节，对齐 12 个交付包责任分解表。

## 1. 当前前提

1. 当前总工作区为 `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`，用于总控、台账、周报和治理文档。
2. 当前文档工作区不是 Git 仓库，不能提供实施仓库级分支、remote、dirty state 证据。
3. 本文件只解决"实施前准备进入哪里看、先看什么、拿什么证据"，不等于已开始真实实施。
4. 当前专项回报接入状态：
   - 已接入首轮回报：宪衡、链同、厂行、数枢、知源、灵策（6/11）
   - 已建显性会话待启动：仓图、接稳、评衡、证验（4/11）
   - 新增缺口项目（待建仓/待克隆）：MMC、PKC、XiaoG

## 2. 当前已确认仓库证据

以下证据来自 2026-06-08 的只读 Git 预检（部分缺口项目已在 2026-06-12 补充）。

| 仓库 | 路径 | 当前分支 | Git 状态证据 | Remote 证据 | 当前判断 |
|---|---|---|---|---|---|
| WAES | `/Users/lujunxiang/Documents/Codex Space/WAES` | `waes/integration-release` | 工作区存在修改 | `origin=https://github.com/Jiumilu/WAES.git` | 可进入 WAES 域只读预检 |
| PVAOS | `/Users/lujunxiang/Documents/Codex Space/PVAOS` | `pvaos/pm-governance` | dirty state 本轮未成功返回，至少已确认在 Git 仓库内 | `origin=https://github.com/Jiumilu/PVAOS.git` | 可进入 PVAOS 域只读预检，但需补 dirty state 证据 |
| GFIS | `/Users/lujunxiang/Projects/GlobalCloud GFIS` | `codex/gcfis-demo-v0.1` | `ahead 1`，且存在修改 | `origin=https://github.com/Jiumilu/gcfis.git` | 可进入 GFIS 域只读预检 |
| GPC（现有原型） | `/Users/lujunxiang/Projects/GlobalCloud GPC` | `19.0` | `ahead 18`，有未跟踪标准化文件 | `origin=odoo/odoo`，`fork=Jiumilu/odoo` | 仅作为 Odoo 原型只读预检，不代表 GPC-Native 已建成 |
| Brain | `/Users/lujunxiang/Projects/GlobalCloud Brain` | `master` | 工作区存在修改 | 本轮未返回 remote | 可进入灵策域只读预检（知源协同知识治理入口） |
| XiaoC | `/Users/lujunxiang/Projects/GlobalCloud XiaoC` | `develop` | `ahead 22`，且存在修改 | `origin=linshenkx/prompt-optimizer`，`fork=Jiumilu/prompt-optimizer` | 可进入 AI 服务域只读预检 |
| Hermes | `/Users/lujunxiang/Projects/hermes-webui` | `codex/health-100` | 存在未跟踪 Harness 文件 | `origin=https://github.com/nesquena/hermes-webui.git` | 可进入 AI 服务域只读预检 |
| XGD | `/Users/lujunxiang/Projects/GlobalCloud XGD` | `codex/xgd-harness-100` | 本轮未见 dirty 输出 | `origin=Jiumilu/XGD`，`xiaog=Jiumilu/XiaoG` | 可进入 AI 服务域只读预检 |
| XiaoG | 待克隆 | - | 未确认 | `origin=Jiumilu/XiaoG`（已在 XGD remote 中识别） | 需独立克隆 XiaoG 仓库，ESP32 语音硬件接入 |
| MMC | 待建仓 | - | 无仓库 | `https://github.com/Jiumilu/GCGPCF`（项目群主仓，需确认独立仓路径） | 尚无独立项目仓库，试点期可先以 GPCF 子目录启动 |
| PKC | 待建仓 | - | 无仓库 | 待确认 | 尚无独立项目仓库，与链同域 PKC 交付包对齐 |

## 3. 专项（对应交付包）的真实项目仓库映射

### 3.1 宪衡专项

- 专项范围：WAES 治理与控制塔包、MMC 管理配置中心包
- 主仓库：
  - `/Users/lujunxiang/Documents/Codex Space/WAES`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md`
- 当前说明：
  - 设计边界已稳定
  - 真实运行证据仍未采集
  - MMC 尚无独立仓库，试点期可依托 WAES 仓库或 GPCF 子目录启动

### 3.2 链同专项

- 专项范围：PVAOS 生态入口包 + GPC-Native 运营协同包 + PKC 个人知识工作台包
- 主仓库：
  - `/Users/lujunxiang/Documents/Codex Space/PVAOS`
  - `/Users/lujunxiang/Projects/GlobalCloud GPC`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/ADR-GPC从Odoo二开调整为原生协同中台.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对象目录.md`
- 当前说明：
  - 当前只能对 PVAOS 和现有 Odoo GPC 原型做预检
  - `GPC-Native` 仍是目标主线，不是现成独立仓库
  - PKC 尚无独立仓库，试点期可依托 PVAOS 仓库或独立建仓启动

### 3.3 厂行专项

- 专项范围：GFIS 工厂执行包 + Edge 边缘接入包
- 主仓库：
  - `/Users/lujunxiang/Projects/GlobalCloud GFIS`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对象目录.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系事件合同.md`
- 当前说明：
  - GFIS 有真实仓库
  - Edge 当前没有独立确认仓库，应按 GFIS 相关实现与架构文档联合预检

### 3.4 数枢专项

- 专项范围：AI 与数据底座包
- 主证据仓库：
  - `/Users/lujunxiang/Documents/Codex Space/WAES`
  - `/Users/lujunxiang/Documents/Codex Space/PVAOS`
  - `/Users/lujunxiang/Projects/GlobalCloud GFIS`
  - `/Users/lujunxiang/Projects/GlobalCloud GPC`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系数据治理模型.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系系统-数据库边界总表.md`
- 当前说明：
  - 数枢不是单一业务仓库
  - 实施前预检必须跨仓库采样数据库边界、事件、读模型和证据链

### 3.5 知源专项

- 专项范围：企业级知识主存与知识引擎包
- 主仓库：
  - `/Users/lujunxiang/Projects/GlobalCloud Brain`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系企业级知识库方案.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识主存层与知识引擎层分层方案.md`
- 当前说明：
  - Brain 是当前知识域主仓库
  - KDS 为企业级知识主存（canonical source），Brain 为知识 UI 平台；LLM Wiki 为知识编制工具

### 3.6 灵策专项（AI 服务）

- 专项范围：XiaoC + Hermes + XGD AI 服务包、Brain 智能知识平台包
- 主仓库：
  - `/Users/lujunxiang/Projects/GlobalCloud XiaoC`
  - `/Users/lujunxiang/Projects/hermes-webui`
  - `/Users/lujunxiang/Projects/GlobalCloud XGD`
  - `/Users/lujunxiang/Projects/GlobalCloud Brain`（Brain UI 层协同）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系AI服务模型.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md`
- 当前说明：
  - 真实工具权限、模型调用、越权拦截、知识回指必须回到这些仓库与运行配置验证

### 3.7 仓图专项

- 专项范围：资源仓库域、11 池映射、扩池能力（横向）
- 主证据仓库：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`（控制台账与映射总表）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系资源仓库-业务对象映射总表.md`
- 当前说明：
  - 资源仓库当前仍停留在规划和映射汇总阶段
  - 尚未形成任务化执行清单与运行前采集样本

### 3.8 接稳专项

- 专项范围：连接器可靠性、DLQ/Replay/降级方案、XiaoG 本地语音助手包（横向）
- 主证据仓库：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`（控制台账与连接器合同）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系连接器合同.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系事件合同.md`
- 当前说明：
  - 连接器与可靠性主线已建显性会话，运行证据未启动
  - XiaoG ESP32 语音硬件接入规范预研中，仓库待独立克隆

### 3.9 MMC 管理配置中心（缺口项目，试点 P1）

- 专项范围：MMC 管理配置中心包（宪衡牵头、链同协同）
- 主仓库：
  - 待建仓：尚无独立项目仓库
  - 试点期建议路径：GPCF 子目录 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/mmc/` 或 WAES 仓库内子模块
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队12个交付包责任分解表.md`（第 2.9 节）
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队Loop Engineering全面改进方案.md`（第 5 节）
- 当前说明：
  - 交付包已正式定义：治理模板基线、配置标准化、管理控制台、项目初始化模板
  - 当前五试点之一，目标轮次 3 轮
  - 首轮重点：治理模板基线导出与 Manifest 模板标准化

### 3.10 PKC 个人知识工作台（缺口项目，试点 P1）

- 专项范围：PKC 个人知识工作台包（链同牵头、灵策协同）
- 主仓库：
  - 待建仓：尚无独立项目仓库
  - 试点期建议路径：可依托 PVAOS 仓库子模块或独立建仓
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队12个交付包责任分解表.md`（第 2.11 节）
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队Loop Engineering全面改进方案.md`（第 5 节）
- 当前说明：
  - 交付包已正式定义：个人仪表盘、端到端用户知识闭环、任务与通知中心
  - 当前五试点之一，目标轮次 3 轮
  - 首轮重点：个人工作台状态同步接口与用户闭环验证

### 3.11 XiaoG 本地语音助手（缺口项目，预激活 P2）

- 专项范围：XiaoG 本地语音助手包（接稳牵头、厂行协同）
- 主仓库：
  - 待克隆：`origin=Jiumilu/XiaoG`（已在 XGD 仓库 remote 中识别）
  - 建议克隆路径：`/Users/lujunxiang/Projects/GlobalCloud XiaoG`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队12个交付包责任分解表.md`（第 2.12 节）
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队Loop Engineering全面改进方案.md`（第 5.3 节）
- 当前说明：
  - 交付包已正式定义：ESP32 语音硬件接入、WebSocket 连接可靠性、离线缓存与补传
  - 非试点项目，预激活准备阶段
  - 接稳需产出 XiaoG ESP32 接入规范首版与 WebSocket 可靠性基线文档

### 3.12 评衡专项（评估审计）

- 专项范围：评估复评、评分门禁、偏差复核与复核节奏
- 主仓库：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`（控制台账与模型）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前证据与阻塞总表.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队PMBOK项目管理台账.md`
- 当前说明：
  - 评估审计为显性会话，待启动后按 `GlobalCloud智能体团队实施前准备差距清单` 中条目继续补齐样本

### 3.13 证验专项（证据验收）

- 专项范围：证据签核、状态升级放行、阻塞关闭记录
- 主仓库：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`（控制台账与验收条款）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前证据与阻塞总表.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队PMBOK项目管理台账.md`
- 当前说明：
  - 证验为显性会话，待启动后形成统一证据看板与签核闭环

## 4. 只读预检统一步骤

每个专项进入真实项目仓库前，统一执行以下只读步骤：

1. `pwd`
2. `git branch --show-current`
3. `git status --short --branch`
4. `git remote -v`
5. 只读确认当前仓库与专项边界是否一致
6. 只读采样专项相关目录、核心文档、配置或接口定义
7. 记录：
   - 当前分支
   - dirty state
   - remote
   - 与专项责任边界的符合度
   - 当前阻塞

## 5. 全量专项的预检重点

| 专项 | 第一预检重点 | 第二预检重点 | 第三预检重点 |
|---|---|---|---|
| 宪衡 | WAES Git 与 dirty state | 治理对象/事件/门禁实现位置 | 真实 Evidence/Status/Agent 授权样本可行性 |
| 链同 | PVAOS 组织/项目/伙伴入口 | GPC 原型中订单/ASN/预约/运输/POD 相关实现 | GPC-Native 与 Odoo 原型切换边界 |
| 厂行 | GFIS 工单/质量/库存/批次/发货主线 | Edge 与 GFIS 的事实转换点 | 是否存在外部直写工厂主账风险 |
| 数枢 | 数据库边界与访问口径 | 读模型、Event、Replay、DLQ、Evidence/Trace 链路 | 跨系统直写阻断与幂等设计 |
| 知源 | KDS 知识治理/准入/审计 | 正式知识主存与知识引擎分层证据 | 失效治理与引用回指可行性 |
| 灵策 | XiaoC 模型/Prompt/工具权限 | Hermes/XGD Agent 运行与回执链、Brain UI 层联邦闭环 | AI 越权拦截与无主账写入证据 |
| 仓图 | 11 池映射完整性 | 资源池扩展边界与权限模型 | 跨项目资源引用闭环 |
| 接稳 | DLQ/Replay 样本与重放闭环 | 连接器合同执行态验证 | XiaoG ESP32 接入规范与 WebSocket 可靠性基线 |
| **MMC** | 治理模板基线导出 | 配置标准化模型落地 | Manifest 模板与项目初始化路径 |
| **PKC** | 个人工作台状态同步接口 | 端到端用户知识闭环验证 | 跨项目状态同步接口实现 |
| **XiaoG** | ESP32 硬件接入规范 | WebSocket 连接可靠性机制 | OT/IT 边界安全与离线补传 |
| 评衡 | 评分复评入口与偏差样本 | PMBOK 复核口径、范围/进度/成本/质量偏差 | A7/A9/A13/A19/A20 放行样本与复核闭环 |
| 证验 | 证据签核与人审闭环 | 证据看板、签核记录与阻塞关闭证据 | A7/A9/A13/A19/A20 样本归档与状态升级条件 |

## 6. 当前限制

1. 当前文件只解决"进哪里看"和"先核什么"，不解决"是否已通过预检"。
2. MMC、PKC 两个试点项目尚无独立项目仓库，需先建仓再执行只读预检。
3. XiaoG 仓库 remote 已识别但未本地克隆，需先克隆再预检。
4. 在完成各专项只读预检前，不得把当前状态写成：
   - 实施已开始完成
   - 联调已完成
   - 试运行已完成
   - `complete`

## 7. 当前结论

当前已经完成：

1. 6 个已有仓库专项的真实项目仓库映射
2. 4 个横向/审计专项（仓图、接稳、评衡、证验）的映射与预检入口
3. 3 个缺口项目（MMC、PKC、XiaoG）的交付包-仓库映射与建仓建议
4. 第一版只读预检顺序与检查口径
5. 当前可进入真实仓库只读预检的范围定义

当前仍未完成：

1. 6 个已有仓库专项逐仓库只读预检结果
2. MMC、PKC 项目仓库初始化
3. XiaoG 仓库本地克隆
4. 基于真实仓库证据的正式只读预检结论
5. 运行前样本验证
