import pandas as pd


if __name__ == "__main__":
    for filename in ["date_1.csv", "date_2.csv", "date_3.csv", "date_4.csv"]:
        df = pd.read_csv("sample_data/" + filename, parse_dates=["Date"])
        df.to_parquet("sample_data/" + filename.split(".")[0] + ".parquet")
