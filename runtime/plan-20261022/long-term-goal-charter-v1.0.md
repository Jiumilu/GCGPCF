---
doc_id: GPCF-DOC-LONG-TERM-GOAL-CHARTER-20261022
title: 项目群长期目标实施章程 v1.0（2026-10-22）
project: GPCF
related_projects: [GPCF, WAE, WAME, PKC, GFIS, GPC, KDS, XWAIL, XiaoC, FireQuote]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/runtime/plan-20261022/long-term-goal-charter-v1.0.md
source_path: runtime/plan-20261022/long-term-goal-charter-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群长期目标实施章程 v1.0（2026-10-22）

## 1. 长期目标

按《GlobalCloud 项目群完成度与综合能力提升_任务优先级清单_v1.0》（45 项，P0 11 / P1 23 / P2 11）持续实施，提升：
1. **完成度双账本**：`C_dev` 与 `C_real`；
2. **六维能力**：K1–K6（架构、交付、真实业务、治理、复用、可观测）；
3. **证据与门禁**：每个 Feature 可回放，禁止无证据状态提升。

**Goal ID**：`goal-b0948e79-29b1-41af-b922-417dbcc455b1`（max 30 rounds）。

## 2. 基线（2026-10-22；最近刷新 2026-10-24 00:30，Goal Round 155）

| 指标 | 当前 | 90 天目标 |
|---|---|---|
| `C_dev` | **37.53%**（VU 97 / 权重和 105；5 处阶段按证据修正） | ≥ 55.00% |
| `C_real` | **0.00%** | ≥ 12.00% |
| 六维能力 K | **≈ 24.60 / 100**（估算；K3 55 / K4 48 / K5 32） | 37（P0 目标） |
| 活跃 Feature | 19（closed 18） | 按计划收敛 |
| 项目范围 | 29（FireQuote 新纳入；caliber baseline pass） | 29 或回 28 |
| 契约冲突 | 8/8 closed | 维持 |
| 批次 2 前置 | 0/2 | 外部输入后 ≥ 2/2 |
| 口径基线校验 | `validate_project_group_caliber_baseline.py` pass（project_count=29） | 每次刷新必过 |

## 3. 阶段划分

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 基线 | 双账本、口径基线、dirty 分类、单一授权台账、证据规则冻结 | 已完成 |
| P1 交付 | 45 项中的 P0/P1：Feature 收口、WAE/PKC 接入、契约统一、状态页 | 进行中 |
| P2 真实业务 | 批次 2/3、真实 SOR、外部 runtime、PMC 幂等、Hermes 对外 | 待外部输入/授权 |
| P3 规模化 | 28/29 项目逐页覆盖、能力复用、季度评审 | 未开始 |

## 4. 每轮工作协议

1. **选择**：用 `decide_template(priority_rank)` + 问答选项确定本轮任务。
2. **执行**：优先本地可验证；跨仓需授权；不 commit/push/deploy；不做状态提升。
3. **证据**：每轮产出可回放证据（命令/输出/路径）与门禁结果。
4. **记录**：追加 `runtime/plan-20261022/wave0-report.md` 对应章节。
5. **收口**：只有证据齐全且授权到位的 Feature 才进入关闭流程；关闭必须用户确认。

## 5. 授权与红线

- 需要授权/确认：一律问答 + 决策模型概率（红线先 `gate(rule="redline")`）。
- 红线：删除 L2+、凭据创建/外发、生产写入/发布、对外承诺、状态提升。
- 决策模型六类开关常开（policy 0.3.0），关闭即红线。

## 6. 指标与复盘

- 每周：C_dev/C_real、活跃 Feature、门禁通过率、未决授权项。
- 每两周：K1–K6 评分与瓶颈复盘。
- 每轮结束：更新本文件基线表与 wave0-report。

## 7. 当前未决项

| 项 | 状态 | 下一步 |
|---|---|---|
| F-036 PKC 接入 | conditional | 六门 pass；本地 dev 嵌入验证通过；生产/CSP/SSO/403、正式评审待做 |
| F-035 WAME 侧栏 | **closed** | 契约消费+tsc+5/5+E2E 冒烟；FunctionPanel 独立、file: 依赖决策；私有 registry 另立 |
| 批次 2 | 0/2（龄期 1 天） | 业务方 5 类单据、GPC PG-11；3 工作日（10-27）升级 |
| 契约残留 | 已收口部分 | 漂移告警/packageRef schema 已落；强制签名代码/packageRef 运行时/域名迁移待做 |
| FireQuote 29 口径 | 已补 OpenSpec/技能链/实施方案台账；caliber pass | 范围/分母确认 |
| 多仓未提交 | GPCF 1118 dirty | 按显式路径分批提交（需授权） |
| 门禁/测试 | 11/11 pass；pytest 60/60 | 保持 |
| 剩余 P2 任务 | 未开始 | 按清单推进 |
| 活跃 Feature | 19；已关闭 F-024/F-026/F-027/F-030 | 继续按证据关闭 |

## 8. 非声明

- 本文件是实施章程，不声明任何项目已达成目标；
- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明 90 天目标已实现。
