---
doc_id: GPCF-DOC-PJ12-F017-ATTRIBUTION-20261022
title: PJ-12 KDS F-017 归属纠正与只读检查（2026-10-22）
project: GPCF
related_projects: [SpaceAI, KDS, GPCF]
domain: status
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pj12-f017-attribution-20261022.md
source_path: docs/harness/evidence/pj12-f017-attribution-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PJ-12 KDS F-017 归属纠正与只读检查（2026-10-22）

> 任务：PJ-12（KDS：F-017 归属纠正 + runtime 只读检查）。
> 范围：只改 `features/active/F-017-cwme-city-world-model-engine/feature.yaml` 与本文；
> 不改 `runtime/queue.json`（Orchestrator 职责）；不写真实 KDS API；不 commit/push。
> 非声明：不声明 F-017 关闭、不声明任何状态提升、不声明 KDS 数据被修改。

## 1. 现状（纠正前实测）

| 载体 | 纠正前表述 | 位置 |
|---|---|---|
| `features/active/F-017-cwme-city-world-model-engine/feature.yaml` | `project: kds` | 第 3 行 |
| `runtime/queue.json` | `"project": "kds"`、`status: evaluated`、`current_role: Evaluator` | F-017 条目（第 214 行起） |
| `projects/spaceai/STATUS.md` | 「**当前 Feature**」列 F-017，证据索引指向 `../GlobalCloud SpaceAI/.harness/runs/20261016-080823-spaceai-was-city-flood-replay/evidence-index.yaml` | 第 46 行 |
| `GlobalCloud SpaceAI/README.md` | 「关联 Feature：GPCF F-017（CWME）；Platform 的 F-024 在主目录执行」 | 第 36 行 |
| F-017 证据 JSON（本目录） | `"project_identity": "CWME"`、`"registry_alias": "SpaceAI"`；另一份为 `"project": "SpaceAI"` | `evidence/cwme-city-model-app-20261016.json`、`evidence/was-city-flood-replay-20261016.json` |
| `runtime/state.json` | 无 F-017 条目 | — |

结论：同一 Feature 的载体给出两种归属（`kds` vs SpaceAI），属**账实不符**；
且 F-017 自身证据文件已声明 SpaceAI 别名，仅 `feature.yaml` 与派生 `queue.json` 仍写 kds。

## 2. 证据核验（只读实测）

| 检查 | 方式 | 结果 |
|---|---|---|
| SpaceAI 本地应用存在 | `ls "GlobalCloud SpaceAI/apps/city-model/index.html"` | 存在（1,673,971 B，mtime 2026-10-22 05:09） |
| 内涝切片回放样板存在 | `ls "GlobalCloud SpaceAI/prototypes/was-city-flood/README.md"` | 存在（4,201 B） |
| 运行证据索引存在 | `ls "GlobalCloud SpaceAI/.harness/runs/20261016-080823-spaceai-was-city-flood-replay/evidence-index.yaml"` | 存在（11,403 B）；内容 `project=CWME`、`registry_alias=SpaceAI` |
| F-017 journal 工作位置 | 读 `journal.md` | 2026-10-16 条目：「仅在 SpaceAI 隔离样板目录实现」「应用入口 SpaceAI `apps/city-model/index.html`」 |
| 同仓 Feature 归属一致性 | `features/active/F-024-panorama-engineering-convergence/feature.yaml` | `project: spaceai`（第 3 行） |
| KDS 侧 CWME 本体产物 | `ls "GlobalCloud KDS/世界资产/引擎/ontology/"` | 存在 `cwme-ext.ttl`、`cwme_gen.py`、`ci-gate.sh`、`neo4j/` 等（知识内容） |
| journal 记载路径是否一致 | `ls "GlobalCloud KDS/世界资产/世界模型引擎/ontology"` | **不存在**；现路径为 `世界资产/引擎/ontology/`（路径漂移，KDS 侧待核，不在本任务处置） |
| KDS 项目节奏文件是否列 F-017 | `grep F-017 projects/kds/STATUS.md` | 无命中 |

## 3. 判定

**判定：F-017 的执行项目归属为 SpaceAI（registry slug `spaceai`）；`project: kds` 属立项期记录错误。**

正向依据：

