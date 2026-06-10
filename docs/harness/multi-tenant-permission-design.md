# GBrain 多租户知识库权限体系 — v3.1 Hardening

> 版本: v3.1
> 日期: 2026-06-10
> 状态: 设计阶段（P0 可落地）
> 变更: 修正权限判断顺序、统一 ID 规范、修复脱敏实现、API Key hash化、收敛 P0

---

## 一、需求全景

### 1.1 租户定义

| ID | 显示名 | 性质 | 核心诉求 |
|----|--------|------|---------|
| `gehua` | 葛化 | 工厂建设/运营 | 工厂图纸、设备参数、SOP、成本测算 |
| `hblc` | 湖北磷材供应链 | 销售/原料供应 | 客户报价、采购订单、原料行情 |
| `cjsl` | 长江数联 | 平台运营/建设 | 技术架构、运维手册、部署方案 |
| `csy` | 楚商云 | 供应链生态合作 | 合作框架、商机信息、生态协同 |

### 1.2 权限判定优先级（新增）

```
1. explicit_deny     — 显式排除（exclude_roles, revoked key）
2. expired           — 已过期（key expiry, exception until）
3. exception_allow   — 临时授权例外
4. tenant_allow      — 租户匹配（含跨租户组）
5. role_allow        — 角色匹配
6. sensitivity_allow — 敏感级匹配

判定逻辑: 任一 deny → 立即拒绝；过期 → 拒绝；全部 allow → 放行
```

### 1.3 敏感度分级

| 级别 | 含义 | 默认可见 |
|:---:|------|---------|
| S0 | 公开 | 所有人（含未认证） |
| S1 | 内部 | 所有认证租户 |
| S2 | 受限 | 本租户内指定角色 |
| S3 | 机密 | 指定人员列表 |
| — | field_level | 模式标记（非独立级别，见 §五） |

---

## 二、权限模型（修正）

### 2.1 修正后的 can_access()

```python
def can_access(doc: dict, ctx: PermissionContext) -> bool:
    # ---- 1. explicit deny (最高优先级) ----
    if ctx.role in doc.get("visibility", {}).get("exclude_roles", []):
        log_audit("deny", ctx, doc, "exclude_role")
        return False

    # ---- 2. expired ----
    if ctx.expired:
        log_audit("deny", ctx, doc, "key_expired")
        return False

    # ---- 3. exception allow ----
    for exc in doc.get("visibility", {}).get("exceptions", []):
        if exc["user_id"] == ctx.user_id:
            if not exc.get("until") or datetime.fromisoformat(exc["until"]) > datetime.now():
                log_audit("allow", ctx, doc, "exception")
                return True
    # 即使有例外但已过期，继续走下面流程，不在此处拒绝

    # ---- 4. tenant_allow ----
    doc_tenants = doc.get("visibility", {}).get("tenants", [doc.get("project", "")])
    tenant_in_doc = ctx.tenant_id in doc_tenants

    if not tenant_in_doc:
        # 跨租户组只解决"租户候选"，不直接放行
        group_match = False
        for g in doc.get("visibility", {}).get("groups", []):
            if ctx.tenant_id in CROSS_TENANT_GROUPS.get(g, {}).get("members", []):
                group_match = True
                break
        if not group_match:
            log_audit("deny", ctx, doc, "tenant_mismatch")
            return False

    # ---- 5. role_allow ----
    doc_roles = doc.get("visibility", {}).get("roles", [])
    if doc_roles and ctx.role not in doc_roles:
        log_audit("deny", ctx, doc, "role_mismatch")
        return False

    # ---- 6. sensitivity_allow ----
    doc_level = doc.get("visibility", {}).get("level", "S1")
    if sensitivity_value(doc_level) > sensitivity_value(ctx.max_sensitivity):
        log_audit("deny", ctx, doc, "sensitivity_exceeded")
        return False

    log_audit("allow", ctx, doc, "all_checks_passed")
    return True
```

### 2.2 修正后的字段可见性

```python
def field_visible(field: dict, ctx: PermissionContext) -> bool:
    """field: {level, visible_roles, visible_users, visible_tenants}"""
    if not field.get("level"):
        return True
    if sensitivity_value(field["level"]) <= sensitivity_value(ctx.max_sensitivity):
        return True
    if ctx.role in field.get("visible_roles", []):
        return True
    if ctx.user_id in field.get("visible_users", []):
        return True
    if ctx.tenant_id in field.get("visible_tenants", []):
        return True
    return False
```

---

## 三、数据模型

### 3.1 ID 规范（新增）

```
所有权限字段使用稳定英文 ID:
  tenant_id: gehua, hblc, cjsl, csy
  role_id:   admin, engineer, operator, observer
  user_id:   zhangsan, lisi  (唯一标识)

显示名仅用于 UI 展示，通过 tenant-permissions.json 映射:
  gehua → "葛化"
  admin → "管理员"
```

