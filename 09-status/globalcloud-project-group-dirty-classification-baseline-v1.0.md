---
doc_id: GPCF-DOC-F8471AE0DA
title: GlobalCloud 项目群 dirty 分类基线 v1.0（PG-04 自指 dirty 治理·分类部分）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP, PQC, SpaceAI, SpaceAIStudio, World, GCMEM, WAE, Project, PDC, SLC, DRC]
domain: status
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-group-dirty-classification-baseline-v1.0.md
source_path: 09-status/globalcloud-project-group-dirty-classification-baseline-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 dirty 分类基线 v1.0

> **任务包**：PG-04 自指 dirty 治理（分类基线部分）。
> **数据来源**：本机 2026-10-22T05:39:03+08:00 – 2026-10-22T05:39:05+08:00 的实测输出，全部由
> `tools/kds-sync/classify_dirty_paths.py v1.0` 生成并原样粘贴（脚本 JSON 为数值源，
> `--text`/`--markdown` 原文见 §2–§4）；本文所有数字均来自脚本输出或由脚本输出直接相加/相除，
> **无手写估值**，也不引用历史文档中的 dirty 数字作为本次事实（历史值仅 §1.3 作对照）。
> **状态**：`draft`——待人工确认后转 `controlled`。

---

## 0. 一句话结论

28 个仓共 **608 条**未提交变更，其中 **governance 357 条（58.7%）**；
把其中 **机制自动产物 276 条（45.4%）** 与 noise 31 条移出被审面后，
Git gate 可枚举的变更集为 **301 条（49.5%）**。
即：**「门禁恒 dirty」的主因不是产品代码未交付，而是治理机器自己在写被审工作树**；
dirty 总数是治理活动的函数，不能当作静态基线或归零目标。

被审面（需 review）为 **301 条** = product 218 + governance/controlled 81
+ sensitive 2（218 + 81 + 2 = 301，
与 608 − 276 − 31 = 301 一致）。

---

## 1. 采集口径

### 1.1 采集时点与命令原文（脚本 stdout 原文）

```text
==============================================================================
PG-04 项目群 dirty 路径分类  classify_dirty_paths.py v1.0
==============================================================================
采集时点      : 2026-10-22T05:39:03+08:00
工作区根      : /Users/lujunxiang/Projects/GlobalCloud V0.0.1
config        : /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/config/project-group-projects.yaml
命令模板      : git --no-optional-locks -c core.quotePath=false -C <repo> status --porcelain -uall
仓覆盖        : 28/28 个仓读取成功（失败 0）
dirty 汇总    : 608 条 / dirty 仓 23 个 / clean 仓 5 个
```

- 采集窗口：`2026-10-22T05:39:03+08:00` – `2026-10-22T05:39:05+08:00`（三次渲染模式在同一窗口内完成并已核对 digest 一致，尝试 2 次）。
- 脚本：`GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py`（`v1.0`，仅 Python 3 标准库）。
- 对 config 中 28 个仓逐一执行上面的命令；解析 `XY path`，rename/copy 取 new 路径。
- 结果指纹：`digest = e769dcb03e805a269b8ad8b587a2d1e3d0168316268bfce3918f9e8681760937`（同一工作树状态下重复运行逐字节一致，见 §8.2）。
- 只读性：脚本不写任何文件、不删除、不移动、不 stage/commit/push；本次执行零删除。

### 1.2 覆盖与分类口径

- 覆盖：28/28 仓读取成功（失败 0）；dirty 23 仓 / clean 5 仓。
- 五类语义（优先级 `sensitive > noise > governance > product > unknown`）：

| 分类 | 语义 | 是否进入被审 review |
|---|---|---|
| `governance` | 治理机制产物与受控治理文档。再分 `mechanical`（机制自动产出：`.harness/`、`.kds/`、`runtime/`、`features/*/evidence|artifacts`、`99_Reports/`、`.okf/`、`_meta/` 等）与 `controlled`（受控方案、`01-architecture/`、`projects/*/`、`09-status/`、`features/*/feature.yaml|journal.md`、`review/`） | `controlled` 需 review；`mechanical` 不应进入被审面 |
| `product` | 产品/工程代码、测试、契约、交付文档与业务知识内容 | 需 review（PG-16 文档债的处置对象） |
| `noise` | 本机构建/编辑/系统垃圾（`.DS_Store`、`__pycache__`、`*.log`、`.scratch/`、临时备份等） | 不需 review |
| `sensitive` | 凭据/密钥类命名（`.env*`、`*.pem`、`*.key`、`*token*`、`*secret*` 等） | 必须转人工安全复核，不做代码 review |
| `unknown` | 规则未覆盖的残余（本次为 0） | 待定 |

