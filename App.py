import numpy as np
import pandas as pd
import shap
import pickle
from lightgbm import LGBMClassifier
from flask import Flask, request, jsonify

# Crée l’objet application Flask, qui contient les données de l’application et les méthodes.
app = Flask(__name__)
# Modyfying part of the original config / check print(app.config)
app.config["DEBUG"] = True
#app.config['JSON_SORT_KEYS'] = False

# Load the Pickle file in the memory
pickle_in = open('best_model.pickle', 'rb')
model = pickle.load(pickle_in)

# Instruction de routage '/predict' = chemin predict ++> "POST" pour recevoir des données utilisateur
@app.route('/predict', methods=["POST"])
def prediction():
    data = request.get_json() # Parses the incoming JSON request data and returns it. / convertit l’objet JSON en données Python
    #print(data)
    prediction_value = np.array2string(model.predict_proba(data)[0, 1]) # retourne la proba de la class 1
    #print(prediction_value)

    return jsonify(prediction_value) # Serialize data to JSON

# Instruction de routage
@app.route('/explain', methods=["POST"])
def explain():
    data_client = request.json
    print("1", data_client)
    data_client_values = np.array([list(data_client.values())])
    print("2", ata_client_values)
    data_client_features = list(data_client.keys())
    print("3", data_client_features)
    explainer_shap = shap.TreeExplainer(model)
    print("4", explainer_shap) 
    shap_values_client = explainer_shap.shap_values(data_client_values)
    print("5", shap_values_client)
    shap_values_client_serie = pd.Series(index=data_client_features, data=shap_values_client[1][0, :])
    print("6", shap_values_client_serie)

    return jsonify(shap_values_client_serie.to_dict())

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

    
if __name__ == '__main__':
    app.run()