1. SpaceAI 仓 `README.md`（owner 老卢，`status: partial`，2026-10-18）明确写「关联 Feature：GPCF F-017（CWME）」，并说明本目录现用于保存 CWME 本地应用/样板/证据。
2. F-017 的 2026-10-16 工作内容（内涝切片回放、CWME 本地应用）全部在 SpaceAI 仓实现，运行证据索引位于 SpaceAI `.harness/runs/`。
3. F-017 自身证据 JSON 声明 `project_identity=CWME / registry_alias=SpaceAI`（另一份 `project=SpaceAI`）。
4. `projects/spaceai/STATUS.md`（controlled, v1.3, 2026-10-20 复核）把 F-017 列入 SpaceAI「当前 Feature」。
5. 同仓关联 Feature F-024 已登记 `project: spaceai`，同仓归属一致。

反向证据与为何不改变判定：

- KDS 侧 `世界资产/引擎/ontology/` 仍存 B4 本体产物 → 属 KDS **知识空间内容**（知识库主存），是知识资产载体而非执行项目；若把知识库载体当执行项目，会重演同一错位。
- KDS `projects/kds/STATUS.md` 未列 F-017；KDS runtime 开发空间索引 0 条 F-017/CWME 文档（§5）。
- `runtime/queue.json` 与日报仍写 kds，属**待刷新派生数据**（§6），不作为归属依据。

## 4. 改动（仅 feature.yaml）

文件：`features/active/F-017-cwme-city-world-model-engine/feature.yaml`

| 项 | 改前 | 改后 |
|---|---|---|
| 第 3 行 `project` | `kds` | `spaceai` |
| 第 4–12 行 | — | 新增 `attribution_note`（原值 kds、纠正依据、queue.json 未改需 Orchestrator 刷新） |
| `updated_at` | `2026-10-11T07:19:54+00:00` | `2026-10-21T23:24:11+00:00` |

未改动：`status: active`、`loop.current_step: b4_first_month_completed`、`evidence`（tests/build/summary=pass、
screenshots/api=waived）、`acceptance`、`blockers`、`owner`、`priority`；未改 `journal.md`。

补充边界：`runtime/queue.json`、`runtime/state.json` 存在本任务开始前（mtime 2026-10-22 07:19，早于本任务 07:22 开始）的
既有未提交改动，**非本任务产生**；本任务对 `runtime/` 零写入，queue 中 F-017 条目保持 `project: kds` 未变。

验证（只读）：

- PyYAML 解析通过：`project = spaceai`、`attribution_note`（第 4–12 行，624 字符），顶层字段 18 个。
- `PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py`
  → `gpcf_2_feature_workspace=pass feature_delivery_center=true project_scope=28
  new_feature_entry=enabled close_feature_exit=enabled status_promotion_allowed=false`（exit 0）。
- 未运行 `scripts/gpcf_check_evidence.py`：该脚本会重写 feature.yaml/evidence 受管块，超出「只做归属纠正」范围。

## 5. KDS runtime 索引只读检查（2026-10-22 07:25:02–07:25:03 +0800）

原则：只做 `GET`（health / documents 索引），**无 POST/PUT/DELETE**，未改 KDS 数据。
凭据经 `~/.globalcloud/kds.env` 加载（文件权限 600），token 只记录指纹、不记录明文。

| 检查 | 结果 |
|---|---|
| `GET {KDS_API_BASE_URL}/api/v1/health` | **HTTP 200**，`{"ok": true, "status": "healthy", "version": "1.1.0", "total_pages": 3324}`，62 ms |
| `GET /spaces/开发/documents`（只读索引） | **HTTP 200**，1197 文档，786 ms |
| 开发空间 `91-治理与验收/` 前缀 | 71 条 |
| 开发空间 `91-治理与验收/features/active/` | **0 条** |
| 开发空间 F-017 / CWME 命中 | **0 条** |
| 其它知识空间只读探测（世界资产 / 智慧城市 / 工业绿链） | **HTTP 403 Forbidden**（token 仅授权开发空间；未越权、未重试） |
| token 配置 | fingerprint=`bfd9553d`，owner=`lujunxiang`，space=`开发`，base=`http://127.0.0.1:18080`（本机，非公网） |
| 本地镜像 | `.kds/development-space/开发/91-治理与验收/features/active/F-017-cwme-city-world-model-engine/` 存在 `journal.md`、`summary.md`；`09-status/kds-development-space-sync-register.md` 第 3215–3216 行状态 `pending_api` |

