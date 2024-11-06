import pandas as pd
import numpy as np
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix


warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (10, 10)

handdata = pd.read_csv ('Alphabet_database.csv')
handdata['Gesture'].value_counts()

#Class distribution.
handdata.dropna(axis=0, inplace=True)
handdata['Gesture'].value_counts()

# #copy og dataframe
hd = handdata.copy()

# label encoder
label_encoder = LabelEncoder()
hd['Gesture_Encoded'] = label_encoder.fit_transform(hd['Gesture'])
print(hd['Gesture_Encoded'].value_counts())
#select features
feature = hd.drop(['Gesture', 'Gesture_Encoded'], axis=1)

# select target
target = hd['Gesture_Encoded']

#train_test_split
X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=0.2, random_state=42)

# print("Shape of X_train:", X_train.shape)
# print("Shape of X_test:", X_test.shape)
# print("Shape of y_train:", y_train.shape)
# print("Shape of y_test:", y_test.shape)

#Build the model:

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

#Evaluate model
accuracy = clf.score(X_test, y_test)
print("Accuracy:", accuracy)

pred_prob = clf.predict_proba(X_test)
# print(f"Predicted probabilities: {pred_prob}")
# for values in pred_prob:
  # print(values)


y_pred = clf.predict(X_test)
# y_pred_classes = np.argmax(y_pred)
# print(y_pred_classes)

class_labels = clf.classes_

cm = confusion_matrix(y_test, y_pred, labels=class_labels)

plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True,
            fmt='d',
            cmap='Greens',
            xticklabels=class_labels,
            yticklabels=class_labels)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

cmn = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])
fig, ax = plt.subplots(figsize=(8,8))
sns.heatmap(cmn, annot=True, fmt='.0%',
            cmap='Greens',
            xticklabels=class_labels,
            yticklabels=class_labels)

plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title("Confusion Matrix")
plt.show()

joblib.dump(clf, 'rand_forest_model.joblib')

labels = class_labels
joblib.dump(clf, "rfc_alpha_model.joblib")
with open('rfc_labels.pkl', 'wb') as f:
    pickle.dump(labels, f)