#!/usr/bin/env python3
"""Shared runtime for real KDS development-space synchronization.

The module keeps secrets out of logs and makes every mutating KDS operation
explicit. It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SYNC_REGISTER = ROOT / "09-status/kds-development-space-sync-register.md"
LOCAL_KDS_ROOT = ROOT / ".kds/development-space"
PLAN_PATH = ROOT / ".kds/sync-plan.json"
LEDGER_PATH = ROOT / ".kds/sync-ledger.jsonl"
DEFAULT_ENV_FILE = Path("/Users/lujunxiang/.globalcloud/kds.env")

ALLOWED_SYNC_STATUSES = {"controlled", "operational_controlled"}
SKIPPED_SYNC_STATUSES = {"archive", "draft", "deprecated", "superseded"}


def load_env_file(path: Path | None = None) -> None:
    env_file = path or Path(os.environ.get("KDS_ENV_FILE", str(DEFAULT_ENV_FILE)))
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        try:
            parsed = shlex.split(value, posix=True)
        except ValueError:
            parsed = [value.strip().strip('"').strip("'")]
        os.environ[key] = parsed[0] if parsed else ""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(token: str) -> str:
    if not token:
        return "missing"
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]


def redact(value: str, token: str | None = None) -> str:
    if not value:
        return value
    redacted = value
    secret = token or os.environ.get("KDS_DEVELOPMENT_SPACE_TOKEN", "")
    if secret:
        redacted = redacted.replace(secret, f"<redacted:{fingerprint(secret)}>")
    return redacted


def run_local(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, redact(output)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


@dataclass(frozen=True)
class SyncRecord:
    doc_id: str
    source_path: str
    kds_path: str
    sync_direction: str
    kds_api_status: str

    @property
    def source(self) -> Path:
        return ROOT / self.source_path

    @property
    def local_mirror(self) -> Path:
        return LOCAL_KDS_ROOT / self.kds_path

    @property
    def status(self) -> str:
        if not self.source.exists():
            return "missing"
        if self.source_path.startswith(".codex/skills/") and self.source_path.endswith("/SKILL.md"):
            return "operational_controlled"
        return parse_frontmatter(self.source.read_text(encoding="utf-8")).get(
            "status", "missing"
        )

    @property
    def title(self) -> str:
        if not self.source.exists():
            return self.source_path
        fm = parse_frontmatter(self.source.read_text(encoding="utf-8"))
        return fm.get("title", self.source.stem)


def parse_sync_register(path: Path = SYNC_REGISTER) -> list[SyncRecord]:
    records: list[SyncRecord] = []
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| GPCF-DOC-"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        records.append(SyncRecord(cells[0], cells[1], cells[2], cells[3], cells[4]))
    return records


def load_plan(path: Path = PLAN_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_ledger(entry: dict[str, Any], path: Path = LEDGER_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = json.dumps(entry, ensure_ascii=False)
    path.open("a", encoding="utf-8").write(redact(safe) + "\n")


class KdsClientError(RuntimeError):
    pass


class KdsClient:
    """Small configurable REST client for KDS document APIs."""

    def __init__(self) -> None:
        load_env_file()
        self.base_url = os.environ.get("KDS_API_BASE_URL", "").rstrip("/")
        self.token = os.environ.get("KDS_DEVELOPMENT_SPACE_TOKEN", "")
        self.space = os.environ.get("KDS_SPACE_NAME", "开发")
        self.auth_header = os.environ.get("KDS_API_AUTH_HEADER", "Authorization")
        self.auth_scheme = os.environ.get("KDS_API_AUTH_SCHEME", "Bearer")
        self.timeout = float(os.environ.get("KDS_API_TIMEOUT_SECONDS", "20"))
        self.documents_path = os.environ.get(
            "KDS_API_DOCUMENTS_PATH", "/spaces/{space}/documents"
        )
        self.document_path = os.environ.get(
            "KDS_API_DOCUMENT_PATH", "/spaces/{space}/documents/{document_id}"
        )

    def require_configured(self) -> None:
        missing = []
        if not self.base_url:
            missing.append("KDS_API_BASE_URL")
        if not self.token:
            missing.append("KDS_DEVELOPMENT_SPACE_TOKEN")
        if missing:
            raise KdsClientError("missing " + ",".join(missing))

    def _url(self, template: str, **values: str) -> str:
        encoded = {k: urllib.parse.quote(v, safe="") for k, v in values.items()}
        encoded.setdefault("space", urllib.parse.quote(self.space, safe=""))
        path = template.format(**encoded)
        return self.base_url + path

    def _headers(self) -> dict[str, str]:
        auth_value = self.token if not self.auth_scheme else f"{self.auth_scheme} {self.token}"
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            self.auth_header: auth_value,
        }

    def request(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        self.require_configured()
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers=self._headers(),
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                body = json.loads(raw) if raw else {}
                return response.status, body
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise KdsClientError(redact(f"{method} {url} failed {exc.code}: {raw}", self.token))
        except urllib.error.URLError as exc:
            raise KdsClientError(redact(f"{method} {url} failed: {exc}", self.token))

    def list_documents(self) -> list[dict[str, Any]]:
        url = self._url(self.documents_path, space=self.space)
        _, body = self.request("GET", url)
        if isinstance(body, list):
            return body
        docs = body.get("documents", [])
        if not isinstance(docs, list):
            raise KdsClientError("KDS list response must be a list or contain documents[]")
        return docs

    def create_document(self, record: SyncRecord, content: str) -> tuple[int, dict[str, Any]]:
        payload = {
            "space": self.space,
            "path": record.kds_path,
            "title": record.title,
            "content": content,
            "metadata": {"doc_id": record.doc_id, "source_path": record.source_path},
        }
        return self.request("POST", self._url(self.documents_path, space=self.space), payload)

    def update_document(
        self,
        remote_document: dict[str, Any],
        record: SyncRecord,
        content: str,
    ) -> tuple[int, dict[str, Any]]:
        document_id = str(
            remote_document.get("id")
            or remote_document.get("document_id")
            or remote_document.get("path")
            or record.kds_path
        )
        payload = {
            "space": self.space,
            "path": record.kds_path,
            "title": record.title,
            "content": content,
            "metadata": {"doc_id": record.doc_id, "source_path": record.source_path},
            "version": remote_document.get("version"),
            "etag": remote_document.get("etag"),
        }
        return self.request(
            "PUT",
            self._url(self.document_path, space=self.space, document_id=document_id),
            payload,
        )


def remote_index(documents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for doc in documents:
        path = str(doc.get("path") or doc.get("kds_path") or "")
        if path:
            index[path] = doc
    return index


def remote_hash(document: dict[str, Any]) -> str:
    for key in ("hash", "sha256", "content_hash"):
        value = document.get(key)
        if value:
            return str(value)
    content = document.get("content")
    if isinstance(content, str):
        return sha256_text(content)
    return ""
