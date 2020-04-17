import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from sklearn.impute import SimpleImputer as Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


data = pd.read_csv('Data.csv')
data = data.fillna(data.mean())# Essa linha substitui o comentário
X = data.iloc[:,:-1].values
y = data.iloc[:,len(X[0])].values
'''
imp = Imputer(missing_values=np.nan,strategy='mean')
imp = imp.fit(X[:,1:3])
X[:,1:3] = imp.transform(X[:,1:3])
'''
label_x = LabelEncoder()
X[:,0] = label_x.fit_transform(X[:,0])
transformer_X = ColumnTransformer(transformers=[("Country",OneHotEncoder(),[0])], remainder='passthrough')
X = transformer_X.fit_transform(X)
transformer_y = LabelEncoder()
y = transformer_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

print(X_train)