解读（不越权推断）：

- 开发空间运行索引中无 F-017 文档 → 「F-017 属 KDS 执行项目」在 KDS runtime 侧**没有索引支撑**；
  本任务未据此做任何删除/迁移。
- 知识空间返回 403，未读取 → **不能**断言 KDS 知识空间无 CWME 内容；限制如实记录。
- `total_pages=3324` 与开发空间索引 `1197` 口径不同（前者跨空间总页数），未进一步核实。

## 6. 待刷新项（本任务不改，属 Orchestrator / 其它任务职责）

| # | 载体 | 现状 | 责任方与动作 |
|---|---|---|---|
| 1 | `runtime/queue.json` F-017 条目 | `"project": "kds"`（第 214 行起） | **Orchestrator**：刷新为 `spaceai`；本任务按指令未改 queue.json |
| 2 | `runtime/audit/daily-status-20261022.jsonl` | `kds.active_features=1`（F-017）、`spaceai.active_features=1`（F-024），生成于 2026-10-22T06:39:40+08:00 | 日巡检脚本下次运行自动更正；更正前日报口径为旧值 |
| 3 | 派生账本 | `09-status/globalcloud-project-group-completion-baseline-v1.0.md` 与 `runtime/vu-ledger.yaml` 仍写「F-017 登记在 kds 名下、证据在 SpaceAI 仓，账实不符」 | PG-02 owner 复核；纠正后该描述过时 |
| 4 | KDS 同步登记 | `09-status/kds-development-space-sync-register.md` 第 3215–3216 行的 kds_path 是「GPCF→KDS 文档同步路径」 | 无需改动（登记文档路径，非项目字段） |
| 5 | Feature 计数口径 | 刷新后 KDS active Feature 1→0，SpaceAI 1→2（F-017 + F-024） | Orchestrator / PG-10 口径同步；**不构成状态提升** |

## 7. 非声明

1. 不声明 F-017 已完成或关闭：`status: active`、`current_step`、`evidence` 五项原值均未改。
2. 不声明任何状态提升（`accepted` / `integrated` / `production_ready` / `customer_accepted` 一律未声明）。
3. 不声明 KDS 数据被修改：只做 GET health/index，无写调用；403 空间未越权。
4. 不声明 `runtime/queue.json` 已更正：queue 仍为 `kds`，待 Orchestrator 刷新。
5. 不声明 KDS 知识空间无 CWME 内容（403 无法读取，未据此推断）。
6. 不声明 journal 记载的 `世界资产/世界模型引擎/ontology/` 已核实——实际为 `世界资产/引擎/ontology/`，路径漂移属 KDS 侧待核。

## 8. 复核命令

```bash
cd "GlobalCloud GPCF"
grep -n "^project:" features/active/F-017-cwme-city-world-model-engine/feature.yaml          # → 3:project: spaceai
grep -n "attribution_note" features/active/F-017-cwme-city-world-model-engine/feature.yaml   # → 第 4 行
python3 -c "import json;q=json.load(open('runtime/queue.json'));print([f for f in q['queue'] if f['id']=='F-017'])"
# → 仍为 project kds（待 Orchestrator 刷新，属预期）
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py     # → pass
# KDS 只读（GET only）
python3 - <<'EOF'
import sys, os, urllib.request
sys.path.insert(0, 'tools/kds-sync')
import kds_runtime as kr
kr.load_env_file()
print(urllib.request.urlopen(os.environ['KDS_API_BASE_URL'] + '/api/v1/health', timeout=10).read().decode())
EOF
```

## 9. 结论

- F-017 执行项目归属由 `kds` 纠正为 `spaceai`，仅改 `feature.yaml` 并附 `attribution_note`；其余载体入 §6 待刷新。
- KDS runtime 只读检查可执行：health 200 / 开发空间索引 1197 文档，F-017 在开发空间索引为 0 条；知识空间 403 受限如实记录。
- 本任务零删除、零移动、零 commit/push、零真实 KDS 写操作。
