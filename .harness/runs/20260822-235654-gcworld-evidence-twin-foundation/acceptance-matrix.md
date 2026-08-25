---
doc_id: GPCF-DOC-GCWORLD-025
title: GCWORLD证据数字孪生底座验收矩阵
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, MMC, GFIS, Brain, Studio]
domain: harness-evidence
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/20260822-235654-gcworld-evidence-twin-foundation/acceptance-matrix.md
source_path: .harness/runs/20260822-235654-gcworld-evidence-twin-foundation/acceptance-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

# GCWORLD证据数字孪生底座验收矩阵

| OpenSpec任务 | 对应需求 | 实现或产物 | 证据 | 判定 |
| --- | --- | --- | --- | --- |
| 1.1—1.4 治理与准入 | 运行边界：系统职责分离、分阶段演进 | F-013绑定、只读授权、CodeGraph影响声明 | `validation-summary.yaml`中的F-013与GKE-001门禁 | 结构通过；KDS准入仍阻塞 |
| 2.1—2.4 证据孪生 | 资产、四世界、时态关系、WAS继承、双时间、快照 | 世界模型Schema、样例、校验器及总体规划 | 3个正例、4个负例、3次确定性结果 | 通过 |
| 3.1—3.5 覆盖评估 | 只读来源、覆盖与例外、五类对象处置 | 只读读取器、受控分类器、台账、报告及规范 | 28项回归；KDS前后摘要一致；覆盖结果明确为部分完成 | 部分完成边界正确 |
| 4.1—4.4 智能体治理 | 注册、行动信封、执行账本、候选边界、记忆与风险 | 职能智能体治理Schema、样例及校验器 | 4个正例、12个负例、4种模式、6种账本结果 | 通过 |
| 5.1—5.4 世界权限 | 身份授权责任分域、交集、快照、义务、撤销、职责分离 | 世界权限Schema、样例及校验器 | 5个正例、14个负例、真实授权0 | 结构通过；无真实授权 |
| 6.1—6.4 世界运行时 | 服务分离、标准闭环、任务承诺、风险回执、模拟提升 | 世界运行时Schema、样例及校验器 | 6个正例、15个负例、真实执行0 | 结构通过；无真实运行 |
| 7.1—7.4 工作台 | 十二中心、单一档案、全链路裁剪、多租户共享 | 工作台Schema、样例及校验器 | 6个正例、16个负例、真实跨租户共享0 | 结构通过；无界面运行 |
| 8.1—8.4 工程治理 | 七层数据、投影重建、存储职责、标识事件、安全与阶段门禁 | 工程治理Schema、样例及校验器 | 7个正例、21个负例、8阶段、11指标 | 通过 |
| 9.1 回归与豁免 | 四级验收状态与证据真实性 | 单元、模型、确定性、零写入回归；构建/API/UI豁免 | `validation-summary.yaml` | 通过 |
| 9.2 严格校验与文档门禁 | 文控与项目群准入要求 | OpenSpec严格校验、文档门禁、17仓就绪门禁 | 缺失元数据0、缺失README 0、17/17通过 | 通过 |
| 9.3 独立Harness复核 | 证据真实性与状态上限 | Evidence Index、交接包、独立审计报告 | `harness-status-audit.yaml` | `pass_with_runtime_blockers` |
| 9.4 后续独立授权提案 | 分阶段演进；前一阶段不得自动授权下一阶段 | 未生成KDS、界面或运行时集成提案 | 覆盖报告尚无人工作出最终复核，F-013仍阻塞 | 阻塞，保持未完成 |

构建、真实API、真实界面和中文搜索不在本轮授权与实现范围，均按“不适用”记录；这不是运行通过证据。

