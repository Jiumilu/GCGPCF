---
doc_id: GPCF-DOC-CROSS-PROJECT-CONTRACT-MATRIX-20261022
title: 项目群跨项目契约矩阵 v1.0（PG-12 inventory）
project: GPCF
related_projects: [XWAIL, WAME, AAAS, KDS, Brain, XiaoC, GPCF]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-cross-project-contract-matrix-v1.0.md
source_path: 09-status/globalcloud-cross-project-contract-matrix-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群跨项目契约矩阵 v1.0（PG-12 inventory 版）

> **性质**：任务执行报告（PG-12 跨项目契约收敛·inventory 版）。本文件按任务交付路径写入 `09-status/`，但**尚未登记受控文档头**（无 `doc_id` / `kds_path` / `sync_direction`），待 GPCF 文档控制流程登记后方可视为受控文档。
> **任务**：PG-12 跨项目契约收敛（inventory）｜**执行日期**：2026-10-22｜**矩阵文件**：`runtime/contract-matrix.yaml`｜**校验器**：`tools/kds-sync/validate_contract_matrix.py`
> **写入范围**：仅 `runtime/contract-matrix.yaml`、`tools/kds-sync/validate_contract_matrix.py`、本报告。未改任何被盘点契约文件，未 `stage` / `commit` / `push`。
> **非声明**：本矩阵是**只读索引**（`source_of_truth: false`），不是契约本体。**不声明契约已统一、已冻结、已签署、已集成完成**；不提升任何项目状态；不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted` / `real_business_verified`。

---

## 1. 盘点结论

1. **三套跨项目契约都已存在，但成熟度差一档，且互不引用**：
   - **XAP 治理交换契约**：字段级规格 + Manifest JSON Schema + 已跑通的受理实现 + 签名工具，但规格仍是草案（`v0.1`），回执/执行报告没有正式 Schema 文件。
   - **跨项目事件合同**：已冻结到受控状态（`frontmatter v1.0`，正文记「一期事件合同 v2」），一期 12 类事件族齐全，但**只有 Markdown**，没有机器可读 Schema。
   - **知识资产 canonical 契约**：唯一有「manifest + JSON Schema + 词表 + 示例 + 确定性 validator + freeze 记录」完整闭环的一套，但 `v0.1` 下已发生两次哈希修订，freeze 状态是 `controlled_candidate_pending_independent_review`、`release_unblocked: false`。
2. **冲突不是设计分歧，而是"同一概念多处定义、无单一注册表"**：摘要（contentDigest/totalSha256/包体摘要/信封摘要）4 种口径、错误码 3 处清单不一致、`decision` 字段两套枚举、版本号 4 处与实际内容不符、签名边界工具已就绪但门禁未定。
3. **8 条冲突中 5 条 high**，其中 `CONFLICT-01`（contentDigest 口径）与 `CONFLICT-07`（`decision` 同名双枚举）**会直接导致越权解读或幂等失效**，应优先裁决；`CONFLICT-02`（错误码）与 `CONFLICT-05`（签名）是"实现已先行、契约未追认"的典型。
4. **本矩阵可直接作为收敛排序依据**：每条冲突都绑定了 `severity`、被影响的契约、真实证据路径与建议动作，未使用任何推断值（`inferred: false`，全部版本/状态均可回指文件）。

---

## 2. 盘点表（三套契约）

| # | contract_id | 契约 | 集合 | owner | version | status | schema_paths | consumers | 关联冲突 |
|---:|---|---|---|---|---|---|---:|---:|---|
| 1 | `CONTRACT-XAP-GOVERNANCE-EXCHANGE` | XAP 治理交换契约（请求包 / 回执 / 执行报告 / 幂等 / 错误码） | `xap` | GPCF（提交侧规格）；正式 Schema 归 XWAIL | **v0.1** | **draft** | 4 | 7 | 01/02/04/05/07 |
| 2 | `CONTRACT-EVENT-ENVELOPE` | 跨项目事件合同（事件信封 + 一期事件族 + 幂等/补偿） | `event` | KDS（文档 owner）；生产者 GFIS/GPC/WAME/PVAOS | **v1.0**（正文另记 v2） | **controlled** | 1 | 9 | 03/04/06/08 |
| 3 | `CONTRACT-KNOWLEDGE-ASSET-CANONICAL` | 知识资产 canonical 契约（KnowledgeObject + KnowledgeAssetEnvelope） | `knowledge` | GPCF（canonical 契约源）；KDS 持知识事实主存 | **v0.1** | **controlled**（freeze 待独立评审） | 5 | 8 | 03/04/07 |

**版本与状态依据（均来自真实文件，未使用 `unknown`）**

| 契约 | 依据文件 | 关键行 |
|---|---|---|
| XAP | `01-architecture/XAP回执与执行报告规格草案_v0.1.md` | 文件名/标题「草案 v0.1」；frontmatter `version: v1.0` / `status: controlled`；正文"提交侧规格草案" |
| 事件 | `03-data-ai-knowledge/GlobalCloud绿色供应链体系事件合同.md` | frontmatter `version: v1.0` / `status: controlled`；正文「版本：一期事件合同 v2（口径修正稿）」 |
| canonical | `okf/knowledge-asset-contract-manifest.yaml` | `contract_version: v0.1` / `status: controlled`；freeze 文件记 `controlled_candidate_pending_independent_review`、`release_unblocked: false` |

**schema_paths / evidence 全部经校验器逐条核对存在**（见 §5）。canonical 契约是唯一具备 5 份机器可读产物的契约：`okf/knowledge-asset-contract-manifest.yaml`、`okf/knowledge-asset-envelope.schema.json`、`okf/knowledge-object.schema.json`、`okf/knowledge-asset-vocabulary.yaml`、`okf/knowledge-asset-envelope.example.json`。

---

## 3. 冲突清单与建议（8 条）

| # | conflict_id | 主题 | 严重度 | 受影响契约 | 冲突要点 | 建议动作 |
|---:|---|---|---|---|---|---|
| 1 | `CONFLICT-01` | contentDigest 口径 | **high** | XAP、canonical | 同一摘要四种定义：①回执规格 `packageRef.contentDigest`（请求包摘要，进幂等键）；②WAME 实现 `sha256(contents)` 实算比对（不符即 XAP-2004）；③XWAIL `xap_sign` 的 `totalSha256`（逐文件 sha256 汇总，payload=`xap-sign-v1\|packageId\|version\|totalSha256`）；④XiaoC 正式提案要求绑定 **AaaS ServicePackage 包体** canonical SHA-256 且禁用 PoC 信封 digest | XWAIL 侧定义 digest 命名空间（request-envelope / service-package / file-manifest），字段名带作用域；裁决前禁止跨作用域复用 |
| 2 | `CONFLICT-02` | WAME 错误码 | **high** | XAP | 无单一权威注册表：GPCF 清单登记 XAP-1001/1002/1003/2001/2002/2003/2004/5001；回执规格定义 6xxx 全段；WAME 实现实际抛出 2004/4001/5001/5002/5003/6001-6004/6006。**XAP-4001/5002/5003 未见于 GPCF 清单，XAP-6005 实现未用** | 建 XAP 错误码注册表（码/语义/引入版本/提出方/是否可重试），未注册码不得进实现 |
| 3 | `CONFLICT-03` | 字段命名与 casing | medium | XAP、event、knowledge | camelCase（`packageRef`/`contentDigest`/`eventId`）与 snake_case（`contract_id`/`canonical_manifest_sha256`/`content_digest`/`receipt_id`）混用，无 casing 规则与转换责任方 | 定义「线上 camelCase、存储 snake_case、转换点唯一」，写入消费者接入清单 |
| 4 | `CONFLICT-04` | 版本语义 | **high** | XAP、event、knowledge | 四版本号与实际内容不符：XAP 标题 v0.1 / frontmatter v1.0；XWAIL 清单 frontmatter controlled v1.0 / 正文 draft；事件合同 frontmatter v1.0 / 正文 v2；canonical `v0.1` 下两次哈希修订（76ac→17c9） | 统一「契约版本 semver + 内容哈希」双标识；内容变即哈希变，破坏性变更才升主版本 |
| 5 | `CONFLICT-05` | XAP 签名/无签名边界 | **high** | XAP | `signature` 在规格中可选且 P2 预留；`xap-manifest.schema.json` 无 signature/digest 定义（靠 `additionalProperties: true` 放行）；XWAIL 已有 Ed25519 签名/验签脚本；F-033 验收写「包完整性通过（无签名）」 | Manifest Schema 显式定义 signature/digest；台账记 `signature_status`；正式受理要求签名，PoC 标 `no_signature` 且不作治理证据 |
| 6 | `CONFLICT-06` | 幂等键构成 | medium | XAP、event | 事件级 `idempotencyKey`（16 必填字段之一，重复只标 duplicate）与包级 `packageId+version+contentDigest` 粒度不同，信封未说明两者对应 | 定义「业务动作 → 事件 → XAP 包」三段幂等映射，或在信封加 packageRef 关联 |
| 7 | `CONFLICT-07` | `decision` 字段同名双枚举 | **high** | XAP | manifest `decision`=兼容性判断（compatible/migration_required/deprecated/blocked），回执 `decision`=治理裁定（rejected/returned_for_evidence/accepted/granted/revoked）；规格已承认歧义但迁移未做，Schema 仍叫 `decision` | 按规格三义分列落地：`manifest.compatibilityDecision` / `回执.decision` / 请求包 `requestedDecision`，配负例 |
| 8 | `CONFLICT-08` | WAES→WAME 命名漂移 | medium | event | 事件合同仍用 `waes.` 域名与 `CON-GFIS-WAES-001`；canonical freeze 已记「WAES 缩写停用、体系命名统一为 WAME」并因此触发哈希修订 | 事件合同补命名对照（waes. 为历史别名），连接器编号标 superseded，订阅方按新名迁移 |

**收敛顺序建议**

- **P0（先裁，阻塞其他收敛）**：`CONFLICT-01` contentDigest 口径 → `CONFLICT-07` decision 双枚举。这两条不裁，任何"对齐 contentDigest"或"回执联调"的工作都会反复返工。
- **P1**：`CONFLICT-02` 错误码注册表、`CONFLICT-05` 签名边界。两者都需要 XWAIL 侧出正式 Schema 版本，属同一交付包。
- **P2**：`CONFLICT-04` 版本语义（需要三套契约同时改法）、`CONFLICT-03` casing、`CONFLICT-06` 幂等映射、`CONFLICT-08` 命名漂移。

---

## 4. 矩阵字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` / `matrix_id` / `generated_at` | int / str / str | 矩阵自身标识与生成时间 |
| `owner` / `scope` | str | `GPCF`；inventory 只读范围声明 |
| `source_of_truth` | bool | **固定 `false`**：矩阵是索引，不是契约本体（校验器强制拒绝 `true`） |
| `update_rule` | str | 契约文件变更后必须重跑校验器并更新 version/status/evidence；找不到依据写 `unknown` 且 `inferred: true` |
| `contract_sets` | list | 三个集合 `xap` / `event` / `knowledge`（校验器要求每个集合至少一条契约） |
| `contracts[].contract_id` | str | 唯一契约标识（校验器查重） |
| `contracts[].contract_set` | str | 归属集合 |
| `contracts[].name` / `owner` | str | 契约名与责任方 |
| `contracts[].version` / `version_basis` | str | 版本号 **+ 出处**（含冲突提示，避免"只写 v0.1 看不出处"） |
| `contracts[].status` / `status_basis` | str | 状态 + 判据（文档受控 ≠ 契约冻结） |
| `contracts[].schema_paths` | list | Schema/规格文件路径，逐条校验存在 |
| `contracts[].evidence` | list | 证据文件（预检记录、feature、实现、freeze 记录），逐条校验存在 |
| `contracts[].consumers` | list | 消费方项目名（校验格式与去重） |
| `contracts[].compat_rule` | str | 兼容规则（来自真实文档，不自行发明） |
| `contracts[].conflicts` | list | 引用的冲突 id（必须有定义） |
| `contracts[].open_questions` | list | 待裁决项 |
| `contracts[].inferred` | bool | 是否存在推断值；`version`/`status` 写 `unknown` 时必须为 `true` |
| `conflicts[].*` | — | `conflict_id / topic / severity(high\|medium\|low) / contracts / description / evidence / impact / recommendation / status(open\|mitigated\|closed) / inferred` |

