import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import warnings
warnings.simplefilter('ignore')

def pca_train(df):
   n_pc = len(df.columns)
   pca = PCA(n_components = n_pc)
   #pcs = pca.fit_transform(df.to_numpy())
   pcs = pca.fit(df.to_numpy())
   #return pd.DataFrame(pcs), pca
   return pca

### preparing and sorting data into testing and training datasets.

# df3 = pd.read_csv("Left_alpha_database.csv")

# df1 = pd.read_csv("combined_Isa_dataset.csv")
# df2 = pd.read_csv("Joshs_database.csv")
#
# for values in df2["Gesture"]:
#    if values == "Mom" or values == "Dad":
#       df2.drop(df2[df2["Gesture"] == values].index, inplace=True)
#
# original_dataset = pd.concat([df1, df2])

# df3 = df3.loc[:, ~df3.columns.str.contains('ring')]
original_dataset = pd.read_csv("Final_gestures_hopefully.csv")

original_dataset.dropna(inplace=True)
df = original_dataset
diff_labels = original_dataset["Gesture"].unique().tolist()

print(df.shape)
labels = df['Gesture']
features = df.drop(columns='Gesture', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.20, random_state=42, shuffle=True)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.5, random_state=42, shuffle=True)


### Principal component analysis

pca = pca_train(pd.DataFrame(X_train))
X_pca_train = pd.DataFrame(pd.DataFrame(pca.transform(X_train)))
X_pca_val = pd.DataFrame(pd.DataFrame(pca.transform(X_val)))
X_pca_test = pd.DataFrame(pd.DataFrame(pca.transform(X_test)))

X_train = X_pca_train
X_test = X_pca_test
X_val = X_pca_val


print(X_train.shape)
# check how the classes are distributed:
# cur = "Vinegar"
# for i in range(0, y_val.shape[0]):
#   if y_val.iloc[i] != cur:
#     cur = y_val.iloc[i]
#     # print(cur)

y_train_1 = pd.get_dummies(y_train)

