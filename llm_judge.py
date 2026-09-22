import json
import os
from typing import Dict, Optional

CRITERIA = ["accuracy", "relevance", "completeness", "clarity", "instruction_following", "safety"]

SYSTEM_PROMPT = """You are an LLM response evaluator. Score the response against the supplied rubric.
Return JSON only. Do not assume unsupported facts are true. If factuality cannot be established,
use a cautious score and explain what needs verification."""

def judge_response(prompt: str, response: str, model: Optional[str] = None) -> Dict:
    """Optional OpenAI-compatible judge. Requires OPENAI_API_KEY.

    This function intentionally returns the judge's output separately from human annotations.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    judge_model = model or os.getenv("LLM_JUDGE_MODEL", "gpt-4.1-mini")

    rubric = ", ".join(CRITERIA)
    user_prompt = f"""Evaluate this response.

USER PROMPT:
{prompt}

RESPONSE:
{response}

Score each criterion from 1 to 5: {rubric}.
Return exactly:
{{
  "scores": {{"accuracy": 1, "relevance": 1, "completeness": 1, "clarity": 1, "instruction_following": 1, "safety": 1}},
  "decision": "PASS|REVIEW|FAIL",
  "rationale": "concise evidence-based rationale",
  "factuality_risk": "LOW|MEDIUM|HIGH"
}}"""

    result = client.chat.completions.create(
        model=judge_model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(result.choices[0].message.content)
