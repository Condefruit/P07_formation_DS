import streamlit as st

st.title('Welcome to the credit answer dashboard')

port=os.environ.get('PORT', '8501')
print(port)

run(host='0.0.0.0', port=port)

