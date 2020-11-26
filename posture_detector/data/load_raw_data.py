from pathlib import Path
import pandas as pd


def load_raw_from_csv(csv_path: str):
    file = Path(csv_path).resolve()
    df = pd.read_csv(file)
    df[0] = pd.to_numeric(df[0], 'coerce')
    df = df[df[0] < 1024]
    return df
