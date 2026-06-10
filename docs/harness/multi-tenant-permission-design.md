# GBrain 多租户知识库权限体系 — v3.1.1 Implementation Patch

> 版本: v3.1.1
> 日期: 2026-06-10
> 状态: P0 可实施基线
> 变更: 修正 exception 敏感级判断、S1 语义澄清、effective_tenant_ids、补 15 条测试用例

---

## 一、需求全景

### 1.1 租户定义

| ID | 显示名 | 性质 | 核心诉求 |
|----|--------|------|---------|
| `gehua` | 葛化 | 工厂建设/运营 | 工厂图纸、设备参数、SOP、成本测算 |
| `hblc` | 湖北磷材供应链 | 销售/原料供应 | 客户报价、采购订单、原料行情 |
| `cjsl` | 长江数联 | 平台运营/建设 | 技术架构、运维手册、部署方案 |
| `csy` | 楚商云 | 供应链生态合作 | 合作框架、商机信息、生态协同 |

### 1.2 权限判定优先级

```
1. explicit_deny     — 显式排除（exclude_roles, revoked key）
2. expired           — 已过期（key expiry, exception until 过期）
3. exception_allow   — 临时授权例外（仍需过敏感级判断）
4. tenant_allow      — 租户匹配（含跨租户组）
5. role_allow        — 角色匹配
6. sensitivity_allow — 敏感级匹配

判定逻辑: 任一 deny → 立即拒绝；过期 → 拒绝；全部 allow → 放行
```

### 1.3 敏感度分级

| 级别 | 语义 | 默认可见 |
|:---:|------|---------|
| S0 | 公开 | 所有人（含未认证） |
| S1 | 内部 | 认证后可见，仍受 tenants/groups 限制 |
| S2 | 受限 | 本租户内指定角色 |
| S3 | 机密 | 指定人员列表 |
| — | field_level | 模式标记（非独立级别，见 §五） |

> **S1 与跨租户的关系**：S1 = "认证用户可在其有权限的租户/组范围内查看"，**不等于**所有认证租户可见。如需全平台可见，显式声明 `tenants: [gehua, hblc, cjsl, csy]` 或使用 `groups: [all-tenants]`。

---

## 二、权限模型

### 2.1 修正后的 can_access()

```python
def can_access(doc: dict, ctx: PermissionContext) -> bool:
    # ---- S0: 公开，直接放行 ----
    doc_level = doc.get("visibility", {}).get("level", "S1")
    if doc_level == "S0":
        return True

    # ---- 1. explicit deny ----
    if ctx.role in doc.get("visibility", {}).get("exclude_roles", []):
        log_audit("deny", ctx, doc, "exclude_role")
        return False

    # ---- 2. expired ----
    if ctx.expired:
        log_audit("deny", ctx, doc, "key_expired")
        return False

    # ---- 3. exception_allow (修正: 仍需过敏感级) ----
    for exc in doc.get("visibility", {}).get("exceptions", []):
        if exc["user_id"] == ctx.user_id:
            if not expired(exc.get("until")):
                exc_level = exc.get("level", ctx.max_sensitivity)
                if sensitivity_value(exc_level) >= sensitivity_value(doc_level):
                    log_audit("allow", ctx, doc, "exception")
                    return True
                else:
                    # 临时授权敏感级不足，禁止访问
                    log_audit("deny", ctx, doc, "exception_level_insufficient")
                    return False
            # exception 已过期，不在此处拒绝，继续走下面流程

    # ---- 4. tenant_allow ----
    doc_tenants = doc.get("visibility", {}).get("tenants", [doc.get("project", "")])
    tenant_in_doc = ctx.tenant_id in doc_tenants

    if not tenant_in_doc:
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
    if sensitivity_value(doc_level) > sensitivity_value(ctx.max_sensitivity):
        log_audit("deny", ctx, doc, "sensitivity_exceeded")
        return False

    log_audit("allow", ctx, doc, "all_checks_passed")
    return True
```

### 2.2 field_visible()（修正：可见性作用域约束）

