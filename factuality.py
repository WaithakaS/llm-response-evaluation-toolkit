import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FactualityFinding:
    risk_level: str
    flag: str
    evidence: str

HIGH_CERTAINTY = re.compile(
    r"\b(always|never|definitely|certainly|100%|proves that|guaranteed)\b", re.I
)
CITATION_PATTERN = re.compile(r"\b(according to|study|research|report|source|data shows)\b", re.I)
NUMERIC_CLAIM = re.compile(r"\b\d+(?:\.\d+)?%?\b")

def screen_factuality(text: str, reference_text: Optional[str] = None) -> List[FactualityFinding]:
    """Lightweight risk screening. It does not establish whether a claim is true."""
    findings = []
    if not text:
        return findings

    if HIGH_CERTAINTY.search(text):
        findings.append(FactualityFinding(
            "medium", "high_certainty_language",
            "Absolute/certain language detected; verify supporting evidence."
        ))

    numeric_hits = NUMERIC_CLAIM.findall(text)
    if numeric_hits and not CITATION_PATTERN.search(text):
        findings.append(FactualityFinding(
            "medium", "specific_numeric_claim",
            "Specific numeric claim detected without an obvious evidence cue."
        ))

    if reference_text:
        # Conservative lexical contradiction screen: only flags strong negation mismatch.
        text_lower, ref_lower = text.lower(), reference_text.lower()
        if "not " in text_lower and "not " not in ref_lower:
            findings.append(FactualityFinding(
                "low", "possible_reference_mismatch",
                "Potential mismatch with supplied reference; human verification required."
            ))

    return findings

def summarise_factuality(findings: List[FactualityFinding]) -> str:
    levels = {f.risk_level for f in findings}
    if "high" in levels:
        return "HIGH"
    if "medium" in levels:
        return "MEDIUM"
    if "low" in levels:
        return "LOW"
    return "LOW"
