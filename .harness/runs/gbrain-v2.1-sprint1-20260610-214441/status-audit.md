# Harness Governance: gbrain-v2.1-sprint1

## Sprint 1 — 权限引擎硬化

### 交付清单

| 文件 | 状态 |
|------|------|
| `server/services/permissions.py` | ✅ 重写为正式决策引擎 |
| `server/services/tenants.py` | ✅ 新增，4 租户 + 6 角色 |
| `server/services/masking.py` | ✅ 新增，snippet + content masking |
| `server/routes/admin_permissions.py` | ✅ 新增，tenant/role/test 端点 |
| `tests/test_permissions.py` | ✅ 8 tests, all pass |

### 权限判定顺序（已固化）

```
explicit_deny → expired → exception_allow
  → tenant_allow → role_allow → sensitivity_allow
```

### 测试覆盖 8/8

| 场景 | 预期 | 结果 |
|------|------|------|
| S0 public | ALLOW | ✅ |
| explicit deny (observer excluded) | DENY | ✅ |
| expired grant | DENY | ✅ |
| exception allow (temporary S2 grant) | ALLOW | ✅ |
| tenant mismatch (gehua → hblc) | DENY | ✅ |
| role allow (engineer in roles list) | ALLOW | ✅ |
| sensitivity exceeded (observer S0 → S2 page) | DENY | ✅ |
| can_read_page wrapper (None ctx) | ALLOW | ✅ |

### API 验证

`/admin/permissions/test?tenant=gehua&role=observer&sensitivity=S0`:
- S0: ALLOW ✅
- S1: DENY (sensitivity_exceeded) ✅
- S2 cross-tenant: DENY (tenant_mismatch) ✅

### 判定: ready_for_human_acceptance
