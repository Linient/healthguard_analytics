"""
Data Ingestion Pipeline for HealthGuard Analytics.
Loads cohort CSV datasets and handles invalid entries gracefully.
"""

import pandas as pd
from typing import List, Tuple
from src.models.entities import Patient, BiometricRecord, InvalidBiometricError


class CohortDataLoader:
    """Handles CSV ingestion and patient entity instantiation."""

    @staticmethod
    def load_from_csv(filepath: str) -> Tuple[List[Patient], List[str]]:
        """
        Reads patient biometric data from a CSV file.
        Returns:
            Tuple of (valid_patients_list, error_logs_list)
        """
        df = pd.read_csv(filepath)
        valid_patients: List[Patient] = []
        error_logs: List[str] = []

        for index, row in df.iterrows():
            try:
                # 1. Create Patient
                patient = Patient(
                    patient_id=str(row["patient_id"]),
                    name=str(row["name"]),
                    age=int(row["age"]),
                    gender=str(row["gender"])
                )

                # 2. Create Biometric Record (validates bounds automatically)
                bio = BiometricRecord(
                    systolic_bp=int(row["systolic_bp"]),
                    diastolic_bp=int(row["diastolic_bp"]),
                    fasting_glucose=float(row["fasting_glucose"]),
                    bmi=float(row["bmi"]),
                    cholesterol=float(row["cholesterol"])
                )
                patient.record_biometrics(bio)
                valid_patients.append(patient)

            except (InvalidBiometricError, ValueError) as err:
                error_logs.append(f"Row {index + 1} ({row.get('patient_id', 'Unknown')}): {err}")

        return valid_patients, error_logs