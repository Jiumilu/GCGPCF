---
doc_id: GPCF-DOC-B2A5E41836
title: GlobalCloud 绿色供应链体系项目群控制表
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, XiaoG, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud智慧工厂项目群控制表.md
source_path: 01-architecture/GlobalCloud智慧工厂项目群控制表.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系项目群控制表

日期：2026-06-07
用途：作为 GlobalCloud 绿色供应链体系项目群架构设计后的执行跟踪入口。当前表格只反映本轮只读采样证据，不代表生产完成状态。
当前口径：主架构采用治理与监控层、运营与协同层、生产与执行层；四流采用治理流、业务流、数据流、AI 服务流；WAES 只做规则、监控、治理、证据、状态和 AI 授权，不审批具体事务。

当前补充口径：阅读本表时，平台主线统一按 `GPC` 理解，宪法内容统一按 `WAES` 治理约束理解。
当前实施控制补充口径：项目群推进统一采用多智能体协同实施机制，按交付包进行项目控制；当前 `100 分` 仅代表设计基线完备度，不代表真实联调和试运行已经完成。

| 项目 | 路径 | 当前分支/状态证据 | 绿色供应链体系角色 | 第一优先级动作 | 风险/阻塞 |
|---|---|---|---|---|---|
| GFIS | `/Users/lujunxiang/Projects/GlobalCloud GFIS` | `codex/gcfis-demo-v0.1`，ahead 1，工作区有大量修改/未跟踪文件 | 单厂本地执行核心：MES、QMS、WMS、LES、EAM、发货事实 | 冻结 dirty state；补 LES 最小对象；输出 GFIS 只读事件/API 合同 | 不可覆盖既有改动；外部 UAT/生产证据仍需人工确认 |
| GPC（目标主线）/ Odoo GPC（历史原型） | 目标主线待建；现有原型 `/Users/lujunxiang/Projects/GlobalCloud GPC` | 现有 Odoo 原型为 `19.0`，ahead 18，双 remote：`origin=odoo/odoo`、`fork=Jiumilu/odoo` | 轻量绿色供应链协同平台、TMS、外部协同、供应商/客户/监管平台；Odoo 降级为 back-office connector 候选 | 冻结 Odoo core 二开；建立 GPC ADR、对象目录、事件合同；定义 GFIS-GPC 订单、发货、签收、回单映射 | 不再继续维护私有 Odoo 发行版；目标主线需新建或重构 |
| WAES | `/Users/lujunxiang/Documents/Codex Space/WAES` | 轻量确认 `waes/integration-release`，完整 dirty state 未确认 | 治理与监控中枢、Agent Desktop、证据台账、规则审批、状态审计 | 建只读控制塔连接器、Evidence Ledger 和治理规则台账 | Git 状态检查较慢；不能作为业务主账，不能承办具体事务审批 |
| PVAOS | `/Users/lujunxiang/Documents/Codex Space/PVAOS` | 轻量确认 `pvaos/pm-governance`，完整 dirty state 未确认 | 价值联盟门户、组织/项目/伙伴接入 | 对齐租户、组织、项目、伙伴 ID 与 GPC/GFIS | Git 状态检查较慢；不承载生产执行 |
| Brain | `/Users/lujunxiang/Projects/GlobalCloud Brain` | `master`，无 remote 输出，工作区大量修改/未跟踪文件 | SOP、知识库、RAG、案例、复盘 | 纳入 V3.1、GFIS/GPC 规则和异常 SOP；建立 RAG 准入 | Knowledge 不是运行事实；doctor/索引状态需单独验收 |
| XiaoC | `/Users/lujunxiang/Projects/GlobalCloud XiaoC` | `develop`，ahead 22，工作区大量修改/未跟踪文件 | Prompt/MCP/模型适配/Agent prompt 资产 | 建 8 类智慧工厂 Agent prompt 模板和评估样例 | 当前 Harness 状态仍 partial；Wrangler/测试阻塞需隔离 |
| XiaoG Agent | `/Users/lujunxiang/Projects/hermes-webui` | `codex/health-100`，有 Harness 未跟踪文件 | 持续运行 Agent Web 控制台和后台任务入口 | 只读监控 WAES/GFIS/GPC，生成日报/预警/待办 | 不得读写真实用户状态或绕过治理授权和业务系统确认 |
| XGD | `/Users/lujunxiang/Projects/GlobalCloud XGD` | `codex/xgd-harness-100`，双 remote：`origin=Jiumilu/XGD`、`xiaog=Jiumilu/XiaoG` | 大象：长程 Agent、重分析、多端交互和复杂任务承载 | 设计班组长/调度/设备/质量语音查询与异常上报 | 当前状态有 runtime/release blockers；不得发布或签名 |
| Harness 控制台 | `/Users/lujunxiang/Projects/GlobalCloud开发控制台` | 当前目录不是 Git 仓库 | 工程治理标准、项目注册、Manifest、验收清单 | 建绿色供应链体系总 Manifest 和阶段验收矩阵 | 不是业务系统；不能替代当前项目现场证据 |

## 下一步执行顺序

1. 先按四流专项基线冻结接口边界：连接器合同、SOP 模板、AI 服务模型、数据治理模型、多厂协同模型、Edge 接入安全模型。
2. 冻结 GFIS/现有 Odoo GPC/WAES/PVAOS 当前 Git 与 dirty state。
3. 将 `Domain Object Catalog`、`Event Contracts` 和 A10-A18 验收场景同步到项目级实施计划。
4. 以 GFIS 为核心做一期订单到交付闭环，同时验证连接器降级、DLQ/重放和 AI 越权拦截。
5. 用 WAES 做治理控制塔，不写 GFIS/GPC 事实。
6. 用 Brain/XiaoC（蚁后）/Hermes/XGD（大象） 做 AI 辅助，不越过 L3/L4/L5 授权边界。
7. 具体事务确认留在 GFIS/GPC；WAES 只做治理规则、证据确证、状态升级和 AI 授权。
8. 在真实运行态联调和人工验收前，项目群状态不得标记为 `complete`。

## 实施组织与项目控制补充

### 多智能体实施组织

1. 总控智能体：统一负责任务拆分、集成、评分、状态升级和定版。
2. 专业智能体：治理架构、协同业务、工厂执行、数据平台、资源仓库、知识体系、AI 服务、连接器可靠性。
3. 审计智能体：评估审计、证据验收。

### 项目控制维度

项目群实施阶段统一按以下维度控制：

1. 交付包完成率
2. 对象补齐率
3. 事件补齐率
4. 验收场景补齐率
5. 设计基线得分
6. 边界冲突数
7. AI 越权风险未闭合数
8. 数据库边界未闭合数
9. 状态升级准确率
10. 证据完整率

### 当前阶段控制结论

1. 当前工作区已达到设计基线完备度 100/100。
2. 当前体系成熟度仍为 `L3 可实施级`。
3. 后续主任务不再是补总体口径，而是推进交付包骨架、联调准备和试运行验证。
