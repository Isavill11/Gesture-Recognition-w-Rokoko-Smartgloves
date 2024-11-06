import json
import os
import socket
import pickle
import pandas as pd
from joblib import load
import numpy as np
import time
from sklearn.decomposition import PCA
from prepare_data import pca
from data_to_df import live_data_to_df
from collections import Counter

# # Suppress TensorFlow warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# # Disable oneDNN custom operations
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

mod = load("Final_database.joblib")
# labels = ['Before(past)', 'Cold', 'Dad', 'Day',
#           'Home', 'Hot', 'Mom', 'Night',
#           'Today(now)', 'Water', 'Will(Future)', 'Work']  #josh database labels

with open("Final_database_model.pkl", 'rb') as f:
    labels = pickle.load(f)

# labels = ['Before(past)', 'Class_Blue', 'Class_Cold', 'Class_Dad',
#        'Class_Day', 'Class_Doubt', 'Class_Drink', 'Class_Home', 'Class_Hot',
#        'Class_Mom', 'Class_Night', 'Class_No', 'Class_Please',
#        'Class_Thank You', 'Class_Today(now)', 'Class_Water', 'Class_Why',
#        'Class_Will(Future)', 'Class_Work', 'Class_Yes']


wait = input("PRESS TO START")
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

while True:

    df = live_data_to_df(100)
    new_data = df
    new_data_pca = pd.DataFrame(pd.DataFrame(pca.transform(new_data)))

    prediction = mod.predict(new_data_pca)
    # prediction = prediction / prediction.sum(axis=1, keepdims=True)
    prediction_indices = np.argmax(prediction, axis=1).tolist()
    prediction_class = np.array(labels)[prediction_indices]
    # print(prediction_class)
    counter = Counter(prediction_class)
    most_frequent_val = counter.most_common(1)[0][0]
    #
    print(most_frequent_val)

    # for values in prediction_class:
    #     if most_frequent_val is values:
    #         print(most_frequent_val)
    print("******")


    # words = np.unique(prediction_class).tolist()
    # pred_string = ''
    # for word in words:
    #     pred_string += word + ' '
    # print(pred_string)
    # print("Waiting...")
    # print("3")
    # time.sleep(.5)
    # print("2")
    # time.sleep(.5)
    # print("1")
    # time.sleep(.5)
