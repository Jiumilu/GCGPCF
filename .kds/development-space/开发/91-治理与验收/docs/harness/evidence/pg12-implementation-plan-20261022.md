---
doc_id: GPCF-DOC-PG12-IMPLEMENTATION-PLAN-20261022
title: PG-12 实施准备：digest 命名空间化与三义分列（2026-10-22）
project: GPCF
related_projects: [GPCF, XWAIL, WAME, AAAS, XiaoC, PVAOS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pg12-implementation-plan-20261022.md
source_path: docs/harness/evidence/pg12-implementation-plan-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PG-12 实施准备：digest 命名空间化与三义分列（2026-10-22）

> 任务：**PG-12 实施准备（不跨仓写）**。只写本文件；不修改 XWAIL / WAME / AAAS / XiaoC 任何仓；不 commit / push。
> 依据：裁决 A（`CONFLICT-01` digest 命名空间化、`CONFLICT-07` 三义分列）｜`runtime/contract-matrix.yaml`｜`09-status/globalcloud-cross-project-contract-matrix-v1.0.md`｜`docs/harness/evidence/pg12-contract-adjudication-pack-20261022.md`。
> 性质：**实施准备 / 建议稿**。本文所有 schema 片段、代码 diff、字段映射均为**建议，未落仓**；"现状"均来自只读核对（§4.1 记录真实命令与输出），未伪造任何执行结果。
> 非声明：不声明任何跨仓改动已完成、任何契约已统一/冻结、任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`。

## 0. 一页结论

| 仓 | 建议改动（建议，未落仓） | 落地门槛 | 依赖 |
|---|---|---|---|
| XWAIL | `schemas-json/xap-manifest.schema.json`、`scripts/xwail_common.py`、`schemas-json/testcases/{positive,negative}` | 需 XWAIL 属主授权（A1） | 无（可先落） |
| WAME | `server/xap-intake/intake_core.py` 双读、`tests/test_intake.py` 新测试；（可选）测试基建 `REF_ROOTS` 路径修复 | 需 WAME 属主授权（A2） | A1（建议先落 schema） |
| AAAS | `schemas-json/aaas-service-package.schema.json` 增 canonicalization + 禁自含 digest、`scripts/validate_service_package.py` 增校验 | 需 AAAS 属主授权（A3） | A1/A2 的命名空间定义 |
| XiaoC | `docs/integration/artifacts/*.candidate.json`（candidate）字段对齐、`docs/integration/*.md` 口径更新 | 需 XiaoC 属主授权（A4） | A1–A3；全部保持 `candidate_not_effective` |
| GPCF | 本文；后置：XAP 规格条款、错误码注册表（CONFLICT-02）、矩阵状态刷新 | 需 GPCF/老卢（A5，后置） | A1–A4 |

**关键现状判断（只读核对）**：
1. XWAIL manifest Schema **没有** `signature` / `digest` 定义（靠 `additionalProperties: true` 放行），且 `required` 仍强制 `decision`（兼容性枚举）。
2. WAME 受理实现已按"三义分列"处理了 `decision`（排除留白扫描）与 `requestedDecision`（排除），但**没有** `compatibilityDecision` 双读；`REQ_TYPES` **没有** `service_package_registration`；主线**没有**正式注册表/端点（正式注册仍为 XiaoC 候选件 + transition 分支，未并入主线）。
3. XiaoC 候选 Schema 已把 `contentDigest` 定义为 **AaaS ServicePackage 包体** canonical SHA-256（不是信封 digest），并有 `registrationRecord.contentDigest` / `pocPublicationDigest`；AAAS 主线 Schema 无任何 digest 字段（最小 schema）。
4. 基线回归：XWAIL 三组校验全绿；WAME 受理测试 **76 运行 / 2 失败**（已知成因：测试基建 `REF_ROOTS` 指向改名前的 `GlobalCoud GPCF`，证据引用不可访问 → 待补证），属**开工前既有**，不得算作本轮新回归（§4.1）。
5. 建议稿已在**内存**中完成 JSON Schema 自检与正负例预演（§1.5）：建议 schema 通过 Draft2020-12 元 schema 自检；2 条正例通过、3 条负例按预期拒绝；真实 F-033 legacy manifest 通过（additive 兼容成立）。该预演**不替代**落仓后回归。

## 1. XWAIL `xap-manifest.schema.json` 建议 diff（建议，未落仓）

### 1.1 现状（原文摘要）

`GlobalCloud XWAIL/schemas-json/xap-manifest.schema.json`（894 B，`additionalProperties: true`）：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://globalcloud.example/xwail/xap-manifest.schema.json",
  "required": ["packageId", "version", "wasBaseline", "ontologyVersion", "xwailVersion", "wameStatus", "decision", "models"],
  "properties": {
    "wameStatus": {"enum": ["Draft", "Registered", "Authorized", "Published", "Deprecated", "Archived"]},
    "decision": {"enum": ["compatible", "migration_required", "deprecated", "blocked"]},
    "models": {"type": "array", "minItems": 1}
  },
  "additionalProperties": true
}
```

Python 侧独立校验器 `scripts/xwail_common.py:validate_xap_manifest()` 额外强制：`decision` 必填且属 `ALLOWED_DECISIONS`（违反 → `XAP-1003`）、`wameStatus` 枚举（`XAP-1002`）、`models` 非空与逐文件 sha256（`XAP-2001/2002/2003/2004`）、Authorized/Published 需 `wameEvidenceRef`（`XAP-5001`）。**schema 与 Python 校验器必须同批改，否则两套判据漂移。**

### 1.2 问题映射（裁决 A 要求）

| 冲突 | 现状 | 建议处理 |
|---|---|---|
| `CONFLICT-07` | manifest 字段名 `decision`（兼容性枚举），与回执 `decision`（治理枚举）同名 | 新增 `compatibilityDecision`；`decision` 降级为 **deprecated 兼容别名**（1.x 保留、2.0 移除）；`required` 改为 `anyOf` 二者至少其一 |
| `CONFLICT-01` | 无作用域 digest 字段；`signature.digest`（xap_sign）未入 Schema | 新增三个**显式带作用域**的 digest 字段：`requestEnvelopeDigest` / `servicePackageDigest` / `fileManifestDigest`；`signature.digest` 语义绑定 `file-manifest` |
| `CONFLICT-05` | 无 `signature` 定义 | 新增可选 `signature` 对象（字段对齐 `xap_sign.py` 实际输出）；**不在 manifest 内自证"签名有效"**，验签结论由验证方/受理台账记录 |

### 1.3 建议 schema（完整建议稿，未落仓）

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://globalcloud.example/xwail/xap-manifest.schema.json",
  "title": "XAP Manifest Minimal Schema (contract v1.1 proposal)",
  "x-contract-version": "1.1",
  "type": "object",
  "required": ["packageId", "version", "wasBaseline", "ontologyVersion", "xwailVersion", "wameStatus", "models"],
  "anyOf": [
    {"required": ["compatibilityDecision"]},
    {"required": ["decision"]}
  ],
  "properties": {
    "packageId": {"type": "string", "minLength": 1},
    "version": {"type": "string", "minLength": 1},
    "wasBaseline": {"type": "string", "minLength": 1},
    "ontologyVersion": {"type": "string", "minLength": 1},
    "xwailVersion": {"type": "string", "minLength": 1},
    "wameStatus": {"enum": ["Draft", "Registered", "Authorized", "Published", "Deprecated", "Archived"]},
    "schemaVersion": {"enum": ["1.0", "1.1"], "description": "可选；缺省按 1.0 legacy 处理"},
    "compatibilityDecision": {
      "enum": ["compatible", "migration_required", "deprecated", "blocked"],
      "description": "兼容性判断（三义分列之一）。治理裁定不在 manifest；不得取 accepted/granted/rejected 等回执枚举"
    },
    "decision": {
      "enum": ["compatible", "migration_required", "deprecated", "blocked"],
      "deprecated": true,
      "description": "DEPRECATED：v1.0 兼容别名，语义等同 compatibilityDecision；新写入方必须写 compatibilityDecision"
    },
    "requestEnvelopeDigest": {
      "$ref": "#/$defs/Sha256Hex",
      "description": "request-envelope 命名空间：请求信封 canonical sha256（由受理方计算，进幂等键/发布记录；不是包体 digest）"
    },
    "servicePackageDigest": {
      "$ref": "#/$defs/Sha256Hex",
      "description": "service-package 命名空间：AaaS ServicePackage 正文 canonical sha256（不是信封 digest；不得复用 PoC 信封 digest）"
    },
    "fileManifestDigest": {
      "$ref": "#/$defs/Sha256Hex",
      "description": "file-manifest 命名空间：XWAIL 逐文件 sha256 汇总 totalSha256（签名对象）；须注明 artifactKind=dir|zip"
    },
    "signature": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "keyId", "signature", "scope"],
      "properties": {
        "algorithm": {"const": "Ed25519"},
        "keyId": {"type": "string", "minLength": 1},
        "publicKey": {"type": "string", "minLength": 1},
        "signature": {"type": "string", "minLength": 1},
        "signedAt": {"type": "string", "minLength": 1},
        "scope": {"const": "package-integrity-v1"},
        "digest": {"$ref": "#/$defs/Sha256Hex"},
        "signNote": {"type": "string"}
      },
      "description": "签名证据（可选）。只声明签名对象与算法，不自证有效性。",
      "allOf": [
        {
          "if": {"properties": {"scope": {"const": "package-integrity-v1"}}, "required": ["scope"]},
          "then": {"required": ["digest"]}
        }
      ]
    },
    "models": {"type": "array", "minItems": 1}
  },
  "additionalProperties": true,
  "$defs": {
    "Sha256Hex": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
  }
}
```

说明（全部为建议）：
- `$id` **不变**（避免已引用方断裂），用 `x-contract-version` 标注契约代际；`additionalProperties: true` 保持（旧 manifest 的 `profileVersion` / `aaasServicePackageVersion` / `rollback` / `boundary` 等扩展键仍被放行）。
- `signature.digest` 与 `fileManifestDigest` 是同一命名空间的两种落点：**若同时存在必须相等**（JSON Schema 无法表达相等，由 XWAIL/WAME 校验器判）。
- `schemaVersion` 可选：缺省 = 1.0 legacy；新写入方建议写 `"1.1"`。
- 负例 3 条见 §1.4；正例 2 条用于守住"旧包仍通过 / 新包带签名通过"。

### 1.4 建议负例（3 条）与正例（2 条）

放置：`GlobalCloud XWAIL/schemas-json/testcases/{positive,negative}/xap-manifest.schema.json__<case>.json`（`check_object_schemas.py` 按 `文件名__前缀` 匹配 schema）。**当前该目录下没有 xap-manifest 的任何样例（只读核对），需新增。**

| # | 文件（建议） | 构造 | 期望 |
|---|---|---|---|
| N1 | `negative/xap-manifest.schema.json__neg-compat-governance-enum.json` | `compatibilityDecision: "granted"`（把治理回执枚举写进兼容性字段） | 拒绝（enum 不符）→ 对应 CONFLICT-07 误用 |
| N2 | `negative/xap-manifest.schema.json__neg-no-compat-field.json` | 既无 `compatibilityDecision` 也无 legacy `decision` | 拒绝（`anyOf` 不满足） |
| N3 | `negative/xap-manifest.schema.json__neg-signature-missing-digest.json` | `signature.scope="package-integrity-v1"` 但缺 `signature.digest` | 拒绝（`if/then` 要求 digest） |
| P1 | `positive/xap-manifest.schema.json__pos-legacy-decision.json` | 只带 legacy `decision: "compatible"`（F-033 风格旧包） | 通过（1.x 兼容） |
| P2 | `positive/xap-manifest.schema.json__pos-v11-signed.json` | `compatibilityDecision: "compatible"` + `schemaVersion: "1.1"` + `signature{...digest}` | 通过 |

建议同批在 `xwail_common.validate_xap_manifest()` 增加（超出 JSON Schema 能力的判据）：
- 双字段并存且值不同 → `XAP-1003`（复用现有码；新码需待 CONFLICT-02 错误码注册表裁决，**本计划不新增未注册码**）；
- `signature.digest` ≠ `fileManifestDigest` → `XAP-1003`；
- `schemaVersion: "1.1"` 但两个 decision 字段都缺 → `XAP-1003`（与 `anyOf` 同义，供 Python 校验器给出可读信息）。

### 1.5 建议稿的本地内存校验（**非落仓验证**，仅验证"建议 schema 自身可判"）

在不写任何文件的前提下，把 §1.3 建议 schema 与 §1.4 的 5 个用例在**内存中**跑 `jsonschema` Draft2020-12 校验（2026-10-22 实测）：

```text
Draft2020-12 元 schema 自检：OK
P1 legacy decision（真实 F-033 风格）        → PASS
P2 v1.1 + signature（含 digest）            → PASS
N1 compatibilityDecision="granted"          → REJECT（'granted' is not one of ['compatible', 'migration_required', ...]）
N2 两个 decision 字段都缺                    → REJECT（anyOf 不满足）
N3 signature.scope=package-integrity-v1 缺 digest → REJECT（'digest' is a required property）
真实 F-033 legacy manifest（只读载入）       → PASS（additive 兼容成立）
```

**口径**：该结果只证明"建议稿在 JSON Schema 层面可判、正负例行为符合预期"，**不替代**落仓后的 `check_object_schemas.py` 回归（§4.2 R1），也不代表任何仓已接受该 schema。

## 2. WAME 受理/回执双读过渡方案（建议，未落仓）

### 2.1 现状（只读核对，`server/xap-intake/intake_core.py`）

- `REQ_TYPES` 仅 8 类（`asset_registration` / `domain_registration` / `term_request` / `state_request` / `authorization` / `repair_request` / `arche_registration` / `other`）——**无 `service_package_registration`**（与 XiaoC 候选注册请求的 `requestType` 不一致，当前会在 R02 被判非法）。
- `_validate_asset()`：`required` 含 `decision`；`A05` 对 `blocked` 直接拒、`deprecated` 给补证提示、其余值不在 `("compatible","migration_required")` 即阻断；**留白扫描前剔除 `decision`**（`scan_target = {k:v for ... if k != "decision"}`）。
- 请求包（`packageKind=request`）侧：`contentDigest` 与 `sha256(canonical(contents))` 比对（不符 `XAP-2004`）；`requestedDecision` 已在 `_scan_ruling_claims` 排除；`to=wame`、`evidenceRefs` 格式与前缀存在性（不可访问 → 待补证）。
- 三义现状：回执 `DECISIONS = {rejected, returned_for_evidence, accepted, granted, revoked}`（治理裁定，**保持不变**）；manifest `decision` = 兼容性（**待改名**）；请求包 `requestedDecision` = 请求结果（已分列，仅缺枚举约束）。
- 发布记录 `publications.content_digest = sha256(envelope)`（**request-envelope 命名空间**；F-033 PoC 值 `0d858501…` 即此口径，不得被当作 ServicePackage 包体 digest）。
- 主线**无**正式注册表（`registrations`）、无注册端点；XiaoC 正式注册仍为候选件 + transition 分支（未并入主线）。

### 2.2 双读规则（建议伪 diff）

```python
# intake_core.py — _validate_asset()（建议，未落仓）
-required = [..., "wameStatus", "decision", "governanceOwner", "models"]
+required = [..., "wameStatus", "governanceOwner", "models"]      # decision 由双读判定
...
-decision = env.get("decision")
+COMPAT_DECISIONS = {"compatible", "migration_required", "deprecated", "blocked"}
+compat_new = env.get("compatibilityDecision")
+compat_legacy = env.get("decision")
+read_mode = os.environ.get("XAP_COMPAT_DECISION_READ", "dual")   # legacy|dual|strict
+if read_mode == "strict" and compat_new is None:
+    blockers.append("A05: strict 模式要求 compatibilityDecision（legacy decision 不再受理）")
+if compat_new is not None and compat_legacy is not None and compat_new != compat_legacy:
+    blockers.append("XAP-1003: compatibilityDecision 与 legacy decision 冲突（值不同）")
+decision = compat_new if compat_new is not None else compat_legacy
+source = ("compatibilityDecision" if compat_new is not None
+          else ("legacy_decision" if compat_legacy is not None else None))
+if decision not in COMPAT_DECISIONS:
+    blockers.append(f"A05: 兼容性 decision 非法（现值={decision}）")
 elif decision == "blocked":
...
-scan_target = {k: v for k, v in env.items() if k != "decision"}
+scan_target = {k: v for k, v in env.items()
+               if k not in ("decision", "compatibilityDecision")}   # 两字段均已做枚举校验
```

响应/留痕（建议增量，纯 additive）：
```python
# validate_envelope/_validate_asset 的返回或 submit 响应中增加（仅 asset）：
"manifestContract": {
  "generation": "1.0" if compat_new is None else "1.1",
  "compatibilityDecisionSource": source,          # compatibilityDecision | legacy_decision
  "readMode": read_mode
}
```
- **不把** `compatibilityDecision` 写进回执（回执 `decision` 仅治理裁定；三义分列边界）。
- 台账：phase 1 **不改表**（`manifestContract` 进 events note / 响应体）；phase 2 再评估 `requests` 增列（`ALTER TABLE ... ADD COLUMN`，向后兼容）。

### 2.3 版本判定与分批

| 代际 | 判据（建议） | WAME 行为 |
|---|---|---|
| legacy 1.0 | 有 `decision`、无 `compatibilityDecision` | dual：接受，source=`legacy_decision`；strict：阻断并提示升级 |
| v1.1 双写 | 两者都有且值相同 | 接受，source=`compatibilityDecision` |
| v1.1 新写 | 只有 `compatibilityDecision` | 接受（dual/strict）；**旧版 WAME 会因 `decision` 缺失而 A01 阻断** → 必须等本改动上线后再让写方停发 legacy 字段 |
| 冲突 | 两者都有但值不同 | 阻断（`XAP-1003`），不自动选边 |

### 2.4 回滚（WAME）

- 运行时开关：`XAP_COMPAT_DECISION_READ`（默认 `dual`）→ `legacy` 即完全回到旧行为（忽略 `compatibilityDecision`，仍要求 legacy `decision`）；`strict` 仅在新写方全部切换后使用。
- 代码回滚：`git restore server/xap-intake/intake_core.py tests/test_intake.py`；无数据库迁移（phase 1），无需数据回滚。
- 风险边界：双读只影响 **asset 包兼容性判断**；请求包/回执/发布/幂等路径不变。

### 2.5 建议新增测试（`tests/test_intake.py`）

1. legacy manifest（仅 `decision`）在 dual/strict/legacy 三模式下的受理结果；
2. 仅 `compatibilityDecision` 的新 manifest 在 dual/strict 受理、在 legacy 阻断；
3. 双字段值冲突 → `XAP-1003` 阻断（不落台账为已接收）；
4. `compatibilityDecision` 不触发 R06 留白误判；
5. `blocked` / `deprecated` 语义与现状一致（A05 不变）；
6. 响应体 `manifestContract.generation/source/readMode` 正确（additive 字段不破坏既有断言）。

### 2.6 需要同批评估的"注册链路"companion（建议，不属双读最小改动）

XiaoC 正式注册候选件使用 `requestType="service_package_registration"`、`contents` 为 AaaS ServicePackage、且 `contents.wame.decision` 是 AaaS 的**候选绑定标记**（`candidate_only_not_published`，非治理裁定）。若 WAME 要受理该类请求，需：
- `REQ_TYPES` 增加 `service_package_registration`；
- R06 扫描对 `contents.wame.decision` **仅在** `aaasCandidateMarker` 匹配 `{path:"contents.wame.decision", value:"candidate_only_not_published"}` 时跳过，否则照常判"自称裁定"；
- 注册表/注册号（`WAME-SP-*`，scheme A，仅 Registered 时分配）属正式注册实现，**主线没有**，需独立任务与授权（见 §5 A2 备注）。

## 3. AAAS / XiaoC ServicePackage digest 对齐（建议，未落仓）

### 3.1 现状（只读核对）

| 对象 | 文件 | 现状 |
|---|---|---|
| AaaS ServicePackage Schema | `GlobalCloud AAAS/schemas-json/aaas-service-package.schema.json` | 最小 schema：`required` 9 键；`wame`/`xwailBinding`/`metering`/`sla`/`evidenceRequirement` 仅 `type: object`；**无任何 digest 字段**；无 canonicalization 定义 |
| AaaS 校验器 | `scripts/validate_service_package.py`（+ `aaas_common.validate_common_package`） | 只做最低结构校验；无 digest 口径校验 |
| AaaS 样例 | `service-packages/examples/*/service-package.aaas.json`（2 包） | 基线：`validate_service_package.py` pass / 0 issues（F-033 复核记录） |
| XiaoC 正式注册候选 Schema | `docs/integration/artifacts/wame-service-package-registration.schema.candidate.json` | `Canonicalization` 已定义（sha256 + `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)` + target=`contents`）；`requestEnvelope.contentDigest` = AaaS 包体 canonical SHA-256；`registrationRecord.contentDigest` + `pocPublicationDigest`；`aaasCandidateMarker` 标注 |
| XiaoC 文档口径 | `wame-formal-registration-number-proposal.md` / `wame-service-package-registration-local-formal-closeout.md` | 明确 `contentDigest` 必须绑定 AaaS 包体（closeout 实测 `e0c276…`），PoC 信封 digest `0d858…` 不得复用；PoC `rcpt-*` 不能当登记号 |
| PVAOS 执行报告候选 | `docs/integration/artifacts/pvaos-execution-report.candidate.json` | `publication.contentDigest = 0d858501…`（实为 request-envelope digest） |

### 3.2 命名空间字段定义（建议，三作用域）

| 命名空间 | 建议字段名 | 计算对象 | 规范化规则 | 计算方 | 已知真实值（仅作样例，不重算） |
|---|---|---|---|---|---|
| `request-envelope` | `requestEnvelopeDigest` | 请求信封（**排除** digest/signature 字段本身） | canonical JSON（同 XiaoC 定义）→ sha256 | WAME（受理方，权威） | PoC `0d858501f43c7a8a4394d4929bc939ec764e14bb72e9635215f90607855cbfd6`（= WAME publication `content_digest`，即 sha256(envelope)） |
| `service-package` | `servicePackageDigest` | `contents`（AaaS ServicePackage 正文） | canonical JSON → sha256 | 提交方计算 + WAME 复核 | XiaoC closeout `e0c276c081ad8b69985dddb663046ff3a633fc823ad2a68e87294c2a323c5331` |
| `file-manifest` | `fileManifestDigest` | 逐文件 `sha256` 汇总（`totalSha256`） | `sha256(∑ "relpath:sha256\n")`（xap_sign/xap_verify 现行算法） | XWAIL 打包/签名方；验证方重算 | F-033 目录模式实测 `ab3f6b6d3edef92d44297a01…`（round-01 记录 `b47830a3…` 来自 `.xap` zip 模式——**两种 artifact 形态摘要不同，必须显式 artifactKind**） |

不变量（建议写入三仓口径）：
1. **正文不自含自身 digest**（AaaS ServicePackage 里不得出现 `contentDigest`/`servicePackageDigest`/`requestEnvelopeDigest`，避免固定点）；digest 由受理方或登记方在**信封/登记记录**中承载。
2. **禁止跨作用域复用**：`requestEnvelopeDigest` 不得当包体 digest、PoC 信封 digest 不得当 `servicePackageDigest`（XiaoC 提案已明确）。
3. **字段名带作用域**：新字段一律三个显式名；旧名 `contentDigest` 在未来一个版本内作为 **deprecated 别名**（语义 = `servicePackageDigest`），`totalSha256` 只作为 `fileManifestDigest` 的算法别名。
4. **argot 明确**：`file-manifest` 摘要必须同时声明 `artifactKind: "dir" | "zip"`（否则目录/打包件摘要不可比，见 §4.1 实测差异）。

### 3.3 AAAS schema 建议（additive，未落仓）

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://globalcloud.local/schemas/aaas-service-package.schema.json",
  "title": "GlobalCloud AaaS ServicePackage (digest-namespace aligned proposal)",
  "type": "object",
  "required": ["kind", "packageId", "version", "baselines", "wame", "xwailBinding", "metering", "sla", "evidenceRequirement"],
  "properties": {
    "...": "既有 9 键保持不变（此处省略重复声明）",
    "canonicalization": {
      "type": "object",
      "additionalProperties": false,
      "required": ["algorithm", "json", "encoding"],
      "description": "包体 canonical 规则（声明即承诺）；digest 由受理方按此计算，正文不得自含 digest。",
      "properties": {
        "algorithm": {"const": "sha256"},
        "json": {"const": "json.dumps(obj, sort_keys=True, separators=(\",\",\":\"), ensure_ascii=False)"},
        "encoding": {"const": "UTF-8"}
      }
    }
  },
  "not": {
    "anyOf": [
      {"required": ["contentDigest"]},
      {"required": ["servicePackageDigest"]},
      {"required": ["requestEnvelopeDigest"]},
      {"required": ["fileManifestDigest"]}
    ]
  },
  "additionalProperties": true
}
```