- 规则可扩展：全部规则写在脚本常量区（`GOVERNANCE_*` / `PRODUCT_*` / `NOISE_*` / `SENSITIVE_*`），
  并随 `--json` 的 `rules` 字段输出，便于评审与后续版本比对。

### 1.3 与 `runtime/plan-20261022/constraints.md` §c-1 的对照（差异即实测漂移）

| 口径 | constraints.md（2026-10-22T05:15） | 本次实测（2026-10-22T05:39:03+08:00 起） | 差异 |
|---|---:|---:|---|
| dirty 总数 | 575（按 §c-1 表内 22 仓相加；原文未给总数） | **608** | +33 |
| dirty 仓数 | 22 | **23** | +1 |
| `GlobalCoud GPCF` | 243 | **254** | +11 |
| `GlobalCloud Mem` | 19 | **38** | +19 |
| `GlobalCloud PMC` | 0（clean） | **7** | +7（由 clean 变 dirty） |
| `GlobalCloud SpaceAI Platform` | 11 | **6** | -5（未核实原因） |
| `GlobalCloud World` | 0（未列） | **1** | +1 |
| 其余 20 仓 | 见 §c-1 | 见 §3 | 逐仓持平 |

差异原因：采集窗口内本机仍有并行任务在写各仓工作树（本文件自身落盘也是其中一条，见 §6.3），
且本分类脚本自身也在 `tools/kds-sync/` 新增 1 条；未逐条追溯每个增量。
**结论不变**：dirty 总数随治理活动持续增长，因此本基线以「分类占比 + digest」而非
「dirty 整数」作为可复现指标。

---

## 2. 28 仓汇总（`--markdown` 输出原文，未改动任何数字）

**全局**：28/28 仓读取成功；dirty 共 **608** 条，分布 23 个仓，clean 5 个仓。

| 分类 | 条数 | 占比 |
|---|---:|---:|
| `governance` | 357 | 58.7% |
| `product` | 218 | 35.9% |
| `noise` | 31 | 5.1% |
| `sensitive` | 2 | 0.3% |
| `unknown` | 0 | 0.0% |
| ├─ `governance/mechanical` | 276 | 45.4% |
| └─ `governance/controlled` | 81 | 13.3% |

**移出被审面后**（剔除 `governance/mechanical` + `noise`）Git gate 可枚举变更集：**301** 条（49.5%）。

### 2.1 gitignore / 迁移只读模拟（脚本原文）

| 口径 | 条数 |
|---|---:|
| 当前 dirty 总数 | 608 |
| governance/mechanical 未跟踪（`.gitignore` 可直接隐藏） | 183 |
| governance/mechanical 已跟踪（需目录移出或 `git rm --cached`） | 93 |
| noise 未跟踪 / 已跟踪 | 27 / 4 |
| 仅新增 `.gitignore` 后 git gate 可见 | 398 |
| 迁移（目录移出 / `git rm --cached` + ignore）后 git gate 可见 | 301 |

> 只读模拟说明：`.gitignore` 只影响**未跟踪**文件；已跟踪文件的修改（`M`）不受 ignore
> 影响，必须靠目录移出或 `git rm --cached` 处理。因此「仅加 `.gitignore`」只能把
> 608 降到 398，把治理产物真正移出被审面后才降到 301。
> 迁移动作本次**未执行**。

## 3. 逐仓分类表（脚本原文）

### 逐仓分类表

