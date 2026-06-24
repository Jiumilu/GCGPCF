---
doc_id: GPCF-DOC-6D3A7A52DA
title: GPCF-L4-GFIS-REPAIR-146 GFIS 合同链真实回执 live-intake 负例拒收门禁
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-146.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-146.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-146 GFIS 合同链真实回执 live-intake 负例拒收门禁

## 输入

- GFIS `GFIS-RUNTIME-SOP-E2E-138` 已建立 live-intake validator，确认 26 个真实回执槽位中 `submitted_files=0`、`valid_receipts=0`、`missing_files=26`。
- 用户确认：葛化工厂仍在建设阶段，当前使用现代精工工厂进行 OEM 代加工；GFIS 是现代精工代加工生产阶段及葛化自建工厂投产后的同一运行时系统。
- 本轮目标不是证明真实业务完成，而是证明错误 JSON、弱材料、KDS 候选、WAES 文字或未签章审阅稿不能被 live-intake 误收。

## 动作

- 接收 GFIS 新增的辽宁远航合同链真实回执 live-intake 负例拒收门禁、5 个 rejected example、builder、validator 和只读 API。
- 将 GFIS 主 validator 新增状态回写到 GPCF 总控 loop-state、evidence index、控制板和项目群状态矩阵。
- 保持 GPCF/GFIS `repair_required`，不提升 accepted/integrated。

## 输出

```text
liaoning_yuanhang_contract_chain_real_receipt_live_intake_negative_fixture_guard=pass negative_fixture_count=5 rejected_fixture_count=5 accepted_fixture_count=0 runtime_ready=0 verified=0 state=real_receipt_live_intake_negative_fixtures_rejected runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_contract_chain_real_receipt_live_intake_negative_fixture_guard=real_receipt_live_intake_negative_fixtures_rejected:negative_fixture_count=5:rejected_fixture_count=5:accepted_fixture_count=0:runtime_ready=0:verified=0
```

## 检查

| 检查 | 结果 |
|---|---|
| GFIS negative fixture guard builder | pass；写入 negative fixture guard JSON/Markdown 和 5 个 rejected example |
| GFIS negative fixture guard validator | pass；`negative_fixture_count=5`、`rejected_fixture_count=5`、`accepted_fixture_count=0` |
| GFIS runtime SOP validator | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GFIS Demo E2E regression | 26 passed；`pass_demo_only`，不作为 runtime SOP acceptance |
| GPCF 状态回写 | partial；不提高完成度 |

## 反馈

- 本轮是 1 个真实实质轮次。
- GFIS 运行层仍是唯一 SOP 主体；GFIS Demo 只能作为展示/培训/前端回归。
- 本轮只证明 live-intake 对 5 类负例保持拒收，不证明签章完成件、客户确认函、采购订单/合同、KDS write receipt 或 WAES confirmation 已取得。
- 未执行 Git push、生产写入、真实外部 API 写入、真实 KDS 写入、真实 WAES 写入、bench migrate、schema sync、权限变更、部署或 ECS/阿里云/Caddy/隧道/Docker 配置变更。

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 9
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一轮

下一轮应在 GFIS 建立真实回执 post-intake 人工/WAES review queue 前置门禁，验证无真实有效回执时 `review_queue=0`、`runtime_intake=0`、`WAES_review=0`、`verified=0`，不得释放 accepted 或 integrated。
