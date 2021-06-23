import pickle
import pandas as pd
import sklearn

model = None
destination_file = '../data/raw/session0'


async def post_data_handler(payload):
    global destination_file

    content = await payload.json()
    print(content)
    data = pd.DataFrame([content])
    data.to_csv(destination_file, mode='a', header=False)


def set_destination_file(path):
    global destination_file
    destination_file = path


def set_model(path: str = '../snakes/test.pkl') -> sklearn.base.ClassifierMixin:
    global model
    with open(path, 'rb') as file:
        model = pickle.load(file)
