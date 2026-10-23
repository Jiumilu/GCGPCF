---
doc_id: GPCF-DOC-GKE001-CHAIN-MATRIX-20261022
title: GKE-001 知识工程链路矩阵 v1.0（PG-13 inventory）
project: GPCF
related_projects: [GPCF, KDS, Studio, Brain, MMC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-gke001-chain-matrix-v1.0.md
source_path: 09-status/globalcloud-gke001-chain-matrix-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud GKE-001 知识工程链路矩阵 v1.0（PG-13 inventory）

> **性质**：任务执行报告（PG-13 GKE-001 知识工程链路 inventory）。本文件按任务交付路径写入 `09-status/`，但**尚未登记受控文档头**（无 `doc_id` / `kds_path` / `sync_direction`），待 GPCF 文档控制流程登记后方可视为受控文档。
> **任务**：PG-13 GKE-001 知识工程链路最小闭环（inventory 版）｜**执行日期**：2026-10-22｜**矩阵**：`runtime/gke001-chain-matrix.yaml`｜**校验器**：`tools/kds-sync/validate_gke001_chain_matrix.py`
> **写入范围**：仅上述矩阵、校验器、本报告。**未改 KDS / Studio / Brain / MMC 任一仓**，未 `stage` / `commit` / `push`。
> **非声明**：本矩阵是链路索引（`source_of_truth: false`、`chain_closed: false`），**不声明链路闭环、不声明授权已生效、不声明任何项目状态提升**。规范 §14 当前口径保持 `cross_project_status = partial`、`completion_status = not_complete`、`status_promotion_authorized = false`。

---

## 1. 结论摘要

1. **链路已经"各仓都动过"，但没有一环走到闭环**：6 个环节中 4 个达 S2（本地实现+可回放证据）、1 个停在 S1（MMC 授权只有申请包）、1 个 `pending`（人工确认）。
2. **断点不在技术实现，而在"授权—确认"两环**：MMC 授权只有 `human_authorization_request_only` 申请包，未产生 `granted` 回执；人工确认环节无任何回执落证据。控制台账保持 `authorization_granted=0`、`action_executed=0`。
3. **状态上限由规范固定，不由本矩阵给**：`real_kds_write_authorized=false`、`long_term_memory_write_authorized=false`、`business_state_change_authorized=false`、`status_promotion_authorized=false`。因此即便技术环节全 S3，链路也不能自称闭环。
4. **状态全部有据**（`inferred: false`）：每个环节的 `status_basis` 指向具体 run 文件或 freeze 记录，未使用 `unknown`。

---

## 2. 状态尺度（本矩阵定义，写进矩阵 `stage_scale`）

| 状态 | 含义 |
|---|---|
| `S0` | 无产物（环节尚未启动） |
| `S1` | 有规格、契约或申请包等设计产物，没有本地可运行实现与可回放证据 |
| `S2` | 有本地实现与可回放证据（run 记录 / validator / freeze 记录），未完成跨仓联调与独立评审 |
| `S3` | 跨仓联调与独立评审证据齐备（**仍不等于 accepted**，不构成授权或状态提升） |
| `pending` | 等待上游环节或人工授权，当前无法推进 |
| `unknown` | 找不到真实证据（必须同时 `inferred: true`；本次未使用） |

---

## 3. 链路矩阵表（6 环节）

| # | stage_id | 环节 | owner | 状态 | 产物/证据（摘要） | 依赖 | 主要缺口 |
|---:|---|---|---|---|---|---|---|
| 1 | `STAGE-01-CANONICAL-CONTRACT` | canonical 契约 | GPCF（F-013） | **S2** | okf manifest + envelope Schema + KnowledgeObject Schema + 词表 + 示例；freeze 17c9 / 76ac；确定性 validator | — | freeze 待独立评审（`release_unblocked=false`）；manifest `updated_at` 落后 freeze；v0.1 下两次哈希修订无 patch 位 |
| 2 | `STAGE-02-KDS-STORAGE` | KDS 存储 | KDS | **S2** | KDS Release0 canonical read facade run（`status: partial` / `completion: not_complete`）；读契约 freeze `contract_frozen_for_future_implementation_not_integrated` | 01 | 契约未 integrated；run 未收口；真实 KDS 写入未授权；vendored 镜像哈希准入未成门禁 |
| 3 | `STAGE-03-STUDIO-INGEST` | Studio 接入 | Studio | **S2** | canonical read BFF 集成 run（`completed_pending_targeted_independent_review` / 内层 `partial_not_complete`）；build-result | 01, 02 | 定向独立评审未做；`local_release_review_boundary` 未解除；无 `review_required → approved` 回放 |
| 4 | `STAGE-04-BRAIN-CANDIDATE` | Brain candidate | Brain | **S2** | consumer audit（`report_only_static_and_test_replay`）；page 隔离 run（`status_claim: partial`）；canonical preview 系列 run | 01, 02 | 非真实数据联调；`human_review_boundary`；candidate 与 Studio 复核缺同一 correlationId 关联 |
| 5 | `STAGE-05-MMC-AUTHORIZATION` | MMC 授权 | MMC | **S1** | canonical read relay acceptance（a10i2）；policy admission run（`status: partial`）；preflight | 02, 03, 04 | 只有申请包（`human_authorization_request_only`），无 granted 回执；`authorization_granted=0`；策略 apply 需单独授权 |
| 6 | `STAGE-06-HUMAN-CONFIRMATION` | 人工确认 | 人工（业务/场景 owner） | **pending** | 控制台账（授权边界列）；F-013 feature blockers | 05 | 无任何人工确认回执；F-013 blockers 未清；Agent 不得代行 |

**状态分布**：`S0=0 / S1=1 / S2=4 / S3=0 / pending=1`。**没有任何环节达 S3**，即"跨仓联调 + 独立评审证据齐备"这一档尚未出现。

**证据基底（可回放）**

- GPCF 侧：`features/active/F-013-knowledge-asset-model-system/artifacts/`（canonical freeze、read-contract freeze、brain consumer audit、studio bridge、mmc authorization 等协调记录）
- KDS 侧：`.harness/runs/20260811-193752-implement-release0-canonical-read-facade/`（run.yaml / acceptance-matrix.md / f013-handoff.md / evidence-index.yaml）
- Studio 侧：`.harness/runs/20260811-195500-integrate-release0-canonical-read-bff/`（run.yaml / acceptance-matrix.md / build-result.md / handoff.md）
- Brain 侧：`.harness/runs/20260814-isolate-brain-release0-page-from-mmc-fallback-a10r4/`、`.harness/runs/20260905-100845-canonical-search-preview-identity/`
- MMC 侧：`.harness/runs/20260811-132225-implement-release0-canonical-read-relay-a10i2/`、`.harness/runs/20260813-admit-release0-canonical-read-policy-a10c7/`

---

## 4. 当前断点排序（7 条：P0 2 / P1 3 / P2 2，blocking 5）

| 序 | breakpoint_id | 环节 | 标题 | 严重度 | 阻塞 | 处理建议 |
|---:|---|---|---|---|---|---|
| 1 | `BP-01-HUMAN-CONFIRMATION-GAP` | 06 人工确认 | 人工确认环节空洞，链路末端无回执 | **P0** | 是 | 先只对「KDS Release0 只读访问」一条权限做一次人工确认并登记回执，不涉写入/记忆/状态提升 |
| 2 | `BP-02-MMC-AUTH-NOT-EFFECTIVE` | 05 MMC 授权 | MMC 授权只有申请包，未生效 | **P0** | 是 | 把「申请包 → 人工确认 → 回执登记」做成最小闭环，让 Studio/Brain 读请求引用同一授权号 |
| 3 | `BP-03-KDS-CONTRACT-NOT-INTEGRATED` | 02 KDS 存储 | 读契约 frozen 但未 integrated，run 仍 partial | P1 | 是 | 用同一契约哈希做一次只读联调回放，把契约版本写进 KDS run 证据并收口 partial |
| 4 | `BP-04-CANONICAL-FREEZE-PENDING` | 01 canonical | freeze 待独立评审，版本锚点滞后 | P1 | 是 | 先出独立评审结论并回写 manifest `updated_at` 与 patch 位规则，再把哈希下传到三个下游环节 |
| 5 | `BP-05-PER-REPO-REVIEW-INCOMPLETE` | 03 Studio 接入 | Studio / Brain 各仓独立评审未完成 | P1 | 是 | 两仓各做一次定向独立评审（同一 acceptance-matrix 口径），只收口各自环节结论 |
| 6 | `BP-06-NO-CHAIN-EVIDENCE-INDEX` | 01 canonical | 跨仓证据无统一链路索引，回放靠人工拼接 | P2 | 否 | 新增链路级 evidence-index（只登记路径与哈希），由 stage_id 与各仓 run id 双向引用 |
| 7 | `BP-07-CONTRACT-DOMAIN-ALIGNMENT` | 05 MMC 授权 | 知识链路未与跨项目契约矩阵对齐 | P2 | 否 | 在 PG-12 契约矩阵补知识域条目，把授权失败映射到统一错误码后再联调 |

> 排序规则：先 `blocking` 为真、再按 P0→P1→P2；校验器强制断点表按 P0→P1→P2 非降序排列（乱序即 fail）。

---

## 5. 最小闭环建议（只做只读，不做写入/记忆/状态提升）

**建议的最小闭环 = 「一条只读权限 + 一次端到端回放 + 一条人工回执」**，不追求 6 环全部 S3：

1. **固定起点**：以当前 canonical freeze（17c9…）与控制面 manifest 哈希为唯一锚点，先出独立评审结论（清 `BP-04`）。
2. **打通授权**：MMC 就「KDS Release0 只读」发一次授权申请 → 人工确认 → 登记 `granted` 回执（清 `BP-02`、`BP-01` 的第一条），授权号写进后续证据。
3. **端到端回放**：用 KDS 只读 facade → Studio BFF → Brain preview 做**同一次**只读查询，三个仓共用同一 `correlationId` + 同一契约哈希，产出单份链路 evidence-index（清 `BP-03`、`BP-06` 的前半）。
4. **收口口径**：三个仓各写一份结论（S2 维持或升 S3），但**状态提升仍需人工确认**，不由本链路自动给出。
5. **禁止跨级**：本地 fixture / validator / dry-run 通过一律不得写成"链路闭环"；写入、长期记忆、业务状态变更、状态提升四类动作在规范 §14 下保持 `false`。

---

## 6. 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `stage_id` / `stage_key` | str | 环唯一标识；`stage_key` 取值固定 6 种，校验器要求每种恰好出现 1 次 |
| `name` / `owner` | str | 环节名与责任方 |
| `status` | enum | `S0/S1/S2/S3/pending`（找不到证据才用 `unknown` + `inferred: true`） |
| `status_basis` | str | **状态判据**：必须写出该状态的证据依据（run 结论或 freeze 字段） |
| `artifacts` / `evidence` | list | 产物与证据文件路径，逐条校验存在（相对 GPCF 根或工作区根） |
| `depends` | list | 上游环节 id；校验器查存在性、自依赖与环 |
| `gaps` | list | 缺口；未完成环节（S0/S1/S2/pending/unknown）必须 ≥1 条 |
| `inferred` | bool | 是否存在推断值 |
| `breakpoints[]` | — | `breakpoint_id / stage_id / title / severity(P0-P2) / blocking / detail / evidence / recommendation / inferred`，按 P0→P1→P2 排序 |

---

## 7. 验证命令与真实输出

### 7.1 通过

```bash
cd "GlobalCoud GPCF"
python3 tools/kds-sync/validate_gke001_chain_matrix.py
```

```text
PASS validate_gke001_chain_matrix
  matrix         : /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/runtime/gke001-chain-matrix.yaml
  domain         : GKE-001（canonical_feature=F-013）
  chain_closed   : False（source_of_truth=False）
  declared       : engineering=active cross_project=partial completion=not_complete
  stages         : 6 个环节
    - STAGE-01-CANONICAL-CONTRACT: key=canonical_contract status=S2 owner=GPCF（F-013 canonical 契约与独立验收工作包） artifacts=5 evidence=4 gaps=3
    - STAGE-02-KDS-STORAGE: key=kds_storage status=S2 owner=KDS artifacts=4 evidence=3 gaps=4
    - STAGE-03-STUDIO-INGEST: key=studio_ingest status=S2 owner=Studio artifacts=4 evidence=1 gaps=3
    - STAGE-04-BRAIN-CANDIDATE: key=brain_candidate status=S2 owner=Brain artifacts=3 evidence=2 gaps=3
    - STAGE-05-MMC-AUTHORIZATION: key=mmc_authorization status=S1 owner=MMC artifacts=4 evidence=3 gaps=4
    - STAGE-06-HUMAN-CONFIRMATION: key=human_confirmation status=pending owner=人工（业务对象 owner / 场景 owner；Agent 不得代行） artifacts=2 evidence=2 gaps=4
  status_dist    : S0=0 S1=1 S2=4 S3=0 pending=1
  breakpoints    : 7 条（P0=2 P1=3 P2=2，blocking=5）
  checks         : schema=pass stages=pass unique_id=pass artifacts=pass evidence=pass status=pass depends=pass gaps=pass breakpoints_order=pass no_closure_claim=pass sensitive=pass
[exit code: 0]
```

### 7.2 六个负例（故意破坏，均 exit 1）

```text
===== 负例：dup-id =====
FAIL stage_id 重复：STAGE-01-CANONICAL-CONTRACT
FAIL 环节缺失或重复：stage_key=kds_storage（出现 0 次，必须恰好 1 次）
FAIL STAGE-03-STUDIO-INGEST 的 depends 引用了不存在的环节：STAGE-02-KDS-STORAGE
FAIL STAGE-04-BRAIN-CANDIDATE 的 depends 引用了不存在的环节：STAGE-02-KDS-STORAGE
FAIL STAGE-05-MMC-AUTHORIZATION 的 depends 引用了不存在的环节：STAGE-02-KDS-STORAGE
FAIL breakpoints[2](BP-03-KDS-CONTRACT-NOT-INTEGRATED) stage_id 未指向已定义环节：'STAGE-02-KDS-STORAGE'
FAIL validate_gke001_chain_matrix: 6 项校验失败（matrix=/tmp/pg13-neg/dup-id.yaml）
[exit: 1]

===== 负例：dup-stage-key =====
FAIL 环节缺失或重复：stage_key=brain_candidate（出现 2 次，必须恰好 1 次）
FAIL 环节缺失或重复：stage_key=human_confirmation（出现 0 次，必须恰好 1 次）
FAIL validate_gke001_chain_matrix: 2 项校验失败（matrix=/tmp/pg13-neg/dup-stage-key.yaml）
[exit: 1]

===== 负例：bad-path =====
FAIL stages[0](STAGE-01-CANONICAL-CONTRACT) 的 artifacts 路径不存在：okf/not-exist-object.schema.json（尝试：['okf/not-exist-object.schema.json', '../okf/not-exist-object.schema.json']）
FAIL validate_gke001_chain_matrix: 1 项校验失败（matrix=/tmp/pg13-neg/bad-path.yaml）
[exit: 1]

===== 负例：invalid-status =====
FAIL stages[5](STAGE-06-HUMAN-CONFIRMATION) status 非法：'S9'，允许 ('S0', 'S1', 'S2', 'S3', 'pending', 'unknown')
FAIL validate_gke001_chain_matrix: 1 项校验失败（matrix=/tmp/pg13-neg/invalid-status.yaml）
[exit: 1]

===== 负例：closure-claim =====
FAIL chain_closed 必须为 false：本任务不声明链路闭环
FAIL validate_gke001_chain_matrix: 1 项校验失败（matrix=/tmp/pg13-neg/closure-claim.yaml）
[exit: 1]

===== 负例：sensitive-key =====
FAIL 敏感字段名：/stages[0]/api_key#key -> api_key（不允许登记凭据类字段）
FAIL 疑似密钥值：/stages[0]/api_key 命中 \bsk-[A-Za-z0-9_-]{16,}
FAIL validate_gke001_chain_matrix: 2 项校验失败（matrix=/tmp/pg13-neg/sensitive-key.yaml）
[exit: 1]
```

> 负例均为 `/tmp/pg13-neg/` 下的一次性副本，不改仓库文件。六类依次覆盖：id 唯一性、6 环节齐备、路径存在性、状态合法、不声明闭环、敏感内容。

### 7.3 校验项清单

| 校验项 | 说明 |
|---|---|
| schema | 顶层 13 个必填字段、`stage_scale` 五档、`declared_status` 七字段 |
| stages | 6 个 `stage_key` 各恰好 1 次 |
| unique_id | `stage_id`、`breakpoint_id` 唯一 |
| artifacts / evidence | 每条路径解析到真实文件（绝对 → GPCF 根 → 工作区根） |
| status | `S0/S1/S2/S3/pending`，`unknown` 必须 `inferred: true` |
| depends | 引用存在、无自依赖、无环（三色 DFS） |
| gaps | 未完成环节至少 1 条缺口 |
| breakpoints_order | 断点必须按 P0→P1→P2 非降序、`stage_id` 指向真实环节 |
| no_closure_claim | `chain_closed` 与 `source_of_truth` 必须为 false；`completion_status` 不得为完成类；四项授权布尔必须为 false |
| sensitive | 凭据类键名与密钥形态值扫描 |

---

## 8. 待办与非声明

### 8.1 待办（本次未做）

1. **不推进任何环节状态**：本任务只盘点，6 个环节状态与断点均按现状登记，未改 KDS / Studio / Brain / MMC 任一仓。
2. **不产生人工确认**：`STAGE-06` 保持 `pending`，人工确认只能由业务/场景 owner 给出。
3. **未建立链路级 evidence-index**：`BP-06` 只登记为断点，落地需新增文件（超出本任务写入范围）。
4. **本报告未登记受控文档头**：`09-status/` 新增 Markdown 需由 `document_control.py` 生成 `doc_id` / `kds_path`，本次未跑（会重写全量台账，超出写入范围）。
5. **未纳入门禁链**：建议把 `validate_gke001_chain_matrix.py` 加入 LOOP 文档门禁或 GPCF 2.0 Evidence Gate。

### 8.2 非声明

- 不声明 GKE-001 链路闭环：`chain_closed: false`，且无任何环节达 S3，两个关键环节分别停在 S1 与 pending。
- 不声明 MMC 授权已生效、人工确认已完成、KDS 写入已授权、长期记忆写入已授权、业务状态可变、状态可提升（矩阵 `declared_status` 四项授权布尔全为 `false`）。
- 不声明冲突/缺口已解决：7 条断点全部保留，其中 5 条 blocking。
- 不声明矩阵覆盖全部知识工程工作（仅 6 个链路环节，GKE-001 的 Release 1–3、PDF/OCR、转写、长期记忆等未纳入）。
- 不声明任何项目状态提升。

### 8.3 回滚

- **撤什么**：删除 `runtime/gke001-chain-matrix.yaml`、`tools/kds-sync/validate_gke001_chain_matrix.py`、本报告。
- **保持什么**：未修改任何被盘点仓文件，无需回滚他人产物；失败时状态保持 `repair_required`。
- **不自动做什么**：不自动 `stage` / `commit` / `push` / `delete` / `deploy`；不自动运行 `document_control.py` 或任何会重写台账的命令。
