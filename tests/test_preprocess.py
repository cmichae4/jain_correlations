import pytest
from src.preprocess import load_from_parquet


class TestPreProcess:
    def test_load_data(self):
        df = load_from_parquet("sample_data")
        assert(df.shape == (4, 3)) # correct wide pivot
        assert(list(df.columns) == ["A", "B", "C"]) # one stock per column, no NaN