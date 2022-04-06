import streamlit as st
import pandas as pd
import s3fs
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
import json

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# ----------------------------------------
# ----------------------------------------

#Loading data

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

def read_file(filename):
    with fs.open(filename) as f:
        return pd.read_csv(f)


X_train = read_file("p07oc/X_train.csv")
y_train = read_file("p07oc/y_train.csv")
X_test = read_file("p07oc/X_test.csv")
y_test = read_file("p07oc/y_test.csv")

X_train = X_train.set_index('Unnamed: 0')
X_test = X_test.set_index('Unnamed: 0')

# General
# ----------------------------------------
# ----------------------------------------

cus = X_test.shape[0]
customers = X_test.index


# Sidebar
# ----------------------------------------
# ----------------------------------------


st.sidebar.write('The number of available client number is ', cus)
customer_number = st.sidebar.selectbox('Select the customer number', customers)

# Separation
st.sidebar.markdown("""---""")

threshold = st.sidebar.slider("Choose a threshold", min_value=0.0, max_value = 1.0, value=0.5, step = 0.01)


st.sidebar.markdown("""---""")

amount = X_test['AMT_CREDIT'].loc[customer_number]
st.sidebar.write(amount)


# Main page
# ----------------------------------------
# ----------------------------------------


st.title('Welcome to the credit answer dashboard !')

st.write('## This application predict if the client will refund or not his loan')

st.dataframe(X_test.loc[customer_number])

a = 1
if a == 1 :
    # Communicating with the Heroku API
    url = "https://p07oc.herokuapp.com/predict"
    client_datas = [X_test.loc[customer_number].values.tolist()]
    st.write(client_datas)
    j_data = json.dumps(client_datas)
    response_api = requests.post(url, data=j_data)
    risk = float(response_api.text.split('"')[1])
    st.write(risk)



# summarize

categories = list(X_train)

st.subheader("Feature importance")

select_element1 = st.selectbox('Pick a first category', categories)
select_element2 = st.selectbox('Pick a second category', categories)

col1, col2 = st.columns(2)

col1.subheader("Description of the category")
fig1 = px.scatter(X_test, x=select_element1)
col1.write(fig1, use_column_width=True)

col2.subheader("Description of the category")
fig2= px.scatter(X_test, x=select_element2)
col2.write(fig2, use_column_width=True)



