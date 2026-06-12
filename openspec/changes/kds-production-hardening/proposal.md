## Why

KDS v3.0 is a feature-complete knowledge governance platform prototype (12 routes, 20 services, 56 APIs, 42 tests), but lacks production-grade hardening in security, data consistency, audit reliability, agent safety, and operational recoverability. Without these, the platform cannot safely serve multiple tenants, cannot pass a security audit, and cannot be delivered as a commercial product. v3.1 closes the gap from "capability prototype" to "production-hardened platform."

## What Changes

### Security Hardening (P0)
- Session-based auth with CSRF protection replacing BasicAuth
- Unified permission middleware across ALL APIs (frontend + admin)
- API Key scoping (search/read/admin/export/agent) with hash storage, expiry, and rate limiting
- Permission decision explainability (reason, matched_rule, tenant, role, sensitivity per decision)

### Data Consistency (P0)
- audit_events DB table as primary fact source, JSONL as append-only archive
- schema_migrations tracking table with up/down/checksum/applied_at
- Embedding version management (model, dimension, chunking_strategy, chunk_hash)
- Standard audit fields on all core tables

### Search & DQ Governance (P1)
- 7-dimension DQ scoring (authority, freshness, completeness, metadata, link_health, duplication, security)
- Golden Query Set for search quality regression testing
- Search score explanation with per-component breakdown
- Repair task SLA tracking (owner, reviewer, due_at, sla_level)
- Permission filter pushed to SQL query layer (not post-retrieval in-memory)

### Agent Safety (P0)
- 4-layer defense: workspace isolation -> patch allowlist -> static risk scan -> human review
- 6-state agent task machine with mandatory rollback plans
- **BREAKING**: Agent can no longer modify auth.py, db.py, migrations, or deploy scripts

### Operations & Platform (P1/P2)
- /api/metrics endpoint, tunnel monitor with auto-reconnect
- Backup retention policy (7 daily + 4 weekly + 6 monthly + restore drills)
- Connector contract, project policy templates, modularized admin frontend

## Capabilities

### New Capabilities
- `session-auth`: Session + CSRF authentication replacing BasicAuth for admin
- `api-key-scopes`: Scoped API keys with hash storage, expiry, rate limiting
- `unified-permission-middleware`: Permission middleware applied to all API routes
- `permission-explainability`: Structured permission decision output
- `audit-db-primary`: Database as primary audit fact source
- `schema-migrations`: Migration state tracking table
- `embedding-versioning`: Embedding model/dimension/chunk_hash version management
- `dq-seven-dim`: 7-dimension DQ scoring with grade and breakdown
- `golden-query-set`: Search quality regression test dataset
- `search-score-explanation`: Per-component search score breakdown
- `repair-task-sla`: SLAs, owners, and reviewers for repair tasks
- `agent-safety-matrix`: 4-layer agent defense with file-type/path/risk allowlist
- `agent-six-state`: 6-state agent task state machine with mandatory rollback plans
- `release-gate`: Automated release reports
- `api-metrics`: Operational metrics endpoint
- `tunnel-monitor`: SSH tunnel health monitoring and auto-reconnect
- `connector-contract`: Data source connector interface contract
- `admin-frontend-modules`: Modularized admin panel with role-based navigation

### Modified Capabilities
None — v3.0 has no existing OpenSpec specs; all capabilities are net-new.

## Impact

- **Code**: 30+ server modules across 6 layers, 10 route files, modular admin frontend (11 JS/CSS/HTML files)
- **API**: All endpoints now under unified permission middleware; new /api/v1/admin/* routes; new /api/metrics
- **Database**: schema_migrations table, new columns on existing tables, audit_events structure changes
- **Dependencies**: python-jose, passlib, itsdangerous for session/CSRF
- **Deployment**: New launchd config for tunnel monitor, updated backup scripts
- **Tests**: From 42 to 102+ tests across permission matrix, search quality, agent safety, E2E coverage
