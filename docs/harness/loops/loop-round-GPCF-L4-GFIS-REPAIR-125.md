---
doc_id: GPCF-DOC-87727AC882
title: GPCF-L4-GFIS-REPAIR-125 辽宁远航正式报价单来源 intake
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-125.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-125.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-125 辽宁远航正式报价单来源 intake

## 本轮输入

- 用户确认 `/Users/lujunxiang/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_fi3sre8utioh12_43c3/temp/drag/IGL-LY-QT-20260525-001_Rev.01_正式报价书_审批版.pdf` 是葛化工厂项目报价单。
- GPCF 已受控登记 PDF 与元数据：
  - `08-evidence-samples/GFIS/liaoning-yuanhang/IGL-LY-QT-20260525-001_Rev.01_formal-quotation-approved.pdf`
  - `08-evidence-samples/GFIS/liaoning-yuanhang/IGL-LY-QT-20260525-001_Rev.01_formal-quotation-approved.metadata.md`
- GFIS 当前 `quote_original_intake_preflight` 仍要求客户确认函。

## 本轮目标

把正式报价书审批版从 GPCF 受控样本转入 GFIS 运行层 validator，验证 hash 与关键字段，同时保持客户确认函、采购订单、合同、授权 envelope、责任方回执、review queue、runtime intake 和 verified artifact 全部阻断。

## 本轮输出

- GFIS 新增 `scripts/build_gfis_liaoning_yuanhang_formal_quotation_source_intake.py`
- GFIS 新增 `scripts/validate_gfis_liaoning_yuanhang_formal_quotation_source_intake.py`
- GFIS 新增 `docs/harness/sop-e2e/evidence/liaoning-yuanhang-formal-quotation-source-intake.json`
- GFIS 新增 `docs/harness/sop-e2e/liaoning-yuanhang-formal-quotation-source-intake.md`
- GFIS 主 runtime SOP validator 接入 `runtime_liaoning_yuanhang_formal_quotation_source_intake`

## 验证结果

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_gfis_liaoning_yuanhang_formal_quotation_source_intake.py`：pass
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_liaoning_yuanhang_formal_quotation_source_intake.py`：pass
- GFIS 语法只读 compile：pass
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py`：expected `runtime_validator_rc=2`
- `npm run test:e2e`：26 passed；仅 `pass_demo_only`
- `git diff --check -- .` in GFIS：pass

主 validator 新增输出：

```text
runtime_liaoning_yuanhang_formal_quotation_source_intake=formal_quotation_source_controlled_customer_confirmation_missing:quotation_sources=1:quote_originals=1:hash_valid=1:fields_valid=15:customer_confirmations=0:purchase_orders=0:runtime_ready=0:verified=0
```

## 真实性边界

- 报价 PDF 的 sha256 和 15 项关键字段已验证。
- 报价 PDF 不等于客户确认函、采购订单、合同、授权 envelope、责任方回执或量产验收。
- 本轮不创建 review queue、WAES review、runtime intake 或 verified artifact。
- 本轮不执行生产写入、真实外部 API 写入、bench migrate、schema sync、权限变更、部署或 accepted/integrated 升级。

## 计数与停止

- declared_rounds: `1/15`
- substantive_rounds: `1/15`
- generated_items: `5`
- batch_generated: `false`
- substance_gate: `pass`
- stop_type: `authorization_boundary`

## 下一轮

建立客户确认函/采购订单/合同补证请求包，继续把报价 PDF 作为来源锚点，而不是后续凭证替代物。
