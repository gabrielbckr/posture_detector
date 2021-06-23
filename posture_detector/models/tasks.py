import numpy as np
from sklearn import model_selection
import pandas as pd


def get_model_comparisons_dataframe(model_register, X, y, scoring, cv: int = 5, decimals: int = 4) -> pd.DataFrame:
    results = []
    cols = pd.MultiIndex.from_product([scoring, ['train', 'test']])

    for mn, model in model_register:
        scores = model_selection.cross_validate(
            model, X, y,
            cv=cv,
            scoring=scoring,
            return_train_score=True
        )
        dict_scores = pd.DataFrame(scores).mean().to_dict()
        train_scores = {k.split('_')[-1]: v for k, v in dict_scores.items() if 'train' in k}
        test_scores = {k.split('_')[-1]: v for k, v in dict_scores.items() if 'test' in k}
        data = np.array(list(map(
            lambda x: np.round(x, decimals),
            list(train_scores.values()) + (list(test_scores.values()))
        )))
        results.append(
            pd.DataFrame(data.reshape((1, 2*len(scoring))), columns=cols, index=[mn])
        )
    return pd.concat(results)
