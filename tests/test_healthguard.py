"""
Unit tests for HealthGuard Analytics.
Verifies Encapsulation, Abstraction, Inheritance, and Polymorphism.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.models.entities import Patient, BiometricRecord, InvalidBiometricError
from src.engines.risk_models import (
    HypertensionRiskModel,
    DiabetesRiskModel,
    CardiovascularRiskModel,
    CompositeRiskEvaluator
)


def test_biometric_validation_valid():
    """Tests that biologically valid values instantiate properly."""
    record = BiometricRecord(systolic_bp=120, diastolic_bp=80, fasting_glucose=5.5, bmi=24.5, cholesterol=4.5)
    assert record.systolic_bp == 120
    assert record.diastolic_bp == 80


def test_biometric_validation_invalid_bp():
    """Tests that impossible blood pressure values raise InvalidBiometricError."""
    with pytest.raises(InvalidBiometricError):
        # Diastolic greater than systolic
        BiometricRecord(systolic_bp=100, diastolic_bp=110, fasting_glucose=5.5, bmi=24.5, cholesterol=4.5)


def test_hypertension_model_evaluation():
    """Tests the specialized Hypertension scoring."""
    patient = Patient("P01", "Test Patient", 50, "F")
    patient.record_biometrics(
        BiometricRecord(systolic_bp=165, diastolic_bp=100, fasting_glucose=5.0, bmi=24.0, cholesterol=4.0)
    )

    model = HypertensionRiskModel()
    result = model.evaluate_risk(patient)
    assert result.condition_name == "Hypertension"
    assert result.risk_category == "High"


def test_diabetes_model_evaluation():
    """Tests Diabetes scoring for high fasting glucose."""
    patient = Patient("P02", "Diabetic Patient", 60, "M")
    patient.record_biometrics(
        BiometricRecord(systolic_bp=120, diastolic_bp=80, fasting_glucose=12.0, bmi=31.0, cholesterol=4.5)
    )

    model = DiabetesRiskModel()
    result = model.evaluate_risk(patient)
    assert result.condition_name == "Type 2 Diabetes"
    assert result.risk_category == "High"


def test_polymorphic_composite_evaluator():
    """Tests that CompositeRiskEvaluator evaluates all models uniformly."""
    patient = Patient("P03", "Cohort Member", 55, "M")
    patient.record_biometrics(
        BiometricRecord(systolic_bp=140, diastolic_bp=90, fasting_glucose=6.0, bmi=28.0, cholesterol=5.5)
    )

    evaluator = CompositeRiskEvaluator([
        HypertensionRiskModel(),
        DiabetesRiskModel(),
        CardiovascularRiskModel()
    ])

    results = evaluator.evaluate_patient(patient)
    assert len(results) == 3
    conditions = [r.condition_name for r in results]
    assert "Hypertension" in conditions
    assert "Type 2 Diabetes" in conditions
    assert "Cardiovascular Disease" in conditions