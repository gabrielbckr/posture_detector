import click
import pickle
from pathlib import Path
from sklearn.linear_model import RidgeClassifier

from posture_detector.data import load_raw_from_csv, parse_dataset, preprocess_data
from posture_detector.constants.columns import Record


def train_model(X, y):
    model: RidgeClassifier = RidgeClassifier().fit(X, y)
    score = model.score(X, y)
    click.echo(f'Training score: {score}')
    return model


def process_classification(training_data_path, model_path):
    data = load_raw_from_csv(training_data_path)
    data = parse_dataset(data)
    data = preprocess_data(data, ['a', 'c'])

    y = data.pop(Record.Label)
    X = data
    model = train_model(X, y)

    save_model(model, model_path)


def save_model(model, model_path: str):
    path = Path(model_path)
    with open(path, 'wb') as file:
        pickle.dump(model, file)
    click.echo(f'Model saved at {path}')