---

## 5. 验证命令与真实输出

### 5.1 校验器（只读，不写任何文件）

```bash
cd "GlobalCoud GPCF"
python3 tools/kds-sync/validate_contract_matrix.py
```

### 5.2 真实输出：通过

```text
PASS validate_contract_matrix
  matrix        : /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/runtime/contract-matrix.yaml
  matrix_id     : globalcloud.cross_project_contract_matrix（source_of_truth=False）
  contract_sets : xap, event, knowledge
  contracts     : 3 条
    - CONTRACT-XAP-GOVERNANCE-EXCHANGE: set=xap version=v0.1 status=draft schema_paths=4 consumers=7
    - CONTRACT-EVENT-ENVELOPE: set=event version=v1.0 status=controlled schema_paths=1 consumers=9
    - CONTRACT-KNOWLEDGE-ASSET-CANONICAL: set=knowledge version=v0.1 status=controlled schema_paths=5 consumers=8
  conflicts     : 8 条（high=5 medium=3 low=0）
  checks        : schema=pass contract_sets=pass unique_id=pass schema_paths=pass evidence_paths=pass version=pass consumers=pass conflict_links=pass themes=pass sensitive=pass
[exit code: 0]
```

### 5.3 真实输出：四个负例（故意破坏，均 exit 1）

