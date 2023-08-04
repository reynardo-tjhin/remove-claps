from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.tree import ExtraTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import NuSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score 
import pandas as pd
import numpy as np


# get the data
dataset = pd.read_csv("../../data/data.csv")
X = dataset.iloc[:, 1:-1].values # independent variables: the features
y = dataset.iloc[:, -1].values # dependent variables: the class

# Encoding the Dependent Variables
le = LabelEncoder()
y = le.fit_transform(y)

# perform feature scaling
sc = StandardScaler()
X = sc.fit_transform(X)

# performing 10-Fold Stratified Cross Validation
skf = StratifiedKFold(n_splits=10)


# list of ML-based techniques classification
classifiers = [
    ['SVC', SVC(kernel="rbf", C=1)],
    ['ExtraTreesClassifier', ExtraTreeClassifier()],
    ['LinearDiscriminantAnalysis', LinearDiscriminantAnalysis()],
    ['DecisionTreeClassifier', DecisionTreeClassifier()],
    ['KNeighborsClassifier', KNeighborsClassifier()],
    ['RandomForestClassifier', RandomForestClassifier()],
    ['MLPClassifier', MLPClassifier(max_iter=500)],
    ['AdaBoostClassifier', AdaBoostClassifier()],
    ['NuSVC', NuSVC()],
    ['GaussianNB', GaussianNB()],
    ['QuadraticDiscriminantAnalysis', QuadraticDiscriminantAnalysis()]
]

# store metrics in .csv file
metrics = pd.DataFrame({
    'Model': [],
    'Accuracy (Train)': [],
    'Accuracy (Test)': [],
    'F1 (Train)': [],
    'F1 (Test)': [],
    'Precision (Train)': [],
    'Precision (Test)': [],
    'Recall (Train)': [],
    'Recall (Test)': [] 
})

accuracy_trains = np.zeros((1,10))
accuracy_tests = np.zeros((1,10))
f1_score_trains = np.zeros((1,10))
f1_score_tests = np.zeros((1,10))
precision_trains = np.zeros((1,10))
precision_tests = np.zeros((1,10))
recall_trains = np.zeros((1,10))
recall_tests = np.zeros((1,10))

# training
for classifier in classifiers:
    
    # get the classifier name and model
    name_of_classifier = classifier[0]
    model = classifier[1]

    i = 0 # index

    print(f"Training using {name_of_classifier} model...")

    # cross-validation
    for train_index, test_index in skf.split(X, y):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # train the model
        model.fit(X_train, y_train)

        # get the classification
        y_train_predicted = model.predict(X_train)
        y_test_predicted = model.predict(X_test)

        # scores
        accuracy_trains[0][i] = accuracy_score(y_train, y_train_predicted)
        accuracy_tests[0][i] = accuracy_score(y_test, y_test_predicted)

        f1_score_trains[0][i] = f1_score(y_train, y_train_predicted)
        f1_score_tests[0][i] = f1_score(y_test, y_test_predicted)

        precision_trains[0][i] = precision_score(y_train, y_train_predicted)
        precision_tests[0][i] = precision_score(y_test, y_test_predicted)

        recall_trains[0][i] = recall_score(y_train, y_train_predicted)
        recall_tests[0][i] = recall_score(y_test, y_test_predicted)

        i += 1

    scores = [
        name_of_classifier,
        accuracy_trains.mean(),
        accuracy_tests.mean(),
        f1_score_trains.mean(),
        f1_score_tests.mean(),
        precision_trains.mean(),
        precision_tests.mean(),
        recall_trains.mean(),
        recall_tests.mean()
    ]

    metrics.loc[len(metrics)] = scores

# export result
metrics.to_csv("train_result.csv", index=False)
    

# tuning hyperparameters? Are there automatic ways?

# what evaluation metrics should we focus on?
