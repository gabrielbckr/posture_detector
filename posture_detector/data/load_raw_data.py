import numpy as np
from scipy import signal
from pathlib import Path
from typing import Iterable
import pandas as pd
from constants.columns import Record


def load_raw_from_csv(csv_path: str) -> pd.DataFrame:
    file = Path(csv_path).resolve()
    assert file.exists() and file.is_file()
    df = pd.read_csv(file, sep=';')
    return df


def preprocess_data(df: pd.DataFrame, valid_classes: Iterable[str] = ('a', 'c')) -> pd.DataFrame:
    slice_dropna = ~df[Record.Label].apply(lambda x: x == 'nan')
    slice_with_labels = ~df[Record.Label].apply(lambda x: x == 'Key.enter')
    slice_with_postures = ~df[Record.Label].apply(lambda x: x not in valid_classes)
    data = df[slice_dropna & slice_with_labels & slice_with_postures]
    return data


def parse_dataset(df):
    replace_label = {'t': None, 'e': 0, 'c': 1, 'm': 0}
    data = df.copy()
    data['Label'] = data['Label'].apply(
        lambda x: replace_label[x] if x is not np.nan else None
    )

    data = data.drop(columns='Temperature').dropna(axis=0)
    data['Label'] = data['Label'].astype('int')
    return data



def filter_signal(sig: pd.Series, coef=(1, 0.01)):
    b, a = signal.butter(*coef)
    return signal.filtfilt(b, a, sig)
