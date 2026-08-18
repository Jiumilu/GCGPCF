#!/usr/bin/env python3
"""Validate the GKE-001 OpenSpec Program and CodeGraph domain bindings."""

from __future__ import annotations

import argparse
import copy
import hashlib
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
PROGRAM_BINDING = ROOT / "governance/openspec/gke001-program-binding.yaml"
CODEGRAPH_BINDING = ROOT / "governance/codegraph/gke001-engineering-domain-binding.yaml"
CODEGRAPH_REGISTRY = ROOT / "governance/codegraph/repo-codegraph-registry.yaml"
OPENSPEC_CONFIG = ROOT / "openspec/config.yaml"
OPENSPEC_CHANGE = ROOT / "openspec/changes/integrate-gke001-openspec-codegraph"
ROADMAP = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-application-program-roadmap-v1.yaml"
CANONICAL_MANIFEST = ROOT / "okf/knowledge-asset-contract-manifest.yaml"
IMPLEMENTATION_PLAN = ROOT / "03-data-ai-knowledge/GlobalCloud知识工程应用体系实施方案.md"
COORDINATOR_PROMPT = ROOT / "02-governance/loop/GKE-001长期实施调度提示词.md"

COORDINATOR_THREAD = "019f0697-c8ce-7110-8ac8-9a7dbc6ba2a5"
REVIEW_THREAD = "019fc228-2403-7123-9cae-fb9028850b84"
CANONICAL_SHA256 = "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de"
ROADMAP_SHA256 = "32f00e131b0dab667fa7403dbd6d6a79c865f517959c5d6b227f82340534ad9f"
PROJECTS = {
    "AAAS", "Brain", "WAS", "XiaoC", "WAES", "GPC", "Studio", "GPCF", "XWAIL",
    "GFIS", "MMC", "KDS", "XiaoG", "PVAOS", "SOP", "PKC", "XGD", "ICP",
}
REPOSITORIES = {
    "gfis", "gpc", "pvaos", "waes", "kds", "brain", "pkc", "xiaoc", "xgd",
    "xiaog", "mmc", "gpcf", "studio", "was",
}
UNINDEXED_PROJECTS = {"AAAS", "XWAIL", "SOP", "ICP"}
RELEASES = {"release_0", "release_1", "release_2", "release_3"}


