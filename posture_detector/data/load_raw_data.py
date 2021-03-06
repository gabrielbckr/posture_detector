from scipy import signal
from pathlib import Path
import pandas as pd
import numpy as np


def load_raw_from_csv(csv_path: str):
    file = Path(csv_path).resolve()
    df = pd.read_csv(file, sep=';', header=None)

    if 'Unnamed 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    df = df[~(df[1] == ' ')]
    df = df[~(df[1] == " '-'")]
    df[0] = pd.to_numeric(df[0], 'coerce')
    df[1] = df[1].apply(lambda x: str(x).replace('\'', '').replace(' ', ''))

    df[0] = filter_signal(df[0])
    return df


def parse_dataset(df: pd.DataFrame):

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    df['Label'] = df['Label'].apply(
        lambda x: str(x).replace('\'', '').replace(' ', '')
    )

    # df[df[] < 1024] = np.nan
    return df


def filter_signal(sig: pd.Series, coef=(1, 0.01)):
    b, a = signal.butter(*coef)
    return signal.filtfilt(b, a, sig)


def load_data_from_metadata_options():
    raise NotImplementedError