### 3.2 文档 Frontmatter（修正）

```yaml
---
title: PP原料采购成本测算
project: gehua                         # 统一英文 ID
type: cost_analysis
created: 2026-06-05

visibility:
  level: S2
  tenants: [gehua, hblc]               # 英文 ID
  roles: [admin, purchasing, engineer]
  exclude_roles: [observer]
  groups: [gehua-hblc-cjsl]

  exceptions:
    - user_id: auditor-001
      level: S2
      until: "2026-07-01T00:00:00Z"
      reason: "季度审计"

sensitivity:
  mode: field_level                    # 非 S4 独立级别，而是模式标记
  fields:
    - label: PP原料单价                # Markdown 内标签匹配
      level: S3
      visible_roles: [admin, purchasing]
      mask: "***"
    - path: frontmatter.price.pp       # frontmatter 路径
      level: S3
      visible_roles: [admin]
      mask: "--"
    - table_column: 供应商报价          # 表格列名匹配
      level: S3
      visible_roles: [admin]
      mask: "[商业机密]"

  sections:
    - heading: "供应商分析"             # 任意级标题
      level: S3
      visible_roles: [admin, purchasing]
      replacement: "[此部分包含供应商商业信息，需更高权限查看]"
    - heading: "成本明细"
      level: S2
      visible_roles: [admin, engineer, purchasing]
      replacement: "[成本明细需授权查看]"
---
```

### 3.3 租户-角色配置（修正）

```json
{
  "keys": [
    {
      "key_id": "gh-ops-1c4e",
      "key_hash": "sha256:a1b2c3d4e5f6...",
      "tenant_id": "gehua",
      "role": "operator",
      "user_id": "wangwu",
      "max_sensitivity": "S1",
      "tags": ["日报", "工单"],
      "status": "active",
      "created": "2026-06-01",
      "expires": null
    },
    {
      "key_id": "gh-adm-8a3f",
      "key_hash": "sha256:f6e5d4c3b2a1...",
      "tenant_id": "gehua",
      "role": "admin",
      "user_id": "zhangsan",
      "max_sensitivity": "S3",
      "tags": ["*"],
      "status": "active"
    }
  ],

  "tenants": {
    "gehua": {
      "display": "葛化磷石膏高值化利用示范项目",
      "roles": {
        "admin":    {"level": 4, "max_sensitivity": "S3", "permissions": ["read","write","delete","grant","audit"]},
        "engineer": {"level": 3, "max_sensitivity": "S2", "permissions": ["read","write"]},
        "operator": {"level": 2, "max_sensitivity": "S1", "permissions": ["read"]},
        "observer": {"level": 1, "max_sensitivity": "S1", "permissions": ["read"], "readonly": true}
      }
    },
    "hblc": {
      "display": "湖北磷材供应链",
      "roles": {
        "admin":      {"level": 4, "max_sensitivity": "S3", "permissions": ["read","write","delete","grant","audit"]},
        "sales":      {"level": 3, "max_sensitivity": "S2", "permissions": ["read","write"]},
        "purchasing": {"level": 3, "max_sensitivity": "S2", "permissions": ["read","write"]}
      }
    },
    "cjsl": {
      "display": "长江数联",
      "roles": {
        "admin":    {"level": 4, "max_sensitivity": "S3", "permissions": ["read","write","delete","grant","audit"]},
        "engineer": {"level": 3, "max_sensitivity": "S2", "permissions": ["read","write"]}
      }
    },
    "csy": {
      "display": "楚商云",
      "roles": {
        "admin":    {"level": 3, "max_sensitivity": "S2", "permissions": ["read","write"]},
        "observer": {"level": 1, "max_sensitivity": "S1", "permissions": ["read"], "readonly": true}
      }
    }
  },

  "cross_tenant_groups": {
    "gehua-hblc-cjsl": {
      "display": "葛化-磷材-数联 三方协作",
      "members": ["gehua", "hblc", "cjsl"]
    }
  }
}
```

---

## 四、内容脱敏引擎（重写）

### 4.1 三类字段匹配

字段脱敏不再用文字替换，改为定位匹配：

| 匹配类型 | 声明方式 | 示例 |
|---------|---------|------|
| frontmatter 路径 | `path: frontmatter.price.pp` | 直接取 YAML 值 |
| Markdown 表格列 | `table_column: PP原料单价` | 匹配表头，替换该列所有单元格 |
| 文内标签 | `label: PP原料单价` | 匹配 `**PP原料单价**：5910元/吨` 中冒号后的值 |

