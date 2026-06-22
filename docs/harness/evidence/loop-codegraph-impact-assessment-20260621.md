---
doc_id: GPCF-DOC-3C7CC5439F
title: Loop CodeGraph Impact Assessment Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-impact-assessment-20260621.md
source_path: docs/harness/evidence/loop-codegraph-impact-assessment-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Impact Assessment Evidence

## 结论

本轮状态为 `codegraph_operational_value_evidenced_with_active_watchlist`。

CodeGraph 已经在 LOOP 中发挥实际作用：它不只是生成 `.codegraph/`，而是已经用于项目群覆盖证明、漂移发现、同步决策、GFIS residual 分类、下一轮输入生成和可回放 validator。当前 Brain 与 Studio 仍存在活动 drift watchlist，这不削弱 CodeGraph 的作用，反而证明它能阻止虚假静止状态。

本评估不证明项目业务完成，不升级 `accepted`、`integrated` 或 `production_ready`。

## 输入证据

| 证据 | 作用 |
|---|---|
| `loop-codegraph-project-group-coverage-20260620.json` | 证明项目群 CodeGraph 覆盖从试点进入项目群范围 |
| `loop-codegraph-sync-drift-20260621.json` | 证明 CodeGraph 能发现并收敛 sync drift |
| `loop-codegraph-gfis-residual-notice-20260621.json` | 证明 CodeGraph 能暴露 GFIS residual 并定位候选 |
| `loop-codegraph-large-file-policy-20260621.json` | 证明 residual 不被误判为业务失败，而是进入策略分类 |
| `loop-codegraph-project-group-graphized-20260621.json` | 证明 14 仓图谱化覆盖、11 仓 up-to-date、Brain 与 Studio active watchlist、GFIS controlled residual |
| `loop-codegraph-project-group-monitor-20260621.json` | 证明 monitor 能回放当前状态和 `.codegraph` Git 保护 |

## 评估矩阵

| 维度 | 分数 | 证据判断 |
|---|---:|---|
| 覆盖真实度 | 5 / 5 | 14 个本机 Git 仓均已 indexed，且 `.codegraph/` 未进入 Git |
| 漂移发现能力 | 5 / 5 | Brain 活动 drift 扩大到 32 个文件、Studio 出现 4 个 pending 图谱变更，并被 CodeGraph 发现，未被旧完成态掩盖 |
| LOOP 决策支持 | 5 / 5 | CodeGraph 状态已产生 monitor、sync drift、residual notice、large-file policy、project-group monitor 等下一轮输入 |
| 降本证据 | 3 / 5 | 已将排查从项目群不确定性压缩到仓级和文件级；但尚未形成连续 MTTD/MTTR 趋势和量化节省 |
| 风险控制 | 5 / 5 | Brain 与 Studio 活动 drift 存在时不宣称静止完成，GFIS residual 未被误写为业务完成或生产就绪 |
| 可回放性 | 5 / 5 | graphized 与 monitor validator 可复跑验证当前 CodeGraph 状态、Git 保护和 GFIS policy exception |

综合评分：`28 / 30`，评级为 `effective_with_active_watchlist`。

## 已经发挥的实际作用

1. 发现变化：CodeGraph 将 Brain、Studio、GPCF、KDS 的 drift 暴露为可处理对象，并在本轮阻止把 Studio 误判为已清空。
2. 限定范围：CodeGraph 把项目群不确定性缩小到具体仓、具体 pending 类型，部分轮次进一步定位到具体文件。
3. 驱动 LOOP：CodeGraph 状态直接生成下一轮输入，而不是依赖人工猜测。
4. 防止误判：在 drift 未闭合前，LOOP 未声明完成；GFIS residual 被归入 policy exception。
5. 可回放：validator 可以重复检查 14 仓覆盖、Git 保护、up-to-date 数量和 residual 策略。

## 尚未证明的作用

- 未量化连续多轮 MTTD。
- 未量化连续多轮 MTTR。
- 未证明业务功能完成。
- 未证明客户验收、UAT、生产写入或部署完成。

## 下一轮输入

`GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`

目标：持续监控 Brain 与 Studio 活动 CodeGraph drift，开始记录 drift 检出时间、决策时间、关闭时间和人工搜索避免说明，形成可量化 MTTD/MTTR 趋势。
