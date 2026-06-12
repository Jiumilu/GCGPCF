## Architecture Overview

KDS v3.1 re-architects the v3.0 flat `services/` directory into 6 domain layers:

```
server/
  core/         — config, db pool, auth, errors, logging
  knowledge/    — search, render, graph, embed, vector_index
  governance/   — permissions, tenants, masking, dq, repair_tasks, evidence, audit
  operations/   — reports, batch_actions, notifications, trends
  agent/        — agent_tasks, patch_review, conflict_detection, workspace
  platform/     — project_registry, connectors
  routes/       — 10 route files (ops, frontend, admin, admin_agent, admin_audit, admin_dq, admin_operations, admin_permissions, admin_platform)
```

## Key Design Decisions

### 1. Unified Config (Single Source of Truth)
All configuration merges from: env vars > .env > defaults. No duplicate `config.py` in subdirectories. Sensitive values (session_secret, csrf_secret) are auto-generated with `os.urandom(32)` if not provided.

### 2. Session + CSRF Auth
- `itsdangerous.URLSafeTimedSerializer` for signed session cookies
- CSRF tokens bound to session via HMAC-SHA256
- Cookie attributes: HttpOnly, SameSite=Lax, Secure (production)
- API keys: SHA-256 hashed, scoped (comma-separated), with expires_at/last_used_at/is_revoked

### 3. Permission Decision Engine (Immutable Order)
Six-step fixed order: explicit_deny -> expired -> exception_allow -> tenant_allow -> role_allow -> sensitivity_allow. Every decision returns structured output with reason, matched_rule, tenant, role, sensitivity. Tenant and sensitivity filters pushed to SQL WHERE clauses to prevent in-memory post-retrieval filtering.

### 4. Seven-Dimension DQ Scoring
Weighted average: authority(20%), freshness(20%), completeness(15%), metadata(15%), link_health(10%), duplication(10%), security(10%). Each dimension returns (score, issues[]) for actionable feedback.

### 5. Agent Four-Layer Defense
Layer 1: Workspace isolation (`.harness/runs/<id>/workspaces/`)
Layer 2: Patch allowlist (file extension + path rules)
Layer 3: Static risk scan (SQL DROP, os.system, import os, permission changes)
Layer 4: Human review (required for risk >= medium)

### 6. Audit Architecture
PostgreSQL `audit_events` = primary fact source (queryable). JSONL file = append-only archive. Writes go DB-first, then JSONL. Queries only hit DB. Each event carries request_id, session_id, ip_hash, user_agent_hash, route, method, status_code, latency_ms.

### 7. API Versioning
All routes under `/api/v1/` prefix. Backward compatible with v3.0 paths via redirect layer. Unified response format: `{ok, data, error, meta}` with request_id and version.

## Data Model Changes

New tables: schema_migrations, api_keys, evidence_ledger, notifications, projects (v3.1 schema migration `001_v3.1_schema.sql`).

New columns on existing tables: created_at, updated_at, created_by, updated_by, deleted_at, version on all core tables. Embedding versioning fields (embedding_model, embedding_dimension, chunking_strategy, chunk_hash, content_hash) on content_chunks.

## Frontend Architecture

Admin panel modularized into shell (`index.html` + `app.js` + `app.css`) with 7 page modules (dashboard, dq, permissions, audit, agent, operations, platform) and 4 reusable components (toast, modal, table, filters). Public template (`server/templates/index.html`) with stats display and hybrid search UI showing score explanations.
