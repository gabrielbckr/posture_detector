from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def get_regressor_pipeline() -> Pipeline:
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression()),
    ])
    return model


def process_regression():
    raise NotImplementedError()
