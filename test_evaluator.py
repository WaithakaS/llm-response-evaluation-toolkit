import pytest
from src.evaluator import LLMEvaluator

def scores(value=5):
    return {k: value for k in ["accuracy","relevance","completeness","clarity","instruction_following","safety"]}

def test_weighted_score():
    evaluator = LLMEvaluator()
    assert evaluator.calculate_overall_score(scores()) == 5.0

def test_invalid_score():
    evaluator = LLMEvaluator()
    bad = scores()
    bad["accuracy"] = 6
    with pytest.raises(ValueError):
        evaluator.calculate_overall_score(bad)

def test_missing_score():
    evaluator = LLMEvaluator()
    with pytest.raises(ValueError):
        evaluator.calculate_overall_score({"accuracy": 5})

def test_decisions():
    evaluator = LLMEvaluator()
    assert evaluator.decision_from_score(4.0) == "PASS"
    assert evaluator.decision_from_score(3.0) == "REVIEW"
    assert evaluator.decision_from_score(2.0) == "FAIL"

def test_blocking_issue():
    evaluator = LLMEvaluator()
    assert evaluator.decision_from_score(4.8, blocking_issue=True) == "FAIL"
