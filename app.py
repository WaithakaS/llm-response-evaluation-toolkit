import io
import pandas as pd
import streamlit as st
import plotly.express as px

from src.evaluator import LLMEvaluator
from src.factuality import screen_factuality, summarise_factuality
from src.error_analysis import identify_errors, model_error_summary
from src.agreement import decision_agreement, mean_absolute_score_difference, cohen_kappa, comparison_table

st.set_page_config(page_title="LLM Response Evaluation Dashboard", page_icon="🧪", layout="wide")

st.title("🧪 LLM Response Evaluation Dashboard")
st.caption("Human-in-the-loop quality evaluation, factuality risk screening and evaluator agreement.")

@st.cache_data
def load_data(uploaded):
    if uploaded is None:
        return pd.read_csv("data/sample_responses.csv")
    return pd.read_csv(uploaded)

uploaded = st.sidebar.file_uploader("Upload evaluation CSV", type=["csv"])
df = load_data(uploaded)

evaluator = LLMEvaluator()
try:
    results = evaluator.evaluate_dataframe(df)
except Exception as exc:
    st.error(f"Could not evaluate dataset: {exc}")
    st.stop()

# Factuality screening
if "response_text" in df.columns:
    risks = df["response_text"].fillna("").apply(lambda x: summarise_factuality(screen_factuality(x)))
    results["factuality_risk"] = risks
else:
    results["factuality_risk"] = "NOT_SCREENED"

st.sidebar.header("Filters")
models = st.sidebar.multiselect("Models", sorted(results["model"].unique()), default=sorted(results["model"].unique()))
decisions = st.sidebar.multiselect("Decision", ["PASS", "REVIEW", "FAIL"], default=["PASS", "REVIEW", "FAIL"])
view = results[results.model.isin(models) & results.decision.isin(decisions)]

avg = view["overall_score"].mean() if not view.empty else 0
pass_rate = (view["decision"] == "PASS").mean() if not view.empty else 0
review_rate = (view["decision"] == "REVIEW").mean() if not view.empty else 0
fail_rate = (view["decision"] == "FAIL").mean() if not view.empty else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Average score", f"{avg:.2f}")
c2.metric("PASS rate", f"{pass_rate:.0%}")
c3.metric("REVIEW rate", f"{review_rate:.0%}")
c4.metric("FAIL rate", f"{fail_rate:.0%}")

st.subheader("Model comparison")
model_summary = view.groupby("model", as_index=False)["overall_score"].mean().sort_values("overall_score", ascending=False)
if not model_summary.empty:
    st.plotly_chart(px.bar(model_summary, x="model", y="overall_score", range_y=[1,5], title="Average weighted score"), use_container_width=True)

st.subheader("Decision distribution")
decision_counts = view["decision"].value_counts().rename_axis("decision").reset_index(name="count")
if not decision_counts.empty:
    st.plotly_chart(px.bar(decision_counts, x="decision", y="count", title="PASS / REVIEW / FAIL"), use_container_width=True)

criteria = ["accuracy", "relevance", "completeness", "clarity", "instruction_following", "safety"]
criterion_rows = []
for model, group in view.groupby("model"):
    for c in criteria:
        criterion_rows.append({"model": model, "criterion": c, "score": group[f"{c}_score"].mean()})
criterion_df = pd.DataFrame(criterion_rows)
if not criterion_df.empty:
    st.subheader("Criterion-level performance")
    st.plotly_chart(px.bar(criterion_df, x="criterion", y="score", color="model", barmode="group",
                            range_y=[1,5], title="Average criterion score"), use_container_width=True)

st.subheader("Factuality / hallucination risk screening")
if "factuality_risk" in view:
    risk_counts = view["factuality_risk"].value_counts().rename_axis("risk").reset_index(name="count")
    st.plotly_chart(px.pie(risk_counts, names="risk", values="count", title="Screened factuality risk"), use_container_width=True)
    st.info("Risk screening is heuristic. A flagged response is not automatically a hallucination.")

st.subheader("Error / failure analysis")
errors = identify_errors(view)
if errors.empty:
    st.success("No criterion scores at or below the default error threshold.")
else:
    st.dataframe(errors, use_container_width=True)
    summary = model_error_summary(view)
    st.plotly_chart(px.bar(summary, x="error_category", y="count", color="model", barmode="group",
                            title="Error categories by model"), use_container_width=True)

st.subheader("Human vs LLM evaluator comparison")
if {"human_decision", "llm_decision"}.issubset(view.columns):
    comp = view.dropna(subset=["human_decision", "llm_decision"])
    if not comp.empty:
        agreement = decision_agreement(comp.human_decision, comp.llm_decision)
        kappa = cohen_kappa(comp.human_decision, comp.llm_decision)
        mad = None
        if {"human_overall_score", "llm_overall_score"}.issubset(comp.columns):
            mad = mean_absolute_score_difference(comp.human_overall_score, comp.llm_overall_score)
        a, b, c = st.columns(3)
        a.metric("Decision agreement", f"{agreement:.1%}")
        b.metric("Cohen's κ", f"{kappa:.2f}")
        c.metric("Mean abs. score difference", "N/A" if mad is None else f"{mad:.2f}")
        st.dataframe(comparison_table(comp), use_container_width=True)
    else:
        st.info("No paired human/LLM annotations available.")
else:
    st.info("Add human_decision and llm_decision columns to activate evaluator comparison.")

st.subheader("Download results")
csv = view.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered CSV", csv, "llm_evaluation_results.csv", "text/csv")
