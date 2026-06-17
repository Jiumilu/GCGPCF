---
doc_id: GPCF-DOC-53DE2C5397
title: GPCF-L4-GFIS-REPAIR-144 GFIS 合同链真实回执提交结构门禁
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-144.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-144.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-144 GFIS 合同链真实回执提交结构门禁

## 输入

- GFIS `GFIS-RUNTIME-SOP-E2E-136` 已确认合同链真实回执接收目录存在，但签章完成件、KDS write receipt、WAES confirmation、客户确认函和采购订单/合同均为 0。
- 用户已确认 GFIS 是现代精工 OEM 代加工生产阶段和葛化自建工厂投产后的同一运行时系统。
- 本轮不得把用户口述、计划文字、KDS 候选、合同审阅稿或 GFIS Demo 结果升级为业务完成。

## 动作

- 接收 GFIS 新增的真实回执提交结构门禁、弱材料拒收反例、builder、validator 和只读 API。
- 将 GFIS 主 validator 新增状态回写到 GPCF 总控 loop-state、evidence index、控制板和项目群状态矩阵。
- 保持 GPCF/GFIS `repair_required`，不提升 accepted/integrated。

## 输出

```text
liaoning_yuanhang_contract_chain_real_receipt_submission_schema_gate=pass categories=5 expected_receipt_files=26 rejected_examples=1 valid_receipts=0 runtime_ready=0 verified=0 state=real_receipt_submission_schema_ready_no_valid_receipts runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_contract_chain_real_receipt_submission_schema_gate=real_receipt_submission_schema_ready_no_valid_receipts:categories=5:expected_receipt_files=26:rejected_examples=1:valid_receipts=0:runtime_ready=0:verified=0
```

## 检查

| 检查 | 结果 |
|---|---|
| GFIS schema gate validator | pass |
| GFIS runtime SOP validator | expected exit 2；`gfis_runtime_sop_e2e=repair_required` |
| GPCF 状态回写 | partial；不提高完成度 |

## 反馈

- 本轮是 1 个真实实质轮次。
- GFIS 运行层仍是唯一 SOP 主体；GFIS Demo 只能作为展示/培训/前端回归。
- 本轮只定义真实回执提交结构和拒收反例，不证明任何真实回执已取得。
- 未执行 Git push、生产写入、真实外部 API 写入、真实 KDS 写入、真实 WAES 写入、bench migrate、schema sync、权限变更、部署或 ECS/阿里云/Caddy/隧道/Docker 配置变更。

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 8
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一轮

下一轮应在 GFIS 建立真实回执文件接收 validator 的 live-intake 入口。若真实文件仍缺失，继续保持 `repair_required`，不得释放 review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated。
