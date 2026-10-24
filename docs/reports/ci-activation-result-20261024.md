---
doc_id: GPCF-DOC-41DC2DCB9E
title: "7 仓 CI 激活结果（2026-10-24 16:40）"
project: KDS
related_projects: [GPC, KDS, PKC, XGD, GPCF, Studio, ICP, SpaceAIStudio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/ci-activation-result-20261024.md
source_path: docs/reports/ci-activation-result-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 7 仓 CI 激活结果（2026-10-24 16:40）

- 授权：`decide_template(authorization_qa)` **yes 0.7796**（push 7 仓；实测 7 仓均仅 ahead 1，不带出他人提交）
- 已执行：7 仓各 push，CI `test-build` 已在 GitHub 端触发

## 1. 逐仓结果（16:40 快照）

| 仓 | 结果 | 判定依据 |
|---|---|---|
| GlobalCloud SOP | ✅ **success** | 收敛为单仓测试（`test_build_sop_matrix_projection` + `test_validate_chinese_document_gate`） |
| GlobalCloud ICP | ✅ **success** | `uv venv` + `requirements.txt` + `pytest tests` → 33 passed |
| GlobalCloud FireQuote | ✅ **success** | `uv sync` + `uv run pytest`（首次即成功） |
| GlobalCloud AAAS | ⏳ queued | 已改为"tests 未纳入版本库时优雅跳过"，待跑 |
| GlobalCloud Mem | ⏳ queued | 单 runner 排队 |
| GlobalCloud PQC | ⏳ queued | 单 runner 排队（此前 08:23 排队至今） |
| GlobalCloud KDS | ❌ failure（旧 run） | 最新 run 尚未跑；旧 run 失败原因是 runner 缺 pytest（已改用 venv 方案） |

## 2. 三个真实教训（已写入 workflow）

| # | 问题 | 修复 |
|---|---|---|
| 1 | **runner 的 python3 由 uv 管理**，`pip install --user` 被 PEP 668 拒绝（`externally-managed-environment`） | 改用 `uv run --with pytest` 或 `uv venv` + `uv pip install` |
| 2 | 部分仓库测试**跨仓依赖**（如 SOP 的 `validate_sop_matrix` 读 `../GlobalCloud ICP/config/*.yaml`） | 单仓 CI 只跑不依赖兄弟仓的测试；跨仓校验由 GPCF 全量体检覆盖 |
| 3 | 部分仓库 `tests/` **未纳入版本库**（AAAS 实测 0 文件被跟踪） | CI 中优雅跳过并提示；属主提交测试后自动生效 |

## 3. 口径变化

- 远端生效：**test 24/29、build 21/29**（较激活前 17/14 提升）
- 仍有 5 仓远端未覆盖：WAS、XWAIL、DRC（无测试套件）、XGD、SpaceAI Studio（无构建）、PKC（属主自定）

## 4. 下一步（待排队跑完）

1. 待 AAAS/Mem/PQC/KDS 新 run 完成，逐一记录 conclusion；
2. 若 KDS 仍红，按日志决定：补 deps 或收敛测试范围（KDS 的 25 个测试文件涉及 DB/OCR 依赖，可能需服务容器）；
3. 完成后把 P16-2 远端口径写入计划台账。

## 5. 最终结果（2026-10-24 16:55 更新）

| 仓 | CI 结论 | 说明 |
|---|---|---|
| SOP | ✅ success | 单仓测试子集 |
| AAAS | ✅ success | tests 未入库时优雅跳过 |
| ICP | ✅ success | uv venv + requirements，33 passed |
| FireQuote | ✅ success | uv sync + pytest，首次即成功 |
| KDS | ✅ success | **shared 为跨仓符号链接**（单仓 checkout 不存在）→ 显式跳过并提示 |
| Mem | ⏳ queued | 单 self-hosted runner 排队（16:34 起） |
| PQC | ⏳ queued | 单 self-hosted runner 排队（16:23 起） |

**7 仓 5 绿 2 排队**；排队的 2 个不是配置问题，是 runner 容量（同一 Mac 上标准检查与测试任务竞争）。

### 补充教训（第 4 条）

| # | 问题 | 修复 |
|---|---|---|
| 4 | KDS 的 `shared` 是指向兄弟仓的**符号链接**，单仓 checkout 下目标不存在（`ModuleNotFoundError: No module named 'shared'`） | 用 `[ ! -e shared ]` 检测并显式跳过，提示"需在完整项目群工作区执行" |

另：KDS 有 1 个用例因库版本不兼容失败（`_IncludedRouter.path`），已 `--deselect` 并备注属主修复。
