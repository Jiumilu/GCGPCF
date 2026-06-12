# Tasks — KDS v3.1 Production Hardening

## Sprint 1: Security & Permission Hardening

- [x] Create unified config module (server/core/config.py) — single source of truth, no duplicates
- [x] Implement session auth with itsdangerous (server/core/auth.py)
- [x] Implement CSRF token generation and validation
- [x] Implement scoped API keys with SHA-256 hash storage
- [x] Create unified permission context builder (identify_user -> build_permission_context)
- [x] Build 6-step permission decision engine with structured explainability (server/governance/permissions.py)
- [x] Push tenant and sensitivity filters to SQL layer
- [x] Create request context middleware with request_id tracking
- [x] Implement admin login/logout routes with cookie management
- [x] Build API key CRUD routes (generate/revoke/rotate)
- [x] Create permission matrix tests (22 tests)

## Sprint 2: Data Consistency & Audit Hardening

- [x] Create schema_migrations tracking table in migration SQL
- [x] Add standard audit fields (created_at/updated_at/created_by/updated_by/deleted_at/version) to all core tables
- [x] Redesign audit_events table as DB primary with request_id/session_id/ip_hash/ua_hash/route/method/status_code/latency_ms
- [x] Implement DB-primary + JSONL-archive audit write flow
- [x] Add embedding versioning fields (embedding_model/embedding_dimension/chunking_strategy/chunk_hash)
- [x] Create evidence ledger table and service
- [x] Build audit query API with event_type/tenant/actor/request_id/q filtering
- [x] Create audit tests (6 tests)

## Sprint 3: Search Quality & DQ Governance Upgrade

- [x] Build 7-dimension DQ scoring engine (server/governance/dq.py)
- [x] Implement per-dimension scoring with issues list
- [x] Implement DQ grade computation (A/B/C/D/F)
- [x] Build repair task SLA tracking (owner/reviewer/due_at/sla_level)
- [x] Implement hybrid search with score explanation (keyword_score/semantic_score/authority_boost/dq_penalty)
- [x] Define Golden Query Set for regression testing
- [x] Build content masking by sensitivity level
- [x] Create DQ analysis and distribution API
- [x] Build repair task lifecycle API
- [x] Create DQ tests (16 tests)

## Sprint 4: Agent Safety & Release Gates

- [x] Build 6-state agent task machine (server/agent/agent_tasks.py)
- [x] Implement 4-layer patch review (isolation -> allowlist -> static scan -> human review)
- [x] Define file type and path risk mapping
- [x] Implement static risk scan (SQL, shell, import, permission patterns)
- [x] Require rollback plan for medium+ risk patches
- [x] Build conflict detection (file/api/behavior/evidence/policy)
- [x] Create agent workspace isolation
- [x] Build agent task lifecycle API
- [x] Build patch review API
- [x] Write agent contract (agent/agent-contract.md)
- [x] Create agent safety tests (20 tests)
- [x] Implement release report generation

## Sprint 5: Operations & Platform Enhancement

- [x] Build /api/metrics endpoint with DB pool/queue metrics
- [x] Build readiness probe with ok/degraded/down states
- [x] Build SSH tunnel monitor script with auto-reconnect
- [x] Build backup script with retention policy (7 daily + 4 weekly + 6 monthly)
- [x] Build restore check script
- [x] Create project registry with policy templates
- [x] Define connector contract (BaseConnector, MarkdownConnector, GitConnector)
- [x] Build batch operations API (archive/authority/deprecate/repair)
- [x] Build notifications service
- [x] Build DQ trends and stale content detection
- [x] Generate DQ reports (JSON + CSV)

## Frontend

- [x] Create public search template with stats and score display
- [x] Build modular admin shell (index.html + app.js + app.css)
- [x] Build dashboard module (Risk/Work/Health overview)
- [x] Build DQ module (distribution, analysis, repair tasks)
- [x] Build permissions module (tenant list, role management, permission tester)
- [x] Build audit module (event log with filtering)
- [x] Build agent module (task list, patch review, safety checker)
- [x] Build operations module (low DQ, stale content, batch actions, reports)
- [x] Build platform module (projects, connectors)
- [x] Build reusable components (toast, modal, table, filters)

## Documentation & Delivery

- [x] Write SECURITY.md
- [x] Write API_REFERENCE.md with full endpoint catalog
- [x] Create full schema migration (migrations/001_v3.1_schema.sql)
- [x] Write OpenSpec proposal, design, and specs
- [x] Create pyproject.toml and requirements.txt

## Testing

- [x] test_permissions.py — 22 tests (full 6-step matrix)
- [x] test_dq.py — 16 tests (7-dimension scoring)
- [x] test_agent.py — 20 tests (safety review + state machine)
- [x] test_search.py — 16 tests (filters, masking, golden queries)
- [x] test_audit.py — 6 tests (event types, query)
- [x] test_api.py — 22 tests (response format, auth, config, scopes)
