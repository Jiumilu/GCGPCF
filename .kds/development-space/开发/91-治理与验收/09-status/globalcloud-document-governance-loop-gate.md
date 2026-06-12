---
doc_id: GPCF-DOC-71779DF3C3
title: GlobalCloud 文档治理 Loop 门禁
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-document-governance-loop-gate.md
source_path: 09-status/globalcloud-document-governance-loop-gate.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 文档治理 Loop 门禁

日期：2026-06-12
状态：v1.0
适用范围：GlobalCloud 项目群全部 Loop

## 1. 门禁定位

本文档定义文档治理如何影响 Loop Engineering 状态升级。

文档治理门禁是状态升级前置条件，不是附属检查。

## 2. 门禁矩阵

| 检查项 | 通过条件 | 失败状态 |
|---|---|---|
| 文档元数据 | 所有可修改 Markdown 有 doc_id | rework_required |
| 目录 README | 文档目录均有 README | rework_required |
| KDS 同步 | 本地镜像和同步流水数量一致 | partial / blocked |
| TOKEN 安全 | 专用 TOKEN 配置存在且不泄漏 | blocked |
| 污染检查 | 旧口径、旧定位、真实性污染为 0 | rework_required |
| 文档债务 | 无未关闭文档债务 | partial |

## 3. 状态上限

| 情况 | 状态上限 |
|---|---|
| 文档控制通过、KDS 同步通过、TOKEN 通过、无污染 | 可进入下一状态 |
| 有文档债务 | partial |
| KDS TOKEN 缺失 | blocked |
| 旧口径污染命中 | rework_required |
| KDS 冲突未处理 | blocked |

## 4. 执行命令

```bash
python3 tools/kds-sync/loop_document_gate.py
```

输出结果必须进入本轮 Loop evidence。