配套：`scripts/validate_service_package.py`（或 `aaas_common.validate_common_package`）增加 2 条检查——① 正文出现上述 digest 键 → 阻断（防固定点/跨域复用）；② 声明了 `canonicalization` 则三字段必须与固定规则一致（否则阻断）。现有 2 个样例包不含 digest 键 → 预期仍 pass（**需实测确认，作为 A3 验收条件**）。

### 3.4 XiaoC 候选件与文档对齐（建议，全部保持 candidate）

| 文件 | 建议改动 |
|---|---|
| `wame-service-package-registration.schema.candidate.json` | `requestEnvelope.contentDigest` → `servicePackageDigest`（旧名 deprecated 别名保留一个版本）；`RegistrationRecord` 增 `requestEnvelopeDigest`（必填）+ `servicePackageDigest`（必填，替代 `contentDigest`）；`pocPublicationDigest` 语义注释改为"PoC request-envelope digest 历史证据" |
| `wame-service-package-registration.request.candidate.json` | 信封字段改名；`requestedDecision`/`aaasCandidateMarker` 不变 |
| `.example.candidate.json` / `.bundle.candidate.json` | 同步改名；示例值用 `servicePackageDigest: e0c276…`、`requestEnvelopeDigest: <WAME 受理后回填>` |
| `pvaos-execution-report.candidate.json` | `publication.contentDigest` → `publication.requestEnvelopeDigest`（0d858… 属该命名空间） |
| `wame-formal-registration-number-proposal.md` | `contentDigest` 定义改为 `servicePackageDigest`（命名空间化），保留别名说明；PoC 值只作历史 |
| `wame-service-package-registration-local-formal-closeout.md` | 记录 digest 命名空间映射（0d858→request-envelope、e0c276→service-package），声明 transition 分支未并入主线 |
| `xiaoc-service-package.aaas.candidate.json` / `xiaoc-delivery-manifest.candidate.json` | 核对是否需要携带 digest（正文**不得**自含 service-package digest；交付清单若引用则为外部字段） |

