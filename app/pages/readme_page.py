import streamlit as st

with open("README.md") as file:
    content = file.read()

st.markdown(content, unsafe_allow_html=True)