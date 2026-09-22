from pathlib import Path
import pandas as pd
from src.evaluator import LLMEvaluator

BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data" / "sample_responses.csv")
results = LLMEvaluator().evaluate_dataframe(df)

print("\nLLM RESPONSE EVALUATION RESULTS")
print("=" * 80)
print(results[["response_id", "model", "overall_score", "decision"]].to_string(index=False))

results.to_csv(BASE / "evaluation_results.csv", index=False)
results.to_json(BASE / "evaluation_results.json", orient="records", indent=2)
print("\nSaved evaluation_results.csv and evaluation_results.json")