```python
def field_visible(field: dict, ctx: PermissionContext, doc_tenants: list) -> bool:
    """
    字段级可见性。visible_roles 仅在文档级 can_access 通过后生效。
    对跨租户共享文档，字段级 visible_roles 按 tenant 分组校验。
    """
    if not field.get("level"):
        return True
    if sensitivity_value(field["level"]) <= sensitivity_value(ctx.max_sensitivity):
        return True
    # 带作用域的 visible_roles
    for entry in field.get("visible_roles", []):
        if isinstance(entry, str):
            # 简化：仅本租户内角色
            if ctx.tenant_id in doc_tenants and ctx.role == entry:
                return True
        elif isinstance(entry, dict):
            # 完整：指定租户+角色
            if ctx.tenant_id == entry.get("tenant_id") and ctx.role in entry.get("roles", []):
                return True
    if ctx.user_id in field.get("visible_users", []):
        return True
    if ctx.tenant_id in field.get("visible_tenants", []):
        return True
    return False
```

---

## 三、数据模型

### 3.1 ID 规范

```
所有权限字段使用稳定英文 ID:
  tenant_id: gehua, hblc, cjsl, csy
  role_id:   admin, engineer, operator, observer, sales, purchasing
  user_id:   zhangsan, lisi

显示名仅用于 UI，通过 tenant-permissions.json 映射。
```

### 3.2 文档 Frontmatter

```yaml
---
title: PP原料采购成本测算
project: gehua
type: cost_analysis
created: 2026-06-05

visibility:
  level: S2
  tenants: [gehua, hblc]               # 跨租户时显式列出
  roles: [admin, purchasing, engineer]
  exclude_roles: [observer]
  groups: [gehua-hblc-cjsl]

  exceptions:
    - user_id: auditor-001
      level: S2                        # 例外敏感级必须覆盖文档级
      until: "2026-07-01T00:00:00Z"
      reason: "季度审计"

sensitivity:
  mode: field_level
  fields:
    - label: PP原料单价
      level: S3
      visible_roles:
        - tenant_id: gehua
          roles: [admin, purchasing]
        - tenant_id: hblc
          roles: [admin]
      mask: "***"
    - table_column: 供应商报价
      level: S3
      visible_roles: [admin]
      mask: "[商业机密]"

  sections:
    - heading: "供应商分析"
      level: S3
      visible_roles: [admin, purchasing]
      replacement: "[此部分包含供应商商业信息，需更高权限查看]"
---
```

### 3.3 租户-角色配置

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
      "status": "active"
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
      "display": "葛化",
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
      "display": "葛化-磷材-数联",
      "members": ["gehua", "hblc", "cjsl"]
    },
    "all-tenants": {
      "display": "全平台共享",
      "members": ["gehua", "hblc", "cjsl", "csy"]
    }
  }
}
```

---

## 四、索引侧权限元数据

### 4.1 effective_tenant_ids（新增）

```python
def compute_effective_tenants(doc: dict) -> list:
    """索引时将 group 展开为 effective_tenant_ids"""
    explicit = doc.get("visibility", {}).get("tenants", [doc.get("project", "")])
    groups = doc.get("visibility", {}).get("groups", [])
    expanded = set(explicit)
    for g in groups:
        for member in CROSS_TENANT_GROUPS.get(g, {}).get("members", []):
            expanded.add(member)
    return sorted(expanded)

# 索引时写入 chunk metadata
chunk_metadata = {
    "effective_tenant_ids": compute_effective_tenants(doc),
    "visibility_level": doc.get("visibility", {}).get("level", "S1"),
    "allowed_roles": doc.get("visibility", {}).get("roles", []),
    "source_doc_id": doc["slug"]
}

# 查询时直接用 effective_tenant_ids 过滤，与 can_access() 语义一致
results = gbrain.query(query, metadata_filter={
    "effective_tenant_ids": {"$in": [ctx.tenant_id]},
    "visibility_level": {"$lte": ctx.max_sensitivity}
})
```

---

## 五、安全模型

### 5.1 生产/调试双模式

```python
DEBUG_MODE = os.environ.get("GBRAIN_DEBUG", "false") == "true"

def build_response(results, filtered, ctx):
    resp = {"results": results, "meta": {"tenant": ctx.tenant_id, "visible": len(results)}}

    if DEBUG_MODE or ctx.role == "admin":
        resp["debug_filtered"] = {
            "total_from_gbrain": filtered["total"],
            "filtered_by_tenant": filtered["by_tenant"],
            "filtered_by_sensitivity": filtered["by_sensitivity"]
        }
    elif len(results) == 0 and filtered["total"] > 0:
        resp["meta"]["message"] = "未找到匹配结果"

    return resp
