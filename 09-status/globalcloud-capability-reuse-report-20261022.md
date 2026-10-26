---
doc_id: GPCF-DOC-CAPABILITY-REUSE-REPORT-20261022
title: 项目群能力复用报告（2026-10-22）
project: GPCF
related_projects: [GPCF, XiaoC, WAME, KDS, MMC, Studio, XGD, WAE]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-capability-reuse-report-20261022.md
source_path: 09-status/globalcloud-capability-reuse-report-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群能力复用报告（PG-09 能力复用中台·最小版）

> **性质**：任务执行报告（PG-09）。本文件按任务交付路径写入 `09-status/`，但**尚未登记受控文档头**（无 `doc_id` / `kds_path` / `sync_direction`），待 GPCF 文档控制流程登记后方可视为受控文档。
> **任务**：PG-09 能力复用中台（最小版）｜**执行日期**：2026-10-22｜**执行者**：项目群执行智能体（灵策 / 知源 能力面）
> **写入范围**：`runtime/asset-registry/registry.yaml`（仅追加）、`tools/kds-sync/validate_asset_registry.py`、本报告。未改其它文件，未 `stage` / `commit` / `push`。
> **非声明**：本报告不提升任何项目状态；不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted` / `real_business_verified`。

---

## 1. 结论摘要

1. 项目群高频能力资产**分散在四类载体**：提示词（方案+执行提示词、任务书、片段库）、技能（`.codex/skills`）、模板（`templates/`）、组件（`tools/kds-sync/`、`scripts/`）。此前**没有统一注册表**，只有 `02-governance/loop/LOOP_CAPABILITY_REGISTRY.md` 这一个局部能力注册表（覆盖技能池/工具池/方法池，不含提示词与模板）。
2. 本次建立**统一资产注册表**：`runtime/asset-registry/registry.yaml`，已登记 **25 条资产**（四类 **24 条** + bootstrap 1 条），覆盖 prompt 7 / skill 6 / template 5 / component 6，登记复用项目 **18 个**。
3. 配套 `tools/kds-sync/validate_asset_registry.py`：9 类校验全部 pass；4 个负例（重复 id / 路径不存在 / 敏感字段 / license 为空）均按预期 fail 并返回非 0。
4. **最大复用缺口**：`openspec` 技能族无单一权威副本，13 个项目各手工复制一份；`loop_document_gate.py` 在 8 个项目被逐字引用但同时被 631 处 GPCF 内部引用，属于"事实标准但无登记"的资产。这两类是后续收敛的第一优先级。

---

## 2. 盘点结论：现有资产分散情况

### 2.1 载体分布（只读统计，2026-10-22）

| 载体 | 位置 | 规模 | 现状问题 |
|---|---|---|---|
| 组件（校验器） | `GlobalCoud GPCF/tools/kds-sync/` | 868 个 `.py`，其中 `validate_*.py` **728 个**、`build_*.py` 63 个 | 按事件命名膨胀（如 `validate_gckf_p0_*_d131…d190`），无统一入口与去重 |
| 组件（Feature 入口） | `GlobalCoud GPCF/scripts/` | `gpcf_new_feature.py` / `gpcf_close_feature.py` / `gpcf_dispatch.py` / `gpcf_check_evidence.py` | 已有 GPCF 2.0 统一入口，但未登记为可复用资产 |
| 技能 | `GlobalCoud GPCF/.codex/skills/`（7 个）+ 各项目 `.codex/skills` | GPCF 7 个；`openspec-*` 在 **13 个项目**各复制一份 | 无权威版本，靠人工复制同步 |
| 模板 | `GlobalCoud GPCF/templates/` | 19 个文件 | 高频 LOOP 模板与低频方案模板混放，无使用频次登记 |
| 提示词 | `02-governance/*提示词*.md`、`01-architecture/*提示词库*`、`KDS/世界资产/`、`MMC/docs/planning/` | 40 份 `02-governance/*.md` 中含 3 份"方案+执行提示词"、1 份提示词库；跨仓另有 3 份项目任务书 | 同一骨架被重写多版；无引用入口，新任务靠"再写一份" |
| 局部能力注册表 | `02-governance/loop/LOOP_CAPABILITY_REGISTRY.md` | 1 份（controlled） | 只覆盖技能/工具/方法池，**不含提示词、模板、组件路径**，且无 `source_path` 字段 |

### 2.2 复用现状的量化证据（ripgrep 只读统计）

| 资产/模式 | 跨项目引用分布 | 解读 |
|---|---|---|
| `loop_document_gate.py` | GPCF 631 / Studio 115 / KDS 62 / SOP 24 / SpaceAI 7 / SpaceAI Platform 5 / PQC 4 / ICP 4 | 事实标准门禁，跨 8 个项目使用，此前无登记 |
| `document_control.py` | GPCF 340 / KDS 97 / WAE 3 / MMC 1 | 文档治理事实入口，跨 4 个项目 |
| `check_document_pollution.py` | GPCF 365 / KDS 51 / SOP 13 | 防污染检查跨 3 个项目 |
| LOOP 轮次记录（`loop-round-*`） | GPCF 1270 / Studio 1015 / GFIS 360 / MMC 23 / XGD 10 / KDS 6 | 模板被广泛套用，但模板本身无登记 |
| `openspec-propose` 技能 | 13 个项目各 1 份副本（GFIS/GPC/ICP/KDS/MMC/PVA/PVAOS/SOP/Studio/WAME/WAME-p1/XGD/XiaoC） | **典型无权威副本**：13 份手工复制 |
| 智慧工厂提示词库 | KDS 77 / GPCF 8 | 片段库体裁被跨仓复用 |
| 项目总体方案 / 实施方案 | KDS / MMC / GFIS / Studio 根目录均存在成对文件 | 模板被套用，未登记 |

### 2.3 结论

- **不是缺资产，是缺"入口 + 元数据"**：高频资产已存在并被跨项目使用（如 `loop_document_gate.py`、LOOP 模板、`openspec` 技能族），但因为没登记，每次新任务仍倾向重写一份，形成 C8 文档债的放大器。
- **复用方向单向**：GPCF → 各项目。反向（项目 → 项目群）没有通道，项目内沉淀的资产无法回流。
- **局部注册表缺关键字段**：`LOOP_CAPABILITY_REGISTRY.md` 无 `source_path` / `license` / `reused_by` / `reuse_count`，无法机检"资产是否真实存在、被谁引用多少次"。本次注册表补齐这些字段。

---

## 3. 注册表字段说明

### 3.1 顶层字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` | int | 固定 `1`（沿用 bootstrap 会话建立的值，未改写） |
| `registry_status` | str | `bootstrap`（沿用原值；扩展期状态见 `extension_phase`） |
| `owner` / `domain` | str | `GPCF` / `governance`（沿用） |
| `updated` | date | 最近更新日 `2026-10-22` |
| `source_tasks` | list | 归属任务 `PG-09`、`PG-10`（沿用） |
| `bootstrap_entries` | list | **本次新增**：声明由 2026-10-22 05:57 并行会话建立的条目 id（`startlux-decision`）。这些条目只按基础字段校验，允许 `capability_service` 类型，**本任务不改写** |
| `extension_phase` | str | **本次新增**：扩展阶段说明 |
| `generated_at` | str | **本次新增**：生成时间戳（字符串，避免 YAML 时间类型误解析） |
| `usage_rule` | str | **本次新增**：使用规则（见 §6） |
| `entries` | list | 资产列表（**等价于 PG-09 规格中的 `assets`**；未重命名以兼容 bootstrap） |

### 3.2 条目字段

| 规格字段（PG-09） | 注册表字段 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | `id` | 是 | 全局唯一；`<type>.<slug>`，如 `component.loop-document-gate` |
| `type` | `type` | 是 | `prompt` / `skill` / `template` / `component`（bootstrap 条目可为 `capability_service`） |
| `name` | `title` | 是 | 人类可读名称 |
| `version` | `version` | 是 | 版本串 |
| `owner` | `owner` | 是 | 维护方项目 |
| — | `governor` | 是 | 治理方（本批统一 `GPCF`） |
| `scope` | `scope` | 是 | 用途与消费方（字符串列表） |
| — | `access` | 是 | 访问形态（`read-only` / `mcp+skill` 等） |
| `license` | `license` | 是 | 字符串或 mapping，值不得为空 |
| `source_path` | `source_path` | 扩展必填 | 真实存在的相对路径；解析顺序：绝对路径 → GPCF 根 → 工作区根 |
| `evidence` | `evidence` | 是 | 存在性/引用/产物证据（注明核对日期与统计口径） |
| `reused_by` | `reused_by` | 扩展必填 | 已核实的使用项目名列表（去重） |
| `reuse_count` | `reuse_count` | 扩展必填 | 必须等于 `reused_by` 去重项目数 |
| — | `reuse_basis` | 扩展可选 | `verified_reference`（有文件逐字引用/复制）或 `artifact_usage`（有按该资产格式产出的下游产物） |
| `status` | `status` | 扩展必填 | `active` / `draft` / `deprecated` |
| `notes` | `notes` | 扩展必填 | 使用注意事项 |
| — | `constraints` | 是 | 使用约束（防越权、防替代主存） |

> **bootstrap 兼容说明**：`registry.yaml` 与同目录 `README.md` 的 bootstrap 由另一会话于 2026-10-22 05:57 建立（`schema_version: 1`，`entries` 内已有 1 条 `startlux-decision`）。本次**只追加**：新增 4 个顶层键与 24 条条目；`startlux-decision` 条目一字未改，仍按 bootstrap 规则校验。`README.md` 未修改（其"文档清单"仅列 Markdown 文档，本次未在该目录新增 Markdown）。

---

## 4. 首批资产清单（25 条）

| # | asset id | type | owner | status | 复用项目数 | source_path |
|---:|---|---|---|---|---:|---|
| 1 | `startlux-decision` | capability_service | WAME | *（bootstrap，未设 status）* | *related 6* | *（bootstrap 无该字段）* |
| 2 | `prompt.gpcf-agent-reach-execution` | prompt | GPCF | active | 1 | `02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md` |
| 3 | `prompt.gpcf-was-ontology-execution` | prompt | GPCF | active | 1 | `02-governance/GlobalCloud项目群WAS／Ontology全量实施方案与执行提示词.md` |
| 4 | `prompt.gpcf-headroom-lcx-execution` | prompt | GPCF | active | 1 | `02-governance/GlobalCloud项目群Headroom-LCX全量实施方案与执行提示词.md` |
| 5 | `prompt.smartfactory-prompt-library` | prompt | GPCF | active | 2 | `01-architecture/GlobalCloud智慧工厂进一步梳理与提示词库.md` |
| 6 | `prompt.wae-assembly-taskbook` | prompt | KDS | active | 2 | `../GlobalCloud KDS/世界资产/WAE项目按装配体系推进_实施提示词_v1.0.md` |
| 7 | `prompt.mmc-project-line-taskbook` | prompt | MMC | active | 1 | `../GlobalCloud MMC/docs/planning/MMC项目线实施提示词_v1.0.md` |
| 8 | `prompt.project-group-task-prompt-library` | prompt | GPCF | **draft** | 1 | `../runtime/plan-20261022/GlobalCloud项目群任务提示词库_v1.0.md` |
| 9 | `skill.globalcloud-loop-orchestrator` | skill | GPCF | active | 6 | `.codex/skills/globalcloud-loop-orchestrator/SKILL.md` |
| 10 | `skill.globalcloud-document-governance` | skill | GPCF | active | 2 | `.codex/skills/globalcloud-document-governance/SKILL.md` |
| 11 | `skill.globalcloud-openspec-governance` | skill | GPCF | active | 2 | `.codex/skills/globalcloud-openspec-governance/SKILL.md` |
| 12 | `skill.openspec-change-cycle` | skill | GPCF | **draft** | **13** | `../GlobalCloud KDS/.codex/skills/openspec-propose/SKILL.md` |
| 13 | `skill.globalcloud-ui-quality-gate` | skill | GPCF | active | 2 | `.codex/skills/globalcloud-ui-quality-gate/SKILL.md` |
| 14 | `skill.globalcloud-project-group-git-clean` | skill | GPCF | active | 1 | `.codex/skills/globalcloud-project-group-git-clean/SKILL.md` |
| 15 | `template.loop-round` | template | GPCF | active | 6 | `templates/LOOP_ROUND_TEMPLATE.md` |
| 16 | `template.loop-evidence` | template | GPCF | active | 2 | `templates/LOOP_EVIDENCE_TEMPLATE.md` |
| 17 | `template.loop-round-five-direction` | template | GPCF | active | 1 | `templates/loop-round-v2-five-direction.yaml` |
| 18 | `template.project-master-plan` | template | GPCF | active | 5 | `templates/project-master-plan-template.md` |
| 19 | `template.real-evidence-record` | template | GPCF | active | 1 | `templates/real-evidence-record-template.md` |
| 20 | `component.loop-document-gate` | component | GPCF | active | **8** | `tools/kds-sync/loop_document_gate.py` |
| 21 | `component.document-control` | component | GPCF | active | 4 | `tools/kds-sync/document_control.py` |
| 22 | `component.document-pollution-check` | component | GPCF | active | 3 | `tools/kds-sync/check_document_pollution.py` |
| 23 | `component.check-frontmatter-gate` | component | GPCF | active | 3 | `tools/kds-sync/check_frontmatter_gate.py` |
| 24 | `component.gpcf-new-feature` | component | GPCF | active | 1 | `scripts/gpcf_new_feature.py` |
| 25 | `component.asset-registry-validator` | component | GPCF | active | 1 | `tools/kds-sync/validate_asset_registry.py` |

**统计**：四类 24 条（prompt 7 / skill 6 / template 5 / component 6）+ bootstrap 1 条；`status` 分布 active 22、draft 2（条目 12 许可待核实、条目 8 为 scratch 未受控）、bootstrap 1。

**复用项目并集（18 个）**：GFIS、GPC、GPCF、ICP、KDS、MMC、PQC、PVA、PVAOS、SOP、SpaceAI、SpaceAI Platform、Studio、WAE、WAME、WAME-p1、XGD、XiaoC。

---

## 5. 复用度量定义

| 指标 | 定义 | 本批实测 |
|---|---|---|
| 被引用项目数 `reuse_count` | 该资产 `reused_by` 去重后的项目数（含创作方自身在用） | 中位数 2，最大 13（`skill.openspec-change-cycle`） |
| 复用项目并集 | 全表 `reused_by` 去重后项目名集合大小 | **18 个** |
| 复用覆盖度 | 复用项目数 ≥2 的资产占比 | 14 / 24 ≈ 58% |
| 单项目资产 | `reuse_count = 1`，仅创作方在用 | 10 条，列入"待推广"清单 |
| 节省工时估算 | `Σ(单位成本 × (reuse_count − 1))`，单位成本按类型经验值：prompt 0.5、skill 1.0、template 0.5、component 1.5 人日 | **≈47 人日**（prompt 1.0 + skill 20.0 + template 5.0 + component 21.0） |

> **估算口径与非声明**：单位成本是经验值，**未实测**、不含维护与对齐成本（13 份副本的漂移成本单独计）；该数字只用于排序"先收敛哪个资产"，不得作为交付绩效或预算依据。`reuse_basis` 必须随 `reused_by` 一起读：`verified_reference` 有文件可复现，`artifact_usage` 只能证明"按该资产形态产出了下游产物"。

**优先收敛建议（按节省工时 × 缺口风险）**：
1. `skill.openspec-change-cycle`（13 份副本 → 1 份权威 + 分发方式）—— 12 人日；
2. `component.loop-document-gate`（8 个项目逐字引用同一路径，缺登记与版本约定）—— 7 人日；
3. `template.loop-round` + `skill.globalcloud-loop-orchestrator`（轮次记录 2700+ 份，模板无版本锚点）—— 10 人日；
4. 10 条单项目资产：先做"是否需要跨项目复用"的判定，再决定推广或降级。

---

## 6. 使用规则

1. **先查表再动手**：新增提示词/技能/模板/组件前，先按 `type` 与关键词查 `entries`；存在即复用并回填 `reused_by`，**不新建平行资产**。
2. **只引用路径，不复制正文**：本表只登记元数据；取用一律回 `source_path` 指向的受控文件（权威落点回链）。
3. **复用即登记**：任何项目使用某资产，应在对应条目 `reused_by` 追加项目名、`reuse_count` 同步 +1，并更新 `evidence`（引用位置或产物路径）。新增 `reused_by` 必须有证据。
4. **`status` 语义**：`active` 可用；`draft` 不得直接用于对外交付（本批 2 条：许可待核实、scratch 未受控）；`deprecated` 不得新引用，只保留追溯。
5. **资产登记 ≠ 授权/验收/状态提升**：登记只表示"该资产存在且可复用"，不替代 WAME 裁决、KDS 事实主存、GFIS source-of-record、Harness 证据验收，不构成任何项目实施授权。
6. **禁止登记的内容**：凭据、客户原件、受限正文、未脱敏生产数据；只登记路径与元数据（校验器会拦截凭据类键名与密钥形态的值）。
7. **变更即校验**：每次改 `registry.yaml` 后必须运行 `python3 tools/kds-sync/validate_asset_registry.py`，非 0 不得提交。

---

## 7. 校验器：`tools/kds-sync/validate_asset_registry.py`

只读校验，不写任何文件；依赖标准库 + PyYAML 6.0.2。校验项：

| 编号 | 校验项 | 失败表现 |
|---|---|---|
| R1 | 顶层 schema（`schema_version`/`registry_status`/`owner`/`domain`/`updated`/`source_tasks`/`entries`）与 `bootstrap_entries` | 缺字段、类型错 |
| R2 | 条目必填字段（`id/title/version/type/owner/governor/scope/access/license/evidence/constraints`） | 缺字段、空值 |
| R3 | `id` 唯一（大小写不敏感） | 重复 id |
| R4 | `type` / `status` 白名单（`capability_service` 仅限 bootstrap 条目） | 非法类型/状态 |
| R5 | `source_path` 真实存在（绝对 → GPCF 根 → 工作区根 顺序解析，必须是文件） | 路径不存在 |
| R6 | `license` 非空（字符串非空，或 mapping 所有值非空） | 空 license |
| R7 | `reused_by` 是非空项目名列表、无重复、`reuse_count` 一致、`reuse_basis` 合法 | 不一致/格式错 |
| R8 | 敏感内容：凭据类键名（`token/secret/password/api_key/credential/...`）与密钥形态值（`sk-...`/`ghp_...`/`AKIA...`/PRIVATE KEY 等） | 命中即失败 |
| R9 | 覆盖度：四类齐备、四类资产数 ≥ `--min-assets`(20)、复用项目数 ≥ `--min-reuse-projects`(3) | 覆盖不足 |

### 7.1 真实输出 A：bootstrap 状态（扩展前，`registry.yaml` 仍 37 行 / 1 条条目）

```text
$ python3 tools/kds-sync/validate_asset_registry.py
FAIL entries[0](startlux-decision) 只有 bootstrap_entries 中的条目可以使用类型 capability_service
FAIL entries[0](startlux-decision) 缺扩展字段：source_path（非 bootstrap 条目必须补齐）
FAIL entries[0](startlux-decision) 缺扩展字段：reused_by（非 bootstrap 条目必须补齐）
FAIL entries[0](startlux-decision) 缺扩展字段：reuse_count（非 bootstrap 条目必须补齐）
FAIL entries[0](startlux-decision) 缺扩展字段：status（非 bootstrap 条目必须补齐）
FAIL entries[0](startlux-decision) 缺扩展字段：notes（非 bootstrap 条目必须补齐）
FAIL 四类资产总数 0 < 下限 20
FAIL type 覆盖缺失：没有任何 prompt 类资产
FAIL type 覆盖缺失：没有任何 skill 类资产
FAIL type 覆盖缺失：没有任何 template 类资产
FAIL type 覆盖缺失：没有任何 component 类资产
FAIL 复用项目数 0 < 下限 3
WARN entries[0](startlux-decision) id 建议以 'capability_service.' 前缀开头
FAIL validate_asset_registry: 12 项校验失败（registry=/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/runtime/asset-registry/registry.yaml）
[exit code: 1]
```

> 该次失败说明：校验器先按"全部条目都需扩展字段"处理，因此**必须先**在顶层声明 `bootstrap_entries`，再追加条目。这是本次"先跑校验器、再补注册表"的中间态记录，保留以证明校验器确实生效。

### 7.2 真实输出 B：扩展后正式通过

```text
$ python3 tools/kds-sync/validate_asset_registry.py
PASS validate_asset_registry
  registry        : /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/runtime/asset-registry/registry.yaml
  schema_version  : 1 (registry_status=bootstrap, updated=2026-10-22)
  entries         : 25 条（四类 24 条, capability_service=1）
  type_distribution: prompt=7 skill=6 template=5 component=6
  reuse_projects  : 18 个 -> GFIS, GPC, GPCF, ICP, KDS, MMC, PQC, PVA, PVAOS, SOP, SpaceAI, SpaceAI Platform, Studio, WAE, WAME, WAME-p1, XGD, XiaoC
  checks          : schema=pass unique_id=pass type=pass source_path=pass license=pass reused_by=pass coverage=pass sensitive=pass
[exit code: 0]
```

### 7.3 真实输出 C：四个负例（故意破坏，均返回非 0）

```text
===== 负例：dup-id =====
FAIL asset id 重复：template.loop-round（entries[14] 与 entries[24]）
WARN entries[24](template.loop-round) id 建议以 'component.' 前缀开头
FAIL validate_asset_registry: 1 项校验失败（registry=/tmp/pg09-neg/dup-id.yaml）
[exit code: 1]

===== 负例：bad-path =====
FAIL entries[16](template.loop-round-five-direction) source_path 不存在：templates/not-exist-template-v9.yaml（尝试：['templates/not-exist-template-v9.yaml', '../templates/not-exist-template-v9.yaml']）
FAIL validate_asset_registry: 1 项校验失败（registry=/tmp/pg09-neg/bad-path.yaml）
[exit code: 1]

===== 负例：sensitive-key =====
FAIL 敏感字段名：/entries[14]/api_key#key -> api_key（不允许登记凭据类字段）
FAIL 疑似密钥值：/entries[14]/api_key 命中 \bsk-[A-Za-z0-9_-]{16,}
FAIL validate_asset_registry: 2 项校验失败（registry=/tmp/pg09-neg/sensitive-key.yaml）
[exit code: 1]

===== 负例：empty-license =====
FAIL entries[18](template.real-evidence-record) license 不能为空（字符串非空，或 mapping 的每个值非空）
FAIL validate_asset_registry: 1 项校验失败（registry=/tmp/pg09-neg/empty-license.yaml）
[exit code: 1]
```

> 负例均为 `/tmp/pg09-neg/` 下的一次性副本，不改仓库文件；三个受审计的负例类别（重复 id / 路径不存在 / 敏感字段）与任务要求一致，另加 license 为空一项。

---

## 8. 自检清单

| 检查项 | 结果 |
|---|---|
| 资产总数 ≥20 | ✅ 25 条（四类 24 条 + bootstrap 1 条） |
| 四类覆盖面 | ✅ prompt 7 / skill 6 / template 5 / component 6 |
| ≥3 个项目出现在 `reused_by` | ✅ 18 个项目 |
| `source_path` 真实存在 | ✅ 校验器 R5 全量核对（相对 GPCF 根 / 工作区根两种基准，均在条目中写明） |
| 无凭据 / 客户原件 / 受限内容 | ✅ R8 敏感扫描 pass；注册表只含路径与元数据 |
| bootstrap 条目未被改写 | ✅ `startlux-decision` 原样保留，改用 `bootstrap_entries` 声明 |
| 只写三处 | ✅ `runtime/asset-registry/registry.yaml`（仅追加）、`tools/kds-sync/validate_asset_registry.py`、本报告 |
| 未 commit / push / deploy | ✅ 仅本地工作区写入 |
| 未改 `runtime/audit/`（PG-10 并行产物） | ✅ 未触碰 |
| 未跑 `document_control.py` | ✅ 未跑（会重写全量台账与 `.kds` 镜像，超出写入范围） |

---

## 9. 边界、待办与回滚

### 9.1 待办（本次未做，需单独授权/排期）

1. **KDS 镜像未刷新**：`GlobalCloud KDS/concepts/开发/91-治理与验收/runtime/asset-registry/` 仍是 bootstrap 版镜像。刷新需运行 `document_control.py`，会重写全量文档控制台账与 `.kds` 镜像（超出本任务写入范围），需授权后单独执行。
2. **本报告未登记受控文档头**：`09-status/` 新增 Markdown 必须由 `document_control.py` 生成 `doc_id` / `kds_path`，本次未做（同上原因）。当前只能按任务产出报告使用。
3. **`registry.yaml` 未纳入门禁链**：建议后续把 `validate_asset_registry.py` 加入 LOOP 文档门禁或 GPCF 2.0 Evidence Gate，使注册表变更自动被校验。
4. **单项目资产推广判定**：10 条 `reuse_count = 1` 的资产需要逐条判定"推广 / 保持单项目 / 降级"，本次只做标记。

### 9.2 非声明

- 不声明任何项目状态提升（`accepted` / `integrated` / `production_ready` / `customer_accepted` / `real_business_verified`）。
- 不声明注册表已覆盖项目群全部能力资产（本批为最小版首批 24 条，相对 728 个校验器与 19 个模板仍是抽样）。
- 不声明 §5 的节省工时已被实测。
- 不声明 KDS 镜像已同步、其它项目已采纳本注册表。
- 不声明 `bootstrap_entries` 内的 `startlux-decision` 条目已按新 schema 完成改造（其字段与许可仍以原 bootstrap 记录为准）。

### 9.3 回滚

- **撤什么**：删除 `registry.yaml` 中 24 条扩展条目与 4 个新增顶层键（恢复至 37 行 bootstrap 内容）；删除 `tools/kds-sync/validate_asset_registry.py`；删除本报告。
- **保持什么**：`startlux-decision` 条目与同目录 `README.md` 不动（并行会话产物）；失败时状态保持 `repair_required`，不回退已通过的历史证据。
- **不自动做什么**：不自动 `stage` / `commit` / `push` / `delete` / `deploy`，不自动运行 `document_control.py` 或任何会重写台账的命令。
