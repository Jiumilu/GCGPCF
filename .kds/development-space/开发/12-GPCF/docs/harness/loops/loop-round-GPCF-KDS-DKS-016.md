---
doc_id: GPCF-DOC-A7F413046C
title: Loop Round GPCF-KDS-DKS-016
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-016.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-016.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-016

日期：2026-06-17
状态：v0.1 受控 Loop 记录
主题：PKC-KDS 个人知识与贡献入口清单
项目群范围：GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC 个人知识、XiaoC / 小即、XGD、XiaoG、MMC、GPCF。

## 1. 输入

1. `GPCF-KDS-DKS-014` 已建立项目群与分布式 KDS 关系总图。
2. `GPCF-KDS-DKS-015` 已明确 KDS 存事实，Brain 编知识。
3. 用户目标明确：KDS 管全局事实，PKC 管个人参与。
4. 用户目标明确：个人知识、个人任务、个人积分、个人悬赏、个人 AI 服务和合作单位成员空间需要接入 KDS 11 个底座资源池及增强治理账本对象。
5. 当前 GFIS / GPCF 仍为 repair_required，本轮只做 PKC-KDS 边界清单和 Loop 纳入，不升级项目整体状态。

## 2. 动作

1. 新增 `GlobalCloudPKC-KDS个人知识与贡献入口清单.md`。
2. 明确“KDS 管全局事实，PKC 管个人参与”的边界。
3. 定义个人知识、个人任务、个人贡献、个人积分、个人悬赏、个人 AI 服务和合作单位成员空间入口。
4. 将 PKC 个人对象挂接到 KDS 11 个底座资源池和积分池、悬赏池、额度池、争议池、贡献账本等增强治理账本。
5. 明确葛化物流和湖北磷材试点中 PKC 的第一阶段作用。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| PKC-KDS 入口清单 | `03-data-ai-knowledge/GlobalCloudPKC-KDS个人知识与贡献入口清单.md` | 定义个人知识、任务、积分、悬赏、AI 服务和成员空间如何接入 KDS |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-016.md` | 记录本轮输入、动作、输出、检查和反馈 |

## 4. 检查

已执行以下治理检查：

```bash
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

并执行 DKS-016 范围内的 `git diff --check`。

检查结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| 文档控制 | pass | 新增文档进入 README、文档控制台账、KDS 开发空间同步台账和 `.kds` 本地镜像 |
| DKS-016 局部 `git diff --check` | pass | DKS-016 相关源文件、台账和镜像无空白格式错误 |
| 污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass`，`missing_metadata=0`，`missing_readme_dirs=0` |

本轮只声明 DKS-016 范围内门禁通过；不改变 GFIS / GPCF 既有修复状态，不升级项目整体状态。

## 5. 反馈

本轮把 PKC 从“个人入口”收口为受 KDS、WAES、MMC、GPCF 和委员会机制约束的个人知识、个人贡献和个人 AI 服务入口。

本轮不创建真实账号、不写生产系统、不开放真实资料、不启动真实 AI 服务计费、不确认订单、质量、POD、到账、收益、积分或业务完成。

## 6. 下一轮建议

```text
GPCF-KDS-DKS-017：
KDS 11 池与增强治理账本项目群级映射。
```

建议下一轮把 12 个项目贡献 / 消费的知识、事实、证据、SOP、积分、收益、额度、悬赏、争议、权限和 Loop 证据统一映射到 KDS 11 个底座资源池。
