from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
from .rubric import DEFAULT_RUBRIC

@dataclass
class CriterionScore:
    criterion: str
    score: int
    rationale: str = ""

@dataclass
class EvaluationResult:
    response_id: str
    model: str
    overall_score: float
    decision: str
    criterion_scores: List[CriterionScore]

    def to_flat_dict(self):
        row = {
            "response_id": self.response_id,
            "model": self.model,
            "overall_score": self.overall_score,
            "decision": self.decision,
        }
        for item in self.criterion_scores:
            row[f"{item.criterion}_score"] = item.score
            row[f"{item.criterion}_rationale"] = item.rationale
        return row

class LLMEvaluator:
    def __init__(self, rubric=None, pass_threshold=3.5, fail_threshold=2.5):
        self.rubric = rubric or DEFAULT_RUBRIC
        self.pass_threshold = pass_threshold
        self.fail_threshold = fail_threshold

    @staticmethod
    def validate_score(score):
        if not isinstance(score, int) or not 1 <= score <= 5:
            raise ValueError("Each score must be an integer from 1 to 5.")

    def calculate_overall_score(self, scores: Dict[str, int]) -> float:
        weighted_total = 0
        total_weight = 0
        for criterion in self.rubric:
            if criterion.name not in scores:
                raise ValueError(f"Missing score for: {criterion.name}")
            score = scores[criterion.name]
            self.validate_score(score)
            weighted_total += score * criterion.weight
            total_weight += criterion.weight
        return round(weighted_total / total_weight, 2)

    def decision_from_score(self, overall, blocking_issue=False):
        if blocking_issue or overall < self.fail_threshold:
            return "FAIL"
        if overall >= self.pass_threshold:
            return "PASS"
        return "REVIEW"

    def evaluate(self, response_id, model, scores, rationales=None, blocking_issue=False):
        rationales = rationales or {}
        overall = self.calculate_overall_score(scores)
        decision = self.decision_from_score(overall, blocking_issue)
        criterion_scores = [
            CriterionScore(c.name, scores[c.name], str(rationales.get(c.name, "")).strip())
            for c in self.rubric
        ]
        return EvaluationResult(response_id, model, overall, decision, criterion_scores)

    def evaluate_dataframe(self, df):
        output = []
        for _, row in df.iterrows():
            scores = {c.name: int(row[f"{c.name}_score"]) for c in self.rubric}
            rationales = {c.name: row.get(f"{c.name}_rationale", "") for c in self.rubric}
            output.append(
                self.evaluate(str(row["response_id"]), str(row["model"]), scores, rationales).to_flat_dict()
            )
        return pd.DataFrame(output)

    @staticmethod
    def identify_weak_criteria(result, threshold=2):
        return [x.criterion for x in result.criterion_scores if x.score <= threshold]
