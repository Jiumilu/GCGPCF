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

判据使用纪律：以上四条均为可复跑计数，不接受「基本完成」「已收敛」这类口头表述；报数必须同屏给命令与输出。

## 5. 待裁定（本页只列，不自行执行）

| 编号 | 事项 | 现状 | 卡在哪 |
|---|---|---|---|
| A1 | 32 篇 WAME 属主 loop 文档的归档/移交 | **已转可推进路径**：改为先对 16 篇无入口文档逐篇确认引用方 | 非永久挂起。确认清单见 `docs/governance/loop-无入口文档引用方确认清单.md`，分批推进：#1 零消费方 3 篇 → #2 架构 1 篇 → #3 本仓 T3 消费者 6 篇 → #4 跨 WAME 主计划 4 篇；规则类 2 篇倾向保留。每批须 WAME 属主书面同意，归档动作由 Chief 一次性书面调拨 |
| A2 | GPCF 属主 2 篇中真正无入口的那篇：`LOOP_CAPABILITY_USAGE_MATRIX.md`（另一篇 `GKE-001长期实施调度提示词.md` 被 `document_control.py` 读取，属 T1） | 未动 | 已被 WAME 的 `LOOP_CAPABILITY_REGISTRY.md`、`LOOP_CONTROL_BOARD.md` 与 GFIS 执行台账引用（真消费方 4 个），不能因「属 GPCF」就单方处置 |
| A3 | 49 个无入口脚本是否批量标 `P2 仅审计` | 未动 | 批量改档需 Chief 书面；且需逐个确认无一被外部定时任务调用 |
| A4 | F-004 关闭口径与 PMC #255 对齐 | **已裁定（Chief 2026-10-27）**：以仓内 `feature.yaml` 为准，PMC 是投影。首轮 done = 首轮收敛完成，当前为第二轮 | 已在 `feature.yaml` 增 `second_round` 段（`starts: 2026-10-27`、`pmc_ref: PMC #255`、判据 J1–J4、观测值、`explicit_non_actions`） |
| A5 | PMC 同步器路径 typo（`GlobalCoud GPCF`，缺一个 `l`）导致 `pmc_sync_gpcf` 退出码 1 | 已实测 | 不在本仓写区，Chief 2026-10-27 回复已另转人修，不经本仓 |

## 6. 四栏头

- **出具人**：GPCF 属主（Bot）
- **会话 ID**：`session-4acd4b7f-d146-419a-91d8-2e01d7207f52`
- **关键命令与退出码**：`git log -1` rc=0；基线统计 heredoc（§1）rc=0；`python3 tools/kds-sync/report_loop_governance_growth.py` rc=0；`python3 tools/kds-sync/document_control.py --check` rc=0；`python3 tools/kds-sync/loop_document_gate.py --check-only --repository-only` rc=0；`python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py` rc=0
- **配套文件**：`docs/governance/loop-无入口文档引用方确认清单.md`（16 篇逐篇确认）、`features/done/F-004-loop-governance-slimming/feature.yaml` 的 `second_round` 段（唯一状态源）
- **复核人**：待 Chief / 运营官按台账核
- **复核防误判**：`loop_document_gate.py` 的 `check_failures.feature_workspace` 会因**其他属主正在写 `features/*/feature.yaml`** 而瞬时变红（2026-10-27 21:16 实测一次，写入完成后复跑 rc=0）。遇到该红项先看是否跨属主并发写，不要当成 loop 收敛的证据。
