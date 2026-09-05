"""
Automated Pytest for wsi-patch-vision-transformer-agent Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    FeaturesEngine,
    RealtimeMonitoringDashboardEngine,
    AutomatedEscalationProtocolEngine,
    MultisiteDeploymentFrameworkEngine,
    TamperevidentAuditTrailEngine,
    ClinicalWorkflowIntegrationEngine,
    PredictiveAnalyticsEngine,
    PatientOutcomeTrackingEngine,
    BaseEnrichmentEngine,
    EnrichmentEngineResult,
    WsipatchvisiontransformeragentEnrichmentSuite,
    enrichment_suite,
)

def test_enrichment_suite_execution():
    suite = WsipatchvisiontransformeragentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 1
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = WsipatchvisiontransformeragentEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_base_engine_inheritance():
    """Test that all engines inherit from BaseEnrichmentEngine."""
    engines = [
        FeaturesEngine,
        RealtimeMonitoringDashboardEngine,
        AutomatedEscalationProtocolEngine,
        MultisiteDeploymentFrameworkEngine,
        TamperevidentAuditTrailEngine,
        ClinicalWorkflowIntegrationEngine,
        PredictiveAnalyticsEngine,
        PatientOutcomeTrackingEngine,
    ]
    for engine_cls in engines:
        assert issubclass(engine_cls, BaseEnrichmentEngine)
        instance = engine_cls()
        assert hasattr(instance, 'evaluate')
        assert hasattr(instance, 'history')

def test_engine_result_dataclass():
    """Test EnrichmentEngineResult dataclass creation."""
    result = EnrichmentEngineResult(
        feature_name="Test",
        status="OPTIMAL",
        score=1.0,
        alerts=[],
        recommendations=["Test recommendation"]
    )
    assert result.feature_name == "Test"
    assert result.status == "OPTIMAL"
    assert isinstance(result.timestamp, str)
