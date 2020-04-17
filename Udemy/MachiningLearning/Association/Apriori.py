import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from sklearn.preprocessing import StandardScaler

#Input dataset
data = pd.read_csv('Market_Basket_Optimisation.csv')
X = data.iloc[:,:-1].values
y = data.iloc[:,len(X[0])].values
#Splitting the dataset into the Training set and Test set

'''
#Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
'''
