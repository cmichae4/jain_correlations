import pandas as pd
import glob
import time # imported because was profiling read speeds
from concurrent.futures import ThreadPoolExecutor

def read_single_csv(filepath: str):
    return pd.read_csv(filepath, usecols=["Date", "Ticker", "Price"], parse_dates=["Date"])

def read_single_parquet(filepath: str):
    return pd.read_parquet(filepath)

def load_from_parquet(directory):
    files_to_read = list(glob.glob(directory + "/*.parquet"))
    # the threadpool didn't help much on my machine (operation was I/O bounded not CPU, but doesn't hurt)
    with ThreadPoolExecutor(max_workers=8) as pool:
        df_list = list(pool.map(read_single_parquet, files_to_read))
    master_df = pd.concat(df_list, ignore_index=True)
    master_df.dropna(subset=["Date", "Ticker", "Price"], inplace=True)
    pivoted = master_df.pivot(index="Date", columns="Ticker", values="Price")

    return pivoted

def alternative_pre_process():
    """
    Legacy method, initially was just reading in the csv's, use load_from_parquet instead.
    :return:
    """
    files_to_read =  [x for x in glob.glob("data/stock_data/*.csv") if x != 'data/stock_data/20210222.csv']
    with ThreadPoolExecutor(max_workers=8) as pool:
        df_list = list(pool.map(read_single_csv, files_to_read))

    master_df = pd.concat(df_list,  ignore_index=True)

    master_df.dropna(subset=['Date', 'Ticker', 'Price'], inplace=True)
    pivoted = master_df.pivot(columns='Ticker', index='Date', values='Price')

    return pivoted



