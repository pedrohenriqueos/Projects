import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler

#Input dataset
data = pd.read_csv('Position_Salaries.csv')
X = data.iloc[:,1:2].values
y = data.iloc[:,2].values


#Splitting the dataset into the Training set and Test set
#X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.8,random_state=42)

'''
#Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
'''

regressor = DecisionTreeRegressor(random_state = 42)
regressor.fit(X,y)


#X_grid = np.arange(min(X),max(X),0.1) #alter precision
#X_grid = X_grid.reshape((len(X_grid),1))

X_grid = np.arange(min(X),max(X),0.01) #alter precision
X_grid = X_grid.reshape((len(X_grid),1))
plt.scatter(X, y,color = 'r',s=15)
plt.plot(X_grid,regressor.predict(X_grid),color = 'b')
plt.title('Decidion Tree')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
