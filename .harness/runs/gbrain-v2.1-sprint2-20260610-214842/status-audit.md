# Harness Governance: gbrain-v2.1-sprint2

## Sprint 2 — 权限感知混合搜索 ✅

### 交付清单

| 文件 | 状态 |
|------|------|
| `services/search.py` | ✅ hybrid/ keyword/ semantic orchestrator |
| `services/highlight.py` | ✅ term highlight + snippet extraction |
| `services/vector_index.py` | ✅ TurboVec stub (pgvector fallback) |
| `routes/search.py` | ✅ `/api/search/v2` endpoint |
| `tests/test_search.py` | ✅ 4 tests |

### 搜索链路

```
query → keyword(tsquery) + semantic(gbrain query)
  → dedup merge → permission filter → snippet → response
```

### 验证

| 测试 | 结果 |
|------|------|
| 关键词搜索 `工业绿链` | 3 results, match_type=["keyword"] ✅ |
| 权限过滤 (observer S0) | S2 pages filtered out ✅ |
| 无 ctx 搜索 | all results returned ✅ |

### 全量测试: 17/17 ✅

### 判定: ready_for_human_acceptance
