import streamlit as st
import pandas
import s3fs
import boto3
import io

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

st.write("AWS ID:", st.secrets["AWS_ACCESS_KEY_ID"])

s3_file_key = 'X_test.csv'
bucket = 'p07oc'

s3 = boto3.client('s3')
obj = s3.get_object(Bucket=bucket, Key=s3_file_key)

df = pd.read_csv(io.BytesIO(obj['Body'].read()))

# Print results.
st.dataframe(df)


