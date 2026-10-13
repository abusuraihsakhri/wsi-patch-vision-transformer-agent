"""Regression tests for security, CSV parsing, and API behavior."""
import csv
import json

import pytest

from agents.base import AuditTrail
from agents.csv_utils import parse_csv_boolean, escape_csv_formula
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from cli import main as main_cli
from patho_vit_agent.cli import main as legacy_cli


def test_hmac_detects_entry_tampering():
    trail = AuditTrail(secret_key="unit-test-key")
    trail.log("test", "worker", "EVENT", {"case": "synthetic"})
    assert trail.verify_integrity()
    trail.logs[0]["event_type"] = "MODIFIED"
    assert not trail.verify_integrity()


def test_hmac_detects_signature_tampering():
    trail = AuditTrail(secret_key="unit-test-key")
    trail.log("test", "worker", "EVENT", {"case": "synthetic"})
    trail.logs[0]["current_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_audit_trail_is_defensively_copied():
    trail = AuditTrail(secret_key="unit-test-key")
    trail.log("test", "worker", "EVENT", {"case": "synthetic"})
    trail.get_trail()[0]["actor"] = "tampered-copy"
    assert trail.verify_integrity()


@pytest.mark.parametrize("value,expected", [
    (False, False), (True, True), ("False", False), (" TRUE ", True),
    ("0", False), ("1", True), ("no", False), ("yes", True), ("", False),
])
def test_csv_boolean_values(value, expected):
    assert parse_csv_boolean(value) is expected


@pytest.mark.parametrize("value", ["maybe", "truthy", "2"])
def test_csv_boolean_rejects_ambiguous(value):
    with pytest.raises(ValueError, match="Invalid boolean"):
        parse_csv_boolean(value)


def test_csv_formula_escape():
    assert escape_csv_formula(" =1+2") == "' =1+2"
    assert escape_csv_formula("@SUM(A1)") == "'@SUM(A1)"
    assert escape_csv_formula("SPECIMEN-1") == "SPECIMEN-1"


@pytest.mark.parametrize("entrypoint,status_field", [
    (main_cli, "overall_urgency"), (legacy_cli, "overall_status")
])
def test_batch_false_does_not_trigger_critical(tmp_path, entrypoint, status_field):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"
    with source.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=[
            "task_id", "target_identifier", "primary_metric", "secondary_metric",
            "is_critical_flag", "status_descriptor"
        ])
        writer.writeheader()
        writer.writerow(dict(task_id="T1", target_identifier="KEY-1",
            primary_metric="5", secondary_metric="3",
            is_critical_flag="False", status_descriptor="NOMINAL"))
        writer.writerow(dict(task_id="T2", target_identifier="KEY-2",
            primary_metric="5", secondary_metric="3",
            is_critical_flag="True", status_descriptor="NOMINAL"))
    assert entrypoint(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 2
    assert rows[0][status_field] in ("ROUTINE", "NOMINAL_OPTIMAL")
    assert "CRITICAL" in rows[1][status_field]


def test_benchmark_cases():
    from pathlib import Path
    dataset = json.loads((Path(__file__).parent.parent / "benchmark_dataset.json").read_text())
    supervisor = SystemSupervisor()
    for case in dataset["test_cases"]:
        if "payload" not in case:
            continue
        dossier = supervisor.process_task(SystemTaskPayload(**case["payload"]))
        assert dossier.overall_urgency.value == case["expected_urgency"]
        assert dossier.integrity_status.value == case["expected_integrity"]


def test_api_web_routes_and_sensitive_input():
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert client.get("/app.mjs").status_code == 200
    payload = dict(task_id="T1", target_identifier="KEY-1",
                   primary_metric=5, secondary_metric=3, status_descriptor="NOMINAL")
    assert client.post("/api/audit", json=payload).status_code == 200
    payload["target_identifier"] = "MRN-123456"
    assert client.post("/api/audit", json=payload).status_code == 422
