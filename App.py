import streamlit as st
import os
import s3fs

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

st.write("AWS ID:", st.secrets["db_username"])

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

st.title('Welcome to the credit answer dashboard')

df = read_file("p07oc/X_test.csv")

# Print results.
st.dataframe(df)