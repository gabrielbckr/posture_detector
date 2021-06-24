import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import model_selection
from sklearn.ensemble import AdaBoostClassifier
import sklearn
import yellowbrick
from yellowbrick.features import RadViz
from yellowbrick.model_selection import FeatureImportances


def plot_positions_from_df(df_g, categories, value_col, ax = None):
    df_g.dropna(axis=0)
    if ax is None:
        ax = plt
    ax.plot(df_g[value_col], c='grey', alpha=0.3)
    for c in categories:
        c = df_g[df_g['Label'] == c][value_col]
        ax.scatter(c.index, c.values, marker='.', lw=[0.05]*len(c.index))


def get_model_comparisons(model_register, X, y):
    results = {}
    for mn, model in model_register:
        scores = model_selection.cross_validate(
            model, X, y,
            cv=5,
            scoring=('accuracy', 'f1'),
            return_train_score=True
        )
        results.update({mn: pd.DataFrame(scores).mean().to_dict()})
    result = pd.DataFrame(results).drop(index=['fit_time', 'score_time'])
    return result


def plot_radial_feature_comparisons(X, y):
    visualizer = RadViz(classes=['Correto', 'Incorreto'])
    visualizer.fit(X, y.values)
    visualizer.transform(X)
    visualizer.show()
    plt.show()


def plot_confusion_matrix(model, X, y):
    confusion_matrix = sklearn.metrics.confusion_matrix(
        y,
        model.predict(X),
        normalize='true',
    )
    confusion_matrix *= 100

    sklearn.metrics.ConfusionMatrixDisplay(
            confusion_matrix,
            display_labels=['Correto', 'Incorreto']
        ).plot(cmap='cividis', values_format='.2g')
    plt.ylabel('Classe Correta')
    plt.xlabel('Classe Predita')


def plot_auc(model, X_train, X_test, y_train, y_test, classes):
    roc_auc_viz = yellowbrick.classifier.ROCAUC(model, classes=classes)
    roc_auc_viz.fit(X_train, y_train)
    roc_auc_viz.score(X_test, y_test)
    roc_auc_viz.show()
    plt.show()


def plot_feature_importances(X, y):
    feature_viz = FeatureImportances(AdaBoostClassifier())
    feature_viz.fit(X, y)
    feature_viz.show()
    plt.show()


def plot_decision_boundary(model, X, y, variable_1=None, variable_2=None):
    if not variable_1 or not variable_2:
        X = sklearn.decomposition.PCA(n_components=2).fit_transform(X, y)
        X = pd.DataFrame(X)
        variable_1 = 0
        variable_2 = 1
    model.fit(X[[variable_1, variable_2]], y)

    xmin = min(X[variable_1].values)
    ymin = min(X[variable_2].values)
    xmax = max(X[variable_1].values)
    ymax = max(X[variable_2].values)

    xx, yy = np.mgrid[xmin:xmax:.001, ymin:ymax:.01]
    grid = np.c_[xx.ravel(), yy.ravel()]
    probs = model.decision_function(grid).reshape(xx.shape)

    f, ax = plt.subplots(figsize=(8, 6))
    ax.contour(xx, yy, probs, levels=[.5], cmap="Greys", vmin=0, vmax=.6)

    ax.scatter(X[variable_1].values, X[variable_2].values, c=y.values, s=50,
           cmap="RdBu", vmin=-.2, vmax=1.2,
           edgecolor="white", linewidth=1)

    plt.show()
