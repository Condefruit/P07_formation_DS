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
# Ama = 1, load from SS / Ama = 0, load from git
Ama = 0
# ----------------------------------------

#Loading data from amazon / desactivated to avoid useless data consu
if Ama == 1:
    # Create connection object.
    # `anon=False` means not anonymous, i.e. it uses access keys to pull data.
    fs = s3fs.S3FileSystem(anon=False)

    # Retrieve file contents.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)

    def read_file(filename):
        with fs.open(filename) as f:
            return pd.read_csv(f)


    # X_train = read_file("p07oc/X_train.csv")
    # y_train = read_file("p07oc/y_train.csv")
    X_test = read_file("p07oc/X_test_na.csv")
    # y_test = read_file("p07oc/y_test.csv")
    desc = read_file("p07oc/description.csv")


    # X_train = X_train.set_index('Unnamed: 0')
    X_test = X_test.set_index('SK_ID_CURR')


# ----------------------------------------
# ----------------------------------------

#Loading data from a local source
if Ama == 0:
    url_X_test = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/X_test_na.csv"
    # url_y_test = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/y_test_na.csv"
    # url_train = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/X_train_light.csv"
    url_def = "https://raw.githubusercontent.com/Condefruit/P07_formation_DS/main/description.csv"

    # X_train = pd.read_csv(url_train, index_col=[0])
    X_test = pd.read_csv(url_X_test, index_col=[0])
    # y_test = pd.read_csv(url_y_test, index_col=[0])
    desc = pd.read_csv(url_def)

# General
# ----------------------------------------
# ----------------------------------------

cus = X_test.shape[0]
customers = X_test.sort_index().index


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

# Partie changement montant cr??dit
# ----------------------------------------
# ----------------------------------------

# amount = X_test['AMT_CREDIT'].loc[customer_number]
# ab = 6

# cola, colb = st.sidebar.columns(2)

# with cola:
#     st.header(amount)
#     st.write(ab)

# with colb:
#     new_amount = st.number_input('New credit amount', min_value = 1)

# update = st.sidebar.button('Change Amount')
# if update:
#     ab = new_amount


# Communication with the API
# ----------------------------------------
# ----------------------------------------

# Communicating with the Heroku API
urla = "https://p07oc.herokuapp.com/predict" # adress of the Heroku API
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
client_datas = [X_test.loc[customer_number].values.tolist()]
j_data = json.dumps(client_datas) # json produit toujours des objets str
response_api_preditct = requests.post(urla, data=j_data, headers=headers) # post --> send datas to the server
risk = float(response_api_preditct.text.split('"')[1])

# Sending the API the scaled data and getting a dict of the shap values
urlb = "https://p07oc.herokuapp.com//explain"
data_client = X_test.loc[customer_number].to_dict()
response_api_explain = requests.post(urlb, json=data_client)

# # Sending the API the dataframe
# urlc = "https://p07oc.herokuapp.com//globals"
# datas = X_test.head(1).to_json(orient="index")
# response_api_globals = requests.post(urlc, json=datas)

# We'll use a dataframe for convenience, sorting etc
explanation_client = pd.DataFrame({'shap_value': response_api_explain.json().values(),
                                       'feature_name': response_api_explain.json().keys()})

# Getting most important lines using absolute values
explanation_client['shap_value_abs'] = explanation_client.shap_value.map(abs)
# Tagging positive and negative values and setting a color for plotting
explanation_client['color'] = explanation_client.shap_value > 0
explanation_client.color.replace(True, 'deeppink', inplace=True)
explanation_client.color.replace(False, 'dodgerblue', inplace=True)
# Sorting by abs value
explanation_client.sort_values('shap_value_abs', ascending=False, inplace=True)
# Getting only the number asked by user
explanation_client = explanation_client.head(nb_features_explain)
# Changing the order because plotly plots from bottom to top
explanation_client.sort_values('shap_value_abs', ascending=True, inplace=True)
# Getting raw data and writing it on the labels
explanation_client['raw_data'] = X_test.loc[[customer_number]][explanation_client.feature_name].iloc[0].values
explanation_client['bar_labels'] = explanation_client.feature_name + '\n=' \
                                       + explanation_client.raw_data.round(2).astype(str)

# ----------------------------------------
# ----------------------------------------  
#                

st.title('Welcome to the credit answer dashboard !')
st.write('This application predict if the selected client will statistically refund or not his loan')

st.write('the risk of fail refunding is :', risk)
final_result = threshold - risk
if final_result >= 0 :
    text = "According to the thresold, the loan offer is Acceptep"
else :
    text = "According to the thresold, the loan offer is Refused"

#couleur du background de l'annonce
if -1<=final_result<-0.5 :
    color = '#df1717'
elif -0.5<=final_result<-0.25 :
    color = '#df5617'
elif -0.25<=final_result<0 :
    color = '#dfa517'
elif 0<=final_result<0.25 :
    color = '#afdf17'
elif 0.25<=final_result<1.1 :
    color = '#3ddf17'

text_color = '#000000'

def example(color, text_color, content):
     st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color}, {color});color:{text_color};font-size:24px;border-radius:2%;">{content}</p>', unsafe_allow_html=True)
example(color, text_color, text)


# st.markdown(f"<center style='font-family:Verdana ; color:{color_decision}; font-size: 60px;'>{litteral_decision.upper()}</center>",   unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Client datas')
    st.write('')
    st.write('')
    st.write('Scroll to check ones of the', X_test.shape[1], 'client features')
    st.write('')
    st.dataframe(X_test.loc[customer_number].sort_index())

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
st.write('----------------')

categories = list(X_test)

st.subheader("Current client compared with other clients")

select_element1 = st.selectbox('Pick a first category', categories)
st.write("Description :", desc[desc['col name'] == select_element1]['Description'].iloc[0])

select_element2 = st.selectbox('Pick a second category', categories)
st.write("Description :", desc[desc['col name'] == select_element2]['Description'].iloc[0])

col1, col2 = st.columns(2)

with col1 :
    st.subheader('feature 1')
    fig1 = px.scatter(X_test, x=select_element1)
    fig1.add_vline(x = X_test[select_element1].loc[customer_number], line_width = 3, line_dash='dot', line_color = 'red')
    col1.write(fig1, use_column_width=True)

col2.subheader("Feature 2")
fig2= px.scatter(X_test, x=select_element2)
fig2.add_vline(x = X_test[select_element2].loc[customer_number], line_width = 3, line_dash='dot', line_color = 'red')
col2.write(fig2, use_column_width=True)

col3, col4 = st.columns(2)

with col3 :
    st.subheader('Pair plot')
    fig3 = px.scatter(X_test, x = select_element1, y = select_element2)
    fig3.add_vline(x = X_test[select_element1].loc[customer_number], line_width = 1, line_color = 'red')
    fig3.add_hline(y = X_test[select_element2].loc[customer_number], line_width = 1, line_color = 'red')
    st.write(fig3)

from PIL import Image
image = Image.open('shap_glob.png')

col4.subheader("globale explainations")
col4.image(image, caption='Global feature impacts')

# testo = response_api_globals
# st.write(testo)

# st.write('----------------')