| # | 项目 | 仓目录 | dirty | governance | ├ mechanical | └ controlled | product | noise | sensitive | unknown | governance 占比 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | GPCF | `GlobalCoud GPCF` | 254 | 214 | 162 | 52 | 39 | 1 | 0 | 0 | 84.3% |
| 2 | XiaoC | `GlobalCloud XiaoC` | 115 | 92 | 90 | 2 | 21 | 0 | 2 | 0 | 80.0% |
| 3 | KDS | `GlobalCloud KDS` | 80 | 24 | 22 | 2 | 52 | 4 | 0 | 0 | 30.0% |
| 4 | PVAOS | `GlobalCloud PVAOS` | 43 | 7 | 2 | 5 | 36 | 0 | 0 | 0 | 16.3% |
| 5 | GCMEM | `GlobalCloud Mem` | 38 | 1 | 0 | 1 | 13 | 24 | 0 | 0 | 2.6% |
| 6 | AAAS | `GlobalCloud AAAS` | 16 | 4 | 0 | 4 | 11 | 1 | 0 | 0 | 25.0% |
| 7 | SOP | `GlobalCloud SOP` | 15 | 2 | 0 | 2 | 13 | 0 | 0 | 0 | 13.3% |
| 8 | WAE | `GlobalCloud WAE` | 11 | 0 | 0 | 0 | 11 | 0 | 0 | 0 | 0.0% |
| 9 | PQC | `GlobalCloud PQC` | 8 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0.0% |
| 10 | Project | `GlobalCloud PMC` | 7 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0.0% |
| 11 | SpaceAI | `GlobalCloud SpaceAI Platform` | 6 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0.0% |
| 12 | PDC | `GlobalCloud PDC` | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 100.0% |
| 13 | WAS | `WAS世界资产体系` | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0.0% |
| 14 | Brain | `GlobalCloud Brain` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 15 | GFIS | `GlobalCloud GFIS` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 16 | GPC | `GlobalCloud GPC` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 17 | ICP | `GlobalCloud ICP` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 18 | MMC | `GlobalCloud MMC` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 19 | PKC | `GlobalCloud PKC` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 20 | Studio | `GlobalCloud Studio` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 21 | World | `GlobalCloud World` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 22 | XWAIL | `GlobalCloud XWAIL` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 23 | XiaoG | `GlobalCloud XiaoG` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 100.0% |
| 24 | DRC | `GlobalCloud DRC` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% |
| 25 | SLC | `GlobalCloud SLC` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% |
| 26 | SpaceAIStudio | `GlobalCloud SpaceAI Studio` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% |
| 27 | WAME | `GlobalCloud WAME` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% |
| 28 | XGD | `GlobalCloud XGD` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% |

## 4. Top 20 路径（按目录聚合，脚本原文）

### Top 20 目录聚合

| 目录 | 条数 | governance | product | noise | sensitive | unknown |
|---|---:|---:|---:|---:|---:|---:|
| `.harness/evidence/` | 90 | 89 | 0 | 0 | 1 | 0 |
| `.harness/runs/` | 53 | 53 | 0 | 0 | 0 | 0 |
| `.kds/development-space/` | 48 | 48 | 0 | 0 | 0 | 0 |
| `features/active/` | 43 | 43 | 0 | 0 | 0 | 0 |
| `(仓根)` | 41 | 28 | 10 | 2 | 1 | 0 |
| `docs/current/` | 32 | 0 | 32 | 0 | 0 | 0 |
| `.scratch/backfill-2026-10/` | 24 | 0 | 0 | 24 | 0 | 0 |
| `scripts/` | 17 | 0 | 17 | 0 | 0 | 0 |
| `工业绿链/图谱/` | 15 | 0 | 15 | 0 | 0 | 0 |
| `99_Reports/` | 13 | 12 | 0 | 1 | 0 | 0 |
| `tools/kds-sync/` | 13 | 0 | 13 | 0 | 0 | 0 |
| `docs/` | 12 | 0 | 12 | 0 | 0 | 0 |
| `features/done/` | 12 | 12 | 0 | 0 | 0 | 0 |
| `openspec/changes/` | 11 | 0 | 11 | 0 | 0 | 0 |
| `09-status/` | 10 | 10 | 0 | 0 | 0 | 0 |
| `PVA价值联盟/业务系统/` | 10 | 0 | 10 | 0 | 0 | 0 |
| `packages/mcp-server/` | 8 | 0 | 8 | 0 | 0 | 0 |
| `tests/` | 8 | 0 | 8 | 0 | 0 | 0 |
| `体系/AaaS架构_20261017/` | 8 | 0 | 8 | 0 | 0 | 0 |
| `research/` | 6 | 0 | 6 | 0 | 0 | 0 |

读取要点（数字均为上表相加/相除，非估计）：

