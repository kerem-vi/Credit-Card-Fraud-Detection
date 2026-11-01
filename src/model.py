from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "creditcard.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "fraud_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"


class FraudModel:
    def __init__(self) -> None:
        self.pipeline: Pipeline | None = None
        self.feature_names: list[str] = []
        self.metrics: dict[str, Any] = {}
        self.class_distribution: dict[str, int] = {}

    def load(self) -> bool:
        if not MODEL_PATH.exists():
            return False

        payload = joblib.load(MODEL_PATH)
        self.pipeline = payload["pipeline"]
        self.feature_names = payload["feature_names"]
        self.class_distribution = payload.get("class_distribution", {})
        if METRICS_PATH.exists():
            self.metrics = json.loads(METRICS_PATH.read_text())
        return True

    def train(self, data_path: Path = DATA_PATH) -> dict[str, Any]:
        if not data_path.exists():
            raise FileNotFoundError(
                f"Veri seti bulunamadı: {data_path}. "
                "Kaggle creditcard.csv dosyasını data/ klasörüne ekleyin."
            )

        frame = pd.read_csv(data_path)
        if "Class" not in frame.columns:
            raise ValueError("Veri setinde hedef sütunu olarak 'Class' bulunamadı.")

        frame = frame.dropna(subset=["Class"])
        features = frame.drop(columns=["Class"])
        target = frame["Class"].astype(int)
        self.feature_names = list(features.columns)
        self.class_distribution = {
            "normal": int((target == 0).sum()),
            "fraud": int((target == 1).sum()),
        }

        numeric_features = list(features.columns)
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="median")),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    numeric_features,
                )
            ]
        )

        model = RandomForestClassifier(
            n_estimators=120,
            class_weight="balanced",
            n_jobs=-1,
            random_state=42,
        )
        self.pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("classifier", model)]
        )

        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=0.2,
            stratify=target,
            random_state=42,
        )
        self.pipeline.fit(x_train, y_train)
        probabilities = self.pipeline.predict_proba(x_test)[:, 1]
        predictions = (probabilities >= 0.5).astype(int)
        self.metrics = {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "precision": round(
                float(precision_score(y_test, predictions, zero_division=0)), 4
            ),
            "recall": round(
                float(recall_score(y_test, predictions, zero_division=0)), 4
            ),
            "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
            "test_size": int(len(y_test)),
        }

        MODEL_DIR.mkdir(exist_ok=True)
        joblib.dump(
            {
                "pipeline": self.pipeline,
                "feature_names": self.feature_names,
                "class_distribution": self.class_distribution,
            },
            MODEL_PATH,
        )
        METRICS_PATH.write_text(json.dumps(self.metrics, indent=2))
        return self.metrics

    def predict(self, values: dict[str, float]) -> dict[str, Any]:
        if self.pipeline is None:
            raise RuntimeError("Model henüz yüklenmedi veya eğitilmedi.")

        row = pd.DataFrame(
            [{name: float(values.get(name, 0)) for name in self.feature_names}],
            columns=self.feature_names,
        )
        probability = float(self.pipeline.predict_proba(row)[0, 1])
        is_fraud = probability >= 0.5
        return {
            "is_fraud": is_fraud,
            "label": "Şüpheli işlem" if is_fraud else "Normal işlem",
            "probability": round(probability * 100, 2),
        }


def build_comparison(data_path: Path = DATA_PATH) -> dict[str, Any]:
    """Train the two baseline models described in the project scope."""
    frame = pd.read_csv(data_path)
    features = frame.drop(columns=["Class"])
    target = frame["Class"].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        stratify=target,
        random_state=42,
    )
    preprocessor = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                list(features.columns),
            )
        ]
    )
    candidates = {
        "logistic_regression": LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        ),
        "decision_tree": DecisionTreeClassifier(
            class_weight="balanced", max_depth=12, random_state=42
        ),
    }
    results: dict[str, Any] = {}
    for name, classifier in candidates.items():
        pipeline = Pipeline(
            [("preprocessor", preprocessor), ("classifier", classifier)]
        )
        pipeline.fit(x_train, y_train)
        probabilities = pipeline.predict_proba(x_test)[:, 1]
        predictions = (probabilities >= 0.5).astype(int)
        results[name] = {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "precision": round(
                float(precision_score(y_test, predictions, zero_division=0)), 4
            ),
            "recall": round(
                float(recall_score(y_test, predictions, zero_division=0)), 4
            ),
            "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        }
    return results
