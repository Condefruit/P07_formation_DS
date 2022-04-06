import streamlit as st
import pandas as pd
import s3fs
import numpy as np
import plotly.express as px
import json
import requests

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


# Communicating with the Heroku API
url = "https://p07oc.herokuapp.com/predict" # adress of the Heroku API
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
client_datas = [X_test.loc[customer_number].values.tolist()]
j_data = json.dumps(client_datas) # json produit toujours des objets str
response_api_preditct = requests.post(url, data=j_data, headers=headers) # post --> send datas to the server
#st.write('reponse ok', response_api_preditct)
risk = float(response_api_preditct.text.split('"')[1])
st.write(risk)

# Sending the API the scaled data and getting a dict of the shap values
url = "https://p07oc.herokuapp.com//explain"
data_client = X_test.loc[customer_number].to_dict()
response_api_explain = requests.post(url, json=data_client)
st.write('reponse ok', response_api_explain)

# We'll use a dataframe for convenience, sorting etc
explanation_client = pd.DataFrame({'shap_value': response_api_explain.json().values(),
                                       'feature_name': response_api_explain.json().keys()})

st.dataframe(explanation_client.head(2))

nb_features_explain = 5

# Getting most important lines using absolute values
explanation_client['shap_value_abs'] = explanation_client.shap_value.map(abs)
# Tagging positive and negative values and setting a color for plotting
explanation_client['color'] = explanation_client.shap_value > 0
explanation_client.color.replace(True, 'red', inplace=True)
explanation_client.color.replace(False, 'green', inplace=True)
# Sorting by abs value
explanation_client.sort_values('shap_value_abs', ascending=False, inplace=True)
# Getting only the number asked by user
explanation_client = explanation_client.head(nb_features_explain)
# Changing the order because plotly plots from bottom to top
explanation_client.sort_values('shap_value_abs', ascending=True, inplace=True)
# Getting raw data and writing it on the labels
explanation_client['raw_data'] = data_raw_client[explanation_client.feature_name].iloc[0].values
explanation_client['bar_labels'] = explanation_client.feature_name + '\n=' \
                                       + explanation_client.raw_data.round(2).astype(str)
# Setup figure
fig = go.Figure(go.Bar(x=explanation_client['shap_value'],
                           y=explanation_client['bar_labels'],
                           orientation='h',
                           marker={'color': explanation_client['color']},
                           ),
                    )
fig.update_layout(xaxis_title="Influence sur le niveau de risque",
                      )

st.plotly_chart(fig,
                    use_container_width=True)






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



