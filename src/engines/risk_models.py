"""
Clinical Risk Stratification Engines.
Demonstrates Abstraction, Inheritance, and Polymorphism.
"""

from abc import ABC, abstractmethod
from typing import List
from src.models.entities import Patient, BiometricRecord, StratificationResult


class RiskStratifier(ABC):
    """
    Abstract Base Class defining the contract for clinical risk models (Abstraction).
    """
    def __init__(self, condition_name: str):
        self.condition_name = condition_name

    @abstractmethod
    def evaluate_risk(self, patient: Patient) -> StratificationResult:
        """Polymorphic method: must be implemented by derived risk models."""
        pass


class HypertensionRiskModel(RiskStratifier):
    """
    Inherits from RiskStratifier (Inheritance & Specialization).
    Evaluates blood pressure stages based on WHO / AHA guidelines.
    """
    def __init__(self):
        super().__init__("Hypertension")

    def evaluate_risk(self, patient: Patient) -> StratificationResult:
        bio = patient.biometrics
        if not bio:
            return StratificationResult(self.condition_name, 0.0, "Unknown", "No biometrics recorded.")

        sys = bio.systolic_bp
        dia = bio.diastolic_bp

        if sys >= 180 or dia >= 120:
            return StratificationResult(self.condition_name, 95.0, "Critical", "Hypertensive crisis. Immediate medical attention required.")
        elif sys >= 140 or dia >= 90:
            return StratificationResult(self.condition_name, 75.0, "High", "Stage 2 Hypertension. Pharmacological intervention recommended.")
        elif sys >= 130 or dia >= 80:
            return StratificationResult(self.condition_name, 45.0, "Moderate", "Stage 1 Hypertension. Lifestyle modification recommended.")
        else:
            return StratificationResult(self.condition_name, 15.0, "Low", "Blood pressure within normal ranges.")


class DiabetesRiskModel(RiskStratifier):
    """
    Inherits from RiskStratifier.
    Evaluates glycemic risk from fasting plasma glucose and BMI.
    """
    def __init__(self):
        super().__init__("Type 2 Diabetes")

    def evaluate_risk(self, patient: Patient) -> StratificationResult:
        bio = patient.biometrics
        if not bio:
            return StratificationResult(self.condition_name, 0.0, "Unknown", "No biometrics recorded.")

        glucose = bio.fasting_glucose
        bmi = bio.bmi

        # Risk scoring logic
        score = 10.0
        if glucose >= 11.1:
            score += 70.0
        elif glucose >= 7.0:
            score += 50.0
        elif glucose >= 5.6:
            score += 25.0

        if bmi >= 30.0:
            score += 15.0
        elif bmi >= 25.0:
            score += 10.0

        score = min(score, 100.0)

        if score >= 75.0:
            category = "High"
            note = "High risk of Diabetes. Diagnostic HbA1c testing recommended."
        elif score >= 40.0:
            category = "Moderate"
            note = "Pre-diabetes risk indicator. Dietary intervention advised."
        else:
            category = "Low"
            note = "Glycemic indicators within healthy baseline."

        return StratificationResult(self.condition_name, score, category, note)


class CardiovascularRiskModel(RiskStratifier):
    """
    Inherits from RiskStratifier.
    Assesses composite risk from age, cholesterol, systolic BP, and BMI.
    """
    def __init__(self):
        super().__init__("Cardiovascular Disease")

    def evaluate_risk(self, patient: Patient) -> StratificationResult:
        bio = patient.biometrics
        if not bio:
            return StratificationResult(self.condition_name, 0.0, "Unknown", "No biometrics recorded.")

        score = 0.0
        # Age contribution
        if patient.age >= 60:
            score += 30.0
        elif patient.age >= 45:
            score += 15.0

        # Blood pressure contribution
        if bio.systolic_bp >= 140:
            score += 25.0
        elif bio.systolic_bp >= 130:
            score += 15.0

        # Cholesterol contribution
        if bio.cholesterol >= 6.2:
            score += 25.0
        elif bio.cholesterol >= 5.2:
            score += 15.0

        # BMI contribution
        if bio.bmi >= 30.0:
            score += 20.0

        score = min(score, 100.0)

        if score >= 70.0:
            category = "High"
            note = "Elevated composite cardiovascular risk profile."
        elif score >= 40.0:
            category = "Moderate"
            note = "Moderate CVD risk. Regular screening recommended."
        else:
            category = "Low"
            note = "Favorable cardiovascular risk metrics."

        return StratificationResult(self.condition_name, score, category, note)


class CompositeRiskEvaluator:
    """
    Demonstrates Polymorphism.
    Holds a list of diverse RiskStratifier models and evaluates them uniformly.
    """
    def __init__(self, models: List[RiskStratifier]):
        self._models = models

    def evaluate_patient(self, patient: Patient) -> List[StratificationResult]:
        # Polymorphic invocation: calls evaluate_risk regardless of specific concrete subclass
        return [model.evaluate_risk(patient) for model in self._models]