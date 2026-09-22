from typing import Dict, List
import pandas as pd

ERROR_MAP = {
    "accuracy_score": "Factuality / accuracy",
    "relevance_score": "Relevance",
    "completeness_score": "Completeness",
    "clarity_score": "Clarity",
    "instruction_following_score": "Instruction following",
    "safety_score": "Safety",
}

def identify_errors(df: pd.DataFrame, threshold=2) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        for col, label in ERROR_MAP.items():
            if col in row.index and pd.notna(row[col]) and float(row[col]) <= threshold:
                rows.append({
                    "response_id": row.get("response_id"),
                    "model": row.get("model"),
                    "error_category": label,
                    "score": row[col],
                    "decision": row.get("decision"),
                })
    return pd.DataFrame(rows)

def model_error_summary(df: pd.DataFrame) -> pd.DataFrame:
    errors = identify_errors(df)
    if errors.empty:
        return pd.DataFrame(columns=["model", "error_category", "count"])
    return (
        errors.groupby(["model", "error_category"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
