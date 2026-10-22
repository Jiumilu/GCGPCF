---
doc_id: GPCF-DOC-D0D0365291
title: P05 · 7 个 blocked Feature 分类与处理（2026-10-22）
project: KDS
related_projects: [GPC, PVAOS, WAME, KDS, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p05-blocked-classification-20261022.md
source_path: docs/reports/p05-blocked-classification-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P05 · 7 个 blocked Feature 分类与处理（2026-10-22）

- 依据：后续工作计划 P05（0–30 天 W3）｜状态边界：只补证据声明与豁免理由，**不做状态提升**
- 实测命令：`python3 scripts/gpcf_check_evidence.py <F> --check-only`
- 背景变化：F-031 已于 2026-10-22 21:01 经老卢逐项签收关单（blocked 8→7）；门禁已于同日 `pass`

## 1. 分类结果（按根因）

| Feature | 项目 | 归类 | 根因 | 本批处理 | 剩余依赖 |
|---|---|---|---|---|---|
| F-013 knowledge-asset-model-system | GPCF | 治理型 | dirty worktree（KDS P1 apply 受阻）+ 4 文件 delta 待独立复核与提交处置 | ✅ 补 `verification.tests/build` + api 豁免范围理由 | 脏树收敛 + 独立复核（需 KDS 侧） |
| F-014 industrial-meeting-to-project-control-loop | GPCF | 真实数据型 | 真实试点、权威接收台账 owner、留存策略、KDS/MMC 运行配置边界均超出本地 fixture 授权 | ✅ 同上 | 真实数据与配置边界授权（外部） |
| F-015 org-readonly-vertical-slice | Studio | 证据型 | api/summary 仍 pending；真实人员组织关系资料缺 | ✅ 补 tests/build 声明 | 真实资料或受控例外（Studio 已裁退出） |
| F-021 world-project-onboarding | World | 混合型 | Ontology 版本冲突（方案仍 candidate）+ 证据声明缺 | ✅ 补 tests/build + screenshots/api 豁免理由 | Ontology 裁定（WAS）+ metadata 补齐 |
| F-026 gcmem-governance-onboarding | GCMEM | 治理型 | 原理由为「中央门禁 rework_required」——**该门禁已于 2026-10-22 pass，理由已过期** | ✅ 已有 verification 块，无需补 | 待复核是否可解除（需授权） |
| F-027 governance-remediation | GPCF | 治理型 | 方案候选未全核验 + 历史 done Feature 未满足关闭规则（审计分母应 14） | ✅ 已有 verification 块 | P17 补验/受控例外 |
| F-030 pdc-project-group-onboarding | PDC | 证据型 | tests/summary fail，根因是 GPCF 全群门禁（非 PDC 缺陷）；门禁现已 pass | ⏳ 需重采 | PDC 仓重跑 tests/summary（属主执行） |

## 2. 本批实际改动（4 个 feature.yaml）

统一补 `verification.tests` / `verification.build` 与豁免范围理由（豁免必须写"范围特定理由"，不得用 `not_required` 替代）：

```yaml
verification:
  tests:
  - python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py
  build:
  - python3 tools/kds-sync/check_python_bytecode.py
  waivers:
    api: <范围特定理由，说明该 Feature 无对外接口面>
```

复跑结果：`F-013/F-014/F-021` 的「command not declared / waiver has no reason」三项理由全部消除，只剩真实治理阻塞。

## 3. 需要授权的下一步（未做）

1. **F-026 解除阻塞判定**：其 blocker 理由（中央门禁失败）已过期，是否重采并解除需授权（涉及状态推进）。
2. **F-030 重采**：需 PDC 属主在 PDC 仓重跑 tests/summary 证据（跨项目，GPCF 不代跑）。
3. **F-015**：Studio 已裁退出，建议登记为"随 Studio 退出结项"或转受控例外（P17）。
