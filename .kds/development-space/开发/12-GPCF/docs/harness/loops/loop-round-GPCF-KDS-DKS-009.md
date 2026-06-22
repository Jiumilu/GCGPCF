---
doc_id: GPCF-DOC-820B756EF3
title: GPCF-KDS-DKS-009 葛化 GFIS AI 助手首批问答与文档验收评测集 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-009.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-009.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-009 葛化 GFIS AI 助手首批问答与文档验收评测集 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

上一轮 `GPCF-KDS-DKS-008` 已完成葛化第一阶段 GFIS AI 助手三件套实施清单，并建议本轮建立首批问答与文档验收评测集。

本轮默认采用以下实施方向：

1. 三类助手先进入项目组内部试用，再开放给合作单位。
2. 文档验收助手优先覆盖辽宁远航链路与现代精工 OEM 过渡资料。
3. 金融凭证资料默认只做脱敏索引，不进入开放问答。
4. 权威政策/标准网站先进入待白名单确认状态。
5. 评测集采用 100 分制和红线 hard_fail 机制。

## 2. 动作

本轮执行动作：

1. 建立受控评测集：
   `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md`
2. 定义来源引用、事实分层、门禁意识、操作可用性、禁止输出控制五项评分。
3. 定义知识问答助手、使用助手、文档验收助手和 SOP 建议评测样例。
4. 定义红线测试和 hard_fail 机制。
5. 定义评测记录字段和内测前通过条件。

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 葛化 GFIS AI 助手首批问答与文档验收评测集 | `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md` | 定义三件套助手评测样例、评分规则、红线测试和通过条件 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-009.md` | 记录本轮五段式治理微循环 |

## 4. 检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 评测覆盖 | pass | 覆盖 KQA、GUA、DVA、SOP 四类场景 |
| 红线控制 | pass | 设置 8 个 hard_fail 红线 |
| 金融边界 | pass | 金融资料只做脱敏索引，不确认资金事实 |
| OEM 责任边界 | pass | 明确现代精工 OEM 与葛化目标工厂责任区分 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |

## 5. 反馈

本轮结论：

1. 葛化三件套助手的首批评测集已形成。
2. 评测集支持后续内测、缺陷回流和知识缺口悬赏。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-010：
葛化 GFIS AI 助手内测运行记录模板，定义内测用户、问题采样、助手输出、评分记录、缺陷回流、知识缺口悬赏和 WAES/KDS 回写字段。
```

待用户回答：

1. 三件套内测是否先限制在楚商云/葛化项目组，不开放给外部合作单位？
2. 红线测试是否作为上线前一票否决项？
3. 评测分数是否先采用 85 分通过阈值？
4. 评测记录是否允许记录脱敏输入输出摘要，不保存敏感原文？
5. DKS-010 是否进入内测运行记录模板？
