# F-018 证据索引（evidence summary）

> 交付方式：本线（Hermes）实施 M1-M3；本目录为**如实**证据索引（每条可溯源）。

## 1. 数据面工具（GPCF 仓 tools/）

| 工具 | 产物 | 实测 |
|---|---|---|
| `export_governance_state.py` | `runtime/evidence/governance-state-20261014-*.json` | findings=0；queue 16／okf 206／projects 22／台账 20 行 |
| `index_governance_ledgers.py` | `runtime/evidence/ledger-index-20261014-*.json` | 34/34 controlled；findings=0 |
| `probe_governance_state.py` | `runtime/evidence/governance-probe-20261014-*.json` | ok 13／stale 2（如实分级） |

## 2. 提交记录（changelog）

| 仓 | 提交 | 说明 |
|---|---|---|
| GPCF | `90b5d78c7` | 导出器 v0.1（M1·D1.1） |
| GPCF | `a2d8eeb1d` | 索引器＋探针（M1·D1.2/1.3） |
| GPCF | `774668d74` | 导出器补逐项队列＋项目群明细（M2·D2.3 数据面） |
| GPCF | `01ec65e4f` | 台账 §4 解析＋三节奏明细（M3 深化） |
| WAE | `fbe57f2` | 模块包＋母本第6项＋只读代理＋对账表 v0.6（M2） |
| WAE | `68a8c7a` | 主方案表＋项目群三节奏卡（M3） |
| KDS | `77b8b5dd` | registry v0.6（gpcf-console available·mmc 校准） |
| KDS | `eb35a54a`／`de47b2bd` | 规划件 M1-M3 进度标注 |

## 3. E2E 真机（浏览器）

- 地址：`http://localhost:4300/global-cloud-workbench/gpcf`（WAE 母本·第 6 项导航）。
- 八页签：概览/交付/项目群/主方案/闭环/台账/规则/门禁——切换实测通过（Radix mousedown 事件链）。
- 交付视图：F-xxx 条目 17（16 队列＋1 当前）；门禁视图：探针表 15 行；主方案：20 项目在案。
- 截图（本地）：`~/.hermes/cache/scratch/gpcf_console_v2.png`（概览）｜`gpcf_m3_masterplan.png`（主方案）。

## 4. 诚实记录（不作为验收声明）

- 全仓 typecheck 唯一红点＝`apps/wae-console/vite.config.ts`（他线在途改动·与本 Feature 无关）；我方文件（module-gpcf-console/wame）全绿。
- 探针 stale 信号（state.json 38.6 天／loops 98 天）＝**治理侧待处置事项**，本控制台如实呈现、不代处置。
- 生产就绪声明：`production_ready=false`（无生产/发布/接受声明）。

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: pass
- api: fail
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
<!-- GPCF_EVIDENCE_GATE_END -->
