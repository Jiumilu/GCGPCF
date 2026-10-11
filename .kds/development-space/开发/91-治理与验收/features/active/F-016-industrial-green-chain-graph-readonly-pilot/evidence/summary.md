---
doc_id: GPCF-DOC-F016-GRAPH-READONLY-PILOT-EVIDENCE-20261011
title: F-016 证据摘要（B1 交付 + B2 预览）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-016-industrial-green-chain-graph-readonly-pilot/evidence/summary.md
source_path: features/active/F-016-industrial-green-chain-graph-readonly-pilot/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# F-016 证据摘要（B1 交付 + B2 预览）

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass（图谱校验器 12/12，确定性检查）
- build: pass（生成器实跑；KDS `e8eb05a8` / GPCF `67ce85d5` 已提交并推送）
- screenshots: waived（P1 表格/局部视图，无 UI 变更）
- api: waived（本地只读文件，无接口调用）
- lint: 生成器/校验器为纯 Python 标准库 + PyYAML；写入经 YAML 校验
- risk: 未授权项列明——无写回、无定时任务、无状态提升、无对外发送
<!-- GPCF_EVIDENCE_GATE_END -->

## 一、B1 交付（可审阅）
- `artifacts/b1-三链来源与责任清单.md`（草案；责任字段=待落实，未虚构任命）
- `artifacts/b1-接口与依赖可用性清单.md`（13 项：3 项已验证可用 / 半就位 1 / 边界引用 4 / 未接入 3 / 环境项 2）

## 二、B2 预览（技术预演，只读）
- 生成：`工业绿链/图谱/scripts/graph_builder.py`（承接 v2.0 §5/§9：claim 统一字段、断言类别、命名空间、状态分离、零任务化）
- 校验：`工业绿链/图谱/scripts/graph_check.py`（T 项可自动化子集：T03/T04/T05/T11/T16/T17/T19部分/T20）
- 快照：`工业绿链/图谱/snapshots/2026-10-11_b2-preview/`
  - 对象 **85** · 声明 **51** · 映射 **75**；内容摘要 `77828c8e3bfc…`（sha256，含规则版本）
  - 校验 **12/12 全过**（含：跨运行摘要一致 C01；E01/F001 命名空间单点 C02；参数/费用类零任务化 C03；计划/事实分离 C04；来源未变 C07；映射 100% 可回溯 C06）
- 恢复与变更检测（B2 覆盖说明）：
  - 内容幂等：相同来源+规则重跑 → 相同摘要（C01）；运行时间/耗时独立于内容（receipt.json）
  - 变更检测：来源 sha256 基线入库（manifest_snapshot.json），再跑对比（C07）
  - 恢复：快照可随时由来源重放（只读派生）；失败不影响来源（本轮无失败）
- 边界：**不是** B2 放行结论；B2 放行仍待 B1 审阅 + 源记录逐条对账 + 权限/恢复测试评审。

## 三、未覆盖（如实保留）
- 三链之外项目未接入（按 v2.0：三链范围由 B1 来源清单冻结）
- SOP 适用性完整核验（B3）、人员使用/复核任务流（B4）、系统接入（B5）均未开始
- 口径与排除：任务候选集 236 条中仅选取三链关键对象；参数/费用/占位/汇总 12 条零任务化留源
- 已知缺口：'行动项N'↔M0512-A00N 对应待复核；PVA-BMW-PACKAGING 注册表未收录（建议补登记）；供应/付款角色源内未标
