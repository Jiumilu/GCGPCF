---
name: globalcloud-project-group-git-clean
description: GlobalCloud 项目群 17 个 Git 仓库全量 clean 门禁技能。用于用户要求“项目群 17 仓 Git clean”“全量 Git 收口”“Loop Git clean 门禁”“检查所有仓库是否 clean”“纳入 Loop 的 Git clean 技能”时，逐仓检查存在性、分支 upstream、dirty/untracked、ahead/behind、diff check 和敏感文件路径，并输出可回放 gate 证据。只做只读审计，不自动提交、推送、stash、reset、clean 或删除文件。
metadata:
  doc_id: GPCF-DOC-7F9C2E9A61
---

# GlobalCloud Project Group Git Clean

## 目标

本技能为 GlobalCloud 项目群提供 17 仓全量 Git clean 门禁。它只做确定性审计，输出 `pass`、`partial` 或 `blocked`，供 Loop 判断是否可以继续推进、提交、推送或进入验收。

## 使用时机

当用户要求以下事项时使用本技能：

- 项目群 17 个 Git 仓库全量 clean 检查。
- Loop 启动、继续或收口前需要全仓 Git 状态证据。
- 判断 dirty、未推送、远端落后、敏感文件路径是否阻塞状态升级。
- 为提交、推送或验收前生成 Git gate 证据。

## 受控仓库

门禁固定检查以下 17 个仓库：

- `GlobalCloud AAAS`
- `GlobalCloud Brain`
- `WAS世界资产体系`
- `GlobalCloud XiaoC`
- `GlobalCloud WAES`
- `GlobalCloud GPC`
- `GlobalCloud Studio`
- `GlobalCoud GPCF`
- `GlobalCloud XWAIL`
- `GlobalCloud GFIS`
- `GlobalCloud MMC`
- `GlobalCloud KDS`
- `GlobalCloud XiaoG`
- `GlobalCloud PVAOS`
- `GlobalCloud SOP`
- `GlobalCloud PKC`
- `GlobalCloud XGD`

默认项目群根目录为当前 GPCF 仓库的上级目录：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1`。

## 快速运行

在 GPCF 仓库根目录运行：

```bash
python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py
```

指定项目群根目录：

```bash
python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1"
```

需要在检查前做只读网络探测时：

```bash
python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --fetch-dry-run
```

## 判定规则

`pass` 必须同时满足：

- 17 个仓库全部存在且是 Git 仓库。
- 每个仓库有当前分支和 upstream。
- `git status --porcelain=v1` 为空。
- `ahead=0` 且 `behind=0`。
- `git diff --check -- .` 通过。
- Git 状态路径中没有敏感文件模式。

以下情况为 `blocked`：

- 仓库缺失或不是 Git 仓库。
- upstream 缺失。
- 当前分支落后 upstream。
- `git diff --check -- .` 失败。
- Git 状态中出现 `.env`、TOKEN、SECRET、证书、私钥等敏感路径。

以下情况为 `partial`：

- 存在普通 dirty/untracked 变更。
- 本地分支 ahead upstream 但无敏感路径、无 diff check 错误、无 behind。

## Loop 接入要求

Loop 启动、继续、提交前或验收前，如涉及项目群整体状态，必须运行本技能脚本并把输出纳入本轮 evidence。门禁未 `pass` 时不得宣告项目群 Git 全量 clean；若有敏感路径或远端冲突，状态最高为 `blocked`。

本技能不会自动执行任何修复动作。若需要提交或推送，必须在用户授权、敏感检查通过、变更范围受控后另行执行。

## 输出边界

本技能必须严格遵守 `DO NOT send optional commentary`。输出只保留 Git gate 结论、阻塞仓库、敏感路径风险、授权确认请求和可复现验证证据，不发送可选过程性说明。
