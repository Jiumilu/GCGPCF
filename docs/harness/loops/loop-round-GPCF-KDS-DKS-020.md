---
doc_id: GPCF-DOC-37814096BB
title: Loop Round GPCF-KDS-DKS-020
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-020.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-020.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-020

日期：2026-06-17  
状态：controlled  
主题：积分池、收益池、额度池、悬赏池、争议池联动规则  
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. 用户要求继续推进 GlobalCloud 项目群分布式 KDS 知识事实体系和绿色供应链试点落地。
2. `GPCF-KDS-DKS-017` 已明确 KDS 11 池与增强治理账本项目群级映射。
3. `GPCF-KDS-DKS-018` 已完成葛化 GFIS 资料包入库验收与 AI 助手试运行任务书。
4. `GPCF-KDS-DKS-019` 已完成湖北磷材拓厂与新工厂复制试点任务书。
5. 本轮需要把积分池、收益池、额度池、悬赏池、争议池、潜在产值池、贡献账本和 SOP 账本收束为统一联动规则。

## 2. 动作

1. 新增 `03-data-ai-knowledge/GlobalCloud积分收益额度悬赏争议联动规则.md`。
2. 明确增强账本不是底座资源池，必须挂接 KDS 11 个底座资源池。
3. 定义统一对象字段、统一状态机、异常分支和保护状态。
4. 定义知识积分、产值积分、渠道积分、潜在产值、悬赏积分、治理积分、纠错积分和违规扣减规则。
5. 定义收益池到账正式确认、开票统计口径和自购 AI 额度不入池规则。
6. 定义额度池、悬赏池、争议池、潜在产值转正式产值和试点映射。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| 积分收益额度悬赏争议联动规则 | `03-data-ai-knowledge/GlobalCloud积分收益额度悬赏争议联动规则.md` | DKS-020 正式规则，覆盖增强账本联动、状态机、试点映射和治理边界 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-020.md` | 本轮输入、动作、输出、检查和反馈证据 |

## 4. 检查

| 检查项 | 结果 | 备注 |
|---|---|---|
| 文档控制台账 | pass | 已运行 `python3 tools/kds-sync/document_control.py`；主规则和本 Loop 记录已进入 `globalcloud-document-control-register.md` |
| KDS 本地开发空间镜像 | pass | 已镜像到 `开发/05-KDS/03-data-ai-knowledge/` 和 `开发/12-GPCF/docs/harness/loops/`；同步状态保持 `pending_api` |
| scoped git diff check | pass | 已对本轮触达文件运行 scoped `git diff --check`，无输出 |
| 防污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass, repo_md=807, kds_md=820, missing_metadata=0, missing_readme_dirs=0` |
| 项目群 Loop 编排器 | partial | `document_gate=pass`；全局 `git_gate=rework_required` 源于既有多文件 EOF 空行问题，运营门禁仍受 GFIS/GPCF 既有修复态影响；本轮不得升级状态 |

## 5. 反馈

1. 本轮把积分、收益、额度、悬赏、争议、潜在产值、贡献和 SOP 统一为 KDS 11 池之上的增强治理账本联动规则。
2. 规则保留 AI 候选边界、KDS/WAES/人工确认流程、委员会裁决机制和用户治理权。
3. 本轮只形成治理规则，不声明真实积分、真实收益、真实额度、真实悬赏、真实争议或真实分配已经发生。
4. 下一阶段建议进入葛化资料包样本表、湖北磷材拓厂评估样本表和 MMC 规则参数表。
5. 项目群 Loop 编排器仍应按全局 `partial / rework_required` 边界处理：GFIS 运行层 SOP E2E 尚未完成，本文档通过不等于业务完成。

## 6. 阶段收口建议

`GPCF-KDS-DKS-014` 至 `GPCF-KDS-DKS-020` 已形成本目标第一阶段的受控规则骨架。下一阶段建议转入样本表、评分记录、参数表和试点运行记录，但不升级任何项目状态。
