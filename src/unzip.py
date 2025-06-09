import zipfile
import glob
import pandas as pd
import os

def unzip_file(file_path, destination):
    with zipfile.ZipFile("../data/stock_data.zip") as zip_path:
        zip_path.extractall("../data")

def convert_to_csv(directory_path):
    parquet_dir = os.path.join(directory_path, "parquet")
    os.makedirs(parquet_dir, exist_ok=True)
    for f in glob.glob("../data/stock_data/*.csv"):
        if f ==  "../data/stock_data/20210222.csv":
            continue
        df = pd.read_csv(f, parse_dates=["Date"])
        df.to_parquet(os.path.join(parquet_dir, os.path.basename(f).replace(".csv", ".parquet")),
                      index=False)

if __name__ == "__main__":
    zip_path = "../data/stock_data.zip"
    dest_dir = "../data"
    unzip_file(zip_path, dest_dir)
    convert_to_csv(dest_dir)