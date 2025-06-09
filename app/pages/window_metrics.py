import streamlit as st
import pandas as pd
import numpy as np
from src import correlation, cached_data_loader
from src.plotting import plot_fast, plot_heatmap_smart

st.set_page_config(layout="wide")
left_column, right_column = st.columns(2, gap="medium", )
p_table = cached_data_loader.get_pivot_table()


@st.cache_data
def get_valid_windows(p_table: pd.DataFrame):
    valid_windows = correlation.sliding_windows(p_table)
    return dict(valid_windows)


@st.cache_data
def correlation_dict(valid_windows: dict):
    return_dfs = map(correlation.price_to_returns, map(lambda x: x[1], valid_windows))
    valid_dates_for_lookback = map(lambda x: x[0], valid_windows)
    correlation_matrices = map(correlation.correlation, return_dfs)
    return dict(zip(valid_dates_for_lookback, correlation_matrices))

date_to_window = get_valid_windows(p_table)
available_dates = list(date_to_window.keys())[::-1]

# Initialize session state
if "target_date" not in st.session_state:
    st.session_state.target_date = available_dates[0]

if "ticker_select" not in st.session_state:
    st.session_state.ticker_select = p_table.columns[0]

st.session_state.target_date = st.sidebar.selectbox(
    label="Select date for correlation matrix",
    options=available_dates,
    format_func=lambda x: x.date().isoformat(),
    index=available_dates.index(st.session_state.target_date) if "target_date" in st.session_state else 0,
)

st.session_state.ticker_select = st.sidebar.selectbox(
    label="Select Ticker for Timeseries display",
    options=p_table.columns,
    index=p_table.columns.get_loc(st.session_state.ticker_select) if "ticker_select" in st.session_state else 0,
)


@st.cache_data(max_entries=30)
def get_correlation_matrix(target_date):
    window = date_to_window[target_date]
    return_df = correlation.price_to_returns(window)
    return correlation.correlation(return_df)


corr_matrix = get_correlation_matrix(st.session_state.target_date)
k = 10
top_k_positive_correlations = corr_matrix[st.session_state.ticker_select].nlargest(k+1).iloc[1:]
top_k_negative_correlations = corr_matrix[st.session_state.ticker_select].nsmallest(k)

with right_column:
    st.header(f"Single Ticker: {st.session_state.ticker_select}")
    st.markdown(f"Price series of ticker {st.session_state.ticker_select}")
    st.line_chart(p_table[st.session_state.ticker_select])
    st.markdown(f"Top {k} largest positive correlations for {st.session_state.ticker_select}")
    st.table(top_k_positive_correlations)
    st.markdown(f"Top {k} largest negative correlations for {st.session_state.ticker_select}")
    st.table(top_k_negative_correlations)


@st.cache_data
def get_top_bottom_k_fast(corr_df, k=10):
    # Get upper triangle indices since they are symmetric
    i, j = np.triu_indices_from(corr_df.values, k=1)


    values = corr_df.values[i, j]
    idx = pd.MultiIndex.from_arrays([corr_df.index[i], corr_df.columns[j]])

    # this method gets top k without sorting, for speed
    top_idx = np.argpartition(values, -k)[-k:]
    bottom_idx = np.argpartition(values, k)[:k]

    top_k = pd.Series(values[top_idx], index=idx[top_idx])
    bottom_k = pd.Series(values[bottom_idx], index=idx[bottom_idx])

    return top_k, bottom_k


top_k, bottom_k = get_top_bottom_k_fast(corr_matrix, k=10)
with left_column:
    st.header(f"Aggregate Statistics for {st.session_state.target_date.date().isoformat()}")
    st.markdown(f"Top {k} positive and negative correlations across all stocks for lookback window")
    top_k.index.names=['Ticker 1', 'Ticker 2']
    bottom_k.index.names=['Ticker 1', 'Ticker 2']
    x = top_k.reset_index().sort_values(by=0, ascending=False).rename(columns={0: 'Correlations'})
    y = bottom_k.reset_index().sort_values(by=0).rename(columns={0: 'Correlations'})
    st.table(x)
    st.table(y)
    plot_fast(top_k, bottom_k)
    st.markdown(f"Correlation matrix of {k} largest correlations for lookback window")
    plot_heatmap_smart(corr_matrix, top_k, bottom_k)
