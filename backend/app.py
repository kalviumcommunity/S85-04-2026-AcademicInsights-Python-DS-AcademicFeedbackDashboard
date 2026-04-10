import os
import re
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS


CORE_SCORE_FEATURES = (
    "teaching_score",
    "course_score",
    "exam_score",
    "lab_score",
    "library_score",
    "extra_score",
)


def load_artifact(artifact_path: str) -> Dict[str, Any]:
    """Load model artifact from disk."""
    if not os.path.exists(artifact_path):
        raise FileNotFoundError(f"Model artifact not found at: {artifact_path}")
    artifact = joblib.load(artifact_path)

    required_keys = {"model", "imputer", "feature_columns"}
    missing = required_keys.difference(artifact.keys())
    if missing:
        raise ValueError(f"Artifact missing required keys: {sorted(missing)}")

    return artifact


def get_model_name(artifact_obj: Dict[str, Any], model_obj) -> str:
    """Get model name from artifact metadata, or fallback to class name."""
    return artifact_obj.get("model_name") or model_obj.__class__.__name__


def detect_sentiment_features(columns) -> list:
    """Detect likely sentiment-derived features by name pattern."""
    pattern = re.compile(r"(sentiment|polarity|subjectivity|emotion|opinion|vader|compound|comment)", re.IGNORECASE)
    return [c for c in columns if pattern.search(c)]


def _normalize_importance(values: np.ndarray, feature_columns) -> Dict[str, float]:
    """Normalize importance values to sum to 1 when possible."""
    values = np.array(values, dtype=float).flatten()
    values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)
    values = np.abs(values)
    total = float(values.sum())
    if total > 0:
        values = values / total

    return {
        feature: round(float(val), 6)
        for feature, val in zip(feature_columns, values)
    }


def compute_feature_importance(model_obj, feature_columns, prepared_input: pd.DataFrame) -> Dict[str, float]:
    """
    Compute feature importance with dynamic fallback logic:
    1) feature_importances_
    2) coef_
    3) perturbation-based fallback
    """
    if hasattr(model_obj, "feature_importances_"):
        return _normalize_importance(model_obj.feature_importances_, feature_columns)

    if hasattr(model_obj, "coef_"):
        coef = np.array(model_obj.coef_, dtype=float)
        if coef.ndim > 1:
            coef = coef.mean(axis=0)
        return _normalize_importance(coef, feature_columns)

    # Fallback: perturbation-based relative importance
    base_pred = float(model_obj.predict(prepared_input)[0])
    deltas = []
    for feature in feature_columns:
        simulated = prepared_input.copy()
        simulated.loc[0, feature] = min(5.0, float(simulated.loc[0, feature]) + 1.0)
        new_pred = float(model_obj.predict(simulated)[0])
        deltas.append(abs(new_pred - base_pred))

    return _normalize_importance(np.array(deltas, dtype=float), feature_columns)


def get_top_feature_importance(
    model_obj,
    feature_columns,
    prepared_input: pd.DataFrame,
    top_n: int = 5,
):
    """Return top-N normalized importances sorted desc, plus most/least important features."""
    full = compute_feature_importance(model_obj, feature_columns, prepared_input)
    sorted_items = sorted(full.items(), key=lambda kv: kv[1], reverse=True)
    top_items = sorted_items[:top_n]

    top_total = float(sum(v for _, v in top_items))
    if top_total > 0:
        top_features = {k: round(float(v / top_total), 6) for k, v in top_items}
    else:
        top_features = {k: round(float(v), 6) for k, v in top_items}

    most_important = sorted_items[0][0] if sorted_items else ""
    least_important = sorted_items[-1][0] if sorted_items else ""
    return top_features, most_important, least_important


def compute_impact_analysis_to_max(model_obj, prepared_input: pd.DataFrame, selected_features) -> Dict[str, float]:
    """For selected features, simulate current->1.0 and return sorted prediction deltas."""
    base_pred = float(model_obj.predict(prepared_input)[0])
    impact = {}

    for feature in selected_features:
        simulated = prepared_input.copy()
        simulated.loc[0, feature] = 1.0
        new_pred = float(model_obj.predict(simulated)[0])
        impact[feature] = round(float(new_pred - base_pred), 6)

    sorted_impact = dict(sorted(impact.items(), key=lambda kv: kv[1], reverse=True))
    return sorted_impact


def compute_average_comparison(
    prepared_input: pd.DataFrame,
    predicted_score: float,
    score_features,
) -> Dict[str, float]:
    """Compare prediction vs average of core score features only, on 0-1 scale."""
    available = [f for f in score_features if f in prepared_input.columns]
    if not available:
        raise ValueError("No core score features are available for average calculation.")

    score_vals = prepared_input.loc[0, available].astype(float).clip(lower=0.0, upper=1.0)
    average_score = float(score_vals.mean())
    return {
        "average_score": round(average_score, 6),
        "model_prediction": round(float(predicted_score), 6),
        "difference_from_average": round(float(predicted_score - average_score), 6),
    }


