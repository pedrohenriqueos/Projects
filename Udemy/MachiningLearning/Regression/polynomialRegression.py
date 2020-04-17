import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
#from sklearn.preprocessing import StandardScaler

#Input dataset
data = pd.read_csv('Position_Salaries.csv')
X = data.iloc[:,1:2].values
y = data.iloc[:,2].values


#Splitting the dataset into the Training set and Test set
#X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

'''
#Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
'''

lin_reg = LinearRegression()
lin_reg.fit(X,y)

print(lin_reg.predict([[6.5]]))


poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly,y)


X_grid = np.arange(min(X),max(X),0.1)
X_grid = X_grid.reshape((len(X_grid),1))
plt.scatter(X, y,color = 'r',s=15)
plt.plot(X_grid,lin_reg_2.predict(poly_reg.fit_transform(X_grid)),color = 'b')
plt.title('Polynomial Regression')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()

