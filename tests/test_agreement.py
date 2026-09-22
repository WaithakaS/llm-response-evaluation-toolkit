from src.agreement import decision_agreement, mean_absolute_score_difference, cohen_kappa

def test_agreement():
    h = ["PASS", "REVIEW", "FAIL", "PASS"]
    l = ["PASS", "REVIEW", "FAIL", "FAIL"]
    assert decision_agreement(h, l) == 0.75
    assert cohen_kappa(h, l) >= 0

def test_score_difference():
    assert mean_absolute_score_difference([4,3,2], [5,3,1]) == 2/3