约束：以上全部为 **candidate_not_effective** 文档/样例；不声明正式注册、正式授权、正式发布；`registrationNumberStatus` 保持 `example_only_not_allocated`。

## 4. 回归与回滚

### 4.1 只读基线（2026-10-22 真实执行，未改任何被盘点仓）

| 仓 / 命令 | 真实结果 |
|---|---|
| `GlobalCloud XWAIL`：`python3 scripts/check_object_schemas.py schemas-json` | `合计：PASS 26 / FAIL 0`，exit 0（当前**无** xap-manifest 正/负例） |
| `GlobalCloud XWAIL`：`python3 scripts/validate_xwail.py --all` | `status=pass`，checked 3 个模型，`issue_count=0` |
| `GlobalCloud XWAIL`：`python3 scripts/verify_xap.py --all` | `status=pass`，checked 1 个 manifest，`issue_count=0` |
| `GlobalCloud XWAIL`：`python3 scripts/xap_verify.py "<F-033 xap-package>"` | `包：xap.prompt-asset…@0.1.1`；`文件数：1`（注：`xap_verify` 的目录模式不把 `manifest.xap.json` 计入文件数，包内实际 2 个文件）；`total_sha256(重算)：ab3f6b6d3edef92d44297a01…`；`⚙️ 完整 + 无签名`，exit 0 |
| `GlobalCloud WAME/server/xap-intake`：`python3 -m unittest discover -s tests -q` | **`Ran 76 tests`，`FAILED (failures=2)`**：`test_B1a_real_term_and_igl`、`test_B1b_real_cwme_and_repair`。成因（已知、非本轮引入）：`tests/test_intake.py:REF_ROOTS` 指向改名前的 `/…/GlobalCoud GPCF`；目录已改名 `GlobalCloud GPCF`，证据引用不可访问 → `XAP-6004` 待补证。 |
| 仓状态（只读；核对时快照，可能随并行会话变动） | XWAIL HEAD `158f1c7`（dirty 1）；WAME HEAD `1d221db`（`wame/pm-governance`，dirty 1）；AAAS HEAD `de9770d`（dirty 16）；XiaoC HEAD `3d3efff7`（dirty 208）——均为开工前既有脏树，本轮未触碰。 |