def compute_non_linear_test(model_obj, prepared_input: pd.DataFrame, feature_name: str) -> Dict[str, Any]:
    """Move the key feature from 0->1 and show prediction delta."""
    if not feature_name:
        return {"feature": "", "min_prediction": 0.0, "max_prediction": 0.0, "delta": 0.0}

    x_min = prepared_input.copy()
    x_max = prepared_input.copy()
    x_min.loc[0, feature_name] = 0.0
    x_max.loc[0, feature_name] = 1.0

    min_prediction = float(model_obj.predict(x_min)[0])
    max_prediction = float(model_obj.predict(x_max)[0])

    return {
        "feature": feature_name,
        "min_prediction": round(min_prediction, 6),
        "max_prediction": round(max_prediction, 6),
        "delta": round(max_prediction - min_prediction, 6),
    }


def compute_sentiment_impact(model_obj, prepared_input: pd.DataFrame, sentiment_features) -> float:
    """Prediction delta with sentiment present vs sentiment set to 0."""
    if not sentiment_features:
        return 0.0

    with_sentiment = float(model_obj.predict(prepared_input)[0])
    without_sentiment_df = prepared_input.copy()
    for f in sentiment_features:
        if f in without_sentiment_df.columns:
            without_sentiment_df.loc[0, f] = 0.0
    without_sentiment = float(model_obj.predict(without_sentiment_df)[0])

    return round(with_sentiment - without_sentiment, 4)


def compute_core_impact_analysis(
    model_obj,
    prepared_input: pd.DataFrame,
    core_score_features,
    base_prediction: float,
) -> Dict[str, float]:
    """Simulate each core score at max (1.0) from processed input and return deltas."""
    impacts = {}
    available = [f for f in core_score_features if f in prepared_input.columns]

    for col in available:
        temp = prepared_input.copy()
        temp.loc[0, col] = 1.0
        new_pred = float(model_obj.predict(temp)[0])
        impacts[col] = round(new_pred - float(base_prediction), 4)

    return dict(sorted(impacts.items(), key=lambda x: x[1], reverse=True))


def _scale_likert_like_columns(input_df: pd.DataFrame, assume_one_to_five: bool = False) -> pd.DataFrame:
    """Scale score/rating columns from 0-5 to 0-1 when needed."""
    scaled = input_df.copy().astype(float)
    likert_pattern = re.compile(r"(score|rating)", re.IGNORECASE)
    likert_cols = [c for c in scaled.columns if likert_pattern.search(c)]

    if not likert_cols:
        return scaled

    likert_values = pd.to_numeric(scaled.loc[0, likert_cols], errors="coerce").dropna()
    infer_one_to_five_scale = assume_one_to_five or (
        len(likert_values) > 0
        and bool((likert_values >= 1.0).all())
        and bool((likert_values <= 5.0).all())
        and float(likert_values.max()) > 1.0
    )

    for col in likert_cols:
        val = scaled.loc[0, col]
        if pd.isna(val):
            continue
        val = float(val)
        if infer_one_to_five_scale and 1.0 <= val <= 5.0:
            scaled.loc[0, col] = val / 5.0
        elif 1.0 < val <= 5.0:
            scaled.loc[0, col] = val / 5.0

    return scaled


