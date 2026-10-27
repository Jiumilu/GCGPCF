---
doc_id: GPCF-DOC-LOOP-SLIMMING-SCOPE-20261027
title: loop 治理收敛范围与判据
project: GPCF
related_projects: [GPCF, WAME, KDS, GFIS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/governance/loop-治理收敛范围与判据.md
source_path: docs/governance/loop-治理收敛范围与判据.md
sync_direction: bidirectional
last_reviewed: 2026-10-27
supersedes: []
superseded_by: []
---

# loop 治理收敛范围与判据

F-004 loop-governance-slimming（PMC #255）第一批可核物。本页只回答三件事：**收敛什么、不收敛什么、怎么算收敛**。

本页不含任何已执行的删除、归档或改档动作；所有「建议」在裁定前均为待议。

## 0. 本页不是什么

1. 不是归档执行单：没有一篇文档、没有一个校验器因本页被改档或删除。
2. 不是架构裁定：L1–L7 分层与宪法条文不在本页范围（架构师裁定）。
3. 不是跨仓授权：34 篇 loop 正文里 32 篇属主为 WAME，本页只列事实与建议，不构成处置。

## 1. 基线（HEAD c7f8204e4，2026-10-27 20:53）

| 项 | 当前值 |
|---|---|
| `02-governance/loop/` 入库 Markdown | 36 个（34 篇正文 + 2 个 README），正文合计 5535 行 |
| 34 篇正文属主 | GPCF 2 篇 / WAME 32 篇 |
| 硬编码引用 loop 文档路径的 `.py` 脚本 | 55 个 |
| 其中被 CI 真门禁执行（`.github/workflows/*.yml`） | 2 个 |
| 其中被手动入口执行（`scripts/gpcf_full_sweep.py`、`tools/kds-sync/run_frontmatter_pipeline.sh`、`tests/`） | 4 个 |
| 其中无任何入库入口 | 49 个 |
| 文档维度：被上述入口实际读取 | 18 篇 |
| 文档维度：仅被无入口脚本或清单页引用 | 16 篇 |

复跑命令（只读，不改仓）：

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPCF"
python3 - <<'PY'
import subprocess,os,re
from collections import Counter
def tracked(p="."):
    return subprocess.run(["git","-c","core.quotepath=false","ls-files",p],
                          capture_output=True,text=True).stdout.splitlines()
def rd(p):
    try: return open(p,encoding="utf-8",errors="ignore").read()
    except Exception: return ""
allf=tracked()
ci="".join(rd(p) for p in allf if p.startswith(".github/workflows/"))
T1=set(re.findall(r'tools/kds-sync/[A-Za-z0-9_]+\.py',ci))
manual=[p for p in allf if p in ("scripts/gpcf_full_sweep.py",
        "tools/kds-sync/run_frontmatter_pipeline.sh","scripts/gpcf_check_evidence.py",
        "scripts/console_export.py") or p.startswith("tests/")]
T2=set()
for p in manual:
    for x in re.findall(r'validate_[a-z0-9_]+\.py',rd(p)): T2.add("tools/kds-sync/"+x)
ref={p for p in allf if p.endswith(".py") and "/.okf/" not in p
     and not p.startswith((".kds/","features/","openspec/")) and "02-governance/loop/" in rd(p)}
tier=lambda p:"T1" if p in T1 else ("T2" if p in T2 else "T3")
print("引用脚本:",len(ref),dict(Counter(tier(p) for p in ref)))
md=[p for p in tracked("02-governance/loop") if p.endswith(".md") and not p.endswith("/README.md")]
live=[p for p in md if any(tier(q) in ("T1","T2") and ("02-governance/loop/"+os.path.basename(p)) in rd(q) for q in ref)]
print("正文:",len(md),"被T1/T2读取:",len(live),"孤儿:",len(md)-len(live))
PY
```

**反面检验**：这份表在收敛没做之前也是这个数，所以它本身不能证明收敛完成——它只定义起点。

### 1.1 立论：为什么「CI 绿」不能当收敛判据

真门禁（CI）只读取 55 个引用脚本中的 2 个，另有 4 个只在手动入口里跑、49 个没有任何入口。于是出现两个方向同时失效：

- **删多了不会变红**：把一篇只被 T3 脚本引用的文档归档，CI 照样全绿——闸口已经被拆，红灯不会亮。
- **删对了也不会变绿**：治理面从 34 篇降到 20 篇，CI 状态与今天完全一致。

一条判据若在「收敛完成」与「一行没动」两种情况下输出相同，它就不是判据（判据自匹配之外的第二类假判据：与被证明对象不相关）。所以本页用 J1–J4 的**计数**判收敛，CI 只用于证明「没把在用的东西弄坏」，两者分工不重叠。

## 2. 收敛什么（范围内）

- **R1 入口登记**：34 篇正文 + 55 个引用脚本，每一件必须落到 `T1 真门禁` / `T2 手动入口` / `P2 仅审计` / `归档建议` 四类之一，不允许「没人知道它归哪」。
- **R2 无入口产物降级**：49 个无入口脚本、16 篇孤儿文档，先标 `P2 仅审计`（显式声明「不阻断交付」），再决定归档或保留。
- **R3 「暂停新增」立观测**：F-004 基线（`LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md` 冻结规则 1/2）规定暂停新增治理文档与非 P0 校验器，而 2026-10-27 前**没有任何机制观测这条规则**；10-27 当天仍有批量入库（`726e923be`「C 段入库 4/4 治理类 62 项（G-14）」，新增文件 31 个，其中 `.md` 23 个）。规则没有观测手段，就等于没有规则。**本页已把它落地为 J3 观测器**，首次观测见 §4。
- **R4 挂账口径一致**：仓内 `features/done/F-004-loop-governance-slimming/` 已判关闭、PMC #255 仍开放。Chief 2026-10-27 裁定以仓内 `feature.yaml` 为准、PMC 为投影：首轮 done = 首轮收敛完成，自本页起为**第二轮**（见 `feature.yaml` 的 `second_round` 段）。

## 3. 不收敛什么（范围外）

- **N1 他仓属主文档**：32 篇属主是 WAME。跨仓处置须 WAME 属主同意 + Chief 书面，GPCF 单方不动。
- **N2 分层与宪法**：L1–L7 架构分层、宪法条文属架构师裁定，本页不涉及。
- **N3 现存真闸口**：被 `T1`/`T2` 实际读取的 18 篇文档与 6 个脚本不得进归档候选。误删的后果不是 CI 变红，而是闸口静默消失——因为 4 个 T2 脚本本就是手动跑。
- **N4 受控文档不得删除**：`status: controlled` 文档一律走「归档 + 替代关系」，不删文件（`02-governance/loop/README.md` 受控规则）。
- **N5 证据与状态边界**：不触碰真实业务证据、状态提升、生产动作。

## 4. 怎么算收敛（判据）

| 编号 | 判据 | 通过条件 | 反面检验（反面情况下该判据会不会保持不变） |
|---|---|---|---|
| J1 | 四分类覆盖率 | 34 篇 + 55 脚本全部有类，未分类数 = 0 | 会变：新增一篇未分类文档，未分类数立刻 +1 |
| J2 | 误伤为零 | 「归档建议」集合 ∩ 「T1/T2 读取」集合 = 空 | 会变：把 `LOOP_RISK_GATE` 放进归档建议，交集立即非空 |
| J3 | 暂停新增可观测 | **J3-a（判据）**：`02-governance/loop/` 连续 2 个完整自然月新增 `.md` 篇数 = 0；**J3-b（仅观测，不作判据）**：净增行数 | 会变：只要当月新增 1 篇，J3-a 立刻从成立变不成立 |
| J4 | 挂账口径一致 | `features/done/F-004-loop-governance-slimming/feature.yaml` 为**唯一状态源**，PMC #255 为投影（Chief 2026-10-27 裁定） | 会变：feature.yaml 的 `second_round.status` 改一次，口径就变一次 |
| J5 | 搬迁类改动无旧路径残留 | 可执行代码（`.py`/`.sh`/`.bash`）中旧路径常量命中 = 0；数据/证据/记录文件出现旧路径时，须同文件写明新路径（迁移留痕）；`.md` 不在判据范围 | 会变：新增一处代码硬编码旧路径，命中即从 0 变 1 |

J3 已落地为观测器（只读）：

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPCF"
python3 tools/kds-sync/report_loop_governance_growth.py            # 人读：文档 + 校验器双范围
python3 tools/kds-sync/report_loop_governance_growth.py --json     # 机器读
python3 tools/kds-sync/report_loop_governance_growth.py --strict   # 需要时转成阻断（J3-a 未生效则 rc=1）
```

2026-10-27 首次观测（HEAD `c7f8204e4`）：

| 指标 | 2026-08 | 2026-09 | 2026-10（进行中） | 结论 |
|---|---|---|---|---|
| 文档新增篇数 | 0 | 0 | 0 | J3-a **已生效**（连续 2 个完整月 0 新增） |
| 文档净增行数 | +888 | 0 | +453 | 仅观测：文档没新增但行数在涨 |
| 校验器新增 `.py` | 18 | 3 | 34 | 冻结规则 2 **未生效** |

**为什么 J3-b 不能当判据**：2026-08 新增篇数为 0、净增行数 +888（改名同步、翻译补行同样推高行数）。用行数判「新增」，会在文档一篇没加的时候判成「新增了」——假判据。因此行数降为观测指标，其退出条件另立。

**为什么把规则 2 也纳入观测**：冻结规则 2「暂停新增非 P0 validator」同样没有观测手段，而实测 2026-08 新增 18 个、2026-09 新增 3 个、2026-10 至 27 日已新增 34 个 `.py`。规则没人看，就是口号。

### 4.1 J5：搬迁类改动的判据（2026-10-27 实测落地）

事故：KDS `b26fff66a`（2026-10-13 `git mv` 保历史）把 `世界资产/世界模型引擎/ontology` 迁到 `世界资产/引擎/ontology`，同步了活跃区 158 处引用，漏了 GPCF 两个验证器的路径常量 → 两条门禁双双 `exit 1`，静默 14 天无人发现。

修复：`1448f6339`，只改 4 行路径常量、不动逻辑（`validate_cwme_ontology_chain.py` 1 行、`validate_cwme_space_domain_extension_registration_request.py` 3 行）。改前两条 `exit=1`（`FAIL: missing file: cwme-ext.ttl` / `FAIL: attachment missing: …/世界模型引擎/ontology/cwme-ext.ttl`），改后两条 `exit=0`。

判据命令（代码/配置后缀，范围 GPCF + KDS）：

```bash
OLD="世界模型引擎/ontology"
grep -rn "$OLD" "GlobalCloud GPCF" "GlobalCloud KDS" \
  --include=*.py --include=*.sh --include=*.bash --include=*.yaml --include=*.yml \
  --include=*.json --include=*.toml --include=*.ts --include=*.js \
  --exclude-dir=node_modules --exclude-dir=.git | wc -l
```

2026-10-27 实测（改后）：可执行代码命中 **0**；6 个数据/记录文件共 10 行命中，且**全部**同文件内已写明新路径（留痕合格）。改前：两个被改文件分别 1 行 + 3 行。

**为什么判据不是「全仓命中 0」**：历史证据 JSON 里的旧路径是当时的史实，把它改成新路径等于伪造历史并切断血缘；`features/active/F-017…/feature.yaml` 那种「现路径 X；journal 记载为 Y」的写法正是合规留痕。若把判据写成全仓 0，下一次搬迁会逼人改写历史记录——判据反过来伤害证据链。

**为什么 `.md` 不在判据范围**：规则文档必须能写出旧路径才传得下去，纳入就会判据自匹配（本页会命中自己）。

**这条判据必须成对使用**：路径改对 ≠ 门禁修好。本次两条脚本**不在 CI、不在手动入口、不被任何脚本调用**（复核命令见下），所以哪怕路径昨天就改对，14 天里也没有一次运行机会。「修好没人跑」与 §1.1「CI 绿不是判据」是同一个病：门禁的价值等于它的入口覆盖，不等于脚本存在。

```bash
grep -rn "validate_cwme_ontology_chain\|validate_cwme_space_domain_extension_registration_request" \
  --include=*.yml --include=*.yaml --include=*.sh --include=*.py \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.kds --exclude-dir=.okf . \
  | grep -v "^./tools/kds-sync/validate_" | grep -v "^./docs/"
# 期望：无输出（当前实测即无输出 → 两条门禁仍无入口，已列入 §5 A6）
```

判据使用纪律：以上五条均为可复跑计数，不接受「基本完成」「已收敛」这类口头表述；报数必须同屏给命令与输出。

### 4.2 A6 入口现状（2026-10-27 实测，防「已纳入 CI」被读成「CI 在把关」）

| 入口 | 状态 | 依据 |
|---|---|---|
| `scripts/gpcf_full_sweep.py` | ✅ **真入口**，本地可跑；`cwme_` 3 处命中 | `grep -c cwme_ scripts/gpcf_full_sweep.py` → 3；红路见 §4.3 |
| `.github/workflows/governance.yml` | ✅ 已写 3 步；✅ **CI 在跑**（job=`gpcf-gates`，`runs-on: ubuntu-latest`，GitHub 托管）；❌ **但结论 failure**；⛔ **A6 三步至今未被执行过**（前置步骤先失败，后续全部 skip） | `grep -n runs-on …` → `:9`/`:42` 均 `ubuntu-latest`；`gh run list` → `40416780567`/`40415151472`/`40414681800`（10-26）均 completed；`gh run view 40416780567`：job `gpcf-gates` 失败在 `document_control.py --check`（`changed_count=31`，exit 1），其后各步 skip ⇒ **第 71-73 行那三步没跑过**；另一 job `repository-checks` 因 pytest `test_project_registry_matches_current_project_scope` 断言失败。**「在跑」≠「跑过了」≠「跑对了」** |
| `.github/workflows/standards.yml` | ⚠️ `runs-on: [self-hosted, macOS]`；本机唯一 runner 自 2026-10-22 20:31 起被禁用 | `ls ~/Library/LaunchAgents \| grep actions.runner` → `actions.runner.Jiumilu-GCGPCF.mac-mini-gpcf.plist.disabled-20261022`；`launchctl list \| grep actions.runner` 无输出；最近一次 success（`40414681461`，10-26 22:44）由谁执行**未证** |

**关键区分（防误判）**：A6 那三步在 `governance.yml`，用的是 ubuntu-latest，**不受本机 self-hosted runner 禁用影响**；依赖 self-hosted 的是 `standards.yml`，它的在线性未证实——两者不能混成一句「CI 跑不起来」。

### 4.2.1 「会不会跑」的证据分层（照抄结论前先看这一栏）

判断「这条门禁会不会跑」必须**逐个 workflow 看 `runs-on`**，不许按仓、按人、按本机进程推——同一仓里可能两种 runner 并存。

**已证**
1. 本机 `Runner.Listener` 进程数 = 0；
2. 本机唯一 runner `actions.runner.Jiumilu-GCGPCF.mac-mini-gpcf.plist.disabled-20261022` 处于禁用态（10-22）；
3. `gh api repos/Jiumilu/GCGPCF/actions/runners` 返回 0 个；
4. `standards.yml` 最近一次运行 `40414681461` = **success / 13s / 2026-10-26 22:44Z**；
5. `governance.yml`、`console.yml` 的 `runs-on` 均为 `ubuntu-latest`（GitHub 托管，不依赖本机 runner）。

**未证**
- `standards.yml` 那次 success **是谁执行的**（进程不在、API 报 0，却成功过）。

**推得出来的**：`standards.yml` 的「在线性**未证实**」；A6 所在的 `governance.yml` 不受本机 runner 禁用影响。
**推不出来的**：「这条门禁是死的」——三个已证事实合起来推不出该结论。

**处置**：runner 健康核**交运维官统一核**（属对外连接与凭据，红线，本仓不碰）；本页只登记状态，标「待运维官核」。

### 4.3 A6 红路（验在 sweep 上，因为那是当前唯一本地真入口）

```
# ① 从 sweep 摘掉两条门禁（保留入口存在性判据）
$ python3 tools/kds-sync/validate_cwme_gate_entrypoints.py
FAIL: sweep does not run tools/kds-sync/validate_cwme_ontology_chain.py
FAIL: sweep does not run tools/kds-sync/validate_cwme_space_domain_extension_registration_request.py
cwme_gate_entrypoints=fail targets=3        exit=1

# ② 摘回来
$ python3 tools/kds-sync/validate_cwme_gate_entrypoints.py
cwme_gate_entrypoints=pass targets=3 entries=2 sweep=wired ci=wired   exit=0
$ git status --porcelain -- scripts/gpcf_full_sweep.py   → 0 行
```

路径常量红路（从入口 `scripts/gpcf_full_sweep.py` 跑）：`:18` 改回旧路径 → `cwme_ontology_chain 1`、`汇总 13/19`、`SWEEP_EXIT=1`；恢复 → `cwme_ontology_chain 0`、`汇总 14/19`（其余 5 项既有失败非本批）。

## 5. 待裁定（本页只列，不自行执行）

| 编号 | 事项 | 现状 | 卡在哪 |
|---|---|---|---|
| A1 | 32 篇 WAME 属主 loop 文档的归档/移交 | **已转可推进路径**：改为先对 16 篇无入口文档逐篇确认引用方 | 非永久挂起。确认清单见 `docs/governance/loop-无入口文档引用方确认清单.md`，分批推进：#1 零消费方 3 篇 → #2 架构 1 篇 → #3 本仓 T3 消费者 6 篇 → #4 跨 WAME 主计划 4 篇；规则类 2 篇倾向保留。每批须 WAME 属主书面同意，归档动作由 Chief 一次性书面调拨 |
| A2 | GPCF 属主 2 篇中真正无入口的那篇：`LOOP_CAPABILITY_USAGE_MATRIX.md`（另一篇 `GKE-001长期实施调度提示词.md` 被 `document_control.py` 读取，属 T1） | 未动 | 已被 WAME 的 `LOOP_CAPABILITY_REGISTRY.md`、`LOOP_CONTROL_BOARD.md` 与 GFIS 执行台账引用（真消费方 4 个），不能因「属 GPCF」就单方处置 |
| A3 | 49 个无入口脚本是否批量标 `P2 仅审计` | 未动 | 批量改档需 Chief 书面；且需逐个确认无一被外部定时任务调用 |
| A4 | F-004 关闭口径与 PMC #255 对齐 | **已裁定（Chief 2026-10-27）**：以仓内 `feature.yaml` 为准，PMC 是投影。首轮 done = 首轮收敛完成，当前为第二轮 | 已在 `feature.yaml` 增 `second_round` 段（`starts: 2026-10-27`、`pmc_ref: PMC #255`、判据 J1–J4、观测值、`explicit_non_actions`） |
| A5 | PMC 同步器路径 typo（`GlobalCoud GPCF`，缺一个 `l`）导致 `pmc_sync_gpcf` 退出码 1 | 已实测 | 不在本仓写区，Chief 2026-10-27 回复已另转人修，不经本仓 |
| A6 | 两条 CWME 门禁（`validate_cwme_ontology_chain`、`validate_cwme_space_domain_extension_registration_request`）修好路径后**仍无任何入口**：不在 CI、不在 `gpcf_full_sweep.py`、不被任何脚本调用 | **已纳入**（`6cb7afebe`，依据 Chief 2026-10-27 裁定：sweep 与 CI 两处各加一步）；入口存在性判据 `validate_cwme_gate_entrypoints.py` 为**自加项**。入口现状见 §4.2 | 无（已闭环）；残余风险：`standards.yml` 用的 self-hosted runner 在线性未证实，见 §4.2 |

## 6. 四栏头

- **出具人**：GPCF 属主（Bot）
- **会话 ID**：`session-4acd4b7f-d146-419a-91d8-2e01d7207f52`
- **关键命令与退出码**：`git log -1` rc=0；基线统计 heredoc（§1）rc=0；`python3 tools/kds-sync/report_loop_governance_growth.py` rc=0；`python3 tools/kds-sync/document_control.py --check` rc=0；`python3 tools/kds-sync/loop_document_gate.py --check-only --repository-only` rc=0；`python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py` rc=0；CWME 两条门禁改前 exit=1 / 改后 exit=0（§4.1，commit `1448f6339`）
- **配套文件**：`docs/governance/loop-无入口文档引用方确认清单.md`（16 篇逐篇确认）、`features/done/F-004-loop-governance-slimming/feature.yaml` 的 `second_round` 段（唯一状态源）
- **复核人**：待 Chief / 运营官按台账核
- **复核防误判**：`loop_document_gate.py` 的 `check_failures.feature_workspace` 会因**其他属主正在写 `features/*/feature.yaml`** 而瞬时变红（2026-10-27 21:16 实测一次，写入完成后复跑 rc=0）。遇到该红项先看是否跨属主并发写，不要当成 loop 收敛的证据。
