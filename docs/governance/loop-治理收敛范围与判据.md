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

**反面检验**：这份表在收敛没做之前也是这个数，所以它本身不能证明收敛完成——它只定义起点。另需注意：CI 全绿在收敛前后都绿（真门禁只读 2 个引用脚本），**不能用「CI 绿」当收敛判据**。

## 2. 收敛什么（范围内）

- **R1 入口登记**：34 篇正文 + 55 个引用脚本，每一件必须落到 `T1 真门禁` / `T2 手动入口` / `P2 仅审计` / `归档建议` 四类之一，不允许「没人知道它归哪」。
- **R2 无入口产物降级**：49 个无入口脚本、16 篇孤儿文档，先标 `P2 仅审计`（显式声明「不阻断交付」），再决定归档或保留。
- **R3 「暂停新增」立观测**：F-004 基线（`LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md` 冻结规则 1/2）规定暂停新增治理文档与非 P0 校验器，但当前**没有任何机制观测这条规则**；10-27 当天仍有批量入库（`726e923be`「C 段入库 4/4 治理类 62 项（G-14）」，新增文件 31 个，其中 `.md` 23 个）。规则没有观测手段，就等于没有规则。
- **R4 挂账口径一致**：仓内 `features/done/F-004-loop-governance-slimming/` 已判关闭，PMC #255 仍开放。同一件事两个状态源，必须先对齐口径，否则收敛结论无处落地。

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
| J3 | 新增可观测 | 按月统计 `02-governance/loop/*.md` 净增篇数与净增行数；连续 2 个自然月净增 ≤ 0 才可言「暂停新增生效」 | 会变：只要当月新增 1 篇，净增即 > 0 |
| J4 | 挂账口径一致 | `features/` 状态与 PMC #255 状态指向同一结论 | 会变：任一侧改状态而另一侧未跟，即不一致 |

J3 的取数命令：

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPCF"
git log --since="<月初>" --numstat --format="%h %ad" --date=short -- "02-governance/loop/*.md" | awk 'NF==3{add+=$1;del+=$2} END{print "add="add,"del="del,"net="add-del}'
```

判据使用纪律：以上四条均为可复跑计数，不接受「基本完成」「已收敛」这类口头表述；报数必须同屏给命令与输出。

## 5. 待裁定（本页只列，不自行执行）

| 编号 | 事项 | 现状 | 卡在哪 |
|---|---|---|---|
| A1 | 32 篇 WAME 属主 loop 文档的归档/移交 | 未动 | 跨仓，需 WAME 属主同意 + Chief 书面；StartLux 红线闸口实测 p=0.7166 判 **stop** |
| A2 | GPCF 属主 2 篇中真正无入口的那篇：`LOOP_CAPABILITY_USAGE_MATRIX.md`（另一篇 `GKE-001长期实施调度提示词.md` 被 `document_control.py` 读取，属 T1） | 未动 | 需先确认 CodeGraph/WAS 是否有外部消费方 |
| A3 | 49 个无入口脚本是否批量标 `P2 仅审计` | 未动 | 批量改档需 Chief 书面；且需逐个确认无一被外部定时任务调用 |
| A4 | F-004 关闭口径与 PMC #255 对齐 | 未动 | 仓内已 done、PMC 仍开，谁为准待裁 |
| A5 | PMC 同步器路径 typo（`GlobalCoud GPCF`，缺一个 `l`）导致 `pmc_sync_gpcf` 退出码 1 | 已实测 | 不在本仓写区，报 Chief 转派 |

## 6. 四栏头

- **出具人**：GPCF 属主（Bot）
- **会话 ID**：`session-4acd4b7f-d146-419a-91d8-2e01d7207f52`
- **关键命令与退出码**：`git log -1` rc=0；基线统计 heredoc（§1）rc=0；`python3 tools/kds-sync/document_control.py --check` rc=0；`python3 tools/kds-sync/loop_document_gate.py --check-only --repository-only` rc=0
- **复核人**：待 Chief / 运营官按台账核
