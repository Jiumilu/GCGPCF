# GlobalCloud 智能体团队真实项目仓库映射与只读预检计划

日期：2026-06-08  
状态：实施前准备工作文件 v1  
用途：在不进入真实代码修改的前提下，为小即团队 10 个固定专项建立真实项目仓库映射、只读预检顺序和证据采集口径（其中 6 个正式专项已接入，4 个会话为显性待启动）。

## 1. 当前前提

1. 当前总工作区为 `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`，用于总控、台账、周报和治理文档。
2. 当前文档工作区不是 Git 仓库，不能提供实施仓库级分支、remote、dirty state 证据。
3. 本文件只解决“实施前准备进入哪里看、先看什么、拿什么证据”，不等于已开始真实实施。
4. 当前已接入专项回报为 10 个固定专项中的 6/6：
   - 宪衡
   - 链同
   - 厂行
   - 数枢
   - 知源
   - 灵策
   - 评衡（未启动）
   - 证验（未启动）

## 2. 当前已确认仓库证据

以下证据来自 2026-06-08 的只读 Git 预检。

| 仓库 | 路径 | 当前分支 | Git 状态证据 | Remote 证据 | 当前判断 |
|---|---|---|---|---|---|
| WAES | `/Users/lujunxiang/Documents/Codex Space/WAES` | `waes/integration-release` | 工作区存在修改 | `origin=https://github.com/Jiumilu/WAES.git` | 可进入 WAES 域只读预检 |
| PVAOS | `/Users/lujunxiang/Documents/Codex Space/PVAOS` | `pvaos/pm-governance` | dirty state 本轮未成功返回，至少已确认在 Git 仓库内 | `origin=https://github.com/Jiumilu/PVAOS.git` | 可进入 PVAOS 域只读预检，但需补 dirty state 证据 |
| GFIS | `/Users/lujunxiang/Projects/GlobalCloud GFIS` | `codex/gcfis-demo-v0.1` | `ahead 1`，且存在修改 | `origin=https://github.com/Jiumilu/gcfis.git` | 可进入 GFIS 域只读预检 |
| GPC（现有原型） | `/Users/lujunxiang/Projects/GlobalCloud GPC` | `19.0` | `ahead 18`，有未跟踪标准化文件 | `origin=odoo/odoo`，`fork=Jiumilu/odoo` | 仅作为 Odoo 原型只读预检，不代表 GPC-Native 已建成 |
| Brain | `/Users/lujunxiang/Projects/GlobalCloud Brain` | `master` | 工作区存在修改 | 本轮未返回 remote | 可进入知源域只读预检 |
| XiaoC | `/Users/lujunxiang/Projects/GlobalCloud XiaoC` | `develop` | `ahead 22`，且存在修改 | `origin=linshenkx/prompt-optimizer`，`fork=Jiumilu/prompt-optimizer` | 可进入 AI 服务域只读预检 |
| Hermes | `/Users/lujunxiang/Projects/hermes-webui` | `codex/health-100` | 存在未跟踪 Harness 文件 | `origin=https://github.com/nesquena/hermes-webui.git` | 可进入 AI 服务域只读预检 |
| XGD | `/Users/lujunxiang/Projects/GlobalCloud XGD` | `codex/xgd-harness-100` | 本轮未见 dirty 输出 | `origin=Jiumilu/XGD`，`xiaog=Jiumilu/XiaoG` | 可进入 AI 服务域只读预检 |

## 3. 10 个固定专项的真实项目仓库映射

### 3.1 宪衡专项

- 专项范围：WAES 治理与控制塔包
- 主仓库：
  - `/Users/lujunxiang/Documents/Codex Space/WAES`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系WAES控制塔与治理门禁图.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系知识与Agent授权治理总表.md`
- 当前说明：
  - 设计边界已稳定
  - 真实运行证据仍未采集

### 3.2 链同专项

- 专项范围：PVAOS 生态入口包 + GPC-Native 运营协同包
- 主仓库：
  - `/Users/lujunxiang/Documents/Codex Space/PVAOS`
  - `/Users/lujunxiang/Projects/GlobalCloud GPC`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/ADR-GPC从Odoo二开调整为原生协同中台.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系对象目录.md`
