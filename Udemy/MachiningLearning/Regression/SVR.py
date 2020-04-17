import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

#Input dataset
data = pd.read_csv('Position_Salaries.csv')
X = data.iloc[:,1:2].values
y = data.iloc[:,2].values


#Splitting the dataset into the Training set and Test set
#X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)


#Feature Scaling
sc_X = StandardScaler()
X = sc_X.fit_transform(X)
sc_y = StandardScaler()
y = sc_y.fit_transform(y.reshape(-1,1))

regressor = SVR(kernel = 'rbf')
regressor.fit(X,y)

y_pred = sc_y.inverse_transform(regressor.predict(sc_X.transform([[6.5]])))
print(y_pred)

plt.scatter(X, y,color = 'r',s=15)
plt.plot(X,regressor.predict(X),color = 'b')
plt.title('SVR')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

