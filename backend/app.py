import os
import re
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS


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


def compute_average_comparison(prepared_input: pd.DataFrame, predicted_score: float) -> Dict[str, float]:
    """Compare model prediction vs simple average using same model-ready feature vector."""
    average_score = float(prepared_input.iloc[0].mean())
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

    return round(with_sentiment - without_sentiment, 6)


def derive_insights(impact_analysis: Dict[str, float], top_features: Dict[str, float]) -> Dict[str, str]:
    """Create human-friendly strength and improvement guidance."""
    strength = next(iter(impact_analysis), "")
    improvement = min(impact_analysis, key=impact_analysis.get) if impact_analysis else ""
    if not strength and top_features:
        strength = next(iter(top_features))

    insights = []
    if strength:
        insights.append(f"Strongest feature pushing scores up is {strength.replace('_', ' ')}.")
    if improvement:
        insights.append(f"Biggest area for potential improvement is {improvement.replace('_', ' ')}.")
    insights.append("Model uses non-linear ensemble learning and unequal feature importance, not averaging.")

    return insights


def validate_and_prepare_input(payload: Dict[str, Any], feature_columns, imputer) -> pd.DataFrame:
    """Validate required inputs are numeric and in [0,1], then transform using trained imputer."""
    missing_fields = [f for f in feature_columns if f not in payload]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    filtered_payload = {feature: payload[feature] for feature in feature_columns}
    input_df = pd.DataFrame([filtered_payload]).reindex(columns=feature_columns)
    input_df = input_df.apply(pd.to_numeric, errors="coerce")

    invalid_numeric = input_df.columns[input_df.isna().iloc[0]].tolist()
    if invalid_numeric:
        raise ValueError(f"Invalid non-numeric values for fields: {invalid_numeric}")

    out_of_range = [
        c for c in feature_columns
        if not (0.0 <= float(input_df.loc[0, c]) <= 1.0)
    ]
    if out_of_range:
        raise ValueError(f"Fields must be within [0, 1]: {out_of_range}")

    transformed = imputer.transform(input_df)
    prepared = pd.DataFrame(transformed, columns=feature_columns)

    # Keep prepared values mathematically consistent for average comparison and downstream explainability.
    prepared = prepared.clip(lower=0.0, upper=1.0)
    return prepared


def build_prediction_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run prediction + explainability suite and return production JSON payload."""
    prepared_input = validate_and_prepare_input(payload, feature_columns, imputer)
    predicted_score = float(model.predict(prepared_input)[0])

    avg_cmp = compute_average_comparison(prepared_input, predicted_score)
    top_features, most_important, least_important = get_top_feature_importance(
        model, feature_columns, prepared_input, top_n=5
    )

    top_feature_names = list(top_features.keys())
    impact_analysis = compute_impact_analysis_to_max(model, prepared_input, top_feature_names)
    non_linear_test = compute_non_linear_test(model, prepared_input, most_important)
    sentiment_impact = compute_sentiment_impact(model, prepared_input, sentiment_features)
    insights = derive_insights(impact_analysis, top_features)

    return {
        "predicted_score": round(predicted_score, 4),
        "average_score": avg_cmp["average_score"],
        "difference_from_average": avg_cmp["difference_from_average"],
        "model_used": model_name,
        "top_features": top_features,
        "most_important_feature": most_important,
        "least_important_feature": least_important,
        "impact_analysis": impact_analysis,
        "non_linear_test": non_linear_test,
        "sentiment_impact": {
            "difference": sentiment_impact,
            "sentiment_score": payload.get('Sentiment_Score', 0)
        } if sentiment_impact != 0.0 else None,
        "insights": insights,
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
sentiment_features = detect_sentiment_features(feature_columns)

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
    app.run(host="127.0.0.1", port=5000, debug=True)
