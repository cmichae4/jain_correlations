import streamlit as st
from src.correlation import two_stock_sliding_correlation
from src.cached_data_loader import get_pivot_table

st.header("Correlation of two stocks over complete history")
left_column, right_column = st.columns(2)
p_table = get_pivot_table()

if "left_tkr" not in st.session_state:
    st.session_state.left_tkr = p_table.columns[0]

if "right_tkr" not in st.session_state:
    st.session_state.left_tkr = p_table.columns[0]



with left_column:
    st.session_state.left_tkr = st.selectbox("First stock: ", options=p_table.columns, index=p_table.columns.get_loc(st.session_state.left_tkr) if "left_tkr" in st.session_state else 0)

with right_column:
    st.session_state.right_tkr = st.selectbox("Second stock: ", options=p_table.columns, index=p_table.columns.get_loc(st.session_state.right_tkr) if "right_tkr" in st.session_state else 0)

left_tkr, right_tkr = st.session_state.left_tkr, st.session_state.right_tkr
time_series_a, time_series_b = p_table[left_tkr], p_table[right_tkr]


with left_column:
    st.markdown(f"Price series of {left_tkr}")
    st.line_chart(time_series_a)

with right_column:
    st.markdown(f"Price series of {right_tkr}")
    st.line_chart(time_series_b)

st.markdown(f"Correlation of {left_tkr} vs {right_tkr} over time")
corr_over_time = two_stock_sliding_correlation(p_table, left_tkr, right_tkr)
st.line_chart(corr_over_time)


