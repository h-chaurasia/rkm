"""
One-off conversion script: rkm_model.pkl (an Azure AutoML RegressionPipeline)
-> rkm_model_lite.joblib (plain scikit-learn / lightgbm objects only).

The original pickle only unpickles inside the exact azureml-automl-runtime==1.58
environment (huge, Azure-specific, not viable on Streamlit Community Cloud).
Underneath, every ensemble member is a plain sklearn scaler + a plain
sklearn/lightgbm regressor (azureml's StandardScalerWrapper/LightGBMRegressor
just hold one in a `.model` attribute). This script pulls those plain objects
out so the app never has to import azureml again.

Run once, inside the azureml environment, whenever rkm_model.pkl changes:
    source <azureml-venv>/bin/activate
    LD_LIBRARY_PATH=<path-to-bundled-libgomp> python convert_model.py
"""
import pickle
import joblib

FEATURE_COLUMNS = ["UHML", "UI", "Mic", "Str", "E", "Count"]

with open("rkm_model.pkl", "rb") as f:
    model = pickle.load(f, encoding="latin1")

data_transformer = model.steps[0][1]
means = {}
for tm in data_transformer.transformer_and_mapper_list:
    col = tm.mapper.features[0][0][0]
    means[col] = float(tm.transformers[0].statistics_[0])

ensemble = model.steps[1][1]._wrappedEnsemble
members = []
for (name, pipeline), weight in zip(ensemble.estimators, ensemble.weights):
    scaler = pipeline.steps[0][1]
    regressor = pipeline.steps[-1][1]
    # Unwrap azureml's thin wrapper classes down to the plain object they hold.
    scaler = getattr(scaler, "model", scaler)
    regressor = getattr(regressor, "model", regressor)
    members.append({"name": name, "weight": weight, "scaler": scaler, "regressor": regressor})

lite_model = {
    "feature_columns": FEATURE_COLUMNS,
    "impute_means": means,
    "members": members,
}

joblib.dump(lite_model, "rkm_model_lite.joblib")
print("Wrote rkm_model_lite.joblib with", len(members), "ensemble members.")
