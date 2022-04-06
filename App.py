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


    
st.write('yes')
    
if __name__ == '__main__':
    app.run()