1. 前 4 名全部是治理机制目录：`.harness/evidence/` 90 + `.harness/runs/` 53 + `.kds/development-space/` 48 + `features/active/` 43 = **234 条**，
   占全局 608 的 38.5%。
2. product 侧主要来源：`docs/current/` 32、`scripts/` 17、`工业绿链/图谱/` 15、`tools/kds-sync/` 13、`docs/` 12、`openspec/changes/` 11、`PVA价值联盟/业务系统/` 10、`packages/mcp-server/` 8、`tests/` 8、`体系/AaaS架构_20261017/` 8
   —— 工程脚本、交付文档与变更提案，属应 review 的被审面。
3. KDS 中文业务知识目录合计 51 条（本表可见 33 条，其余在 Top 20 之外），属交付物，**不应**列入 `.gitignore`。
4. `(仓根)`（如存在）混合受控方案文档、仓级工程配置与 `.DS_Store`/`.env.bak*` 三类，
   单一 `.gitignore` 规则无法处理，需按仓逐条处置。

## 5. 三个典型仓（`--per-repo-top 6` 输出原文）

```text
[GPCF] GlobalCoud GPCF  dirty=254
        53  .harness/runs/                           governance=53
        48  .kds/development-space/                  governance=48
        43  features/active/                         governance=43
        13  tools/kds-sync/                          product=13
        12  features/done/                           governance=12
        11  openspec/changes/                        product=11
[XiaoC] GlobalCloud XiaoC  dirty=115
        90  .harness/evidence/                       governance=89 sensitive=1
         8  packages/mcp-server/                     product=8
         7  (仓根)                                     governance=2 product=4 sensitive=1
         2  docker/                                  product=2
         2  docs/user/                               product=2
         1  docs/                                    product=1
[KDS] GlobalCloud KDS  dirty=80
        15  工业绿链/图谱/                                 product=15
        13  99_Reports/                              governance=12 noise=1
        10  PVA价值联盟/业务系统/                            product=10
         8  体系/AaaS架构_20261017/                      product=8
         5  体系/                                      product=5
         5  智慧城市/报告/                                 product=5
```

### 5.1 `GlobalCoud GPCF`（254 条，governance 84.3%）

治理中枢仓是最大污染源：本仓 `.harness/runs/` 53 条 +
`.kds/development-space/` 48 条 +
`features/active/` 43 条 = 144 条，
全部是 harness 运行记录、KDS 镜像与 Feature 证据/产物，属机制自动产物；
`governance/controlled` 52 条（`01-architecture/`、`projects/*/`、
`09-status/`、仓根方案与 `features/*/feature.yaml|journal.md`）应入库并 review；
product 39 条中 `tools/kds-sync/`、`scripts/`、`openspec/changes/`、
`tests/` 为工程代码与变更提案——这些才是需要 review 的变更。

### 5.2 `GlobalCloud XiaoC`（115 条，governance 80.0%）

115 条中 governance 92 条，其中 90 条集中在 `.harness/evidence/`（harness 证据快照）；
product 21 条在 `packages/mcp-server/`、`scripts/`、`docs/`，是真实代码/文档变更。
另有 2 条 sensitive：`.env.bak-20261020-hermes-key`、`.harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-audit.jsonl`——
**本次未读取其内容**，只按命名归类，必须转人工安全复核（凭据备份文件原则上应删除而非入库，
处置不在本任务范围）。

### 5.3 `GlobalCloud KDS`（80 条，governance 30.0%）

与 GPCF/XiaoC 相反：KDS 的 dirty 以**业务知识内容**为主（中文业务目录 51 条，属 product）
与 `99_Reports/` 巡检报告 13 条（12 governance
+ 1 noise）。这说明「治理产物占比」不是全局常数：
KDS 的问题是把知识库内容与生成报告混在同一被审工作树里；`.gitignore` 只应覆盖
`99_Reports/` 等生成物，业务知识目录必须入库。

---

## 6. 结论

### 6.1 治理产物占比

- `governance` **357/608 = 58.7%**，其中
  `mechanical` **276/608 = 45.4%**、`controlled` 81/608 = 13.3%。
- 口径敏感性：若只把「机制自动产物」视为应移出的治理产物，占比为 **45.4%**；
  若把受控治理文档也算作治理产物总量，占比为 **58.7%**。
  本基线同时给出两个口径，不合并成单一数字。
