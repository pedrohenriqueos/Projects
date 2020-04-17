import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
#from sklearn.preprocessing import StandardScaler

#Input dataset
data = pd.read_csv('50_Startups.csv')
X = data.iloc[:,:-1].values
y = data.iloc[:,len(X[0])].values

label_x = LabelEncoder()
X[:,3] = label_x.fit_transform(X[:,3])
transformer_X = ColumnTransformer(transformers=[("State",OneHotEncoder(),[3])], remainder='passthrough')
X = transformer_X.fit_transform(X)

X = X[:,1:]

#Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

'''
#Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
'''

regressor = LinearRegression()
regressor.fit(X_train,y_train)

y_pred = regressor.predict(X_test)
X = np.append(arr = np.ones((50,1)).astype(int),values = X,axis = 1)

#BackwardElimination
'''
#BackwardElimination levando em consideração a precisão R-squared
def BackwardElimination(x,SL):
	numVars = len(x[0])
	temp = np.zeros((50,6)).astype(int)
	for i in range(numVars):
		regressor_OLS = sm.OLS(y,x).fit()
		maxVar = max(regressor_OLS.pvalues).astype(float)
		adjR_before = regressor_OLS.rsquared_adj.astype(float)
		if maxVar > SL:
			for j in range(numVars-i):
				if regressor_OLS.pvalues[j].astype(float)==maxVar:
					temp[:,j] = x[:,j]
					x = np.delete(x,j,1)
					tmp_regressor = sm.OLS(y,x).fit()
					adjR_after = tmp_regressor.rsquared_adj.astype(float)
					if adjR_before>=adjR_after: #define a precisão para parar
						x_rollback = np.hstack((x,temp[:,[0,j]]))
						x_roolback = np.delete(x_rollback,j,1)
						print(regressor_OLS.summary())
						return x_rollback
	regressor_OLS.summary()
	return x
'''
'''
#BackwardElimination levando em consideração apenas p-value
def BackwardElimination(x,SL):
	numVars = len(x[0])
	for i in range(numVars):
		regressor_OLS = sm.OLS(y,x).fit()
		maxVar = max(regressor_OLS.pvalues).astype(float)
		if maxVar > SL:
			for j in range(numVars-i):
				if regressor_OLS.pvalues[j].astype(float)==maxVar:
					x = np.delete(x,j,1)
	regressor_OLS.summary()
	return x		
'''
SL = 0.05
X_opt = np.array(X[:,[0,1,2,3,4,5]],dtype = float)
X_Modeled = BackwardElimination(X_opt,SL)
regressor_OLS = sm.OLS(y,X_Modeled).fit()
print(regressor_OLS.summary())
'''
X_opt = np.array(X[:,[0,1,3,4,5]],dtype = float)
regressor_OLS = sm.OLS(y,X_opt).fit()
#print(regressor_OLS.summary())

X_opt = np.array(X[:,[0,3,4,5]],dtype = float)
regressor_OLS = sm.OLS(y,X_opt).fit()
#print(regressor_OLS.summary())

X_opt = np.array(X[:,[0,3,5]],dtype = float)
regressor_OLS = sm.OLS(y,X_opt).fit()
#print(regressor_OLS.summary())

X_opt = np.array(X[:,[0,3]],dtype = float)
regressor_OLS = sm.OLS(y,X_opt).fit()
print(regressor_OLS.summary())
'''
