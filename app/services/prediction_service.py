from datetime import datetime, timezone
import csv
import os

import pandas as pd

from app.core.model_loader import model


CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "cognitive_load_predictions.csv")
FALLBACK_CSV_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "cognitive_load_predictions_fallback.csv"
)

CSV_FIELDS = [
    "student_id",
    "lesson_id",
    "minute_index",
    "pause_frequency",
    "navigation_count_video",
    "rewatch_segments",
    "playback_rate_change",
    "idle_duration_video",
    "time_on_content",
    "navigation_count_adaptation",
    "revisit_frequency",
    "idle_duration_adaptation",
    "quiz_response_time",
    "error_rate",
    "predicted_cognitive_load",
    "predicted_score",
    "predicted_label",
    "confidence",
    "created_at",
]


def get_label(score: int):
    labels = {
        1: "Very Low",
        2: "Low",
        3: "Medium",
        4: "High",
        5: "Very High",
    }
    return labels.get(score, "Unknown")


def save_to_csv(row_data: dict):
    target_file = CSV_FILE

    try:
        _write_csv_row(target_file, row_data)
    except PermissionError:
        # If the main CSV is locked by another app such as Excel, keep the API alive
        # and persist the prediction to a fallback file instead of failing the request.
        target_file = FALLBACK_CSV_FILE
        _write_csv_row(target_file, row_data)


def _write_csv_row(file_path: str, row_data: dict):
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row_data)


def predict_cognitive_load(data):
    input_df = pd.DataFrame(
        [
            {
                "pause_frequency": data.pause_frequency,
                "navigation_count_video": data.navigation_count_video,
                "rewatch_segments": data.rewatch_segments,
                "playback_rate_change": data.playback_rate_change,
                "idle_duration_video": data.idle_duration_video,
                "time_on_content": data.time_on_content,
                "navigation_count_adaptation": data.navigation_count_adaptation,
                "revisit_frequency": data.revisit_frequency,
                "idle_duration_adaptation": data.idle_duration_adaptation,
                "quiz_response_time": data.quiz_response_time,
                "error_rate": data.error_rate,
            }
        ]
    )

    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    confidence = max(proba)
    label = get_label(int(prediction))

    response_data = {
        "student_id": data.student_id,
        "lesson_id": data.lesson_id,
        "minute_index": data.minute_index,
        "pause_frequency": data.pause_frequency,
        "navigation_count_video": data.navigation_count_video,
        "rewatch_segments": data.rewatch_segments,
        "playback_rate_change": data.playback_rate_change,
        "idle_duration_video": data.idle_duration_video,
        "time_on_content": data.time_on_content,
        "navigation_count_adaptation": data.navigation_count_adaptation,
        "revisit_frequency": data.revisit_frequency,
        "idle_duration_adaptation": data.idle_duration_adaptation,
        "quiz_response_time": data.quiz_response_time,
        "error_rate": data.error_rate,
        "predicted_cognitive_load": label,
        "predicted_score": int(prediction),
        "predicted_label": label,
        "confidence": round(float(confidence), 2),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    save_to_csv(response_data)
    return response_data