- 按治理产物**条数**的 Top 3 仓：GPCF 214 + XiaoC 92 + KDS 24 =
  330 条，占全部治理产物 357 条的 **92.4%**；治理优先级应集中在这 3 个仓。
- 按 governance 占比（dirty ≥ 10 的仓）：
  GPCF 84.3% > XiaoC 80.0% > KDS 30.0% > AAAS 25.0%。

### 6.2 移出被审面后的 Git gate 可枚举变更集

- 现状 608 条；仅加 `.gitignore`：**398 条**；
  治理产物目录移出 / `git rm --cached` 后：**301 条（49.5%）**。
- 301 = product 218 + governance/controlled 81 + sensitive 2（校验一致）。
- 因此 PG-04 的可量化目标应表述为：**把 gate 分母从 608 降到 301 并固定分类口径**，
  而不是「dirty 归零」。

### 6.3 自指证据（本任务自身的观测）

- 本分类脚本与本文档本身都落在被审工作树内：脚本 `tools/kds-sync/classify_dirty_paths.py`
  使 GPCF 新增 1 条 product，本文档落盘使 GPCF 新增 1 条 governance/controlled。
- 采集窗口内 GPCF 已因并行任务从 250（05:32 试跑）涨到 254（2026-10-22T05:39:03+08:00），PMC 从 0 涨到 7；
  本文档自身已作为 1 条 untracked（governance/controlled）计入本次快照；若继续有并行写入，
  复跑会得到更高的 dirty 数——这是自指闭环的预期表现，不是分类错误。
- 结论：在治理活动持续写工作树的前提下，dirty 归零不可达；「先冻结分母口径（PG-01）→
  再移出治理产物（本任务建议）→ 最后才谈 gate 通过（PG-08）」是唯一可收敛顺序。

### 6.4 风险登记（本次不处置）

| 风险 | 证据 | 影响 |
|---|---|---|
| 2 条 sensitive 未处置 | XiaoC: `.env.bak-20261020-hermes-key`、XiaoC: `.harness/evidence/xiaoc-mcp-skill-20261020/37-caller-token-audit.jsonl` | 凭据备份/审计文件仍在工作树，需人工安全复核 |
| 2 条 `D`（删除） | PVAOS: `GlobalCloud PVAOS 实施方案.md`、PVAOS: `GlobalCloud PVAOS 总体方案.md` | 受控方案文档在工作树中被删，需项目侧确认是否误删 |
| 已跟踪 mechanical 93 条 | §2.1 | 单靠 `.gitignore` 无效，必须迁移或 `git rm --cached` |

---

## 7. `.gitignore` 建议清单（只建议，不应用）

### 7.1 按仓/按目录建议

| 范围 | 建议规则 | 依据（本次实测） |
|---|---|---|
| 全部 28 仓 | `__pycache__/`、`*.pyc`、`.DS_Store`、`*.log`、`.scratch/`、`node_modules/`、`.turbo/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/`、`*.bak-*`、`*.orig`、`*.rej`、`*~` | noise 31 条；`.DS_Store` 在 AAAS/WAS 已是**被跟踪**文件，ignore 后仍需 `git rm --cached` |
| `GlobalCoud GPCF` | `.harness/runs/`、`.kds/`、`runtime/logs/`、`features/*/evidence/`、`features/*/artifacts/`、`.okf/bundles/` | 本仓 `.harness/runs/` 53、`.kds/development-space/` 48、`features/active/` 43（含 evidence/artifacts） |
| `GlobalCloud XiaoC` | `.harness/evidence/`（或整 `.harness/`） | 115 条中 governance 92 条，其中 `.harness/evidence/` 下 89 条为 mechanical 证据 |
| `GlobalCloud KDS` | `99_Reports/` 下生成报告（如 `daily-mining-*.md`） | `99_Reports/` 13 条中 12 条 governance；**业务知识目录不得 ignore** |
| `GlobalCloud Mem` (GCMEM) | `.scratch/` | 38 条中 24 条 noise，集中于 `.scratch/backfill-2026-10/` |
| 其余 25 仓 | 先只加通用噪声规则；治理产物按 §7.3 迁移 | 逐仓 dirty ≤ 43 条，单仓 mechanical ≤ 2 条 |

### 7.2 明确不建议 ignore 的部分

