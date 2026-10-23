---
doc_id: GPCF-DOC-BATCH2-PREREQUISITES-20261022
title: 批次 2 前置补齐核查（2026-10-22）
project: GPCF
related_projects: [GPCF, GFIS, GPC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/batch2-prerequisites-20261022.md
source_path: docs/harness/evidence/batch2-prerequisites-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 批次 2 前置补齐核查（GFIS 5 类真实单据 / GPC 外部 runtime）

> 性质：**只读核查**。不创建凭据、不读取凭据、不发起外部请求、不做联调、不写生产。
> 批次 2 定义来源：`09-status/globalcloud-external-authorization-list-v1.0.md`（§1 第 1、2 项，§3 批次 2）。

## 1. 批次 2 的两条前置（原文）

| # | 授权项 | 类别 | 当前状态 | 前置条件 |
|---:|---|---|---|---|
| 1 | `AUTH-WAVE1-GFIS-REAL-SOR-20260626` GFIS 真实 source-of-record 接入 | C 真实数据 | pending | **5 类真实单据（订单/规格/交付/责任方/回款）到齐** |
| 2 | `AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626` GPC 外部 runtime 联调 | C 外部联调 | pending_confirmation（`09-status/globalcloud-project-group-single-authorization-ledger-v1.0.md` 第 8 行） | **运行宿主就绪（PG-11）、外部接口可达** |

## 2. GFIS 5 类真实单据矩阵

口径：GFIS 已建立 12 个运行对象、**62 个 live proof 预期槽位**（`docs/harness/sop-e2e/liaoning-yuanhang-runtime-document-evidence-slot-receiving-structure.md`）；本表按槽位标题把 5 类归并。**槽位全部就绪，文件提交数 = 0**。

| 类别 | 对应接收槽位（对象 · 槽位标题） | 现状 | 已有证据（路径） | 缺口 |
|---|---|---|---|---|
| 订单 | `PlatformOrderCandidate` · 真实客户订单原件或平台订单回执、订单数量或平台需求数量；`GFISFactoryOrder` · 客户销售合同签章完成件或采购订单 | **missing** | 仅 `08-evidence-samples/GFIS/liaoning-yuanhang/IGL-LY-QT-20260525-001_Rev.01_formal-quotation-approved.pdf`（**报价单**，627KB，hash 通过） | 客户订单原件／平台订单回执／签章采购订单，0 份 |
| 规格 | `PlatformOrderCandidate` · 产品规格、PP 一级料技术口径和验收口径；`RawMaterialPlanOrBatch` · PP 一级料/改性料规格与技术口径；`QualityInspection` · 过程/成品检验标准 | **missing** | 无（`08-evidence-samples/GFIS/source-files/` 仅有 `现代精工工厂岗位培训学习资料_优化版.pdf`，非单据） | 规格书、技术口径、验收/检验标准，0 份 |
| 交付 | `PlatformOrderCandidate` · 交期或分批交付计划；`DeliveryNote` 5 槽位；`ProofOfDeliveryReference` 5 槽位 | **missing** | 无 | 交期计划、发货/出库凭证、运输记录、客户签收 POD，0 份 |
| 责任方 | `PlatformOrderCandidate` · 客户主体身份与收货主体确认；`SampleRequest` · 客户签样、反馈或等效正式确认；POD · 客户签收原件；intake gate 要求 `owner_confirmation.valid=true` | **missing** | 无（`owner_response_files_scanned=0`） | 责任方/客户主体确认、签样或等效确认，0 份 |
| 回款 | `BusinessLedgerFinanceCandidate` 5 槽位（应收依据、发货与 POD 确认、开票候选、回款或收款确认、人工财务确认） | **missing** | 无 | 回款/收款确认、开票边界，0 份 |
| **合计** | 12 对象 / 62 槽位 | **0 / 5 类到齐** | 报价单 1 份（仅候选线索） | 5 类全部缺失 |

判定依据（实测命令与输出）：

```text
$ python3 scripts/validate_gfis_real_source_record_intake_gate.py     # 在 GlobalCloud GFIS 仓执行
gfis_real_source_record_intake_gate=pass real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 real_runtime_intake_items=0 real_wame_reviews=0 real_verified_artifacts=0 real_business_lane=repair_required business_verification_pending=true

$ python3 scripts/validate_gfis_pending_business_verification.py
gfis_pending_business_verification=pass kds_candidate_sources_found=607 owner_response_files_scanned=0 rejected_example_files_excluded=18 pending_submission_files_found=0 pending_business_verification_submissions=0
```

> 口径校正：`docs/harness/evidence/batch2-feasibility-20261022.md` 记「已有真实单据 1 类（报价 PDF）」。按 intake gate 自身规则（“不把报价单-only 当作真实 source-of-record”），报价 PDF **不计入 5 类**，故本核查记 **0/5**。

## 3. 客户确认状态

| 项 | 值 | 证据 |
|---|---|---|
| 报价来源状态 | `source_state = formal_quotation_source_controlled_customer_confirmation_missing` | `GlobalCloud GFIS/docs/harness/sop-e2e/evidence/liaoning-yuanhang-formal-quotation-source-intake.json` |
| 确认字段 | `customer_confirmation`、`owner_confirmation` **均不存在**（JSON 中 absent） | 同上 |
| 报价确认候选 | `candidates=55 formal=0 weak=7 attachments=7 discovered=37` | `python3 scripts/validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py` |
| 业务验证门 | `business_verification_pending=true`、`runtime_sop_e2e=repair_required` | intake gate 输出 |

结论：**客户/责任方确认缺失（formal=0）**，报价单不可替代采购确认或订单。

## 4. 缺口清单与属主动作

| # | 缺口 | 属主 | 动作（不代为执行） |
|---:|---|---|---|
| 1 | 5 类原件（订单/规格/交付/责任方/回款）共 0 份 | 业务方（辽宁远航、现代精工） | 提供脱敏原件或等效正式确认；单据编号与签章齐备 |
| 2 | 客户确认函/等效确认（formal=0） | 客户（辽宁远航） | 出具客户确认函或采购确认；仅报价单不成立 |
| 3 | 接收与 source validation | GFIS 属主 | 按 12 槽位接收→`source_record_hash` 登记→跑 intake gate/pending 校验，产出 `valid-source-record-index.json` |
| 4 | 责任方与收货主体身份确认 | GFIS + 业务方 | 补 `owner_confirmation.valid=true` 及收货主体确认 |
| 5 | 回款/开票边界 | GFIS + 财务方 | 补应收依据、发货/POD 确认、回款确认 |
| 6 | 批次 2 授权回执 | GPCF | 授权清单回执登记；不得以本核查替代授权 |

## 5. GPC 外部 runtime 就绪度（只读）

| 检查项 | 结果 | 证据 |
|---|---|---|
| 仓状态 | HEAD `aae1feb`（2026-10-22）；脏 1 项（`GlobalCloud GPC 总体方案.md`） | `git -C "GlobalCloud GPC" log -1` / `status --porcelain` |
| PG-11 引用 | **0 命中**（GPC 仓内无 PG-11 任何配置或文档） | `rg -n "PG-11|PG11" "GlobalCloud GPC"` |
| 运行入口 | 仅本地：`GCFIS_RUNTIME_URL=http://127.0.0.1:8080`、`DESK_URL`、`ASSET_URL` 同为本地 | `GlobalCloud GPC/docs/19-gcfis-environment-release-runbook.md` §1 |
| 外部地址 | **未定义**：仓内无公网域名、无 Caddy/nginx/隧道配置、无 external runtime check 证据 | `rg -l "external runtime check"` 仅命中 GPCF 台账，GPC 仓 0 命中 |
| 容器/宿主清单 | 仅 `gcfis_demo/docker-compose.gcfis-local.yml`（本地 Frappe bench，非外部宿主） | 文件路径 |
| 端口占用 | `127.0.0.1:8080` 由 Python 进程（PID 798）监听，**归属待核**；与 GPC 本地入口端口冲突风险 | `lsof -nP -iTCP:8080 -sTCP:LISTEN` |
| PG-11 端点清单 | `docs/runbooks/runtime-host-v1.0.md` 已盘点 Hermes/GCMEM/StartLux/SpaceAI/PQC/XiaoC/MMC，**不含 GPC** | 同左 |
| 权限/访问控制 | 无外部访问控制与权限边界证据（本次不触碰凭据） | — |

结论：GPC 外部 runtime **未就绪**——宿主未定义（PG-11 无 GPC 落点）、外部地址未定义、权限未确认、external runtime check 证据缺失。

## 6. 批次 2 就绪结论

| 前置 | 判定 | 说明 |
|---|---|---|
| GFIS 5 类真实单据到齐 | **否（0/5）** | 12 对象/62 槽位结构就绪、文件提交 0；客户确认 formal=0 |
| GPC 运行宿主就绪（PG-11）+ 外部接口可达 | **否** | 宿主/外部地址/权限/可达性四项均无证据 |
| **批次 2 总体** | **否（0/2 前置满足）** | 具备“可执行条件”的只有接收结构与门禁脚本，不构成批次 2 就绪 |

分项状态：GFIS = `partial`（结构就绪、数据 0）；GPC = `not_ready`。

## 7. 下一步（建议，不执行）

1. **GFIS**：业务方先交 1 份最小可验证组合（订单 + 规格 + 责任方确认），走通一次 source validation 到 `valid_source_records=1`，再扩到 5 类；沿用 `valid-source-record/` 与 12 槽位目录。
2. **GPC**：先出 PG-11 落点方案（宿主、端口、外部地址、访问控制）与 `external runtime check` 脚本/证据，再谈联调；8080 归属需先裁定。
3. **GPCF**：待两条前置有实证后，重新提交批次 2 授权申请（`AUTH-WAVE1-GFIS-REAL-SOR-20260626`、`AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626`），回执入授权台账。

## 8. 非声明

- 不声明批次 2 已就绪或已执行；不声明真实业务验证通过。
- 不声明 GFIS/GPC 任何状态提升（`accepted`/`integrated`/`production_ready`/`customer_accepted`）。
- 不声明外部接口可达、宿主可用、权限已确认。
- 本文件不替代 GFIS/GPC 项目级方案与 Feature 证据；未创建、未读取任何凭据。