class BindingError(ValueError):
    """Raised when a controlled GKE-001 binding drifts."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise BindingError(reason)


def read(path: Path) -> str:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_controlled_yaml(path: Path) -> dict[str, Any]:
    text = read(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        require(len(parts) == 3, f"invalid_frontmatter:{path.relative_to(ROOT)}")
        text = parts[2]
    data = yaml.safe_load(text)
    require(isinstance(data, dict), f"invalid_yaml_root:{path.relative_to(ROOT)}")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_program(program: dict[str, Any], roadmap_sha: str, canonical_sha: str) -> None:
    require(program.get("id") == "GKE-001", "program_id_mismatch")
    require(program.get("representation") == "cross_repository_engineering_domain", "program_representation_mismatch")
    coordinator = program.get("coordinator", {})
    require(coordinator.get("thread_id") == COORDINATOR_THREAD, "coordinator_thread_mismatch")
    require(coordinator.get("role") == "sole_gke001_program_coordinator", "coordinator_role_mismatch")
    canonical = program.get("canonical_governance", {})
    require(canonical.get("review_thread_id") == REVIEW_THREAD, "review_thread_mismatch")
    require(canonical.get("feature_ref") == "F-013", "canonical_feature_mismatch")
    require(canonical.get("contract_revision") == "v0.1", "canonical_revision_mismatch")
    require(canonical.get("manifest_path") == str(CANONICAL_MANIFEST.relative_to(ROOT)), "canonical_manifest_path_mismatch")
    require(canonical.get("manifest_sha256") == CANONICAL_SHA256, "canonical_sha_mismatch")
    require(canonical_sha == CANONICAL_SHA256, "canonical_manifest_content_sha_mismatch")
    roadmap = program.get("application_roadmap", {})
    require(roadmap.get("path") == str(ROADMAP.relative_to(ROOT)), "roadmap_path_mismatch")
    require(roadmap.get("sha256") == ROADMAP_SHA256, "roadmap_declared_sha_mismatch")
    require(roadmap_sha == ROADMAP_SHA256, "roadmap_sha_mismatch")
    change = program.get("openspec_change", {})
    require(change.get("id") == "integrate-gke001-openspec-codegraph", "openspec_change_mismatch")
    require(set(change.get("capabilities", ())) == {"gke001-program-governance", "gke001-codegraph-binding"}, "capability_set_mismatch")
    require({item.get("id") for item in program.get("releases", ())} == RELEASES, "release_set_mismatch")
    scope = program.get("project_scope", {})
    require(scope.get("count") == 18, "project_count_mismatch")
    require(set(scope.get("projects", ())) == PROJECTS, "project_scope_mismatch")
    required = set(program.get("required_change_declaration", ()))
    require({"program_ref", "release_ref", "feature_ref", "codegraph_impact", "authorization", "rollback"} <= required, "change_declaration_incomplete")
    governance = program.get("governance", {})
    require(governance.get("repository_opsx_handoff_required") is True, "opsx_handoff_not_required")
    require(governance.get("independent_harness_review_required") is True, "harness_review_not_required")
    require(governance.get("openspec_completion_is_delivery_acceptance") is False, "openspec_acceptance_boundary_drift")
    require(governance.get("codegraph_index_is_runtime_integration") is False, "codegraph_integration_boundary_drift")
    for key, value in program.get("authorization", {}).items():
        require(value is False, f"program_authorization_drift:{key}")
    require(program.get("status") == {"engineering": "active", "cross_project": "partial", "completion": "not_complete"}, "program_status_mismatch")


def validate_codegraph(binding: dict[str, Any], registry: dict[str, Any]) -> None:
    require(binding.get("id") == "gke001", "codegraph_binding_id_mismatch")
    require(binding.get("engineering_domain") == "GKE-001", "codegraph_domain_mismatch")
    require(binding.get("representation") == "engineering_domain_not_repository", "codegraph_representation_mismatch")
    require(binding.get("indexed_repository_count") == 14, "indexed_repository_count_mismatch")
    require(binding.get("governed_project_count") == 18, "governed_project_count_mismatch")
    require(set(binding.get("indexed_repositories", ())) == REPOSITORIES, "indexed_repository_set_mismatch")
    require(set(binding.get("governed_projects_without_repository_index", ())) == UNINDEXED_PROJECTS, "unindexed_project_set_mismatch")
    nodes = binding.get("nodes", {})
    require(nodes.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "codegraph_coordinator_mismatch")
    require(nodes.get("canonical_feature", {}).get("id") == "F-013", "codegraph_feature_mismatch")
    require(nodes.get("canonical_contract", {}).get("manifest_path") == str(CANONICAL_MANIFEST.relative_to(ROOT)), "codegraph_canonical_manifest_path_mismatch")
    require(nodes.get("canonical_contract", {}).get("manifest_sha256") == CANONICAL_SHA256, "codegraph_canonical_sha_mismatch")
    require(nodes.get("application_roadmap", {}).get("sha256") == ROADMAP_SHA256, "codegraph_roadmap_sha_mismatch")
    require(set(nodes.get("releases", ())) == RELEASES, "codegraph_release_set_mismatch")
    require(nodes.get("openspec_change") == str(OPENSPEC_CHANGE.relative_to(ROOT)), "codegraph_openspec_path_mismatch")
    boundary = binding.get("evidence_boundary", {})
    require(boundary.get("indexed_governance_artifacts_only") is True, "codegraph_evidence_scope_mismatch")
    for key in ("proves_cross_repository_runtime_integration", "proves_real_kds_read_or_write", "proves_customer_test_ready"):
        require(boundary.get(key) is False, f"codegraph_evidence_boundary_drift:{key}")
    for key, value in binding.get("authorization", {}).items():
        require(value is False, f"codegraph_authorization_drift:{key}")
    require(binding.get("status") == {"engineering": "active", "cross_project": "partial", "completion": "not_complete"}, "codegraph_status_mismatch")

    registry_meta = registry.get("registry", {})
    require(registry_meta.get("repo_count") == 14, "registry_repo_count_mismatch")
    require(len(registry.get("repositories", ())) == 14, "registry_repository_length_mismatch")
    require({item.get("id") for item in registry.get("repositories", ())} == REPOSITORIES, "registry_repository_set_mismatch")
    domains = {item.get("id"): item for item in registry.get("engineering_domains", ())}
    require(set(domains) == {"gke001"}, "engineering_domain_registry_mismatch")
    domain = domains["gke001"]
    require(domain.get("binding") == str(CODEGRAPH_BINDING.relative_to(ROOT)), "engineering_domain_binding_path_mismatch")
    require(domain.get("indexed_repository_count") == 14, "engineering_domain_index_count_mismatch")
    require(domain.get("governed_project_count") == 18, "engineering_domain_project_count_mismatch")


def validate_entry_points() -> None:
    config = read(OPENSPEC_CONFIG)
    implementation = read(IMPLEMENTATION_PLAN)
    prompt = read(COORDINATOR_PROMPT)
    for token in (str(PROGRAM_BINDING.relative_to(ROOT)), str(CODEGRAPH_BINDING.relative_to(ROOT))):
        require(token in config, f"openspec_config_binding_missing:{token}")
        require(token in implementation, f"implementation_plan_binding_missing:{token}")
        require(token in prompt, f"coordinator_prompt_binding_missing:{token}")
    for path in (
        OPENSPEC_CHANGE / "proposal.md",
        OPENSPEC_CHANGE / "design.md",
        OPENSPEC_CHANGE / "tasks.md",
        OPENSPEC_CHANGE / "specs/gke001-program-governance/spec.md",
        OPENSPEC_CHANGE / "specs/gke001-codegraph-binding/spec.md",
    ):
        read(path)


def run_self_test(program: dict[str, Any], binding: dict[str, Any], registry: dict[str, Any]) -> None:
    bad_program = copy.deepcopy(program)
    bad_program["application_roadmap"]["sha256"] = "0" * 64
    try:
        validate_program(bad_program, ROADMAP_SHA256, CANONICAL_SHA256)
    except BindingError as error:
        require(str(error) == "roadmap_declared_sha_mismatch", "self_test_wrong_program_failure")
    else:
        raise BindingError("self_test_program_drift_not_detected")

    bad_binding = copy.deepcopy(binding)
    bad_binding["indexed_repository_count"] = 15
    try:
        validate_codegraph(bad_binding, registry)
    except BindingError as error:
        require(str(error) == "indexed_repository_count_mismatch", "self_test_wrong_codegraph_failure")
    else:
        raise BindingError("self_test_codegraph_drift_not_detected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="also prove representative drift is rejected")
    args = parser.parse_args()
    try:
        program = load_controlled_yaml(PROGRAM_BINDING)["gke001_program_binding"]
        binding = load_controlled_yaml(CODEGRAPH_BINDING)["gke001_codegraph_binding"]
        registry = load_controlled_yaml(CODEGRAPH_REGISTRY)
        roadmap_sha = sha256(ROADMAP)
        canonical_sha = sha256(CANONICAL_MANIFEST)
        validate_program(program, roadmap_sha, canonical_sha)
        validate_codegraph(binding, registry)
        validate_entry_points()
        if args.self_test:
            run_self_test(program, binding, registry)
    except (BindingError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"gke001_openspec_codegraph_binding=fail reason={error}")
        return 1
    print(
        "gke001_openspec_codegraph_binding=pass "
        "program=GKE-001 feature=F-013 releases=4 projects=18 repositories=14 "
        f"roadmap_sha256={ROADMAP_SHA256} self_test={'pass' if args.self_test else 'not_run'} "
        "status=active_partial_not_complete"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
