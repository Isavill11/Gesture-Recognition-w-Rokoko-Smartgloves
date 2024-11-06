import pandas as pd
import time
import warnings
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
# alpha1 = pd.read_csv("alphabet_a_m.csv")
# alpha2 = pd.read_csv("alphabet_n_t.csv")
# alpha3 = pd.read_csv("alphabet_u_z.csv")
#
# all_alpha_df = pd.concat([alpha1, alpha2, alpha3])
# print(all_alpha_df['Gesture'].value_counts())
# all_alpha_df.to_csv("Left_alpha_database.csv", index=False)

df1 = pd.read_csv("slight_motion_var1.csv")
df2 = pd.read_csv("slight_motion_var2.csv")
df3 = pd.read_csv("slight_motion_var3.csv")
df4 = pd.read_csv("stationary_var_df4.csv")
df5 = pd.read_csv("slight_motion_var1.csv")

list = [df1, df2, df3, df4, df5]

for dataframe in list:
    maximum = dataframe.max()
    maximum.to_list()
    print(max(maximum))










