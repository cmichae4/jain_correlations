import streamlit as st
from src.preprocess import alternative_pre_process, load_from_parquet


@st.cache_data
def get_pivot_table():
    with st.spinner("Preloading data..."):
        pivot_table = load_from_parquet("data/parquet")
        return pivot_table