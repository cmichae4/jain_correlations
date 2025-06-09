import pytest

import src.correlation
from src.correlation import price_to_returns, correlation, two_stock_sliding_correlation
from src.preprocess import load_from_parquet
import pandas as pd
import numpy as np
import datetime

class TestCorrelationHelpersClass:

    def test_conversion_to_return(self):
        df = load_from_parquet("sample_data")
        return_df = src.correlation.price_to_returns(df)
        assert(return_df.shape == (3, 3))
        assert(not return_df.isna().any().all())
        assert(np.allclose(return_df['B'].values,np.array([0.1, 0, 1.0/11.0])))

    def test_sliding_windows(self):
        df = load_from_parquet("sample_data")
        valid_windows = src.correlation.sliding_windows(df, window_size=2)
        assert(len(valid_windows) == 3)
        assert(all([len(window) == 2 for window in valid_windows]))
        (window_end_date, sub_df) = valid_windows[0]
        assert(window_end_date == datetime.datetime(2020,1,2))
        # TODO: Add a test to cover the max gap case for invalid window

    def test_correlation_matrix(self):
        df = load_from_parquet("sample_data")
        valid_windows = src.correlation.sliding_windows(df, window_size=4)
        (window_end_date, sub_df) = valid_windows[0]
        return_df = price_to_returns(sub_df)
        corr_df = correlation(return_df)
        for stock_a in ("A", "B", "C"):
            for stock_b in ("A", "B", "C"):
                corr = corr_df.loc[stock_a, stock_b]
                if stock_a == stock_b:
                    assert(np.isclose(corr,1))
                else:
                    assert(np.isclose(corr,return_df[[stock_a, stock_b]].corr()[stock_a].loc[stock_b]))


    def test_two_stock_correlation(self):
        # construct two theoretical stocks whose return stream for first window of size 4 is perfectly correlated
        # and last is perfectly inversely correlated
        returns_a  = np.array([0.1, 0.2, -0.3, 0.4, -0.2, 0.15, 0.8, -0.325, 0.001, 0.8])
        n = len(returns_a)
        returns_b = np.concatenate([returns_a[:n//2],-returns_a[n//2:]])
        prices_a = 100 * np.cumprod(1 + returns_a)
        prices_b = 100 * np.cumprod(1 + returns_b)

        date_index = pd.date_range(start="2021-01-01", periods=10, freq="D")
        price_df = pd.DataFrame(data=list(zip(prices_a, prices_b)), columns=["A", "B"], index=date_index)
        df = two_stock_sliding_correlation(price_df, "A", "B", window_size=4)
        assert(np.isclose(df.iloc[0], 1))
        assert(np.isclose(df.iloc[-1], -1))