```python
def mask_field(doc_ast: dict, field: dict, ctx: PermissionContext) -> dict:
    if field_visible(field, ctx):
        return doc_ast

    match field.get("match_type"):
        case "path":
            # frontmatter.price.pp → doc_ast["frontmatter"]["price"]["pp"]
            keys = field["path"].split(".")[1:]  # 跳过 "frontmatter."
            target = doc_ast["frontmatter"]
            for k in keys:
                target = target.get(k, {})
            if isinstance(target, str):
                doc_ast["masked"].append({"path": field["path"], "original_hash": sha256(target)})
                target = field["mask"]  # 替换值

        case "table_column":
            for table in doc_ast.get("tables", []):
                if field["table_column"] in table["headers"]:
                    col_idx = table["headers"].index(field["table_column"])
                    for row in table["rows"]:
                        row[col_idx] = field["mask"]

        case "label":
            # Markdown: **PP原料单价**：5910元/吨 → **PP原料单价**：***
            pattern = re.compile(rf'(\*\*{re.escape(field["label"])}\*\*[：:]\s*)(\S+)')
            doc_ast["body"] = pattern.sub(rf'\1{field["mask"]}', doc_ast["body"])

    return doc_ast
```

### 4.2 Markdown AST 段落屏蔽

不再用正则匹配标题，改用 AST 解析：

```python
def mask_sections(doc_ast: dict, sections: list, ctx: PermissionContext):
    for sec in sections:
        if field_visible(sec, ctx):
            continue
        for node in doc_ast.get("headings", []):
            if node["text"] == sec["heading"]:
                # 找到该标题对应的内容块（到下一个同级或更高级标题为止）
                block = extract_section_block(doc_ast, node)
                block["body"] = sec["replacement"]
                block["masked"] = True
```

### 4.3 索引侧权限元数据（新增）

```python
# 索引入库时，每个 chunk 带权限元数据
chunk_metadata = {
    "tenant_ids": doc.get("visibility", {}).get("tenants", [doc.get("project")]),
    "visibility_level": doc.get("visibility", {}).get("level", "S1"),
    "allowed_roles": doc.get("visibility", {}).get("roles", []),
    "source_doc_id": doc["slug"],
    "sensitivity_fields": [
        {"label": f["label"], "level": f["level"]}
        for f in doc.get("sensitivity", {}).get("fields", [])
    ]
}

# 查询时先做 metadata filter，再做 snippet mask
results = gbrain.query(query, metadata_filter={
    "tenant_ids": {"$in": [ctx.tenant_id]},
    "visibility_level": {"$lte": ctx.max_sensitivity}
})
```

索引阶段就带权限元数据，避免敏感 chunk 参与召回后再被过滤暴露存在性。

---

## 五、安全模型（修正）

### 5.1 生产/调试双模式响应

```python
DEBUG_MODE = os.environ.get("GBRAIN_DEBUG", "false") == "true"

def build_response(results, filtered, ctx):
    resp = {
        "results": results,
        "meta": {
            "tenant": ctx.tenant_id,
            "visible": len(results)
        }
    }

    if DEBUG_MODE or ctx.role == "admin":
        # 仅开发/管理员返回详细过滤统计
        resp["debug_filtered"] = {
            "total_from_gbrain": filtered["total"],
            "filtered_by_tenant": filtered["by_tenant"],
            "filtered_by_sensitivity": filtered["by_sensitivity"]
        }
    elif len(results) == 0 and filtered["total"] > 0:
        # 普通用户：有结果但全被过滤，不暴露数量
        resp["meta"]["message"] = "未找到匹配结果"

    return resp
```

### 5.2 信任边界（修正）

```python
def extract_tenant(request):
    # 1. 丢弃客户端传入的 X-Tenant（不可信）
    # 2. 从 API Key 解析 tenant_id（权威来源）
    key = request.headers.get("X-API-Key", "")
    key_info = lookup_key(key)
    if not key_info or key_info["status"] != "active":
        raise AuthError("invalid_key")

    resolved_tenant = key_info["tenant_id"]

    # 3. 域名期望租户（仅用于交叉校验，不作为授权依据）
    expected_tenant = request.headers.get("X-Expected-Tenant", "")
    if expected_tenant and expected_tenant != resolved_tenant:
        log_alert("tenant_mismatch", {
            "expected": expected_tenant,
            "resolved": resolved_tenant,
            "key_id": key_info["key_id"]
        })
        raise AuthError("tenant_mismatch")

    return PermissionContext(
        tenant_id=resolved_tenant,
        role=key_info["role"],
        user_id=key_info["user_id"],
        max_sensitivity=key_info["max_sensitivity"],
        tags=key_info.get("tags", []),
        readonly=key_info.get("readonly", False),
        expired=key_info.get("expires") and datetime.fromisoformat(key_info["expires"]) < datetime.now()
    )
```

