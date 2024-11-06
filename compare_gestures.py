# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
#
#
# def get_regression(csvdata):
#     csvdata = csvdata.iloc[3:, :]
#
#     list_of_slopes = []
#     list_of_intercepts = []
#
#     for column_name in csvdata:
#         if column_name != "timestamp":
#             df = pd.DataFrame(csvdata, columns=['timestamp', column_name])
#
#             model = LinearRegression()
#             X = np.array(df['timestamp']).reshape(-1, 1)
#             y = np.array(df[column_name])
#             model.fit(X, y)
#
#             slope = model.coef_[0]
#             intercept = model.intercept_
#
#             list_of_slopes.append(slope)
#             list_of_intercepts.append(intercept)
#     return list_of_slopes, list_of_intercepts
#
#
# def compare_numbers(n1, n2, i1, i2):
#     sl = abs(n1 - n2)
#     if sl <= 0.05:
#         s = "Similar"
#     else:
#         s = "No"
#
#     inte = abs(i1 - i2)
#     if inte <= 0.1:
#         intee = "Similar"
#     else:
#         intee = "No"
#
#     return s, intee
#
#
# data = pd.read_csv("copy_of_Yes.csv")
# data = data.iloc[3:, :]
#
# print(data)
#
# slope, intercept = get_regression(data)
# # print(f"this is slope of dataset 1 : {slope}")
# # print(f"this is the incercepts of dataset 1 : {intercept}")
# # print("****************************")
#
# data2 = pd.read_csv("copy_of_Yes.csv")
# data2 = data2.iloc[3:, :]
#
# slope2, intercept2 = get_regression(data2)
# # print(f"this is slope of dataset 2 : {slope2}")
# # print(f"this is the incercepts of dataset 2 : {intercept2}")
#
# list_of_slope_compar = []
# list_of_intercept_compar = []
#
# for i in range(140):
#     reg1 = slope[i]
#     reg2 = slope2[i]
#     int1 = intercept[i]
#     int2 = intercept2[i]
#
#     slopeans, intans = compare_numbers(reg1, reg2, int1, int2)
#     list_of_slope_compar.append(slopeans)
#     list_of_intercept_compar.append(intans)
#
# print("**************************")
# print(f"slopes: {list_of_slope_compar}")
# print(f"intercepts: {list_of_intercept_compar}")
#
# countyes = 0
# countno = 0
#
#
# for i in range(140):
#     if list_of_slope_compar[i] == list_of_intercept_compar[i] == "Similar":
#         countyes += 1
#     else:
#         countno += 1
#
# print(f"count yes: {countyes}")
# print(f"count no: {countno}")
#
#
# if countyes > countno:
#     print("They are the same gesture")
# else:
#     print("They are NOT the same gesture")
#
#
#














# print("**************************")
# print(f"slopes: {list_of_slope_compar}")
# print(f"intercepts: {list_of_intercept_compar}")

# for index in list_of_slope_compar:
#     if index == "No":
#         countno +=1
#     elif index == "Similar":
#         countyes +=1
#
# print(f"count no: {countno}")
# print(f"count yes: {countyes}")

# print(f"{slope[50]}x + {intercept[50]}")
# print(f"{slope[60]}x + {intercept[60]}")
# print("****************************")
#
# print(f"{slope2[50]}x + {intercept2[50]}")
# print(f"{slope2[60]}x + {intercept2[60]}")