```

### 5.2 信任边界

```python
def extract_tenant(request):
    key = request.headers.get("X-API-Key", "")
    key_info = lookup_key(key)
    if not key_info or key_info["status"] != "active":
        raise AuthError("invalid_key")

    resolved_tenant = key_info["tenant_id"]

    expected = request.headers.get("X-Expected-Tenant", "")
    if expected and expected != resolved_tenant:
        log_alert("tenant_mismatch", {"expected": expected, "resolved": resolved_tenant})
        raise AuthError("tenant_mismatch")

    return PermissionContext(tenant_id=resolved_tenant, role=key_info["role"], ...)
```

### 5.3 API Key Hash

```python
def create_api_key(tenant_id, role, user_id):
    raw_key = secrets.token_hex(16)
    key_hash = sha256(raw_key.encode()).hexdigest()
    key_id = f"{tenant_id[:2]}-{role[:3]}-{raw_key[:4]}"
    save_key({"key_id": key_id, "key_hash": key_hash, ...})
    return raw_key          # 仅展示一次

def lookup_key(raw_key):
    key_hash = sha256(raw_key.encode()).hexdigest()
    for key in keys_config["keys"]:
        if key["key_hash"] == key_hash and key["status"] == "active":
            return key
    return None
```

---

## 六、实施路线

### P0-A: 租户隔离

| # | 任务 | 验收 |
|---|------|------|
| 1 | tenant_id 全统一英文 | gehua/hblc/cjsl/csy |
| 2 | frontmatter `visibility.tenants` | 英文 ID |
| 3 | 查询按 tenant 过滤 | can_access step 4 |
| 4 | 无 frontmatter 默认不可跨租户 | S1 + 仅 project 租户 |
| 5 | API Key hash 化 | sha256，仅展示一次 |
| 6 | 审计日志 | request_id, tenant_id, role, query, visible_count |
| 7 | 信任边界 | 丢弃客户端 X-Tenant |
| 8 | 跨租户组不跳过角色/敏感级 | group 仅解决 tenant 候选 |

### P0-B: 文档级敏感度

| # | 任务 | 验收 |
|---|------|------|
| 1 | S0-S3 文档级判断 | can_access step 6 |
| 2 | role max_sensitivity 生效 | operator(S1) 不能看 S2+ |
| 3 | exclude_roles > allow | 立即拒绝 |
| 4 | exception 须过敏感级 | level=S1 的例外不能看 S3 |
| 5 | S1 = 认证 + tenant/group 范围内 | 非全认证租户可见 |
| 6 | 生产模式不返回 filtered 明细 | 普通用户看不到 |
| 7 | effective_tenant_ids 索引入库 | group 展开后写入 chunk |

### P1: 内容脱敏

| # | 任务 |
|---|------|
| 1 | 字段脱敏（path/table_column/label） |
| 2 | AST 段落屏蔽 |
| 3 | 搜索摘要脱敏 |

### P2: 高级特性

| # | 任务 |
|---|------|
| 1 | 跨租户共享组（前端） |
| 2 | 临时授权 + 过期 |
| 3 | Key 轮换 |
| 4 | ECS 多域名 |

---

## 七、P0 验收测试矩阵（15 条）

| # | 租户 | 角色 | 文档 | 预期 |
|---|------|------|------|------|
| 1 | gehua | admin | S3, tenants=[gehua] | ✅ |
| 2 | gehua | operator | S3, tenants=[gehua] | ❌ 敏感级 |
| 3 | gehua | operator | S1, tenants=[gehua] | ✅ |
| 4 | hblc | sales | S2, tenants=[gehua] | ❌ 租户 |
| 5 | hblc | sales | S2, tenants=[gehua,hblc] | ✅ |
| 6 | hblc | sales | S3, tenants=[gehua,hblc] | ❌ 敏感级 |
| 7 | gehua | engineer | S2, exclude_roles=[engineer] | ❌ 排除 |
| 8 | gehua | observer | S1, tenants=[gehua] | ✅ |
| 9 | csy | observer | S2, tenants=[gehua,hblc,cjsl,csy] | ❌ 敏感级 |
| 10 | gehua | admin | 无 frontmatter | ✅ S1+project |
| 11 | hblc | admin | 无 frontmatter, project=gehua | ❌ 租户 |
| 12 | — | — | S0 | ✅ 公开 |
| 13 | hblc | sales | S2, groups=[gehua-hblc-cjsl], roles=[admin] | ❌ 角色不匹配 |
| 14 | gehua | engineer | S3, exceptions=[{user:engineer,level:S1}] | ❌ 例外敏感级不足 |
| 15 | gehua | operator | S1, 全被过滤 | ✅ 空结果，无 filtered 计数 |

---

> **关联文档**: `docs/harness/project-isolation-design.md`、`docs/harness/project-backfill-phase2.md`
