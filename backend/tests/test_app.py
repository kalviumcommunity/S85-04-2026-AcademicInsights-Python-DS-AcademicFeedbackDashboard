import sys
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import app as backend_app  # noqa: E402


# ---------------------------
# 🔧 DUMMY SETUP
# ---------------------------

class DummyImputer:
    def __init__(self, feature_columns):
        self.feature_columns = feature_columns

    def transform(self, input_df: pd.DataFrame):
        return input_df[self.feature_columns].fillna(0.0).to_numpy()


class DummyModel:
    def __init__(self, feature_columns, sentiment_columns):
        self.feature_columns = feature_columns
        self.sentiment_columns = sentiment_columns

        self.feature_importances_ = np.array([0.30, 0.24, 0.18, 0.12, 0.10, 0.06, 0.01, 0.01])

    def predict(self, X: pd.DataFrame):
        core = list(backend_app.CORE_SCORE_FEATURES)
        core_mean = float(X.loc[:, core].mean(axis=1).iloc[0])
        sent_sum = float(X.loc[:, self.sentiment_columns].sum(axis=1).iloc[0])

        pred = 0.75 * core_mean + 0.05 * sent_sum + 0.1
        return np.array([float(np.clip(pred, 0.0, 1.0))])


def setup_backend():
    feature_columns = [
        "teaching_score",
        "course_score",
        "exam_score",
        "lab_score",
        "library_score",
        "extra_score",
        "teaching_comment_sentiment",
        "course_comment_sentiment",
    ]

    sentiment_columns = ["teaching_comment_sentiment", "course_comment_sentiment"]

    backend_app.feature_columns = feature_columns
    backend_app.sentiment_features = sentiment_columns
    backend_app.imputer = DummyImputer(feature_columns)
    backend_app.model = DummyModel(feature_columns, sentiment_columns)
    backend_app.model_name = "Gradient Boosting"


# ---------------------------
# 🧪 TEST CASES (0–5 SCALE ONLY)
# ---------------------------

# 1. ALL LOW
def test_all_low_scores():
    setup_backend()

    payload = {
        "teaching_score": 0,
        "course_score": 0,
        "exam_score": 0,
        "lab_score": 0,
        "library_score": 0,
        "extra_score": 0,
    }

    res = backend_app.build_prediction_response(payload)

    assert res["predicted_score"] < 0.5


# 2. ALL HIGH
def test_all_high_scores():
    setup_backend()

    payload = {
        "teaching_score": 5,
        "course_score": 5,
        "exam_score": 5,
        "lab_score": 5,
        "library_score": 5,
        "extra_score": 5,
    }

    res = backend_app.build_prediction_response(payload)

    assert res["predicted_score"] > 0.8


# 3. LOW IMPORTANT FEATURE (LAB)
def test_low_lab_is_detected():
    setup_backend()

    payload = {
        "teaching_score": 5,
        "course_score": 5,
        "exam_score": 5,
        "lab_score": 0,  # LOW
        "library_score": 5,
        "extra_score": 5,
    }

    res = backend_app.build_prediction_response(payload)

    assert res["area_to_improve"] == "lab_score"
    assert res["strength"] != "lab_score"


# 4. LOW TEACHING
def test_low_teaching_detected():
    setup_backend()

    payload = {
        "teaching_score": 0,
        "course_score": 5,
        "exam_score": 5,
        "lab_score": 5,
        "library_score": 5,
        "extra_score": 5,
    }

    res = backend_app.build_prediction_response(payload)

    assert res["area_to_improve"] == "teaching_score"


# 5. MIXED REALISTIC CASE
def test_realistic_mix():
    setup_backend()

    payload = {
        "teaching_score": 3,
        "course_score": 2,
        "exam_score": 5,
        "lab_score": 1,
        "library_score": 4,
        "extra_score": 3,
    }

    res = backend_app.build_prediction_response(payload)

    assert 0.4 < res["predicted_score"] < 0.8


# 6. SENTIMENT IMPACT
def test_sentiment_effect():
    setup_backend()

    base = {
        "teaching_score": 4,
        "course_score": 4,
        "exam_score": 4,
        "lab_score": 4,
        "library_score": 4,
        "extra_score": 4,
    }

    positive = base | {
        "teaching_comment_sentiment": 1,
        "course_comment_sentiment": 1,
    }

    negative = base | {
        "teaching_comment_sentiment": 0,
        "course_comment_sentiment": 0,
    }

    res_pos = backend_app.build_prediction_response(positive)
    res_neg = backend_app.build_prediction_response(negative)

    assert res_pos["predicted_score"] > res_neg["predicted_score"]


# 7. DYNAMIC CHANGE TEST
def test_prediction_changes():
    setup_backend()

    payload1 = {
        "teaching_score": 5,
        "course_score": 5,
        "exam_score": 5,
        "lab_score": 5,
        "library_score": 5,
        "extra_score": 5,
    }

    payload2 = payload1.copy()
    payload2["lab_score"] = 0

    res1 = backend_app.build_prediction_response(payload1)
    res2 = backend_app.build_prediction_response(payload2)

    assert res1["predicted_score"] != res2["predicted_score"]
    assert res1["area_to_improve"] != res2["area_to_improve"]


# ---------------------------
# 🚀 RUN TESTS
# ---------------------------

if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", __file__, "-q"]))