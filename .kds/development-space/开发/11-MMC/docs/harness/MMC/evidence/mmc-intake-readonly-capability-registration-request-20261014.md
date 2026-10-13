---
doc_id: GPCF-DOC-MMC-INTAKE-REG-REQUEST-20261014
title: MMC 受理器只读能力登记请求 2026-10-14
project: MMC
related_projects: [GPC, WAME, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: MMC
kds_space: 开发
kds_path: 开发/11-MMC/docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.md
source_path: docs/harness/MMC/evidence/mmc-intake-readonly-capability-registration-request-20261014.md
sync_direction: bidirectional
last_reviewed: 2026-10-14
supersedes: []
superseded_by: []
---

# MMC 受理器只读能力登记请求 2026-10-14

## 1. 定位

本文为 `MMC-INTAKE-READONLY-CAPABILITY-REGISTRATION-REQUEST-20261014` 的受控证据件：请求治理方批准 MMC 将 **XWAIL 受理器（xap-intake·:3210）的 6 条只读能力**登记入 MMC 能力目录（candidate 态）。

本件只做**登记请求**——不改受理器、不改 WAES 仓、不接写面；裁定权属治理方。

## 2. 请求内容

| # | capability_id | 方法 | 路径 |
|---|---|---|---|
| 1 | `intake.xap.health` | GET | `/health`（现场实测 200） |
| 2 | `intake.xap.requests_list` | GET | `/intake/requests` |
| 3 | `intake.xap.request_get` | GET | `/intake/requests/<rid>` |
| 4 | `intake.xap.receipt_get` | GET | `/intake/receipts/<rid>` |
| 5 | `intake.xap.publication_get` | GET | `/intake/publications/<packageId>/<version>` |
| 6 | `intake.xap.projects_list` | GET | `/projects` |

**排除写面**（明示不接）：`/intake/submit`、`/intake/resubmit`、`/intake/decide`、`/intake/publish`、`/intake/revoke`、`/intake/execution-report`、`POST /projects`、`/projects/sync`。

## 3. 边界

- **请求范围**（`scope`）：mmc_intake_readonly_capability_registration_request_only；
- **请求裁定**（`requested_decision`）：admit_intake_readonly_capabilities_into_mmc_catalog；
- **当前裁定态**（`current_decision`）：`accepted`（2026-10-14·老卢「受理」）。

## 4. 门禁清单

```text
request_package_generated | true
submitted | true
governance_reviewed | true
accepted | true
registry_entry_added | true
wame_authorized | false
production_ready | false
```

## 5. 受理记录

- **裁定**：accepted（2026-10-14）；
- **授权来源**：老卢「受理」（会话逐字·2026-10-14）；
- **依据**：requested_decision=admit_intake_readonly_capabilities_into_mmc_catalog（6 只读能力·候选登记·写面排除）；
- **next_step**：MMC catalog 登记 6 只读能力（candidate 态）→ `registry_entry_added` 翻 true。

## 6. 非声明

不改受理器代码/数据；不改 WAES 仓；不接写面；候选登记（非运行授权）；治理裁定记录以 GPCF evidence 为权威（本件保持 `pending_governance_review`）。
