from scipy import signal
from pathlib import Path
import pandas as pd


def load_raw_from_csv(csv_path: str):
    file = Path(csv_path).resolve()
    df = pd.read_csv(file, header=None)

    df = df[~(df[1] == ' ')]
    df = df[~(df[1] == " '-'")]
    df[0] = pd.to_numeric(df[0], 'coerce')
    df = df[df[0] < 1024]
    df[1] = df[1].apply(lambda x: str(x).replace('\'', '').replace(' ', ''))

    df[0] = filter_signal(df[0])
    return df


def filter_signal(sig: pd.Series):
    b, a = signal.butter(1, 0.01)
    return signal.filtfilt(b, a, sig)