### 4.2 落地后回归矩阵（验收门）

| # | 仓 | 命令 | 期望 |
|---|---|---|---|
| R1 | XWAIL | `python3 scripts/check_object_schemas.py schemas-json` | 自检全 PASS；正例 2 通过、负例 3 按预期拒绝；`合计 PASS 31 / FAIL 0`（26 + 5） |
| R2 | XWAIL | `python3 scripts/validate_xwail.py --all`；`python3 scripts/verify_xap.py --all` | 与基线一致（pass，issue 0；旧 manifest 仍通过） |
| R3 | XWAIL | 对 F-033 `xap-package` 跑 `python3 scripts/xap_verify.py` | 与基线一致（完整+无签名；目录模式摘要不变） |
| R4 | WAME | `cd server/xap-intake && python3 -m unittest discover -s tests -q` | 若先做 A2b（REF_ROOTS 路径修复）：**0 failures**；否则**基线一致**（同一 2 条已知失败，不新增失败），新增双读用例全 pass |
| R5 | WAME | 新增 §2.5 六类用例 | 全 pass；legacy 包行为与基线一致 |
| R6 | AAAS | `cd "GlobalCloud AAAS" && python3 scripts/validate_service_package.py`（+ 其余 4 个本地校验器） | 现有 2 包仍 pass；新增"正文含 digest 键"负例被拒 |
| R7 | XiaoC | 候选件 JSON 自检（`python3 -m json.tool`）+ 与 `wame-service-package-registration.schema.candidate.json` 本地校验（jsonschema） | 全部 JSON 合法；请求/登记/示例/bundle 与候选 schema 一致；仍为 candidate |
| R8 | GPCF | `python3 tools/kds-sync/validate_contract_matrix.py`（**A5 后置**，矩阵状态刷新后） | 校验 pass；CONFLICT-01/07 状态与落地事实一致（不提前写 closed） |

