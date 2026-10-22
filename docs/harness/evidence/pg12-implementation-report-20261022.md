---
doc_id: GPCF-DOC-PG12-IMPLEMENTATION-REPORT-20261022
title: PG-12 落仓实施报告：A1+A2+A2b（digest 命名空间化 + 三义分列，2026-10-22）
project: GPCF
related_projects: [GPCF, XWAIL, WAME, AAAS, XiaoC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pg12-implementation-report-20261022.md
source_path: docs/harness/evidence/pg12-implementation-report-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PG-12 落仓实施报告：A1+A2+A2b（2026-10-22）

> 任务：**PG-12 落仓 A1+A2+A2b**（老卢已授权跨仓，**不 commit / push**）。
> 依据：`docs/harness/evidence/pg12-implementation-plan-20261022.md`（实施准备建议稿）、`runtime/contract-matrix.yaml`、`09-status/globalcloud-cross-project-contract-matrix-v1.0.md`。
> 范围：仅 A1（XWAIL）/ A2（WAME 双读）/ A2b（WAME 测试基建路径修复）；**未做 A3（AAAS）/ A4（XiaoC）/ A5（GPCF 规格与错误码注册表）**。
> 非声明：不声明契约已冻结/签署/统一完成；不声明任何项目状态提升（`accepted` / `integrated` / `production_ready` / `customer_accepted`）。

## 0. 结论

| 项 | 结果 |
|---|---|
| A1 XWAIL schema + validator + 正负例 | **已落仓（工作区），验证通过**：`check_object_schemas` **PASS 31 / FAIL 0**（基线 26 + 新增 5）；`validate_xwail --all` pass（3 模型 / 0 issue）；`verify_xap --all` pass（1 manifest / 0 issue） |
| A2 WAME 双读 | **已落仓（工作区），验证通过**：intake 测试 **84 tests / OK**（基线 76 + 新增 8），0 失败 |
| A2b REF_ROOTS 路径修复 | **已落仓**：`GlobalCoud GPCF` → `GlobalCloud GPCF`（`tests/test_intake.py` 与 `intake_server.py` 两处同源路径）；原 2 条既有失败（`test_B1a_real_term_and_igl` / `test_B1b_real_cwme_and_repair`）消失 |
| 负例 | 3 条负例均按预期拒绝（schema 层），Python 校验器给出预期码（XAP-1003 / XAP-1001） |
| F-033 legacy 兼容 | F-033 `manifest.xap.json` 在新 schema 与旧 schema 下**均 PASS**；`xap_verify` 完整性校验 pass（完整+无签名） |
| 矩阵状态 | `CONFLICT-01` / `CONFLICT-07`：`closed` → **`mitigated`**（A1+A2 已落仓并验证） |
| 阻塞 | 无阻塞；A3/A4/A5 未做（属后续批次） |

## 1. 授权与边界

- 授权：老卢 2026-10-22 授权 A1+A2+A2b 跨仓改动（不 commit/push）。
- 写入范围：`GlobalCloud XWAIL`（schema/validator/testcases）、`GlobalCloud WAME`（xap-intake 核心/服务/测试）、`GlobalCloud GPCF`（本报告 + 矩阵两文件）。
- 未改：AAAS / XiaoC / PVAOS 任何文件；未改 XWAIL/WAME 其它无关文件；**未 revert 任何他人未提交改动**。
- 开工基线（`git status --porcelain -uall`）：
  - XWAIL：分支 `main`，dirty 1 —— `GlobalCloud XWAIL 总体方案.md`（开工前既有，本任务未触碰）；
  - WAME：分支 `wame/pm-governance`，dirty 1 —— 未跟踪 `docs/harness/evidence/wame-lint-runtime-fix-20261022.md`（开工前既有，本任务未触碰）；
  - GPCF：`runtime/contract-matrix.yaml`、`09-status/globalcloud-cross-project-contract-matrix-v1.0.md`、`docs/harness/evidence/pg12-implementation-plan-20261022.md` 均为未跟踪新文件。

## 2. 改动文件清单

### 2.1 `GlobalCloud XWAIL`（A1）

| 文件 | 类型 | 改动 |
|---|---|---|
| `schemas-json/xap-manifest.schema.json` | 改 | 契约 v1.1（`x-contract-version: "1.1"`）：`required` 去掉 `decision`；`anyOf` 要求 `compatibilityDecision` 或 legacy `decision` 至少其一；新增 `compatibilityDecision`、`schemaVersion`、`requestEnvelopeDigest`、`servicePackageDigest`、`fileManifestDigest`、可选 `signature`（if/then 要求 `digest`）；`$defs.Sha256Hex` 统一 64 位小写十六进制 |
| `scripts/xwail_common.py` | 改 | `validate_xap_manifest()` 双读：new 优先 / legacy deprecated 别名 / 双字段冲突 `XAP-1003`；`schemaVersion` 校验；三命名空间 digest 格式校验；`signature` 结构、`scope`、`digest` 与 `fileManifestDigest` 一致性校验（冲突用既有 `XAP-2004`，**不新增未注册错误码**） |
| `schemas-json/testcases/positive/xap-manifest.schema.json__pos-legacy-decision.json` | 新增 | 正例：仅 legacy `decision`（F-033 风格），additive 兼容 |
| `schemas-json/testcases/positive/xap-manifest.schema.json__pos-v11-signed.json` | 新增 | 正例：v1.1 `compatibilityDecision` + `fileManifestDigest` + `signature` |
| `schemas-json/testcases/negative/xap-manifest.schema.json__neg-compat-governance-enum.json` | 新增 | 负例：`compatibilityDecision: "granted"`（治理枚举误用） |
| `schemas-json/testcases/negative/xap-manifest.schema.json__neg-no-compat-field.json` | 新增 | 负例：两个兼容性字段都缺 |
| `schemas-json/testcases/negative/xap-manifest.schema.json__neg-signature-missing-digest.json` | 新增 | 负例：`signature.scope=package-integrity-v1` 但缺 `digest` |

> `git diff --stat`（tracked）：`xap-manifest.schema.json +63/-2`、`xwail_common.py +63/-2`；新增 5 个 fixture（未跟踪）。

### 2.2 `GlobalCloud WAME`（A2 + A2b）

| 文件 | 类型 | 改动 |
|---|---|---|
| `server/xap-intake/intake_core.py` | 改 | 新增 `COMPAT_DECISIONS` / `COMPAT_READ_MODES` / `COMPAT_READ_ENV`；新增 `_is_asset_like()` 与 `_manifest_contract()`（`legacy|dual|strict` 三模式，默认 dual）；`_validate_asset()` 双读（new 优先、双写冲突 `XAP-1003`、legacy 兼容、strict 收紧）；R06 留白扫描同时排除 `compatibilityDecision` 与 legacy `decision`；`submit()` 对 asset 包在成功/补证/拒收响应中追加 additive `manifestContract`（`generation` / `compatibilityDecisionSource` / `readMode`）；**回执 `decision` 未改**（治理裁定口径不变） |
| `server/xap-intake/intake_server.py` | 改（A2b） | 服务默认 `ref_roots.GPCF`：`GlobalCoud GPCF` → `GlobalCloud GPCF`（目录改名后的同一路径修复） |
| `server/xap-intake/tests/test_intake.py` | 改（A2b + A2） | ① `REF_ROOTS.GPCF` 路径修复（原 2 条失败根因）；② 新增 `Pg12DualReadTests` 8 例：legacy 在 dual 下受理、仅新字段在 dual/strict 受理、legacy 回滚模式下新字段被忽略、strict 拒绝 legacy-only、双字段冲突 `XAP-1003`、非法模式回退 dual、blocked/deprecated 语义保持、`manifestContract` additive 字段 |

> `git diff --stat`（tracked）：`intake_core.py +80/-?`、`intake_server.py +3/-1`、`test_intake.py +94/-?`。

## 3. 真实命令与结果（2026-10-22）

### 3.1 XWAIL（工作区 `GlobalCloud XWAIL`）

| # | 命令 | 结果 |
|---|---|---|
| 1 | `python3 -m py_compile scripts/xwail_common.py` | OK |
| 2 | `python3 scripts/check_object_schemas.py schemas-json` | **`合计：PASS 31 / FAIL 0`**，exit 0（基线 26 + 新增 2 正例 + 3 负例） |
| 3 | `python3 scripts/validate_xwail.py --all` | `status=pass`，`checked=3`，`issue_count=0`，`high_count=0` |
| 4 | `python3 scripts/verify_xap.py --all` | `status=pass`，`checked=1`，`issue_count=0`（legacy `decision` 的 `packages/examples/logistics/manifest.xap.json` 仍通过） |
| 5 | `git diff --check`（仓根） | exit 0（无空白错误） |

### 3.2 WAME（工作区 `GlobalCloud WAME/server/xap-intake`）

| # | 命令 | 结果 |
|---|---|---|
| 1 | `python3 -m py_compile intake_core.py intake_server.py` | OK |
| 2 | `python3 -m unittest discover -s tests -q` | **`Ran 84 tests ... OK`**（基线 76；新增 8；**0 失败**） |
| 3 | `python3 -m unittest tests.test_intake.Pg12DualReadTests -v` | `Ran 8 tests ... OK` |
| 4 | `git diff --check`（仓根） | exit 0（无空白错误） |

## 4. 负例与正例结果（真实输出）

### 4.1 Schema 层（`check_object_schemas.py`）

```text
[negative] PASS xap-manifest.schema.json__neg-compat-governance-enum.json（按预期拒绝）
[negative] PASS xap-manifest.schema.json__neg-no-compat-field.json（按预期拒绝）
[negative] PASS xap-manifest.schema.json__neg-signature-missing-digest.json（按预期拒绝）
合计：PASS 31 / FAIL 0
```

正例 `pos-legacy-decision` / `pos-v11-signed` 均通过（计入 31 PASS）。

### 4.2 Python 校验器层（`xwail_common.validate_xap_manifest`，附加核对）

对 5 个 fixture 直接调用 Python 校验器（fixtures 的 `models[].path` 指向仓内真实模型文件并带真实 sha256，避免"模型缺失"噪声）：

```text
positive pos-legacy-decision              high=0  PASS
positive pos-v11-signed                   high=0  PASS
negative neg-compat-governance-enum       high=1  FAIL（XAP-1003: compatibilityDecision must be compatible, migration_required, deprecated, or blocked）
negative neg-no-compat-field              high=1  FAIL（XAP-1003: compatibilityDecision is required (legacy decision accepted only as deprecated alias)）
negative neg-signature-missing-digest     high=1  FAIL（XAP-1001: signature.digest is required when scope=package-integrity-v1）
```

跨字段冲突用例（Schema 无法表达的判据，Python 校验器补充）：

```text
compatibilityDecision=compatible + decision=migration_required → FAIL（XAP-1003: conflicts with deprecated decision）
signature.digest != fileManifestDigest                          → FAIL（XAP-2004: differs from fileManifestDigest）
```

## 5. F-033 legacy 兼容性

| 检查 | 结果 |
|---|---|
| F-033 `xap-package/manifest.xap.json`（`decision: compatible`，无 `compatibilityDecision`）对 **HEAD 旧 schema** | PASS |
| 同一 manifest 对 **新 schema（工作区 v1.1）** | PASS（additive 兼容成立） |
| `python3 scripts/xap_verify.py "<F-033 xap-package>"` | `包：xap.prompt-asset…@0.1.1`；`文件数：1`；`total_sha256(重算)：ab3f6b6d3edef92d44297a01…`；`⚙️ 完整 + 无签名`，exit 0（与落仓前基线一致） |

**边界说明（既有事实，不由本次改动引入）**：F-033 包内 `models/prompt-asset.json` 是 PromptAsset 快照，不是 XWAILModel；`verify_xap`（模型级校验）会因此报 `XWAIL-1001/6002/2001` 等，F-033 ROUND-01 已明确以 `xap_pack --no-validate` 跳过模型 schema 校验。本报告的兼容性判据为 **manifest 结构/schema 层 + 完整性层**，不重述该既有边界为通过或失败。

## 6. 回滚边界

| 改动 | 回滚方式 | 数据影响 |
|---|---|---|
| XWAIL schema / validator / 5 fixtures | `git -C "GlobalCloud XWAIL" restore -- schemas-json/xap-manifest.schema.json scripts/xwail_common.py`；删除 5 个新增 fixture（`schemas-json/testcases/{positive,negative}/xap-manifest.schema.json__*.json`） | 无 |
| WAME 双读 + A2b | 运行时回滚：`XAP_COMPAT_DECISION_READ=legacy` 重启（回到只认 legacy `decision` 的旧行为）；代码回滚：`git -C "GlobalCloud WAME" restore -- server/xap-intake/intake_core.py server/xap-intake/intake_server.py server/xap-intake/tests/test_intake.py` | 无（**phase 1 无 DB 迁移**；台账 append-only，无 schema 变更） |
| 矩阵状态（`closed → mitigated`） | `git restore` 或把两条 `status` 改回 `closed`（本任务前为 closed） | 无 |
| 本报告 | 删除本文件 | 无 |

统一原则：先回滚 WAME 到 `legacy` 模式（行为立即回旧），再按需 restore 代码；XWAIL schema 回滚不影响任何已被读取的旧 manifest。

## 7. 矩阵状态更新

- `runtime/contract-matrix.yaml`：`CONFLICT-01`、`CONFLICT-07` 的 `status` 由 `closed`（仅裁决）改为 **`mitigated`**（A1+A2 已落仓并验证），新增 `mitigation` 块记录落仓文件、验证命令/结果与证据路径（本报告）。
- `09-status/globalcloud-cross-project-contract-matrix-v1.0.md`：追加落仓状态小节（不改写历史裁决记录），指向本报告。
- 未把状态写为 `closed`（`closed` 语义为"已验证关闭"，需要 A3/A4/A5 与真实消费方回归后才可主张）。
- 未改写 AAAS/XiaoC 契约文件，因此 `CONFLICT-01` 的跨仓覆盖仍为**部分**（service-package 命名空间只在 XWAIL manifest + WAME 双读侧落地，AAAS/XiaoC 文件对齐属 A3/A4）。

## 8. 本批次第一段（A1/A2/A2b）的未做 / 残留（A3/A4/A5 已在 §10 补齐）

1. **A3 AAAS**：`aaas-service-package.schema.json` 的 canonicalization / 禁正文自含 digest、`validate_service_package.py` 新检查——未做。
2. **A4 XiaoC**：候选件 `contentDigest → servicePackageDigest`、登记记录 `requestEnvelopeDigest`、文档口径——未做（候选件仍 `candidate_not_effective`）。
3. **A5 GPCF**：XAP 回执规格条款、XAP 错误码注册表（CONFLICT-02）、矩阵最终状态——未做。
4. `requestedDecision` 的枚举约束未加（F-033 使用 `registered` 等自由值，收紧需单独评估）。
5. WAME `REQ_TYPES` 未加 `service_package_registration`；AaaS candidate marker 的 R06 跳过规则未实现（正式注册链路仍为候选件，需 XiaoC/WAME 联合任务）。
6. WAME 仓其它 `GlobalCoud` 历史引用（`PROJECT_HARNESS_MANIFEST.md`、`docs/current/DECISION_MODEL_RUNTIME_OWNERSHIP.md`、`tools/kds-sync/loop_document_gate.py` 等）不在 A2b 范围，未改。

## 9. 非声明

- 本次改动**未 commit / push**（XWAIL 与 WAME 均为工作区改动 + 新增未跟踪文件）。
- 不声明契约已冻结/签署/统一；`mitigated` 只表示"A1+A2 已落仓并本地验证通过"，不等于跨仓全部对齐。
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`；不声明 WAME 受理链生产可用。
- 验证均为本地、可回放；未运行真实外部 API、未写生产数据。

---

## 10. A3 + A4 + A5 落仓（2026-10-22 追加）

> 本文件 §1–§9 记录 A1/A2/A2b 阶段；本节记录 A3（AAAS）/ A4（XiaoC）/ A5（GPCF 矩阵关闭）落仓与验证。仍为**工作区改动，未 commit / push**。

### 10.1 A3 `GlobalCloud AAAS` 改动文件

| 文件 | 类型 | 改动 |
|---|---|---|
| `schemas-json/aaas-service-package.schema.json` | 改 | 新增可选 `canonicalization`（`algorithm=sha256`、固定 JSON 规范化字符串、`encoding=UTF-8`，与 XiaoC 候选件口径逐字一致）；新增 `not.anyOf` 禁止正文自含 `contentDigest` / `servicePackageDigest` / `requestEnvelopeDigest` / `fileManifestDigest`；`additionalProperties` 保持 true（向后兼容） |
| `scripts/validate_service_package.py` | 改 | 新增 `validate_digest_namespace()`：① 正文自含 digest → `AAAS-1202`；② `canonicalization` 与固定规则不一致 → `AAAS-1203`（AAAS 本地校验器码位，不进入 XAP 错误码空间） |
| `tests/test_pg12_service_package_digest.py` | 新增 | 6 例：现有样例回归 / 正文自含 digest（新名与旧名）拒绝 / 合法 canonicalization 通过 / 错误规则拒绝 / schema 层自含 digest 拒绝 |

### 10.2 A4 `GlobalCloud XiaoC` 改动文件（全部保持 `candidate_not_effective`）

| 文件 | 类型 | 改动 |
|---|---|---|
| `docs/integration/artifacts/wame-service-package-registration.schema.candidate.json` | 改 | `RequestXapEnvelope`：`contentDigest` → `servicePackageDigest`（required 改为 `anyOf` servicePackageDigest/contentDigest 过渡窗口；旧名 `deprecated: true`）；`RegistrationRecord`：`contentDigest` → `servicePackageDigest` + 新增必填 `requestEnvelopeDigest`；`pocPublicationDigest` 描述改为「PoC request-envelope digest 历史证据，不得复用为 servicePackageDigest」；Canonicalization 描述改为 `contents/servicePackageDigest` |
| `...request.candidate.json` | 改 | 顶层 `contentDigest` → `servicePackageDigest`（e0c276…，service-package 命名空间） |
| `...example.candidate.json` / `...bundle.candidate.json` | 改 | 信封与登记记录字段改名；登记记录写 `requestEnvelopeDigest`（由候选信封 canonical JSON（去除 digest 字段）本地复算：example `3b69f0f1…`、bundle `def2d8db…`，仅示例值，WAME 受理时重算） |
| `...pvaos-execution-report.candidate.json` | 改 | `publication.contentDigest` → `publication.requestEnvelopeDigest`（0d858… 属 request-envelope 命名空间），新增 `digestNamespace`/`digestNote` |
| `wame-formal-registration-number-proposal.md`、`wame-service-package-registration-plan.md`、`wame-service-package-registration-local-formal-closeout.md`、`wame-post-poc-reconciliation.md`、`wame-formal-authority-mmc-design.md` | 改 | 追加「PG-12 digest 命名空间口径」对照表；proposal/plan/closeout 的字段名与表述同步（`contentDigest`→`servicePackageDigest`），PoC publication digest 明确为 `requestEnvelopeDigest` |

未改（因其它在途会话已修改，避免叠加）：`docs/integration/README.md`、`wame-xwail-registration-package.md`、`wame-registration-supplement.md`、`wame-capability-channel-confirmation.md` 等；其 `contentDigest` 旧表述按追加口径表读取。通用 `wame-request-envelope.candidate.v2.json`（非 ServicePackage 请求）保留 `contentDigest`，命名空间决策另议。

### 10.3 A5 `GlobalCloud GPCF` 矩阵关闭

| 文件 | 改动 |
|---|---|
| `runtime/contract-matrix.yaml` | `CONFLICT-01` / `CONFLICT-07`：`mitigated` → **`closed`**；追加 `closure` 块（`closed_at` / `closed_scope` / `closed_changes` / `final_verification` / `residual` / `evidence`）；`generated_at` 刷新 |
| `09-status/globalcloud-cross-project-contract-matrix-v1.0.md` | §7 顶部状态说明更新（→ closed）；追加 §8「CONFLICT-01/07 关闭记录（A3+A4+A5）」：A3/A4 改动、验证、关闭后边界、非声明 |
| 本文件 | 追加本节（§10） |

### 10.4 验证（真实输出）

| # | 命令 | 结果 |
|---|---|---|
| 1 | AAAS 5 个本地校验器 `--all`（service package / binding / metering / SLA / evidence） | 全部 exit 0；现有 2 个样例 pass |
| 2 | AAAS `python3 -m unittest tests.test_pg12_service_package_digest -v` | **Ran 6 tests ... OK** |
| 3 | AAAS `python3 -m unittest discover -s tests -q` | **Ran 10 tests ... OK**（含既有 `test_local_gates`） |
| 4 | XiaoC 候选件 JSON 解析（4 文件） | 全部 OK |
| 5 | XiaoC jsonschema 校验 | example/bundle 对根 schema PASS；request/example/bundle 的 envelope 对 `RequestXapEnvelope` PASS；legacy `contentDigest`-only 仍 PASS（兼容窗口）；无 digest 字段 REJECT（预期） |
| 6 | WAME `python3 -m unittest discover -s tests -q`（回归） | **Ran 84 tests ... OK** |
| 7 | GPCF `python3 tools/kds-sync/validate_contract_matrix.py` | **PASS**（8 条冲突：**2 closed / 6 open**；`evidence_paths=pass`） |

### 10.5 负例结果（A3）

```text
正文自含 servicePackageDigest → 拒绝（AAAS-1202）
正文自含旧名 contentDigest    → 拒绝（AAAS-1202）
canonicalization 规则不一致    → 拒绝（AAAS-1203）
schema 层正文自含 digest       → jsonschema 拒绝
```

### 10.6 回滚边界（A3/A4/A5）

| 改动 | 回滚 |
|---|---|
| AAAS schema / validator / 新测试 | `git -C "GlobalCloud AAAS" restore -- schemas-json/aaas-service-package.schema.json scripts/validate_service_package.py`；删除 `tests/test_pg12_service_package_digest.py` |
| XiaoC 候选件 / 文档 | `git -C "GlobalCloud XiaoC" restore -- docs/integration/artifacts/... docs/integration/*.md`（候选件 `candidate_not_effective`，无生产影响） |
| GPCF 矩阵 | 将两条 `status` 改回 `mitigated`（或 `git restore` 矩阵两文件）；状态回退不影响 A1–A4 代码 |
| 数据 | 无 DB 迁移、无生产写入；无需数据回滚 |

### 10.7 关闭后边界 / 非声明

- `CONFLICT-01` / `CONFLICT-07` 的 `closed` 表示 A1–A4 已落仓并本地验证、A5 矩阵刷新完成；**不表示**跨仓生产集成、契约冻结/签署。
- AAAS/XiaoC 均为 candidate / 本地校验；正式 WAME 注册/授权/发布仍需 WAME owner/registry/MMC 确认；WAME 主线仍无 `registrations` 表/端点。
- 未新增未注册 XAP 错误码（XWAIL/WAME 复用既有码；AAAS 使用本地 AAAS 码位）。
- 未 commit / push；不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
