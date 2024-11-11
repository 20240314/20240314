import numpy as np
from sklearn import (datasets, tree, model_selection)

if __name__ == '__main__':
    wdbc = datasets.load_breast_cancer()
    model = tree.DecisionTreeClassifier()
    cv_results = model_selection.cross_validate(model, wdbc.data, wdbc.target, cv=5, return_train_score=True)

    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    score = max(10 + 100 * (acc_test - 0.9), 0)

    print('Classifier: Decision Tree')
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {score:.0f}')