### 5.3 API Key 只保存 Hash

```python
# 生成时
def create_api_key(tenant_id, role, user_id):
    raw_key = secrets.token_hex(16)        # 32字符 hex
    key_hash = sha256(raw_key.encode()).hexdigest()
    key_id = f"{tenant_id[:2]}-{role[:3]}-{raw_key[:4]}"
    save_key({"key_id": key_id, "key_hash": key_hash, "tenant_id": tenant_id, ...})
    return raw_key  # 仅此一次展示

# 验证时
def lookup_key(raw_key):
    key_hash = sha256(raw_key.encode()).hexdigest()
    for key in keys_config["keys"]:
        if key["key_hash"] == key_hash and key["status"] == "active":
            return key
    return None
```

---

## 六、收敛后的实施路线

### P0-A: 租户隔离（最小闭环）

| # | 任务 | 验收标准 |
|---|------|---------|
| 1 | tenant_id 全部统一为英文 | gehua/hblc/cjsl/csy |
| 2 | frontmatter 支持 `visibility.tenants` | 英文 ID，无默认值 |
| 3 | 查询结果按 tenant 过滤 | can_access 第4步 |
| 4 | 无 frontmatter 默认不可跨租户 | S1 + 仅 project 租户 |
| 5 | API Key hash 化 | 文件存 sha256，展示仅一次 |
| 6 | 审计日志 | request_id, tenant_id, role, query, visible_count |
| 7 | 信任边界：丢弃客户端 X-Tenant | 仅以 key 解析结果为准 |
| 8 | 禁止跨租户组跳过角色/敏感级 | can_access 先判断 tenant，继续走 role/sensitivity |

### P0-B: 文档级敏感度

| # | 任务 | 验收标准 |
|---|------|---------|
| 1 | S0/S1/S2/S3 文档级判断 | can_access 第6步 |
| 2 | role max_sensitivity 生效 | operator(S1) 不能看 S2+ |
| 3 | exclude_roles > allow | 显式排除立即拒绝 |
| 4 | 12 种权限组合测试通过 | 4租户 × 3角色 |
| 5 | 域名校验不通过 → 拒绝 | tenant_mismatch → 401 |
| 6 | 生产模式不返回 filtered 明细 | 普通用户看不到数量 |

### P1: 内容脱敏

| # | 任务 | 验收标准 |
|---|------|---------|
| 1 | 字段级脱敏（三类匹配） | path/table_column/label |
| 2 | Markdown AST 段落屏蔽 | 任意级标题 |
| 3 | 搜索摘要脱敏 | 返回层 mask |
| 4 | 索引侧权限元数据 | chunk 带 tenant_ids + level |

### P2: 高级特性

| # | 任务 |
|---|------|
| 1 | 跨租户共享组 |
| 2 | 临时授权 + 过期自动失效 |
| 3 | API Key 轮换 |
| 4 | ECS 多域名部署 |

---

## 七、测试矩阵（P0 验收）

| # | 租户 | 角色 | 文档 properties | 预期 |
|---|------|------|---------------|------|
| 1 | gehua | admin | S3, tenants=[gehua] | ✅ 可见全文 |
| 2 | gehua | operator | S3, tenants=[gehua] | ❌ 不可见 |
| 3 | gehua | operator | S1, tenants=[gehua] | ✅ 可见 |
| 4 | hblc | sales | S2, tenants=[gehua] | ❌ 租户不匹配 |
| 5 | hblc | sales | S2, tenants=[gehua,hblc] | ✅ 跨租户 |
| 6 | hblc | sales | S3, tenants=[gehua,hblc] | ❌ 敏感级不足 |
| 7 | gehua | engineer | S2, exclude_roles=[engineer] | ❌ 显式排除 |
| 8 | gehua | observer | S1, tenants=[gehua] | ✅ 可见 |
| 9 | csy | observer | S2, tenants=[gehua,hblc,cjsl,csy] | ❌ max_sensitivity=S1 |
| 10 | gehua | admin | 无 frontmatter | ✅ S1 + project 租户 |
| 11 | hblc | admin | 无 frontmatter, project=gehua | ❌ 租户不匹配 |
| 12 | — | — | S0 | ✅ 未认证也可见 |

### 测试命令

```bash
# 逐条验证
curl -H "X-API-Key: gh-ops-1c4e" http://127.0.0.1:19828/search?q=成本  # 场景2
curl -H "X-API-Key: lc-sal-3f8b" http://127.0.0.1:19828/search?q=成本  # 场景5
```

---

> **关联文档**:
> - `docs/harness/project-isolation-design.md` (P2-2 早期设计)
> - `docs/harness/project-backfill-phase2.md` (Phase 2 待确认清单)
