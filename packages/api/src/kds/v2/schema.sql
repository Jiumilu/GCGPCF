CREATE TABLE knowledge_objects (
  id TEXT PRIMARY KEY,
  uri TEXT UNIQUE NOT NULL,
  tenant_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  object_type TEXT NOT NULL,
  project_id TEXT,
  supply_chain_node_id TEXT,
  business_system_ref TEXT,
  owner_type TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  visibility TEXT NOT NULL,
  lifecycle TEXT NOT NULL,
  trust_level TEXT NOT NULL,
  rag_admission TEXT NOT NULL,
  confirmation_status TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT,
  content_ref TEXT,
  metadata_json JSONB DEFAULT '{}',
  source_refs_json JSONB DEFAULT '[]',
  evidence_refs_json JSONB DEFAULT '[]',
  lineage_refs_json JSONB DEFAULT '[]',
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  archived_at TIMESTAMP
);

CREATE TABLE knowledge_sources (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  source_kind TEXT NOT NULL,
  trust_level TEXT NOT NULL,
  title TEXT NOT NULL,
  source_uri TEXT,
  external_ref TEXT,
  metadata_json JSONB DEFAULT '{}',
  collected_by TEXT NOT NULL,
  collected_at TIMESTAMP NOT NULL
);

CREATE TABLE knowledge_evidence (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  evidence_kind TEXT NOT NULL,
  title TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  content_hash TEXT,
  controlled_original_ref TEXT,
  summary TEXT,
  metadata_json JSONB DEFAULT '{}',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE object_pool_bindings (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  pool_code TEXT NOT NULL,
  binding_reason TEXT,
  binding_source TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_candidates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  source_object_id TEXT NOT NULL,
  candidate_text TEXT NOT NULL,
  fact_type TEXT NOT NULL,
  pool_refs_json JSONB DEFAULT '[]',
  generated_by TEXT NOT NULL,
  confidence NUMERIC NOT NULL,
  waes_gate_status TEXT NOT NULL,
  target_system TEXT,
  writeback_status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE sop_candidates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  title TEXT NOT NULL,
  sop_type TEXT NOT NULL,
  based_on_object_refs_json JSONB DEFAULT '[]',
  pool_refs_json JSONB DEFAULT '[]',
  generated_by TEXT NOT NULL,
  confirmation_status TEXT NOT NULL,
  waes_gate_status TEXT NOT NULL,
  applicable_scope_json JSONB DEFAULT '[]',
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE writeback_candidates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  target_system TEXT NOT NULL,
  target_entity_type TEXT NOT NULL,
  target_entity_id TEXT,
  proposed_fields_json JSONB DEFAULT '{}',
  based_on_object_refs_json JSONB DEFAULT '[]',
  evidence_refs_json JSONB DEFAULT '[]',
  pool_refs_json JSONB DEFAULT '[]',
  waes_gate_status TEXT NOT NULL,
  writeback_status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE waes_gate_results (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  gate_type TEXT NOT NULL,
  gate_status TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  result_json JSONB DEFAULT '{}',
  required_actions_json JSONB DEFAULT '[]',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE kwe_work_items (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  source_object_id TEXT NOT NULL,
  target_object_id TEXT,
  project_id TEXT,
  supply_chain_node_id TEXT,
  work_type TEXT NOT NULL,
  target_domain TEXT NOT NULL,
  status TEXT NOT NULL,
  priority TEXT NOT NULL,
  assignee_type TEXT,
  assignee_id TEXT,
  required_actions_json JSONB DEFAULT '[]',
  evidence_gap_refs_json JSONB DEFAULT '[]',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE knowledge_events (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_source TEXT NOT NULL,
  payload_json JSONB DEFAULT '{}',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE knowledge_acl (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  principal_type TEXT NOT NULL,
  principal_id TEXT NOT NULL,
  permission TEXT NOT NULL,
  scope_json JSONB DEFAULT '{}',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE knowledge_embeddings (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  embedding_ref TEXT NOT NULL,
  embedding_model TEXT NOT NULL,
  vector_dimension INTEGER NOT NULL,
  rag_admission TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE knowledge_index_jobs (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  job_type TEXT NOT NULL,
  status TEXT NOT NULL,
  result_json JSONB DEFAULT '{}',
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE kds_pools (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  pool_code TEXT NOT NULL,
  pool_name TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE waes_gate_policies (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  policy_code TEXT NOT NULL,
  gate_type TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  policy_json JSONB DEFAULT '{}',
  status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE kwe_workpacks (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  work_item_id TEXT NOT NULL,
  workpack_type TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  evidence_refs_json JSONB DEFAULT '[]',
  required_actions_json JSONB DEFAULT '[]',
  status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gap_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  gap_type TEXT NOT NULL,
  pool_refs_json JSONB DEFAULT '[]',
  discovered_by TEXT NOT NULL,
  priority TEXT NOT NULL,
  bounty_enabled BOOLEAN DEFAULT FALSE,
  bounty_ref TEXT,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE bounty_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  gap_id TEXT NOT NULL,
  bounty_type TEXT NOT NULL,
  reward_json JSONB DEFAULT '{}',
  pool_refs_json JSONB DEFAULT '[]',
  status TEXT NOT NULL,
  settlement_status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE confirmation_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  work_item_id TEXT NOT NULL,
  object_id TEXT NOT NULL,
  confirmation_type TEXT NOT NULL,
  decision TEXT NOT NULL,
  evidence_refs_json JSONB DEFAULT '[]',
  confirmed_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE committee_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  committee_type TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  issue_refs_json JSONB DEFAULT '[]',
  decision_ref TEXT,
  status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE dispute_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  dispute_type TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  party_refs_json JSONB DEFAULT '[]',
  status TEXT NOT NULL,
  committee_ref TEXT,
  decision_ref TEXT,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contribution_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  contributor_type TEXT NOT NULL,
  contributor_id TEXT NOT NULL,
  contribution_type TEXT NOT NULL,
  candidate_score NUMERIC,
  confirmed_score NUMERIC,
  confirmation_status TEXT NOT NULL,
  related_object_refs_json JSONB DEFAULT '[]',
  pool_refs_json JSONB DEFAULT '[]',
  revenue_related BOOLEAN DEFAULT FALSE,
  revenue_ref TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE revenue_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  revenue_type TEXT NOT NULL,
  amount NUMERIC,
  currency TEXT,
  basis TEXT NOT NULL,
  distribution_status TEXT NOT NULL,
  contribution_refs_json JSONB DEFAULT '[]',
  pool_refs_json JSONB DEFAULT '[]',
  evidence_refs_json JSONB DEFAULT '[]',
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quota_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  quota_type TEXT NOT NULL,
  owner_type TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  amount NUMERIC NOT NULL,
  used_amount NUMERIC NOT NULL,
  pool_refs_json JSONB DEFAULT '[]',
  revenue_pool_eligible BOOLEAN DEFAULT FALSE,
  note TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE decision_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  decision_type TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  decision_status TEXT NOT NULL,
  decision_body TEXT NOT NULL,
  committee_ref TEXT,
  evidence_refs_json JSONB DEFAULT '[]',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE loop_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  loop_name TEXT NOT NULL,
  project_id TEXT,
  goal TEXT NOT NULL,
  input_refs_json JSONB DEFAULT '[]',
  new_object_refs_json JSONB DEFAULT '[]',
  new_gap_refs_json JSONB DEFAULT '[]',
  candidate_fact_refs_json JSONB DEFAULT '[]',
  candidate_sop_refs_json JSONB DEFAULT '[]',
  waes_result_refs_json JSONB DEFAULT '[]',
  confirmation_refs_json JSONB DEFAULT '[]',
  committee_refs_json JSONB DEFAULT '[]',
  risk_json JSONB DEFAULT '[]',
  next_actions_json JSONB DEFAULT '[]',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE harness_evidence_records (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  evidence_type TEXT NOT NULL,
  object_refs_json JSONB DEFAULT '[]',
  evidence_uri TEXT NOT NULL,
  content_hash TEXT,
  result_json JSONB DEFAULT '{}',
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE capability_invocations (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  capability_type TEXT NOT NULL,
  capability_name TEXT NOT NULL,
  actor_type TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  input_refs_json JSONB DEFAULT '[]',
  output_refs_json JSONB DEFAULT '[]',
  waes_result_refs_json JSONB DEFAULT '[]',
  no_write BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE agent_used_knowledge (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  invocation_id TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  knowledge_object_id TEXT NOT NULL,
  usage_type TEXT NOT NULL,
  trust_level TEXT NOT NULL,
  rag_admission TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE okf_policy_versions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  policy_code TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  policy_path TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);
