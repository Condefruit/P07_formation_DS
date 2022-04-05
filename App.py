import streamlit as st
import numpy as np
import pandas as pd
import shap
import pickle5 as pickle
from flask import Flask, request, jsonify
from lightgbm import LGBMClassifier

# Crée l’objet application Flask, qui contient les données de l’application et les méthodes.
app = Flask(__name__)
# Modyfying part of the original config / check print(app.config)
app.config["DEBUG"] = True
#app.config['JSON_SORT_KEYS'] = False

# Load the Pickle file in the memory
pickle_in = open('best_model.pickle', 'rb')
model = pickle.load(pickle_in)


st.write("ok tout continu de marcher")

# Instruction de routage '/predict' = chemin predict ++> "POST" pour recevoir des données utilisateur
@app.route('/predict', methods=["POST"])
def prediction():
    data = request.get_json()
    prediction_value = np.array2string(model.predict_proba(data)[0, 1])

    return jsonify(prediction_value)

# Instruction de routage
@app.route('/explain', methods=["POST"])
def explain():
    data_client = request.json
    data_client_values = np.array([list(data_client.values())])
    data_client_features = list(data_client.keys())
    explainer_shap = shap.TreeExplainer(model)
    shap_values_client = explainer_shap.shap_values(data_client_values)
    shap_values_client_serie = pd.Series(index=data_client_features, data=shap_values_client[1][0, :])

    return jsonify(shap_values_client_serie.to_dict())
    
st.write('yes')
    
if __name__ == '__main__':
    app.run()

