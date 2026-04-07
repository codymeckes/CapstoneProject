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