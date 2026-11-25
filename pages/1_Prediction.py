"""
Prediction page: predicts yarn Tenacity from cotton fiber properties
UHML, UI, Mic, Str, E, Count.

Uses rkm_model_lite.joblib (plain scikit-learn + lightgbm objects extracted
from the original Azure AutoML model, see convert_model.py) so the app has
no azureml dependency and is light enough for Streamlit Community Cloud.
"""
import io

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from common import APP_TITLE, render_footer, render_header

FEATURE_COLUMNS = ["UHML", "UI", "Mic", "Str", "E", "Count"]
MODEL_PATH = "rkm_model_lite.joblib"

st.set_page_config(page_title=f"Prediction | {APP_TITLE}", page_icon="static/images/icar_1.png", layout="wide")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def predict(df: pd.DataFrame) -> np.ndarray:
    model = load_model()
    means = model["impute_means"]
    X = df[model["feature_columns"]].fillna(value=means).to_numpy(dtype=float)

    preds, weights = [], []
    for member in model["members"]:
        Xs = member["scaler"].transform(X)
        preds.append(member["regressor"].predict(Xs))
        weights.append(member["weight"])

    return np.average(np.array(preds), axis=0, weights=weights)


render_header()

tab_single, tab_csv = st.tabs(["Single Entry", "File Upload"])

with tab_single:
    with st.form("single_entry_form"):
        c1, c2 = st.columns(2)
        with c1:
            uhml = st.number_input("UHML", value=0.0, format="%.4f")
            mic = st.number_input("Mic", value=0.0, format="%.4f")
            e = st.number_input("E", value=0.0, format="%.4f")
        with c2:
            ui = st.number_input("UI", value=0.0, format="%.4f")
            strength = st.number_input("Str", value=0.0, format="%.4f")
            count = st.number_input("Count", value=0.0, format="%.4f")
        submitted = st.form_submit_button("Submit")

    if submitted:
        row = pd.DataFrame(
            [[uhml, ui, mic, strength, e, count]], columns=FEATURE_COLUMNS
        )
        tenacity = predict(row)[0]
        row["Tenacity"] = tenacity
        st.success(f"Predicted Tenacity: {tenacity:.4f}")
        st.dataframe(row, hide_index=True)

with tab_csv:
    st.caption("CSV must have columns: " + ", ".join(FEATURE_COLUMNS))
    with open("static/example_input/sample.csv", "rb") as f:
        st.download_button("Download sample CSV", f, file_name="sample.csv")

    uploaded = st.file_uploader("Upload CSV File", type="csv")
    if uploaded is not None:
        try:
            data = pd.read_csv(uploaded)
            result = predict(data)
            data["Tenacity"] = result
            st.subheader("Result")
            st.dataframe(data, hide_index=True)

            buf = io.StringIO()
            data.to_csv(buf, index=False)
            st.download_button(
                "Download the Result",
                buf.getvalue(),
                file_name="output.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"Could not process this file: {exc}")

render_footer()
