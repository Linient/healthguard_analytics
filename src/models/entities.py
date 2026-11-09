"""
Domain models for HealthGuard Analytics.
Demonstrates Encapsulation and Data Integrity.
"""

from dataclasses import dataclass
from typing import List, Optional


class InvalidBiometricError(ValueError):
    """Raised when biometric values are outside physically possible biological ranges."""
    pass


@dataclass
class BiometricRecord:
    """
    Encapsulates vital sign measurements for a patient.
    Enforces validation rules on creation.
    """
    systolic_bp: int       # mmHg (normal ~ 90-180)
    diastolic_bp: int      # mmHg (normal ~ 50-120)
    fasting_glucose: float # mmol/L or mg/dL (here in mmol/L: normal 3.9 - 11.0)
    bmi: float             # kg/m^2 (normal ~ 15 - 50)
    cholesterol: float     # mmol/L (normal ~ 2.5 - 10.0)

    def __post_init__(self):
        # Validation rules: ensure biologically sensible numbers
        if not (50 <= self.systolic_bp <= 260):
            raise InvalidBiometricError(f"Invalid systolic BP: {self.systolic_bp} mmHg.")
        if not (30 <= self.diastolic_bp <= 160):
            raise InvalidBiometricError(f"Invalid diastolic BP: {self.diastolic_bp} mmHg.")
        if self.diastolic_bp >= self.systolic_bp:
            raise InvalidBiometricError("Diastolic BP cannot be greater than or equal to systolic BP.")
        if not (1.0 <= self.fasting_glucose <= 35.0):
            raise InvalidBiometricError(f"Invalid glucose reading: {self.fasting_glucose} mmol/L.")
        if not (10.0 <= self.bmi <= 70.0):
            raise InvalidBiometricError(f"Invalid BMI value: {self.bmi}.")
        if not (1.0 <= self.cholesterol <= 20.0):
            raise InvalidBiometricError(f"Invalid cholesterol level: {self.cholesterol} mmol/L.")


@dataclass
class StratificationResult:
    """Represents the output of a risk evaluation."""
    condition_name: str
    risk_score: float      # Score from 0 to 100
    risk_category: str     # 'Low', 'Moderate', 'High', 'Critical'
    clinical_note: str


class Patient:
    """
    Represents an individual patient, encapsulating their demographics and records.
    """
    def __init__(self, patient_id: str, name: str, age: int, gender: str):
        if age < 0 or age > 120:
            raise ValueError(f"Invalid age: {age}")
        if gender.upper() not in ["M", "F", "OTHER"]:
            raise ValueError(f"Invalid gender: {gender}")

        self._patient_id = patient_id
        self._name = name
        self._age = age
        self._gender = gender.upper()
        self._biometrics: Optional[BiometricRecord] = None

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    def gender(self) -> str:
        return self._gender

    @property
    def biometrics(self) -> Optional[BiometricRecord]:
        return self._biometrics

    def record_biometrics(self, record: BiometricRecord) -> None:
        """Sets the patient's current biometric record."""
        self._biometrics = record

    def __repr__(self) -> str:
        return f"Patient(id='{self._patient_id}', name='{self._name}', age={self._age}, gender='{self._gender}')"