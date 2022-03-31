import streamlit as st
import pandas as pd
import s3fs

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

def read_file(filename):
    with fs.open(filename) as f:
        return pd.read_csv(f)

df = read_file("p07oc/X_test.csv")

st.dataframe(df)

# https://p07oc.s3.eu-west-3.amazonaws.com/X_test.csv

