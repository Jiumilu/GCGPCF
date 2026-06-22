---
doc_id: GPCF-DOC-E574C9CB52
title: Loop Round GPCF-GF-LR-001
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GPCF-GF-LR-001.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GPCF-GF-LR-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GF-LR-001

## 1. 输入

- 输入来源：`08-evidence-samples/GFIS/source-files/现代精工工厂岗位培训学习资料_优化版.pdf`
- 本轮目标：生成 GFIS 岗位-流程-数据-门禁抽取包，作为 GFIS 项目仓初始化和后续开发的第一轮输入。
- 入口条件：
  - PDF 已纳入受控 evidence。
  - PDF 结构化分析已生成。
  - GPCF 总控仓已进入 Loop L2。
  - KDS TOKEN 在本开发机阶段暂缓，不阻断本地 Loop 开发。
- 关联需求/文档：
  - `08-evidence-samples/GFIS/GPCF-GF-LR-001-input.md`
  - `08-evidence-samples/GFIS/modern-jinggong-training-analysis.md`
  - `09-status/globalcloud-project-mainline-alignment-matrix.md`
- 不处理范围：
  - 不宣称 GFIS 系统已实现。
  - 不替代现场实际访谈和数据采集。
  - 不把 GPC 的客户协同、合同、回款主责放入 GFIS。

## 2. 动作

| 类型 | 文件 | 说明 |
|---|---|---|
| 新增 | `08-evidence-samples/GFIS/loop-state.md` | GFIS 托管 Loop 状态 |
| 新增 | `08-evidence-samples/GFIS/gfis-role-map.md` | 岗位到 GFIS 能力映射 |
| 新增 | `08-evidence-samples/GFIS/gfis-business-object-candidates.md` | 首批业务对象候选 |
| 新增 | `08-evidence-samples/GFIS/gfis-document-record-candidates.md` | 单据与记录候选 |
| 新增 | `08-evidence-samples/GFIS/gfis-quality-gate-candidates.md` | 质量、安全和业务门禁候选 |
| 新增 | `08-evidence-samples/GFIS/gfis-gpc-boundary-notes.md` | GFIS/GPC/WAES/KDS/Brain 边界说明 |
| 新增 | `08-evidence-samples/GFIS/gfis-field-study-data-capture.md` | 现场采集表 |
| 新增 | `08-evidence-samples/GFIS/evidence-index.md` | GFIS 首轮 evidence 索引 |
| 新增 | `GFIS:docs/harness/loop-state.md` | GFIS 独立项目仓 Loop 状态 |
| 新增 | `GFIS:docs/harness/gpcf-gf-lr-001-initialization-manifest.md` | GFIS 独立项目仓初始化 Manifest |

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 岗位映射 | `08-evidence-samples/GFIS/gfis-role-map.md` | 把培训资料岗位转为 GFIS 能力输入 |
| 对象候选 | `08-evidence-samples/GFIS/gfis-business-object-candidates.md` | 首批业务对象、主责和边界 |
| 单据记录 | `08-evidence-samples/GFIS/gfis-document-record-candidates.md` | 工厂执行单据与记录候选 |
| 门禁候选 | `08-evidence-samples/GFIS/gfis-quality-gate-candidates.md` | 未检验、未确认、未放行等红线 |
| 边界说明 | `08-evidence-samples/GFIS/gfis-gpc-boundary-notes.md` | 防止 GFIS 扩张为全平台 |
| 采集表 | `08-evidence-samples/GFIS/gfis-field-study-data-capture.md` | 下一轮现场调研数据项 |

## 4. 检查

| 检查项 | 命令/方式 | 结果 | 证据 |
|---|---|---|---|
| 输入可追溯 | 对照 PDF 结构化分析 | pass | `modern-jinggong-training-analysis.md` |
| 边界一致性 | 对照项目主线矩阵 | pass | `globalcloud-project-mainline-alignment-matrix.md` |
| 文档治理 | `python3 tools/kds-sync/document_control.py` | 待本轮结束执行 | 文档台账 |
| KDS TOKEN | 本开发机阶段暂缓 | deferred | 正式同步前必须配置 |
| 实现验收 | 本轮不做系统实现验收 | not_applicable | 仅开发输入包 |

## 5. 反馈

- 阻塞项：
  - 现场真实数据尚未采集。
- 风险项：
  - 培训资料包含商务、财务、客户交付内容，容易把 GFIS 扩张为 GPC。
  - 部分质量放行动作必须由 WAES 形成治理门禁，GFIS 只提供工厂事实。
- 下一轮输入：
  - 将本轮抽取包继续转化为 GFIS 数据字典 v0.1 和接口契约草案。
  - 现场采集真实工单、质检、入库、出库样本。
- 建议状态：`partial`
- Harness 判定：允许继续开发输入准备，不允许进入 `accepted`。

## 6. 本轮回溯

- 开始时间：2026-06-12
- 完成时间：2026-06-12
- 循环耗时（分钟）：本轮未做分钟级计时
- 是否触发阻塞：是
- Round ID：GPCF-GF-LR-001
