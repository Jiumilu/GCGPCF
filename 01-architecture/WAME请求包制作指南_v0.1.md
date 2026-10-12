---
doc_id: GPCF-DOC-WAME-REQUEST-PACK-GUIDE-20261011
title: WAME 请求包制作指南
project: GPCF
related_projects: [GPCF, WAS, XWAIL, WAME, KDS]
domain: architecture
status: controlled
version: v0.1
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/WAME请求包制作指南_v0.1.md
source_path: 01-architecture/WAME请求包制作指南_v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# WAME 请求包制作指南 v0.1（S3 接入工具包）

- 日期：2026-10-11 ｜ 依据：《WAME统一审核请求机制_v0.1》（GPCF 01-architecture）
- 给谁用：**各系统提交方**（凡有内容需发往 WAME 审核/注册/发布者）
- 一句话：**三步做出合规请求包**——定类型 → 填信封 → 自检

## 一、三步流程

### 第 1 步 · 定类型（`requestType` 7 选 1）

| 类型 | 适用 |
|---|---|
| `asset_registration` | 资产/接口注册（含模型） |
| `domain_registration` | 域/域切片登记 |
| `term_request` | 术语/词表增补 |
| `state_request` | 状态词表增补 |
| `authorization` | 执行授权 |
| `repair_request` | 修复请求 |
| `other` | 兜底（须说明） |

### 第 2 步 · 填信封（10 必填）

`packageId`／`packageKind="request"`／`requestType`／`from`（你的系统名）／`to="wame"`／`subject`（对象名+ref）／`requestedDecision`（期望裁定，**留白**——不是你自己裁定）／`evidenceRefs[]`（≥1 条可核验引用）／`constraints{}`（scope 绑定＋non-claims）／`createdAt`。

**最小示例**（term_request）：

```json
{
  "packageId": "xap.request.term_request.yoursystem.20261011",
  "packageKind": "request",
  "requestType": "term_request",
  "from": "yoursystem",
  "to": "wame",
  "subject": {"name": "你要申请的术语", "ref": "出处文件"},
  "requestedDecision": "admit_xxx_candidate",
  "evidenceRefs": ["KDS:path/to/evidence.md"],
  "constraints": {"scope_binding": ["工业绿链(IGL)"], "non_claims": "不改动任何既有件；不声明裁定"},
  "currentDecision": "pending_governance_review",
  "createdAt": "2026-10-11"
}
```

### 第 3 步 · 自检（必须跑）

```bash
python3 "KDS/工业绿链/图谱/ontology/xwail-v12-poc/mkrequest.py" \
    --type <类型> --from <你的系统> --subject "名称|ref" \
    --decision "期望裁定" --evidence "来源:路径" --scope "绑定范围" \
    --out "你的请求包.json"          # ① 制作器直接生成合规骨架

python3 "KDS/工业绿链/图谱/ontology/xwail-v12-poc/requestcheck.py" "你的请求包.json"
# ② 检查器自检：期望输出「[PASS] 信封合规——…裁定留白 ✓」
```

## 二、常见错误速查（R01-R06 对照）

| 症状 | 原因 | 修法 |
|---|---|---|
| R01 拦 | `packageKind` 非 "request" | 改 `"request"` |
| R02 拦 | `requestType` 不在 7 枚举 | 对照 §一 表更正 |
| R03 拦 | 信封必填缺失（最高频：`subject`／`evidenceRefs`） | 对照 §二 清单补齐 |
| R04 拦 | `to` 不是 "wame" | 固定 `"wame"` |
| R05 拦 | `evidenceRefs` 空 | 至少 1 条（格式 `来源系统:路径`） |
| **R06 拦** | **`currentDecision` 自称了裁定**（如 "accepted"） | **一律 `"pending_governance_review"`**——裁定由治理方填写；既有裁定用 `traceability` 块引述 |

## 三、交接与边界

1. 请求包=**提交侧**准备件；送入 WAME 统一受理流程的时点由治理方决定（当前受理器待 WAME 立项——S4）；
2. 已有真实件参照：`KDS/工业绿链/图谱/ontology/requests/`（4 件，覆盖 3 类型）；
3. 本指南与机制文件冲突时以机制文件为准；**不声明**任何请求已受理。

> 工具链一览：`mkrequest.py`（制作）→ `requestcheck.py`（自检）→ [WAME 受理器]（识别/分流/回执——待 S4）。