```text
===== 负例：dup-id =====
FAIL contract_id 重复：CONTRACT-XAP-GOVERNANCE-EXCHANGE（contracts[0] 与 [1]）
FAIL validate_contract_matrix: 1 项校验失败（matrix=/tmp/pg12-neg/dup-id.yaml）
[exit code: 1]

===== 负例：bad-path =====
FAIL contracts[2](CONTRACT-KNOWLEDGE-ASSET-CANONICAL) 的 schema_paths 路径不存在：okf/not-exist-object.schema.json（尝试：['okf/not-exist-object.schema.json', '../okf/not-exist-object.schema.json']）
FAIL validate_contract_matrix: 1 项校验失败（matrix=/tmp/pg12-neg/bad-path.yaml）
[exit code: 1]

===== 负例：sensitive-key =====
FAIL 敏感字段名：/contracts[0]/api_key#key -> api_key（不允许登记凭据类字段）
FAIL 疑似密钥值：/contracts[0]/api_key 命中 \bsk-[A-Za-z0-9_-]{16,}
FAIL validate_contract_matrix: 2 项校验失败（matrix=/tmp/pg12-neg/sensitive-key.yaml）
[exit code: 1]

===== 负例：missing-theme =====
FAIL 必检冲突主题未覆盖：XAP 签名/无签名边界（无任何冲突条目命中 /签名|signature/）
FAIL validate_contract_matrix: 1 项校验失败（matrix=/tmp/pg12-neg/missing-theme.yaml）
[exit code: 1]
```

