---
doc_id: GPCF-DOC-5E62A3403A
title: 0–30 天尾巴清理包：剩余 4 个 blocked（交属主/上级裁定）
project: KDS
related_projects: [GPC, WAME, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/p05-tail-clearance-packet-20261022.md
source_path: docs/reports/p05-tail-clearance-packet-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 0–30 天尾巴清理包：剩余 4 个 blocked（交属主/上级裁定）

- 日期：2026-10-22 21:42｜依据：老卢裁定「先清 0–30 天尾巴」
- 当前 blocked 由 8 降为 4（F-031 关单、F-026 解除、F-015 退役结项、F-027 解除）
- 本文件只出动作与判据，**不代写跨项目仓**、不做状态提升

## 1. F-013（GPCF，治理型）
- 阻塞：`kds_p1_apply_blocked_by_dirty_worktree`；`gpcf_a10r27 4 文件 delta 待独立复核与单独提交`
- 属主动作：KDS 侧收敛工作树 → 复核 4 文件 delta → 单独提交并回执
- 判据：`git -C "GlobalCloud KDS" status --porcelain -uall | wc -l` 收敛到已登记范围；4 文件 delta 有独立 commit
- GPCF 侧同步：`python3 scripts/gpcf_check_evidence.py F-013 --check-only` → 只剩 blocker 文本

## 2. F-014（GPCF，真实数据型）
- 阻塞：真实试点、权威接收台账 owner、留存策略、KDS/MMC 运行配置边界均超出本地 fixture 授权
- 属主动作：由老卢指定**权威接收台账 owner** + 留存策略口径；KDS/MMC 运行配置变更走各自授权
- 判据：回执 `authorization_granted=true`（真实数据）+ owner 书面指定；`evidence/summary.md` 更新
- 备注：这是唯一必须"外部授权"才能闭环的 blocker，建议与 P12 PQC 试点授权一并处理

## 3. F-021（World，混合型）
- 阻塞：World 总体方案 Ontology 版本冲突（0.2.x vs 实发 0.2.0，方案仍 candidate）；证据声明已补（P05 已修）
- 属主动作：WAS 出具 Ontology 基线裁定 → World 更新方案 → 6 项 metadata 补齐
- 判据：`loop_document_gate` 对该 Feature 无 rework_required；方案状态 candidate→authoritative 由台账确认
- 关联：World 仓 F-021 归属同步清单已出（`world-f021-attribution-sync-checklist-20261022.md`）

## 4. F-030（PDC，证据型）
- 阻塞：tests/summary fail（根因是 GPCF 全群门禁，现已 pass）
- 属主动作：按《PDC 重采清单》重跑并回填 2 个证据文件
- 判据：`python3 scripts/gpcf_check_evidence.py F-030 --check-only` 不再报 evidence 类理由

## 5. 汇总口径

| Feature | 责任方 | 是否需老卢授权 | 预计闭环 |
|---|---|---|---|
| F-013 | KDS 属主 | 否（属主执行） | 1–2 天 |
| F-014 | 老卢指定 owner + 授权 | **是**（真实数据与配置边界） | 3–5 天 |
| F-021 | WAS 裁定 + World 属主 | 否（裁定走治理链） | 2–3 天 |
| F-030 | PDC 属主 | 否（属主执行） | 1 天 |