- 当前说明：
  - 当前只能对 PVAOS 和现有 Odoo GPC 原型做预检
  - `GPC-Native` 仍是目标主线，不是现成独立仓库

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
  - LLM Wiki / GBrain 仍属于知识引擎候选能力，不可直接当作正式知识真源

### 3.6 灵策专项（AI 服务）

- 专项范围：XiaoC + Hermes + XGD AI 服务包
- 主仓库：
  - `/Users/lujunxiang/Projects/GlobalCloud XiaoC`
  - `/Users/lujunxiang/Projects/hermes-webui`
  - `/Users/lujunxiang/Projects/GlobalCloud XGD`
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系AI服务模型.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud绿色供应链体系整体评估模型与100分优化方案.md`
- 当前说明：
  - 真实工具权限、模型调用、越权拦截、知识回指必须回到这些仓库与运行配置验证

### 3.7 评衡专项（评估审计）

- 专项范围：评估复评、评分门禁、偏差复核与复核节奏
- 主仓库：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂`（控制台账与模型）
- 只读辅助证据：
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队实施前证据与阻塞总表.md`
  - `/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队PMBOK项目管理台账.md`
- 当前说明：
  - 评估审计为显性会话，待启动后按 `GlobalCloud智能体团队实施前准备差距清单` 中条目继续补齐样本

### 3.8 证验专项（证据验收）

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

## 5. 6 个专项的预检重点

| 专项 | 第一预检重点 | 第二预检重点 | 第三预检重点 |
|---|---|---|---|
| 宪衡 | WAES Git 与 dirty state | 治理对象/事件/门禁实现位置 | 真实 Evidence/Status/Agent 授权样本可行性 |
| 链同 | PVAOS 组织/项目/伙伴入口 | GPC 原型中订单/ASN/预约/运输/POD 相关实现 | GPC-Native 与 Odoo 原型切换边界 |
| 厂行 | GFIS 工单/质量/库存/批次/发货主线 | Edge 与 GFIS 的事实转换点 | 是否存在外部直写工厂主账风险 |
| 数枢 | 数据库边界与访问口径 | 读模型、Event、Replay、DLQ、Evidence/Trace 链路 | 跨系统直写阻断与幂等设计 |
| 知源 | Brain 中知识治理/准入/审计位置 | 正式知识主存与知识引擎分层证据 | 失效治理与引用回指可行性 |
| 灵策 | XiaoC 模型/Prompt/工具权限 | Hermes/XGD Agent 运行与回执链 | AI 越权拦截与无主账写入证据 |
| 评衡 | 评分复评入口与偏差样本 | PMBOK 复核口径、范围/进度/成本/质量偏差 | A7/A9/A13/A19/A20 放行样本与复核闭环 |
| 证验 | 证据签核与人审闭环 | 证据看板、签核记录与阻塞关闭证据 | A7/A9/A13/A19/A20 样本归档与状态升级条件 |

## 6. 当前限制

1. 当前文件只解决“进哪里看”和“先核什么”，不解决“是否已通过预检”。
2. 在完成各专项只读预检前，不得把当前状态写成：
   - 实施已开始完成
   - 联调已完成
   - 试运行已完成
   - `complete`

## 7. 当前结论

当前已经完成：

1. 6 个专项的真实项目仓库映射
2. 第一版只读预检顺序与检查口径
3. 当前可进入真实仓库只读预检的范围定义
4. 6/6 专项首轮正式回报已经接入完成

当前仍未完成：

1. 6 个专项逐仓库只读预检结果
2. 基于真实仓库证据的正式只读预检结论
3. 运行前样本验证
