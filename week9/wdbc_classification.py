# Importing necessary libraries for the implementation.
from sklearn.svm import SVC
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load the data using the provided function from the skeleton code.
class WDBCData:
    data = []
    target = []
    target_names = ['malignant', 'benign']
    feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 
                     'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 
                     'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 
                     'area error', 'smoothness error', 'compactness error', 'concavity error', 
                     'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 
                     'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 
                     'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']

def load_wdbc_data(filename):
    wdbc = WDBCData()
    with open(filename) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            wdbc.target.append(0 if items[1] == 'M' else 1)
            wdbc.data.append(list(map(float, items[2:])))
        wdbc.data = np.array(wdbc.data)
        wdbc.target = np.array(wdbc.target)
    return wdbc

# Loading the data from the provided file path.
data_file_path = 'C:/SPB_Data/20240314/week9/data/wdbc.data'
wdbc = load_wdbc_data(data_file_path)

# Define and train the SVM model
model = SVC(random_state=0)
model.fit(wdbc.data, wdbc.target)

# Predictions and accuracy calculation
predictions = model.predict(wdbc.data)
accuracy = balanced_accuracy_score(wdbc.target, predictions)

# Scatter plot visualization
cmap = np.array([(1, 0, 0), (0, 1, 0)])  # Red for malignant, green for benign
clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]

plt.figure()
plt.title(f'My Classifier (Accuracy: {accuracy:.3f})')
plt.scatter(wdbc.data[:, 0], wdbc.data[:, 1], c=cmap[wdbc.target], edgecolors=cmap[predictions])
plt.xlabel(wdbc.feature_names[0])
plt.ylabel(wdbc.feature_names[1])
plt.legend(handles=clabel, framealpha=0.5)
plt.savefig('./wdbc_classification_scatter.png')
plt.show()

# Confusion matrix visualization
conf_matrix = confusion_matrix(wdbc.target, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=wdbc.target_names)
disp.plot(cmap='viridis', colorbar=True)
plt.savefig('./wdbc_classification_matrix.png')
plt.show()
