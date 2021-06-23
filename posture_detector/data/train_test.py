import pandas as pd
from pathlib import Path
from posture_detector.data import load_raw_from_csv
from posture_detector.constants.columns import Record


DEFAULT_CSV_TRAIN_TEST_FILE = '../../data/raw/datalog_at_2020-11-26_23_58_33.576158'


def get_train_test_data_df(file: str = None):
    if file is None:
        file = Path('.').resolve().joinpath(DEFAULT_CSV_TRAIN_TEST_FILE).__str__()
    df = load_raw_from_csv(file)
    return df


def get_train_test_data(file: str = None):
    df = get_train_test_data_df(file)
    return split_record_data(df)


def split_record_data(df: pd.DataFrame, feature_columns=None, label=None) -> pd.DataFrame:
    y = df[Record.Label]
    X = df[feature_columns] if feature_columns else df.drop(columns=Record.Label)
    return X, y
