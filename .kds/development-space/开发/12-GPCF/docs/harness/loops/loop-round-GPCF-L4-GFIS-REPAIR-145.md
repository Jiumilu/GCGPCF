---
doc_id: GPCF-DOC-0746434FE9
title: GPCF-L4-GFIS-REPAIR-145 GFIS 合同链真实回执 live-intake validator
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-145.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-145.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-145 GFIS 合同链真实回执 live-intake validator

## 输入

- GFIS `GFIS-RUNTIME-SOP-E2E-137` 已定义 5 类真实回执、26 个预期文件槽位和弱材料拒收规则。
- 用户确认：葛化工厂仍在建设阶段，当前使用现代精工工厂进行 OEM 代加工；GFIS 是现代精工代加工生产阶段及葛化自建工厂投产后的同一运行时系统。
- 本轮不得把用户口述、计划文字、KDS 候选、合同审阅稿或 GFIS Demo 结果升级为业务完成。

## 动作

- 接收 GFIS 新增的辽宁远航合同链真实回执 live-intake validator、接收目录 README、builder、validator 和只读 API。
- 将 GFIS 主 validator 新增状态回写到 GPCF 总控 loop-state、evidence index、控制板和项目群状态矩阵。
- 保持 GPCF/GFIS `repair_required`，不提升 accepted/integrated。

## 输出

```text
liaoning_yuanhang_contract_chain_real_receipt_live_intake_validator=pass scanned_receipt_slots=26 submitted_files=0 valid_receipts=0 missing_files=26 runtime_ready=0 verified=0 state=real_receipt_live_intake_blocked_no_valid_receipts runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_contract_chain_real_receipt_live_intake_validator=real_receipt_live_intake_blocked_no_valid_receipts:scanned_receipt_slots=26:submitted_files=0:valid_receipts=0:missing_files=26:runtime_ready=0:verified=0
```

## 检查

| 检查 | 结果 |
|---|---|
| GFIS live-intake builder | pass；写入 live-intake JSON/Markdown 与接收目录 README |
| GFIS live-intake validator | pass；`submitted_files=0`、`valid_receipts=0`、`missing_files=26` |
| GFIS runtime SOP validator | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GPCF 状态回写 | partial；不提高完成度 |

## 反馈

- 本轮是 1 个真实实质轮次。
- GFIS 运行层仍是唯一 SOP 主体；GFIS Demo 只能作为展示/培训/前端回归。
- 本轮只建立真实回执 live-intake 扫描入口，不证明任何真实回执已取得。
- 未执行 Git push、生产写入、真实外部 API 写入、真实 KDS 写入、真实 WAES 写入、bench migrate、schema sync、权限变更、部署或 ECS/阿里云/Caddy/隧道/Docker 配置变更。

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 7
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一轮

下一轮应在 GFIS 建立 live-intake 无效结构/拒收 fixture 门禁，验证伪造、缺字段、弱证据、Demo 证据和未签章合同审阅稿都不能释放 review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated。
