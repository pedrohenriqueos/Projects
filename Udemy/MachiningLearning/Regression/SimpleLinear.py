import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import metrics

#Input dataset
data = pd.read_csv('Salary_Data.csv')
X = data.iloc[:,:-1].values
y = data.iloc[:,len(X[0])].values
#Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=1/3,random_state=42)

'''
#Feature Scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
'''

lr = LinearRegression()
lr.fit(X_train,y_train)
predict = lr.predict(X_test)
'''
plt.scatter(X_train,y_train, color='r',s=10, label='Salary real')
plt.plot(X_train,lr.predict(X_train), color='b',label='Regression')
plt.title('Salary vs Experience (Training set)')
'''

plt.title('Salary vs Experience (Test set)')
plt.scatter(X_test,y_test, color='r',s=10, label='Salary real')
plt.plot(X_train,lr.predict(X_train), color='c',label='Regression')

plt.xlabel('Experience')
plt.ylabel('Salary')
plt.legend()
plt.show()
