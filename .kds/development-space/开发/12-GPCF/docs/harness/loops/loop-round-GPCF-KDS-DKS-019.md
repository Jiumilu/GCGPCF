---
doc_id: GPCF-DOC-06D6A2F8D3
title: Loop Round GPCF-KDS-DKS-019
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-019.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-019.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-019

日期：2026-06-17  
状态：controlled  
主题：湖北磷材拓厂与新工厂复制试点任务书  
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. 用户要求继续推进 GlobalCloud 项目群分布式 KDS 知识事实体系和绿色供应链试点落地。
2. `GPCF-KDS-DKS-018` 已完成葛化 GFIS 资料包入库验收与 AI 助手试运行任务书。
3. 湖北磷材作为第二条并行线，第一阶段不做 GFIS 深度运行。
4. 本轮重点是拓厂项目知识库、原料/行业/订单知识库、新工厂复制模板和葛化母版复用路径。

## 2. 动作

1. 修订 `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md` 为 `GPCF-KDS-DKS-019` 正式任务书。
2. 明确 HBLC 五类资料包：拓厂项目、原料、行业、订单线索、新工厂复制模板。
3. 定义拓厂项目知识库、原料/行业/订单知识库和新工厂复制模板。
4. 定义 `FactoryExpansionAssessment` 模型和权重建议。
5. 固化 KDS 11 底座池与增强治理账本挂接规则。
6. 明确 Brain、PKC、小即、XGD、XiaoG、MMC 的第一阶段任务。
7. 补充 AI 建议、知识缺口、悬赏候选、权限密级和试点节奏。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| 湖北磷材拓厂与新工厂复制试点任务书 | `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md` | DKS-019 正式任务书，覆盖拓厂、原料/行业/订单、新工厂复制和葛化母版复用 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-019.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py` |
| KDS 本地开发空间镜像 | pass | 已生成或更新本地开发空间镜像，真实 API 同步仍按台账状态处理 |
| scoped git diff check | pass | 已仅检查本轮触达文件，无 whitespace error |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | 串行复核 `gate=pass`，repo markdown 804，KDS markdown 817，missing metadata 0，missing README dirs 0 |
| 项目群 Loop 编排器 | partial | `document_gate=pass`，但全局 `git_gate=rework_required` 且 operational gates 仍有既有 GFIS/GPCF repair/blocked 信号；本轮不升级状态 |

## 5. 反馈

1. 本轮把旧队列 HBLC 模板校正为当前队列 `DKS-019` 的正式任务书。
2. 湖北磷材第一阶段明确不做 GFIS 深度运行，优先形成拓厂项目知识库、原料/行业/订单知识库和新工厂复制模板。
3. 葛化母版作为结构输入，但不得把葛化候选事实直接写成湖北磷材事实。
4. 本轮只形成治理和试点任务书，不声明真实资料已入库、真实拓厂评估已通过、真实订单/原料事实已确认或真实 KDS API 已同步。

## 6. 下一轮建议

`GPCF-KDS-DKS-020`：积分池、收益池、额度池、悬赏池、争议池联动规则。
