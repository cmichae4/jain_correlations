from datetime import timedelta
import pandas as pd
import numpy as np
import streamlit

def sliding_windows(df: pd.DataFrame, window_size=21, max_gap_allowed=5):
    """
    get 21 days before, check if large gaps exist, decide on return type in that case
    store these so that they are indexed by the "result-date", and the result will be a T x N window
    where T is window size, N is number of stocks (so across all of them)
    """
    valid_windows = []
    windows = df.rolling(window=window_size)
    cnt = 0
    for w in windows:
        cnt += 1
        deltas = w.index.diff()
        no_max_gap = len(w) >= window_size and (deltas[1:] < timedelta(days=max_gap_allowed)).all() # deltas[1:] because first is always NaT
        if no_max_gap:
            valid_windows.append(( w.index[-1], w))
    return valid_windows


def correlation(window_df: pd.DataFrame):
    """
    given a T x N price dataframe - where N is number of tickers,
    construct a correlation matrix (hopefully upper diagonal for memory saving,
    return it so that it can be indexed by [ticker_a, ticker_b] and the result will be the trailing correlation
    :param window_df:
    :return:
    """
    return pd.DataFrame(np.corrcoef(window_df.values, rowvar=False), columns=window_df.columns, index=window_df.columns)

@streamlit.cache_data(max_entries=100)
def two_stock_sliding_correlation(df: pd.DataFrame, tkr_a: str, tkr_b: str, window_size=20):
    """
    Should output a timeSeries indexed by date (end of window) and a single value for correlation.
    :param df:
    :param tkr_a:
    :param tkr_b:
    :return:
    """
    if tkr_a == tkr_b:
        series = df[tkr_a]
        two_ticker_df = pd.DataFrame({tkr_a: series, tkr_b: series})
    else:
        two_ticker_df = df[[tkr_a, tkr_b]]
    return_df = price_to_returns(two_ticker_df)
    valid_windows = sliding_windows(return_df, window_size=window_size)
    dates, corrs = [], []
    for (date, window_df) in valid_windows:
        window_correlation = window_df[tkr_a].corr(window_df[tkr_b])
        dates.append(date)
        corrs.append(window_correlation)
    return pd.Series(data=corrs, index=dates)

def price_to_returns(window_df: pd.DataFrame):
    """
    Convert price time-series to return time-series. Aim for vectorized, fast approach across whole dataframe.
    :param window_df:
    :return:
    """
    return window_df.pct_change(1).iloc[1:]