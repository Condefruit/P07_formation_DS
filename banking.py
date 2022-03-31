import streamlit as st
import pandas as pd
import s3fs
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

def read_file(filename):
    with fs.open(filename) as f:
        return pd.read_csv(f)

st.title('Welcome to the credit answer dashboard !')

st.write('## This application predict if the client will refund or not his loan')

X_train = read_file("p07oc/X_train.csv")
y_train = read_file("p07oc/y_train.csv")
X_test = read_file("p07oc/X_test.csv")
y_test = read_file("p07oc/y_test.csv")

st.dataframe(X_train.head(3))

cus = int(len(X_test))
st.write(cus)

st.sidebar.write('The number of available client is ', cus)
customer_number = st.sidebar.number_input('Please select the customer number', min_value=0, max_value=cus, value=int(cus/2), step=1)

threshold = st.sidebar.slider("Choose a threshold", min_value=0.0, max_value = 1.0, value=0.5, step = 0.01)

if customer_number != "" :
    st.markdown(
    f"""
    * Client number : {customer_number}
    """
)

RFinal = DecisionTreeClassifier(
    random_state=1, min_samples_split=2, max_features="sqrt"
)

RFinal.fit(X_train, y_train)

yhat = RFinal.predict_proba([list(X_test.iloc[customer_number])])
result = yhat[0][1]
# summarize

categories = list(X_train)

st.subheader("Feature importance")

select_element = st.selectbox('Pick a category', categories)

st.subheader("Description of the category")
fig = px.scatter(X_test, x=select_element)
st.write(fig)