### 4.3 F-033 回放（拟用现有证据，不改任何仓）

证据目录：`GlobalCloud XiaoC/.harness/evidence/xiaoc-vision-r1-ecosystem-20261021/`。回放步骤（建议在**落地前**与**落地后**各跑一次，对比差异）：

```bash
# 1) 启动 WAME 受理器（本地 PoC；测试完停止）
cd "GlobalCloud WAME/server/xap-intake" && python3 intake_server.py --port 3210 &

# 2) 重放 F-033 信封（asset-like request；实测 requestId 将因 DB 状态不同而不同）
curl -s -X POST http://127.0.0.1:3210/intake/submit \
  -H 'Content-Type: application/json' \
  --data-binary @"…/xiaoc-vision-r1-ecosystem-20261021/02-envelope-only.json"

# 3) 台账/回执查询（未裁定时应仍为「待审核」/回执 404）
# 4) XWAIL 验包（目录模式；与 round-01 的 .xap 模式摘要不可直接比）
python3 "GlobalCloud XWAIL/scripts/xap_verify.py" \
  "…/xiaoc-vision-r1-ecosystem-20261021/xap-package"
```

期望：F-033 信封（`requestType=other`、`contents`=PromptAsset）**不受** manifest 双读改动影响（其 manifest 为 XWAIL 侧 `decision: compatible`，属 legacy 兼容路径）；XWAIL 打包/验包结果与基线一致（完整+无签名）。新增 `manifestContract` 字段对非 asset 请求不引入；若回放中 asset manifest 走 WAME 双读，legacy `decision` 仍应通过（dual 模式）。**F-033 回放不重跑 decide/publish**（PoC 裁定权在 WAME 治理角色，本轮不越权）。

