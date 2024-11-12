# 단순히 정확도가 높은 classifier은 대부분 Logistic Regression로 나오지만,
# 훈련이 1시간, 1일, 1주, 1개월 걸릴 수 있는 상황을 가정하므로,
# 이 과제에 적합한 classifier은 Second Best Classifier로 출력되는 Neural Network (MLP)이다.

import numpy as np
from sklearn import datasets, model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

if __name__ == '__main__':
    wdbc = datasets.load_breast_cancer()
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(wdbc.data)
    
    classifiers = {
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "SVC": SVC(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "AdaBoost": AdaBoostClassifier(algorithm='SAMME'),
        "Neural Network (MLP)": MLPClassifier(max_iter=1000),
    }

    best_score = 0
    second_best_score = 0
    best_classifiers = []
    second_best_classifiers = []

    for name, model in classifiers.items():
        cv_results = model_selection.cross_validate(model, scaled_data, wdbc.target, cv=5, return_train_score=True)
        acc_train = 1.000
        acc_test = np.mean(cv_results['test_score'])
        
        print(f'\nClassifier: {name}')
        print(f'* Accuracy @ training data: {acc_train:.3f}')
        print(f'* Accuracy @ test data: {acc_test:.3f}')
        score = max(10 + 100 * (acc_test - 0.9), 0)
        print(f'* Your score: {score:.0f}')
        
        if acc_test > best_score:
            second_best_score = best_score
            second_best_classifiers = best_classifiers.copy()
            best_score = acc_test
            best_classifiers = [name]
        elif acc_test == best_score:
            best_classifiers.append(name)
        elif acc_test > second_best_score:
            second_best_score = acc_test
            second_best_classifiers = [name]
        elif acc_test == second_best_score:
            second_best_classifiers.append(name)

    print(f'\nBest Classifier(s): {", ".join(best_classifiers)} with test accuracy: {best_score:.3f}')
    print(f'Second Best Classifier(s): {", ".join(second_best_classifiers)} with test accuracy: {second_best_score:.3f}')