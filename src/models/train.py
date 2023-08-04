from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
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


# get the data
dataset = pd.read_csv("../../data/data.csv")
X = dataset.iloc[:, 1:-1].values # independent variables: the features
y = dataset.iloc[:, -1].values # dependent variables: the class

# Encoding the Dependent Variables
le = LabelEncoder()
y = le.fit_transform(y)

# split the dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# perform feature scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# list of ML-based techniques classification
classifiers = [
    ['SVC', SVC(kernel="rbf")],
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

# training
for classifier in classifiers:
    
    # get the classifier name and model
    name_of_classifier = classifier[0]
    model = classifier[1]

    # train the model
    model.fit(X_train, y_train)

    # get the classification
    y_train_predicted = model.predict(X_train)
    y_test_predicted = model.predict(X_test)

    # scores
    accuracy_train = accuracy_score(y_train, y_train_predicted)
    accuracy_test = accuracy_score(y_test, y_test_predicted)

    f1_score_train = f1_score(y_train, y_train_predicted)
    f1_score_test = f1_score(y_test, y_test_predicted)

    precision_train = precision_score(y_train, y_train_predicted)
    precision_test = precision_score(y_test, y_test_predicted)

    recall_train = recall_score(y_train, y_train_predicted)
    recall_test = recall_score(y_test, y_test_predicted)

    scores = [
        name_of_classifier,
        accuracy_train,
        accuracy_test,
        f1_score_train,
        f1_score_test,
        precision_train,
        precision_test,
        recall_train,
        recall_test
    ]

    metrics.loc[len(metrics)] = scores

# export result
metrics.to_csv("train_result.csv", index=False)
    

# tuning hyperparameters? Are there automatic ways?

# what evaluation metrics should we focus on?
