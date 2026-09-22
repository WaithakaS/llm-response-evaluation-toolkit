from src.factuality import screen_factuality, summarise_factuality

def test_certainty_flag():
    findings = screen_factuality("This is definitely correct.")
    assert any(x.flag == "high_certainty_language" for x in findings)

def test_numeric_claim_without_evidence():
    findings = screen_factuality("The study shows 100% improvement.")
    assert any(x.flag == "specific_numeric_claim" for x in findings)

def test_low_risk_empty():
    assert summarise_factuality([]) == "LOW"
