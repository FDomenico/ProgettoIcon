import pandas as pd
from sklearn.preprocessing import StandardScaler
from Models import *


def supervised(display: True, save: True):
    path = "../report"
    df = pd.read_csv('../dataset/new_dataset.csv', low_memory=False)
    df.drop(['UniqueCode'], axis=1, inplace=True)
    y = df['violation_type']
    X = df.drop(['violation_type'], axis=1)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    fold_number = 10

    dt = decision_tree(X, y, fold_number)
    if display:
        print(dt)
    if save:
        with open(f"{path}/decision_tree.txt", "w") as f:
            f.write(dt)

    kn = knn(X, y, fold_number)
    if display:
        print(kn)
    if save:
        with open(f"{path}/knn.txt", "w") as f:
            f.write(kn)

    nb = naive_bayes(X, y, fold_number)
    if display:
        print(nb)
    if save:
        with open(f"{path}/naive_bayes.txt", "w") as f:
            f.write(nb)

    lr = log_regression(X, y, fold_number)
    if display:
        print(lr)
    if save:
        with open(f"{path}/log_regression.txt", "w") as f:
            f.write(lr)

    rf = random_forest(X, y, fold_number)
    if display:
        print(rf)
    if save:
        with open(f"{path}/random_forest.txt", "w") as f:
            f.write(rf)

    sv = svm(X, y, fold_number)
    if display:
        print(sv)
    if save:
        with open(f"{path}/svm.txt", "w") as f:
            f.write(sv)


    ab = ada_boost(X, y, fold_number)
    if display:
        print(ab)
    if save:
        with open(f"{path}/ada_boost.txt", "w") as f:
            f.write(ab)

    nn = neural_network(X, y, fold_number)
    if display:
        print(nn)
    if save:
        with open(f"{path}/neural_network.txt", "w") as f:
            f.write(nn)


print("Starting...")
supervised(display=True, save=True)
print("Done!")
