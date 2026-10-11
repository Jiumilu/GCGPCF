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
  - 对象 **85** · 声明 **51** · 映射 **70**；内容摘要 `c64844689aba…`（v0.1.3；初版 77828c8e）
  - 校验 **13/13 全过**（v0.1.2 起含 C13；含：跨运行摘要一致 C01；E01/F001 命名空间单点 C02；参数/费用类零任务化 C03；计划/事实分离 C04；来源未变 C07；映射 100% 可回溯 C06）
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

## 四、B2 放行材料补全（2026-10-11 追加）
- 校验 13/13（含 C13 派生层最小暴露：0 敏感命中）；映射 70 行无重复键；未映射结构节点 25（项目/事件/当事人，经 source_refs 回溯）
- 复核队列 v0.1：**39 项**（拟判断4 / 映射4 / 角色权责附注22 / 别名2 / 结构缺口7；接收人已落实-暂定（各链负责人＋核验老卢），期限待定）
- P1 视图集：5 视图 + 局部 Mermaid（阻塞与缺口 / 主体业务关系 / SOP执行核验[B3骨架，全 sop_gap] / 来源与变更 / 三链_mermaid）
- 差异复核工具 `graph_diff.py`：测试通过（重跑重建 = 0 差异；对比修订快照 = 9 处差异检出）
- 注册表关联：`IGL-BMW-TURNOVER-BOX.linked_project=PVA-BMW-PACKAGING`（2026-10-11，老卢确认）；真实变更闭环（检出→重建→差异复核 15 对象/11 声明）证据：KDS `工业绿链/图谱/evidence/2026-10-11_注册表关联变更复核.md`
- 五连演练（副本执行，真实来源零触碰）：损坏检出 / 重建恢复（摘要一致）/ 源修订检出（C07）/ 关键源阻断（exit 3）/ 非关键源 partial 回执 —— 证据：KDS `工业绿链/图谱/evidence/2026-10-11_恢复与变更检测演练.md`
- 结论边界：以上为**本地可回放证据**，不构成 B2 放行；放行 = B1 审阅 + 源记录人工逐条对账 + 权限/恢复评审

## 五、B2 放行与工程加固（2026-10-11 续执行）
- **B2 受控只读试点放行**：抽样核对单（8 条；机器预核 8/8）＋校验 13/13＋五连演练；老卢确认（current_step=b2_released）。
- 工程加固 v0.1.4：暂存→复算保护→**原子替换**（上一快照 `.old*` 保留、零删除）；校验 +C14 依赖环路 → **14/14**。
- T01—T20 现状对照：**13 全覆盖 / 6 部分 / 1 待 SOP**（+U/E 类现状节）（KDS `工业绿链/图谱/evidence/2026-10-11_T01-T20现状对照.md`）。
- 负例与专项（追加）：T01 插入/改名专项通过（身份保持/定位更新/新行吸收）；T10 环注入、T13 敏感注入均 FAIL 检出（KDS `evidence/2026-10-11_负例与专项测试.md`）。
- 方案修订：v2.0 新增 §14.3—14.6 U/E 类验收（方案侧 2026-10-11；已随本批登记）。
- **B3 机制预置（2026-10-11 追加）**：SOP 适用绑定引擎+sop_registry（空登记=全量 sop_gap；合成测试：绑定/冲突/在途/草稿四规则全数通过）；导出包（打包+校验通过）；《查询与导出契约 v0.1》；校验 **15/15**。证据：KDS `evidence/2026-10-11_B3机制预置与导出包.md`。
- 下一步：B3（待首批 SOP 首版）→ B4（人员使用与人工全量核对）。
