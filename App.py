import numpy as np
import pandas as pd
import shap
import pickle5 as pickle
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

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

    
if __name__ == '__main__':
    app.run()

