from typing import Iterable, Tuple
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

def decision_agreement(human: Iterable[str], llm: Iterable[str]) -> float:
    h, l = list(human), list(llm)
    if not h or len(h) != len(l):
        raise ValueError("Evaluator arrays must be non-empty and equal length.")
    return sum(a == b for a, b in zip(h, l)) / len(h)

def mean_absolute_score_difference(human, llm) -> float:
    h, l = list(human), list(llm)
    if len(h) != len(l) or not h:
        raise ValueError("Evaluator arrays must be non-empty and equal length.")
    return sum(abs(a-b) for a, b in zip(h, l)) / len(h)

def cohen_kappa(human, llm) -> float:
    h, l = list(human), list(llm)
    if len(h) != len(l) or not h:
        raise ValueError("Evaluator arrays must be non-empty and equal length.")
    return float(cohen_kappa_score(h, l))

def comparison_table(df: pd.DataFrame, human_col="human_decision", llm_col="llm_decision"):
    subset = df[[human_col, llm_col]].dropna()
    if subset.empty:
        return pd.DataFrame()
    return pd.crosstab(subset[human_col], subset[llm_col], rownames=["Human"], colnames=["LLM"])

def criterion_agreement(df, criterion, human_suffix="_human", llm_suffix="_llm"):
    hcol, lcol = f"{criterion}{human_suffix}", f"{criterion}{llm_suffix}"
    subset = df[[hcol, lcol]].dropna()
    if subset.empty:
        return None
    return {
        "exact_agreement": float((subset[hcol] == subset[lcol]).mean()),
        "mean_absolute_difference": float((subset[hcol] - subset[lcol]).abs().mean()),
        "kappa": float(cohen_kappa_score(subset[hcol], subset[lcol])),
    }
