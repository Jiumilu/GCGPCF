---
doc_id: GPCF-DOC-GCWORLD-024
title: GCWORLD KDS只读普查准入核验记录
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, MMC, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/artifacts/gcworld-kds-readonly-admission-assessment-20260823.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/artifacts/gcworld-kds-readonly-admission-assessment-20260823.md
sync_direction: bidirectional
last_reviewed: 2026-08-23
supersedes: []
superseded_by: []
---

# GCWORLD KDS只读普查准入核验记录

## 核验结论

GCWORLD 已取得范围明确的KDS只读来源授权，并已按用户确认完成KDS保全式整理和4个既有提交的普通快进推送。推送当时KDS工作树为干净状态，本地与远端主分支完全一致；其后本地服务形成10项新变化，当前F-013实际准入恢复为 `blocked_dirty_worktree`。本轮已基于该10项变化稳定不变的隔离快照完成全来源受控分级；实时KDS中的10项变化未被清理、移动或写入。

## 授权基线

| 项目 | 当前事实 |
| --- | --- |
| 授权文件 | `artifacts/gcworld-kds-readonly-source-authorization-v1.yaml` |
| 授权文件摘要值 | `3869c1a6f015c8a957827170f35cf9d28feccd0f5accf3ed03e1df3fd558aba2` |
| 允许的元数据范围 | 全KDS空间及默认纳入的事实来源 |
| 允许的内容范围 | S0、S1、S2本地只读分析 |
| S3边界 | 仅登记存在性和受控指针，不读取正文、不生成预览、不进入智能体记忆 |
| 人工争议裁决责任 | 老卢，当前任务发起人，临时承担最终人工裁决 |
| 写入授权 | 无 |

## KDS工作树状态演进

| 指标 | 初次只读核验 | 保全授权执行前 | 保全后 | 推送后 | 当前隔离快照基线 |
| --- | --- | --- | --- | --- | --- |
| 当前提交 | `cbeeddc86e6c08a3be7357971a5bc430a10c0027` | 同左 | 同左 | 同左 | 同左 |
| 远端主分支 | `2ac85c55163b7acf0ede699184ac360579ccefaa` | 同左 | 同左 | `cbeeddc86e6c08a3be7357971a5bc430a10c0027` | 同左 |
| 远端领先、本地领先 | 0、4 | 0、4 | 0、4 | 0、0 | 0、0 |
| 工作树变更项 | 417 | 773 | 0 | 0 | 10 |
| 工作树状态摘要值 | `ad8c6775feb1899649e19e17c5834366d36fa573e0bca37d04df68bc3b253284` | `ba9e5be785b3e0127ef537fba129fef636d13850af68798d61ba05b3d4475337` | 空工作树 | 空工作树 | `67e20664ee229add0bd5c7ca9b84fde2bab73933847b946db06682f08a843a29` |

417项是初次核验时的汇总状态；持续运行的本地服务随后新增了文件，保全前在暂停写入方并连续复核后，稳定基线为773项。保全后HEAD和领先关系保持不变，工作树变更为0。773项均已被保全对象覆盖，路径集合及内容恢复演练无缺失、无额外项、无不一致项。

## 准入校验结果

当前执行F-013 KDS应用准入校验得到：

- 规划产物完整，OpenSpec严格校验通过；
- KDS契约镜像完整且摘要匹配；
- KDS工作树有10项既存变化；
- 本地与远端主分支完全一致，领先和落后均为0；
- 实际准入状态为 `blocked_dirty_worktree`；
- KDS写入授权为否；
- 部署授权为否；
- 完成状态为 `not_complete`。

## GKE-001读取约束

1. 只允许本地文件系统读取，不允许调用KDS或MMC写接口。
2. 已形成可复放的稳定快照；在逐路径权威分级门禁完成前，不执行未决来源的S0—S2内容提取。
3. S3只登记存在性，不读取正文、字段、附件、缩略图或向量内容。
4. 所有来源必须进入明确处置台账，解析失败、重复、镜像、归档和未分类项不得静默遗漏。
5. 人员或组织身份不得自动合并；争议必须进入老卢负责的人工裁决队列。
6. 除本次已明确授权并完成的4个既有提交快进推送外，后续仍不允许新增推送、部署、修改KDS正文或调用写接口。

## 解除条件

元数据普查已完成。只有同时满足以下剩余条件，才可进入确定性只读读取器的内容普查：

- 建立独立、权威、先判级后开文件的逐路径分级清单；
- 重新核验授权文件仍有效且来源范围未扩大；
- 执行前记录新的KDS提交、工作树和来源清单快照。

当前来源层分级处置已经完成，但身份归一、例外复核和事实提升尚未完成。状态应保持 `partial / rework`，不得声明已覆盖全部人员组织、已完成世界初始化、已集成或生产就绪。