### 4.4 回滚边界（分改动的可逆性）

| 改动 | 回滚方式 | 是否涉及数据 |
|---|---|---|
| XWAIL schema / python validator / testcases | `git restore -- schemas-json/xap-manifest.schema.json scripts/xwail_common.py schemas-json/testcases` | 否 |
| WAME intake 双读 + 测试 | `XAP_COMPAT_DECISION_READ=legacy` 重启（立即回旧行为）；或 `git restore -- server/xap-intake/intake_core.py tests/test_intake.py` | 否（phase 1 无 DB 迁移；台账 append-only） |
| AAAS schema + validator | `git restore` 两文件 | 否 |
| XiaoC 候选件 + 文档 | `git restore` 列明文件；候选件本就 `candidate_not_effective` | 否 |
| GPCF 矩阵/规格（A5 后置） | `git restore`；矩阵只读索引，不改契约本体 | 否 |

统一原则：**先双读、后切换写方、再收紧**；任何一步都可停在"dual 双读"状态运行（legacy 兼容窗口保留一个版本）。

## 5. 跨仓落仓授权请求清单（供老卢问答）

| # | 仓 | 文件 | 建议改动 | 风险 | 回滚 | 建议 |
|---|---|---|---|---|---|---|
| **A1** | `GlobalCloud XWAIL` | `schemas-json/xap-manifest.schema.json`；`scripts/xwail_common.py`；`schemas-json/testcases/positive/` + `negative/` 各 2/3 个新样例 | 按 §1.3/§1.4 落 schema 与 validator 双读、负例 | 中：XWAIL 是 manifest Schema 的正式维护方；改动为 additive，旧 manifest 仍通过；若 validator 改动与 schema 不同步会导致两套判据漂移 | restore 上述文件 | 建议先授权（无跨仓依赖） |
| **A2** | `GlobalCloud WAME` | `server/xap-intake/intake_core.py`；`tests/test_intake.py` | `_validate_asset` 双读 + R06 排除 + 响应 `manifestContract`；新增 §2.5 测试 | 中：改受理行为（仅 asset 兼容判断路径）；默认 dual，回旧行为有 env 开关 | `XAP_COMPAT_DECISION_READ=legacy` 重启 / restore 两文件 | 建议 A1 后授权 |
| **A2b（可选）** | `GlobalCloud WAME` | `server/xap-intake/tests/test_intake.py` 的 `REF_ROOTS` | `GlobalCoud GPCF` → `GlobalCloud GPCF`（目录改名后的测试基建修复） | 低：只改测试基建；不改产品代码 | restore 一行 | 建议与 A2 合并授权（否则 R4 只能以"基线 2 失败一致"验收） |
| **A3** | `GlobalCloud AAAS` | `schemas-json/aaas-service-package.schema.json`；`scripts/validate_service_package.py`（或 `aaas_common.py`） | §3.3 canonicalization + 禁正文自含 digest；validator 2 条新检查 | 中：AaaS 是 ServicePackage 语义 owner；additive 且现有样例预期不变 | restore 两文件 | 建议 A1/A2 后授权 |
| **A4** | `GlobalCloud XiaoC` | `docs/integration/artifacts/`（schema/request/example/bundle/pvaos-report 候选件）；`docs/integration/*.md`（提案、closeout） | §3.4 字段改名/新增与文档口径 | 低：全部 `candidate_not_effective`，无生产接口影响；但候选 schema 字段改名需与 WAME 受理实现同版本 | restore 列明文件 | 建议 A1–A3 后授权 |
| **A5（后置，不在本任务）** | `GlobalCloud GPCF` | `01-architecture/XAP回执与执行报告规格草案_v0.1.md`；错误码注册表（CONFLICT-02 新建）；`runtime/contract-matrix.yaml` 冲突状态 | 写入 digest 命名空间/三义分列条款与错误码；矩阵状态从 `closed`（裁决）→ `landed_pending_verification`（落地后） | 低–中：文档口径与治理状态刷新，需 GPCF 会话执行 | restore | 建议 A1–A4 验收后再授权 |