def validate_and_prepare_input(payload: Dict[str, Any], feature_columns, imputer) -> pd.DataFrame:
    """Validate input, scale score-like columns, and prepare model-ready dataframe."""
    required_core = [f for f in CORE_SCORE_FEATURES if f in feature_columns]
    missing_fields = [f for f in required_core if f not in payload]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    filtered_payload = {feature: payload.get(feature, np.nan) for feature in feature_columns}
    input_df = pd.DataFrame([filtered_payload], columns=feature_columns)
    input_df = input_df.apply(pd.to_numeric, errors="coerce")

    provided_fields = [f for f in feature_columns if f in payload]
    invalid_numeric = [f for f in provided_fields if pd.isna(input_df.loc[0, f])]
    if invalid_numeric:
        raise ValueError(f"Invalid non-numeric values for fields: {invalid_numeric}")

    # Context-aware scale inference:
    # - If any provided score/rating is >1, payload is definitely 1-5.
    # - If request provides only *_score (no *_rating) and values are in [1,5],
    #   treat as raw 1-5 API input (covers all-ones low-score case).
    provided_score_like = [
        c for c in provided_fields
        if re.search(r"(score|rating)", c, flags=re.IGNORECASE)
    ]
    has_rating_fields = any(c.endswith("_rating") for c in provided_score_like)
    has_score_fields = any(c.endswith("_score") for c in provided_score_like)
    score_like_vals = pd.to_numeric(input_df.loc[0, provided_score_like], errors="coerce").dropna()

    any_gt_one = bool((score_like_vals > 1.0).any()) if len(score_like_vals) else False
    score_only_one_to_five = (
        has_score_fields
        and not has_rating_fields
        and len(score_like_vals) > 0
        and bool((score_like_vals >= 1.0).all())
        and bool((score_like_vals <= 5.0).all())
    )

    input_df = _scale_likert_like_columns(
        input_df,
        assume_one_to_five=(any_gt_one or score_only_one_to_five),
    )

    sentiment_cols = set(detect_sentiment_features(feature_columns))
    non_sentiment_cols = [c for c in provided_fields if c not in sentiment_cols]

    out_of_range_non_sent = [
        c for c in non_sentiment_cols
        if not (0.0 <= float(input_df.loc[0, c]) <= 1.0)
    ]
    if out_of_range_non_sent:
        raise ValueError(f"Non-sentiment fields must be within [0, 1]: {out_of_range_non_sent}")

    out_of_range_sentiment = [
        c for c in provided_fields
        if c in sentiment_cols and not (-1.0 <= float(input_df.loc[0, c]) <= 1.0)
    ]
    if out_of_range_sentiment:
        raise ValueError(f"Sentiment fields must be within [-1, 1]: {out_of_range_sentiment}")

    transformed = imputer.transform(input_df)
    prepared = pd.DataFrame(transformed, columns=feature_columns)
    return prepared


def build_scaled_input_payload(prepared_input: pd.DataFrame, feature_columns) -> Dict[str, float]:
    """Build a JSON-safe scaled payload for debug logging and observability."""
    return {
        col: float(prepared_input.loc[0, col])
        for col in feature_columns
    }


def build_prediction_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run prediction + explainability suite and return production JSON payload."""
    prepared_input = validate_and_prepare_input(payload, feature_columns, imputer)
    scaled_payload = build_scaled_input_payload(prepared_input, feature_columns)
    predicted_score = float(model.predict(prepared_input)[0])

    row = prepared_input.iloc[0]
    available_core = [f for f in CORE_SCORE_FEATURES if f in prepared_input.columns]
    average_score = float(row[available_core].mean())
    if not (0.0 <= average_score <= 1.0):
        raise ValueError(f"Average score out of range after scaling: {average_score}")

    print("Raw payload:", payload)
    print("Scaled input:", scaled_payload)
    print("Processed row:", row[available_core].to_dict())
    print("Average:", average_score)

    top_features, _, _ = get_top_feature_importance(
        model, feature_columns, prepared_input, top_n=5
    )
    top_feature = max(top_features, key=top_features.get) if top_features else ""

    core_series = row[available_core].astype(float) if available_core else pd.Series(dtype=float)
    area_to_improve = core_series.idxmin() if not core_series.empty else ""

    if not core_series.empty:
        contribution = {
            feat: float(top_features.get(feat, 0.0)) * float(core_series[feat])
            for feat in core_series.index
        }
        strength = max(contribution, key=contribution.get) if contribution else top_feature
    else:
        strength = top_feature

    sentiment_impact = compute_sentiment_impact(model, prepared_input, sentiment_features)
    impact_analysis = compute_core_impact_analysis(
        model,
        prepared_input,
        CORE_SCORE_FEATURES,
        predicted_score,
    )

    return {
        "predicted_score": round(predicted_score, 4),
        "average_score": round(average_score, 4),
        "difference_from_average": round(predicted_score - average_score, 4),
        "model_used": model_name,
        "top_features": top_features,
        "top_feature": top_feature,
        "most_important_feature": top_feature,
        "strength": strength,
        "area_to_improve": area_to_improve,
        "impact_analysis": impact_analysis,
        "sentiment_impact": sentiment_impact,
        "explanation": "Model uses non-linear relationships and unequal feature importance.",
    }


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ARTIFACT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "student_satisfaction_best_model.joblib")
)
ARTIFACT_PATH = os.getenv("MODEL_ARTIFACT_PATH", DEFAULT_ARTIFACT_PATH)

artifact = load_artifact(ARTIFACT_PATH)
model = artifact["model"]
imputer = artifact["imputer"]
feature_columns = artifact["feature_columns"]
model_name = get_model_name(artifact, model)
sentiment_features = artifact.get("sentiment_columns") or detect_sentiment_features(feature_columns)

app = Flask(__name__)
CORS(app)


@app.get("/")
def health_check():
    return "API is running", 200


@app.post("/predict")
def predict():
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Invalid JSON body."}), 400

        response = build_prediction_response(payload)
        return jsonify(response), 200

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Prediction failed: %s", exc)
        return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    print("Starting Flask server with auto-reload enabled...")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)
