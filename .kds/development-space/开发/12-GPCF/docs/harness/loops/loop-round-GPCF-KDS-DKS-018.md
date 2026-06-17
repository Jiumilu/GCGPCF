---
doc_id: GPCF-DOC-E16CA336E0
title: Loop Round GPCF-KDS-DKS-018
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-018.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-018.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-018

日期：2026-06-17  
状态：controlled  
主题：葛化 GFIS 资料包入库验收与 AI 助手试运行任务书  
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. 用户要求继续推进 GlobalCloud 项目群分布式 KDS 知识事实体系和绿色供应链试点落地。
2. `GPCF-KDS-DKS-017` 已完成 KDS 11 池与增强治理账本项目群级映射。
3. 葛化为第一阶段标准母版，优先形成 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手、订单运行母版和预运营期订单链路。
4. 首批资料范围包括建设资料、工厂运营资料、订单资料、辽宁远航链路、现代精工 OEM 过渡资料、质量/发货/POD/金融凭证门禁资料。

## 2. 动作

1. 修订 `03-data-ai-knowledge/GlobalCloud葛化首批资料包入库验收与GFISAI助手试运行任务书.md` 为 `GPCF-KDS-DKS-018` 正式任务书。
2. 明确七类资料包的编号、密级、最小字段、必要证据、常见缺口和通过后输出。
3. 固化资料包到 KDS 11 底座资源池和增强治理账本的挂接规则。
4. 明确预运营期订单链路中目标工厂与 OEM 承接方的事实责任拆分。
5. 形成 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手的首批试运行样本。
6. 补充评分记录模板、硬失败规则、知识缺口、悬赏候选和候选 SOP 形成规则。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| 葛化 GFIS 资料包入库验收与 AI 助手试运行任务书 | `03-data-ai-knowledge/GlobalCloud葛化首批资料包入库验收与GFISAI助手试运行任务书.md` | DKS-018 正式任务书，覆盖资料包验收、三类助手试运行、评分、悬赏候选和 SOP 候选 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-018.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py` |
| KDS 本地开发空间镜像 | pass | 已生成或更新本地开发空间镜像，真实 API 同步仍按台账状态处理 |
| scoped git diff check | pass | 已仅检查本轮触达文件，无 whitespace error |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass`，repo markdown 801，KDS markdown 814，missing metadata 0，missing README dirs 0 |
| 项目群 Loop 编排器 | partial | `document_gate=pass`，但全局 `git_gate=rework_required` 且 operational gates 仍有既有 GFIS/GPCF repair/blocked 信号；本轮不升级状态 |

## 5. 反馈

1. 本轮把葛化资料包任务书从旧队列草案校正为当前队列 `DKS-018` 的正式任务书。
2. 七类资料包、三类 AI 助手、评分记录、知识缺口悬赏候选和候选 SOP 形成规则已经统一挂接到 KDS 11 池和增强治理账本。
3. 本轮只形成治理和试运行任务书，不声明真实资料已入库、真实 AI 助手已上线、真实业务事实已确认或真实 KDS API 已同步。
4. 下一轮建议进入 `GPCF-KDS-DKS-019`，聚焦湖北磷材拓厂与新工厂复制试点任务书。

## 6. 下一轮建议

`GPCF-KDS-DKS-019`：湖北磷材拓厂与新工厂复制试点任务书。