> 负例均为 `/tmp/pg12-neg/` 下的一次性副本，不改仓库文件。四个负例分别覆盖：id 唯一性、`schema_paths` 存在性、敏感内容、必检冲突主题覆盖——与"失败必须 exit 1"的要求一致。

### 5.4 校验项清单

| 校验项 | 说明 |
|---|---|
| schema | 顶层 9 个必填字段、`source_of_truth` 必须为 `false` |
| contract_sets | 必须覆盖 xap / event / knowledge，且每集合 ≥1 条契约 |
| unique_id | `contract_id`、`conflict_id` 唯一（大小写敏感） |
| schema_paths / evidence_paths | 每条路径必须解析到真实文件（绝对 → GPCF 根 → 工作区根） |
| version | 非空；写 `unknown` 必须同时 `inferred: true` |
| consumers | 非空项目名列表、无重复 |
| conflict_links | 契约引用的冲突 id 必须已在 `conflicts` 定义 |
| themes | 必检 5 个冲突主题：contentDigest / 错误码 / 字段命名 / 版本 / 签名 |
| sensitive | 凭据类键名与密钥形态值扫描 |

---

## 6. 待办与回滚

### 6.1 待办（本次未做）

1. **不裁决冲突**：本矩阵只登记冲突，不选边、不改任何被盘点契约；`CONFLICT-01/07` 的裁决需 XWAIL + XiaoC + WAME + GPCF 共同确认。
2. **事件合同无机器可读 Schema**：本次只登记现状，未新建事件 JSON Schema（属契约变更，需 owner 授权）。
3. **回执/执行报告正式 Schema 缺失**：只找到 manifest Schema；回执 Schema 是否存在需 XWAIL 侧确认（已列 open_question）。
4. **本报告未登记受控文档头**：`09-status/` 新增 Markdown 需由 `document_control.py` 生成 `doc_id` / `kds_path`，本次未跑（会重写全量台账，超出写入范围）。
5. **未纳入门禁链**：建议把 `validate_contract_matrix.py` 加入 LOOP 文档门禁或 GPCF 2.0 Evidence Gate。

### 6.2 非声明

