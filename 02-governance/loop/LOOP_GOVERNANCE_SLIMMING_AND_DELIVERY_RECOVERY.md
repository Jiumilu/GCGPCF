---
doc_id: GPCF-DOC-LOOP-V11-SLIMMING-DELIVERY-RECOVERY
title: LOOP v1.1 治理瘦身与交付恢复基线
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, PKC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# LOOP v1.1 治理瘦身与交付恢复基线

## 核心判断

当前 LOOP 控制面已经足够强。下一阶段目标不是继续扩展治理能力，而是治理瘦身与交付恢复。

原则：

```text
用最少的治理动作挡住最大的风险，把主要时间还给真实开发。
```

## v1.1 冻结规则

1. 暂停新增 LOOP 治理文档，除非该文档能直接减少开发阻塞或关闭 P0 风险。
2. 暂停新增非 P0 validator，除非该 validator 能降低误报、减少阻断或防止状态误升。
3. 暂停扩展 L4/L5 自治规则。
4. 暂停新增能力族治理。
5. 所有新增治理规则必须证明能减少开发阻塞。
6. 日常开发默认使用 Delivery Loop。
7. 只有 guarded、blocked、状态提升、生产动作、阶段收口才进入 Governance Loop。

## 双 Loop 架构

| Loop | 用途 | 默认强度 | 触发条件 |
|---|---|---|---|
| Delivery Loop | 服务日常开发推进 | 轻量 | 本地开发、mock、fixture、dry-run、普通测试补齐 |
| Governance Loop | 服务审计收口与状态裁决 | 严格 | guarded、blocked、状态提升、生产动作、阶段结束、触碰敏感路径 |

Delivery Loop 每轮只回答：

1. 本轮目标是什么。
2. 改了哪些文件。
3. 怎么验证。
4. 是否触发硬风险。
5. 下一步做什么。

Governance Loop 继续使用 `run / stop / verify / recover / debug`，并保留完整证据、门禁和回滚要求。

## 阶段性治理收口

治理动作从“每轮同步”改为“批处理”：

- 每 5 个 Delivery Loop 做一次 Governance Summary。
- 每个阶段结束做一次治理收口。
- 状态提升前做一次完整审计。

Governance Summary 只回答：

1. 哪些切片完成。
2. 哪些验证通过。
3. 哪些风险仍在。
4. 有没有越权。
5. 有没有状态提升申请。
6. 哪些 evidence 应进入 KDS。

已登记开发切片未达到 5 个时，不强制生成实际 Summary 文档；一旦达到 5 个 Delivery Loop，必须先收口再进入状态提升、提交候选或下一阶段治理判断。达到 5 个 Delivery Loop 后的首个收口证据为 `docs/harness/evidence/loop-v11-delivery-governance-summary-20260628.md`。

## 三档治理强度

| 档位 | 适用场景 | 证据要求 |
|---|---|---|
| G0 快速开发 | 纯本地、mock、无敏感边界 | 切片结束一条记录 |
| G1 受控开发 | 普通项目主开发、多文件、测试、接口契约 | 每切片 1 个 round + 1 个验证结果 |
| G2 严格治理 | KDS、WAES、生产配置、真实 API、schema、状态提升 | 完整 `run / stop / verify / recover / debug` |

## 当前项目建议状态

| 项目 | lifecycle | loop_mode | autonomy_level | risk_gate | governance_intensity | priority |
|---|---|---|---|---|---|---|
| GPCF | governance | evolve | L2 | partial | G1/G2 | 治理瘦身，不再扩张 |
| GFIS | dev | build | L3_candidate | partial | G1 | runtime SOP E2E 最小闭环 |
| KDS | dev | audit | L2 | partial | G2 | KDS blocker 已解除；保持 hold review、dry-run 和真实 KDS API 未授权边界 |
| WAES | governance | audit | L1/L2 | guarded | G2 | 裁决层，不参与日常开发 |
| SOP/PKC | maintenance | verify | L2 | partial | G0/G1 | 专项验证和小切片维护 |

## L3.5 / L4 延后规则

只有当 GFIS 同时出现以下非零真实业务计数后，才允许讨论 `L3 -> L3.5`、GFIS `dev -> staging` 或 L4 自动运营候选：

- runtime intake > 0。
- review queue > 0。
- WAES review > 0。
- verified artifact candidate > 0。

在上述计数保持 0 时，不扩展 L4/L5，不启动 L3.5/L4 评估，不声明 accepted、integrated、production_ready 或 customer_accepted。

## 非声明边界

- 本基线不创建 GFIS source-of-record。
- 本基线不创建 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本基线不授权生产写入、真实外部 API 写入、schema migrate、bench migrate、commit、push 或 deploy。
- 本基线不声明 accepted、integrated、production_ready 或 customer_accepted。

## 验收标准

- 没有新的治理文档继续扩大控制面。
- 开发任务可以通过 Delivery Loop 启动。
- 专项治理 validator 漂移不阻断 GFIS 本地开发。
- P0 风险仍然硬阻断。
- 状态提升、发布和生产动作仍必须进入 Governance Loop 与人工确认。
