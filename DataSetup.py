import os
import pandas as pd

data_folder = "data"
output_folder = "cleaned"

os.makedirs(output_folder, exist_ok=True)

stock_files = {
    "SIVB.csv": "SIVB",
    "SBNYP.csv": "SBNY",
    "FRC.csv": "FRC",
    "DB.csv": "DB",
    "CS.csv": "CS"
}

for file_name, ticker in stock_files.items():
    file_path = os.path.join(data_folder, file_name)
    df = pd.read_csv(file_path)

    df.columns = [col.strip().lower() for col in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df["ticker"] = ticker

    df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]
    df.to_csv(os.path.join(output_folder, f"cleaned_{ticker}.csv"), index=False)

nasdaq = pd.read_csv(os.path.join(data_folder, "nasdq.csv"))
nasdaq.columns = [col.strip().lower() for col in nasdaq.columns]
nasdaq["date"] = pd.to_datetime(nasdaq["date"])

nasdaq.to_csv(os.path.join(output_folder, "cleaned_nasdq.csv"), index=False)

print("Cleaning complete.")
print("Cleaning complete. Now loading into PostgreSQL...")

from sqlalchemy import create_engine

engine = create_engine("postgresql://capstone_user:capstone_pass_123@localhost:5432/thesis_data")

# Combine stock data (reuse your cleaned dfs if you already made them)
stock_files = {
    "SIVB.csv": "SIVB",
    "SBNYP.csv": "SBNY",
    "FRC.csv": "FRC",
    "DB.csv": "DB",
    "CS.csv": "CS"
}

import os
import pandas as pd

all_stocks = []

for file_name, ticker in stock_files.items():
    df = pd.read_csv(os.path.join("data", file_name))
    
    df.columns = [col.strip().lower() for col in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df["ticker"] = ticker
    
    df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]
    all_stocks.append(df)

stock_df = pd.concat(all_stocks)

# overwrite table each run (good for now)
stock_df.to_sql("stock_data", engine, if_exists="replace", index=False)

# Macro data
macro = pd.read_csv(os.path.join("data", "nasdq.csv"))
macro.columns = [col.strip().lower() for col in macro.columns]
macro["date"] = pd.to_datetime(macro["date"])

macro.to_sql("market_indicators", engine, if_exists="replace", index=False)

print("Data successfully loaded into PostgreSQL ")