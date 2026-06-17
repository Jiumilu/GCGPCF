---
doc_id: GPCF-DOC-F2DE220F45
title: GPCF-L4-GFIS-REPAIR-157
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-157.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-157.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-157

## 输入

- 用户确认葛化工厂仍在建设期，辽宁远航首笔订单当前由现代精工工厂 OEM 代加工承载。
- 用户确认 GFIS 是现代精工 OEM 代加工阶段和葛化自建工厂投产后的同一运行时系统。
- GFIS 上一轮仍缺有效人工批准、真实回执、签章完成件、客户确认、KDS write receipt 和 WAES confirmation。

## 本轮目标

把上述业务口径落实为 GFIS 项目仓机器门禁，并回写 GPCF 总控状态，防止后续再次把 GFIS Demo、葛化已投产假设或合同审阅稿误当作运行层 SOP 主体。

## 输出

```text
liaoning_yuanhang_runtime_positioning_consistency_guard=pass positioning_rules=7 rules_passed=7 wrong_subjects_blocked=4 demo_subject_allowed=0 current_runtime_sites=1 future_runtime_sites=1 review_queue=0 runtime_intake=0 waes_review=0 verified=0 state=runtime_positioning_consistency_guard_passed_no_release runtime_sop_e2e=repair_required
```

## 验证

- GFIS 新门禁 validator：pass。
- GFIS 主 runtime SOP validator：expected exit 2，保持 `repair_required`。
- GFIS Demo E2E：26 passed，仅为 `pass_demo_only`。
- GFIS `git diff --check -- .`：pass。

## 边界

- 未写真实 KDS、WAES、外部 API 或生产数据库。
- 未执行 `bench migrate`、schema sync、权限变更、部署、ECS/阿里云/Caddy/隧道/Docker 变更。
- 未创建签章完成件、客户确认函、采购订单/合同、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated。

## 真实计数

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `7`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`