- 不声明三套契约已统一、已冻结、已签署或已完成集成（矩阵 `source_of_truth: false`，且三套契约的 `status` 仍分别为 draft / controlled / controlled-待评审，均未达"正式冻结+消费者签认"）。
- 不声明冲突已解决：8 条全部 `status: open`。
- 不声明矩阵覆盖项目群全部契约（本版仅 3 套：XAP / 事件 / 知识资产 canonical；连接器合同、DRC 目录契约、WAE 令牌与入口契约未纳入）。
- 不声明任何项目状态提升。

### 6.3 回滚

- **撤什么**：删除 `runtime/contract-matrix.yaml` 与 `tools/kds-sync/validate_contract_matrix.py`，删除本报告。
- **保持什么**：不改写任何被盘点契约文件，因此无需回滚他人文件；失败时状态保持 `repair_required`。
- **不自动做什么**：不自动 `stage` / `commit` / `push` / `delete` / `deploy`；不自动运行 `document_control.py` 或任何会重写台账的命令。

## 6. 裁决记录（2026-10-22）

| conflict_id | 裁决 | 裁决人 | 说明 |
|---|---|---|---|
| `CONFLICT-01` | **A：digest 命名空间化** | 老卢 | request-envelope / service-package / file-manifest；字段名带作用域 |
| `CONFLICT-07` | **A：三义分列** | 老卢 | manifest.compatibilityDecision / 回执.decision / 请求包.requestedDecision |

其余 6 条仍为 open，按 §3 收敛顺序处理。裁决不改变契约文件本身；实施需 XWAIL/WAME/AaaS 属主各自落地并补负例。

---

## 7. 落仓状态（2026-10-22 · PG-12 A1+A2+A2b 实施）

> 本节为 **append-only 追加**：上文 §1–§6 为 inventory / 裁决时快照（其中 §6.2「8 条全部 status: open」是当时事实），**不改写**；本节记录裁决 A 的部分落仓结果。
> 机器状态以 `runtime/contract-matrix.yaml` 为准：`CONFLICT-01` / `CONFLICT-07` 的 `status` 已由 `closed`（仅裁决）→ `mitigated`（A1+A2 落仓）→ **`closed`**（A3+A4+A5 落仓并本地验证，见 §8）；其余 6 条仍 `open`。

### 7.1 已落仓改动（工作区改动，**未 commit / push**）

| 仓 | 文件 | 摘要 |
|---|---|---|
| `GlobalCloud XWAIL` | `schemas-json/xap-manifest.schema.json` | 契约 v1.1：`compatibilityDecision` 正式字段 + legacy `decision`（deprecated，`anyOf` 兼容）；三命名空间 digest 字段 `requestEnvelopeDigest` / `servicePackageDigest` / `fileManifestDigest`；可选 `signature`（if/then 要求 `digest`） |
| `GlobalCloud XWAIL` | `scripts/xwail_common.py` | `validate_xap_manifest()` 双读与冲突判定（`XAP-1003`）；digest/signature 字段校验（冲突用既有 `XAP-2004`，未新增错误码） |
| `GlobalCloud XWAIL` | `schemas-json/testcases/{positive,negative}/xap-manifest.schema.json__*.json` | 新增 2 正例 + 3 负例（治理枚举误用 / 双字段都缺 / 签名缺 digest） |
| `GlobalCloud WAME` | `server/xap-intake/intake_core.py` | manifest 兼容性双读（new 优先 / legacy 兼容 / strict 收紧 / `XAP_COMPAT_DECISION_READ` 回滚）；R06 同时排除两字段；响应 additive `manifestContract`；回执 `decision` 口径不变 |
| `GlobalCloud WAME` | `server/xap-intake/intake_server.py` | `ref_roots.GPCF` 路径修复：`GlobalCoud GPCF` → `GlobalCloud GPCF`（A2b） |
| `GlobalCloud WAME` | `server/xap-intake/tests/test_intake.py` | `REF_ROOTS.GPCF` 路径修复（原 2 条既有失败根因）+ 新增 `Pg12DualReadTests` 8 例 |

### 7.2 验证（2026-10-22 真实执行，本地可回放）