- `governance/controlled` 81 条：`01-architecture/`、`projects/*/`、`09-status/`、`review/`、
  仓根 `*总体方案*.md` / `*实施方案*.md` / `AGENTS.md`、`features/*/feature.yaml|journal.md`
  —— 受控治理文档，应入库并 review。
- KDS 中文业务知识目录 51 条、PVAOS `docs/current/` 32 条等 product 交付文档
  —— 属被审交付面。
- `openspec/changes/` 变更提案与 `research/` 调研产物 —— 属交付内容，不是机制产物。

### 7.3 迁移 dry-run 影响面（只描述，不执行）

| 步骤 | 动作 | 预期结果 | 风险 |
|---|---|---|---|
| 1 | 各仓仅追加 §7.1 的 `.gitignore` | gate 可见 608 → 398（隐藏 210 条未跟踪项） | 已跟踪 mechanical 93 条 + noise 已跟踪 4 条仍在，gate 仍不干净 |
| 2 | 对已跟踪 mechanical 执行 `git rm --cached`（保留本地文件） | 93 条从索引移除，需一次受控 commit | 改写索引；需先冻结 GPCF `behind 128` 的同步问题，否则提交基线与远端不一致 |
| 3 | 治理产物目录迁出被审树（Evidence 落点到独立证据仓/运行宿主，PG-11） | gate 可见 → 301 条 | 涉及跨仓目录迁移与引用改链，须单独授权 |
| 4 | 处置 2 条 sensitive（人工安全复核） | 301 → 299 条 | 凭据类处置必须人工确认 |
| 5 | 冻结分母口径（分类后 301）+ 分类脚本进 CI | gate 首次可稳定判定 | 需 PG-01 口径冻结与 PG-08 远端 CI 配合 |

**本次未执行任何一步**：未改 `.gitignore`、未 `git rm --cached`、未迁移目录、未提交。

---

## 8. 复跑与自检

### 8.1 复跑命令

```bash
# 默认：全局统计 + 逐仓表 + Top20 目录
python3 "GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py"
# 文档表格 / 机器可读 / 小样 / 逐仓明细
python3 "GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py" --markdown --top 20
python3 "GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py" --json
python3 "GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py" --only GPCF,XiaoC,KDS
python3 "GlobalCoud GPCF/tools/kds-sync/classify_dirty_paths.py" --per-repo-top 6 --only GPCF,XiaoC,KDS
```

### 8.2 自检结论

| 检查项 | 结果 |
|---|---|
| 28 仓覆盖 | 28/28 读取成功，失败 0 |
| 分类完整性 | 五类之和 357+218+31+2+0 = 608 = dirty 总数 608，unknown = 0 |
| 二次运行一致性 | `--no-timestamp --json` 连续两次输出逐字节一致（`cmp`/`md5` 相同） |
| 零删除/零移动 | 脚本无删除、无移动、无 `git add/commit/push`；本次仅新建 2 个文件 |
| 脚本副作用 | 不写任何文件（`--json/--markdown/--text` 仅 stdout）；执行后未产生额外工作树文件 |
| digest | `e769dcb03e805a269b8ad8b587a2d1e3d0168316268bfce3918f9e8681760937`（同状态重跑一致；工作树变动则随之变化） |
| 采集窗口一致性 | 三种渲染模式在同一窗口 2026-10-22T05:39:03+08:00 – 2026-10-22T05:39:05+08:00 内 digest 一致（尝试 2 次），非跨时点拼接 |

> 注意：本文档自身已作为 1 条 untracked（governance/controlled）计入本次快照；其后若还有
> 并行任务写入工作树，复跑会得到更大的 dirty 数——这是自指闭环的预期表现，不是分类错误。
> 基线以本文记录的时刻与 `digest` 为准。

---

## 9. 不声明事项

1. 不声明 dirty 已清零、不声明 gate 已通过；只提供分类基线与迁移影响面测算。
2. 不声明 `.gitignore` 已应用、不声明迁移已执行、不声明已 `git rm --cached`。
3. 不声明 2 条 sensitive 已处置或已确认安全（未读取内容）。
4. 不把「product 218 条」等同于「待交付完成」——它只表示该部分落在被审产品面，仍需逐条 review。
5. 不把 `constraints.md` §c-1 的历史数字当成本次事实；§1.3 中的历史值仅作对照。
6. 不声明任何项目状态提升（`accepted` / `integrated` / `production_ready` / `customer_accepted`）。
