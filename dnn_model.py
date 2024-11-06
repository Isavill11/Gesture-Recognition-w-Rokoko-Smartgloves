import pickle
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.simplefilter('ignore')

from prepare_data import X_train, X_test, X_val, y_train, y_test, y_val, diff_labels, y_train_1

### Model Creation:

model = Sequential()

model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.7))
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(len(diff_labels), activation= 'sigmoid'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, mode='max', restore_best_weights=True)
history = model.fit(X_train, pd.get_dummies(y_train), epochs=100, batch_size=128 ,validation_data=(X_val,  pd.get_dummies(y_val)),callbacks=[early_stopping])

y_pred = model.predict(X_test) #prediction
y_pred_classes = np.argmax(y_pred, axis=1)

class_labels = pd.get_dummies(y_test).columns #classificaton_report
classification_rep = classification_report(y_test, class_labels[y_pred_classes])
print("Classification Report:")
print(classification_rep)

loss, accuracy = model.evaluate(X_test, pd.get_dummies(y_test))

print("Loss:", loss)
print("Accuracy:", accuracy)

### Graphing confusion matrix and model accuracy chart

cm = confusion_matrix(y_test, class_labels[y_pred_classes])
plt.figure(figsize=(10, 10))
sns.heatmap(cm, annot=True, fmt='d',
            cmap='Reds',
            xticklabels=class_labels,
            yticklabels=class_labels)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Gesture Confusion Matrix")
plt.show()


cmn = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(cmn, annot=True, fmt='.0%',
            cmap='Reds',
            xticklabels=class_labels,
            yticklabels=class_labels)

plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title("Gesture Confusion Matrix")
plt.show()


rcParams['figure.figsize'] = 10, 4


plt.plot(history.history['accuracy']) #plot accuracy
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


# plt.plot(history.history['loss']) #plot loss
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'validation'], loc='upper left')
# plt.show()

labels = y_train_1.columns
joblib.dump(model, "improved_new_model.joblib")
with open('new_model_labels.pkl', 'wb') as f:
    pickle.dump(labels, f)

#Twelve Gesutre Accuracy 98.47%
#Josh Database Accuracy 100%
