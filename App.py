import streamlit as st
import numpy as np
import pandas as pd
import shap
import joblib
from flask import Flask, request,


st.write("ok tout continu de marcher")

@app.route('/predict', methods=["POST"])
def prediction():
    data = request.get_json()
    prediction_value = np.array2string(model.predict_proba(data)[0, 1])

    return jsonify(prediction_value)

