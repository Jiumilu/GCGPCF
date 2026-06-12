---
doc_id: GPCF-DOC-8CDB82A404
title: GlobalCloud 智能体团队下一步执行清单
project: XiaoC
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XiaoG, MMC, GPCF]
domain: agent-team
status: controlled
version: v1.0
owner: XiaoC
kds_space: 开发
kds_path: 开发/08-XiaoC/05-agent-team/GlobalCloud智能体团队下一步执行清单.md
source_path: 05-agent-team/GlobalCloud智能体团队下一步执行清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 智能体团队下一步执行清单

日期：2026-06-12
状态：下一步执行清单 v4
用途：作为小即总控在"12 个交付包完成映射 + 五项目试点启动"后的直接执行清单。
变更：v3→v4 新增 MMC/PKC/Brain/XiaoG 缺口项目执行条目，对齐 Loop Engineering 试点调度。

总目标入口：

- [GlobalCloud智能体团队当前总目标.md](/Users/lujunxiang/Documents/GlobalCloud智慧工厂/GlobalCloud智能体团队当前总目标.md)

## 1. 当前阶段判断

当前阶段变更为：

- 实施前准备收口完成
- 12 个交付包已完成映射（含 MMC/Brain/PKC/XiaoG）
- 6 个专项正式只读预检已完成
- 进入首轮实施前验证准备 + 五项目试点启动
- 总体状态：`in_progress`

当前已完成：

1. 小即团队组织与控制机制
2. Linear 项目台账
3. 半小时自动同步
4. 首版周报
5. 宪衡/链同/厂行/数枢/知源/灵策 6 专项接入
6. 评衡/证验/仓图/接稳 4 横向专项会话建立
7. 第一版真实项目仓库映射与只读预检计划（v2 已覆盖 12 交付包）
8. 第一版实施前准备差距清单
9. 第一版实施前证据与阻塞总表
10. 小即实施前准备完成结论
11. 12 个交付包责任分解表（v2 已补齐 MMC/Brain/PKC/XiaoG）
12. Loop Engineering 全面改进方案（v1.1 已正式绑定试点项目）

当前未完成：

1. MMC、PKC 项目仓库初始化
2. Brain 试点首轮微循环启动（灵策牵头）
3. XiaoG 仓库本地克隆
4. 6 个专项首轮实施前验证包
5. 运行前样本准备
6. 首轮实施前验证入口判断

## 2. 下一阶段预检与启动任务

### 2.1 五项目试点首轮启动（P0）

必须完成：

1. **MMC**：建立项目仓库（GPCF 子目录或独立仓）、建立专属会话、启动首轮微循环（宪衡）
2. **KDS**：已有仓库/会话，继续推进数据指标与 evidence 结构化（数枢）
3. **Brain**：依托现有仓库，灵策牵头启动首轮微循环，建立 KDS↔Brain 联邦数据流依赖（灵策）
4. **PKC**：建立项目仓库、建立专属会话、启动首轮微循环（链同）
5. **GFIS**：依托现有仓库，厂行牵头启动首轮微循环，工厂主链试点（厂行）

### 2.2 链同专项

必须完成：

1. GPC 原型关键对象与接口运行前样本要求
2. GPC 一期蓝图收敛
3. 链侧协同验证包建立
4. PKC 个人工作台状态同步接口设计

### 2.3 厂行专项

必须完成：

1. GFIS 主链运行前样本要求
2. Edge 事实转换样本要求
3. 厂行首轮验证包建立

### 2.4 知源专项

必须完成：

1. Brain remote 补全
2. A19 验收包拆解
3. ingest / 回指 / 失效拦截样本要求
4. 知源首轮验证包建立

### 2.5 宪衡专项

必须完成：

1. EvidenceRecord / StatusAudit / AgentToolGrant 样本要求
2. 连接器治理与规则门运行前样本要求
3. WAES 首轮验证包建立
4. MMC 治理模板基线导出与 Manifest 模板标准化

### 2.6 数枢专项

必须完成：

1. 数据库权限样本要求
2. 读模型只读、DLQ/Replay、Trace/Evidence 样本要求
3. 数枢首轮验证包建立

### 2.7 灵策专项

必须完成：

1. Agent 权限、AISuggestion、越权拦截、主账无写入样本要求
2. 灵策首轮验证包建立
3. Brain 试点首轮微循环，KDS↔Brain 联邦闭环验证

### 2.8 缺口项目建仓（P0/P2）

| 项目 | 优先级 | 牵头 | 动作 |
|---|---|---|---|
| MMC | P0 | 宪衡 | 建仓（GPCF 子目录或独立仓）、建会话、首轮微循环 |
| PKC | P0 | 链同 | 建仓、建会话、首轮微循环 |
| XiaoG | P2 | 接稳 | 克隆仓库 `Jiumilu/XiaoG`、预激活准备 |

## 3. 接入完成后的总控动作

在缺口建仓与试点启动完成后，小即必须执行：

1. 更新专项回报汇总台账（v2）
2. 更新首版周报
3. 更新 GC-9 总控事项
4. 更新 Linear 项目总台账
5. 输出首轮实施前验证入口判断
6. 进入首轮实施前验证准备

## 4. 当前阶段的明确限制

1. 不得把正式只读预检完成写成联调完成
2. 不得把缺运行证据的专项升级到 `ready_for_human_acceptance`
3. 不得把运行前样本要求写成运行通过

## 5. 小即当前下一步

小即当前最直接的下一步：

1. 优先关闭 MMC、PKC 建仓缺口，启动试点首轮微循环
2. Brain 试点由灵策牵头进入首轮微循环
3. 6 个专项首轮实施前验证包继续推进
4. 进入按专项收集运行前样本阶段
5. XiaoG 仓库克隆（P2，非阻塞）

## 6. 本阶段目标切换

当前已正式切换到：

- 首轮实施前验证阶段目标 + 五项目试点 Loop Engineering 首轮微循环
- 核心任务是 6 个专项运行前样本抽取 + 5 试点项目首轮 evidence 产出
- 当前已启动：
  - 宪衡专项第一轮样本抽取 → 扩展至 MMC 试点
  - 知源专项第一轮样本抽取
  - 数枢专项第一轮样本抽取 → 扩展至 KDS 试点

## 7. 当前样本抽取进度

当前已形成：

1. 宪衡：已形成治理对象、审批链、证据链、连接器阻断链样本
2. 知源：已形成 `search/doctor/rag export/evidence gates` 第一批 live 样本
3. 数枢：已形成数据库禁止直写、只读隔离、outbox、trace/evidence 第一批实现侧样本

当前主要未关闭缺口：

1. MMC/PKC 尚无项目仓库
2. Brain remote 仍为空
3. `gbrain import` live 样本未取得
4. `validate_rag_export.py` 当前失败
5. 数枢域仍缺真实 DLQ / Replay / 数据库拒绝返回样本
6. XiaoG 仓库待本地克隆
