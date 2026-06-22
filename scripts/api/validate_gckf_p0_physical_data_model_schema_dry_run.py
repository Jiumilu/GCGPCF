#!/usr/bin/env python3
"""Validate P0 physical data model schema draft.

This validator parses SQL text only. It does not execute migrations, connect to
databases, mutate KDS, write business systems, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-physical-data-model-schema-dry-run-v0.1.json"


def parse_tables(sql: str) -> dict[str, str]:
    matches = re.finditer(r"CREATE TABLE\s+([a-zA-Z0-9_]+)\s*\((.*?)\);", sql, re.S | re.I)
    return {match.group(1): match.group(2) for match in matches}


def main() -> int:
    fixture = json.loads(FIXTURE.read_text())
    schema_path = ROOT / fixture["schemaPath"]
    sql = schema_path.read_text()
    tables = parse_tables(sql)
    expected = fixture["expectedSummary"]
    failures: list[str] = []

    required_tables = fixture["requiredTables"]
    missing_tables = [table for table in required_tables if table not in tables]
    extra_required_dupes = len(required_tables) - len(set(required_tables))
    if missing_tables:
        failures.append(f"missing tables: {missing_tables}")
    if extra_required_dupes:
        failures.append(f"duplicate required tables: {extra_required_dupes}")
    if len(required_tables) != expected["tableCount"]:
        failures.append(f"tableCount expected={expected['tableCount']} actual={len(required_tables)}")

    tables_with_pk = 0
    tables_with_tenant = 0
    for table in required_tables:
        body = tables.get(table, "")
        if re.search(r"\bid\s+TEXT\s+PRIMARY\s+KEY\b", body, re.I):
            tables_with_pk += 1
        else:
            failures.append(f"{table} missing id TEXT PRIMARY KEY")
        if re.search(r"\btenant_id\s+TEXT\s+NOT\s+NULL\b", body, re.I):
            tables_with_tenant += 1
        else:
            failures.append(f"{table} missing tenant_id TEXT NOT NULL")

    if tables_with_pk != expected["tablesWithPrimaryKey"]:
        failures.append(f"tablesWithPrimaryKey expected={expected['tablesWithPrimaryKey']} actual={tables_with_pk}")
    if tables_with_tenant != expected["tablesWithTenantId"]:
        failures.append(f"tablesWithTenantId expected={expected['tablesWithTenantId']} actual={tables_with_tenant}")

    if len(fixture["tableGroups"]) != expected["tableGroupCount"]:
        failures.append(
            f"tableGroupCount expected={expected['tableGroupCount']} actual={len(fixture['tableGroups'])}"
        )
    grouped = {table for group_tables in fixture["tableGroups"].values() for table in group_tables}
    if grouped != set(required_tables):
        failures.append(
            f"grouped table mismatch missing={sorted(set(required_tables) - grouped)} extra={sorted(grouped - set(required_tables))}"
        )

    forbidden_matches = [pattern for pattern in fixture["forbiddenSql"] if pattern.upper() in sql.upper()]
    if len(forbidden_matches) != expected["forbiddenSqlMatches"]:
        failures.append(f"forbiddenSqlMatches expected=0 actual={forbidden_matches}")

    for key, value in fixture["forbiddenExecution"].items():
        if value != 0:
            failures.append(f"{key} must be 0")
        if expected.get(key) != value:
            failures.append(f"{key} expected={expected.get(key)!r} actual={value!r}")
    if expected["noWrite"] is not True:
        failures.append("noWrite must be true")

    if failures:
        print("gckf_p0_physical_data_model_schema_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_physical_data_model_schema_dry_run=pass "
        f"tables={expected['tableCount']} groups={expected['tableGroupCount']} "
        f"primary_keys={tables_with_pk} tenant_ids={tables_with_tenant} "
        "forbidden_sql=0 runs_migration=0 connects_database=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