| 命令 | 结果 |
|---|---|
| `python3 scripts/check_object_schemas.py schemas-json`（XWAIL） | **PASS 31 / FAIL 0**（基线 26 + 新增 5；3 负例按预期拒绝） |
| `python3 scripts/validate_xwail.py --all`（XWAIL） | pass，3 模型，issue 0 |
| `python3 scripts/verify_xap.py --all`（XWAIL） | pass，1 manifest，issue 0（legacy `decision` 包仍通过） |
| F-033 legacy manifest（`GlobalCloud XiaoC/.harness/evidence/xiaoc-vision-r1-ecosystem-20261021/xap-package/manifest.xap.json`） | 旧/新 schema 均 PASS；`xap_verify` 完整性 pass（完整+无签名） |
| `python3 -m unittest discover -s tests -q`（WAME `server/xap-intake`） | **Ran 84 tests ... OK**（基线 76 + 新增 8；0 失败） |
| `python3 tools/kds-sync/validate_contract_matrix.py`（GPCF） | **PASS**（8 条冲突，2 mitigated / 6 open；evidence_paths=pass） |

证据与完整命令输出：`docs/harness/evidence/pg12-implementation-report-20261022.md`；实施建议稿：`docs/harness/evidence/pg12-implementation-plan-20261022.md`。

### 7.3 回滚

| 改动 | 回滚 |
|---|---|
| XWAIL schema / validator / fixtures | `git -C "GlobalCloud XWAIL" restore -- schemas-json/xap-manifest.schema.json scripts/xwail_common.py`；删除新增 5 个 fixture |
| WAME 双读 + A2b | 运行时：`XAP_COMPAT_DECISION_READ=legacy` 重启（回旧行为）；代码：`git -C "GlobalCloud WAME" restore -- server/xap-intake/intake_core.py server/xap-intake/intake_server.py server/xap-intake/tests/test_intake.py` |
| 矩阵 | 将两条 `status` 改回 `closed`（或 `git restore`），并回退 `generated_at` |
| 数据 | 无 DB 迁移；台账 append-only；无数据回滚需求 |

### 7.4 未落 / 残留（不属本批次）

1. **A3 AAAS**（`aaas-service-package.schema.json` canonicalization / 禁自含 digest、validator 新检查）未落。
2. **A4 XiaoC**（候选件 `contentDigest→servicePackageDigest`、登记记录 `requestEnvelopeDigest`、文档口径）未落，候选件仍 `candidate_not_effective`。
3. **A5 GPCF**（XAP 回执规格条款、错误码注册表 CONFLICT-02、矩阵最终状态）未落。
4. `requestedDecision` 枚举约束未收紧；WAME `REQ_TYPES` 未加 `service_package_registration`；AaaS candidate marker 的 R06 跳过规则未实现。
5. 因此 `CONFLICT-01` 的跨仓覆盖仍为**部分**（service-package 命名空间仅在 XWAIL manifest + WAME 双读侧落地），故状态是 `mitigated` 而非 `closed`。

### 7.5 非声明

