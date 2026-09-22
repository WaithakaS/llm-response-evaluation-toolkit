# LLM Response Evaluation Toolkit

A portfolio-ready evaluation framework for systematically testing, scoring, comparing, and diagnosing LLM responses.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Evaluation](https://img.shields.io/badge/LLM%20evaluation-human%20%2B%20LLM-purple)

## Project overview

This toolkit turns LLM response evaluation into a repeatable QA workflow rather than a simple 1–5 scoring exercise.

It supports:

- configurable rubric-based human evaluation
- `PASS`, `REVIEW`, and `FAIL` labels
- weighted evaluation metrics
- Streamlit dashboard and visual analytics
- optional LLM-as-a-Judge evaluation
- hallucination/factuality risk checks
- human-vs-LLM evaluator comparison
- Cohen's kappa and agreement analysis
- annotation guidelines and calibration examples
- structured error/failure analysis
- model-level and criterion-level comparisons
- CSV/JSON reporting
- automated tests

> **Important:** Automated judges and heuristic factuality checks are decision-support tools, not ground truth. High-impact factual or safety claims should be verified by qualified human reviewers against appropriate evidence.

## Architecture

```text
                         ┌──────────────────────┐
                         │  Test Cases / CSV     │
                         └──────────┬───────────┘
                                    │
                           ┌────────▼────────┐
                           │ Evaluation       │
                           │ Rubric Engine    │
                           └───────┬──────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
        ┌───────▼──────┐  ┌────────▼────────┐  ┌──────▼─────────┐
        │ Human Scores │  │ LLM-as-a-Judge  │  │ Factuality /   │
        │ + Rationale  │  │ (optional)      │  │ Hallucination  │
        └───────┬──────┘  └────────┬────────┘  └──────┬─────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌────────────────────┐
                         │ Metrics + Error    │
                         │ / Agreement Layer  │
                         └─────────┬──────────┘
                                   ▼
                         ┌────────────────────┐
                         │ Streamlit Dashboard│
                         └────────────────────┘
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python evaluate.py
pytest -q
streamlit run app.py
```

Windows:

```powershell
.venv\Scripts\activate
```

## Dashboard

The Streamlit dashboard provides:

1. dataset upload
2. KPI cards for average score, pass/review/fail rates and factuality risk
3. model comparison
4. criterion-level charts
5. evaluation label distribution
6. hallucination/factuality risk distribution
7. human-vs-LLM agreement analysis
8. failure and error analysis
9. downloadable evaluation results

### Screenshots

![Dashboard overview](screenshots/dashboard_overview.png)

![Error analysis](screenshots/error_analysis.png)

## Evaluation rubric

Each criterion is scored from 1–5:

| Criterion | What it measures |
|---|---|
| Accuracy | Factual correctness and support |
| Relevance | Directness and usefulness |
| Completeness | Coverage of required content |
| Clarity | Organisation and readability |
| Instruction following | Compliance with explicit constraints |
| Safety | Avoidance of harmful or unsafe output |

Weights are configurable in `src/rubric.py`.

### Decision labels

- **PASS** — meets the configured quality threshold and has no blocking issue.
- **REVIEW** — borderline, ambiguous, or requires human verification.
- **FAIL** — below the minimum threshold or contains a blocking error.

The thresholds are configurable and should be calibrated to the use case.

## Hallucination and factuality checks

`src/factuality.py` provides a lightweight risk-screening layer that looks for:

- unsupported certainty language
- unverifiable factual-style claims
- missing evidence for claims marked as requiring support
- contradiction indicators
- high-risk factuality flags

This is deliberately described as **risk screening**, not proof of hallucination. For evidence-backed verification, supply reference facts or documents and perform human review.

## Optional LLM-as-a-Judge

`src/llm_judge.py` contains an optional OpenAI-compatible judge adapter.

Set an API key in your environment:

```bash
export OPENAI_API_KEY="your-key"
```

Then use the judge from Python or enable it in the dashboard.

The judge returns structured criterion scores, rationales and a decision. The project keeps LLM judging separate from human labels so agreement can be measured instead of silently treating the model as ground truth.

## Human-vs-LLM evaluator comparison

The toolkit compares evaluator outputs using:

- exact decision agreement
- criterion-level agreement
- mean absolute score difference
- Cohen's kappa for categorical labels
- confusion matrix
- disagreement examples

See `src/agreement.py`.

## Annotation guidelines

See `ANNOTATION_GUIDELINES.md` for:

- scoring anchors
- evidence requirements
- PASS/REVIEW/FAIL rules
- factuality handling
- safety escalation
- tie/borderline handling
- calibration procedure
- examples of common annotation errors

## Test suite

The test suite covers:

- weighted scoring
- invalid/missing scores
- decision labels
- weak-criterion detection
- factuality risk checks
- agreement metrics
- error categorisation

Run:

```bash
pytest -q
```

## Portfolio value

This project demonstrates practical AI evaluation skills:

- evaluation rubric design
- data annotation and quality assurance
- LLM output assessment
- structured error analysis
- factuality/hallucination screening
- statistical agreement analysis
- Python and Pandas
- Streamlit analytics
- test-driven development
- human-in-the-loop evaluation design
- reproducible reporting

## Suggested portfolio description

> Built a production-style LLM response evaluation toolkit combining human annotation, optional LLM-as-a-Judge scoring, factuality risk screening, inter-rater agreement analysis and interactive Streamlit analytics. Designed configurable rubrics, PASS/REVIEW/FAIL decisioning, comprehensive test cases and failure-analysis workflows to assess response quality consistently across models.

## Limitations

This is an evaluation framework, not an autonomous truth engine. Factuality heuristics can produce false positives and false negatives, and LLM judges can exhibit bias or evaluator drift. Human review remains essential for ambiguous, high-risk, or evidence-sensitive cases.
## Author

**Samwel Isaboke**  
AI Trainer | Data Analyst  
GitHub: [@WaithakaS](https://github.com/WaithakaS)  
LinkedIn: [Samwel Isaboke](https://www.linkedin.com/in/samwel-isaboke-1592a58a/)  
Email: [samwelwaithakaisaboke@gmail.com](mailto:samwelwaithakaisaboke@gmail.com)
