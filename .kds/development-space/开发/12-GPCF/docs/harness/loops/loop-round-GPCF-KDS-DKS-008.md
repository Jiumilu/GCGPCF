---
doc_id: GPCF-DOC-E7EC0E51E9
title: GPCF-KDS-DKS-008 葛化第一阶段 GFIS AI 助手三件套实施清单 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-008.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-008 葛化第一阶段 GFIS AI 助手三件套实施清单 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

用户已确认葛化第一阶段先做：

1. GFIS 知识问答助手。
2. GFIS 使用助手。
3. GFIS 文档验收助手。
4. AI 基于知识库向 GFIS 或其他业务系统输入候选事实，驱动 SOP 形成。

上一轮 `GPCF-KDS-DKS-007` 已完成知识收益治理委员会 DecisionRecord 与争议处理模板，并建议本轮进入三件套实施清单。

## 2. 动作

本轮执行动作：

1. 建立受控实施清单：
   `03-data-ai-knowledge/GlobalCloud葛化第一阶段GFISAI助手三件套实施清单.md`
2. 定义三类助手的目标用户、核心能力、禁止事项和首批状态。
3. 定义葛化首批知识源分级、可信等级和密级规则。
4. 写入三类助手的系统提示词、输出字段和首批场景。
5. 定义文档验收模板、SOP 建议流程、首批 AI 建议编号和评测集。

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 葛化第一阶段 GFIS AI 助手三件套实施清单 | `03-data-ai-knowledge/GlobalCloud葛化第一阶段GFISAI助手三件套实施清单.md` | 定义知识问答助手、使用助手、文档验收助手的提示词、场景、门禁和评测集 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-008.md` | 记录本轮五段式治理微循环 |

## 4. 检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| GFIS 主体边界 | pass | 三类助手均不替代 GFIS 运行层事实 |
| AI 越权边界 | pass | 助手只生成回答、指导、验收、候选事实和 SOP 建议 |
| 文档验收边界 | pass | 文档验收通过不等于业务完成 |
| OEM 责任边界 | pass | 明确现代精工 OEM 与葛化目标工厂责任区分 |
| 金融边界 | pass | 金融凭证只做脱敏索引和人工确认入口 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |

## 5. 反馈

本轮结论：

1. 葛化第一阶段三类 AI 助手已形成可配置实施清单。
2. 首批知识源、提示词、场景、文档验收模板、SOP 建议对象和评测集已定义。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-009：
葛化 GFIS AI 助手首批问答与文档验收评测集，把 DKS-008 的场景转成可复测的问题、样例输入、期望输出、禁止输出和评分规则。
```

待用户回答：

1. 葛化三类助手是否先在项目组内部试用，再开放给合作单位？
2. 文档验收助手首批是否优先验收辽宁远航链路和现代精工 OEM 过渡资料？
3. 金融凭证资料是否默认只做脱敏索引，不进入开放问答？
4. 权威政策/标准网站是否先由用户指定白名单，再纳入 T3 高可信源？
5. DKS-009 是否按评测集和评分规则继续推进？
