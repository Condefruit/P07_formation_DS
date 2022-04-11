import streamlit as st
import pandas as pd
import s3fs
import numpy as np
import plotly.express as px
import json
import requests
import plotly.graph_objects as go

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# ----------------------------------------
# ----------------------------------------

# #Loading data from amazon / desactivated to avoid useless data consu

# # Create connection object.
# # `anon=False` means not anonymous, i.e. it uses access keys to pull data.
# fs = s3fs.S3FileSystem(anon=False)

# # Retrieve file contents.
# # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)

# def read_file(filename):
#     with fs.open(filename) as f:
#         return pd.read_csv(f)


# X_train = read_file("p07oc/X_train.csv")
# y_train = read_file("p07oc/y_train.csv")
# X_test = read_file("p07oc/X_test.csv")
# y_test = read_file("p07oc/y_test.csv")

# X_train = X_train.set_index('Unnamed: 0')
# X_test = X_test.set_index('Unnamed: 0')

# ----------------------------------------
# ----------------------------------------

# #Loading data from a local source

url_X_test = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/X_test.csv"
url_y_test = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/y_test.csv"

X_test = pd.read_csv(url_X_test, index_col=[0])
y_test = pd.read_csv(url_y_test, index_col=[0])



# General
# ----------------------------------------
# ----------------------------------------

cus = X_test.shape[0]
customers = X_test.index


# Sidebar
# ----------------------------------------
# ----------------------------------------


st.sidebar.write('Available number of clients ', cus)

customer_number = st.sidebar.selectbox('Select the customer ID', customers)

# Separation
st.sidebar.markdown("""---""")

threshold = st.sidebar.slider("Choose a threshold", min_value=0.0, max_value = 1.0, value=0.5, step = 0.01)

st.sidebar.markdown("""---""")

nb_features_explain = st.sidebar.slider('Number of explanation features', min_value=1, max_value = 15, value=5, step = 1)

st.sidebar.markdown("""---""")

amount = X_test['AMT_CREDIT'].loc[customer_number]
ab = 6

cola, colb = st.sidebar.columns(2)

with cola:
    st.header(amount)
    st.write(ab)

with colb:
    new_amount = st.number_input('New credit amount', min_value = 1)

update = st.sidebar.button('Change Amount')
if update:
    ab = new_amount


# Communication with the API
# ----------------------------------------
# ----------------------------------------

# Communicating with the Heroku API
url = "https://p07oc.herokuapp.com/predict" # adress of the Heroku API
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
client_datas = [X_test.loc[customer_number].values.tolist()]
j_data = json.dumps(client_datas) # json produit toujours des objets str
response_api_preditct = requests.post(url, data=j_data, headers=headers) # post --> send datas to the server
risk = float(response_api_preditct.text.split('"')[1])

# Sending the API the scaled data and getting a dict of the shap values
url = "https://p07oc.herokuapp.com//explain"
data_client = X_test.loc[customer_number].to_dict()
response_api_explain = requests.post(url, json=data_client)

# We'll use a dataframe for convenience, sorting etc
explanation_client = pd.DataFrame({'shap_value': response_api_explain.json().values(),
                                       'feature_name': response_api_explain.json().keys()})

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
explanation_client['raw_data'] = X_test.loc[customer_number][explanation_client.feature_name].iloc[0]
explanation_client['bar_labels'] = explanation_client.feature_name + '\n=' \
                                       + explanation_client.raw_data.round(2).astype(str)


# Main page
# ----------------------------------------
# ----------------------------------------                                       


st.title('Welcome to the credit answer dashboard !')
st.write('This application predict if the selected client will statistically refund or not his loan')

st.write('the risk of fail refunding is :', risk)
if risk < threshold :
    st.success("#### According to the thresold, the loan offer is Acceptep")
else :
    st.error("#### According to the thresold, the loan offer is Refused")


# st.markdown(f"<center style='font-family:Verdana ; color:{color_decision}; font-size: 60px;'>{litteral_decision.upper()}</center>",   unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Client datas')
    st.write('')
    st.write('')
    st.write('Scroll to check ones of the', X_test.shape[1], 'client features')
    st.write('')
    st.dataframe(X_test.loc[customer_number])

with col2:
    st.subheader('Features importance')

    # Setup figure
    fig = go.Figure(go.Bar(x=explanation_client['shap_value'],
                           y=explanation_client['bar_labels'],
                           orientation='h',
                           marker={'color': explanation_client['color']},
                           ),
                    )

    st.plotly_chart(fig,
                    use_container_width=False)


# summarize

categories = list(X_test)

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



