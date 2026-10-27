---
doc_id: GPCF-DOC-LOOP-SLIMMING-CONFIRM-20261027
title: loop 无入口文档引用方确认清单
project: GPCF
related_projects: [GPCF, WAME, GFIS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/governance/loop-无入口文档引用方确认清单.md
source_path: docs/governance/loop-无入口文档引用方确认清单.md
sync_direction: bidirectional
last_reviewed: 2026-10-27
supersedes: []
superseded_by: []
---

# loop 无入口文档引用方确认清单

配套文档：`docs/governance/loop-治理收敛范围与判据.md`（范围与判据）
关联工作项：F-004 第二轮收敛（`features/done/F-004-loop-governance-slimming/feature.yaml` 的 `second_round`），PMC #255

**本清单不含任何归档动作。** 归档须先按本文走完「逐篇确认」，再由 Chief 书面调拨。当前 16 篇一篇未动。

## 0. 口径：什么算「引用方」

| 类型 | 举例 | 算不算消费方 |
|---|---|---|
| T1 真门禁脚本 | `.github/workflows/*.yml` 里执行的 `.py` | 算 |
| T2 手动入口脚本 | `scripts/gpcf_full_sweep.py`、`run_frontmatter_pipeline.sh`、`tests/` | 算 |
| T3 无入口脚本 | `tools/kds-sync/validate_*.py` 中未被 T1/T2 调用的 | 算「消费方」，但**归档改了它也不会有门禁变红**——所以必须靠清单确认，不能靠跑一遍 |
| 证据 / loop-round / 规范文档 | `docs/harness/evidence/*`、`docs/harness/loops/*`、`04-ui-delivery/*` | 算 |
| 目录页 / 登记页 | `02-governance/README.md`、`02-governance/loop/README.md`、`09-status/kds-development-space-sync-plan.md`、`loop/studio/README.md` | **不算消费方，只算索引** |
| 判据文档自身 | 本文件、`loop-治理收敛范围与判据.md` | **不算消费方**（否则判据自匹配） |

「目录页不算消费方」的反面检验：把一篇文档移走，目录页那行会变成死链，但**没有任何执行路径改变**。所以目录页只证明「被登记过」，不证明「被使用」。

「判据文档不算消费方」的反面检验：本文件为了说明某篇文档而去引用它的文件名，若把它算作消费方，就等于判据自己被判据搜到——第 1 版就踩过这个坑（`LOOP_CAPABILITY_USAGE_MATRIX` 一度被本清单算成 5 个消费方，其中 1 个是我自己的判据文档）。

据此推出归档三件套（缺一不可）：**移文档 → 同步删登记行 → 写替代关系**。只做第一件会留下死链。

## 1. 16 篇逐篇确认表

基线：HEAD `c7f8204e4`，复跑命令见 §3。「真消费方」列已剔除目录页、登记页与判据文档；数字与 §3 命令输出逐行对齐。

| # | 文档 | 属主 | 真消费方数 | 主要消费方（节选） | 需书面签字的人 | 我的初步意见 |
|---|---|---|---|---|---|---|
| 1 | LOOP_L3_5_REAL_API_VERIFICATION.md | WAME | 0 | —（仅目录页/登记页） | WAME 属主 | 可归档；本仓无反对 |
| 2 | LOOP_L5_FULL_PRODUCTION_AUTONOMY.md | WAME | 0 | —（仅目录页/登记页） | WAME 属主 | 可归档；内容涉 L5 自治，建议架构师顺带看一眼 |
| 3 | LOOP-STUDIO-INITIALIZATION.md | WAME | 0 | —（仅 `loop/studio/README.md` 目录页） | WAME 属主 | 可归档；Studio 是否仍在用需 WAME 确认 |
| 4 | LOOP_L4_AUTONOMOUS_OPERATIONS.md | WAME | 1 | `01-architecture/…最小闭环L4实施方案.md` | **架构师** + WAME 属主 | 唯一真引用在架构文档，须架构师先判 |
| 5 | LOOP_CAPABILITY_USAGE_MATRIX.md | **GPCF** | 4 | `LOOP_CAPABILITY_REGISTRY.md`、`LOOP_CONTROL_BOARD.md`（均 WAME）、GFIS 执行台账、1 个 T3 脚本 | GPCF（自属）+ WAME + GFIS 属主 | 我属主，但被 WAME 登记表与 GFIS 台账引用，不能单方定 |
| 6 | LOOP_AGENT_REACH_EXA_AUTH_PACK.md | WAME | 3 | 1 T3 脚本 + 1 evidence + 1 loop-round | GPCF（脚本与证据均本仓） | 按 T3 脚本处置，脚本降 P2 后可归档 |
| 7 | LOOP_AGENT_REACH_L3_CANDIDATE_PIPELINE.md | WAME | 2 | 1 T3 脚本 + 1 loop-round | GPCF | 同上 |
| 8 | LOOP_CODEGRAPH_NORMALIZATION_CHECKLIST.md | WAME | 3 | 1 T3 脚本 + 1 evidence + 1 loop-round | GPCF | 同上 |
| 9 | LOOP_CODEGRAPH_P1_PILOT_ADMISSION.md | WAME | 3 | 1 T3 脚本 + 1 evidence + 1 loop-round | GPCF | 同上 |
| 10 | LOOP_CODEGRAPH_LARGE_FILE_POLICY.md | WAME | 9 | **6 个 T3 脚本** + 2 份 evidence + 1 份 loop-round | GPCF | 消费者最多（6 个脚本），须先定脚本去留再谈文档 |
| 11 | LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md | WAME | 14 | 3 个 T3 脚本 + 8 份 evidence + 1 份 loop-round + `loop/context/headroom/policy.yaml` + 1 个 fixture | GPCF | 有运行时配置引用，不能只看脚本 |
| 12 | LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md | WAME | 4 | 2 个 T3 脚本 + 1 份 evidence + `LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md`（WAME） | GPCF + WAME | 被 WAME 主计划引用，需 WAME 一并确认 |
| 13 | LOOP_ENGINEERING_SELF_CORRECTION.md | WAME | 9 | 1 个 T3 脚本 + 2 份 evidence + **5 份 loop-round** + WAME 主计划 | GPCF | 历史轮次引用最多，归档会断历史回放 |
| 14 | LOOP_GOVERNANCE_OPERATING_BOUNDARY.md | WAME | 6 | 2 个 T3 脚本 + 3 份 evidence + `LOOP_GOVERNANCE_PHASE_GOAL.md`（WAME） | GPCF + WAME | 定义治理进程与实施进程边界，属**规则类**，倾向保留 |
| 15 | LOOP_MULTI_AGENT_EXECUTION_POLICY.md | WAME | 3 | `LOOP_CAPABILITY_REGISTRY.md`（WAME）+ 1 evidence + 1 loop-round | GPCF + WAME | 策略类，倾向保留 |
| 16 | LOOP_UI_PRODUCT_FIRST_CONTROL.md | WAME | 8 | 2 个 T3 脚本 + 3 篇 WAME 文档 + `04-ui-delivery/UI 规范` + `.codex` 技能 + 2 份 reports | GPCF + WAME + **设计/UI 属主** | 被 UI 规范与技能引用，须设计侧确认 |

## 2. 推进顺序（先易后难，不一次要 16 篇）

1. **第 1 批（零消费方，3 篇）**：#1 #2 #3 —— 只需 WAME 属主书面同意。#2 建议架构师顺带看一眼。
2. **第 2 批（唯一真引用在架构文档，1 篇）**：#4 —— 等架构师判定 L4 实施方案是否仍引用。
3. **第 3 批（消费者是本仓 T3 脚本，6 篇）**：#6 #7 #8 #9 #10 #11 —— 前置条件是先定这些脚本的去留（P2 或归档），文档跟着脚本走。
4. **第 4 批（跨 WAME 主计划/登记表，4 篇）**：#5 #12 #13 #15 —— 需 WAME 属主一起确认。
5. **暂不推（规则/策略类，2 篇）**：#14 #16 —— 定义治理边界与 UI 优先控制，删了没有门禁会拦，倾向保留，只在体量上做减法。

每批完成后回填本表「状态」列，并把结论写进 `loop-治理收敛范围与判据.md` 的 J1 覆盖计数。

## 3. 复跑命令（重新生成 §1 的消费方数据）

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPCF"
python3 - <<'PY'
import subprocess,os,re
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
INDEX=(("02-governance/README.md","02-governance/loop/README.md",
        "02-governance/loop/studio/README.md","09-status/kds-development-space-sync-plan.md",
        "09-status/globalcloud-document-control-register.md",
        "09-status/kds-development-space-sync-register.md",
        "docs/governance/loop-治理收敛范围与判据.md",
        "docs/governance/loop-无入口文档引用方确认清单.md"))
for p in [x for x in tracked("02-governance/loop") if x.endswith(".md") and not x.endswith("/README.md")]:
    b=os.path.basename(p)
    if any(tier(q) in ("T1","T2") and ("02-governance/loop/"+b) in rd(q) for q in ref): continue
    real=[q for q in allf if q!=p and q not in INDEX and not q.startswith((".kds/",".okf/"))
          and b in rd(q)]
    print("%-52s 真消费方=%d" % (b,len(real)))
    for x in real: print("     ",x)
PY
```

反面检验：若某篇文档其实有 T1 消费者但被本表列为「无入口」，上面命令会把它打印出来——表错则命令立刻对不上。

## 4. 四栏头

- **出具人**：GPCF 属主（Bot）
- **会话 ID**：`session-4acd4b7f-d146-419a-91d8-2e01d7207f52`
- **关键命令与退出码**：§3 heredoc rc=0；`validate_gpcf_2_feature_workspace.py` rc=0
- **复核人**：待 Chief / 运营官按台账核；WAME 属主确认后回填状态列
