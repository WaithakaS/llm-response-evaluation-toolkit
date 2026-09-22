# Portfolio Notes

## Project

**LLM Response Evaluation Toolkit**

## Strong portfolio summary

Built an end-to-end LLM evaluation toolkit for systematic quality assurance of AI-generated responses. The project combines configurable rubric scoring, PASS/REVIEW/FAIL classification, factuality risk screening, optional LLM-as-a-Judge evaluation, human-vs-LLM agreement analysis, error taxonomy, inter-rater statistics and an interactive Streamlit dashboard.

## Skills demonstrated

Python • Pandas • Streamlit • Plotly • LLM evaluation • Data annotation • QA • Rubric design • Factuality screening • Hallucination analysis • Cohen's kappa • Error analysis • Statistical agreement • Test automation • Human-in-the-loop AI evaluation • GitHub documentation

## Interview talking points

- Why separate human labels from LLM-judge labels? To avoid treating an automated evaluator as ground truth.
- Why use REVIEW? To preserve uncertainty instead of forcing ambiguous cases into PASS or FAIL.
- Why is factuality screening heuristic? A true fact requires evidence; lexical signals alone cannot establish truth.
- Why measure inter-rater agreement? Consistency is a core quality metric for annotation operations.
- Why use both score and decision? Scores preserve nuance while labels support operational triage.
