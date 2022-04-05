import streamlit as st
import pandas as pd
import s3fs
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px

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

# General
# ----------------------------------------
# ----------------------------------------

cus = int(len(X_test))


# Sidebar
# ----------------------------------------
# ----------------------------------------

st.multiselect('bloobla', X_test)

st.sidebar.write('The number of available client number is ', cus)
customer_number = st.sidebar.number_input('Please select the customer number', min_value=0, max_value=cus, value=int(cus/2), step=1)

if customer_number != "" :
    st.markdown(
    f"""
    * Client number : {customer_number}
    """
)

# Separation
st.sidebar.markdown("""---""")

threshold = st.sidebar.slider("Choose a threshold", min_value=0.0, max_value = 1.0, value=0.5, step = 0.01)


st.sidebar.markdown("""---""")

amount = X_test['AMT_CREDIT']
st.sidebar.write(amount)


# Main page
# ----------------------------------------
# ----------------------------------------

test = X_train.copy()
test = test.set_index('Unnamed: 0')
st.dataframe(test.head(3))


st.title('Welcome to the credit answer dashboard !')

st.write('## This application predict if the client will refund or not his loan')

st.dataframe(X_train.head(3))

st.write(cus)


st.write(1)

RFinal = DecisionTreeClassifier(
    random_state=1, min_samples_split=2, max_features="sqrt"
)

st.write(2)

a = 0

if a == 1 :
    # Communicating with the Heroku API
    url = "https://p07oc.herokuapp.com/predict"
    client_datas = X_test.loc[customer_number].to_dict()
    response_api = requests.post(url, json=client_datas)


# summarize

st.write(3)

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



