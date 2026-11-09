"""
Clinical Visualization and Summary Analytics for HealthGuard.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict
from src.models.entities import Patient, StratificationResult
from src.engines.risk_models import CompositeRiskEvaluator


class ClinicalVisualizer:
    """Generates diagnostic charts for clinical cohorts."""

    @staticmethod
    def build_summary_dataframe(patients: List[Patient], evaluator: CompositeRiskEvaluator) -> pd.DataFrame:
        """Combines patient details, biometrics, and risk scores into a DataFrame."""
        rows = []
        for p in patients:
            res_list = evaluator.evaluate_patient(p)
            res_dict = {res.condition_name: res.risk_category for res in res_list}
            scores_dict = {f"{res.condition_name}_score": res.risk_score for res in res_list}

            row = {
                "patient_id": p.patient_id,
                "name": p.name,
                "age": p.age,
                "gender": p.gender,
                "systolic_bp": p.biometrics.systolic_bp,
                "diastolic_bp": p.biometrics.diastolic_bp,
                "glucose": p.biometrics.fasting_glucose,
                "bmi": p.biometrics.bmi,
                "cholesterol": p.biometrics.cholesterol,
                "hypertension_risk": res_dict.get("Hypertension"),
                "diabetes_risk": res_dict.get("Type 2 Diabetes"),
                "cvd_risk": res_dict.get("Cardiovascular Disease"),
                "cvd_score": scores_dict.get("Cardiovascular Disease_score", 0.0)
            }
            rows.append(row)
        return pd.DataFrame(rows)

    @staticmethod
    def plot_cohort_summary(df: pd.DataFrame):
        """Generates a multi-panel visual dashboard of cohort risks."""
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # 1. Blood pressure vs Glucose scatter with CVD Risk hue
        sns.scatterplot(
            data=df,
            x="systolic_bp",
            y="glucose",
            hue="cvd_risk",
            palette={"Low": "green", "Moderate": "orange", "High": "red"},
            s=90,
            ax=axes[0]
        )
        axes[0].set_title("Blood Pressure vs. Fasting Glucose")
        axes[0].set_xlabel("Systolic BP (mmHg)")
        axes[0].set_ylabel("Fasting Glucose (mmol/L)")

        # 2. Hypertension Risk Category Counts
        sns.countplot(
            data=df,
            x="hypertension_risk",
            order=["Low", "Moderate", "High", "Critical"],
            palette="Set2",
            ax=axes[1]
        )
        axes[1].set_title("Hypertension Risk Stratification Breakdown")
        axes[1].set_xlabel("Risk Category")
        axes[1].set_ylabel("Number of Patients")

        # 3. BMI vs Cholesterol by Gender
        sns.scatterplot(
            data=df,
            x="bmi",
            y="cholesterol",
            hue="gender",
            style="gender",
            s=80,
            ax=axes[2]
        )
        axes[2].set_title("BMI vs. Total Cholesterol by Gender")
        axes[2].set_xlabel("BMI (kg/m²)")
        axes[2].set_ylabel("Total Cholesterol (mmol/L)")

        plt.tight_layout()
        plt.show()