**需要老卢确认的问答项（建议以选择题呈现）**：
1. 是否按 **A1 → A2(+A2b) → A3 → A4 → A5** 顺序落仓，还是先只落 A1+A2（schema+双读）观察一轮？
2. A2b（`REF_ROOTS` 路径修复）是否与 A2 合并授权（推荐合并，否则 WAME 回归只能"基线 2 失败一致"）？
3. 双读窗口长度：保留 legacy `decision` 一个契约版本（推荐）还是两个版本？
4. 是否允许本轮把 XiaoC candidate 件字段改名（保持 `candidate_not_effective`，不触生产）？
5. 正式 WAME 注册表/注册号实现（`WAME-SP-*` scheme A）是否单独立项（本计划不包含其实现，仅登记依赖）？

## 6. 建议执行顺序与验收门

```text
Phase 0（本任务）：本计划（只读核对 + 建议 diff） —— 已完成文件，未落仓
Phase 1：A1 XWAIL schema+validator+testcases → R1/R2/R3 绿
Phase 2：A2 WAME 双读（默认 dual）+ 测试（+A2b） → R4/R5 绿；进入"双写窗口"
Phase 3：写方切换（XiaoC/AaaS 输出 compatibilityDecision；下发"可停发 legacy decision"通知）→ F-033 回放 R3 绿
Phase 4：A3 AAAS + A4 XiaoC 候选件对齐 → R6/R7 绿
Phase 5：A5 GPCF 规格/错误码/矩阵刷新 → R8 绿；再评估是否收紧 strict / 进入 2.0 移除阶段
```

## 7. 非声明

- 本文件是**实施准备建议稿**：不声明任何仓已修改、任何 diff 已落仓、任何契约已统一/冻结/签署/集成。
- 所有"现状"均为 2026-10-22 只读核对结果；`§4.1` 的 WAME 2 条失败为**开工前既有**，不归因于本计划、也不因此声明 WAME 受理链可用或不可用。
- 不声明任何项目状态提升（`accepted` / `integrated` / `production_ready` / `customer_accepted` / `real_business_verified`）。
- 不新增未注册错误码；冲突码位统一待 CONFLICT-02 错误码注册表裁决。
- 未 commit / push；本文件为 GPCF 仓唯一写入。
