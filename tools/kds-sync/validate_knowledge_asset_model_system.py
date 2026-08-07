#!/usr/bin/env python3
"""Validate the GlobalCloud knowledge asset model contract and handoff boundary."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "okf/knowledge-asset-contract-manifest.yaml"
MODEL_DOC = ROOT / "03-data-ai-knowledge/GlobalCloud知识资产模型体系综合方案.md"
KNOWLEDGE_README = ROOT / "03-data-ai-knowledge/README.md"
DOCUMENT_REGISTER = ROOT / "09-status/globalcloud-document-control-register.md"
MASTER_PLAN = ROOT / "01-architecture/GlobalCloud 项目群总体方案.md"
IMPLEMENTATION_PLAN = ROOT / "GlobalCloud 项目群实施方案.md"
FEATURE = ROOT / "features/active/F-013-knowledge-asset-model-system/feature.yaml"
KDS_HANDOFF = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/kds-p1-handoff.md"
DOCUMENT_CONTROL = ROOT / "tools/kds-sync/document_control.py"

EXPECTED_ARTIFACT_ROLES = {
    "model_plan",
    "schema",
    "vocabulary",
    "canonical_example",
    "approved_copy_example",
    "example",
    "validator",
}
EXPECTED_DEPENDENCY_ROLES = {"knowledge_object", "domain_policy"}
EXPECTED_ACCESS_SPACES = {"private", "personal", "family", "team", "partner", "public", "ops"}
EXPECTED_KNOWLEDGE_DOMAINS = {"private", "workspace", "project", "org", "supply_chain", "public", "governance"}
EXPECTED_SPACE_DOMAIN_MAPPINGS = {
    "private": {"private"},
    "personal": {"workspace"},
    "family": {"collection_only"},
    "team": {"project", "org"},
    "partner": {"supply_chain"},
    "public": {"public"},
    "ops": {"content_domain_plus_ops_tag"},
}
EXPECTED_LEGACY_SPACE_MAPPINGS = {
    "private": "private",
    "personal": "workspace",
    "family": "collection_only",
    "team": "project_or_org",
    "partner": "supply_chain_with_external_account_acl",
    "public": "public",
    "ops": "domain_tag_ops",
}
SPACE_DOMAIN_MARKERS = {"collection_only", "content_domain_plus_ops_tag"}
EXPECTED_GOVERNANCE_RULES = {f"KAM-{index:03d}" for index in range(1, 8)}
EXPECTED_CONTEXT_REF_PREFIXES = {
    "platformGroupRefs": "platform-group://",
    "systemRefs": "system://",
    "engineeringProjectRefs": "engineering-project://",
    "businessPortfolioRefs": "business-portfolio://",
    "businessProjectRefs": "business-project://",
    "organizationRefs": "organization://",
    "workstreamRefs": "workstream://",
    "domainRefs": "domain://",
    "geographyRefs": "geography://",
    "productRefs": "product://",
    "processRefs": "process://",
}
EXPECTED_CONSUMERS = {
    "kds": "versioned_mirror_and_canonical_metadata_owner",
    "brain": "authorized_read_model_consumer",
    "mmc": "authorized_model_invocation_only",
    "waes": "authorization_and_status_gate",
    "gpcf": "contract_and_compatibility_owner",
}
EXPECTED_MODEL_DOCUMENT_CONTROL = {
    "project": "GPCF",
    "related_projects": [
        "WAS",
        "XWAIL",
        "AAAS",
        "WAES",
        "GFIS",
        "GPC",
        "PVAOS",
        "KDS",
        "Brain",
        "Studio",
        "MMC",
        "PKC",
        "XGD",
        "XiaoC",
        "XiaoG",
        "SOP",
        "GPCF",
        "ICP",
    ],
    "status": "draft",
    "version": "v0.1",
    "owner": "GPCF",
    "kds_path": "开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud知识资产模型体系综合方案.md",
}


def fail(reason: str) -> None:
    raise SystemExit(f"knowledge_asset_model_gate=fail reason={reason}")


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_yaml(path: Path) -> dict:
    require(path.is_file(), f"missing_yaml:{rel(path)}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"invalid_yaml:{rel(path)}:{exc}")
    require(isinstance(payload, dict), f"yaml_root_not_mapping:{rel(path)}")
    return payload


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing_json:{rel(path)}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid_json:{rel(path)}:{exc}")
    require(isinstance(payload, dict), f"json_root_not_object:{rel(path)}")
    return payload


def sha256_file(path: Path) -> str:
    require(path.is_file(), f"missing_hashed_file:{rel(path)}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def keyed_entries(payload: object, label: str) -> dict[str, dict]:
    require(isinstance(payload, list), f"{label}_not_list")
    result: dict[str, dict] = {}
    for item in payload:
        require(isinstance(item, dict), f"{label}_entry_not_mapping")
        role = str(item.get("role") or "")
        require(role, f"{label}_missing_role")
        require(role not in result, f"{label}_duplicate_role:{role}")
        result[role] = item
    return result


def validate_hash_entries(entries: dict[str, dict], expected_roles: set[str], label: str) -> None:
    require(set(entries) == expected_roles, f"{label}_roles_mismatch")
    for role, entry in entries.items():
        source_path = str(entry.get("path") or "")
        expected_hash = str(entry.get("sha256") or "")
        require(source_path and expected_hash, f"{label}_entry_incomplete:{role}")
        path = ROOT / source_path
        require(sha256_file(path) == expected_hash, f"{label}_hash_mismatch:{role}:{source_path}")


def require_text(path: Path, tokens: list[str]) -> str:
    require(path.is_file(), f"missing_text:{rel(path)}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"missing_token:{rel(path)}:{token}")
    return text


def validate_document_control_metadata() -> None:
    namespace = runpy.run_path(str(DOCUMENT_CONTROL))
    build_records = namespace.get("build_records")
    require(callable(build_records), "document_control_build_records_missing")
    records = build_records([MODEL_DOC])
    require(len(records) == 1, "document_control_model_record_count_mismatch")
    record = records[0]
    for key, expected in EXPECTED_MODEL_DOCUMENT_CONTROL.items():
        require(record.get(key) == expected, f"document_control_model_metadata_mismatch:{key}")


def validate_negative_examples(validator: Draft202012Validator, example: dict) -> int:
    cases: list[tuple[str, dict]] = []

    second_master = deepcopy(example)
    second_master["canonicalBody"] = {"text": "must stay in the canonical KnowledgeObject"}
    cases.append(("second_knowledge_master_field", second_master))

    collapsed_project = deepcopy(example)
    collapsed_project["contexts"]["projectRefs"] = ["project://ambiguous"]
    cases.append(("collapsed_project_dimension", collapsed_project))

    unknown_asset_type = deepcopy(example)
    unknown_asset_type["classification"]["assetType"] = "uncontrolled_type"
    cases.append(("uncontrolled_asset_type", unknown_asset_type))

    missing_evidence = deepcopy(example)
    missing_evidence["provenance"]["evidenceRefs"] = []
    cases.append(("missing_evidence", missing_evidence))

    missing_lineage = deepcopy(example)
    missing_lineage["provenance"]["lineageRefs"] = []
    cases.append(("missing_lineage", missing_lineage))

    partner_without_acl = deepcopy(example)
    partner_without_acl["accessScope"]["projections"][0]["target"].pop("aclPolicyRef")
    cases.append(("partner_without_acl_policy", partner_without_acl))

    partner_without_approval = deepcopy(example)
    partner_without_approval["accessScope"]["projections"][0]["target"].pop("approvalEvidenceRefs")
    cases.append(("partner_without_approval_evidence", partner_without_approval))

    public_without_policy = deepcopy(example)
    public_target = public_without_policy["accessScope"]["projections"][0]["target"]
    public_target["spaceType"] = "public"
    public_target.pop("publicationPolicyRef", None)
    cases.append(("public_without_publication_policy", public_without_policy))

    write_without_authorization = deepcopy(example)
    write_governance = write_without_authorization["governance"]
    write_governance["metadataStatus"] = "human_confirmed"
    write_governance["authorizationBoundary"] = "authorized"
    write_governance["writeMode"] = "authorized_write"
    cases.append(("authorized_write_without_evidence", write_without_authorization))

    excessive_free_tags = deepcopy(example)
    excessive_free_tags["tags"]["free"] = [f"tag-{index}" for index in range(21)]
    cases.append(("free_tag_limit", excessive_free_tags))

    unknown_relation = deepcopy(example)
    unknown_relation["relations"][0]["relationType"] = "uncontrolled_relation"
    cases.append(("uncontrolled_relation_type", unknown_relation))

    business_ref_in_engineering_dimension = deepcopy(example)
    business_ref_in_engineering_dimension["contexts"]["engineeringProjectRefs"] = [
        "business-project://example/wrong-dimension"
    ]
    cases.append(("business_ref_in_engineering_dimension", business_ref_in_engineering_dimension))

    engineering_ref_in_business_dimension = deepcopy(example)
    engineering_ref_in_business_dimension["contexts"]["businessProjectRefs"] = [
        "engineering-project://globalcloud/wrong-dimension"
    ]
    cases.append(("engineering_ref_in_business_dimension", engineering_ref_in_business_dimension))

    business_ref_in_system_dimension = deepcopy(example)
    business_ref_in_system_dimension["contexts"]["systemRefs"] = [
        "business-project://example/wrong-dimension"
    ]
    cases.append(("business_ref_in_system_dimension", business_ref_in_system_dimension))

    redacted_without_lineage = deepcopy(example)
    redacted_without_lineage["accessScope"]["projections"][0].pop("projectionLineageRefs")
    cases.append(("redacted_projection_without_lineage", redacted_without_lineage))

    approved_copy = deepcopy(example)
    approved_projection = approved_copy["accessScope"]["projections"][0]
    approved_projection["mode"] = "approved_copy"
    approved_projection["approvalEvidenceRefs"] = ["approval://example/approved-copy-001"]
    approved_projection["derivedKnowledgeObjectRef"] = "ko://example/derived-copy-001"

    approved_without_lineage = deepcopy(approved_copy)
    approved_without_lineage["accessScope"]["projections"][0].pop("projectionLineageRefs")
    cases.append(("approved_copy_without_lineage", approved_without_lineage))

    approved_without_approval = deepcopy(approved_copy)
    approved_without_approval["accessScope"]["projections"][0].pop("approvalEvidenceRefs")
    cases.append(("approved_copy_without_approval", approved_without_approval))

    approved_without_derived_object = deepcopy(approved_copy)
    approved_without_derived_object["accessScope"]["projections"][0].pop("derivedKnowledgeObjectRef")
    cases.append(("approved_copy_without_derived_object", approved_without_derived_object))

    reference_with_derived_object = deepcopy(example)
    reference_projection = reference_with_derived_object["accessScope"]["projections"][0]
    reference_projection["mode"] = "reference_only"
    reference_projection["derivedKnowledgeObjectRef"] = "ko://example/forbidden-derived-object"
    cases.append(("reference_only_with_derived_object", reference_with_derived_object))

    for name, payload in cases:
        require(not validator.is_valid(payload), f"negative_case_unexpectedly_valid:{name}")
    return len(cases)


def projection_semantic_violations(envelope: dict) -> list[str]:
    violations: list[str] = []
    canonical_ref = envelope.get("knowledgeObjectRef")
    projections = envelope.get("accessScope", {}).get("projections", [])
    for index, projection in enumerate(projections):
        if projection.get("mode") != "approved_copy":
            continue
        if projection.get("derivedKnowledgeObjectRef") == canonical_ref:
            violations.append(f"approved_copy_reuses_canonical_ref:{index}")
    return violations


def validate_projection_positive_examples(validator: Draft202012Validator, example: dict) -> int:
    cases: list[tuple[str, dict]] = [("redacted_projection", deepcopy(example))]

    reference_only = deepcopy(example)
    reference_projection = reference_only["accessScope"]["projections"][0]
    reference_projection["mode"] = "reference_only"
    reference_projection.pop("projectionLineageRefs", None)
    cases.append(("reference_only", reference_only))

    approved_copy = deepcopy(example)
    approved_projection = approved_copy["accessScope"]["projections"][0]
    approved_projection["mode"] = "approved_copy"
    approved_projection["approvalEvidenceRefs"] = ["approval://example/approved-copy-001"]
    approved_projection["derivedKnowledgeObjectRef"] = "ko://example/derived-copy-001"
    cases.append(("approved_copy", approved_copy))

    for name, payload in cases:
        try:
            validator.validate(payload)
        except Exception as exc:
            fail(f"projection_positive_case_failed:{name}:{type(exc).__name__}:{exc}")
        require(not projection_semantic_violations(payload), f"projection_positive_semantics_failed:{name}")
    return len(cases)


def validate_projection_semantic_negative_examples(example: dict) -> int:
    approved_copy_reusing_canonical = deepcopy(example)
    projection = approved_copy_reusing_canonical["accessScope"]["projections"][0]
    projection["mode"] = "approved_copy"
    projection["approvalEvidenceRefs"] = ["approval://example/approved-copy-001"]
    projection["derivedKnowledgeObjectRef"] = approved_copy_reusing_canonical["knowledgeObjectRef"]
    require(
        bool(projection_semantic_violations(approved_copy_reusing_canonical)),
        "projection_semantic_negative_case_unexpectedly_valid:approved_copy_reuses_canonical_ref",
    )
    return 1


def approved_copy_linkage_violations(envelope: dict, canonical_object: dict, derived_object: dict) -> list[str]:
    violations: list[str] = []
    projections = envelope.get("accessScope", {}).get("projections", [])
    approved_projection = next((item for item in projections if item.get("mode") == "approved_copy"), None)
    if approved_projection is None:
        return ["approved_copy_projection_missing"]
    if approved_projection.get("derivedKnowledgeObjectRef") not in {
        derived_object.get("id"),
        derived_object.get("uri"),
    }:
        violations.append("derived_object_ref_mismatch")
    if {derived_object.get("id"), derived_object.get("uri")} & {
        canonical_object.get("id"),
        canonical_object.get("uri"),
    }:
        violations.append("derived_object_reuses_canonical_identity")
    if derived_object.get("tenantId") != canonical_object.get("tenantId"):
        violations.append("derived_object_tenant_mismatch")
    if derived_object.get("sourceRefs") != canonical_object.get("sourceRefs"):
        violations.append("derived_object_source_mismatch")
    projection_lineage = set(approved_projection.get("projectionLineageRefs") or [])
    if not projection_lineage <= set(derived_object.get("lineageRefs") or []):
        violations.append("derived_object_missing_projection_lineage")
    if derived_object.get("confirmationStatus") != "human_confirmed":
        violations.append("derived_object_not_human_confirmed")
    return violations


def validate_approved_copy_linkage(
    validator: Draft202012Validator,
    knowledge_object_validator: Draft202012Validator,
    example: dict,
    canonical_object: dict,
    derived_object: dict,
) -> int:
    approved_copy = deepcopy(example)
    projection = approved_copy["accessScope"]["projections"][0]
    projection["mode"] = "approved_copy"
    projection["approvalEvidenceRefs"] = ["approval://example/approved-copy-001"]
    projection["projectionLineageRefs"] = ["lineage://example/approved-copy-001"]
    projection["derivedKnowledgeObjectRef"] = derived_object["uri"]
    try:
        validator.validate(approved_copy)
        knowledge_object_validator.validate(derived_object)
    except Exception as exc:
        fail(f"approved_copy_linkage_positive_case_failed:{type(exc).__name__}:{exc}")
    require(
        not approved_copy_linkage_violations(approved_copy, canonical_object, derived_object),
        "approved_copy_linkage_positive_case_invalid",
    )

    cases: list[tuple[str, dict, dict]] = []
    wrong_ref = deepcopy(approved_copy)
    wrong_ref["accessScope"]["projections"][0]["derivedKnowledgeObjectRef"] = "ko://example/unresolved-copy"
    cases.append(("derived_object_ref_mismatch", wrong_ref, derived_object))

    wrong_tenant = deepcopy(derived_object)
    wrong_tenant["tenantId"] = "tenant://other"
    cases.append(("derived_object_tenant_mismatch", approved_copy, wrong_tenant))

    missing_lineage = deepcopy(derived_object)
    missing_lineage["lineageRefs"] = ["lineage://example/import-001"]
    cases.append(("derived_object_missing_projection_lineage", approved_copy, missing_lineage))

    unconfirmed = deepcopy(derived_object)
    unconfirmed["confirmationStatus"] = "human_required"
    cases.append(("derived_object_not_human_confirmed", approved_copy, unconfirmed))

    for name, candidate_envelope, candidate_derived_object in cases:
        require(
            bool(approved_copy_linkage_violations(candidate_envelope, canonical_object, candidate_derived_object)),
            f"approved_copy_linkage_negative_case_unexpectedly_valid:{name}",
        )
    return len(cases)


def canonical_link_violations(
    envelope: dict,
    canonical_object: dict,
    asset_type_compatibility: dict[str, dict],
    space_domain_mappings: dict[str, set[str]],
    knowledge_domains: set[str],
) -> list[str]:
    violations: list[str] = []
    if envelope.get("knowledgeObjectRef") not in {canonical_object.get("id"), canonical_object.get("uri")}:
        violations.append("knowledge_object_ref_mismatch")
    if envelope.get("tenantId") != canonical_object.get("tenantId"):
        violations.append("tenant_mismatch")

    asset_type = envelope.get("classification", {}).get("assetType")
    expected_object_type = (asset_type_compatibility.get(str(asset_type)) or {}).get("default_okf_object_type")
    if canonical_object.get("objectType") != expected_object_type:
        violations.append("default_object_type_mismatch")

    primary_space_type = envelope.get("accessScope", {}).get("primarySpace", {}).get("spaceType")
    directly_mapped_domains = space_domain_mappings.get(str(primary_space_type), set()) & knowledge_domains
    if directly_mapped_domains and canonical_object.get("domain") not in directly_mapped_domains:
        violations.append("primary_space_domain_mismatch")

    envelope_provenance = envelope.get("provenance", {})
    for field in ("sourceRefs", "evidenceRefs", "lineageRefs"):
        if envelope_provenance.get(field) != canonical_object.get(field):
            violations.append(f"provenance_mismatch:{field}")
    return violations


def validate_canonical_link_negative_examples(
    envelope: dict,
    canonical_object: dict,
    asset_type_compatibility: dict[str, dict],
    space_domain_mappings: dict[str, set[str]],
    knowledge_domains: set[str],
) -> int:
    cases: list[tuple[str, dict, dict]] = []

    wrong_reference = deepcopy(envelope)
    wrong_reference["knowledgeObjectRef"] = "ko://example/unrelated-object"
    cases.append(("canonical_reference_mismatch", wrong_reference, canonical_object))

    wrong_tenant = deepcopy(envelope)
    wrong_tenant["tenantId"] = "tenant://other"
    cases.append(("canonical_tenant_mismatch", wrong_tenant, canonical_object))

    wrong_object_type = deepcopy(canonical_object)
    wrong_object_type["objectType"] = "evidence"
    cases.append(("canonical_object_type_mismatch", envelope, wrong_object_type))

    wrong_provenance = deepcopy(canonical_object)
    wrong_provenance["evidenceRefs"] = ["evidence://example/unrelated-evidence"]
    cases.append(("canonical_provenance_mismatch", envelope, wrong_provenance))

    wrong_domain = deepcopy(canonical_object)
    wrong_domain["domain"] = "public"
    cases.append(("primary_space_domain_mismatch", envelope, wrong_domain))

    for name, candidate_envelope, candidate_object in cases:
        require(
            bool(
                canonical_link_violations(
                    candidate_envelope,
                    candidate_object,
                    asset_type_compatibility,
                    space_domain_mappings,
                    knowledge_domains,
                )
            ),
            f"canonical_link_negative_case_unexpectedly_valid:{name}",
        )
    return len(cases)


def main() -> int:
    manifest = load_yaml(MANIFEST_PATH)
    require(manifest.get("contract_id") == "globalcloud.knowledge_asset", "invalid_contract_id")
    require(manifest.get("contract_version") == "v0.1", "invalid_contract_version")
    require(manifest.get("status") == "draft", "contract_status_must_be_draft")
    require(manifest.get("owner") == "GPCF", "invalid_contract_owner")
    require(manifest.get("source_of_truth") == "GPCF", "invalid_source_of_truth")

    compatibility = manifest.get("compatibility") or {}
    require(compatibility.get("mode") == "additive_envelope", "invalid_compatibility_mode")
    require(compatibility.get("extends_contract") == "okf/knowledge-object.schema.json", "invalid_extends_contract")
    require(compatibility.get("domain_policy") == "okf/domain-policy.yaml", "invalid_domain_policy_ref")
    require(
        compatibility.get("canonical_linkage")
        == {
            "reference_match": "id_or_uri",
            "invariant_fields": ["tenantId", "sourceRefs", "evidenceRefs", "lineageRefs"],
            "object_type_mapping": "okf/knowledge-asset-vocabulary.yaml#asset_type_compatibility",
            "space_domain_mapping": "okf/knowledge-asset-vocabulary.yaml#dimensions.access_space",
        },
        "invalid_canonical_linkage_contract",
    )
    require(
        compatibility.get("projection_contract")
        == {
            "modes": ["reference_only", "redacted_projection", "approved_copy"],
            "redacted_requires": ["projectionLineageRefs"],
            "approved_copy_requires": [
                "projectionLineageRefs",
                "approvalEvidenceRefs",
                "derivedKnowledgeObjectRef",
            ],
            "derived_ref_must_differ_from_canonical": True,
            "derived_object_must_resolve_to": "id_or_uri",
            "derived_invariants": ["tenantId", "sourceRefs", "projectionLineageRefs", "confirmationStatus=human_confirmed"],
        },
        "invalid_projection_contract",
    )

    artifacts = keyed_entries(manifest.get("artifacts"), "artifacts")
    dependencies = keyed_entries(manifest.get("dependencies"), "dependencies")
    validate_hash_entries(artifacts, EXPECTED_ARTIFACT_ROLES, "artifacts")
    validate_hash_entries(dependencies, EXPECTED_DEPENDENCY_ROLES, "dependencies")

    schema = load_json(ROOT / artifacts["schema"]["path"])
    example = load_json(ROOT / artifacts["example"]["path"])
    canonical_example = load_json(ROOT / artifacts["canonical_example"]["path"])
    approved_copy_example = load_json(ROOT / artifacts["approved_copy_example"]["path"])
    vocabulary = load_yaml(ROOT / artifacts["vocabulary"]["path"])
    knowledge_object = load_json(ROOT / dependencies["knowledge_object"]["path"])
    domain_policy = load_yaml(ROOT / dependencies["domain_policy"]["path"])

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        validator.validate(example)
        Draft202012Validator.check_schema(knowledge_object)
        knowledge_object_validator = Draft202012Validator(knowledge_object, format_checker=FormatChecker())
        knowledge_object_validator.validate(canonical_example)
        knowledge_object_validator.validate(approved_copy_example)
    except Exception as exc:
        fail(f"schema_validation_failed:{type(exc).__name__}:{exc}")

    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "invalid_schema_draft")
    require(schema.get("properties", {}).get("schemaVersion", {}).get("const") == "v0.1", "schema_version_mismatch")
    schema_spaces = set(
        schema.get("$defs", {}).get("spaceBinding", {}).get("properties", {}).get("spaceType", {}).get("enum", [])
    )
    require(schema_spaces == EXPECTED_ACCESS_SPACES, "schema_access_spaces_mismatch")

    context_schema = schema.get("properties", {}).get("contexts", {})
    context_properties = context_schema.get("properties", {})
    require(set(context_properties) == set(EXPECTED_CONTEXT_REF_PREFIXES), "context_dimensions_mismatch")
    required_contexts = set(context_schema.get("required", []))
    require(required_contexts == {"platformGroupRefs", "systemRefs"}, "required_context_dimensions_mismatch")
    for field, prefix in EXPECTED_CONTEXT_REF_PREFIXES.items():
        field_schema = context_properties.get(field, {})
        require(field_schema.get("type") == "array", f"context_dimension_not_array:{field}")
        require(field_schema.get("uniqueItems") is True, f"context_dimension_not_unique:{field}")
        expected_min_items = 1 if field in required_contexts else 0
        require(field_schema.get("minItems", 0) == expected_min_items, f"context_dimension_min_items_mismatch:{field}")
        require(
            field_schema.get("items", {}).get("pattern") == f"^{prefix}[^\\s]+$",
            f"context_dimension_namespace_mismatch:{field}",
        )

    knowledge_domains = set(knowledge_object.get("properties", {}).get("domain", {}).get("enum", []))
    require(knowledge_domains == EXPECTED_KNOWLEDGE_DOMAINS, "knowledge_domains_mismatch")

    dimensions = vocabulary.get("dimensions") or {}
    access_values = dimensions.get("access_space", {}).get("values", [])
    require(isinstance(access_values, list), "vocabulary_access_values_not_list")
    access_entries = {
        str(item.get("code")): item
        for item in access_values
        if isinstance(item, dict) and item.get("code")
    }
    vocabulary_spaces = set(access_entries)
    require(vocabulary_spaces == EXPECTED_ACCESS_SPACES, "vocabulary_access_spaces_mismatch")
    space_domain_mappings: dict[str, set[str]] = {}
    for space, expected_mapping in EXPECTED_SPACE_DOMAIN_MAPPINGS.items():
        raw_mapping = access_entries.get(space, {}).get("okf_domain_mapping")
        require(isinstance(raw_mapping, list) and raw_mapping, f"space_domain_mapping_missing:{space}")
        mapping = {str(value) for value in raw_mapping}
        require(mapping == expected_mapping, f"space_domain_mapping_mismatch:{space}")
        require(
            mapping <= EXPECTED_KNOWLEDGE_DOMAINS | SPACE_DOMAIN_MARKERS,
            f"space_domain_mapping_unknown_value:{space}",
        )
        space_domain_mappings[space] = mapping
    require(
        domain_policy.get("legacy_space_mapping") == EXPECTED_LEGACY_SPACE_MAPPINGS,
        "domain_policy_space_mapping_mismatch",
    )
    require(
        set(dimensions.get("knowledge_domain", {}).get("values", [])) == EXPECTED_KNOWLEDGE_DOMAINS,
        "vocabulary_knowledge_domains_mismatch",
    )
    schema_asset_types = set(schema.get("properties", {}).get("classification", {}).get("properties", {}).get("assetType", {}).get("enum", []))
    vocabulary_asset_types = set(dimensions.get("asset_type", {}).get("values", []))
    require(schema_asset_types == vocabulary_asset_types, "asset_type_vocabulary_mismatch")

    asset_type_compatibility = vocabulary.get("asset_type_compatibility") or {}
    require(isinstance(asset_type_compatibility, dict), "asset_type_compatibility_not_mapping")
    require(set(asset_type_compatibility) == schema_asset_types, "asset_type_compatibility_keys_mismatch")
    okf_object_types = set(knowledge_object.get("properties", {}).get("objectType", {}).get("enum", []))
    for asset_type, mapping in asset_type_compatibility.items():
        require(isinstance(mapping, dict), f"asset_type_compatibility_entry_not_mapping:{asset_type}")
        default_object_type = mapping.get("default_okf_object_type")
        compatible_object_types = mapping.get("compatible_okf_object_types")
        require(isinstance(compatible_object_types, list) and compatible_object_types, f"empty_compatible_object_types:{asset_type}")
        require(len(compatible_object_types) == len(set(compatible_object_types)), f"duplicate_compatible_object_types:{asset_type}")
        require(default_object_type in compatible_object_types, f"default_object_type_not_compatible:{asset_type}")
        require(set(compatible_object_types) <= okf_object_types, f"unknown_okf_object_type_mapping:{asset_type}")

    schema_governance = schema.get("properties", {}).get("governance", {}).get("properties", {})
    controlled_enum_pairs = {
        "confidentiality": (
            schema.get("properties", {}).get("classification", {}).get("properties", {}).get("confidentiality", {}).get("enum", []),
            dimensions.get("confidentiality", {}).get("values", []),
        ),
        "lifecycle_stage": (
            schema.get("properties", {}).get("classification", {}).get("properties", {}).get("lifecycleStage", {}).get("enum", []),
            dimensions.get("lifecycle_stage", {}).get("values", []),
        ),
        "metadata_status": (
            schema_governance.get("metadataStatus", {}).get("enum", []),
            dimensions.get("metadata_status", {}).get("values", []),
        ),
        "authorization_boundary": (
            schema_governance.get("authorizationBoundary", {}).get("enum", []),
            dimensions.get("authorization_boundary", {}).get("values", []),
        ),
        "write_mode": (
            schema_governance.get("writeMode", {}).get("enum", []),
            dimensions.get("write_mode", {}).get("values", []),
        ),
    }
    for label, (schema_values, vocabulary_values) in controlled_enum_pairs.items():
        require(set(schema_values) == set(vocabulary_values), f"{label}_vocabulary_mismatch")

    schema_relation_types = set(
        schema.get("$defs", {}).get("relation", {}).get("properties", {}).get("relationType", {}).get("enum", [])
    )
    vocabulary_relation_types = set(vocabulary.get("relation_types") or [])
    require(schema_relation_types == vocabulary_relation_types, "relation_type_vocabulary_mismatch")
    require(
        example.get("governance", {}).get("vocabularyVersion")
        == f"{vocabulary.get('vocabulary_id')}@{vocabulary.get('version')}",
        "example_vocabulary_version_mismatch",
    )
    system_values = set(dimensions.get("system", {}).get("values", []))
    for system_ref in example.get("contexts", {}).get("systemRefs", []):
        require(str(system_ref).startswith("system://"), f"example_invalid_system_ref:{system_ref}")
        require(str(system_ref).rsplit("/", 1)[-1] in system_values, f"example_unknown_system_ref:{system_ref}")

    authorized_example = deepcopy(example)
    authorized_governance = authorized_example["governance"]
    authorized_governance["metadataStatus"] = "human_confirmed"
    authorized_governance["authorizationBoundary"] = "authorized"
    authorized_governance["writeMode"] = "authorized_write"
    authorized_governance["authorizationEvidenceRefs"] = ["authorization://example/write-approval-001"]
    try:
        validator.validate(authorized_example)
    except Exception as exc:
        fail(f"authorized_write_positive_case_failed:{type(exc).__name__}:{exc}")

    negative_case_count = validate_negative_examples(validator, example)
    projection_positive_case_count = validate_projection_positive_examples(validator, example)
    projection_semantic_negative_case_count = validate_projection_semantic_negative_examples(example)
    approved_copy_linkage_negative_case_count = validate_approved_copy_linkage(
        validator,
        knowledge_object_validator,
        example,
        canonical_example,
        approved_copy_example,
    )
    canonical_link_errors = canonical_link_violations(
        example,
        canonical_example,
        asset_type_compatibility,
        space_domain_mappings,
        knowledge_domains,
    )
    require(not canonical_link_errors, f"canonical_link_invalid:{','.join(canonical_link_errors)}")
    canonical_link_negative_case_count = validate_canonical_link_negative_examples(
        example,
        canonical_example,
        asset_type_compatibility,
        space_domain_mappings,
        knowledge_domains,
    )
    governance_rules = vocabulary.get("governance_rules") or []
    governance_rule_ids = {str(item.get("id")) for item in governance_rules if isinstance(item, dict)}
    require(governance_rule_ids == EXPECTED_GOVERNANCE_RULES, "governance_rule_ids_mismatch")

    require(manifest.get("consumer_boundaries") == EXPECTED_CONSUMERS, "consumer_boundaries_mismatch")
    status_boundary = manifest.get("status_boundary") or {}
    require(status_boundary.get("completion_status") == "not_complete", "completion_status_must_be_not_complete")
    for flag in ["accepted", "integrated", "production_ready", "customer_accepted", "kds_write_authorized", "deployment_authorized"]:
        require(status_boundary.get(flag) is False, f"status_boundary_must_be_false:{flag}")

    doc_id = "GPCF-DOC-KNOWLEDGE-ASSET-MODEL-20260802"
    require_text(
        MODEL_DOC,
        [
            doc_id,
            "project: GPCF",
            "status: draft",
            "version: v0.1",
            "owner: GPCF",
            "kds_path: 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud知识资产模型体系综合方案.md",
            "okf/knowledge-asset-envelope.schema.json",
            "okf/knowledge-asset-vocabulary.yaml",
            "okf/knowledge-asset-envelope.example.json",
            "completion_status: not_complete",
        ],
    )
    require_text(
        KNOWLEDGE_README,
        [doc_id, "GlobalCloud 知识资产模型体系综合方案", "| GPCF | draft |"],
    )
    require_text(
        DOCUMENT_REGISTER,
        [
            doc_id,
            "GlobalCloud知识资产模型体系综合方案.md",
            "| GPCF | WAS, XWAIL, AAAS",
            "| data-ai-knowledge | draft | 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud知识资产模型体系综合方案.md |",
        ],
    )
    require_text(MASTER_PLAN, ["KnowledgeAssetEnvelope", "GPCF 定义、KDS 主存、Brain 消费、MMC 调用"])
    require_text(IMPLEMENTATION_PLAN, ["知识资产模型实施链路", "KnowledgeAssetEnvelope"])
    validate_document_control_metadata()

    feature = load_yaml(FEATURE)
    require(feature.get("id") == "F-013", "invalid_feature_id")
    require(feature.get("status") == "active", "feature_must_remain_active")
    require((feature.get("loop") or {}).get("current_step") == "evaluate", "feature_step_must_remain_evaluate")
    require(
        "project_group_document_gate_rework_required" not in (feature.get("blockers") or []),
        "stale_project_group_document_gate_blocker",
    )
    require(
        "project_group_gate_readiness_failed" not in (feature.get("blockers") or []),
        "stale_project_group_gate_readiness_blocker",
    )
    require(
        "unexpected_external_kds_local_mirror_write_requires_review" in (feature.get("blockers") or []),
        "missing_external_local_mirror_review_blocker",
    )
    require_text(
        KDS_HANDOFF,
        [
            "adopt-knowledge-asset-envelope",
            "apply-ready",
            "不实施、不提交、不推送",
            "knowledge-object-approved-copy.example.json",
            "GPCF manifest 哈希复核",
        ],
    )
    # The external mirror's current completeness is a dynamic KDS admission
    # condition, evaluated by validate_f013_kds_apply_admission.py. Do not
    # bind this source-contract gate to a historical blocker name.

    print(
        "knowledge_asset_model_gate=pass "
        "contract_id=globalcloud.knowledge_asset contract_version=v0.1 contract_status=draft "
        f"artifacts={len(artifacts)} dependencies={len(dependencies)} "
        f"access_spaces={len(schema_spaces)} knowledge_domains={len(knowledge_domains)} "
        f"space_domain_mappings={len(space_domain_mappings)} "
        f"orthogonal_context_dimensions={len(EXPECTED_CONTEXT_REF_PREFIXES)} "
        f"okf_object_type_mappings={len(asset_type_compatibility)} "
        f"controlled_vocabularies=8 governance_rules={len(governance_rule_ids)} "
        f"example_validation=pass projection_modes_positive_cases={projection_positive_case_count} "
        f"projection_semantic_negative_cases={projection_semantic_negative_case_count} "
        f"approved_copy_linkage_positive_case=pass "
        f"approved_copy_linkage_negative_cases={approved_copy_linkage_negative_case_count} "
        f"canonical_link_positive_case=pass "
        f"canonical_link_negative_cases={canonical_link_negative_case_count} "
        f"authorization_positive_case=pass negative_cases={negative_case_count} hashes=pass "
        "master_plan_propagation=pass document_control_override=pass "
        "kds_handoff=planning_complete kds_apply_admission=separate_gate "
        "completion_status=not_complete accepted=false integrated=false "
        "production_ready=false customer_accepted=false kds_write_authorized=false deployment_authorized=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
