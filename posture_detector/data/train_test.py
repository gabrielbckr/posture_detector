from pathlib import Path
from posture_detector.data import load_raw_from_csv


DEFAULT_CSV_TRAIN_TEST_FILE = '../../data/raw/datalog_at_2020-11-26_23_58_33.576158'


def get_train_test_data_df(file: str = None):
    if file is None:
        file = Path('.').resolve().joinpath(DEFAULT_CSV_TRAIN_TEST_FILE).__str__()
    df = load_raw_from_csv(file)
    return df


def get_train_test_data(file: str = None):
    df = get_train_test_data_df(file)
    X = None
    y = None
    raise NotImplementedError()
    return X, y
