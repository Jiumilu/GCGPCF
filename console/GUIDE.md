---
doc_id: GPCF-DOC-ACC977D1A6
title: GPCF 控制台使用说明
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/console/GUIDE.md
source_path: console/GUIDE.md
sync_direction: bidirectional
last_reviewed: 2026-10-27
supersedes: []
superseded_by: []
---

# GPCF 控制台使用说明

只读治理控制台：把仓库里的 `feature.yaml`、`runtime/queue.json`、项目清单、门禁脚本、文档台账与角色流转日志，渲染成「一页读完、按需下钻」的静态站。

它**不是**业务系统，也**不是**写入口：页面不写任何仓库状态；界面上的「裁定 / 重跑 / 补录」只是提示，不落库。

## 三条命令

```bash
make console-data     # 重建快照 -> console/public/data/*.json
make console-check    # 校验快照与仓库是否一致（过期退出码 1，不写盘）
make serve            # 本地预览 http://127.0.0.1:4173
```

## 数据从哪来

`scripts/console_export.py` 只读以下来源，输出 6 份 JSON：

| 输出 | 来源 |
|---|---|
| `features.json` | `features/{active,done}/F-*/feature.yaml` |
| `projects.json` | `config/project-group-projects.yaml` + 各项目 STATUS/ROADMAP/RISK 是否存在 |
| `gates.json` | 六道闸口的命令与脚本存在性；文档闸结果取自健康报告 |
| `docs.json` | `09-status` 文档控制台账与健康报告（快照值，非实时） |
| `loops.json` | `runtime/logs/F-*.jsonl` 的角色流转 |
| `meta.json` | 计数、漂移、路线、真值来源、非声明边界 |

`--check` 比对时忽略 `generated_at` 与 `source_sha` 两个身份字段（它们随每次提交变化），其余逐字节比对。

## 页面

| 路由 | 内容 |
|---|---|
| `#/` | 主页：进度、卡点、待裁、路线、文档与门禁 |
| `#/features` | 议题：按步骤分组 + 右侧详情（证据五件套 / 门禁六项 / 阻塞 / 派生差异） |
| `#/projects` | 项目：29 个项目、活跃归属、入口文件是否齐全 |
| `#/loops` | 循环：角色分布 + 最近 24 条流转 |
| `#/gates` | 门禁：六道闸口命令（可复制）+ 证据矩阵 |
| `#/docs` | 台账：文档控制与健康快照 |

键盘：`⌘K` 命令面板；`g h` / `g f` / `g p` / `g l` / `g g` / `g d` 依次跳主页 / 议题 / 项目 / 循环 / 门禁 / 台账；议题页 `↑↓` 选中、`Enter` 打开、`Esc` 收起。

## 漂移语义

导出时按 `runtime/status-source-of-truth.yaml` 的 `step_to_queue_status` 与 `role_by_step` 逐条比对，差异分四类：

| 类别 | 含义 | 处理 |
|---|---|---|
| `drift` | 真值与派生视图在一个已映射字段上不一致 | 以 `feature.yaml` 为准，先修派生侧生成逻辑 |
| `mapping_gap` | 派生侧停在初始态（`queued` / `Dispatcher`），但映射表没有定义初始态 | 补映射定义，不算真实漂移 |
| `missing_in_queue` | 工作区存在但队列没有条目 | 补录 |
| `orphan_in_queue` | 队列有条目但工作区不存在 | 清理 |

页面只展示，不修正；`meta.json` 的 `drift.true_drift_features` 是真漂移的 Feature 列表。

## 快照新鲜度

- 本地 `pre-commit`：不一致时**只告警**，不阻断提交（与 loop gate 降级同口径）
- `make console-check`：不一致即非零退出
- CI `gpcf-console`（`.github/workflows/console.yml`）：以失败阻断

改了 `feature.yaml`、`runtime/queue.json`、`runtime/logs`、`config/project-group-projects.yaml`、`projects/**` 或 `09-status` 两份台账，都要 `make console-data` 后与改动同提交。

## 边界

- 只读：不写 `feature.yaml`、`queue.json`、`STATUS.md`
- 不声明 `accepted` / `integrated` / `production_ready`
- 健康快照是导出时读到的那一版（页面会标出生成时间），不是实时值

## 排障

| 现象 | 处理 |
|---|---|
| 页面显示「数据没有加载出来」 | 用静态服务器打开（`make serve`），不要直接双击 `index.html`（`file://` 下 fetch 被拦） |
| `make console-check` 报 stale | `make console-data` 后提交快照 |
| 顶栏出现「已过期」徽标 | 快照超过 24 小时未重建 |
| 门禁检查 | `python3 ../GlobalCloud WAE/scripts/ui_gate.py console --strict` |