- 本次落仓为**工作区改动，未 commit / push**；不声明任何仓已发布或集成完成。
- `mitigated` ≠ `closed`：不等于跨仓全部对齐，也不等于契约冻结/签署。
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`；不声明 WAME 受理链生产可用。

---

## 8. CONFLICT-01/07 关闭记录（2026-10-22 追加 · A3+A4+A5）

> 承接 §7（A1+A2 后为 `mitigated`）。A3/A4 落仓并验证通过后，`runtime/contract-matrix.yaml` 中 `CONFLICT-01` / `CONFLICT-07` 已由 `mitigated` 改为 **`closed`**；本节记录关闭依据（`validate_contract_matrix.py` 校验：2 closed / 6 open）。

### 8.1 A3 `GlobalCloud AAAS` 已落仓（工作区，未 commit/push）

| 文件 | 改动 |
|---|---|
| `schemas-json/aaas-service-package.schema.json` | 新增可选 `canonicalization`（`algorithm=sha256` / 固定 JSON 规范化 / `encoding=UTF-8`，与 XiaoC 口径逐字一致）；新增 `not.anyOf`：正文**不得**自含 `contentDigest` / `servicePackageDigest` / `requestEnvelopeDigest` / `fileManifestDigest` |
| `scripts/validate_service_package.py` | 新增 2 项检查：正文自含 digest → `AAAS-1202`；`canonicalization` 与固定规则不一致 → `AAAS-1203`（AAAS 本地校验器码位，非 XAP 错误码空间） |
| `tests/test_pg12_service_package_digest.py` | 新增 6 例：现有样例回归 / 正文自含 digest 拒绝（含旧名 contentDigest）/ 合法 canonicalization 通过 / 错误规则拒绝 / schema 层自含 digest 拒绝 |

### 8.2 A4 `GlobalCloud XiaoC` 已落仓（全部保持 `candidate_not_effective`）

| 文件 | 改动 |
|---|---|
| `docs/integration/artifacts/wame-service-package-registration.schema.candidate.json` | `RequestXapEnvelope`：`contentDigest` → `servicePackageDigest`（旧名 deprecated 别名 + `anyOf` 过渡窗口）；`RegistrationRecord`：`contentDigest` → `servicePackageDigest`、新增必填 `requestEnvelopeDigest`；`pocPublicationDigest` 注释改为「PoC request-envelope digest 历史证据，不得复用为 servicePackageDigest」 |
| `...request.candidate.json` / `...example.candidate.json` / `...bundle.candidate.json` | 字段改名；登记记录的 `requestEnvelopeDigest` 由候选信封本地复算（不含 digest 字段的 canonical JSON） |
| `...pvaos-execution-report.candidate.json` | `publication.contentDigest` → `publication.requestEnvelopeDigest`（0d858… 属 request-envelope 命名空间），附 `digestNamespace`/`digestNote` |
| `wame-formal-registration-number-proposal.md`、`wame-service-package-registration-plan.md`、`wame-service-package-registration-local-formal-closeout.md`、`wame-post-poc-reconciliation.md`、`wame-formal-authority-mmc-design.md` | 追加「PG-12 digest 命名空间口径」对照表 + 关键字段名/表述同步（proposal/plan/closeout 的 `contentDigest` 已改 `servicePackageDigest` 或旧名标注） |

### 8.3 验证（2026-10-22 真实执行）

| 命令 | 结果 |
|---|---|
| AAAS 5 个本地校验器（`validate_service_package` / `validate_aaas_binding` / `validate_metering` / `validate_sla` / `verify_evidence_requirements`，`--all`） | 全部 exit 0（现有 2 个样例 pass） |
| AAAS `python3 -m unittest tests.test_pg12_service_package_digest -v` | **Ran 6 tests ... OK**（正文自含 digest → AAAS-1202 拒绝；错误 canonicalization → AAAS-1203 拒绝） |
| AAAS `python3 -m unittest discover -s tests -q` | **Ran 10 tests ... OK**（含既有 `test_local_gates`） |
| XiaoC 候选件 | 4 个候选 JSON 全部可解析；example/bundle 对根 schema PASS；request/example/bundle 的 envelope 对 `RequestXapEnvelope` PASS；legacy `contentDigest`-only 仍 PASS（兼容窗口）；无 digest 字段 → 拒绝（预期）；`documentStatus=candidate_not_effective` 未变 |
| WAME 回归 | `python3 -m unittest discover -s tests -q` → **Ran 84 tests ... OK** |
| GPCF 矩阵 | `python3 tools/kds-sync/validate_contract_matrix.py` → **PASS**（8 条冲突：2 closed / 6 open） |

证伪/负例细节与完整输出见 `docs/harness/evidence/pg12-implementation-report-20261022.md` §10。

### 8.4 关闭后仍存在的边界（不构成 reopen 条件，但须如实登记）

1. AAAS/XiaoC 全部为 **candidate / 本地校验**：正式 WAME 注册、授权、发布仍需 WAME owner / registry / MMC 确认；`registrations` 表与端点仍未并入 WAME 主线。
2. XiaoC 仍有其它在途会话修改的文档（`README.md`、`wame-xwail-registration-package.md` 等）未逐处改名，靠本批追加的命名空间口径表读取；通用 `wame-request-envelope.candidate.v2.json`（非 ServicePackage 请求）仍用 `contentDigest`，命名空间决策另议。
3. `requestedDecision` 枚举约束未收紧；WAME `REQ_TYPES` 未加 `service_package_registration`；AaaS candidate marker 的 R06 跳过规则未实现。
4. `CONFLICT-02`（XAP 错误码注册表）仍 `open`；本批未新增任何未注册 XAP 错误码（XWAIL/WAME 复用既有码，AAAS 使用 AAAS 本地码位）。

### 8.5 非声明

- 本次 A3/A4/A5 为**工作区改动，未 commit / push**。
- `closed` 表示 A1–A4 已落仓并本地验证、A5 矩阵刷新完成；**不表示**跨仓生产集成、契约冻结/签署或任何项目状态提升。
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
