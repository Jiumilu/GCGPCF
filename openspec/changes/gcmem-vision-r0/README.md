---
doc_id: GPCF-DOC-09A691DC1E
title: GCMEM R0 变更包索引（gcmem-vision-r0）
project: KDS
related_projects: [GCMEM, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/gcmem-vision-r0/README.md
source_path: openspec/changes/gcmem-vision-r0/README.md
sync_direction: local_only
last_reviewed: 2026-10-21
supersedes: []
superseded_by: []
master_control: GPCF:01-architecture/GlobalCloud 项目群总体方案.md
---

# gcmem-vision-r0（GCMEM R0 可信基线变更包）

**结论：本目录是 GCMEM 首个 OpenSpec 变更包在 GPCF 的中央登记副本（源副本在 GCMEM 仓 `openspec/changes/gcmem-vision-r0/`，内容以源为准），范围为 R0 可信基线（设计阶段 D0 设计冻结 + D1 可信基线），四件套（proposal / design / specs / tasks）齐备；本包只冻结契约与规则，不含任何业务代码交付，状态上界为 `candidate` + 项目 `partial`。中央登记已于 2026-10-21 经老卢授权执行（A1）：`openspec/README.md` 文档清单 + `09-status/globalcloud-document-control-register.md` + 本目录；登记本身不产生任何状态提升。**

## 1. 性质与状态

| 项 | 值 | 说明 |
|---|---|---|
| 变更包名 | `gcmem-vision-r0` | 与 PRD「R0 可信基线」、设计「D0 → D1」对齐（设计 §14.0 阶段映射） |
| 落位 | GPCF 仓 `openspec/changes/gcmem-vision-r0/`（中央登记副本）；源副本在 GCMEM 仓同路径 | 老卢 2026-10-21 全部授权 A1；副本内容以 GCMEM 仓源为准，仅调整 frontmatter 与登记状态句 |
| 覆盖阶段 | D0（设计冻结，0～1 月，5 WP / 12 人日）+ D1（可信基线，0～3 月，7 WP / 39 人日） | 设计 §14.1、§14.2 |
| 当前状态 | `draft`（GPCF 受控状态）/ `candidate`（GCMEM 源文档） | 项目状态 `partial`；登记不产生任何受控状态提升 |
| 中央登记 | **已登记（2026-10-21 老卢授权 A1）** | `openspec/README.md` 文档清单 + `09-status/globalcloud-document-control-register.md` 全量清单；F-026 只读绑定，不改 Feature 文件 |
| 交付判定 | 文档完成 ≠ 功能已实现；checkbox 勾选 ≠ 交付/验收 | 见 `tasks.md` §0.3 |

状态上界总则：本包任何章节完成、任何门禁通过，最多支撑 `candidate` / `partial` / `ready_for_review` 候选；`accepted` / `integrated` / `production_ready` / `customer_accepted` 只能由人工按治理链决定，本文不产生，也不作为宣称。

## 2. 文件索引

| 文件 | doc_id | 用途 | 权威来源 |
|---|---|---|---|
| `.openspec.yaml` | —（YAML，无 frontmatter） | 变更包元数据：保留 GPCF 样本核心键 `schema: spec-driven` / `created`，追加变更包元数据（`change`/`status: draft`/`repository: GlobalCloud Mem`/`program`/`feature`/`registration: registered-gpcf-20261021`/`registered_in: GlobalCoud GPCF`），用于绑定 F-026 与标注中央登记完成；此处 `status: draft` 是 OpenSpec 变更生命周期，GCMEM 源文档状态的 `candidate` 见各 md frontmatter | GPCF `openspec/changes/project-plane-gpcf-integration/.openspec.yaml` |
| `README.md` | `GPCF-DOC-09A691DC1E` | 本索引：范围、状态、阅读顺序、校验与登记说明 | 本文件 |
| `proposal.md` | `GPCF-GCMEM-VISION-R0-PROPOSAL-20261021` | Why / What changes / Affected / Non-goals / Rollback boundary / Feature 绑定 / 证据要求 | PRD §14、设计 §14.0–§14.2 |
| `design.md` | `GPCF-GCMEM-VISION-R0-DESIGN-20261021` | 冻结范围、PRD/设计章节映射、**回滚开关清单（6 类对象）**、影子运行与回退、风险 | 设计 §7.5、§4.5、§10.2、§13.3、§13.4、§12.1 |
| `tasks.md` | `GPCF-GCMEM-VISION-R0-TASKS-20261021` | WP-D0-01..05 与 WP-D1-01..07 任务清单（含依赖与证据要求） | 设计 §14.1、§14.2 |
| `specs/gcmem-vision-r0/spec.md` | `GPCF-GCMEM-VISION-R0-SPEC-20261021` | 能力规格：PRD 需求 ID → Given/When/Then 场景 → 契约引用 | PRD §5（CTX/CAP/EVA/INT/OPS 等）、设计 §9、§10 |

## 3. 建议阅读顺序

1. `proposal.md` §Why / §What Changes —— 先确认「做什么、不做什么、回滚到哪里」；
2. `design.md` §3 冻结范围 → §4 章节映射 → **§5 回滚开关清单（6 类）**；
3. `specs/gcmem-vision-r0/spec.md` —— 逐条需求与场景，核对 PRD ID 与契约文件名；
4. `tasks.md` —— 施工顺序、依赖链、证据要求；先看 §0.3「勾选不等于交付」再读 checkbox。

## 4. 与其他交付物的关系（D0 冻结对象）

| 冻结对象 | 契约文件（D0 交付清单） | 本包对应章节 | 状态（2026-10-21 只读核验） |
|---|---|---|---|
| ContextPack v1 | `contracts/contextpack.v1.schema.json`、`contracts/contextpack.v1.examples.json` | `design.md` §3.1、`spec.md` R1–R2 | 已落盘；`scripts/validate_contracts.py` PASS（合法 4 / 非法 8）。本包只引用文件名与设计 §7.5，不复制内容 |
| meta v2（13 键） | `contracts/ledger-meta.v2.schema.json`、`ledger-meta.v2.contract.md`、`ledger-meta.v2.examples.json` | `design.md` §3.2、`spec.md` R4 | 已落盘；校验 PASS（合法 5 / 非法 10；221 条账本只读回归全解析）。本包只引用文件名与设计 §4.5 |
| 评测集 v2 | `contracts/eval-dataset.v2.schema.json`、`eval-dataset.v2.examples.json`、`docs/GCMEM-评测集v2-分类与holdout规则.md` | `design.md` §3.3、`spec.md` R6 | schema 与样例已落盘且 PASS（合法 3 / 非法 8）；分类与 holdout 规则文档属 WP-D0-04 待收尾，写作时未落盘。本包只引用文件名与设计 §10.1/§10.2 |
| 契约目录说明 | `contracts/README.md` | `README.md` 本表 | 已落盘（目录说明与版本策略，由 WP-D0-02/03/04 汇总） |
| 变更包本体 | 本目录 6 个文件 | 全部 | WP-D0-05 交付范围 |

> 纪律：契约内容以 `docs/GCMEM-远景详细设计方案.md`（v2.0，4113 行）与 `docs/GCMEM-远景产品需求文档-PRD.md`（v2.0，1434 行）为唯一源；本包**不发明字段、不复制契约正文**；发现设计缺口记入 `design.md` §9 待确认项并回报 Lead。契约文件与校验脚本位于 **GCMEM 仓**（`contracts/`、`scripts/validate_contracts.py`），本 GPCF 副本只引用文件名，不复制契约正文与样例。

## 5. 校验与门禁命令

> 下列命令在 **GCMEM 仓**执行；GPCF 副本只做 frontmatter、doc_id 唯一性与登记一致性核对。

| 检查 | 命令 | 通过判据 |
|---|---|---|
| YAML 可解析 | `python3 -c "import yaml,sys;print(yaml.safe_load(open('openspec/changes/gcmem-vision-r0/.openspec.yaml')))"`（或 stdlib 逐行核） | 输出含 `schema: spec-driven` |
| 文档 frontmatter | 逐文件核对 16 键（15 字段 + `master_control`） | 缺一即不通过 |
| 契约校验 | `PYTHONPATH= python3 scripts/validate_contracts.py` | 全部样例 valid/invalid 与期望一致（脚本由 Lead 产出） |
| 旧口径与禁词 | `python3 /tmp/gcmem-vision/check_docs.py .` 覆盖 PRD 与详细设计；本包 5 份 md 由 Lead 用同一旧口径清单与禁词规则复核（本包不复制旧口径字面量，避免自我命中） | 旧口径 0 命中；禁词无非否定表述 |
| 文档门禁 | `bash scripts/gate_check.sh` | 全项 PASS（不改变 `candidate`/`partial`） |
| 回滚清单完备 | 人工核对 `design.md` §5：6 类对象 × 5 列（开关名/默认值/关闭后行为/影响面/验证方式） | 6 类齐备、无空列 |

## 6. 中央登记与授权（已于 2026-10-21 执行）

| 事项 | 状态 | 依据 | 说明 |
|---|---|---|---|
| GPCF 中央登记 | **已登记（2026-10-21）** | 老卢 2026-10-21「全部授权」A1 | 登记位置：本目录 + `openspec/README.md` 文档清单 + `09-status/globalcloud-document-control-register.md` 全量清单 |
| Feature 绑定 | 只读绑定 F-026 | F-026 `feature.yaml`：`status: active`、`loop.current_step: evaluate`、`iteration: 4`、`status_ceiling: partial`；`journal.md` 已记录至 Iteration 5；证据状态 tests/build/summary=pass、screenshots/api=waived | 本包不改 F-026 `feature.yaml` / `journal.md` / `evidence/`；证据回传由 GPCF 侧按后续授权执行 |
| F-026 阻塞（写实） | 未关闭 | `feature.yaml` `blockers`：Feature 专属 tests/build 验收命令未声明、screenshots/api 豁免缺本 Feature 理由，Evidence Gate 不可关闭；中央门禁 `rework_required`（既有 missing_metadata / UI control / document_pollution） | 本包登记不解除 F-026 既有阻塞；证据回传后由 GPCF 侧按授权更新 |
| 推送 | 未推送 | A1 授权「不要 push」 | 已本地 commit，待 Lead 验收后统一推送 |
| 变更包拆分 | 单能力域 `gcmem-vision-r0` | 登记时按 1 个能力域执行 | 如中央要求拆 4 个 capability 目录，另立变更，不修改本包需求内容 |
| `idem` 是否进入正式 meta 契约 | 待老卢确认 | 保守默认「纳入可选键，标注待确认」 | 见 `design.md` §9、`spec.md` R4 |
| 评测集是否允许含项目名/人名（D-03） | 待老卢确认 | 保守默认「可含项目名，人名需脱敏或标注」 | 见 `design.md` §9 |

GPCF 口径说明（本副本与源副本的差异）：

1. frontmatter 按 GPCF 口径调整：`project`（README=KDS，其余=GPCF）、`owner`、`status: draft`、`kds_space: 开发`、`kds_path`、`source_path`（相对 GPCF 仓根）、`sync_direction: local_only`；`doc_id` 换发 GPCF 前缀，避免与 GCMEM 源副本 doc_id 冲突。
2. `sync_direction: local_only` 的依据：本次登记未创建 KDS 镜像、未写 `09-status/kds-development-space-sync-register.md`、未在 KDS 仓落盘；`kds_path` 只是按 GPCF 目录口径声明的目标位置，不是已存在的同步关系。若后续授权 KDS 双向同步，须运行 `python3 tools/kds-sync/document_control.py`，由该主权工具改写为 `bidirectional` 并补同步台账。
3. 正文仅修改「登记状态」相关句子；其余内容与 GCMEM 源副本一致，源变更时需同步本副本（同一变更两仓不一致时以 GCMEM 源为准并回传 GPCF）。

## 7. 变更记录

| 版本 | 日期 | 变更 | 状态 |
|---|---|---|---|
| v1.0 | 2026-10-21 | 首版：建立 D0 设计冻结变更包（6 文件），冻结范围、6 类回滚开关清单、D0/D1 任务清单与能力规格 | candidate（GCMEM 源副本） |
| v1.1 | 2026-10-21 | GPCF 中央登记副本：frontmatter 按 GPCF 口径调整（project/owner/status=draft/kds_space/kds_path/source_path/sync_direction=local_only）、doc_id 换发 GPCF 前缀、登记状态句改为「已登记（A1 授权）」；登记至 `openspec/README.md` 与 `09-status/globalcloud-document-control-register.md` | draft（GPCF 中央登记副本） |
